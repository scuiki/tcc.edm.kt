# Testing Patterns

**Analysis Date:** 2026-05-27

## Test Framework

**Runner:** none. This is a research project: there is **no `pytest`, `unittest`, `nose`, or `hypothesis` framework installed or in use**.

**Config:** none. No `pyproject.toml`, `pytest.ini`, `setup.cfg`, `tox.ini`, `conftest.py`, or `.pre-commit-config.yaml` exists at the repo root or anywhere under `src/` or `notebooks/`.

**Test files:** none. No file matching `test_*.py`, `*_test.py`, or any `tests/` directory exists in the repository.

**Verification commands (no formal test target):**
```bash
# Environment smoke test (from README.md)
python3 -c "import torch, pyBKT, sklearn; print('OK')"
srcml --version

# Replay a notebook end-to-end as a de-facto regression test
jupyter nbconvert --to notebook --execute notebooks/04_bkt.ipynb \
    --output notebooks/04_bkt_executed.ipynb

# Run a verification utility script (post-execution KC inspection)
python3 scripts/inspect_coverage.py
python3 scripts/inspect_kcs.py
```

## De-facto Validation Strategy

The project replaces unit tests with **four overlapping layers of inline validation** embedded directly in the production code and notebooks:

1. **Inline `assert` invariants** in `src/` and in notebook cells (preconditions, postconditions, schema checks).
2. **Benchmark against published paper AUCs** (Shi et al., 2022; Pankiewicz et al., 2025) as the primary correctness signal.
3. **Reproducibility checks** that re-run with the same seed and compare to a pickled reference, plus multi-seed regeneration as a sensitivity test.
4. **Statistical comparison** (Wilcoxon signed-rank with Holm-Bonferroni correction) on the multi-run AUC distributions to validate that observed model differences are not noise.

Each notebook ends with a `## Sanity checks` or `## Sumário` section that re-loads the just-pickled artifact and re-validates its schema.

## Test File Organization

**Location:** validation is **co-located inside the production module or notebook** that generates the artifact being checked. There is no separate test tree.

**Naming:**
- Notebook section headers: `## N — Sanity checks` (e.g. `notebooks/08_multirun_regeneration.ipynb` section 8 cell 19, `notebooks/09_srcml_dkt.ipynb` section 10 cell 23)
- Smoke-test sections in modeling notebooks: `## 4 — Smoke test` / `## 7 — Smoke test de treino (5 épocas, A439, seed=42)` (`notebooks/05_dkt.ipynb`, `notebooks/06_code_dkt.ipynb` cell 19)
- Helpers inside notebooks named with `cmp_` prefix for pairwise checks (`cmp_pair`, `notebooks/08_multirun_regeneration.ipynb` cell 21)

**Structure:**
```
notebooks/<NN>_<model>.ipynb
├── ## 1 — Setup                         # SEED, imports, paths
├── ## 2..N-2 — pipeline sections        # build, train, evaluate
├── ## N-1 — Serialização                # pickle.dump to results/
└── ## N — Sanity checks / Sumário       # re-load and validate
```

## Test Structure

**Inline assertion pattern** (used at the entry of every public function in `src/`):
```python
# src/data_loader.py:71-72
assert filtered["EventType"].nunique() == 1, "EventType inesperado passou pelo filtro BKT/DKT"
assert set(filtered["EventType"].unique()) == {"Run.Program"}, "Filtro BKT/DKT corrompido"
```

**Notebook split-shape validation:**
```python
# notebooks/04_bkt.ipynb cell 4
EVAL_AIDS = [aid for aid in ASSIGNMENT_IDS if len(seqs['test'].get(aid, [])) > 0]
assert set(EVAL_AIDS) == {439, 487, 492, 494, 502}, \
    f"Esperado todos os 5 assignments com test set; got {set(EVAL_AIDS)}"
```

**Notebook parameter-range validation (BKT):**
```python
# notebooks/04_bkt.ipynb cell 12
for aid in ASSIGNMENT_IDS:
    p = all_params[aid].dropna()
    assert (p >= 0).all().all() and (p <= 1).all().all(), f'A{aid}: parâmetros fora de [0,1]'
    gs = p['P(G)'] + p['P(S)']
    assert (gs < 1).all(), f'A{aid}: P(G)+P(S) >= 1 para algum KC'
```

