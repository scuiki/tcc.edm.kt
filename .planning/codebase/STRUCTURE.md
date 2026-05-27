# Codebase Structure

**Analysis Date:** 2026-05-27

## Directory Layout

```
tcc.edm.kt/
├── CLAUDE.md                       # Contexto do projeto + protocolo Shi et al.
├── README.md                       # Setup, dataset, pipeline, artefatos
├── PLAN_TCC1.md                    # Plano original do TCC 1
├── PLAN_KC_GENERATION.md           # Plano do pipeline KCGen-KT (LLM)
├── .gitignore                      # data/, .venv/, *.pt, caches
├── .claude/                        # Configuração Claude Code (local)
├── .harness/                       # Validation criteria e planos do GSD
├── .planning/                      # Documentação de codebase deste fluxo
│   └── codebase/                   # ARCHITECTURE.md, STRUCTURE.md, ...
├── apresentacao/                   # Slides de defesa do TCC (reveal.js)
│   ├── index.html                  # Markup dos slides
│   ├── STYLE.md                    # Guia de estilo dos slides
│   ├── README.md                   # Como executar a apresentação
│   ├── 4. MSGQ-21.01- MANUAL ... .pdf  # Manual de citações UniFacens
│   └── assets/                     # Tema, logos, figuras copiadas
│       ├── theme-unifacens.css     # Tema customizado reveal.js
│       ├── logo-unifacens-white.svg
│       ├── symbol.svg
│       └── fig-codedkt-martins-curves.png
├── data/                           # gitignored — dataset CSEDM
│   └── CSEDM/
│       ├── MainTable.csv           # 360k+ eventos, Spring 2019
│       ├── DatasetMetadata.csv
│       ├── ProgSnap2-v6-31Jul2019.pdf
│       ├── CodeStates/
│       │   └── CodeStates.csv      # 69.627 snapshots de código Java
│       └── LinkTables/
│           └── Subject.csv
├── docs/                           # Papers de referência + notas
│   ├── *.pdf                       # Papers (Shi, Piech, Corbett, srcML-DKT, ...)
│   ├── refs/                       # Resumos markdown dos papers
│   │   ├── INDEX.md
│   │   ├── shi2022_code_dkt.md
│   │   ├── piech2015_dkt.md
│   │   └── ... (12 outros papers)
│   ├── figures/                    # Figuras SVG/PNG para o TCC e apresentação
│   │   └── snippets/               # Snippets de código para figuras
│   ├── code_dkt_implementation.md  # Notas de implementação
│   ├── dkt_implementation.md
│   ├── srcml_dkt_implementation.md
│   ├── METODOLOGIA_FERRAMENTAS.md  # Texto da metodologia (TCC)
│   ├── comparison_plan.md
│   ├── eda_insights.md
│   └── plano_migracao_spring2019.md
├── notebooks/                      # Pipeline sequencial EDM (00 → 09)
│   ├── 00_problem_definition.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03b_kc_generation.ipynb     # KCGen-KT via LLM
│   ├── 03c_eda_kc_crossover.ipynb  # Cruzamento EDA × KCs canônicos
│   ├── 04_bkt.ipynb
│   ├── 05_dkt.ipynb
│   ├── 06_code_dkt.ipynb
│   ├── 07_comparison.ipynb         # Comparação final (4 modelos)
│   ├── 08_multirun_regeneration.ipynb  # 10 seeds × 5 assignments
│   ├── 09_srcml_dkt.ipynb
│   ├── EDA_PLAN.md
│   └── repositories.code-workspace
├── src/                            # Módulos Python reutilizáveis
│   ├── data_loader.py              # Carga, split 80/20, sequências KT
│   ├── code_features.py            # Paths AST via javalang + vocabulário
│   ├── srcml_features.py           # Paths AST via srcML CLI
│   ├── evaluation.py               # AUC pooled, build_problem_index
│   └── models/
│       ├── __init__.py             # vazio
│       ├── bkt.py                  # Wrapper pyBKT
│       ├── dkt.py                  # DKTModel + train/predict/loss
│       └── code_dkt.py             # CodeDKTModel (LSTM + atenção code2vec)
├── scripts/                        # Análises pós-pipeline one-shot
│   ├── analyze_kc_attention_codedkt.py
│   ├── analyze_kc_difficulty_codedkt.py
│   ├── build_methodology_figures.py
│   ├── inspect_coverage.py
│   ├── inspect_kcs.py
│   ├── viz_qmatrix_all.py
│   └── viz_qmatrix_single.py
├── results/                        # gitignored exceto a infra mínima
│   ├── sequences_bkt_dkt.pkl       # Sequências KT (Run.Program)
│   ├── sequences_code_dkt.pkl      # Sequências KT (+ Compile.Error)
│   ├── code_features_cache.pkl     # Cache paths javalang
│   ├── srcml_features_cache.pkl    # Cache paths srcML
│   ├── bkt_results_multirun.pkl    # BKT × 5 assignments (1 run)
│   ├── dkt_results_multirun.pkl    # DKT × 5 × 10 seeds
│   ├── code_dkt_results_multirun.pkl
│   ├── srcml_dkt_results_multirun.pkl
│   ├── codedkt_kc_retrained.pkl    # Estado para análise de KCs
│   ├── comparison_summary.json
│   ├── comparison_table_*.md / .png
│   ├── fig_*.png                   # Figuras finais (boxplot, heatmap, ...)
│   ├── sec*_*.png                  # Figuras de seções específicas
│   ├── kc_raw_{A439,...}.json      # KCs brutos por assignment
│   ├── kc_descriptions_{aid}.json  # KCs canônicos (pós-clustering)
│   ├── kc_clusters_{aid}.json
│   ├── kc_correctness_{aid}.json
│   ├── kc_translations.json
│   ├── qmatrix_{aid}.csv           # Matriz Problem × KC
│   ├── qmatrix_*_heatmap.png
│   ├── ast_signatures_{aid}.json
│   ├── codedkt_attention_*.csv / .json
│   ├── codedkt_kc_difficulty.json
│   └── validation_reports/         # Relatórios automatizados de validação
├── .venv/                          # gitignored — virtualenv Python 3.10+
└── create_notebook_07.py           # Helper one-shot para gerar 07
```

