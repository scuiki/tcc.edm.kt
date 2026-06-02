"""Curvas de aprendizado PREVISTAS pelo Code-DKT por dificuldade de Martins,
narradas por dificuldade: legenda anota o nível inicial (nível@1, menor = mais
difícil) em vez da inclinação. Fundo transparente, sem título embutido."""
import json
import shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica Neue", "DejaVu Sans"]

RES = Path("results")
proj = json.load(open(RES / "codedkt_kc_difficulty.json"))["curves"]
cpt = json.load(open(RES / "kc_translations.json"))["concepts"]

MARTINS = {
    "Estrutura de controle":               ["branching_condicional", "iteracao_indexada", "retorno_antecipado"],
    "Manipulação de variáveis":            ["padrao_acumulador", "inicializacao_variaveis", "estado_com_indices"],
    "Operadores e expressões booleanas":   ["logica_booleana_composta", "negacao_booleana", "comparacao_numerica"],
}
PAL = dict(zip(MARTINS, plt.cm.tab10.colors))

grp = {}
for g, cids in MARTINS.items():
    xs, ys, p1 = [], [], []
    nconc = 0
    for cid in cids:
        if cid in proj and proj[cid].get("pred_at_1") is not None:
            nconc += 1
            p1.append(proj[cid]["pred_at_1"])
            for opp, pred, _, _ in proj[cid]["points"]:
                xs.append(opp); ys.append(pred)
    if xs:
        b, a = np.polyfit(np.array(xs, float), np.array(ys, float), 1)
        grp[g] = {"xs": xs, "ys": ys, "slope": float(b), "intercept": float(a),
                  "nivel1": float(np.mean(p1)), "nconc": nconc}

# ordenar legenda por dificuldade: menor nível@1 (mais difícil) primeiro
order = sorted(grp, key=lambda g: grp[g]["nivel1"])
fig, ax = plt.subplots(figsize=(11.5, 6.2))
fig.patch.set_alpha(0.0); ax.patch.set_alpha(0.0)
xline = np.array([1, 6], float)
for g in order:
    d = grp[g]; col = PAL[g]; fragile = d["nconc"] == 1
    ax.scatter(d["xs"], d["ys"], color=col, alpha=.40, s=30, zorder=3)
    lbl = f"{g}  (nível@1={d['nivel1']:.2f}{', 1 conceito' if fragile else ''})"
    ax.plot(xline, d["intercept"] + d["slope"] * xline, color=col, lw=2.6,
            ls="--" if fragile else "-", label=lbl, zorder=4)
ax.set_xlabel("oportunidade  (n-ésimo problema distinto do KC, primeiras tentativas)", fontsize=17, fontweight="bold")
ax.set_ylabel("mastery prevista pelo Code-DKT", fontsize=17, fontweight="bold")
ax.set_xticks(range(1, 7))
ax.tick_params(axis="both", labelsize=15)
ax.grid(alpha=.25)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for lbl in ax.get_xticklabels() + ax.get_yticklabels():
    lbl.set_fontweight("bold")
leg = ax.legend(title="dificuldade de Martins, Marin e Alves (2024)  ·  menor nível@1 = mais difícil",
                fontsize=15, title_fontsize=13, loc="upper left", framealpha=0.0)
fig.tight_layout()
out = RES / "fig_martins_curves_predicted.png"
fig.savefig(out, dpi=140, bbox_inches="tight", transparent=True)
out_assets = Path("apresentacao") / "assets" / "fig-martins-curves-predita.png"
out_assets.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(out, out_assets)
print("salvo (transparente):", out)
print("copiado para assets:", out_assets)
for g in order:
    print(f"  {g:35} nível@1={grp[g]['nivel1']:.2f} incl={grp[g]['slope']:+.3f} ({grp[g]['nconc']} conc)")
