"""
Parte B — Atenção -> conceito (evidência interpretável, ilustrativa).

Usa os modelos Code-DKT re-treinados (results/codedkt_kc_retrained.pkl) para
extrair, nos eventos de ERRO do test set dos 5 assignments, os paths AST de
maior peso de atenção. Agrega por (problema, token saliente) e mapeia cada
problema aos seus conceitos (Q-matrix), produzindo exemplos ilustrativos do
"que o modelo olha" quando prevê falha em cada KC / dificuldade de Martins.

Saídas:
  results/codedkt_attention_by_concept.csv   (todos os paths salientes por conceito)
  results/codedkt_attention_examples.json    (1 exemplo forte por conceito + por Martins)
"""
from __future__ import annotations
import json, pickle, warnings
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

warnings.filterwarnings("ignore")
from src.models.code_dkt import CodeDKTModel
from src.code_features import build_code_input_tensor

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
AIDS = [439, 487, 492, 494, 502]

MARTINS = {
    "Estruturas de controle":          ["branching_condicional", "iteracao_indexada", "retorno_antecipado"],
    "Manipulação de variáveis":        ["padrao_acumulador", "inicializacao_variaveis", "estado_com_indices"],
    "Operadores e expressões lógicas": ["logica_booleana_composta", "negacao_booleana", "comparacao_numerica"],
    "Funções":                         ["metodos_auxiliares", "tipos_retorno", "parametros_metodo"],
    "Vetores":                         ["manipulacao_array", "bounds_checking", "dual_pointer"],
    "Conhecimento matemático":         ["operador_modulo", "aritmetica_condicional"],
}