## Directory Purposes

**`data/CSEDM/` (gitignored):**
- Purpose: Dataset CSEDM bruto (ProgSnap2 v6).
- Contains: `MainTable.csv` (events), `CodeStates/CodeStates.csv` (snapshots Java), `LinkTables/Subject.csv`, `DatasetMetadata.csv`, especificação `ProgSnap2-v6-31Jul2019.pdf`.
- Key files: `data/CSEDM/MainTable.csv`, `data/CSEDM/CodeStates/CodeStates.csv`.

**`docs/`:**
- Purpose: Papers de referência (PDFs) + notas markdown + figuras para o TCC.
- Contains: PDFs (Shi 2022, Piech 2015, Corbett 1995, Pankiewicz 2025 srcML-DKT, Duan 2025 KCGen-KT, surveys de EDM/KT), `refs/*.md` (resumos), `figures/*.svg|png` (diagramas), planos de implementação (`*_implementation.md`), `METODOLOGIA_FERRAMENTAS.md` (texto do TCC).
- Key files: `docs/refs/INDEX.md`, `docs/METODOLOGIA_FERRAMENTAS.md`, `docs/comparison_plan.md`, `docs/srcml_dkt_implementation.md`.

**`notebooks/`:**
- Purpose: Pipeline EDM sequencial — uma fase por notebook, ordem indicada pelo prefixo numérico.
- Contains: 10 notebooks `.ipynb`, plano de EDA (`EDA_PLAN.md`), workspace VS Code (`repositories.code-workspace`).
- Key files: `notebooks/02_preprocessing.ipynb` (artefatos `.pkl`), `notebooks/07_comparison.ipynb` (output final), `notebooks/08_multirun_regeneration.ipynb` (multi-seed).

**`src/`:**
- Purpose: Biblioteca Python reutilizável; importada por todos os notebooks via `sys.path.insert(0, str(ROOT))` ou `sys.path.insert(0, str(ROOT/'src'))`.
- Contains: 4 módulos top-level + subpacote `models/`.
- Key files: `src/data_loader.py`, `src/evaluation.py`, `src/code_features.py`, `src/srcml_features.py`.

**`src/models/`:**
- Purpose: Implementações dos três modelos KT comparados.
- Contains: `bkt.py` (wrapper pyBKT), `dkt.py` (LSTM puro), `code_dkt.py` (LSTM + atenção code2vec); `__init__.py` vazio.
- Key files: `src/models/dkt.py:DKTModel`, `src/models/code_dkt.py:CodeDKTModel`.