**Schema check on persisted multirun artifacts** (`notebooks/08_multirun_regeneration.ipynb` cell 20):
```python
for model_name, obj, expected_runs in [
    ("bkt", bkt_multirun, 1),
    ("dkt", dkt_multirun, 10),
    ("code_dkt", cdkt_multirun, 10),
]:
    for aid in ASSIGNMENT_IDS:
        runs = obj[aid]["runs"]
        assert len(runs) == expected_runs, f"{model_name} A{aid}: {len(runs)} runs (esperado {expected_runs})"
        seeds_found = sorted([r["seed"] for r in runs])
        expected_seeds = [SEED_DEFAULT] if expected_runs == 1 else list(SEEDS)
        assert seeds_found == expected_seeds, f"{model_name} A{aid}: seeds={seeds_found}"

print("Schema check: ✓ BKT(1 run) + DKT(10 runs) + Code-DKT(10 runs) × 5 assignments")
```

**srcML-DKT schema check** (`notebooks/09_srcml_dkt.ipynb` cell 24):
```python
REQUIRED_KEYS = {
    "all_auc_mean", "all_auc_std", "first_auc_mean", "first_auc_std",
    "runs", "n_train_events", "n_test_events", "config",
    "vocab", "problem_to_idx", "model_state_dict_seed42",
}
errors = []
for aid in ASSIGNMENT_IDS:
    assert aid in r, f"A{aid} ausente no pickle"
    missing = REQUIRED_KEYS - set(r[aid].keys())
    if missing:
        errors.append(f"A{aid}: chaves ausentes {missing}")
    n_runs = len(r[aid]["runs"])
    if n_runs != 10:
        errors.append(f"A{aid}: esperado 10 runs, got {n_runs}")
```

**Patterns:**
- Setup pattern: `## 1 — Setup` cell defines `SEED = 42`, calls `set_global_seed(SEED)`, loads pickles from `RESULTS_ROOT`. Used identically in notebooks 04 to 09.
- Teardown pattern: every modeling notebook ends with a serialization cell + a sanity-check cell that re-opens the pickle.
- Assertion pattern: `assert <invariant>, f"<contexto identificável>"` with f-strings that name the assignment (`A{aid}`) and the broken value. Never a bare `assert` with no message.

## Benchmark Validation Against Published Paper

This is **the primary correctness signal** for the project. AUCs computed by our code must fall within the standard deviation reported by Shi et al. (2022) Table 1 and Table 2 — that is the TCC 1 acceptance criterion #1 from `CLAUDE.md`.

**Hard-coded paper references** appear in notebooks as constants near the evaluation cells:

**DKT vs paper** (`notebooks/05_dkt.ipynb` cell 22):
```python
PAPER_DKT = {
    439: {'all_auc': 71.24, 'first_auc': 72.26, 'all_std': 2.54, 'first_std': 3.69},
    487: {'all_auc': 73.09, 'first_auc': None},
    492: {'all_auc': 76.84, 'first_auc': None},
    494: {'all_auc': 69.16, 'first_auc': None},
    502: {'all_auc': 75.14, 'first_auc': None},
}
```
Followed by a `rows_vs_paper` table that prints `diff_all = our['all_auc'] * 100 - paper['all_auc']` and `diff_first = ... - paper['first_auc']` for visual inspection (cells 23-24).

**BKT vs paper** (`notebooks/04_bkt.ipynb` cell 20):
```python
PAPER_ALL   = {439: 63.78}   # Shi et al. Table 2, A1
PAPER_FIRST = {439: 50.22}   # idem
```
Plus an inline `print` reference under each AUC compute cell: `print(f'Referência Shi et al. (2022) Table 2 — A439: 63.78% (±4.68%)')` (`notebooks/04_bkt.ipynb` cell 16).

**Tolerance policy:**
- `CLAUDE.md` criterion 1: first-attempt AUC for Code-DKT on A439 within **±3%** of paper's ~74%.
- `notebooks/05_dkt.ipynb` cell 25 documents the rationale: paper reports σ = 2.54% for A439 all-auc over 10 runs, so individual-run divergences up to ~5pp are explainable.
- No automated assertion enforces the tolerance — the deviation is printed as a `Δ pp` column and interpreted in the following `**Achado:**` markdown cell.

