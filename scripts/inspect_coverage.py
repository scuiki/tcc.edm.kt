"""Cobertura por KC — quais problemas exigem cada KC, ordenado por frequência."""
import pandas as pd
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for aid in ['A439', 'A487', 'A492', 'A494', 'A502']:
    qm = pd.read_csv(ROOT / f'results/qmatrix_{aid}.csv', index_col=0)
    with open(ROOT / f'results/kc_descriptions_{aid}.json') as f:
        names = {f'kc_{kc["kc_id"]}': kc["name"] for kc in json.load(f)}
    qm = qm.rename(columns=names)
    print(f'\n=== {aid} ===')
    coverage = qm.sum(axis=0).sort_values(ascending=False)
    for kc_name, count in coverage.items():
        problems = list(qm.index[qm[kc_name] == 1])
        print(f'  [{count}/10] {kc_name}')
        print(f'         -> {problems}')