**`scripts/`:**
- Purpose: Análises one-shot pós-pipeline executadas via `python scripts/<arquivo>.py`, fora dos notebooks principais.
- Contains: Análises de atenção/dificuldade por KC (Code-DKT), gerador de figuras para metodologia, inspetores de Q-matrix, visualizadores rápidos.
- Key files: `scripts/analyze_kc_difficulty_codedkt.py`, `scripts/analyze_kc_attention_codedkt.py`, `scripts/build_methodology_figures.py`.

**`results/` (gitignored exceto figs versionadas e .md):**
- Purpose: Artefatos intermediários (caches, sequências) e finais (tabelas, figuras, JSON de métricas).
- Contains: Pickles (`sequences_*.pkl`, `*_results_multirun.pkl`, `*_cache.pkl`), JSON (métricas, KCs), PNG (figuras), CSV (Q-matrix, atenção).
- Key files: `results/sequences_bkt_dkt.pkl`, `results/sequences_code_dkt.pkl`, `results/code_features_cache.pkl`, `results/comparison_summary.json`, `results/comparison_table_first_auc.md`.
- Generated: Sim.
- Committed: Não para `.pkl`/`.pt`; alguns `.png` e `.csv` ficam versionados conforme `.gitignore`.

**`apresentacao/`:**
- Purpose: Apresentação de defesa do TCC 1 em HTML/CSS (reveal.js, tema UniFacens).
- Contains: `index.html` (slides), `STYLE.md` (guia de estilo), `README.md`, manual oficial UniFacens (PDF), `assets/` (tema CSS, logos SVG, figuras PNG copiadas).
- Key files: `apresentacao/index.html`, `apresentacao/STYLE.md`, `apresentacao/assets/theme-unifacens.css`.

**`.planning/codebase/`:**
- Purpose: Documentação viva do codebase consumida por comandos GSD (mapeamento, planejamento, execução).
- Contains: `ARCHITECTURE.md`, `STRUCTURE.md` (este arquivo), e demais docs do focus area.

**`.harness/`:**
- Purpose: Critérios de validação e planos do fluxo GSD (Get Stuff Done).
- Contains: `plans/`, `validation_criteria/`, `eval_feedback/`.

**`.claude/`:**
- Purpose: Configuração local do Claude Code (não versionada).

**`.venv/` (gitignored):**
- Purpose: Virtualenv Python 3.10+ com `torch`, `pyBKT`, `javalang`, `anytree`, `sentence-transformers`, etc.

## Key File Locations

**Entry Points (notebooks):**
- `notebooks/00_problem_definition.ipynb`: Fase 1 EDM — definições formais (KC, métricas, problema).
- `notebooks/01_eda.ipynb`: EDA completa do CSEDM (8 seções).
- `notebooks/02_preprocessing.ipynb`: Carrega `MainTable.csv`, aplica split 80/20, grava `sequences_*.pkl`.
- `notebooks/03b_kc_generation.ipynb`: Pipeline KCGen-KT (LLM + clustering) → `kc_*.json`, `qmatrix_*.csv`.
- `notebooks/03c_eda_kc_crossover.ipynb`: Figuras de cruzamento EDA × KCs canônicos.
- `notebooks/04_bkt.ipynb`: Treino BKT (pyBKT) por assignment, salva `bkt_results.pkl`.
- `notebooks/05_dkt.ipynb`: Treino DKT (LSTM) por assignment.
- `notebooks/06_code_dkt.ipynb`: Treino Code-DKT vanilla (javalang) por assignment.
- `notebooks/07_comparison.ipynb`: Tabela comparativa final, Wilcoxon, figuras.
- `notebooks/08_multirun_regeneration.ipynb`: Re-roda DKT/Code-DKT/srcML-DKT com 10 seeds × 5 assignments.
- `notebooks/09_srcml_dkt.ipynb`: Treino srcML-DKT (extrator srcML, mesma arquitetura Code-DKT).

**Configuration:**
- `CLAUDE.md`: Contexto crítico do projeto (dataset, protocolo Shi et al., decisões metodológicas).
- `README.md`: Setup, dependências, comandos de execução.
- `.gitignore`: `data/`, `.venv/`, `__pycache__/`, caches `.pkl`, `*.pt`, `*.pth`, `.env`.

