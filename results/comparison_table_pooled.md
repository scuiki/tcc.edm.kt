## AUC pooled cross-assignment (%)

| Modelo    | First-attempt AUC (pooled)   | All-attempts AUC (pooled)   |
|:----------|:-----------------------------|:----------------------------|
| BKT       | N/A                          | N/A                         |
| DKT       | 79.80 (seed=42, 1 run)       | 73.62 (seed=42, 1 run)      |
| Code-DKT  | 81.55 (seed=42, 1 run)       | 75.61 (seed=42, 1 run)      |
| srcML-DKT | 78.04 +- 0.41                | 72.19 +- 0.41               |


**Notas:**
1. AUC sobre predicoes concatenadas dos 5 assignments (1 AUC por run).
2. BKT = N/A: pred_df nao persistido no pickle (ver plano §2.3).
3. DKT e Code-DKT: pred_df disponivel apenas no seed=42; valor pontual reportado.
4. srcML-DKT: pred_df em todos os 10 seeds; mean +- std sobre 10 runs.
5. Comparavel com Pankiewicz et al. (2025) Table 3 (dataset diferente: C#, 610 alunos).
