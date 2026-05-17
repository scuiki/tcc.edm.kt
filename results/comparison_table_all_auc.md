## All-attempts AUC por assignment (mean +- std, %)

| Modelo    | A439          | A487          | A492          | A494          | A502          |
|:----------|:--------------|:--------------|:--------------|:--------------|:--------------|
| BKT       | 64.23         | 69.07         | 63.62         | 59.66         | 57.37         |
| DKT       | 70.89 +- 2.15 | 72.77 +- 1.18 | 76.66 +- 0.84 | 72.57 +- 2.79 | 72.48 +- 1.88 |
| Code-DKT  | 70.35 +- 0.67 | 74.89 +- 0.61 | 79.08 +- 0.74 | 75.07 +- 0.97 | 76.24 +- 0.77 |
| srcML-DKT | 67.25 +- 0.44 | 71.80 +- 0.51 | 75.80 +- 0.87 | 70.04 +- 0.92 | 72.59 +- 0.63 |


**Notas:**
1. BKT sem desvio padrão: modelo determinístico.
2. Métrica secundária (all-attempts AUC): todas as tentativas, comparavel com Piech et al. (2015).
3. Celula destacada (verde) = melhor modelo no assignment.
