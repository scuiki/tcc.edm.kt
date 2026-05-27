# Coding Conventions

**Analysis Date:** 2026-05-27

## Naming Patterns

**Files:**
- Python modules: `snake_case.py` — `data_loader.py`, `code_features.py`, `srcml_features.py`, `evaluation.py`
- Model modules in `src/models/`: lowercase model name — `bkt.py`, `dkt.py`, `code_dkt.py`
- Notebooks: zero-padded numeric prefix + snake_case descriptor — `01_eda.ipynb`, `04_bkt.ipynb`, `08_multirun_regeneration.ipynb`. Variant suffix uses letter, e.g. `03b_kc_generation.ipynb`, `03c_eda_kc_crossover.ipynb`
- Result artifacts: `<model>_results.pkl`, `<model>_results_multirun.pkl`, `sequences_<model>.pkl`, `<features>_cache.pkl` — all under `results/`
- Utility scripts: verb-prefix snake_case — `inspect_coverage.py`, `viz_qmatrix_all.py`, `analyze_kc_difficulty_codedkt.py`, `build_methodology_figures.py`

**Functions:**
- `snake_case` (always English identifier) — `load_main_table`, `build_sequences`, `truncate_sequences`, `compute_auc`, `train_bkt`, `train_dkt`, `predict_dkt`, `train_and_evaluate`, `build_input_tensor`, `build_code_input_tensor`, `extract_paths_javalang`, `extract_paths_srcml`, `build_vocab`, `build_cache`
- Private helpers: leading underscore — `_get_token`, `_get_children`, `_build_tree`, `_parse_java`, `_worker_extract`, `_strip_ns`, `_srcml_token`, `_srcml_build_tree` (`src/code_features.py:46-85`, `src/srcml_features.py:53-82`)
- Pipeline entry point per model module: `train_and_evaluate(train_sequences, test_sequences, ..., seed=42) -> dict` (`src/models/bkt.py:95`, `src/models/dkt.py:327`, `src/models/code_dkt.py:307`)
- Notebook helpers always defined inline at top of cell, often as nested closures (e.g. `set_global_seed`, `build_vocab_for_assignment`, `cmp_pair`, `fmt_pct`, `holm_bonferroni`, `bootstrap_ci`)

**Variables:**
- Local variables: `snake_case` (English)
- Constants in notebooks: `UPPER_SNAKE_CASE` — `SEED`, `SEEDS`, `SEED_DEFAULT`, `ROOT`, `DATA_ROOT`, `RESULTS_ROOT`, `RESULTS_DIR`, `ASSIGNMENT_IDS`, `EVAL_AIDS`, `AIDS`, `MODEL_ORDER`, `COLORS`, `DPI`, `TOL`, `DEFAULT_CONFIG`, `GRID`, `PARAM_MAP`, `PAPER_DKT`, `PAPER_ALL`, `PAPER_FIRST`, `CACHE_PATH`, `OUTPUT_PATH`, `SMOKE_TEST`, `MIN_N`, `MAX_OPP`
- Single-letter math symbols allowed in tight numeric loops where the math literature uses them: `M` (problem count per assignment), `N` (sequence count), `L` (sequence length), `R` (paths per step), `B` (batch), `t`, `t_rel`, `i`, `j` — see `src/models/dkt.py:101-135`
- DataFrame columns from CSEDM kept exactly as upstream: `SubjectID`, `AssignmentID`, `ProblemID`, `ServerTimestamp`, `EventType`, `Score`, `CodeStateID`, `Label`. Derived columns are `snake_case`: `correct`, `is_first_attempt`, `correct_predictions`, `user_id`, `skill_name`
- Tensor names follow the model paper: `X`, `Y_next`, `mask`, `y_pred`, `y_true`, `h`, `next_q`, `pred_for_next`

**Types:**
- No `class` types for data — dicts are the standard transport. Sequences are `list[dict]` with fixed keys: `subject_id`, `assignment_id`, `events` (`src/data_loader.py:108-165`)
- Model classes use `PascalCase` — `DKTModel`, `CodeDKTModel`. Suffix `Model` mandatory for `nn.Module` subclasses
- Type hints required on every public function signature in `src/`, including return types. Use PEP 604 unions (`Path | str`) and PEP 585 generics (`list[dict]`, `dict[int, int]`, `dict[str, list]`) — no `typing.List`/`typing.Dict`. See `src/data_loader.py:16`, `src/models/code_dkt.py:42-54`
- `from __future__ import annotations` at top of `src/code_features.py:14` and `src/srcml_features.py:20` for forward references
- `Optional[T]` from `typing` is used when a parameter defaults to `None` (`src/code_features.py:199`)

