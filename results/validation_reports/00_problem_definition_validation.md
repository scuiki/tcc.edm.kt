I now have all the information needed for the validation report.

---

STATUS: MINOR_ISSUES

## Summary

The notebook `00_problem_definition.ipynb` establishes a methodologically sound foundation for the TCC 1 Knowledge Tracing comparison. The core decisions — KC=ProblemID, first-attempt AUC as primary metric, use of the Release split, SEED=42, and the 5-model structure — are all documented with appropriate citations and backed by empirical evidence from the data. The summary table in Section 6 is comprehensive. Two minor gaps exist: (1) the formal research question in Section 5 is misaligned with the actual TCC 1 scope, and (2) BKT's input/mechanism is not described with the same specificity as DKT and Code-DKT. Cross-checking with the serialised artifacts (`sequences_bkt_dkt.pkl`, `sequences_code_dkt.pkl`) confirms that the notebook's claims about assignment IDs, sequence length cap, and seed are internally consistent.

---

## Criteria Evaluation

### 1.1 — KC=ProblemID documented with justification [PASS]

Section 1 (cell `a0000004`) explicitly states: *"KC = ProblemID: cada problema individual dentro de um assignment é uma unidade de conhecimento distinta"*, citing Shi et al. (2022) footnote 1 verbatim. Three independent justifications are given: (a) one model per assignment to avoid cross-assignment contamination, (b) protocol replication of Shi et al. (2022), (c) direct AUC comparability with the paper. The summary table repeats the citation.

### 1.2 — Scope of modeling clear [PASS]

Cell `a0000005` computes the actual KC distribution from `early.csv`/`late.csv` and prints a table showing exactly 5 assignments (IDs: 439, 487, 492, 494, 502), each with 10 ProblemIDs. Cell `805463d4` synthesises: *"5 modelos independentes, um por assignment, com KC=ProblemID"* and specifies the DKT input dimension `2 × 10`. This is independently confirmed by the pkl artifacts: `assignment_ids = [439, 487, 492, 494, 502]`, `max_len = 50`.

### 2.1 — First-attempt AUC as primary metric [PASS]

Cell `74e1a211` defines first-attempt AUC as primary and provides two explicit justifications: autocorrelation elimination (*"tentativas subsequentes do mesmo par (estudante, problema) são estatisticamente dependentes, inflando artificialmente o AUC"*) and direct comparability with Table 2 of Shi et al. (2022). The justification is grounded in empirical evidence computed in the same notebook: 64.6% of (student, problem) pairs have more than one attempt (median = 2, max = 177), making autocorrelation a concrete concern.

### 2.2 — All-attempts AUC as secondary metric [PASS]

Cell `74e1a211` defines all-attempts AUC as secondary with two justifications: larger N for statistical stability and comparability with Piech et al. (2015) / Table 1 of Shi et al. (2022). The complementary role is clearly articulated: *"Reportada para complementar a comparação com a literatura mais ampla, mas não usada como critério de seleção de modelo."*

### 2.3 — Operational definition of "first attempt" [MINOR]

The notebook says first-attempt AUC *"avalia a predição na primeira tentativa de cada estudante em cada problema"* — this correctly identifies the unit (student × problem), but does not specify that ordering is by `ServerTimestamp`. A reader implementing the metric from this description alone would need to infer the temporal ordering mechanism. This is a documentation gap, not a methodological flaw.

### 3.1 — Summary table or section present [PASS]

Section 6 (cell `a0000012`) contains a 10-row table covering: KC definition, training structure, evaluation split, primary metric, secondary metric, label files, score threshold, Compile.Error treatment, sequence truncation length, and seed. All critical decisions are covered with a justification column.

### 3.2 — Three models referenced [MINOR]

BKT, DKT, and Code-DKT are all named in cells `a0000002` and `a0000004`. DKT input (`2 × 10 one-hot`) and Code-DKT input (DKT + code vector concatenated to LSTM) are described. However, BKT's input representation (4-parameter model: P(L₀), P(T), P(G), P(S), applied per-KC sequence) is never described. A reviewer cannot reconstruct what BKT receives as input from the notebook alone, which slightly weakens the comparative characterisation. The pkl artifact `description` field confirms the BKT/DKT distinction (`Run.Program`, `correct=(Score==1.0)`) but this is not surfaced in the notebook text.

### 4.1 — Citations present and correct [PASS]

Shi et al. (2022) is cited in cells `a0000004`, `a0000010`, `74e1a211`, and `a0000012` — always in context (KC definition, metric choice). Pankiewicz, Shi & Baker (2025) is cited in `a0000004` and `a0000012` in the context of Compile.Error / srcML treatment. Abdelrahman et al. (2022) appears in `a0000004` and `a0000010`. Piech et al. (2015) appears in `74e1a211` and `a0000012`. Citations are distributed throughout the relevant sections, not deferred to a bibliography appendix.

### 4.2 — Fixed seed documented [PASS]

`SEED = 42` is defined in the setup cell (`a0000003`). The summary table explicitly records: *"Seed fixo | 42 | Reprodutibilidade obrigatória em todos os notebooks"*. Both pkl artifacts carry `seed: 42`, consistent with the notebook's claim.

### Additional Finding — Research Question misalignment [MINOR]

Section 5 (cell `a0000011`) states the research question as:

> *"KCs gerados de forma automática via análise de AST (srcML) + inferência de LLM melhoram a capacidade preditiva (AUC) dos modelos de Knowledge Tracing em relação ao baseline KC = AssignmentID?"*

This research question is inconsistent with the TCC 1 scope in two ways: (a) KC=AssignmentID is not the baseline being compared — the baseline throughout the notebook is KC=ProblemID; (b) LLM-generated KCs (referenced in Duan et al., 2025) are not among the three models being compared (BKT, DKT, Code-DKT). This language appears to be a draft/placeholder oriented toward a future extension (possibly TCC 2) that was not updated to reflect the finalised scope. Because this cell is standalone and every other section of the notebook is internally consistent, the practical impact is limited, but it risks confusing an external reader about the actual hypothesis being tested.

---

## Recommendations

1. **[2.3] Operational definition of first attempt**: Add one sentence specifying the ordering: *"A primeira tentativa é determinada pela primeira ocorrência de (SubjectID, ProblemID) ordenada por `ServerTimestamp`."* This ensures reproducibility without ambiguity.

2. **[3.2] BKT input description**: Add a brief description of BKT's inputs to the model comparison. For example: *"BKT: modela P(aprendizado) por KC com 4 parâmetros estimados por EM sobre a sequência binária de acerto/erro de um único KC por estudante."* This brings BKT's description to the same level of specificity as DKT and Code-DKT.

3. **[Section 5] Research question**: Rewrite the research question to match TCC 1's actual scope: *"Code-DKT (com representação de código via srcML) supera BKT e DKT na predição de first-attempt AUC para os assignments do CSEDM?"* The current LLM/KC=AssignmentID framing should either be removed or explicitly scoped to TCC 2.

---

## Verdict

STATUS: MINOR_ISSUES
