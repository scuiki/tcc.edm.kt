# Technology Stack

**Analysis Date:** 2026-05-27

## Languages

**Primary:**
- Python 3.12.3 (venv interpreter; project documented as requiring Python 3.10+) — all modelling and analysis code under `src/`, `scripts/`, and `notebooks/`
- Jupyter Notebook JSON (`.ipynb`) — pipeline orchestration in `notebooks/01_eda.ipynb` through `notebooks/09_srcml_dkt.ipynb`

**Secondary:**
- Java (data only, never executed) — student submissions stored as text in `data/CSEDM/CodeStates/CodeStates.csv`; parsed via `javalang` (Code-DKT) and `srcml` (srcML-DKT)
- HTML/CSS — TCC presentation in `apresentacao/index.html` and `apresentacao/assets/theme-unifacens.css`
- Markdown — project docs (`README.md`, `CLAUDE.md`, `PLAN_TCC1.md`, `PLAN_KC_GENERATION.md`) and per-notebook validation reports in `results/validation_reports/`

## Runtime

**Environment:**
- CPython 3.12.3 in a local virtual environment at `.venv/` (config: `.venv/pyvenv.cfg`)
- `include-system-site-packages = false` — fully isolated environment
- Created via `python3 -m venv .venv` (no `uv`, `poetry`, or `pdm` detected)

**Package Manager:**
- `pip` (lockfile: not present — no `requirements.txt`, `pyproject.toml`, `poetry.lock`, or `Pipfile`)
- Reproducibility relies on the `.venv/` directory itself plus the installation hints in `README.md` lines 47–53
- Effective dependency snapshot can be obtained with `.venv/bin/pip freeze`

**GPU / Accelerator:**
- CUDA stack installed (`nvidia-cublas==13.1.0.3`, `nvidia-cudnn-cu13==9.19.0.56`, `cuda-toolkit==13.0.2`, `nvidia-nccl-cu13==2.28.9`, `triton==3.6.0`)
- Runtime device selection pattern is `torch.device("cuda" if torch.cuda.is_available() else "cpu")` in `src/models/dkt.py`, `src/models/code_dkt.py`
- Falls back transparently to CPU if no GPU is present

## Frameworks

**Core:**
- `torch==2.11.0` — LSTM-based KT models (`src/models/dkt.py`, `src/models/code_dkt.py`)
- `pyBKT==1.4.1` — Bayesian Knowledge Tracing baseline (`src/models/bkt.py`)
- `scikit-learn==1.8.0` — `roc_auc_score`, `train_test_split`, `DecisionTreeClassifier`, `KMeans`, `PCA`, `StandardScaler`, `silhouette_score` (used in `src/evaluation.py` and across notebooks 03b, 04, 07)
- `pandas==3.0.2` — DataFrame manipulation throughout (`src/data_loader.py`, all notebooks)
- `numpy==2.4.4` — array math, sampling, masking
- `scipy==1.17.1` — `scipy.stats.wilcoxon`, `scipy.cluster.hierarchy.linkage`, `scipy.spatial.distance.pdist` (used in `notebooks/07_comparison.ipynb` for significance tests, `notebooks/03b_kc_generation.ipynb` for HAC clustering)

**LLM / Embeddings:**
- `anthropic==0.99.0` — Claude API client for KC generation (`notebooks/03b_kc_generation.ipynb`); model `claude-haiku-4-5-20251001`
- `sentence-transformers==5.4.1` — Sentence-BERT embeddings (`all-MiniLM-L6-v2`) for KC clustering in `notebooks/03b_kc_generation.ipynb`
- `transformers==5.8.0`, `tokenizers==0.22.2`, `huggingface_hub==1.13.0`, `safetensors==0.7.0` — pulled in transitively by `sentence-transformers`

**AST / Code Parsing:**
- `javalang==0.13.0` — Java AST parser used by `src/code_features.py` for the Code-DKT path extractor
- `srcml` 1.1.0 (system CLI at `/usr/bin/srcml`, with `libsrcml 1.1.0` and `srcql 1.0.0`) — invoked via `subprocess.run(["srcml", "--language=Java"], ...)` in `src/srcml_features.py` for the srcML-DKT extractor
- `anytree==2.13.0` — tree walking helpers (`Node`, `Walker`, `findall_by_attr`) used in both AST extractors

**Testing:**
- No automated test framework detected (no `pytest`, `unittest`, `tests/` directory)
- Validation is notebook-based; reports are written to `results/validation_reports/*.md`
- A handcrafted harness exists at `.harness/` (`HARNESS_PLAN.md`, `runner.py`, `validator.py`, `evaluator.py`, `progress.md`) — internal planning, not a test runner