## Code Style

**Formatting:**
- No formatter config present (`pyproject.toml`, `setup.cfg`, `.pre-commit-config.yaml` all absent). Style is hand-maintained.
- 4-space indentation, no tabs
- Line length wraps around 88-100 characters (visual, not enforced); long arg lists split one-per-line and aligned (`src/models/dkt.py:42-48`, `src/models/code_dkt.py:42-54`)
- Trailing commas in multi-line literal lists and function signatures (`src/models/dkt.py:316-322`)
- Double quotes for strings in the deep-learning modules (`src/models/code_dkt.py`, `src/srcml_features.py`); single quotes in older modules (`src/models/bkt.py`, `src/data_loader.py`). Both styles coexist; do not retro-fit.
- Inline mathematical comments often use Unicode (`α`, `δ`, `ℝ`, `→`) and box-drawing rules `── ───` to delimit notebook cell sections (`notebooks/06_code_dkt.ipynb` cells 3-4, 23). Avoid em-dashes in prose per repo memory `feedback_no_em_dashes.md` (prefer comma, colon, parentheses).

**Linting:**
- No linter configured. No `ruff`, `flake8`, `pylint`, `mypy`, `black`, or `pre-commit` files present.
- Pattern of self-validation through `assert` statements at key pipeline points instead of external lint (see Testing patterns).

## Import Organization

**Order:**
1. Standard library — `from __future__ import annotations`, then plain imports (`import os`, `import sys`, `import pickle`, `import random`, `import time`, `import warnings`, `from pathlib import Path`, `from typing import Optional`)
2. Third-party scientific stack — `import numpy as np`, `import pandas as pd`, `import torch`, `import torch.nn as nn`, `import torch.nn.functional as F`, `from torch import Tensor`, then sklearn/scipy/seaborn/matplotlib
3. Project-internal imports from `src.` — placed last (`from src.evaluation import compute_auc`, `from src.code_features import build_code_input_tensor`, `from src.models.dkt import dkt_loss`)

**Standard aliases (use these exact names):**
- `import numpy as np`
- `import pandas as pd`
- `import torch.nn as nn`
- `import torch.nn.functional as F`
- `import matplotlib.pyplot as plt`
- `import matplotlib.ticker as mticker`
- `import matplotlib.patches as mpatches`
- `import seaborn as sns`
- `import xml.etree.ElementTree as ET` (`src/srcml_features.py:25`)
- `import multiprocessing as mp` (`src/code_features.py:16`)

**Path Aliases:**
- No tooling alias (no `setup.py`, no editable install). Notebooks bootstrap the project root via:
  ```python
  ROOT = Path(".").resolve().parent  # or Path('..').resolve()
  if str(ROOT) not in sys.path:
      sys.path.insert(0, str(ROOT))
  ```
  (`notebooks/06_code_dkt.ipynb` cell 2, `notebooks/08_multirun_regeneration.ipynb` cell 2, `notebooks/09_srcml_dkt.ipynb` cell 2). Scripts in `scripts/` use `ROOT = Path(__file__).resolve().parents[1]` (`scripts/analyze_kc_difficulty_codedkt.py:34`, `scripts/inspect_coverage.py:5`).
- After bootstrap, imports use the absolute `src.` prefix: `from src.models.code_dkt import CodeDKTModel, train_code_dkt`.

## Error Handling

**Patterns:**
- Defensive parsing returns empty list on failure rather than raising — used for AST extraction where failures must not abort the whole cache build (`src/code_features.py:112-115`, `src/srcml_features.py:118-134`):
  ```python
  try:
      parsed = _parse_java(code)
  except Exception:
      return []
  ```
- Invariants are encoded as `assert` with explanatory message (`src/data_loader.py:71-72`, `src/models/dkt.py:227` style). Example:
  ```python
  assert filtered["EventType"].nunique() == 1, "EventType inesperado passou pelo filtro BKT/DKT"
  ```
