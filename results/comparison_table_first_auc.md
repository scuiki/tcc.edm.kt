## First-attempt AUC por assignment (%)

| Modelo    |   A439 |   A487 |   A492 |   A494 |   A502 |
|:----------|-------:|-------:|-------:|-------:|-------:|
| BKT       |  63.21 |  68.4  |  54.2  |  57.81 |  56.92 |
| DKT       |  75.56 |  76.7  |  82.05 |  80.17 |  80.78 |
| Code-DKT  |  73.27 |  79.56 |  86.12 |  81.85 |  84.98 |
| srcML-DKT |  70.41 |  76.56 |  81.93 |  78.3  |  81.17 |


**Notas:**
1. BKT sem desvio padrão: modelo determinístico; pickle nao inclui `pred_df` para bootstrap.
2. DKT, Code-DKT e srcML-DKT: seeds 42 a 51 (mesma faixa).
3. srcML-DKT treina com eventos `Compile.Error`; avaliacao no mesmo test set dos outros 3.
4. Code-DKT A439 = 73.27%%, alvo CLAUDE.md Criterio 1 (74.31%% +/-3pp): **satisfeito**.
5. Celula destacada (verde) = melhor modelo no assignment.
