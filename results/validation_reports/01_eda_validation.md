I have sufficient information to write the complete validation report.

---

STATUS: PASS

## Summary

The notebook `01_eda.ipynb` is a thorough, methodologically sound Exploratory Data Analysis. All required research criteria are met: key statistics are computed from data rather than hardcoded, the correct Release/Train split is used for comparisons with Shi et al. (2022), SEED=42 is applied consistently to all random operations, and the srcML/Compile.Error design decision is documented with appropriate citations. One minor factual inconsistency exists in a reference comment (student count attributed to the paper is "~410" while the documented and computed value is 329), but this does not affect any downstream analysis. No critical research integrity issues were found.

---

## Criteria Evaluation

### 1. Dados e Qualidade

**1.1 — Taxa de corretos em Release/Train [PASS]**

The benchmark cell computes correct rates for all candidate splits using `(runs['Score'] == 1.0).mean()` applied programmatically to each DataFrame. The output table shows:
- All: 19.65% | Train: 19.92% | Release/Train: **23.70%**

The markdown states: *"Release/Train apresenta 23.70% de corretos — diferença de apenas 0.02pp em relação aos 23.68% de Shi et al. (2022)"*. The divergence is explicitly acknowledged and attributed to rounding; the analysis correctly concludes Release/Train is the only comparable split. The value is computed, not hardcoded.

**One minor inconsistency:** The benchmark cell code comment and `print()` call state `"Referencia Code-DKT paper: ~410 estudantes"`, while the Release family has 246 (train) + 83 (test) = 329 students, consistent with the project's own documented fact ("329 estudantes"). The "~410" figure appears to be an erroneous paper attribution and should be corrected to 329, though it does not affect the analysis because the correct split is used and the 23.70% statistic is accurately computed.

**1.2 — Duplicate rows explicadas [PASS]**

The code computes `n_dups = all_main.duplicated(subset=['SubjectID', 'ProblemID', 'ServerTimestamp']).sum()` and prints the result (236,024). The markdown explicitly states: *"cada Run.Program gera um evento filho Compile com ParentEventID apontando para o EventID do pai e timestamp idêntico"* and *"Esses 236.024 registros não são erros — são a estrutura hierárquica esperada do ProgSnap2"*. No removal of these records is performed without justification.

**1.3 — Cobertura de CodeStateID [PASS]**

The code computes `pct_with_code = all_main['CodeStateID'].notna().mean() * 100` and prints `"Eventos COM CodeStateID: 360,176 (100.0%)"`. A separate check per EventType is also shown. The markdown confirms: *"CodeStateID tem cobertura de 100%"*. Section 6.2 additionally counts distinct CodeStateIDs per problem (mean 937) and reconfirms 100% coverage.

---

### 2. Compile.Error e Decisão do srcML

**2.1 — Proporção de Compile.Error quantificada [PASS]**

The event type distribution cell (Section 1.1.1) computes the proportion using value counts on `all_main['EventType']` and reports: *"Compile.Error: 109,020 (30.27%)"*. Section 6.1 additionally computes the CE rate within Release/Train submissions specifically (46.6% of RP+CE events), providing a second angle on the same phenomenon.

The link to srcML is explicitly made in the same finding markdown: *"O uso de srcML (Pankiewicz, Shi & Baker, 2025) permite incluir esses eventos como correct=0 na sequência KT, preservando informação de esforço mesmo em submissões não-compiláveis."*

**2.2 — Motivação para srcML documentada [PASS]**

Multiple cells address this:
- Section 1.1.1 context cell: *"BKT/DKT usam apenas Run.Program; Code-DKT com srcML inclui também Compile.Error"* (Price et al., 2020 cited)
- Section 6.1 finding: *"descartá-los (como no Code-DKT original com javalang) perde quase metade do sinal de aprendizado. Incluí-los como correct=0 na sequência KT, com features srcML, é a motivação central do srcML-DKT (Pankiewicz, Shi & Baker, 2025)"*
- Section 8.2 finding: *"n_compile_errors (Gini 0.003): justifica inclusão de Compile.Error na sequência Code-DKT"*

Pankiewicz, Shi & Baker (2025) is cited 6+ times throughout the notebook in appropriate context. The BKT/DKT vs Code-DKT filtering difference is clearly explained.

---

### 3. Estrutura de Assignments e Dificuldade

**3.1 — Taxa de acerto por problema calculada e visualizada [PASS]**

Section 3.2 (correct rate by problem) computes per-problem correct rates from Release/Train using `groupby(['AssignmentID', 'ProblemID'])` aggregations and produces a multi-panel barplot saved to `results/sec3_correct_rate_by_problem.png`. The markdown discusses a concrete difficulty ranking: A3 hardest (mean 19.1%, range 20.7pp), A5 easiest (mean 30.4%, range 43.5pp), with explicit within-assignment ranges cited per assignment.

**3.2 — Variabilidade entre assignments mencionada [PASS]**

Section 3.1 (Release/Train composition) reports per-assignment student counts (A1: 233, A2: 224, A3: 234, A4: 221, A5: 228 students) computed from data. The notebook confirms all 5 assignments have exactly 10 ProblemIDs each. Submission count variability by assignment is also shown in the Section 4 sequence distribution table.

