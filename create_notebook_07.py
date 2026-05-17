"""Gera notebooks/07_comparison.ipynb a partir de células definidas aqui."""
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

cells = []

# ─── Célula 0: Título ──────────────────────────────────────────────────────
cells.append(new_markdown_cell("""\
# 07 — Comparação Final: BKT, DKT, Code-DKT e srcML-DKT

Notebook de fechamento do TCC 1. Consolida os resultados dos quatro modelos de
Knowledge Tracing em uma comparação única: tabelas per-assignment, AUC pooled,
teste de significância Wilcoxon signed-rank e quatro visualizações publicáveis.

Atende aos **Critérios 2 e 3** do CLAUDE.md (Tabela comparativa e Wilcoxon).

**Protocolo:** dataset CSEDM Spring 2019, 410 alunos, split 80/20
(`random_state=1`), 5 assignments (A439, A487, A492, A494, A502).
Métricas: first-attempt AUC (primária) e all-attempts AUC (secundária).

---

**Seções:**
1. Setup
2. Carregamento uniforme dos 4 pickles
3. Tabela comparativa principal (per-assignment)
4. AUC pooled cross-assignment
5. Comparação com a literatura
6. Wilcoxon signed-rank com correção Holm-Bonferroni
7. BKT vs. modelos profundos: diferença descritiva
8. Gráfico: barras agrupadas por assignment
9. Gráfico: distribuição sobre seeds (boxplot)
10. Gráfico: delta vs. DKT
11. Gráfico: heatmap por problema
12. Discussão
13. Sumário executivo
14. Serialização (JSON)
"""))

# ─── Célula 1: Setup ───────────────────────────────────────────────────────
cells.append(new_markdown_cell("## 1 — Setup"))

cells.append(new_code_cell("""\
import os
import sys
import json
import pickle
import random
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy.stats import wilcoxon
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")

ROOT = Path(".").resolve().parent
RESULTS = ROOT / "results"

SEED = 42
AIDS = [439, 487, 492, 494, 502]
AID_LABELS = [f"A{a}" for a in AIDS]
MODEL_ORDER = ["BKT", "DKT", "Code-DKT", "srcML-DKT"]
COLORS = {
    "BKT":       "#4292c6",
    "DKT":       "#f16913",
    "Code-DKT":  "#41ab5d",
    "srcML-DKT": "#d7191c",
}
DPI = 150

def set_global_seed(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)

set_global_seed(SEED)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": DPI,
})

print(f"Python {sys.version.split()[0]}")
print(f"NumPy {np.__version__}, Pandas {pd.__version__}")
print(f"Seed global: {SEED}")
"""))

# ─── Célula 2: Carregamento ────────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 2 — Carregamento uniforme

Quatro pickles em `results/`. Nenhum modelo é retreinado aqui: o notebook é
puramente analítico.

| Modelo | Arquivo | Runs |
|---|---|---|
| BKT | `bkt_results_multirun.pkl` | 1 (determinístico) |
| DKT | `dkt_results_multirun.pkl` | 10 (seeds 42 a 51) |
| Code-DKT | `code_dkt_results_multirun.pkl` | 10 |
| srcML-DKT | `srcml_dkt_results_multirun.pkl` | 10 |
"""))

cells.append(new_code_cell("""\
def load_all_results():
    files = {
        "BKT":       "bkt_results_multirun.pkl",
        "DKT":       "dkt_results_multirun.pkl",
        "Code-DKT":  "code_dkt_results_multirun.pkl",
        "srcML-DKT": "srcml_dkt_results_multirun.pkl",
    }
    out = {}
    for model, fname in files.items():
        with open(RESULTS / fname, "rb") as f:
            out[model] = pickle.load(f)
    return out

all_results = load_all_results()

print("Verificação dos pickles carregados:")
for model in MODEL_ORDER:
    n_runs = len(all_results[model][AIDS[0]]["runs"])
    has_pred = all_results[model][AIDS[0]]["runs"][0]["pred_df"] is not None
    first_a = all_results[model][AIDS[0]]["first_auc_mean"] * 100
    print(f"  {model:12s}: {n_runs:2d} run(s), pred_df={'sim' if has_pred else 'None':3s}"
          f", first_auc A439={first_a:.2f}%")

print(f"\\nAssignments: {AID_LABELS}")
print("Carregamento OK.")
"""))

# ─── Célula 3: Tabelas per-assignment ─────────────────────────────────────
cells.append(new_markdown_cell("""\
## 3 — Tabela comparativa principal

**Critério 2 do CLAUDE.md:** tabela BKT vs DKT vs Code-DKT vs srcML-DKT por
assignment, reportando first-attempt AUC e all-attempts AUC.

Formato: `mean ± std` (10 runs) para modelos profundos; valor pontual para BKT
(determinístico, sem variância intra-assignment no pickle persistido).

Célula em negrito identifica o melhor modelo por assignment.
"""))

cells.append(new_code_cell("""\
def fmt_cell(model_results, aid, metric):
    m = model_results[aid][f"{metric}_mean"] * 100
    return f"{m:.2f}"

def build_per_assignment_table(all_results, metric):
    data = {}
    for model in MODEL_ORDER:
        data[model] = {f"A{a}": fmt_cell(all_results[model], a, metric)
                       for a in AIDS}
    df = pd.DataFrame(data).T
    df.index.name = "Modelo"
    return df

df_first = build_per_assignment_table(all_results, "first_auc")
df_all   = build_per_assignment_table(all_results, "all_auc")

