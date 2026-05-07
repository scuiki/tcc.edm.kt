"""Heatmap comparativo dos 5 assignments lado a lado. Salva PNG em results/."""
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

assignments = ['A439', 'A487', 'A492', 'A494', 'A502']
fig, axes = plt.subplots(1, 5, figsize=(30, 6))

for ax, aid in zip(axes, assignments):
    qm = pd.read_csv(ROOT / f'results/qmatrix_{aid}.csv', index_col=0)
    with open(ROOT / f'results/kc_descriptions_{aid}.json') as f:
        names = {f'kc_{kc["kc_id"]}': kc["name"] for kc in json.load(f)}
    qm = qm.rename(columns=names)
    sns.heatmap(qm, annot=True, fmt='d', cmap='Blues', cbar=False,
                linewidths=0.5, ax=ax)
    ax.set_title(f'{aid}\n({qm.shape[1]} KCs, {qm.values.mean():.0%} denso)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right', fontsize=7)

plt.suptitle('Q-matrices — todos os assignments', fontsize=14, y=1.02)
plt.tight_layout()

out = ROOT / 'results/qmatrix_all_heatmap.png'
plt.savefig(out, dpi=120)
print(f'Salvo em {out}')