- Validation errors from public API raise `ValueError` with f-string repr of the bad value (`src/data_loader.py:35`):
  ```python
  raise ValueError(f"split deve ser um de {list(_SPLITS)}; recebido: {split!r}")
  ```
- Missing files raise `FileNotFoundError` with full path (`src/data_loader.py:238`)
- Numeric edge cases return `np.nan` rather than raising (`src/evaluation.py:58-60`):
  ```python
  if len(df) == 0 or df["correct"].nunique() < 2:
      return np.nan
  ```
- Notebook cells often `warnings.filterwarnings("ignore")` once at setup (`notebooks/07_comparison.ipynb` cell 2)

## Logging

**Framework:** plain `print()` only. No `logging`, no `loguru`.

**Patterns:**
- Training progress logged per epoch with fixed-width `f"  Época {epoch:2d}/{epochs} — loss: {avg_loss:.4f}"` (`src/models/dkt.py:261`, `src/models/code_dkt.py:235`). Note: this is one of the few places em-dashes appear in code — they came from the original Code-DKT reference and remain in training loops only.
- Notebook sanity checks emit checkmarks/warnings with Unicode glyphs in strings: `"✓"`, `"⚠"` (`notebooks/08_multirun_regeneration.ipynb` cell 21)
- Tables built by hand using f-string padding rather than `tabulate` (`notebooks/05_dkt.ipynb` cell 2):
  ```python
  header = f"{'Assignment':>12} | {'n_train_seqs':>13} | {'n_test_seqs':>11}"
  print(header)
  print('-' * len(header))
  ```
- `print(...)` with `flush=True` inside long training cells so Jupyter shows progress in real time (`notebooks/08_multirun_regeneration.ipynb` cell 11)
- DataFrames shown via `display(df)` in notebooks (cells importing nothing — `display` is Jupyter built-in) or `print(df.to_string(index=False))` when alignment matters

## Comments

**When to Comment:**
- Module docstring on every `.py` in `src/` and `scripts/` — first line is a one-sentence summary in Portuguese, optionally followed by a longer block with paper citation and pipeline context (`src/data_loader.py:1-8`, `src/models/code_dkt.py:1-13`, `src/srcml_features.py:1-18`)
- Inline comments that cite the source paper and section/figure for any non-obvious algorithmic step. Example pattern (`src/models/dkt.py:69, 84, 110, 122, 162-163`):
  ```python
  # Piech et al. (2015), Section 3: dropout aplicado em h_t antes da projeção
  # Shi et al. (2022): últimas max_len tentativas quando L > max_len
  # c2vRNNModel.py linha 14: +2 reserva slots para PAD (0) e UNK
  ```
- Reference-implementation cross-refs use the file:line format `c2vRNNModel.py linhas 39-42` (`src/models/code_dkt.py:105-106`) so a reader can open the reference repo at `/home/leokuntz/Documents/repositories/experiments/Code-DKT/src/`
- Tensor shape annotations as inline trailing comments `# (B, L, R, 100)` (`src/models/code_dkt.py:114-139`)
- Section dividers in long modules use a row of dashes:
  ```python
  # ---------------------------------------------------------------------------
  # Vocabulário
  # ---------------------------------------------------------------------------
  ```
  (`src/code_features.py:223-225`, `src/srcml_features.py:39-41`)

**Docstrings:**
- Two coexisting styles, **per-file consistent**:
  - **NumPyDoc** in `src/data_loader.py` (Parameters / Returns / Notes sections with dashes)
  - **Google-style** in `src/evaluation.py`, `src/models/bkt.py`, `src/models/dkt.py`, `src/models/code_dkt.py`, `src/code_features.py`, `src/srcml_features.py` (Args: / Returns: with colons)
- New modules: follow Google-style (it is the majority).
- Docstrings are in Portuguese. Class docstrings explain the architecture and cite the paper section implemented (`src/models/dkt.py:22-28`, `src/models/code_dkt.py:30-40`).
- Equations in docstrings written in plain text with the paper reference (`src/models/dkt.py:25-28`):
  ```
  h_t = LSTM(x_t, h_{t-1})
  y_t = sigmoid(W_hy * dropout(h_t))
  ```

## Function Design

**Size:** training/prediction functions run 50-120 lines; AST extraction up to 90 lines. Anything larger is decomposed into private helpers (`_build_tree`, `_get_children`, `_worker_extract`).