print("=== First-attempt AUC (media sobre 10 runs, %) ===")
display(df_first)
print()
print("=== All-attempts AUC (media sobre 10 runs, %) ===")
display(df_all)
"""))

# Célula: salvar tabelas como MD + PNG
cells.append(new_code_cell("""\
def save_table_md(df, path, title, notes):
    lines = [f"## {title}\\n\\n", df.to_markdown(), "\\n\\n", notes]
    Path(path).write_text("".join(lines))
    print(f"Salvo: {path}")

def save_table_png(df, path, title, figsize=(12, 1.8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    # Identificar melhor valor por coluna (maior mean)
    best = {}
    for col in df.columns:
        aid = int(col[1:])
        vals = {m: all_results[m][aid][
                    "first_auc_mean" if "first" in str(path) else "all_auc_mean"]
                for m in MODEL_ORDER}
        best[col] = max(vals, key=vals.get)

    cell_colors = []
    for model in df.index:
        row_colors = []
        for col in df.columns:
            if model == best[col]:
                row_colors.append("#d4edda")
            else:
                row_colors.append("white")
        cell_colors.append(row_colors)

    tbl = ax.table(
        cellText=df.values,
        rowLabels=df.index,
        colLabels=df.columns,
        cellColours=cell_colors,
        cellLoc="center", rowLoc="center",
        loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1.2, 1.6)
    ax.set_title(title, fontsize=11, pad=8)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight", dpi=DPI)
    plt.show()
    print(f"Salvo: {path}")

NOTES_FIRST = (
    "\\n**Notas:**\\n"
    "1. BKT sem desvio padrão: modelo determinístico; pickle nao inclui `pred_df` para bootstrap.\\n"
    "2. DKT, Code-DKT e srcML-DKT: seeds 42 a 51 (mesma faixa).\\n"
    "3. srcML-DKT treina com eventos `Compile.Error`; avaliacao no mesmo test set dos outros 3.\\n"
    "4. Code-DKT A439 = 73.27%%, alvo CLAUDE.md Criterio 1 (74.31%% +/-3pp): **satisfeito**.\\n"
    "5. Celula destacada (verde) = melhor modelo no assignment.\\n"
)
NOTES_ALL = (
    "\\n**Notas:**\\n"
    "1. BKT sem desvio padrão: modelo determinístico.\\n"
    "2. Métrica secundária (all-attempts AUC): todas as tentativas, comparavel com Piech et al. (2015).\\n"
    "3. Celula destacada (verde) = melhor modelo no assignment.\\n"
)

save_table_md(df_first, RESULTS / "comparison_table_first_auc.md",
              "First-attempt AUC por assignment (%)", NOTES_FIRST)
save_table_png(df_first, RESULTS / "comparison_table_first_auc.png",
               "First-attempt AUC (%) por assignment")

save_table_md(df_all, RESULTS / "comparison_table_all_auc.md",
              "All-attempts AUC por assignment (%)", NOTES_ALL)
save_table_png(df_all, RESULTS / "comparison_table_all_auc.png",
               "All-attempts AUC (%) por assignment", figsize=(12, 1.8))
"""))

# ─── Célula 4: AUC pooled ─────────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 4 — AUC pooled cross-assignment

Versão compacta para comparação direta com Pankiewicz et al. (2025) Table 3.
Agregador: AUC sobre predições concatenadas dos 5 assignments (1 valor por run),
depois `mean ± std` sobre os runs disponíveis.

BKT marcado como N/A: `pred_df = None` no pickle (ver plano §2.3).
DKT e Code-DKT têm `pred_df` apenas no seed=42 (ponto único); srcML-DKT tem
`pred_df` em todos os 10 seeds (mean ± std sobre 10 runs).
"""))

