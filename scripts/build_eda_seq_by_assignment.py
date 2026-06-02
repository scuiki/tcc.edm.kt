"""Gera boxplot do tamanho de sequencia (tentativas) por assignment (CSEDM Spring 2019).

Cada sequencia de KT e o conjunto de eventos Run.Program de um estudante em um
assignment, ordenado no tempo. O comprimento (numero de tentativas) por par
(estudante, assignment) descreve esforco e persistencia, e fundamenta a decisao
de truncagem em 50 tentativas de Shi et al. (2022). Aqui a truncagem nao e
desenhada: a figura mostra apenas a distribuicao de tentativas por assignment.

Reproduz a figura isolada da secao 4.2 do notebook 01_eda, porem sem titulo
embutido (vai no slide ABNT), com fundo transparente, eixos em negrito e fontes
ampliadas para projecao.

Uso: python3 scripts/build_eda_seq_by_assignment.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "CSEDM"
RESULTS = ROOT / "results"
OUT_RESULTS = RESULTS / "sec4_seq_boxplot_by_assignment.png"
OUT_ASSETS = ROOT / "apresentacao" / "assets" / "eda-seq-by-assignment.png"

UNI_BLUE = "#2667FF"
BLACK = "#000000"
UNI_GRAY = "#5b6472"

# Uma cor por assignment (A1..A5). Azul UniFacens na lideranca, demais
# distintas e saturadas para leitura em projetor.
ASSIGN_COLORS = ["#2667FF", "#F4A300", "#2BA84A", "#E5484D", "#8B5CF6"]


def main() -> None:
    main_table = pd.read_csv(DATA_ROOT / "MainTable.csv", low_memory=False)

    runs = main_table[main_table["EventType"] == "Run.Program"].copy()

    assignment_order = sorted(runs["AssignmentID"].dropna().unique())
    assign_name = {aid: f"A{i + 1} ({int(aid)})" for i, aid in enumerate(assignment_order)}

    seq_len = (
        runs.groupby(["SubjectID", "AssignmentID"])
        .size()
        .reset_index(name="seq_len")
    )

    data_by_assign = [
        seq_len.loc[seq_len["AssignmentID"] == aid, "seq_len"].values
        for aid in assignment_order
    ]
    tick_labels = [assign_name[aid] for aid in assignment_order]

    fig, ax = plt.subplots(figsize=(10, 5.0), dpi=140)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    bp = ax.boxplot(
        data_by_assign,
        tick_labels=tick_labels,
        patch_artist=True,
        widths=0.58,
        boxprops=dict(edgecolor=BLACK, linewidth=1.6),
        medianprops=dict(color=BLACK, linewidth=2.4),
        whiskerprops=dict(color=BLACK, linewidth=1.6),
        capprops=dict(color=BLACK, linewidth=1.6),
        flierprops=dict(marker="o", markersize=5, markerfacecolor="none",
                        markeredgecolor=BLACK, alpha=0.9),
    )
    # Uma cor por assignment
    for patch, color in zip(bp["boxes"], ASSIGN_COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.80)

    ax.set_ylabel("Tentativas", fontsize=18, color=BLACK, fontweight="bold")
    ax.tick_params(axis="both", labelsize=15, colors=BLACK)
    ax.grid(axis="y", alpha=0.22, color=UNI_GRAY, linestyle=":")
    ax.set_axisbelow(True)
    for spine_name, spine in ax.spines.items():
        if spine_name in {"top", "right"}:
            spine.set_visible(False)
        else:
            spine.set_color(BLACK)
            spine.set_linewidth(1.3)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")

    plt.tight_layout()
    OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_RESULTS, bbox_inches="tight", transparent=True)
    plt.close(fig)

    OUT_ASSETS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT_RESULTS, OUT_ASSETS)

    print(f"OK: {OUT_RESULTS.relative_to(ROOT)}")
    print(f"OK: {OUT_ASSETS.relative_to(ROOT)}")
    print()
    print("=== Estatisticas por assignment (tentativas/sequencia) ===")
    for aid, vals in zip(assignment_order, data_by_assign):
        if len(vals) == 0:
            continue
        s = pd.Series(vals)
        print(
            f"  {assign_name[aid]:<12} | n={len(vals):>3} | mediana={s.median():.0f} | "
            f"media={s.mean():.1f} | P95={s.quantile(0.95):.0f} | max={s.max()}"
        )


if __name__ == "__main__":
    main()
