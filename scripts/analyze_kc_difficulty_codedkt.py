"""
Parte A — Dificuldade de aprendizado por KC semântico, medida pelo Code-DKT.

Re-treina o Code-DKT nas sequências atuais (consistência modelo<->dados),
mede a curva de aprendizado prevista por conceito (oportunidade = n-ésimo
problema DISTINTO do KC, primeiras tentativas, padrão AFM/PFA), extrai
inclinação (linear + AFM-logit) e nível (pred@1, pred@last), e agrega por
sub-dificuldade de Martins, Marin e Alves (2024).

Saídas:
  results/codedkt_kc_retrained.pkl     (state_dicts re-treinados, p/ Parte B)
  results/codedkt_kc_difficulty.json   (todos os números)
  results/fig_codedkt_kc_curves.png
  results/fig_codedkt_difficulty_martins.png
  results/fig_codedkt_level_vs_slope.png
"""
from __future__ import annotations
import io, json, pickle, warnings, contextlib
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
from src.models.code_dkt import CodeDKTModel, train_code_dkt
from src.code_features import build_code_input_tensor
from src.evaluation import compute_auc

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
AIDS = [439, 487, 492, 494, 502]
SEED = 42
MIN_N = 20          # mínimo de observações por ponto da curva
MAX_OPP = 6         # nº máximo de oportunidades (problemas distintos por KC)

# Mapa: sub-dificuldade de Martins (slide) -> concept_ids do KCGen-KT
MARTINS = {
    "Estruturas de controle":          ["branching_condicional", "iteracao_indexada", "retorno_antecipado"],
    "Manipulação de variáveis":        ["padrao_acumulador", "inicializacao_variaveis", "estado_com_indices"],
    "Operadores e expressões lógicas": ["logica_booleana_composta", "negacao_booleana", "comparacao_numerica"],
    "Funções":                         ["metodos_auxiliares", "tipos_retorno", "parametros_metodo"],
    "Vetores":                         ["manipulacao_array", "bounds_checking", "dual_pointer"],
    "Conhecimento matemático":         ["operador_modulo", "aritmetica_condicional"],
}