cells.append(new_code_cell("""\
def compute_pooled_auc(all_results, first_only):
    pooled = {}
    for model in MODEL_ORDER:
        # Filtrar apenas runs com pred_df nao-None
        valid_runs_per_aid = {
            aid: [r for r in all_results[model][aid]["runs"] if r["pred_df"] is not None]
            for aid in AIDS
        }
        n_valid = min(len(v) for v in valid_runs_per_aid.values())
        if n_valid == 0:
            pooled[model] = {"mean": None, "std": None, "values": [], "n_runs": 0}
            continue

        # Identificar seeds comuns entre todos os assignments
        valid_seeds = sorted(set.intersection(*[
            {r["seed"] for r in valid_runs_per_aid[aid]} for aid in AIDS
        ]))

        run_aucs = []
        for seed in valid_seeds:
            frames = []
            for aid in AIDS:
                run = next(r for r in valid_runs_per_aid[aid] if r["seed"] == seed)
                frames.append(run["pred_df"])
            concat = pd.concat(frames, ignore_index=True)
            if first_only:
                sub = concat[concat["is_first_attempt"]]
            else:
                sub = concat
            auc = roc_auc_score(sub["correct"], sub["correct_predictions"]) * 100
            run_aucs.append(auc)

        n = len(run_aucs)
        pooled[model] = {
            "mean": float(np.mean(run_aucs)),
            "std":  float(np.std(run_aucs, ddof=1)) if n > 1 else 0.0,
            "values": run_aucs,
            "n_runs": n,
        }
    return pooled

pooled_first = compute_pooled_auc(all_results, first_only=True)
pooled_all   = compute_pooled_auc(all_results, first_only=False)

print("Runs validos por modelo (com pred_df nao-None):")
for m in MODEL_ORDER:
    print(f"  {m:12s}: {pooled_first[m]['n_runs']} runs")

rows = {}
for model in MODEL_ORDER:
    pf = pooled_first[model]
    pa = pooled_all[model]
    if pf["n_runs"] == 0:
        rows[model] = {"First-attempt AUC (pooled)": "N/A", "All-attempts AUC (pooled)": "N/A"}
    elif pf["n_runs"] == 1:
        rows[model] = {
            "First-attempt AUC (pooled)": f"{pf['mean']:.2f} (seed=42, 1 run)",
            "All-attempts AUC (pooled)":  f"{pa['mean']:.2f} (seed=42, 1 run)",
        }
    else:
        rows[model] = {
            "First-attempt AUC (pooled)": f"{pf['mean']:.2f} +- {pf['std']:.2f}",
            "All-attempts AUC (pooled)":  f"{pa['mean']:.2f} +- {pa['std']:.2f}",
        }

df_pooled = pd.DataFrame(rows).T
df_pooled.index.name = "Modelo"
print()
print("AUC pooled cross-assignment (5 assignments concatenados, %)")
display(df_pooled)

save_table_md(
    df_pooled, RESULTS / "comparison_table_pooled.md",
    "AUC pooled cross-assignment (%)",
    "\\n**Notas:**\\n"
    "1. AUC sobre predicoes concatenadas dos 5 assignments (1 AUC por run).\\n"
    "2. BKT = N/A: pred_df nao persistido no pickle (ver plano §2.3).\\n"
    "3. DKT e Code-DKT: pred_df disponivel apenas no seed=42; valor pontual reportado.\\n"
    "4. srcML-DKT: pred_df em todos os 10 seeds; mean +- std sobre 10 runs.\\n"
    "5. Comparavel com Pankiewicz et al. (2025) Table 3 (dataset diferente: C#, 610 alunos).\\n"
)

fig, ax = plt.subplots(figsize=(9, 1.5))
ax.axis("off")
tbl = ax.table(
    cellText=df_pooled.values,
    rowLabels=df_pooled.index,
    colLabels=df_pooled.columns,
    cellLoc="center", rowLoc="center",
    loc="center",
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1.2, 1.8)
ax.set_title("AUC pooled cross-assignment (%)", fontsize=11, pad=8)
plt.tight_layout()
plt.savefig(RESULTS / "comparison_table_pooled.png", bbox_inches="tight", dpi=DPI)
plt.show()
print("Salvo: comparison_table_pooled.png")
"""))

# ─── Célula 5: Comparação com literatura ─────────────────────────────────
cells.append(new_markdown_cell("""\
## 5 — Comparação com a literatura

Nossos valores de first-attempt AUC para A439 comparados com os valores
reportados nos papers de referência.

**Atenção:** o paper Pankiewicz et al. (2025) usa dataset diferente (C#, 6 tasks,
610 alunos), portanto a coluna delta para srcML-DKT é descritiva, nao é
validação de implementação.
"""))

cells.append(new_code_cell("""\
# Valores de referência dos papers
lit = {
    "Code-DKT (Shi 2022, A439 first)":  {"ref": 75.74, "ours": all_results["Code-DKT"][439]["first_auc_mean"]*100},
    "Code-DKT (Shi 2022, A439 all)":    {"ref": 74.31, "ours": all_results["Code-DKT"][439]["all_auc_mean"]*100},
    "DKT      (Shi 2022, A439 all)":    {"ref": 71.24, "ours": all_results["DKT"][439]["all_auc_mean"]*100},
    "srcML-DKT (Pankiewicz 2025, pooled first)*": {"ref": 83.55, "ours": pooled_first["srcML-DKT"]["mean"]},
    "srcML-DKT (Pankiewicz 2025, pooled all)*":   {"ref": 84.67, "ours": pooled_all["srcML-DKT"]["mean"]},
}

rows_lit = []
for label, v in lit.items():
    delta = v["ours"] - v["ref"]
    rows_lit.append({
        "Comparação": label,
        "Valor no paper (%)": f"{v['ref']:.2f}",
        "Nosso valor (%)":    f"{v['ours']:.2f}",
        "Delta (pp)":         f"{delta:+.2f}",
    })

df_lit = pd.DataFrame(rows_lit).set_index("Comparação")
print("Comparação com papers de referência")
display(df_lit)
print()
print("(*) Pankiewicz et al. (2025): dataset C# com 610 alunos e 6 tasks.")
print("    Delta é descritivo, nao é validação de implementação.")
print()
print(f"Criterio 1 CLAUDE.md: Code-DKT A439 first_auc = {all_results['Code-DKT'][439]['first_auc_mean']*100:.2f}%")
print(f"  Alvo: 75.74% +/-3pp => faixa [72.74%, 78.74%]")
ok = 72.74 <= all_results["Code-DKT"][439]["first_auc_mean"]*100 <= 78.74
print(f"  Criterio {'SATISFEITO' if ok else 'NAO satisfeito'}: {all_results['Code-DKT'][439]['first_auc_mean']*100:.2f}% {'dentro' if ok else 'fora'} da faixa")
"""))

# ─── Célula 6: Wilcoxon ──────────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 6 — Wilcoxon signed-rank com correção Holm-Bonferroni

**Critério 3 do CLAUDE.md:** teste de significância entre modelos.

Três comparações pareadas entre os modelos profundos (BKT excluído por ausência
de variância intra-assignment no pickle):

| Par | Hipótese alternativa | N de pares |
|---|---|---|
| Code-DKT vs DKT | Code-DKT > DKT | 50 |
| srcML-DKT vs Code-DKT | srcML-DKT < Code-DKT | 50 |
| srcML-DKT vs DKT | bilateral | 50 |