**Build / Dev:**
- `jupyter` stack: `ipykernel==7.2.0`, `nbconvert==7.17.1`, `nbformat==5.10.4`, `nbclient==0.10.4`, `jupyter_client==8.8.0`, `jupyter_core==5.9.1`
- `IPython==9.13.0`, `ipython_pygments_lexers==1.1.1`
- `matplotlib==3.10.9`, `seaborn==0.13.2` — figures saved to `results/*.png`
- `pillow==12.2.0`, `contourpy==1.3.3`, `fonttools==4.62.1`, `kiwisolver==1.5.0` — matplotlib backend dependencies
- `tabulate==0.10.0` — Markdown tables for comparison reports (`results/comparison_table_*.md`)
- `tqdm==4.67.3` — progress bars

## Key Dependencies

**Critical (modelling pipeline):**
- `torch==2.11.0` — Code-DKT and DKT LSTM implementations; CUDA path embedded in venv via `nvidia-*` wheels
- `pyBKT==1.4.1` — BKT baseline; project notes (in memory) document three runtime patches applied inside `.venv/` for numpy 2.4 / sklearn 1.8 compatibility; EM step required a sequential fallback because parallel E-step only runs from `__main__`
- `scikit-learn==1.8.0` — every model reports AUC via `sklearn.metrics.roc_auc_score`; `train_test_split(random_state=1)` defines the 80/20 split that anchors the entire experiment
- `javalang==0.13.0` — required for Phase 1 Code-DKT (fails silently on `Compile.Error`, which motivated the srcML alternative)
- `srcml` (system CLI 1.1.0) — required for Phase 2 srcML-DKT; parses non-compilable Java

**Critical (LLM-based KC generation):**
- `anthropic==0.99.0` — `claude-haiku-4-5-20251001` for KC labelling in `notebooks/03b_kc_generation.ipynb`; uses ephemeral prompt caching to keep total cost near $39
- `sentence-transformers==5.4.1` (`all-MiniLM-L6-v2`) — embeds raw KC names before HAC clustering

**Infrastructure:**
- `numpy==2.4.4`, `pandas==3.0.2`, `scipy==1.17.1` — full numerical stack
- `pyzmq==27.1.0`, `tornado==6.5.5`, `nest-asyncio==1.6.0` — Jupyter messaging
- `pyyaml==6.0.3`, `jsonschema==4.26.0`, `attrs==26.1.0` — config/serialization
- `requests==2.33.1`, `httpx==0.28.1`, `httpcore==1.0.9`, `urllib3==2.6.3` — HTTP transport for `anthropic` and `huggingface_hub`

## Configuration

**Environment:**
- No `.env` file present at the repo root
- The Anthropic client reads `ANTHROPIC_API_KEY` from the process environment: `anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment` (`notebooks/03b_kc_generation.ipynb`)
- No `python-dotenv` or comparable loader installed; the key must be exported in the shell before launching Jupyter

**Build / Lint / Format:**
- No `pyproject.toml`, `setup.cfg`, `setup.py`, `ruff.toml`, `.flake8`, `mypy.ini`, `pre-commit-config.yaml`, or `tox.ini` detected
- Code style is project-local convention (Google-style docstrings, NumPy-style parameter blocks observed in `src/data_loader.py`, `src/models/dkt.py`)

**Reproducibility:**
- `SEED = 42` is the project convention for all stochastic notebook code (`CLAUDE.md` line 119, `README.md` line 179)
- `train_test_split(students, test_size=0.2, random_state=1)` in `src/data_loader.py` — the random_state of 1 is fixed by the Shi et al. (2022) protocol and is the only place where seed differs from 42
- `pyBKT.Model(seed=42)` in `src/models/bkt.py`

**Jupyter kernel:**
- `.venv/bin/python` registered as the project kernel (per `.claude/settings.local.json` allowed commands such as `Bash(.venv/bin/jupyter nbconvert *)`)

## Platform Requirements

**Development:**
- Linux (verified: kernel 6.18.7-76061807-generic, zsh shell) — paths use Unix separators throughout `src/`
- Python 3.10+ (running on 3.12.3)
- `srcml` 1.1+ installed system-wide (Ubuntu/Debian: `sudo apt-get install srcml`; project docs at `README.md` line 53 link to https://www.srcml.org/#download)
- Optional NVIDIA GPU + matching CUDA runtime for `torch` (CUDA 13.x wheels are bundled; CPU fallback works automatically)
- ~3 GB free disk for the CSEDM dataset under `data/CSEDM/` (gitignored)

**Production:**
- Not applicable — this is a TCC 1 research project; the "Deployment" phase of the EDM Process is deferred to TCC 2 (`CLAUDE.md` line 9)
- Artifacts of record are the executed notebooks plus binary outputs under `results/` (`*.pkl`, `*.json`, `*.csv`, `*.png`)

---

*Stack analysis: 2026-05-27*