def concept_map(aid: int, tr: dict) -> dict[int, set]:
    qm = pd.read_csv(RES / f"qmatrix_A{aid}.csv").set_index("ProblemID")
    desc = {d["kc_id"]: d["name"] for d in json.load(open(RES / f"kc_descriptions_A{aid}.json"))}
    out = {}
    for pid in qm.index:
        s = set()
        for col in qm.columns:
            if qm.loc[pid, col] == 1:
                cid = tr["translations"].get(desc[int(col.split("_")[1])], {}).get("concept_id")
                if cid:
                    s.add(cid)
        out[pid] = s
    return out


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    saved = pickle.load(open(RES / "code_dkt_results.pkl", "rb"))
    seqs = pickle.load(open(RES / "sequences_code_dkt.pkl", "rb"))
    cache = pickle.load(open(RES / "code_features_cache.pkl", "rb"))
    tr = json.load(open(RES / "kc_translations.json"))

    retrained = {}
    records = []  # (aid, cid, opp, pred, correct)
    auc_report = {}

    for aid in AIDS:
        vocab = saved[aid]["vocab"]
        p2i = saved[aid]["problem_to_idx"]
        cfg = saved[aid]["config"]
        M, maxlen, R = len(p2i), cfg["max_len"], cfg["R"]

        # ---- re-treino (stdout das épocas suprimido) ----
        torch.manual_seed(SEED); np.random.seed(SEED)
        if device.type == "cuda":
            torch.cuda.manual_seed_all(SEED)
        with contextlib.redirect_stdout(io.StringIO()):
            model = train_code_dkt(seqs["train"][aid], p2i, vocab, cfg, cache, seed=SEED)
        model.eval()

        # ---- predição alinhada (forward completo no test) ----
        with torch.no_grad():
            X, _, _ = build_code_input_tensor(
                seqs["test"][aid], cache, vocab["token_to_idx"], vocab["path_to_idx"],
                p2i, max_len=maxlen, R=R)
            yp = model(X.to(device)).cpu().numpy()

        # AUC de sanidade (re-treinado)
        pdf_rows = []
        pc = concept_map(aid, tr)
        for i, seq in enumerate(seqs["test"][aid]):
            ev = seq["events"]
            if len(ev) > maxlen:
                ev = ev.iloc[-maxlen:]
            L = len(ev); start = maxlen - L
            seen = defaultdict(set)
            for t in range(L):
                row = ev.iloc[t]; pid = int(row["ProblemID"])
                pred = float(yp[i, start + t - 1, p2i[pid]]) if t >= 1 else None
                if t >= 1:
                    pdf_rows.append({"skill_name": str(pid), "correct": int(row["correct"]),
                                     "is_first_attempt": bool(row["is_first_attempt"]),
                                     "correct_predictions": pred})
                # oportunidade = n-ésimo problema DISTINTO do KC (só 1ª tentativa)
                if bool(row["is_first_attempt"]):
                    for cid in pc.get(pid, ()):
                        seen[cid].add(pid)
                        if t >= 1:
                            records.append((aid, cid, len(seen[cid]), pred, int(row["correct"])))
        pdf = pd.DataFrame(pdf_rows)
        auc_report[aid] = {"first_auc": round(compute_auc(pdf, True), 4),
                           "all_auc": round(compute_auc(pdf, False), 4),
                           "saved_first_auc": round(saved[aid]["first_auc"], 4)}
        retrained[aid] = {"state_dict": {k: v.cpu() for k, v in model.state_dict().items()},
                          "vocab": vocab, "problem_to_idx": p2i, "config": cfg}
        print(f"A{aid}: first_auc re-treino={auc_report[aid]['first_auc']} "
              f"(salvo {auc_report[aid]['saved_first_auc']}) | all={auc_report[aid]['all_auc']}")

    pickle.dump(retrained, open(RES / "codedkt_kc_retrained.pkl", "wb"))

    # ---- curvas por conceito ----
    df = pd.DataFrame(records, columns=["aid", "cid", "opp", "pred", "correct"])
    curves = {}
    for cid, g in df.groupby("cid"):
        pts = []
        for n in range(1, MAX_OPP + 1):
            sub = g[g.opp == n]
            if len(sub) >= MIN_N:
                pts.append((n, float(sub.pred.mean()), float(sub.correct.mean()), int(len(sub))))
        if len(pts) < 3:
            continue
        ns = np.array([p[0] for p in pts], float)
        ps = np.array([p[1] for p in pts], float)
        b_lin, a_lin = np.polyfit(ns, ps, 1)
        r2_lin = 1 - ((ps - (a_lin + b_lin * ns)) ** 2).sum() / (((ps - ps.mean()) ** 2).sum() + 1e-9)
        logit = np.log(np.clip(ps, .01, .99) / (1 - np.clip(ps, .01, .99)))
        b_afm, a_afm = np.polyfit(ns, logit, 1)
        r2_afm = 1 - ((logit - (a_afm + b_afm * ns)) ** 2).sum() / (((logit - logit.mean()) ** 2).sum() + 1e-9)
        curves[cid] = {
            "pt": tr["concepts"][cid]["pt"], "points": pts,
            "pred_at_1": round(ps[0], 4), "pred_at_last": round(ps[-1], 4),
            "slope_lin": round(float(b_lin), 4), "r2_lin": round(float(r2_lin), 3),
            "slope_afm": round(float(b_afm), 4), "r2_afm": round(float(r2_afm), 3),
            "n_total": int(len(g)),
        }

    # ---- agregação por Martins ----
    by_martins = {}
    for grp, cids in MARTINS.items():
        sl = [curves[c]["slope_lin"] for c in cids if c in curves]
        lv = [curves[c]["pred_at_1"] for c in cids if c in curves]
        af = [curves[c]["slope_afm"] for c in cids if c in curves]
        present = [curves[c]["pt"] for c in cids if c in curves]
        if not sl:
            continue
        by_martins[grp] = {"mean_slope_lin": round(float(np.mean(sl)), 4),
                           "mean_slope_afm": round(float(np.mean(af)), 4),
                           "mean_level_at_1": round(float(np.mean(lv)), 4),
                           "n_concepts": len(sl), "concepts": present}

    json.dump({"auc": auc_report, "curves": curves, "by_martins": by_martins,
               "params": {"min_n": MIN_N, "max_opp": MAX_OPP, "seed": SEED}},
              open(RES / "codedkt_kc_difficulty.json", "w"), ensure_ascii=False, indent=2)

    _figures(curves, by_martins)
    print("\nOK. JSON + 3 figuras salvos em results/.")