**Parameters:**
- Hyperparameters bundled in a `config: dict` with documented required keys, never as positional args (`src/models/dkt.py:182-191`, `src/models/code_dkt.py:160`). Defaults pulled with `config.get("lr", 0.0005)` so the dict can be partial.
- `seed: int = 42` is the standard last parameter on every training entry point (`src/models/bkt.py:39`, `src/models/dkt.py:184`, `src/models/code_dkt.py:152`)
- `data_root: Path | str` accepted as either string or Path, then coerced via `Path(data_root)` in the first line (`src/data_loader.py:33`)

**Return Values:**
- `train_and_evaluate` always returns a `dict` with the same canonical keys across models: `model`, `config`/`params`, `all_auc`, `first_auc`, `n_train_events`/`n_train`, `n_test_events`/`n_test`. Code-DKT also returns `pred_df` so downstream notebooks can pickle the predictions (`src/models/code_dkt.py:346-354`). The dict shape is the de-facto interface used by `notebooks/07_comparison.ipynb`.
- `predict_*` functions return a `pd.DataFrame` with the exact columns: `user_id`, `skill_name`, `correct`, `is_first_attempt`, `correct_predictions`. This schema is shared across `predict_bkt`, `predict_dkt`, `predict_code_dkt` so `compute_auc(pred_df, first_attempt_only=...)` works uniformly (`src/evaluation.py:38`).
- Empty-input safe: `predict_*` returns an empty DataFrame with the right columns when given `[]` (`src/models/dkt.py:289-293`, `src/models/code_dkt.py:267-271`)

## Module Design

**Exports:**
- `src/models/__init__.py` is empty. No re-exports — callers always import from the leaf module: `from src.models.bkt import train_and_evaluate as train_bkt_pipeline` is the typical pattern in notebooks.
- No `__all__` declarations.

**Barrel Files:** none.

## Notebook Conventions

**Header cell:** every notebook begins with a `# NN — Title` markdown cell that states:
1. The pipeline step and method name
2. The reference paper citation (Corbett & Anderson 1995, Piech et al. 2015, Shi et al. 2022, Pankiewicz et al. 2025)
3. A bulleted pipeline outline of the sections in this notebook
4. A "Critérios" line linking back to `CLAUDE.md` when the notebook satisfies a TCC 1 acceptance criterion (`notebooks/07_comparison.ipynb` cell 0)

**Section structure:** numbered sections via markdown headers `## N — Section name`. Subsections use `### N.M — Subsection`. EDA notebook uses three levels (`### 1.1.1`).

**Cell-pair pattern (Setup → Find → Verify):**
1. `## 1 — Setup` markdown
2. Imports + `SEED = 42` + path bootstrap + `set_global_seed(SEED)` (one code cell)
3. `## 2 — <next step>` markdown
4. Code cell that produces a result
5. **Markdown cell starting with `**Achado:**`** that interprets the result in 1-3 paragraphs and may include a follow-up `**Implicação para modelagem:**` paragraph (`notebooks/04_bkt.ipynb` cells 5, 8, 13, 17, 24, 27, 30)

**Closing section:** every modeling notebook ends with a serialization cell that pickles results to `results/<model>_results.pkl` followed by a "Sumário" or "Sanity checks" section that re-loads the pickle and verifies schema (`notebooks/04_bkt.ipynb` cells 32-34, `notebooks/09_srcml_dkt.ipynb` cells 24-26).

**Reproducibility cell (must appear before any stochastic operation):**
```python
SEED = 42

def set_global_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_global_seed(SEED)
```
Mandatory in every notebook that trains models (`notebooks/06_code_dkt.ipynb` cell 3, `notebooks/09_srcml_dkt.ipynb` cell 2). For multi-run notebooks, additionally:
```python
SEEDS = list(range(42, 52))   # 42..51 — 10 runs
SEED_DEFAULT = 42
```
(`notebooks/08_multirun_regeneration.ipynb` cell 2). The 42-51 range is the canonical 10-run sweep — do not change it.

**Setup constants block (after imports):**
```python
ROOT = Path(".").resolve().parent          # notebooks/ -> repo root
DATA_ROOT    = ROOT / "data" / "CSEDM"
RESULTS_ROOT = ROOT / "results"            # also seen as RESULTS_DIR
sys.path.insert(0, str(ROOT))
ASSIGNMENT_IDS = [439, 487, 492, 494, 502]  # or loaded from the pkl
```