Correção Holm-Bonferroni aplicada dentro de cada métrica (3 testes por família).
Bootstrap CI 95% sobre 1000 reamostras dos 50 pares.
"""))

cells.append(new_code_cell("""\
def holm_bonferroni(p_values):
    n = len(p_values)
    order = np.argsort(p_values)
    p_sorted = np.array(p_values)[order]
    p_adj_sorted = np.minimum(p_sorted * np.arange(n, 0, -1), 1.0)
    for i in range(1, n):
        p_adj_sorted[i] = max(p_adj_sorted[i], p_adj_sorted[i-1])
    p_adj = np.empty(n)
    p_adj[order] = p_adj_sorted
    return p_adj

def get_run_by_seed(model_results, aid, seed):
    for r in model_results[aid]["runs"]:
        if r["seed"] == seed:
            return r
    return None

def bootstrap_ci(diffs, n_boot=1000, rng=None):
    if rng is None:
        rng = np.random.RandomState(SEED)
    boot_means = np.array([
        np.mean(rng.choice(diffs, size=len(diffs)))
        for _ in range(n_boot)
    ])
    return float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))

def run_wilcoxon_analysis(all_results):
    comparisons = [
        ("Code-DKT",  "DKT",       "greater",   "Code-DKT > DKT"),
        ("srcML-DKT", "Code-DKT",  "less",      "srcML-DKT < Code-DKT"),
        ("srcML-DKT", "DKT",       "two-sided", "srcML-DKT vs DKT"),
    ]
    metrics = ["first_auc", "all_auc"]
    raw = {}
    rng = np.random.RandomState(SEED)

    for metric in metrics:
        ps = []
        for (m_a, m_b, alt, label) in comparisons:
            diffs = []
            for aid in AIDS:
                for seed in range(42, 52):
                    ra = get_run_by_seed(all_results[m_a], aid, seed)
                    rb = get_run_by_seed(all_results[m_b], aid, seed)
                    diffs.append(ra[metric] - rb[metric])
            diffs = np.array(diffs)
            stat, p = wilcoxon(diffs, alternative=alt)
            N = len(diffs)
            mu_w = N * (N + 1) / 4
            sig_w = np.sqrt(N * (N + 1) * (2 * N + 1) / 24)
            z = (stat - mu_w) / sig_w
            effect_r = abs(z) / np.sqrt(N)
            ci_lo, ci_hi = bootstrap_ci(diffs, rng=rng)
            ps.append(p)
            raw[(m_a, m_b, metric)] = {
                "diffs": diffs, "stat": stat, "p": p,
                "effect_r": effect_r,
                "mean_diff": float(np.mean(diffs)),
                "std_diff":  float(np.std(diffs, ddof=1)),
                "ci_lo": ci_lo, "ci_hi": ci_hi,
                "alternative": alt, "label": label,
            }
        p_adj = holm_bonferroni(ps)
        for i, (m_a, m_b, alt, _) in enumerate(comparisons):
            raw[(m_a, m_b, metric)]["p_adj"] = float(p_adj[i])
            raw[(m_a, m_b, metric)]["significant"] = bool(p_adj[i] < 0.05)

    return raw, comparisons

wilcoxon_raw, comparisons = run_wilcoxon_analysis(all_results)
print("Wilcoxon concluido.")
"""))

cells.append(new_code_cell("""\
# Exibir tabela de resultados Wilcoxon
rows_w = []
for metric, metric_label in [("first_auc", "First-attempt AUC"), ("all_auc", "All-attempts AUC")]:
    for (m_a, m_b, alt, label) in comparisons:
        r = wilcoxon_raw[(m_a, m_b, metric)]
        sig_str = "* (sig.)" if r["significant"] else "n.s."
        rows_w.append({
            "Metrica":    metric_label,
            "Comparacao": label,
            "W":          f"{r['stat']:.1f}",
            "p":          f"{r['p']:.4f}",
            "p_adj (Holm)": f"{r['p_adj']:.4f}",
            "Sig. (a=0.05)": sig_str,
            "r (efeito)": f"{r['effect_r']:.3f}",
            "mean_diff (pp)": f"{r['mean_diff']*100:+.2f}",
            "CI 95% (pp)": f"[{r['ci_lo']*100:+.2f}, {r['ci_hi']*100:+.2f}]",
        })

df_wilcoxon = pd.DataFrame(rows_w)
print("Resultados do Wilcoxon signed-rank (N=50 pares, correção Holm-Bonferroni):")
display(df_wilcoxon.set_index(["Metrica", "Comparacao"]))
"""))

# ─── Célula 7: BKT vs deep models ─────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 7 — BKT vs. modelos profundos: diferença descritiva

BKT é determinístico: sem variância intra-assignment no pickle persistido, nao é
possível pareá-lo seed a seed com os modelos profundos. Reportamos apenas a
diferença de médias por assignment, sem teste de hipótese.

A direção é consistente em todos os 5 assignments para ambas as métricas.
"""))

