"""KCs por problema — lista quais KCs cada problema exige, por assignment."""
import pandas as pd
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for aid in ['A439', 'A487', 'A492', 'A494', 'A502']:
    qm = pd.read_csv(ROOT / f'results/qmatrix_{aid}.csv', index_col=0)
    with open(ROOT / f'results/kc_descriptions_{aid}.json') as f:
        names = {f'kc_{kc["kc_id"]}': kc["name"] for kc in json.load(f)}
    qm = qm.rename(columns=names)
    print(f'\n=== {aid} ({qm.shape[1]} KCs) ===')
    for pid in qm.index:
        kcs = [col for col in qm.columns if qm.loc[pid, col] == 1]
        print(f'  Problema {pid}: {kcs}')