**Result so far (per `project_codedkt_results.md` and `project_multirun_results.md`):** A439 first-attempt AUC = 72.55% (within ±3% of paper); multi-run regeneration confirmed the protocol replication.

## Reproducibility Checks

**Seed regime:**
- `SEED = 42` is mandated by `CLAUDE.md` and enforced by `set_global_seed()` in every modeling notebook.
- Multi-run notebook `08_multirun_regeneration.ipynb` uses `SEEDS = list(range(42, 52))` (10 runs) to estimate `mean ± std` per assignment, aligning with Shi et al. (2022) protocol.
- BKT remains at 1 run because pyBKT is effectively deterministic given a seed.

**Reproducibility assertion: single-run vs multirun seed=42 must agree** (`notebooks/08_multirun_regeneration.ipynb` cell 21):
```python
TOL = 0.03  # 3pp de tolerância (CUDA não-determinismo em LSTM)

def cmp_pair(name, single, multi, aid):
    single_first = single[aid]["first_auc"]
    multi_seed42 = next(r["first_auc"] for r in multi[aid]["runs"] if r["seed"] == 42)
    diff = abs(single_first - multi_seed42) if single_first is not None else float("nan")
    ok = "✓" if (single_first is None or diff <= TOL) else "⚠"
    sf = f"{single_first:.4f}" if single_first is not None else "N/A"
    print(f"  {ok} {name} A{aid}: single={sf} vs multirun_seed42={multi_seed42:.4f} (Δ={diff:.4f})")
    return single_first is None or diff <= TOL
```
Documented tolerance is **3pp** (`TOL = 0.03`) due to known CUDA non-determinism in LSTM (cuDNN). For BKT (pure CPU) the tolerance is effectively zero — `BKT` runs are expected to be bit-identical.

**Reproducibility assertion: srcML-DKT seed=42 matches between section 7 and persisted pickle** (`notebooks/09_srcml_dkt.ipynb` cell 25):
```python
for aid in ASSIGNMENT_IDS:
    run_42_from_multirun = next(run for run in r[aid]["runs"] if run["seed"] == 42)
    run_42_from_s9 = next(run for run in results_all[aid] if run["seed"] == 42)
    diff = abs(run_42_from_multirun["first_auc"] - run_42_from_s9["first_auc"])
    if diff > 1e-6:
        print(f"A{aid}: DIVERGÊNCIA seed=42 first_auc diff={diff:.6f}")
    else:
        print(f"A{aid}: seed=42 reprodutível (diff={diff:.2e})")
```
Tolerance here is `1e-6` because the same Python process re-runs the same code path — any drift indicates a bug in serialization.

**Reproducible AST extraction:**
- `extract_paths_javalang` and `extract_paths_srcml` accept `seed: int = 42` and use **a private `random.Random(seed)` instance** rather than the global RNG so per-call sampling stays deterministic without disturbing the surrounding training-loop seed (`src/code_features.py:174-176`, `src/srcml_features.py:191-194`):
  ```python
  if len(paths) > R:
      rng = random.Random(seed)
      paths = rng.sample(paths, R)
  ```
- AST caches are persisted to `results/code_features_cache.pkl` and `results/srcml_features_cache.pkl` (gitignored). Re-extraction is the recovery path if the cache is missing — there is no diff-check between cached and fresh extractions.

## Statistical Validation (Wilcoxon)

**Significance test built into `notebooks/07_comparison.ipynb`** (criterion 3 of `CLAUDE.md`).

Helper (cell 13):
```python
def holm_bonferroni(p_values):
    n = len(p_values)
    order = np.argsort(p_values)
    p_sorted = np.array(p_values)[order]
    p_adj_sorted = np.minimum(p_sorted * np.arange(n, 0, -1), 1.0)
    for i in range(1, n):
        p_adj_sorted[i] = max(p_adj_sorted[i], p_adj_sorted[i-1])
    p_adj = np.empty(n)
    p_adj[order] = p_adj_sorted
    return p_adj

def bootstrap_ci(diffs, n_boot=1000, rng=None):
    if rng is None:
        rng = np.random.RandomState(SEED)
    boot_means = np.array([
        np.mean(rng.choice(diffs, size=len(diffs))) for _ in range(n_boot)
    ])
    return float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))
```