**Core Logic:**
- `src/data_loader.py`: `load_spring2019_split` (split 80/20), `filter_for_bkt_dkt`, `filter_for_code_dkt`, `build_sequences`, `truncate_sequences`, `load_labels`.
- `src/evaluation.py`: `build_problem_index`, `compute_auc` (pooled, first/all attempts).
- `src/code_features.py`: `load_code_states`, `extract_paths_javalang`, `build_cache`, `build_vocab`, `paths_to_tensor`, `build_code_input_tensor`.
- `src/srcml_features.py`: Análogos para `srcml` CLI — `extract_paths_srcml`, `build_cache_srcml`.
- `src/models/bkt.py`: `sequences_to_pyBKT_df`, `train_bkt`, `predict_bkt`, `train_and_evaluate`.
- `src/models/dkt.py`: `DKTModel` (nn.Module), `build_input_tensor`, `dkt_loss`, `train_dkt`, `predict_dkt`, `train_and_evaluate`.
- `src/models/code_dkt.py`: `CodeDKTModel`, `train_code_dkt`, `predict_code_dkt`, `train_and_evaluate`.

**Testing:**
- Não há suíte automatizada de testes; "smoke tests" estão embutidos nos notebooks (ex.: `notebooks/04_bkt.ipynb` célula 7 valida `train_and_evaluate` em A439 antes do loop completo).

**Documentação para o TCC (texto):**
- `docs/METODOLOGIA_FERRAMENTAS.md`: Seção de metodologia que vai para o texto do TCC.
- `docs/refs/*.md`: Resumos por paper (citáveis).
- `docs/refs/INDEX.md`: Índice de referências.

## Naming Conventions

**Files:**
- Notebooks: `NN_topic.ipynb` ou `NNX_topic.ipynb` (ex.: `02_preprocessing.ipynb`, `03b_kc_generation.ipynb`, `03c_eda_kc_crossover.ipynb`). Prefixo numérico indica ordem de execução. Sufixos `b`, `c` para notebooks paralelos a um estágio (ex.: `03b` e `03c` ambos pós-EDA, pré-modelagem).
- Módulos `src/`: `snake_case.py` (ex.: `data_loader.py`, `code_features.py`).
- Scripts: `verbo_objeto.py` (ex.: `analyze_kc_difficulty_codedkt.py`, `build_methodology_figures.py`, `inspect_coverage.py`, `viz_qmatrix_all.py`).
- Artefatos por assignment: `{nome}_{aid}.{ext}` ou `{nome}_A{aid}.{ext}` (ex.: `qmatrix_A439.csv`, `kc_raw_A439.json`, `ast_signatures_A439.json`).
- Resultados multirun: `{modelo}_results_multirun.pkl` (ex.: `dkt_results_multirun.pkl`, `srcml_dkt_results_multirun.pkl`).
- Figuras: `fig_{contexto}.png` (geral) ou `sec{N}{letra}_{descrição}.png` (figuras de seção específica em EDA/KC crossover).
- Documentação: `UPPERCASE.md` para top-level (`README.md`, `CLAUDE.md`, `PLAN_*.md`, `STYLE.md`); `lowercase_snake.md` em `docs/` (`eda_insights.md`, `comparison_plan.md`, `srcml_dkt_implementation.md`).

**Directories:**
- `lowercase_snake/` para diretórios funcionais (`notebooks/`, `src/`, `scripts/`, `results/`).
- `apresentacao/` em português (consistente com o TCC).
- `docs/refs/`, `docs/figures/snippets/`: subpastas funcionais.

**Constantes Python (nos notebooks):**
- `UPPERCASE`: `SEED`, `ROOT`, `DATA_ROOT`, `RESULTS_DIR`, `ASSIGNMENT_IDS`, `EVAL_AIDS`.

**Funções Python:**
- `snake_case`: `load_spring2019_split`, `build_sequences`, `extract_paths_javalang`, `train_and_evaluate`.
- Prefixos consistentes: `load_*` (I/O), `build_*` (construção de estruturas), `extract_*` (parsing), `train_*` / `predict_*` (modelagem), `compute_*` (métricas).

**Classes:**
- `CamelCase`: `DKTModel`, `CodeDKTModel` (ambas `nn.Module`).

