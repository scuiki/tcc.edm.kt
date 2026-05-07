"""Heatmap da Q-matrix de um assignment específico. Salva PNG em results/.

Uso:
    python3 scripts/viz_qmatrix_single.py          # default: A439
    python3 scripts/viz_qmatrix_single.py A494
"""
import sys
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

aid = sys.argv[1] if len(sys.argv) > 1 else 'A439'

qm = pd.read_csv(ROOT / f'results/qmatrix_{aid}.csv', index_col=0)
with open(ROOT / f'results/kc_descriptions_{aid}.json') as f:
    names = {f'kc_{kc["kc_id"]}': kc["name"] for kc in json.load(f)}
qm = qm.rename(columns=names)

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(qm, annot=True, fmt='d', cmap='Blues', cbar=False,
            linewidths=0.5, ax=ax)
ax.set_title(f'Q-matrix {aid} — ProblemID × KC')
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right', fontsize=8)
plt.tight_layout()

out = ROOT / f'results/qmatrix_{aid}_heatmap.png'
plt.savefig(out, dpi=150)
print(f'Salvo em {out}')