**Plot defaults:**
```python
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 150,
})
```
(`notebooks/07_comparison.ipynb` cell 2). Use the `COLORS` dict for model identity across plots:
```python
COLORS = {
    "BKT":       "#4292c6",
    "DKT":       "#f16913",
    "Code-DKT":  "#41ab5d",
    "srcML-DKT": "#d7191c",
}
```

## Language Choices (Portuguese vs English)

This is a Brazilian undergraduate thesis. The convention is:

- **Code identifiers (functions, variables, classes, file names):** English. No Portuguese identifier in any `src/` or `scripts/` file.
- **Docstrings and inline code comments:** Portuguese.
- **Notebook markdown cells (titles, narrative, "Achado", "Hipótese", "Implicação"):** Portuguese.
- **Notebook `print()` user-facing strings:** Portuguese (e.g. `print(f"  Época {epoch:2d}/{epochs} — loss: {avg_loss:.4f}")`, `notebooks/04_bkt.ipynb` headers like `"Assignment"`, `"n_test_students"`).
- **Assert error messages, ValueError messages:** Portuguese (`src/data_loader.py:35, 71`).
- **DataFrame column names:** keep CSEDM/upstream names as-is (`SubjectID`, `EventType`, etc.) — these are English by virtue of being from the dataset, not by choice. Derived columns added by our code are also English (`correct`, `is_first_attempt`, `correct_predictions`).

When in doubt: anything the Python interpreter parses is English; anything a human reads in prose is Portuguese.

**Em-dash prohibition (per `feedback_no_em_dashes.md`):** avoid `—` in prose (notebook markdown, docstrings, plan documents). Use comma, colon, or parentheses instead. Em-dashes that survive in source are heritage from the Code-DKT reference port (e.g. training loop print strings) and need not be retro-fitted.

## Commit Message Style

Recent commit log (`git log --oneline -30`) shows a consistent informal Portuguese convention:

**Format:** `<topic>: <description in lowercase Portuguese>`

The `<topic>` is one of:
- `<feature-area>` (no formal `feat:`/`fix:` conventional-commits prefixes) — `kc_generation task 3:`, `preprocessing task 4:`, `bkt task6:`, `bkt task6 fix:`
- `<model-or-notebook>:` — `dkt:`, `comparison:`, `apresentacao:`
- `<feature-area> fase <N>:` for staged work split across chat sessions — `code-dkt fase 1:`, `code-dkt fase 2:`, `srcml-dkt fase 1:`, `multirun fase 1:`
- `<feature-area> task <N>:` for harness-driven multi-step plans — `preprocessing task 5: serialização dos artefatos — verificação e marcação como completo`
- `chore:` is used (e.g. `chore: remover artefatos do Playwright MCP do versionamento`) but `feat:`/`fix:`/`docs:`/`refactor:` are NOT used
- Bare descriptive sentences also appear for small commits — `apresentação`, `KCs e EDA`, `comparativo técnico e diagramas`

**Body conventions:**
- Most commits are single-line. Multi-line bodies appear only for plan/decision commits.
- Subjects are lowercase except proper nouns and abbreviations (`BKT`, `DKT`, `Code-DKT`, `srcML-DKT`, `LLM`, `EDA`, `AC4`, `AC5`).
- Em-dash sometimes used in subjects from earlier history (`task 5 — fix AC4`) but newer commits prefer `:` separators (per `feedback_no_em_dashes.md`).
- File names cited with relative path: `notebooks/09_srcml_dkt.ipynb`, `docs/srcml_dkt_chat1_notes.md`, `src/srcml_features.py`.
- Verbs in infinitive Portuguese: `implementa`, `remover`, `adicionar`, or in past-perfect/result form: `concluído`, `executado end-to-end`, `marcação como completo`.

**Examples to mirror:**
```
dkt: implementa 05_dkt.ipynb, src/models/dkt.py e src/evaluation.py
srcml-dkt fase 1: src/srcml_features.py + .gitignore para cache
comparison: notebooks/07_comparison.ipynb completo e executado end-to-end
kc_generation task 5: Q-matrix — verificação e marcação como completo
chore: remover artefatos do Playwright MCP do versionamento
```

No `Co-Authored-By` trailers appear in history. No issue/PR cross-references (single-author project).

---

*Convention analysis: 2026-05-27*