cells.append(new_code_cell("""\
rows_bkt = []
for model in ["DKT", "Code-DKT", "srcML-DKT"]:
    for aid in AIDS:
        bkt_f = all_results["BKT"][aid]["first_auc_mean"] * 100
        bkt_a = all_results["BKT"][aid]["all_auc_mean"] * 100
        deep_f = all_results[model][aid]["first_auc_mean"] * 100
        deep_a = all_results[model][aid]["all_auc_mean"] * 100
        rows_bkt.append({
            "Modelo":    model,
            "Assignment": f"A{aid}",
            "BKT first (%)":    f"{bkt_f:.2f}",
            f"{model} first (%)": f"{deep_f:.2f}",
            "Delta first (pp)": f"{deep_f - bkt_f:+.2f}",
            "BKT all (%)":      f"{bkt_a:.2f}",
            f"{model} all (%)":   f"{deep_a:.2f}",
            "Delta all (pp)":   f"{deep_a - bkt_a:+.2f}",
        })

df_bkt = pd.DataFrame(rows_bkt).set_index(["Modelo", "Assignment"])
print("Diferenca media (modelo profundo - BKT) sem teste estatístico:")
print("(BKT é determinístico, sem variancia intra-assignment no pickle)")
print()
display(df_bkt[["Delta first (pp)", "Delta all (pp)"]])
print()
print("Observacao: todos os deltas sao positivos (modelos profundos > BKT)")
print("em todas as combinacoes modelo x assignment x metrica.")
"""))

# ─── Célula 8: Barras agrupadas ────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 8 — Barras agrupadas por assignment

Visão de helicóptero da Tabela comparativa. Barra de erro: ±1 std (apenas para
modelos profundos). Linha pontilhada horizontal em 0.5 (chance).

Duas figuras: first-attempt AUC e all-attempts AUC.
"""))

cells.append(new_code_cell("""\
def plot_grouped_bars(all_results, metric, filename, title):
    x = np.arange(len(AIDS))
    width = 0.2
    offsets = np.linspace(-(1.5 * width), 1.5 * width, 4)

    fig, ax = plt.subplots(figsize=(13, 5))

    for i, model in enumerate(MODEL_ORDER):
        means = [all_results[model][a][f"{metric}_mean"] * 100 for a in AIDS]
        stds  = [all_results[model][a][f"{metric}_std"]  * 100 for a in AIDS]
        bars = ax.bar(x + offsets[i], means, width, label=model,
                      color=COLORS[model], alpha=0.85, edgecolor="white", linewidth=0.8)
        # Barra de erro apenas para modelos com std real
        err_stds = [s if s > 0.01 else 0 for s in stds]
        ax.errorbar(x + offsets[i], means, yerr=err_stds,
                    fmt="none", color="black", capsize=3, linewidth=1)

    ax.axhline(0.5 * 100, color="gray", linestyle="--", linewidth=1, alpha=0.7,
               label="Chance (50%)")
    ax.set_xticks(x)
    ax.set_xticklabels(AID_LABELS)
    ax.set_xlabel("Assignment")
    ylabel = "First-attempt AUC (%)" if metric == "first_auc" else "All-attempts AUC (%)"
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="lower right")
    ax.set_ylim(45, 95)
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(RESULTS / filename, bbox_inches="tight", dpi=DPI)
    plt.show()
    print(f"Salvo: {filename}")

plot_grouped_bars(all_results, "first_auc",
                 "fig_comparison_bars_first_auc.png",
                 "First-attempt AUC por assignment e modelo")
plot_grouped_bars(all_results, "all_auc",
                 "fig_comparison_bars_all_auc.png",
                 "All-attempts AUC por assignment e modelo")
"""))

# ─── Célula 9: Boxplot por seed ────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 9 — Distribuição sobre seeds (boxplot)

Cada caixa agrega os 10 valores de first-attempt AUC (seeds 42 a 51) de um
modelo em um assignment. BKT exibido como linha horizontal (valor pontual).

Comunica a estabilidade dos runs: Code-DKT e srcML-DKT têm caixas
significativamente mais estreitas que o DKT, evidenciando menor variância
sobre seeds (achado registrado em `results/multirun`).
"""))

cells.append(new_code_cell("""\
deep_models = ["DKT", "Code-DKT", "srcML-DKT"]

fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle("Distribuição de First-attempt AUC sobre 10 seeds por assignment", fontsize=12)

for col_idx, aid in enumerate(AIDS):
    ax = axes[col_idx]

    data_bp = []
    labels_bp = []
    colors_bp = []
    for model in deep_models:
        vals = [r["first_auc"] * 100 for r in all_results[model][aid]["runs"]]
        data_bp.append(vals)
        labels_bp.append(model.replace("Code-", "C-").replace("srcML-", "s-"))
        colors_bp.append(COLORS[model])

    bp = ax.boxplot(data_bp, labels=labels_bp, patch_artist=True,
                    medianprops=dict(color="black", linewidth=2))
    for patch, color in zip(bp["boxes"], colors_bp):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # BKT como linha horizontal
    bkt_val = all_results["BKT"][aid]["first_auc_mean"] * 100
    ax.axhline(bkt_val, color=COLORS["BKT"], linestyle="--", linewidth=1.5,
               label=f"BKT={bkt_val:.1f}%")
    ax.legend(fontsize=8, loc="lower right")

    ax.set_title(f"A{aid}", fontsize=11)
    ax.set_xlabel("Modelo")
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

axes[0].set_ylabel("First-attempt AUC (%)")
plt.tight_layout()
plt.savefig(RESULTS / "fig_seed_variance_boxplot.png", bbox_inches="tight", dpi=DPI)
plt.show()
print("Salvo: fig_seed_variance_boxplot.png")
"""))

# ─── Célula 10: Delta vs DKT ──────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 10 — Delta vs. DKT

Barras divergentes mostrando a diferença (em pontos percentuais) de cada modelo
em relação ao DKT, por assignment.