---

### 4. Curvas de Aprendizado

**4.1 — Learning curves presentes e discutidas [PASS]**

Section 4.1 plots learning curves (correct rate vs attempt number, first 30 attempts) per assignment, saved to `results/sec4_learning_curves.png`. The findings markdown reports results for each direction:
- A1: positive trend (+6.6pp from attempts 1–5 to attempts 26–30)
- A2–A5: declining trends attributed to problem ordering effects within assignments

The interpretation is connected to modeling: the declining trends for A2–A5 are noted as a potential confound in the KT task (later problems in a sequence are harder, not that students are forgetting). Truncation at 50 attempts (Shi et al., 2022) is discussed in Section 4.2 with a computed statistic: 28.3% of student-assignment pairs exceed 50 attempts.

---

### 5. Score e Desbalanceamento

**5.1 — Análise de Score a partir dos dados [PASS]**

Two complementary Score analyses are present:
- **All split (Section 1.2.3):** computes `(runs['Score'] == 1.0).mean()` etc. → 19.65% correct, 36.86% partial; uses f-strings throughout
- **Release/Train (Section 5.1):** separate computation for modeling-relevant split → Score=0.0: 42.3%, Score=1.0: 23.7%, partial 34.0% (200 unique partial values); saved to `results/sec5_score_distribution.png`

Values are computed from data in both cases. The partial-score proportion (34.0% for Release/Train, 36.86% for All) differs between splits; the notebook does not explicitly address this cross-split difference in the partial score percentage, but both values are computed correctly from their respective data.

**5.2 — Imbalance ratio e justificativa de AUC [PASS]**

Section 5.2 computes imbalance ratios per assignment from Release/Train data: global 3.22:1; A3 worst (4.24:1), A5 best (2.29:1). The AUC justification is explicit and quantified: *"Um classificador-baseline ('sempre incorreto') atingiria 76.3% de acurácia sem nenhum poder discriminativo, evidenciando que acurácia é inadequada para este problema."* Shi et al. (2022) and Abdelrahman et al. (2022) are cited as supporting references.

---

### 6. Rastreabilidade Metodológica

**6.1 — SEED fixo [PASS]**

`SEED = 42` is declared as an explicit variable and passed as `random_state=SEED` to all stochastic operations:
- K-Means elbow search: `KMeans(n_clusters=k, random_state=SEED, n_init=10)`
- Silhouette analysis: `KMeans(n_clusters=k, random_state=SEED, n_init=10)`
- Final K-Means (k=3): `KMeans(n_clusters=K_BEST, random_state=SEED, n_init=10)`
- PCA: `PCA(n_components=2, random_state=SEED)`
- Decision Tree (Section 8.2): `SEED = 42` re-declared; `DecisionTreeClassifier(max_depth=5, random_state=SEED)`

The markdown explicitly acknowledges: *"K-Means com k=3 (SEED=42) sobre 453 estudantes."* No random operations appear without seed control.

**6.2 — Split correto [PASS]**

Section 1.2.1 documents the split anatomy: 506 vs 329 students, zero overlap, different semesters (Fall 2019 vs Spring 2019), computed from data. The benchmark cell (Section 1.2.5) correctly identifies Release/Train as the only comparable split and documents the conclusion. Sections 3–5 use Release/Train for all modelling-relevant computations. The markdown explicitly states: *"A análise exploratória usa All por ter maior volume de dados (506 estudantes vs 329); a modelagem final usa exclusivamente Release."*

**6.3 — Ausência de estatísticas hardcoded [PASS]**

All code cells use f-strings (`print(f'...: {variable}')`) or display computed DataFrames. Key statistics are dynamic:
- Event counts: `value_counts()` and `.shape`
- Correct rates: `.mean()` and `.sum()` on boolean Series
- Duplicate count: `.duplicated(...).sum()`
- CodeStateID coverage: `.notna().mean()`
- Imbalance ratios: GroupBy aggregations

Markdown cells summarize computed outputs in static text (standard Jupyter practice). In every case checked, the numbers in the markdown match the code cell outputs immediately preceding them. No evidence of invented values or systematic discrepancy between computed and reported statistics was found.

---

## Recommendations

1. **Fix the student-count reference in the benchmark cell (Section 1.2.5):** The comment and print statement say *"~410 estudantes"* as a paper reference, but the Release family has 329 students total (246 train + 83 test). This number should be corrected to 329 (or the paper source should be verified and cited explicitly). A reader cross-referencing this comment with the computed output (329 students) will notice the inconsistency.

2. **Cross-split partial score comparison (minor):** Section 1.2.3 reports 36.86% partial scores for All, while Section 5.1 reports 34.0% for Release/Train. A one-sentence note acknowledging that this cross-split difference exists (likely due to population/semester differences) would improve completeness.

3. **Document sequence artifact files:** The two artifact files (`sequences_bkt_dkt.pkl`, `sequences_code_dkt.pkl`) in `results/` are not mentioned anywhere in the EDA notebook. If they were generated as part of this notebook's pipeline, a cell should document their contents. If they were generated by the preprocessing notebook, this is not an issue for the EDA notebook.

---

## Verdict

STATUS: PASS