Three planned comparisons with directional alternatives:
```python
comparisons = [
    ("Code-DKT",  "DKT",       "greater",   "Code-DKT > DKT"),
    ("srcML-DKT", "Code-DKT",  "less",      "srcML-DKT < Code-DKT"),
    ("srcML-DKT", "DKT",       "two-sided", "srcML-DKT vs DKT"),
]
```

Pairing is **per-seed per-assignment** (N = 5 assignments × 10 seeds = 50 paired observations) to maximise statistical power.

**Limitation noted in narrative** (`notebooks/06_code_dkt.ipynb` cell 29): when pairing only over the 5 assignments (N=5), the minimum possible p-value is `2^-5 = 0.0312`, so a single-seed run cannot achieve significance below this floor. The multi-run protocol in notebook 08 was introduced specifically to escape that ceiling.

**Established result from `project_comparison_results.md`:** Wilcoxon Code-DKT > DKT yields p = 0.002 (significant); srcML-DKT < Code-DKT also significant.

## Smoke Tests

Each modeling notebook has a "smoke test" section that runs the full pipeline at reduced cost before committing to the full grid/multirun.

**Pattern** (`notebooks/06_code_dkt.ipynb` cell 20):
```python
smoke_config = {**DEFAULT_CONFIG, "epochs": 5}
print("Smoke test config:", smoke_config)

if device.type == "cuda":
    torch.cuda.reset_peak_memory_stats()

set_global_seed(SEED)
t0 = time.time()
smoke_result = train_and_evaluate(
    seqs["train"][439], seqs["test"][439],
    problem_to_idx_a439, ...
)
```

**Configuration:** `epochs = 5` (vs `epochs = 40` for production), single assignment (A439), `seed = 42`. Output is inspected by hand — no assertion on the smoke AUC value, but the call must complete and produce all canonical dict keys.

**Forward-pass-only smoke test** (`notebooks/06_code_dkt.ipynb` cell 18) is even cheaper: instantiates the model and runs `model(X)` on a small batch to confirm tensor shapes match the architecture spec, without any training.

## Mocking

**Framework:** none. **No mocking is used anywhere** in this codebase.

**What to Mock:**
- Nothing. The CSEDM dataset is the unit of truth and is always loaded from disk.
- Even SDK-style external calls (Anthropic API for KC generation in `notebooks/03b_kc_generation.ipynb`) are cached to disk as JSON after the first call; re-runs replay the cache rather than mocking the API.

**What NOT to Mock:**
- Model training. Always train on real data with a fixed seed.
- AST extraction. Always run real `srcml` / `javalang` on real CodeStates.
- pyBKT, PyTorch, scipy.stats — never wrap.

The fixed `SEED = 42` provides the determinism that mocking would otherwise provide.

## Fixtures and Factories

**Test Data:** there are no test fixtures. The pipeline operates on artifacts written by upstream notebooks and stored under `results/`:

- `results/sequences_bkt_dkt.pkl` — output of `notebooks/02_preprocessing.ipynb`, consumed by 04, 05, 06, 07, 08, 09.
- `results/sequences_code_dkt.pkl` — same source, used when `Compile.Error` events must be included in the training sequence (Code-DKT, srcML-DKT).
- `results/code_features_cache.pkl` — output of the AST extraction cell in `notebooks/06_code_dkt.ipynb` (gitignored, regenerable from CSEDM CodeStates).
- `results/srcml_features_cache.pkl` — same, for srcML extractor (gitignored).
- `results/{bkt,dkt,code_dkt,srcml_dkt}_results.pkl` — single-seed model artifacts (cell at end of notebook 04, 05, 06, 09).
- `results/{bkt,dkt,code_dkt,srcml_dkt}_results_multirun.pkl` — 10-run aggregates (notebook 08 for DKT/Code-DKT; notebook 09 for srcML-DKT; BKT pickled as 1 run).

Notebooks declare their dependency on these files in the first code cell after the setup, via `pickle.load(open(RESULTS_ROOT / "sequences_bkt_dkt.pkl", "rb"))` — there is no factory function that synthesizes a smaller test fixture.

**Location:** all in `results/` at the repo root.