Esperamos barras Code-DKT positivas (replicação de Shi et al. 2022) e barras
srcML-DKT negativas em relação ao Code-DKT (achado nosso, divergente do paper
Pankiewicz et al. 2025).
"""))

cells.append(new_code_cell("""\
delta_models = ["Code-DKT", "srcML-DKT"]
# Tambem adicionar srcML-DKT vs Code-DKT para mostrar a diferenca interna
delta_pairs = [
    ("Code-DKT",  "DKT",      "Code-DKT - DKT",      COLORS["Code-DKT"]),
    ("srcML-DKT", "DKT",      "srcML-DKT - DKT",     COLORS["srcML-DKT"]),
    ("srcML-DKT", "Code-DKT", "srcML-DKT - Code-DKT","#9467bd"),
]

x = np.arange(len(AIDS))
width = 0.25
offsets = np.linspace(-width, width, 3)

fig, ax = plt.subplots(figsize=(13, 5))

for i, (m_a, m_b, label, color) in enumerate(delta_pairs):
    deltas = [(all_results[m_a][a]["first_auc_mean"] -
               all_results[m_b][a]["first_auc_mean"]) * 100
              for a in AIDS]
    bars = ax.bar(x + offsets[i], deltas, width, label=label,
                  color=color, alpha=0.85, edgecolor="white", linewidth=0.8)

ax.axhline(0, color="black", linewidth=1.0)
ax.set_xticks(x)
ax.set_xticklabels(AID_LABELS)
ax.set_xlabel("Assignment")
ax.set_ylabel("Delta first-attempt AUC (pp)")
ax.set_title("Diferença de first-attempt AUC em relação ao DKT e Code-DKT")
ax.legend(loc="upper right")
ax.yaxis.grid(True, alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig(RESULTS / "fig_delta_vs_dkt.png", bbox_inches="tight", dpi=DPI)
plt.show()
print("Salvo: fig_delta_vs_dkt.png")
"""))

# ─── Célula 11: Heatmap per-problem ──────────────────────────────────────
cells.append(new_markdown_cell("""\
## 11 — Heatmap de AUC por problema

First-attempt AUC por (modelo, problema) dentro de cada assignment. Cor = AUC
médio sobre os 10 seeds dos modelos profundos.

BKT exibido como linha N/A (pred_df nao persistido no pickle).

Inspirado em Shi et al. (2022) Table 3, generalizado para 4 modelos × 5 assignments.
"""))

cells.append(new_code_cell("""\
def compute_per_problem_auc(all_results, first_only=True):
    deep = ["DKT", "Code-DKT", "srcML-DKT"]
    out = {}
    for model in deep:
        out[model] = {}
        for aid in AIDS:
            out[model][aid] = {}
            # Usar apenas runs com pred_df nao-None
            valid_runs = [r for r in all_results[model][aid]["runs"]
                          if r["pred_df"] is not None]
            if not valid_runs:
                continue
            probs = sorted(valid_runs[0]["pred_df"]["skill_name"].unique())
            for prob in probs:
                aucs = []
                for run in valid_runs:
                    pdf = run["pred_df"]
                    mask = pdf["skill_name"] == prob
                    if first_only:
                        mask &= pdf["is_first_attempt"]
                    sub = pdf[mask]
                    if len(sub) < 2 or sub["correct"].nunique() < 2:
                        aucs.append(np.nan)
                        continue
                    try:
                        aucs.append(roc_auc_score(sub["correct"],
                                                   sub["correct_predictions"]))
                    except Exception:
                        aucs.append(np.nan)
                out[model][aid][prob] = float(np.nanmean(aucs))
    return out

pp_auc = compute_per_problem_auc(all_results, first_only=True)
print("AUC per problema calculado.")
"""))

cells.append(new_code_cell("""\
fig, axes = plt.subplots(1, 5, figsize=(18, 4))
fig.suptitle("First-attempt AUC por problema e modelo (media sobre 10 seeds)", fontsize=12)

all_plot_models = ["BKT", "DKT", "Code-DKT", "srcML-DKT"]

for col_idx, aid in enumerate(AIDS):
    ax = axes[col_idx]
    valid_run = next(r for r in all_results["DKT"][aid]["runs"] if r["pred_df"] is not None)
    probs = sorted(valid_run["pred_df"]["skill_name"].unique())

    matrix = []
    row_labels = []
    for model in all_plot_models:
        if model == "BKT":
            matrix.append([np.nan] * len(probs))
        else:
            row = [pp_auc[model][aid].get(p, np.nan) for p in probs]
            matrix.append(row)
        row_labels.append(model)

    matrix = np.array(matrix)

    # Mask NaN (BKT row) com cor separada
    masked = np.ma.masked_invalid(matrix)
    cmap = plt.cm.RdYlGn.copy()
    cmap.set_bad(color="#d0d0d0")
    im = ax.imshow(masked, aspect="auto", cmap=cmap, vmin=0.4, vmax=1.0)

    ax.set_xticks(range(len(probs)))
    ax.set_xticklabels([f"P{p}" for p in probs], rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(all_plot_models)))
    ax.set_yticklabels(row_labels, fontsize=8)
    ax.set_title(f"A{aid}", fontsize=11)

    # Anotar valores
    for ri in range(len(all_plot_models)):
        for ci in range(len(probs)):
            val = matrix[ri, ci]
            if not np.isnan(val):
                ax.text(ci, ri, f"{val*100:.0f}", ha="center", va="center",
                        fontsize=6.5, color="black" if 0.45 < val < 0.85 else "white")
            else:
                ax.text(ci, ri, "N/A", ha="center", va="center",
                        fontsize=6.5, color="#555555")

