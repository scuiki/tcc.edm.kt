Now I have all the information needed to write the validation report.

---

STATUS: MINOR_ISSUES

## Summary

`notebooks/02_preprocessing.ipynb` is a methodologically sound preprocessing pipeline that correctly implements the core decisions required for reproducible Knowledge Tracing experiments on the CSEDM dataset. The split documentation, filtering logic, sequence construction, truncation, and artefact serialisation all demonstrate rigorous implementation with appropriate assertions. The benchmark reproducibility check (23.70% vs paper's 23.68%) passes. Two minor gaps were identified: (1) the Score==1.0 threshold choice is implicitly accepted from Shi et al. (2022) but the ~37% partial-score fact is never stated nor explicitly justified in the notebook prose; and (2) the `is_first_attempt` integrity assertion after truncation is performed only on BKT/DKT sequences, not on Code-DKT sequences, leaving an unverified edge case that could affect the primary metric computation for Code-DKT.

---

## Criteria Evaluation

### 1. Filtragem por Modelo

**1.1 filter_for_bkt_dkt usa apenas Run.Program** [PASS]

Explicit `assert set(bkt_dkt_train['EventType'].unique()) == {'Run.Program'}` passes at cell `26288004`. The `correct` column is asserted to be binary. Output confirms 46,825 events in Release/Train, all of type `Run.Program`, with 23.70% correct — exactly consistent with the benchmark. No leakage from other EventTypes is possible given the hard set-equality assertion.

**1.2 filter_for_code_dkt inclui Compile.Error** [PASS]

`assert set(code_dkt_train['EventType'].unique()).issubset({'Run.Program', 'Compile.Error'})` passes. Output shows 46,825 Run.Program + 40,858 Compile.Error = 87,683 events in Release/Train. The markdown in cell `0b15e904` explicitly references both Shi et al. (2022) and Pankiewicz, Shi & Baker (2025) for the Compile.Error inclusion decision. The description field of the serialised artefact (`'Sequências KT para Code-DKT — Run.Program + Compile.Error (correct=0)'`) further documents this choice permanently.

**1.3 Justificativa do threshold Score==1.0** [MINOR]

The threshold `Score == 1.0` is applied (evidenced by the 23.70% correct rate matching Shi et al.'s reported 23.68%) and cited via Shi et al. (2022) Section 3.1 ("correct=1 when all tests pass"). However, the notebook never explicitly states that ~37% of executions have partial scores (0 < Score < 1) and never explicitly argues why partial scores are treated as incorrect rather than, e.g., using a threshold of Score > 0 or Score ≥ 0.5. Cell `8ba1410e` discusses class imbalance in terms of AUC vs accuracy but does not address the partial-score distribution. This is a documentation gap: a reader unfamiliar with CSEDM specifics cannot independently evaluate whether Score==1.0 is the most defensible choice without consulting the paper.

---

### 2. Construção de Sequências

**2.1 Ordenação temporal garantida** [PASS]

Cell `552c6234` asserts `ts.is_monotonic_increasing` for every sequence in A1 (BKT/DKT), with `ServerTimestamp` as the ordering column. The assertion iterates over all sequences in the assignment and would raise if any were out of order. The output confirms "OK — ordenação cronológica verificada em todas as sequências." The dtype table in cell `27d24a12` confirms `ServerTimestamp` is `datetime64[us, UTC]`, ensuring timezone-aware comparison.

**2.2 Flag de primeira tentativa presente** [MINOR]

For BKT/DKT, cell `552c6234` asserts `first_counts == 1` for every ProblemID before truncation, and cell `e8d8fc8d` re-asserts this after truncation — confirming that `truncate_sequences` recalculates the flag for the truncated window rather than inheriting the original flags. Both assertions pass with explicit output. However, the equivalent post-truncation assertion is **not performed for Code-DKT sequences**. Given that Code-DKT sequences contain Compile.Error events which do not directly correspond to problem attempts, the interaction between these events and `is_first_attempt` calculation in the truncated window is unverified. If `is_first_attempt` is set only on Run.Program events and a student's first Run.Program for a problem falls outside the last-50 window while Compile.Error events for that problem do fall within it, the is_first_attempt flag would be absent for that problem — silently dropping it from first-attempt AUC computation for Code-DKT. This edge case is unverified.

**2.3 Estrutura das sequências documentada** [PASS]

The markdown in cell `0c78cb38` contains a detailed two-tier schema table: outer dict fields (`subject_id`, `assignment_id`, `events`) and all columns of the `events` DataFrame, with types and descriptions. An example sequence showing the first 6 events is also printed. The markdown in cell `bda503c4` repeats and extends this schema documentation. Structure is thoroughly documented.

---

### 3. Truncagem e Integridade

**3.1 Truncagem em 50 implementada corretamente** [PASS]

Cell `e8d8fc8d` asserts `all(len(seq['events']) <= MAX_LEN for seq in seqs)` for every assignment and both BKT/DKT and Code-DKT — output confirms it passes. The markdown in cell `d902ec7a` explicitly states "Shi et al. (2022) truncam cada sequência de estudante nas **últimas** 50 tentativas" (emphasis on *últimas* = last), and the increase in correct rate after truncation (+4.27pp for BKT/DKT, +7.21pp for Code-DKT) empirically confirms that the last-50 direction is correctly implemented (retaining recent events where students perform better). The reference to Shi et al. (2022) Section 3 is present.

**3.2 Impacto da truncagem reportado** [PASS]

Cell `e8d8fc8d` outputs a per-assignment table reporting: number of sequences, number truncated, percentage truncated, average length before and after. The correct rate before and after truncation is also calculated across all assignments. The max truncation rate is 39.3% (A492, BKT/DKT) and 67.4% (A487, Code-DKT), with quantitative justification of why Code-DKT is more affected. The total event count (36,497 post-truncation for BKT/DKT train, vs the raw 46,825 Run.Program events) allows readers to calculate discarded events (≈10,328 events), though this specific figure is not stated explicitly in the truncation section — it is recoverable from the artefact statistics in cell `c154834c`.

---

### 4. Split e Reprodutibilidade

**4.1 Split correto documentado** [PASS]

The opening markdown table in cell `564d59a7` clearly distinguishes All/ (Fall-2019, set–dez, 506 students) from Release/ (Spring-2019, fev–mai, 329 students) and states "populações não se sobrepõem" and "usar sempre `Release/Train` para treino e `Release/Test` para teste." The notebook loads and uses `release_train` and `release_test` throughout.

**4.2 Taxa de corretos pós-processamento reportada** [PASS]

Cell `a41fa13b` explicitly computes the correct rate in Release/Train (23.7010%), states the paper value (23.6800%), and computes the divergence (0.0210pp). The comment explicitly attributes this to rounding — a plausible and expected explanation. This constitutes a rigorous first-order reproducibility check.

---

### 5. Artefatos e Rastreabilidade

**5.1 Artefatos gerados e documentados** [PASS]

Both `results/sequences_bkt_dkt.pkl` and `results/sequences_code_dkt.pkl` are generated by cell `c154834c` and confirmed to exist (9,613.5 KB and 10,617.8 KB). The outer schema (6 keys: `train`, `test`, `assignment_ids`, `max_len`, `seed`, `description`) and inner schema (sequence dict fields and `events` DataFrame columns) are documented in both the printed output and the subsequent markdown cell `bda503c4`. The artefact structure was verified by direct pickle inspection: both files have the correct top-level structure.

**5.2 Estatísticas dos artefatos reportadas** [PASS]

Cell `c154834c` computes and prints per-split statistics for both artefacts: number of assignments with data, unique students, total sequences, min/mean/max length, total events, and correct rate. Per-assignment breakdowns are also included. All values are computed programmatically from the artefacts, not hardcoded. The unique student count (246 train, 83 test) is consistent with the split sizes reported in cell `486b3c46`.

**5.3 SEED fixo presente** [PASS]

`SEED = 42` is defined in the first code cell, `np.random.seed(SEED)` is called, and `seed` is stored as a field in both serialised artefacts. All preprocessing operations (filtering, sorting, grouping) are deterministic given fixed data; no stochastic operations were identified in the notebook that would require additional seed setting.

---

### 6. Qualidade da Implementação

**6.1 Ausência de placeholders** [PASS]

No `pass`, `TODO`, `NotImplementedError`, or other placeholder patterns appear in any code cell of the notebook. All functions (`filter_for_bkt_dkt`, `filter_for_code_dkt`, `build_sequences`, `truncate_sequences`) are imported from `src/data_loader.py` and produce non-trivial outputs verified by assertions.

**6.2 Código reproduzível** [PASS]

The notebook uses `Path().resolve()` relative to the notebook directory to construct all paths. SEED is fixed. All operations are deterministic. The only external dependency is `src/data_loader.py`, which is part of the repository. Executing the notebook from scratch in an environment with CSEDM data present will produce identical artefacts.

---

## Recommendations

1. **Criterion 1.3 — Document the Score==1.0 threshold choice explicitly.** Add a markdown sentence (in Section 2.1 or a dedicated sub-section) stating: "~37% of Run.Program events have partial scores (0 < Score < 1); these are treated as incorrect (correct=0) for binary KT, following Shi et al. (2022) who define correct=1 only when all tests pass (Score==1.0). Alternative thresholds (Score>0, Score≥0.5) are not used as they would conflate partial and full understanding, inflating the positive class."

2. **Criterion 2.2 — Add is_first_attempt assertion for Code-DKT after truncation.** In cell `e8d8fc8d`, add the same `first_counts == 1` assertion loop over `seqs_code_trunc`. If Compile.Error events are never marked `is_first_attempt=True` (which is the expected and correct behaviour), the assertion should still verify that every ProblemID that appears in the truncated Code-DKT window has exactly one Run.Program event marked as `is_first_attempt=True`.

3. **Minor — Report total events discarded by truncation.** In the truncation impact section, add one line computing `total_discarded = sum(len(s['events']) for seqs in seqs_bkt_all.values() for s in seqs) - sum(len(s['events']) for seqs in seqs_bkt_trunc.values() for s in seqs)` and state the percentage of events removed. This rounds out the truncation impact narrative.

---

## Verdict

STATUS: MINOR_ISSUES
