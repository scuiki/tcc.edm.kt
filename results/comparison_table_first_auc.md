## First-attempt AUC por assignment (mean +- std, %)

| Modelo    | A439          | A487          | A492          | A494          | A502          |
|:----------|:--------------|:--------------|:--------------|:--------------|:--------------|
| BKT       | 63.21         | 68.40         | 54.20         | 57.81         | 56.92         |
| DKT       | 75.56 +- 3.40 | 76.70 +- 3.24 | 82.05 +- 1.66 | 80.17 +- 5.04 | 80.78 +- 4.01 |
| Code-DKT  | 73.27 +- 1.34 | 79.56 +- 0.76 | 86.12 +- 0.53 | 81.85 +- 0.98 | 84.98 +- 1.01 |
| srcML-DKT | 70.41 +- 1.01 | 76.56 +- 0.87 | 81.93 +- 0.71 | 78.30 +- 0.90 | 81.17 +- 0.99 |


**Notas:**
1. BKT sem desvio padrão: modelo determinístico; pickle nao inclui `pred_df` para bootstrap.
2. DKT, Code-DKT e srcML-DKT: seeds 42 a 51 (mesma faixa).
3. srcML-DKT treina com eventos `Compile.Error`; avaliacao no mesmo test set dos outros 3.
4. Code-DKT A439 = 73.27%%, alvo CLAUDE.md Criterio 1 (74.31%% +/-3pp): **satisfeito**.
5. Celula destacada (verde) = melhor modelo no assignment.