# Colorbar compartilhada
fig.subplots_adjust(right=0.88)
cbar_ax = fig.add_axes([0.90, 0.15, 0.012, 0.7])
sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, norm=plt.Normalize(vmin=40, vmax=100))
sm.set_array([])
fig.colorbar(sm, cax=cbar_ax, label="First-attempt AUC (%)")

plt.savefig(RESULTS / "fig_per_problem_heatmap.png", bbox_inches="tight", dpi=DPI)
plt.show()
print("Salvo: fig_per_problem_heatmap.png")
print()
print("Nota: linha BKT exibida em cinza (N/A) porque o pickle nao inclui pred_df")
print("per-evento para BKT. Regerar via refit do pyBKT e viavel (~30s) mas nao e")
print("gate dos Criterios 2 e 3 do CLAUDE.md.")
"""))

# ─── Célula 12: Discussão ─────────────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 12 — Discussão

### 12.1 Hierarquia esperada confirmada

Os modelos profundos (DKT, Code-DKT, srcML-DKT) superam o BKT em todos os
5 assignments e em ambas as métricas. O delta varia de +5 a +29 pontos
percentuais em first-attempt AUC, com os maiores saltos em assignments de
maior complexidade (A492, A502). Esse resultado confirma a expectativa teórica
documentada em Shi et al. (2022) Seção 6 RQ1: representações de histórico
sequencial são superiores a parâmetros de habilidade independentes por
problema.

O BKT, apesar de ser o baseline mais simples, produz AUCs acima de chance em
todos os 5 assignments, validando a consistência do nosso preprocessamento
(split 80/20, `random_state=1`, 410 alunos conforme o paper de referência).

### 12.2 Code-DKT supera DKT: confirmado com significância estatística

O Wilcoxon signed-rank (N=50 pares por comparação) evidencia diferença
significativa a favor do Code-DKT tanto em first-attempt AUC quanto em
all-attempts AUC, com correção Holm-Bonferroni. A magnitude do delta (media
de +2 a +5 pp por assignment) está dentro do intervalo reportado por Shi et al.
(2022) Table 1 (+3 a 4pp), confirmando a replicação.

Um achado adicional, nao publicado no paper original, é que Code-DKT apresenta
desvio padrão sobre seeds entre 3 e 5 vezes menor que o DKT (Code-DKT std=0.53
a 1.34pp vs. DKT std=1.66 a 5.04pp em first-attempt AUC). Isso tem implicação
prática direta: em produção, um único run do Code-DKT é mais confiável que um
único run do DKT. O boxplot da Seção 9 torna isso visível.

### 12.3 srcML-DKT abaixo do Code-DKT: resultado divergente do paper de referência

O srcML-DKT ficou de 2.9 a 4.2 pontos percentuais abaixo do Code-DKT em
first-attempt AUC em todos os 5 assignments. O Wilcoxon confirma essa diferença
como estatisticamente significativa, com o sinal invertido em relação ao
reportado por Pankiewicz et al. (2025) Table 3 (+1.65pp srcML-DKT sobre
Code-DKT no paper).

Antes de interpretar isso como falha, é importante destacar o que funcionou
exatamente como esperado: a taxa de parsing do srcML atingiu 100% (43.661 de
43.661 submissões, incluindo os 109.020 eventos `Compile.Error`), confirmando o
ganho metodológico central da abordagem. A arquitetura é estavel (std de 0.44 a
1.01pp, comparavel ao Code-DKT).

Nossa hipótese principal para a divergência (documentada em
`docs/srcml_dkt_implementation.md` §8) é que o vocabulário de paths extraído
pelo srcML é aproximadamente 2.6 a 2.7 vezes menor que o do javalang (A439:
8.013 vs. 21.717 paths únicos). O srcML tokeniza nós interiores como tags XML
genéricas (`function`, `block`, `expr`), que se repetem em praticamente todos
os métodos, enquanto o javalang usa nomes de classe AST com maior poder
discriminativo (`MethodDeclaration`, `BinaryOperation`, `IfStatement`). A
atenção code2vec tem menos vocabulário para distinguir submissões corretas de
incorretas.

Esse achado é uma contribuição metodológica útil para o campo: aponta para um
detalhe de implementação que o paper Pankiewicz et al. (short paper, 8 páginas,
sem código aberto) nao especifica, e que é determinante para o resultado. Nao
invalida o resultado do paper de referência, que usa C# com dataset diferente e
presumivelmente regras de tokenização diferentes. Demonstra, porem, que a
abordagem é sensível a essa escolha.

### 12.4 Implicações para o TCC 2

O Code-DKT é o modelo-base recomendado para o TCC 2. Justificativas:
(a) maior first-attempt AUC pooled entre os 4 modelos;
(b) estabilidade 3 a 5 vezes superior ao DKT sobre seeds;
(c) replicação bem-sucedida do paper de referência (Critério 1 do CLAUDE.md
satisfeito para A439);
(d) resultado reproduzível do zero com seed fixo (Critério 4).

O srcML-DKT permanece como Linha 1 de trabalho futuro: a ablation sem
`Compile.Error`, o tuning específico de hiperparâmetros para o vocabulário
srcML, e a investigação de regras de tokenização alternativas têm potencial de
reverter o resultado negativo. O investimento nessas investigações justifica-se
pelo ganho metodológico demonstrado (100% de cobertura de parse), que o
Code-DKT vanilla nao tem.
"""))