def _figures(curves, by_martins):
    BLUE, RED = "#2667FF", "#d64550"
    items = sorted(curves.items(), key=lambda kv: kv[1]["slope_lin"])

    # Fig 1: small multiples
    n = len(items); cols = 4; rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 3.0 * rows))
    axes = np.array(axes).reshape(-1)
    for ax, (cid, c) in zip(axes, items):
        ns = [p[0] for p in c["points"]]; ps = [p[1] for p in c["points"]]
        ax.scatter(ns, ps, color=BLUE, s=28, zorder=3)
        xs = np.array([min(ns), max(ns)])
        b, a = np.polyfit(ns, ps, 1)
        ax.plot(xs, a + b * xs, color=RED, lw=1.6)
        ax.set_title(f"{c['pt']}\nincl={c['slope_lin']:+.3f}  R²={c['r2_lin']:.2f}", fontsize=8.5)
        ax.set_ylim(0.15, 0.7); ax.set_xlabel("oportunidade (problema distinto)", fontsize=7)
        ax.tick_params(labelsize=7); ax.grid(alpha=.25)
    for ax in axes[len(items):]:
        ax.axis("off")
    fig.suptitle("Curva de aprendizado prevista pelo Code-DKT por KC (mastery prevista vs prática)",
                 fontsize=12, y=1.005)
    fig.tight_layout()
    fig.savefig(RES / "fig_codedkt_kc_curves.png", dpi=130, bbox_inches="tight")
    plt.close(fig)

    # Fig 2: barra de inclinação por sub-dificuldade de Martins (menor = mais difícil de aprender)
    gm = sorted(by_martins.items(), key=lambda kv: kv[1]["mean_slope_lin"])
    labels = [g for g, _ in gm]
    slopes = [v["mean_slope_lin"] for _, v in gm]
    levels = [v["mean_level_at_1"] for _, v in gm]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ypos = np.arange(len(labels))
    bars = ax.barh(ypos, slopes, color=BLUE, alpha=.85)
    ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("inclinação média da curva de aprendizado (menor = aprende mais devagar)")
    ax.set_title("Dificuldade de aprendizado (Code-DKT) por dificuldade de Martins et al. (2024)", fontsize=11)
    for i, (b, lv) in enumerate(zip(slopes, levels)):
        ax.text(b + 0.0008, i, f"incl={b:+.3f} · nível@1={lv:.2f}", va="center", fontsize=8.5, color="#333")
    ax.grid(axis="x", alpha=.25); ax.margins(x=0.18)
    fig.tight_layout()
    fig.savefig(RES / "fig_codedkt_difficulty_martins.png", dpi=130, bbox_inches="tight")
    plt.close(fig)

    # Fig 3: scatter nível@1 vs inclinação por conceito
    fig, ax = plt.subplots(figsize=(11, 6.5))
    cid2grp = {c: g for g, cs in MARTINS.items() for c in cs}
    palette = {g: col for g, col in zip(MARTINS, plt.cm.tab10.colors)}
    for cid, c in curves.items():
        grp = cid2grp.get(cid, "outros")
        col = palette.get(grp, "#888")
        ax.scatter(c["pred_at_1"], c["slope_lin"], color=col, s=55, zorder=3,
                   edgecolor="white", linewidth=.6)
        ax.annotate(c["pt"], (c["pred_at_1"], c["slope_lin"]), fontsize=7,
                    xytext=(4, 3), textcoords="offset points")
    ax.axhline(np.median([c["slope_lin"] for c in curves.values()]), color="#aaa", ls="--", lw=.8)
    ax.axvline(np.median([c["pred_at_1"] for c in curves.values()]), color="#aaa", ls="--", lw=.8)
    ax.set_xlabel("nível inicial: mastery prevista na 1ª oportunidade (menor = mais difícil de cara)")
    ax.set_ylabel("inclinação: velocidade de aprendizado (menor = aprende devagar)")
    ax.set_title("KCs por nível inicial × velocidade de aprendizado (Code-DKT)", fontsize=11)
    handles = [plt.Line2D([0], [0], marker="o", ls="", color=palette[g], label=g) for g in MARTINS]
    ax.legend(handles=handles, fontsize=8, loc="best", title="dificuldade de Martins")
    ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(RES / "fig_codedkt_level_vs_slope.png", dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
