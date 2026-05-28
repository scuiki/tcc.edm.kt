"""Gera curvas de aprendizado por assignment (CSEDM Spring 2019) para o slide EDA-03.

Para cada assignment A1..A5, plota a taxa de acerto (Score == 1.0) em funcao
da tentativa ordinal dentro do assignment (1a tentativa de qualquer problema,
2a, 3a, ..., ate a 30a). Permite ver:
- A1 com curva ascendente clara (aprendizado intra-assignment)
- A5 comecando alto (alunos chegam aos ultimos assignments mais treinados)

Reproduz a cell de Curvas de Aprendizado do notebook 01_eda (secao 4), porem
sem titulo embutido (titulo vai no slide ABNT) e com fundo transparente.

Uso: python3 scripts/build_eda_learning_curves.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "CSEDM"
RESULTS = ROOT / "results"
OUT_RESULTS = RESULTS / "sec4_learning_curves_clean.png"
OUT_ASSETS = ROOT / "apresentacao" / "assets" / "eda-curvas-aprendizado.png"

MAX_ATT_SHOW = 30
MIN_STUDENTS = 10

BLACK = "#000000"
UNI_GRAY = "#5b6472"
ASSIGN_COLORS = ["#2667FF", "#F2A516", "#1AA260", "#D7191C", "#7B49C6"]


def main() -> None:
    main_table = pd.read_csv(DATA_ROOT / "MainTable.csv", low_memory=False)
    runs = main_table[main_table["EventType"] == "Run.Program"].copy()
    runs["correct"] = (runs["Score"] == 1.0).astype(int)

    assignment_order = sorted(runs["AssignmentID"].dropna().unique())
    assign_name = {aid: f"A{i+1} ({int(aid)})" for i, aid in enumerate(assignment_order)}

    runs_sorted = runs.sort_values(["SubjectID", "AssignmentID", "ServerTimestamp"]).copy()
    runs_sorted["attempt_num"] = (
        runs_sorted.groupby(["SubjectID", "AssignmentID"]).cumcount() + 1
    )

    lc = (
        runs_sorted[runs_sorted["attempt_num"] <= MAX_ATT_SHOW]
        .groupby(["AssignmentID", "attempt_num"])["correct"]
        .agg(mean_correct="mean", n_students="count")
        .reset_index()
    )
    lc = lc[lc["n_students"] >= MIN_STUDENTS]

    fig, axes = plt.subplots(1, 5, figsize=(18, 5), sharey=True, dpi=130)
    fig.patch.set_alpha(0.0)
    for i, aid in enumerate(assignment_order):
        ax = axes[i]
        ax.set_facecolor("none")
        sub = lc[lc["AssignmentID"] == aid]
        if sub.empty:
            continue
        overall = runs[runs["AssignmentID"] == aid]["correct"].mean() * 100
        ax.plot(
            sub["attempt_num"], sub["mean_correct"] * 100,
            marker="o", markersize=5, linewidth=2.2, color=ASSIGN_COLORS[i],
        )
        ax.axhline(
            overall, color=BLACK, linestyle="--", linewidth=1.2,
            label=f"global: {overall:.1f}%",
        )
        ax.set_title(assign_name[aid], fontsize=16, color=BLACK, pad=8, fontweight="bold")
        ax.set_xlabel("Tentativa #", fontsize=14, color=BLACK)
        ax.tick_params(axis="both", labelsize=12, colors=BLACK)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter())
        ax.legend(fontsize=12, loc="upper right", frameon=False, labelcolor=BLACK)
        ax.set_xlim(1, MAX_ATT_SHOW)
        ax.set_ylim(10, 50)
        ax.grid(True, alpha=0.22, color=UNI_GRAY, linestyle=":")
        ax.set_axisbelow(True)
        for spine_name, spine in ax.spines.items():
            if spine_name in {"top", "right"}:
                spine.set_visible(False)
            else:
                spine.set_color(BLACK)
                spine.set_linewidth(1.0)

    axes[0].set_ylabel("Taxa de acerto", fontsize=15, color=BLACK)
    plt.tight_layout()

    OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_RESULTS, bbox_inches="tight", transparent=True)
    plt.close(fig)

    OUT_ASSETS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT_RESULTS, OUT_ASSETS)

    print(f"OK: {OUT_RESULTS.relative_to(ROOT)}")
    print(f"OK: {OUT_ASSETS.relative_to(ROOT)}")
    print()
    print("=== Globais por assignment ===")
    for aid in assignment_order:
        overall = runs[runs["AssignmentID"] == aid]["correct"].mean() * 100
        print(f"  {assign_name[aid]}: {overall:.2f}%")


if __name__ == "__main__":
    main()