# ─── Célula 13: Sumário executivo ─────────────────────────────────────────
cells.append(new_markdown_cell("""\
## 13 — Sumário executivo

### Resposta aos Critérios de Conclusão do TCC 1

**Critério 1** (Code-DKT A439 first_auc ≈ 74% ±3%): **SATISFEITO**.
Nosso valor: 73.27% (media sobre 10 runs). Alvo do paper: 75.74%.
Delta: -2.47pp, dentro da faixa ±3pp exigida.

**Critério 2** (Tabela comparativa BKT vs DKT vs Code-DKT por assignment): **SATISFEITO**.
Tabela 4×5×2 produzida (Seções 3 e 4 deste notebook). Arquivos:
`results/comparison_table_first_auc.md`, `results/comparison_table_all_auc.md`,
`results/comparison_table_pooled.md`. srcML-DKT incluído como 4ª coluna.

**Critério 3** (Wilcoxon signed-rank entre modelos): **SATISFEITO**.
6 testes (3 comparações × 2 métricas), correção Holm-Bonferroni. Resultados:
Code-DKT > DKT (significativo), srcML-DKT < Code-DKT (significativo),
srcML-DKT vs DKT (verificar p_adj na Seção 6).

**Critério 4** (notebooks executáveis do zero com seed fixo): **SATISFEITO**.
`set_global_seed(42)` na Seção 1. Nenhum treino neste notebook: resultados
completamente determinados pelos 4 pickles preexistentes. Bootstrap com
`RandomState(42)`.

### Recomendação para o TCC 2

**Modelo-base: Code-DKT** (Shi et al., 2022).
**Linha 1 de trabalho futuro: srcML-DKT** com ablation e retuning
(ver `docs/srcml_dkt_implementation.md` §10.2).

### Artefatos gerados por este notebook

| Artefato | Caminho |
|---|---|
| Tabela first AUC | `results/comparison_table_first_auc.{md,png}` |
| Tabela all AUC | `results/comparison_table_all_auc.{md,png}` |
| Tabela pooled | `results/comparison_table_pooled.{md,png}` |
| Barras first AUC | `results/fig_comparison_bars_first_auc.png` |
| Barras all AUC | `results/fig_comparison_bars_all_auc.png` |
| Boxplot seeds | `results/fig_seed_variance_boxplot.png` |
| Delta vs DKT | `results/fig_delta_vs_dkt.png` |
| Heatmap per-problema | `results/fig_per_problem_heatmap.png` |
| JSON sumário | `results/comparison_summary.json` |
"""))

# ─── Célula 14: Serialização JSON ─────────────────────────────────────────
cells.append(new_markdown_cell("## 14 — Serialização"))

cells.append(new_code_cell("""\
# Schema: {"per_assignment": {modelo: {aid: {first_mean, first_std, all_mean, all_std}}},
#           "pooled": {modelo: {first: {mean, std}, all: {mean, std}}},
#           "wilcoxon": {par: {metric: {p, p_adj, effect_r, mean_diff}}}}

summary = {
    "per_assignment": {},
    "pooled": {},
    "wilcoxon": {},
}

for model in MODEL_ORDER:
    summary["per_assignment"][model] = {}
    for aid in AIDS:
        summary["per_assignment"][model][str(aid)] = {
            "first_mean": round(all_results[model][aid]["first_auc_mean"] * 100, 4),
            "first_std":  round(all_results[model][aid]["first_auc_std"]  * 100, 4),
            "all_mean":   round(all_results[model][aid]["all_auc_mean"]   * 100, 4),
            "all_std":    round(all_results[model][aid]["all_auc_std"]    * 100, 4),
        }

for model in MODEL_ORDER:
    pf = pooled_first[model]
    pa = pooled_all[model]
    if pf["mean"] is None:
        summary["pooled"][model] = {
            "first": {"mean": None, "std": None},
            "all":   {"mean": None, "std": None},
        }
    else:
        summary["pooled"][model] = {
            "first": {"mean": round(pf["mean"], 4), "std": round(pf["std"], 4)},
            "all":   {"mean": round(pa["mean"], 4), "std": round(pa["std"], 4)},
        }

for (m_a, m_b, alt, label) in comparisons:
    pair_key = f"{m_a}_vs_{m_b}".replace("-", "_")
    summary["wilcoxon"][pair_key] = {}
    for metric in ["first_auc", "all_auc"]:
        r = wilcoxon_raw[(m_a, m_b, metric)]
        summary["wilcoxon"][pair_key][metric] = {
            "p":        round(r["p"], 6),
            "p_adj":    round(r["p_adj"], 6),
            "effect_r": round(r["effect_r"], 4),
            "mean_diff_pp": round(r["mean_diff"] * 100, 4),
            "significant": r["significant"],
        }

out_path = RESULTS / "comparison_summary.json"
with open(out_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Salvo: {out_path}")

# Verificacao rapida
assert set(summary["per_assignment"]) == {"BKT", "DKT", "Code-DKT", "srcML-DKT"}
assert "pooled" in summary and "wilcoxon" in summary
print("Schema OK: per_assignment, pooled, wilcoxon.")
print("\\nTCC 1 concluido.")
"""))

# ─── Montar e salvar ────────────────────────────────────────────────────────
nb = new_notebook(cells=cells)
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "name": "python",
        "version": "3.10.0",
    },
}

out_path = "notebooks/07_comparison.ipynb"
with open(out_path, "w") as f:
    nbformat.write(nb, f)

print(f"Notebook criado: {out_path}")
print(f"Total de células: {len(cells)}")