def concept_map(aid, tr):
    qm = pd.read_csv(RES / f"qmatrix_A{aid}.csv").set_index("ProblemID")
    desc = {d["kc_id"]: d["name"] for d in json.load(open(RES / f"kc_descriptions_A{aid}.json"))}
    out = {}
    for pid in qm.index:
        out[pid] = {tr["translations"].get(desc[int(c.split("_")[1])], {}).get("concept_id")
                    for c in qm.columns if qm.loc[pid, c] == 1}
        out[pid].discard(None)
    return out


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    retr = pickle.load(open(RES / "codedkt_kc_retrained.pkl", "rb"))
    seqs = pickle.load(open(RES / "sequences_code_dkt.pkl", "rb"))
    cache = pickle.load(open(RES / "code_features_cache.pkl", "rb"))
    tr = json.load(open(RES / "kc_translations.json"))

    rows = []  # cid, aid, problem, start, end, path, avg_attn, n_err_events, freq
    for aid in AIDS:
        r = retr[aid]; vocab = r["vocab"]; p2i = r["problem_to_idx"]; cfg = r["config"]
        M, maxlen, R = len(p2i), cfg["max_len"], cfg["R"]
        model = CodeDKTModel(2 * M, cfg["hidden_dim"], M, vocab["node_count"], vocab["path_count"],
                             1, cfg.get("dropout", 0.0), R).to(device)
        model.load_state_dict(r["state_dict"]); model.eval()
        pc = concept_map(aid, tr)
        i2tok = {v: k for k, v in vocab["token_to_idx"].items()}; i2tok[0] = "<PAD/UNK>"
        i2path = {v: k for k, v in vocab["path_to_idx"].items()}; i2path[0] = "<PAD/UNK>"

        X, _, _ = build_code_input_tensor(seqs["test"][aid], cache, vocab["token_to_idx"],
                                          vocab["path_to_idx"], p2i, max_len=maxlen, R=R)
        B, L, _ = X.shape; idim = 2 * M
        with torch.no_grad():
            x = X.to(device)
            c2v = x[:, :, idim:].reshape(B, L, R, 3).long()
            se = model.embed_nodes(c2v[:, :, :, 0]); pe = model.embed_paths(c2v[:, :, :, 1])
            ee = model.embed_nodes(c2v[:, :, :, 2])
            rep = x[:, :, :idim].unsqueeze(2).expand(-1, -1, R, -1)
            full = torch.cat([se, ee, pe, rep], dim=3)
            trans = torch.tanh(model.path_transformation_layer(full))
            attn = F.softmax(model.attention_layer(trans), dim=2).squeeze(-1).cpu().numpy()
        c2v_np = c2v.cpu().numpy()

        # agrega top-5 paths por (problema, outcome=erro) sobre eventos de erro
        agg = defaultdict(lambda: defaultdict(lambda: {"w": 0.0, "n": 0}))  # pid -> path_key -> stats
        nerr = defaultdict(int)
        for i, seq in enumerate(seqs["test"][aid]):
            ev = seq["events"]
            if len(ev) > maxlen:
                ev = ev.iloc[-maxlen:]
            Lr = len(ev); pad = maxlen - Lr
            for t in range(1, Lr):
                row = ev.iloc[t]
                if int(row["correct"]) != 0:   # só eventos de ERRO
                    continue
                pid = int(row["ProblemID"]); tprev = pad + t - 1
                nerr[pid] += 1
                a_step = attn[i, tprev]; ind = c2v_np[i, tprev]
                for rk in np.argsort(-a_step)[:5]:
                    s = i2tok.get(int(ind[rk, 0]), "?"); p = i2path.get(int(ind[rk, 1]), "?")
                    e = i2tok.get(int(ind[rk, 2]), "?")
                    if s == "<PAD/UNK>" and e == "<PAD/UNK>":
                        continue
                    k = (s, e, p)
                    agg[pid][k]["w"] += float(a_step[rk]); agg[pid][k]["n"] += 1

        for pid, paths in agg.items():
            for (s, e, p), st in paths.items():
                for cid in pc.get(pid, ()):
                    rows.append({"cid": cid, "concept": tr["concepts"][cid]["pt"], "aid": aid,
                                 "problem": pid, "start": s, "end": e,
                                 "avg_attn": round(st["w"] / st["n"], 4), "freq": st["n"],
                                 "n_err_events": nerr[pid],
                                 "path": p if len(p) <= 80 else p[:77] + "..."})

    df = pd.DataFrame(rows)
    # filtra paths frequentes e salientes
    df = df[(df.freq >= 5)].sort_values(["cid", "avg_attn"], ascending=[True, False])
    df.to_csv(RES / "codedkt_attention_by_concept.csv", index=False)

    # exemplo mais forte por conceito (maior avg_attn com token informativo)
    def informative(rw):
        toks = {rw["start"], rw["end"]}
        return not toks <= {"<PAD/UNK>", "?"}
    ex_by_concept = {}
    for cid, g in df[df.apply(informative, axis=1)].groupby("cid"):
        top = g.sort_values("avg_attn", ascending=False).iloc[0]
        ex_by_concept[cid] = {"concept": top["concept"], "aid": int(top["aid"]),
                              "problem": int(top["problem"]),
                              "start": top["start"], "end": top["end"],
                              "avg_attn": float(top["avg_attn"]), "freq": int(top["freq"])}
    # 1 exemplo por sub-dificuldade de Martins (conceito com maior avg_attn disponível)
    ex_by_martins = {}
    for grp, cids in MARTINS.items():
        cand = [ex_by_concept[c] for c in cids if c in ex_by_concept]
        if cand:
            best = max(cand, key=lambda d: d["avg_attn"])
            ex_by_martins[grp] = best
    json.dump({"by_concept": ex_by_concept, "by_martins": ex_by_martins},
              open(RES / "codedkt_attention_examples.json", "w"), ensure_ascii=False, indent=2)

    print("=== Exemplo de path saliente (erro) por sub-dificuldade de Martins ===")
    for grp, ex in ex_by_martins.items():
        print(f"  {grp:34s} [{ex['concept'][:30]:30s}] A{ex['aid']} P{ex['problem']}: "
              f"{ex['start']} -> {ex['end']}  (attn={ex['avg_attn']:.3f}, freq={ex['freq']})")
    print(f"\nCSV ({len(df)} linhas) + JSON salvos em results/.")


if __name__ == "__main__":
    main()
