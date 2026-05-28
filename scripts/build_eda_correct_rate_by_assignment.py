"""Gera barras horizontais de taxa de acerto por assignment (Spring 2019).

Lê data/CSEDM/MainTable.csv, filtra EventType == 'Run.Program', calcula
% correto por assignment (Score == 1.0) e salva PNG na paleta UniFacens
em results/ e apresentacao/assets/.

Uso: python3 scripts/build_eda_correct_rate_by_assignment.py
"""
from pathlib import Path
import shutil

import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "data" / "CSEDM" / "MainTable.csv"
OUT_RESULTS = REPO_ROOT / "results" / "sec3_correct_rate_by_assignment.png"
OUT_ASSETS = REPO_ROOT / "apresentacao" / "assets" / "eda-taxa-acerto-por-assignment.png"

UNI_BLUE = "#2667FF"
UNI_INK = "#1f1f1f"
UNI_GRAY = "#5b6472"


def main() -> None:
    df = pd.read_csv(CSV_PATH, low_memory=False)
    run = df[df["EventType"] == "Run.Program"].copy()

    grouped = (
        run.groupby("AssignmentID")
        .agg(n_attempts=("Score", "size"), n_correct=("Score", lambda s: (s == 1.0).sum()))
        .reset_index()
        .sort_values("AssignmentID")
    )
    grouped["rate_pct"] = grouped["n_correct"] / grouped["n_attempts"] * 100
    grouped["label"] = grouped["AssignmentID"].apply(lambda a: f"A{['',1,2,3,4,5][[439,487,492,494,502].index(int(a))+1]} ({int(a)})")

    fig, ax = plt.subplots(figsize=(8.6, 2.6), dpi=160)
    bars = ax.barh(
        grouped["label"],
        grouped["rate_pct"],
        color=UNI_BLUE,
        height=0.55,
        edgecolor=UNI_INK,
        linewidth=0.6,
    )

    for bar, val in zip(bars, grouped["rate_pct"]):
        ax.text(
            val + 0.6,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}%".replace(".", ","),
            va="center",
            ha="left",
            fontsize=11,
            color=UNI_INK,
            fontweight="bold",
        )

    ax.invert_yaxis()
    ax.set_xlim(0, 40)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xticklabels(["0%", "10%", "20%", "30%", "40%"], fontsize=10, color=UNI_GRAY)
    ax.tick_params(axis="y", labelsize=11, colors=UNI_INK)
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine_name, spine in ax.spines.items():
        if spine_name in {"top", "right"}:
            spine.set_visible(False)
        elif spine_name == "bottom":
            spine.set_color(UNI_GRAY)
            spine.set_linewidth(0.8)
        else:
            spine.set_visible(False)

    ax.grid(axis="x", linestyle=":", linewidth=0.6, color=UNI_GRAY, alpha=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout(pad=0.4)
    OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_RESULTS, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    OUT_ASSETS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT_RESULTS, OUT_ASSETS)

    print(f"OK: {OUT_RESULTS.relative_to(REPO_ROOT)}")
    print(f"OK: {OUT_ASSETS.relative_to(REPO_ROOT)}")
    print(grouped[["label", "n_attempts", "n_correct", "rate_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
