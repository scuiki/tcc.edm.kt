# External Integrations

**Analysis Date:** 2026-05-27

## APIs & External Services

**LLM (Knowledge Component generation):**
- **Anthropic Claude API** — used in `notebooks/03b_kc_generation.ipynb` (Phase 3b of the pipeline) to generate raw Knowledge Components from student code and to label per-submission KC mastery
  - SDK/Client: `anthropic==0.99.0` (Python)
  - Client construction: `client = anthropic.Anthropic()` (reads `ANTHROPIC_API_KEY` from the process environment; no inline secrets)
  - Model: `claude-haiku-4-5-20251001` (set via the `LLM_MODEL` constant in the notebook)
  - Features used: `messages.create` with `system` and `messages` payloads, ephemeral prompt caching (`"cache_control": {"type": "ephemeral"}`), `max_tokens=512`
  - Error handling: explicit retry on `anthropic.APITimeoutError` and `anthropic.APIConnectionError` with exponential backoff (15s → 30s → 60s, up to 3 retries)
  - Cost controls: a `BudgetTracker` dataclass enforces a hard stop at $2.30 / $39 total (`BUDGET_USD`, `BUDGET_STOP`); per-call cost is computed from `usage.input_tokens`, `usage.output_tokens`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens` at the per-million prices `$0.80 / $4.00 / $1.00 / $0.08`
  - Auth: `ANTHROPIC_API_KEY` environment variable (not committed; not present in repo)

**Embeddings (KC clustering):**
- **Hugging Face Hub** — model weights are downloaded on first run by `sentence-transformers`
  - SDK/Client: `sentence-transformers==5.4.1` (uses `huggingface_hub==1.13.0` under the hood)
  - Model: `all-MiniLM-L6-v2` (`EMBEDDING_MODEL` constant in `notebooks/03b_kc_generation.ipynb`)
  - Usage: `SentenceTransformer(EMBEDDING_MODEL)` — cached locally by sentence-transformers after first download
  - Auth: none (public model)

**No other external APIs are called.** No HTTP/REST clients (`requests`, `httpx`) appear in `src/` or `scripts/`; both libraries are present only as transitive dependencies of `anthropic` and `huggingface_hub`.

## Data Storage

**Databases:**
- None — this is a file-based research pipeline, not a service

**Datasets (input):**
- **CSEDM / ProgSnap2 v6** — Java introductory dataset (Spring 2019, ~410 students)
  - Location: `data/CSEDM/` (gitignored, must be downloaded separately)
  - Provenance documented in `data/CSEDM/ProgSnap2-v6-31Jul2019.pdf` (dataset specification, shipped with the data)
  - Files consumed:
    - `data/CSEDM/MainTable.csv` — event log (~360k rows; 413 raw students → 410 after `min_attempts >= 3` filter)
    - `data/CSEDM/CodeStates/CodeStates.csv` — 69,627 code snapshots (`CodeStateID` → Java source)
    - `data/CSEDM/LinkTables/Subject.csv` — student-level metadata
    - `data/CSEDM/DatasetMetadata.csv` — ProgSnap2 dataset metadata
  - Loader: `src/data_loader.py` (`load_main_table`, `load_spring2019_split`, `filter_for_bkt_dkt`, `build_sequences`, `truncate_sequences`)
- **Label files:**
  - `data/early.csv`, `data/late.csv` — binary student labels referenced as targets in modelling notebooks

**File Storage (output artefacts):**
- All results land in `results/` (some files gitignored per `.gitignore`):
  - **Cached AST features:** `results/code_features_cache.pkl`, `results/srcml_features_cache.pkl` (gitignored, regenerable via `notebooks/03_code_features.ipynb`)
  - **Preprocessed KT sequences:** `results/sequences_bkt_dkt.pkl`, `results/sequences_code_dkt.pkl` (produced by `notebooks/02_preprocessing.ipynb`)
  - **Trained model artefacts:** `results/bkt_results.pkl`, `results/dkt_results.pkl`, `results/code_dkt_results.pkl`, `results/code_dkt_analysis.pkl`, `results/codedkt_kc_retrained.pkl`
  - **Multi-run results:** `results/bkt_results_multirun.pkl`, `results/dkt_results_multirun.pkl`, `results/code_dkt_results_multirun.pkl`, `results/srcml_dkt_results_multirun.pkl`
  - **LLM-derived KC artefacts (per-assignment):** `results/kc_raw_A{439,487,492,494,502}.json`, `results/kc_descriptions_A*.json`, `results/kc_clusters_A*.json`, `results/kc_correctness_A*.json`, `results/qmatrix_A*.csv`, `results/ast_signatures_A*.json`, `results/kc_translations.json`
  - **Comparison tables:** `results/comparison_summary.json`, `results/comparison_table_first_auc.md`, `results/comparison_table_all_auc.md`, `results/comparison_table_pooled.md` (plus PNG renders)
  - **Figures:** `results/fig_*.png`, `results/sec*.png`, `results/qmatrix_*_heatmap.png`
  - **Attention diagnostics:** `results/code_dkt_attention_paths_a439.csv`, `results/codedkt_attention_by_concept.csv`, `results/codedkt_attention_examples.json`, `results/codedkt_attention_examples_curated.json`
  - **Validation reports:** `results/validation_reports/*.md` (one per executed notebook)
- `*.pt`, `*.pth`, `*.h5` are gitignored (`.gitignore`) — no PyTorch model weights are persisted; models are re-trained on each notebook run

**Caching:**
- Sentence-Transformers cache: managed by `huggingface_hub` under `~/.cache/huggingface/` (outside the repo)
- Anthropic prompt caching: server-side ephemeral cache, billed via `cache_creation_input_tokens` / `cache_read_input_tokens` (not a local cache)

## Authentication & Identity

**Auth Provider:**
- None — no user authentication, no session management
- The only credential in scope is `ANTHROPIC_API_KEY` (Anthropic API token), read from the shell environment by `anthropic.Anthropic()` in `notebooks/03b_kc_generation.ipynb`

## Monitoring & Observability

**Error Tracking:**
- None — no Sentry, Rollbar, or equivalent
- Per-notebook validation is captured manually in `results/validation_reports/*.md` (e.g., `00_problem_definition_validation.md`, `01_eda_validation.md`, `02_preprocessing_validation.md`, `03b_kc_generation_validation.md`)

**Logs:**
- `print()` statements in notebooks and `tqdm` progress bars; no structured logger
- LLM call accounting is in-process via the `BudgetTracker.report()` helper in `notebooks/03b_kc_generation.ipynb`

## CI/CD & Deployment

**Hosting:**
- Not applicable — this is a research notebook project. The TCC 2 prototype concept lives as a static HTML file at `docs/tcc2_prototipo.html` and is not deployed.

**CI Pipeline:**
- None detected (no `.github/workflows/`, `.gitlab-ci.yml`, `circleci/`, `Jenkinsfile`)
- Reproducibility is enforced by the convention in `README.md` lines 62–65: re-execute any notebook via `jupyter nbconvert --to notebook --execute notebooks/<n>.ipynb --output notebooks/<n>.ipynb --ExecutePreprocessor.timeout=600`

**Presentation:**
- `apresentacao/index.html` plus `apresentacao/assets/theme-unifacens.css` and `apresentacao/assets/logo-unifacens-white.svg` constitute the TCC 1 defense deck (static HTML, no build step)
- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — institutional citation manual (Facens), referenced from the deck

## Environment Configuration

**Required env vars:**
- `ANTHROPIC_API_KEY` — required only when executing `notebooks/03b_kc_generation.ipynb`; all other notebooks run with no environment configuration

**Secrets location:**
- Not stored in the repo. The expected practice is to export `ANTHROPIC_API_KEY` in the shell (e.g., `~/.zshrc` or just-in-time before `jupyter notebook`). No `.env` file present.

## Webhooks & Callbacks

**Incoming:**
- None — no HTTP server, no webhook endpoints

**Outgoing:**
- None — the only outbound network traffic is to `api.anthropic.com` (via the `anthropic` SDK) and to `huggingface.co` (one-time model download via `sentence-transformers`)

## External CLI Tools

**`srcml` (system binary, /usr/bin/srcml, version 1.1.0):**
- Replaces `javalang` for Phase 2 (srcML-DKT) because srcML parses non-compilable Java and so can ingest `Compile.Error` events
- Invoked from `src/srcml_features.py` via `subprocess.run(["srcml", "--language=Java"], ...)` reading Java code on stdin and emitting srcML XML on stdout
- XML namespace: `http://www.srcML.org/srcML/src` (handled by `_strip_ns` and `_NS_PREFIX` in `src/srcml_features.py`)
- Verification command (used in `README.md` and `CLAUDE.md`): `srcml --version`

**`pdftotext` (allowed in `.claude/settings.local.json`):**
- Used ad-hoc to convert reference papers under `docs/` (e.g., `docs/Code-DKT.pdf`, `docs/deepKnowledgeTracing.pdf`) into plain text for grep/quote work
- Not part of the modelling pipeline

## External Reference Material

**Reference papers (read-only, under `docs/`):**
- `Code-DKT.pdf` (Shi et al., 2022) — primary architectural reference for `src/models/code_dkt.py`
- `deepKnowledgeTracing.pdf` (Piech et al., 2015) — DKT reference for `src/models/dkt.py`
- `893CorbettAnderson1995.pdf` (Corbett & Anderson, 1995) — BKT reference for `src/models/bkt.py`
- `ProgSnap2.pdf` — dataset format specification
- `2025.EDM.short-papers.83.pdf` (Pankiewicz, Shi & Baker, 2025) — srcML-DKT reference for `src/srcml_features.py`
- `2309.04761v4.pdf` (Duan et al., 2025) — KCGen-KT reference for `notebooks/03b_kc_generation.ipynb`
- Survey/context: `kt_survey.pdf`, `edm_review.pdf`, `EDM_LLM.pdf`, `edm_prediction.pdf`, `AutomatedKC.pdf`, `Benefits_of_Educational_Data_Mining.pdf`, `applsci-15-00772.pdf`, `Master_Thesis_-_Colin_Busropan.pdf`, `Artigo+2+Desafios+na+aprendizagem+de+lógica+de+programação.pdf`
- Subdirectories: `docs/figures/`, `docs/refs/`

**Reference implementation (read-only, outside repo):**
- `/home/leokuntz/Documents/repositories/experiments/Code-DKT/src/` — official Code-DKT codebase; `c2vRNNModel.py`, `run.py`, `config.py`, `path_extractor.py` are mirrored conceptually into this project's `src/code_features.py` and `src/models/code_dkt.py`

---

*Integration audit: 2026-05-27*
