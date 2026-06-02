"""Gera boxplot de X-Grade por numero de assignments completados (CSEDM Spring 2019).

X-Grade e a nota final normalizada do aluno na disciplina (escala 0-1) em
Subject.csv. O numero de assignments completados e contado a partir de
MainTable.csv. O boxplot revela duas tendencias:
- mediana de X-Grade cresce com o numero de assignments completados
- variancia diminui (alunos mais engajados tem desempenho mais consistente)

Reproduz a cell de Distribuicao de X-Grade do notebook 01_eda (secao 2),
porem sem titulo embutido (vai no slide ABNT) e com fundo transparente.

Uso: python3 scripts/build_eda_xgrade_by_completed.py
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
OUT_RESULTS = RESULTS / "sec2_xgrade_by_completed.png"
OUT_ASSETS = ROOT / "apresentacao" / "assets" / "eda-xgrade-completados.png"

UNI_BLUE = "#2667FF"
BLACK = "#000000"
UNI_GRAY = "#5b6472"


def main() -> None:
    subject = pd.read_csv(DATA_ROOT / "LinkTables" / "Subject.csv")
    main_table = pd.read_csv(DATA_ROOT / "MainTable.csv", low_memory=False)

    assign_counts = (
        main_table.dropna(subset=["AssignmentID"])
        .groupby("SubjectID")["AssignmentID"]
        .nunique()
        .rename("n_assignments")
    )
    subject_ext = subject.join(assign_counts, on="SubjectID").dropna(subset=["n_assignments"])
    subject_ext["n_assignments"] = subject_ext["n_assignments"].astype(int)

    bins = sorted(subject_ext["n_assignments"].unique())
    data_by_bin = [
        subject_ext.loc[subject_ext["n_assignments"] == k, "X-Grade"].dropna().values
        for k in bins
    ]
    sample_sizes = [len(d) for d in data_by_bin]
    tick_labels = [f"{k}" for k in bins]

    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=140)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    bp = ax.boxplot(
        data_by_bin,
        tick_labels=tick_labels,
        patch_artist=True,
        widths=0.55,
        boxprops=dict(facecolor=UNI_BLUE, alpha=0.78, edgecolor=BLACK, linewidth=1.4),
        medianprops=dict(color=BLACK, linewidth=2.2),
        whiskerprops=dict(color=BLACK, linewidth=1.4),
        capprops=dict(color=BLACK, linewidth=1.4),
        flierprops=dict(marker="o", markersize=5, markerfacecolor="none",
                        markeredgecolor=BLACK, alpha=0.9),
    )

    ax.set_xlabel("Assignments completados", fontsize=14, color=BLACK, fontweight="bold")
    ax.set_ylabel("X-Grade (nota final, 0 a 1)", fontsize=14, color=BLACK, fontweight="bold")
    ax.tick_params(axis="both", labelsize=12, colors=BLACK)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.22, color=UNI_GRAY, linestyle=":")
    ax.set_axisbelow(True)
    for spine_name, spine in ax.spines.items():
        if spine_name in {"top", "right"}:
            spine.set_visible(False)
        else:
            spine.set_color(BLACK)
            spine.set_linewidth(1.2)
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
    print("=== Estatisticas por bin (X-Grade) ===")
    for k, vals in zip(bins, data_by_bin):
        if len(vals) == 0:
            continue
        s = pd.Series(vals)
        print(
            f"  {k} assign. | n={len(vals):>3} | mediana={s.median():.2f} | "
            f"media={s.mean():.2f} | std={s.std():.2f}"
        )


if __name__ == "__main__":
    main()