## Coverage

**Requirements:** none enforced. No coverage tool (`coverage.py`, `pytest-cov`) is installed.

**View Coverage:** not applicable.

**De-facto "coverage" check:** the four canonical models (BKT, DKT, Code-DKT, srcML-DKT) × 5 assignments (A439, A487, A492, A494, A502) = 20 model artifacts. The comparison notebook `07_comparison.ipynb` asserts all 4 model pickles exist and have entries for all 5 assignments. Any gap is a failure visible at load time.

## Test Types

**Unit Tests:** none.

**Integration Tests:** the notebook re-execution (`jupyter nbconvert --execute`) is the de-facto integration test — it runs the whole pipeline from `sequences_bkt_dkt.pkl` to a final AUC table and a persisted pickle.

**Regression Tests:**
- Re-running a modeling notebook with `seed=42` and comparing the new AUC against the existing pickled run via the `cmp_pair` helper (`notebooks/08_multirun_regeneration.ipynb` cell 21) is the closest thing to a regression test.
- Tolerance: `TOL = 0.03` (3pp) for LSTM-based models; effectively bit-identical for BKT.

**E2E Tests:** running the full notebook chain `02 → 04/05/06/09 → 08 → 07` is the end-to-end pipeline. Expected runtime ~1-2 hours on GPU for the multi-run regeneration.

**Statistical Tests:** Wilcoxon signed-rank (per Section above) tests model ranking, not code correctness. The two roles overlap in this codebase: if a code change degraded a model, the Wilcoxon would expose it because the new pickle would fail the directional alternative `Code-DKT > DKT`.

## Verification Utility Scripts

Under `scripts/` (run by hand from repo root; each does `ROOT = Path(__file__).resolve().parents[1]`):

| Script | Purpose | Output |
|---|---|---|
| `scripts/inspect_coverage.py` | For each assignment, list which problems require each KC, sorted by frequency | stdout table per assignment |
| `scripts/inspect_kcs.py` | For each assignment, list KCs required by each problem | stdout table per assignment |
| `scripts/viz_qmatrix_single.py` | Render Q-matrix heatmap for one assignment | PNG under `results/` |
| `scripts/viz_qmatrix_all.py` | Render Q-matrix heatmaps for all 5 assignments | PNGs under `results/` |
| `scripts/analyze_kc_difficulty_codedkt.py` | Re-train Code-DKT, measure learning curve per KC, aggregate by Martins (2024) sub-difficulties | `results/codedkt_kc_difficulty.json` + 3 PNGs |
| `scripts/analyze_kc_attention_codedkt.py` | Analyse Code-DKT attention weights per KC | stdout + figures |
| `scripts/build_methodology_figures.py` | Render methodology diagrams for the TCC text | PNGs under `results/` |

These are not tests in the formal sense but they double as **smoke checks**: a script that fails (missing pickle, schema mismatch, NaN AUC) signals an upstream bug.

## Common Patterns

**Async Testing:** N/A — no async code.

**Error Testing:**
- Defensive parsing in AST extractors returns `[]` on `Exception` (`src/code_features.py:112-115`, `src/srcml_features.py:118-134`). The downstream cache builder accepts empty lists without error, so failed parses become first-class observable data (`cache[csid] = []`). No test asserts what fraction of cache entries is empty, but `notebooks/06_code_dkt.ipynb` section 3 prints a "métricas de transparência" table showing parse success rate vs the paper's reported coverage.

**Negative-case validation:** the only explicit negative test is the `EventType` filter assertion in `src/data_loader.py:71-72` — if a row with a forbidden `EventType` survives the filter, the assertion fires immediately rather than poisoning the trained model.

**Determinism testing:**
- The `cmp_pair` helper in `notebooks/08_multirun_regeneration.ipynb` cell 21 with `TOL = 0.03` for GPU LSTM models.
- The exact-match check in `notebooks/09_srcml_dkt.ipynb` cell 25 with `diff > 1e-6` threshold for same-process re-runs.

**Pickle round-trip:** the closing "Sumário" / "Sanity checks" cells in every modeling notebook re-open the pickle they just wrote and verify required keys exist, run counts match, and seeds equal the expected `[42]` or `list(range(42, 52))`.

---

*Testing analysis: 2026-05-27*
