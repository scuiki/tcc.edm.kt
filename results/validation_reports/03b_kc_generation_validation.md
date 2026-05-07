Now I have all the information needed to write the validation report.

---

STATUS: CRITICAL_ISSUES

## Summary

The notebook `03b_kc_generation.ipynb` implements Etapas 1–5 of the 7-step KCGen-KT pipeline (Duan et al., 2025) with high methodological fidelity: diversity sampling, LLM-based KC generation, Sentence-BERT + HAC clustering, LLM cluster labeling, and Q-matrix construction are all correctly implemented, well-cited, and produce verified artefacts. However, Etapas 6 (KC Correctness Labeling) and 7 (AST Signatures / post-hoc validation with srcML) are entirely absent from the notebook — no code cells, no markdown sections, no output, and no corresponding artefacts on disk. The mandatory artefacts `kc_correctness_A*.json` and `ast_signatures_A*.json` do not exist. This makes Criteria 6, 7, and significant portions of Criterion 8 unverifiable.

---

## Criteria Evaluation

### 1. Diversity Sampling

**1.1 Estratificação por tentativas antes do acerto** — [PASS]

`_bucket_for()` maps `total_attempts` into exactly 5 buckets: 1, 2–3, 4–6, 7–10, >10. `diversity_sample()` picks one sample per occupied bucket. Duan et al. (2025, Table 5) is cited explicitly in the markdown preceding the implementation. The bucket boundaries are correctly derived from `total_attempts` (= `n_attempts_before + 1`), which is a faithful proxy for difficulty stratification.

**1.2 Número correto de amostras** — [PASS]

`n=5` is the hardcoded default in `diversity_sample()`. The markdown cites the exact AUC values from Table 5 (n=1: 0.798, n=3: 0.807, **n=5: 0.812**, n=7: 0.811, n=10: 0.810), correctly justifying the choice. Observed output: mean 4.94 samples/problem, distribution {5: 47, 4: 3} across all 50 problems — consistent with some buckets being empty for rare problems.

**1.3 Uso exclusivo do Release/Train** — [PASS]

`SEQUENCES_PATH` points to `results/sequences_bkt_dkt.pkl`. The loading code accesses `artifact["train"]` exclusively, and the markdown explicitly states "Uso exclusivo de `Release/Train` (mesma população de Shi et al., 2022) para evitar data leakage."

---

### 2. Geração de KCs via LLM

**2.1 Código bruto como input (não AST)** — [PASS]

Raw Java code is sent in the LLM prompt. The markdown explicitly states: "LLM recebe código bruto — NÃO AST (Table 4: AST-only piora AUC de 0.812 → 0.784)." The docstring for `generate_kcs_for_problem` further reads: "Input: raw student code. Decision: Duan et al. (2025) Table 4 ablation shows AST degrades AUC 0.812 → 0.784." The ablation reasoning is cited twice and is architecturally enforced.

**2.2 In-context examples presentes** — [PASS]

`_FEW_SHOT_EXAMPLES` contains two worked examples (array sum; letter grade mapping) adapted from Duan et al. (2025) Appendix B (Table 8). The code comment cites Table 8 explicitly. Both examples use introductory Java problems of compatible granularity with the CSEDM (3–4 KCs, 3–8 words each). The markdown cites the ablation: "Ablação sem in-context examples: AUC 0.782 (−3pp) vs. base 0.812 — exemplos são obrigatórios."

**2.3 Output estruturado correto** — [PASS]

Expected LLM output: `{"problem_description": str, "kcs": [{"name": str, "reasoning": str}]}`. JSON parsing is robust: strips markdown code fences, finds outermost JSON object to handle preamble text, and has two `assert` statements verifying field presence. Executed output confirms 5.5–6.0 KCs per problem on average across all assignments.

**2.4 Cache obrigatório implementado** — [PASS]

The loop checks `if cache_path.exists()` before any LLM call and writes immediately after generation. All 5 `kc_raw_A*.json` files are on disk and loaded as cache hits in the executed output. The assertion `assert not missing` at the end enforces completeness.

---

### 3. Clustering

**3.1 Embeddings semânticos usados** — [PASS]