## Where to Add New Code

**Nova fase do pipeline EDM:**
- Notebook: `notebooks/NN_topic.ipynb` com prefixo numérico próximo ao estágio.
- Convenções de notebook: célula 0 markdown (descrição + metodologia), célula 1 setup (`SEED=42`, `ROOT`, imports), seções numeradas `## 1 — Título`, "Achado" + "Implicação" no final de cada seção.

**Novo modelo KT:**
- Implementação: `src/models/<nome>.py` (ex.: `src/models/sakt.py`).
- Seguir a interface: classe `nn.Module` + `build_input_tensor` + `train_*` + `predict_*` + `train_and_evaluate(train_seqs, test_seqs, …) → dict`.
- Notebook orquestrador: `notebooks/NN_<nome>.ipynb`.
- Adicionar ao `notebooks/07_comparison.ipynb` (chave em `MODEL_ORDER` e arquivo em `load_all_results`).

**Nova feature de código (parser AST alternativo):**
- Módulo: `src/<nome>_features.py` espelhando a interface de `src/srcml_features.py` (`load_code_states`, `extract_paths_*`, `build_cache_*`).
- Reusar `build_vocab`, `paths_to_tensor`, `build_code_input_tensor` de `src/code_features.py` quando possível.

**Nova análise pós-pipeline:**
- Script: `scripts/<verbo>_<objeto>.py` (one-shot, executável via `python scripts/<arquivo>.py`).
- Não criar notebook se a análise é pontual e não vai entrar no TCC como artefato de pipeline.

**Nova figura para o TCC:**
- Geração: dentro de notebook (preferido) ou em `scripts/build_methodology_figures.py`.
- Output: `results/fig_<descrição>.png` (geral) ou `results/sec<seção>_<descrição>.png` (EDA/crossover).
- Para a apresentação: copiar para `apresentacao/assets/` mantendo nome descritivo (ex.: `fig-codedkt-martins-curves.png`).

**Novo paper de referência:**
- PDF em `docs/<autor><ano>_<topico>.pdf`.
- Resumo em `docs/refs/<autor><ano>_<topico>.md`.
- Atualizar `docs/refs/INDEX.md`.

**Slide novo na apresentação:**
- Editar `apresentacao/index.html` (reveal.js markup).
- Seguir convenções de `apresentacao/STYLE.md` (citações ABNT, classe `.slide-related` para trabalhos correlatos antes de uso, sem em-dashes em prosa).
- Assets em `apresentacao/assets/` (não referenciar `results/` diretamente — copiar).

**Utilitários compartilhados:**
- Se usado por ≥ 2 notebooks: colocar em `src/<modulo>.py`.
- Se usado por 1 notebook e 1 script: também em `src/`.
- Se é one-shot dentro de notebook único: célula do próprio notebook.

## Special Directories

**`data/`:**
- Purpose: Dataset CSEDM bruto.
- Generated: Não (baixado externamente).
- Committed: Não (gitignored linha 2 do `.gitignore`).

**`results/`:**
- Purpose: Artefatos gerados pelo pipeline (caches, sequências, modelos, figuras, JSON).
- Generated: Sim (totalmente regenerável executando os notebooks na ordem).
- Committed: Parcial — `.pkl`/`.pt`/`.pth` ignorados via `.gitignore`; alguns `.png`, `.csv`, `.md` são versionados conforme escolha.
- Subdir: `results/validation_reports/` (relatórios automatizados de validação).

**`.venv/`:**
- Purpose: Virtualenv Python 3.10+.
- Generated: Sim (`python -m venv .venv`).
- Committed: Não.

**`.harness/`, `.planning/`, `.claude/`:**
- Purpose: Ferramentas internas do fluxo GSD/Claude Code.
- Generated: Parcial (alguns arquivos manualmente, outros automatizados).
- Committed: `.harness/` e `.planning/` são versionados parcialmente; `.claude/` é local.

**`docs/figures/snippets/`:**
- Purpose: Snippets de código Java/Python usados como entrada para figuras de AST/atenção.
- Generated: Manualmente.
- Committed: Sim.

**`apresentacao/`:**
- Purpose: Slides de defesa.
- Generated: Manualmente (HTML + CSS).
- Committed: Sim (inclusive o manual PDF da UniFacens, que é referência oficial de citação).

---

*Structure analysis: 2026-05-27*