`SentenceTransformer("all-MiniLM-L6-v2")` is used. The constant `EMBEDDING_MODEL` is named and the markdown documents the choice. Embeddings are computed on KC names (strings), not on Java code. `normalize_embeddings=True` ensures cosine-compatible vectors.

**3.2 HAC com distância cosseno** — [PASS]

Cosine distance is computed via `pdist(embeddings, metric="cosine")` with a floating-point clamp. `linkage(..., method="average")` implements UPGMA. `fcluster` produces the final assignments. Linkage method ("average") is visible in the code but not commented in the markdown section — a very minor documentation gap, not a research integrity issue.

**3.3 Granularidade alvo documentada** — [PASS]

`N_CLUSTERS_CANDIDATES = [10, 12, 15]` is tested for all assignments. Silhouette score selects the best: 15 clusters for A439/A487/A492/A494, 12 for A502. The markdown explains the selection criterion (silhouette score) and interprets the result for A502 (inversion at 15 indicates naturally compact KC space). Final counts (12–15 for 10 problems) are within the stated target range and consistent with Duan et al. (2025)'s ~1 cluster/problem guideline.

**3.4 Reproduzibilidade** — [PASS]

`SEED = 42` is set globally and `np.random.seed(SEED)` is called again before the embedding step. HAC is deterministic given fixed inputs. The embedding model is deterministic once loaded. All clustering results are cached in `kc_clusters_A*.json`.

---

### 4. Rotulagem de Clusters via LLM

**4.1 Prompt de rotulagem baseado em Duan et al.** — [PASS]

The system prompt and user prompt are adapted from Duan et al. (2025) Table 9. The code comment reads: `"We prompt the LLM to either select the most representative KC from the cluster or synthesize a new label capturing the shared concept." — Section 3.1.2.` The decision instruction ("select existing KC vs. synthesize new label") is faithfully reproduced in the prompt body.

**4.2 Cache implementado** — [PASS]

`if cache_path.exists()` guard is present for `kc_descriptions_{aid_str}.json` before any API call. All 5 description files are on disk and the executed output shows all 5 as cache hits. The assertion at the end verifies completeness.

**4.3 KCs finais interpretáveis** — [PASS with minor caveat]

The notebook generates a display table of canonical KCs for A439. In the executed output this renders as `<IPython.core.display.Markdown object>` — the table content is rendered in a live browser session but is not embedded as text in the stored notebook output. The artefact files (`kc_descriptions_A*.json`) contain the KC names and reasoning. The number of canonical KCs (12–15) is within the 10–15 target range. From the available artefacts: A487 has 15 readable KC names (e.g., string indexing, helper methods, conditional logic) — semantically interpretable. The minor caveat is that the human-readable table is not preserved in notebook output, requiring inspection of artefact files to verify KC names.

---

### 5. Q-matrix

**5.1 Formato correto** — [PASS]

`ProblemID` is the DataFrame index; columns are `kc_0, kc_1, ..., kc_N`. Values are 0 or 1 (set via integer list construction). Verified from actual CSV files: A439 has columns `kc_0` through `kc_14`; A502 has columns `kc_0` through `kc_11`.

**5.2 Cobertura completa** — [PASS]

Explicit validation: `no_kc_mask = qmat.sum(axis=1) == 0` with assertion. Executed output confirms "all 10 problems have ≥1 KC — OK" for all 5 assignments.

**5.3 Estatísticas reportadas** — [PASS]

The printed Q-matrix Statistics table reports n_KCs, n_problems, density, max_KCs_per_problem, and problem_id_max — all computed from the data via pandas operations (not hardcoded). Density range 26–32% is in the expected 20–40% band. Max KCs per problem is 6 for all assignments.

**5.4 Per-assignment independente** — [PASS]

Five separate CSV files, each with independent KC vocabulary. A502 has 12 KC columns; the other four have 15. No cross-contamination of column names across assignments (each uses the same generic `kc_i` scheme, but the cluster identities are per-assignment).

---

### 6. KC Correctness Labeling

**6.1 Escopo correto das submissões** — [CRITICAL]

**Etapa 6 is entirely absent.** The notebook has 19 cells (0–18) and ends at Etapa 5 (Q-matrix). No code or markdown section for KC correctness labeling exists. The file `results/kc_correctness_A*.json` does not exist for any assignment.

**6.2 Prompt baseado em Duan et al. Table 10** — [CRITICAL]

No prompt for correctness labeling is implemented. Table 10 is not referenced in any implemented cell. The criterion is unverifiable.

**6.3 Cache por assignment** — [CRITICAL]

No cache logic for `kc_correctness_A*.json` exists. No artefacts on disk.

**6.4 Custo e escala documentados** — [MINOR]

The introductory markdown mentions "~$39–40" total cost and `claude-haiku-4-5-20251001` as the model. The ~26,289 incorrect submissions figure is not stated anywhere in the notebook. This partial documentation exists only in the overview, not in the missing implementation section.

---

### 7. AST Signatures (Validação Post-Hoc)

**7.1 srcML invocado corretamente** — [CRITICAL]

**Etapa 7 is entirely absent.** No subprocess call to `srcml`, no extraction function, and no `ast_signatures_A*.json` artefacts on disk.

**7.2 Uso como validação, não como input LLM** — [CRITICAL]

No code exists to evaluate. The introductory markdown briefly mentions "Validação post-hoc com srcML" as one of the 7 pipeline steps but the section was never implemented.

**7.3 Análise de interpretabilidade presente** — [CRITICAL]

No comparison of KCs to AST signatures, no interpretability analysis, no evidence that the generated KCs are anchored to observable code structures.

---

### 8. Artefatos e Rastreabilidade

**8.1 Todos os artefatos obrigatórios gerados** — [CRITICAL]

Present on disk:
- `qmatrix_A*.csv` — 5/5 ✓
- `kc_raw_A*.json` — 5/5 ✓
- `kc_clusters_A*.json` — 5/5 ✓
- `kc_descriptions_A*.json` — 5/5 ✓

Missing:
- `ast_signatures_A*.json` — **0/5** ✗
- `kc_correctness_A*.json` — **0/5** ✗

Of the 10 mandatory artefacts (`qmatrix_*` + `ast_signatures_*`), only 5 exist. The 10 intermediate files are split 20 present / 10 absent.

**8.2 Schemas documentados** — [MINOR]

For Etapas 1–5, schemas are documented via docstrings (return type descriptions with key names and types) and markdown. For Etapas 6–7, no schemas exist because the sections are not implemented.

**8.3 Reproduzibilidade com cache** — [MINOR]

Etapas 1–5: fully reproducible — all LLM calls are cache-guarded and artefacts are on disk. Etapas 6–7: not applicable as they are absent. A full re-execution of the notebook as written would not trigger any new LLM calls and would produce the same Etapas 1–5 artefacts, but Etapas 6–7 would remain absent.

**8.4 Ausência de placeholders** — [MINOR]

No `pass`, `TODO`, `NotImplementedError`, or `...` within the implemented cells (Etapas 1–5). The absence is structural, not placeholder-based — Etapas 6 and 7 simply do not exist as cells.

---

## Recommendations

1. **Implement Etapa 6 (KC Correctness Labeling):** Add code cells that (a) load incorrect `Run.Program` submissions from Release/Train, (b) construct a prompt based on Duan et al. (2025) Table 10 with `error_reasoning` and `kc_errors` output fields, (c) implement per-assignment cache (`kc_correctness_A{aid}.json`), and (d) report the ~26,289 submission count and ~$39 cost estimate explicitly in a markdown cell.

2. **Implement Etapa 7 (AST Signatures):** Add a function that calls `srcml` via `subprocess` on representative correct submissions, extracts node-type frequency counts (`ForStatement`, `IfStatement`, `WhileStatement`, etc.), saves `ast_signatures_A{aid}.json`, and adds a markdown analysis comparing at least 2 KCs against their corresponding AST signatures to verify interpretability.

3. **Embed KC table content in notebook output:** The `display(Markdown(...))` call for A439 KCs produces an `<IPython.core.display.Markdown object>` output which is not human-readable in static notebook export. Consider adding `print()` of the KC names as a fallback, or use `display` with an `output_type: display_data` cell that stores the rendered HTML.

4. **Document linkage method in clustering markdown:** The use of `method="average"` (UPGMA) vs. other linkage criteria (Ward, complete) is a methodological choice worth one sentence in the Etapa 3 markdown, since it affects cluster compactness.

---

## Verdict

STATUS: CRITICAL_ISSUES
