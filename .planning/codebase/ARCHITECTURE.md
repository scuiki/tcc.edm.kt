<!-- refreshed: 2026-05-27 -->
# Architecture

**Analysis Date:** 2026-05-27

## System Overview

```text
┌─────────────────────────────────────────────────────────────────────┐
│  EDM Process — Pipeline Orquestrado por Notebooks                   │
│  Fase 1: Problem Definition  →  Fase 2: Data Preparation  →         │
│  Fase 3: Modelling & Evaluation  →  Fase 4: Deployment (TCC 2)      │
├──────────────────┬──────────────────┬──────────────────┬────────────┤
│ 00 Problem Def.  │ 01 EDA           │ 04 BKT (pyBKT)   │ 07 Compar. │
│ `notebooks/00_*` │ `notebooks/01_*` │ `notebooks/04_*` │ `notebooks/│
│                  │ 02 Preprocess.   │ 05 DKT (LSTM)    │  07_*`     │
│                  │ `notebooks/02_*` │ `notebooks/05_*` │            │
│                  │ 03b KCGen-KT     │ 06 Code-DKT      │ 08 Multi-  │
│                  │ `notebooks/03b_*`│ `notebooks/06_*` │  run       │
│                  │ 03c KC×EDA       │ 09 srcML-DKT     │            │
│                  │ `notebooks/03c_*`│ `notebooks/09_*` │            │
└────────┬─────────┴────────┬─────────┴────────┬─────────┴─────┬──────┘
         │                  │                  │               │
         ▼                  ▼                  ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  src/ — Módulos Python Reutilizáveis (importados pelos notebooks)   │
│                                                                       │
│  data_loader.py       code_features.py    srcml_features.py          │
│  evaluation.py        models/bkt.py       models/dkt.py              │
│                       models/code_dkt.py                              │
└────────┬─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Data Layer                                                          │
│  Input (read-only):   `data/CSEDM/MainTable.csv`                     │
│                       `data/CSEDM/CodeStates/CodeStates.csv`         │
│  Artefatos (cache):   `results/sequences_bkt_dkt.pkl`                │
│                       `results/sequences_code_dkt.pkl`               │
│                       `results/code_features_cache.pkl`              │
│                       `results/srcml_features_cache.pkl`             │
│  Outputs:             `results/*_results_multirun.pkl`               │
│                       `results/fig_*.png`, `results/comparison_*.md` │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| `data_loader` | Carrega `MainTable.csv`, aplica filtro `min_attempts>=3`, split 80/20 com `random_state=1`, constrói sequências KT por estudante/assignment, truncamento em 50 tentativas | `src/data_loader.py` |
| `code_features` | Extrai paths AST via `javalang`, constrói vocabulário (token/path) e tensores `(R,3)` para Code-DKT; cache multiprocesso | `src/code_features.py` |
| `srcml_features` | Extrai paths AST via `srcml` CLI (tolera código não-compilável), reutiliza vocabulário/tensorização de `code_features` | `src/srcml_features.py` |
| `evaluation` | `build_problem_index` (mapeamento `ProblemID → idx` global train+test) e `compute_auc` (pooled, first/all-attempts) | `src/evaluation.py` |
| `models.bkt` | Wrapper `pyBKT`: `sequences_to_pyBKT_df`, `train_bkt`, `predict_bkt`, `train_and_evaluate` | `src/models/bkt.py` |
| `models.dkt` | `DKTModel` (LSTM + Sigmoid), `build_input_tensor` (one-hot 2M), loss BCE Piech-2015 Eq. 3 | `src/models/dkt.py` |
| `models.code_dkt` | `CodeDKTModel` (LSTM + atenção code2vec sobre R paths), reusa `dkt_loss` | `src/models/code_dkt.py` |
| Notebooks | Orquestradores sequenciais — uma fase EDM por arquivo; importam de `src/` e gravam artefatos em `results/` | `notebooks/*.ipynb` |
| Scripts | Pós-análises one-shot (curvas de aprendizado, atenção por KC, figuras de metodologia) | `scripts/*.py` |
| Apresentação | Slides de defesa do TCC em reveal.js (HTML+CSS, tema UniFacens) | `apresentacao/` |

## Pattern Overview

**Overall:** Pipeline sequencial orquestrado por notebooks (Data Science Notebook Pipeline) + biblioteca compartilhada `src/`.

**Key Characteristics:**
- Cada notebook é um estágio do EDM Process e produz artefatos `.pkl`/`.json`/`.png` em `results/`.
- Notebooks não contêm lógica de modelagem reutilizável — apenas orquestração, parametrização (`SEED=42`, paths) e narração markdown.
- `src/` expõe funções puras (`train_*`, `predict_*`, `compute_auc`, `build_*`) com assinaturas estáveis chamadas por múltiplos notebooks.
- Comunicação entre estágios é feita exclusivamente via arquivos em `results/`, nunca via estado de processo.
- Modelos KT (BKT/DKT/Code-DKT/srcML-DKT) compartilham a mesma interface `train_and_evaluate(train_seqs, test_seqs, …) → dict` para consumo uniforme em `07_comparison.ipynb`.

## Layers

**Notebook Orchestration Layer:**
- Purpose: Sequenciar fases EDM, parametrizar experimentos, narrar achados em markdown.
- Location: `notebooks/`
- Contains: Imports de `src/`, células de carregamento (`pickle.load`), loops por assignment, plots `matplotlib`/`seaborn`, escrita de artefatos.
- Depends on: `src/data_loader`, `src/code_features`, `src/srcml_features`, `src/evaluation`, `src/models/*`.
- Used by: Nenhum (são entry points executáveis).

**Reusable Code Layer (`src/`):**
- Purpose: Funções e classes reutilizáveis para carregamento, features e modelagem.
- Location: `src/` e `src/models/`
- Contains: Funções puras, classes `nn.Module` (DKT, Code-DKT), wrappers `pyBKT`.
- Depends on: `pandas`, `numpy`, `torch`, `pyBKT`, `sklearn`, `javalang`, `anytree`, `srcml` (CLI subprocess).
- Used by: Todos os notebooks (`05_dkt`, `06_code_dkt`, `08_multirun_regeneration`, `09_srcml_dkt`, `04_bkt`).

**Data Layer:**
- Purpose: Persistir dados brutos, caches de features e artefatos de resultado.
- Location: `data/CSEDM/` (read-only, gitignored) e `results/` (gitignored exceto README/figs).
- Contains: `MainTable.csv`, `CodeStates.csv`, `LinkTables/`, pickles de sequências e modelos, JSON de métricas, PNG de figuras.
- Depends on: Sistema de arquivos local.
- Used by: Toda a camada de notebooks e scripts.

**Apresentação Layer (independente):**
- Purpose: Slides de defesa do TCC.
- Location: `apresentacao/`
- Contains: `index.html` (reveal.js), `assets/theme-unifacens.css`, `assets/*.svg`, manual PDF de citações.
- Depends on: Nada do pipeline Python — consome apenas figuras já geradas em `results/` e copia para `assets/`.

## Data Flow

### Primary Pipeline Path (CSEDM raw → AUC comparison)

1. **Carga e split 80/20** (`src/data_loader.py:243` `load_spring2019_split`) — lê `data/CSEDM/MainTable.csv`, filtra `EventType=='Run.Program'`, mantém estudantes com `>= 3` tentativas globais, aplica `train_test_split(students, test_size=0.2, random_state=1)` → 328 train + 82 test.
2. **Filtragem por modelo** (`src/data_loader.py:51` `filter_for_bkt_dkt` / `:77` `filter_for_code_dkt`) — BKT/DKT mantém apenas `Run.Program`; Code-DKT inclui `Compile.Error` com `correct=0`.
3. **Construção de sequências** (`src/data_loader.py:108` `build_sequences`) — agrupa por `SubjectID`, ordena por `ServerTimestamp`, marca `is_first_attempt` por `ProblemID`.
4. **Truncagem** (`src/data_loader.py:168` `truncate_sequences`) — mantém últimas 50 tentativas, recalcula `is_first_attempt`.
5. **Persistência de sequências** (`notebooks/02_preprocessing.ipynb`) — grava `results/sequences_bkt_dkt.pkl` e `results/sequences_code_dkt.pkl`.
6. **Extração de features AST** (`src/code_features.py:192` `build_cache` e `src/srcml_features.py:210` `build_cache_srcml`) — multiprocessing.Pool sobre `CodeStates.csv`, cache em `results/code_features_cache.pkl` e `results/srcml_features_cache.pkl`.
7. **Indexação de problemas** (`src/evaluation.py:16` `build_problem_index`) — scan global train+test para mapear `ProblemID → idx`.
8. **Vocabulário de paths** (`src/code_features.py:227` `build_vocab`) — construído APENAS do train set (evita data leakage); tokens/paths do test ausentes mapeiam para 0 (PAD/UNK).
9. **Treino do modelo KT** — um modelo por assignment:
   - BKT: `src/models/bkt.py:39` `train_bkt` (EM via pyBKT, `seed=42`).
   - DKT: `src/models/dkt.py:179` `train_dkt` (Adam lr=0.0005, 40 épocas, batch=128, grad clip=10).
   - Code-DKT: `src/models/code_dkt.py:146` `train_code_dkt` (LSTM + atenção, mesmas hyperparams).
   - srcML-DKT: reusa `train_code_dkt` com cache srcML.
10. **Predição** (`*.py:predict_*`) — `correct_predictions` para cada evento `t+1` a partir do estado em `t`.
11. **AUC pooled** (`src/evaluation.py:38` `compute_auc`) — concatena todas as predições, calcula `roc_auc_score`; flag `first_attempt_only=True` filtra para a métrica primária do paper.
12. **Persistência de resultados multirun** (`notebooks/08_multirun_regeneration.ipynb`) — 10 seeds (42–51) × 5 assignments → `results/*_results_multirun.pkl`.
13. **Comparação final** (`notebooks/07_comparison.ipynb`) — carrega 4 pickles, tabela `mean ± std`, Wilcoxon signed-rank, figuras `fig_comparison_*.png`, `fig_seed_variance_boxplot.png`, `fig_delta_vs_dkt.png`.

### Secondary Flow: KCGen-KT (descoberta de KCs semânticos)

1. **Diversity sampling** (`notebooks/03b_kc_generation.ipynb`) — amostra submissões corretas por problema (`CodeStates.csv`).
2. **LLM call** (Claude/Anthropic) — gera KCs brutos por problema → `results/kc_raw_{aid}.json`.
3. **Clusterização** (Sentence-BERT + HAC) — agrega KCs em rótulos canônicos → `results/kc_clusters_{aid}.json`, `results/kc_descriptions_{aid}.json`.
4. **Q-matrix binária** — `results/qmatrix_{aid}.csv` (ProblemID × KC).
5. **Cruzamento com EDA** (`notebooks/03c_eda_kc_crossover.ipynb`) — figuras `sec9*_*.png` relacionam KCs canônicos a taxas de acerto/dificuldade.

**State Management:**
- Cada notebook é stateless entre execuções: estado vive em `results/*.pkl`.
- Reprodutibilidade garantida por: `SEED=42` em todos os notebooks (numpy/torch/random), `random_state=1` no split 80/20, `random.Random(seed)` na amostragem de paths em `code_features.py:175`.

## Key Abstractions

**Sequência KT:**
- Purpose: Representação canônica de tentativas de um estudante em um assignment para todos os modelos KT.
- Examples: lista de `dict` retornada por `build_sequences`; persistida em `results/sequences_bkt_dkt.pkl`, `results/sequences_code_dkt.pkl`.
- Pattern: cada elemento é `{"subject_id": str, "assignment_id": int, "events": pd.DataFrame}` com colunas `ProblemID, correct, is_first_attempt, ServerTimestamp, CodeStateID, EventType`.

**Path AST (code2vec):**
- Purpose: Representação tripla `(start_token, path_str, end_token)` de um caminho entre folhas da AST; entrada do mecanismo de atenção do Code-DKT.
- Examples: `src/code_features.py:88` `extract_paths_javalang`, `src/srcml_features.py:88` `extract_paths_srcml`.
- Pattern: filtros `max_path_length=8`, `max_path_width=2`, `R=50` paths por submissão; vocabulário mapeia tokens/paths para índices `Embedding(N+2, 100)`.

**Modelo KT (interface uniforme):**
- Purpose: Toda família de modelos expõe `train_and_evaluate(train_seqs, test_seqs, …) → dict` com chaves `model`, `all_auc`, `first_auc`, `n_train*`, `n_test*` para consumo pelo notebook de comparação.
- Examples: `src/models/bkt.py:95`, `src/models/dkt.py:327`, `src/models/code_dkt.py:307`.
- Pattern: separação `train_*` / `predict_*` / `compute_auc` permite reuso e testes parciais.

**AUC pooled:**
- Purpose: Métrica única sobre todas as predições concatenadas (sem média por estudante), seguindo o evaluation.py do repositório oficial Code-DKT.
- Examples: `src/evaluation.py:38` `compute_auc` (também replicado em `src/models/bkt.py:74` para conveniência local).
- Pattern: `roc_auc_score(df["correct"], df["correct_predictions"])` após filtro opcional `is_first_attempt==True`.

## Entry Points

**Notebooks (entry points humanos):**
- Location: `notebooks/00_problem_definition.ipynb` até `notebooks/09_srcml_dkt.ipynb`.
- Triggers: execução manual via Jupyter ou `jupyter nbconvert --to notebook --execute`.
- Responsibilities: orquestrar uma fase do EDM Process, parametrizar `SEED=42`, carregar `results/*.pkl` produzidos por estágios anteriores, gravar novos artefatos.

**Scripts pós-análise:**
- Location: `scripts/analyze_kc_attention_codedkt.py`, `scripts/analyze_kc_difficulty_codedkt.py`, `scripts/build_methodology_figures.py`, `scripts/inspect_*.py`, `scripts/viz_qmatrix_*.py`.
- Triggers: execução one-shot via `python scripts/<arquivo>.py`.
- Responsibilities: análises ad-hoc (curvas de aprendizado por KC, mapas de atenção, figuras para a apresentação) que não pertencem ao pipeline principal.

**Apresentação:**
- Location: `apresentacao/index.html`.
- Triggers: abertura em browser ou servidor estático.
- Responsibilities: slides reveal.js da defesa; consome figuras já geradas em `results/` (copiadas para `apresentacao/assets/`).

## Architectural Constraints

- **Reprodutibilidade obrigatória:** `SEED=42` em todos os notebooks (`np.random.seed`, `torch.manual_seed`, `random.Random(seed)` interno em `code_features.py`). O split 80/20 usa `random_state=1` (não 42) por fidelidade ao protocolo do Shi et al. (2022). Quebrar essa convenção invalida comparação com Table 1 do paper.
- **Sem retreino em `07_comparison.ipynb`:** o notebook de comparação é puramente analítico — carrega `*_results_multirun.pkl` e calcula tabelas/figuras. Qualquer mudança em hiperparâmetros exige re-rodar `08_multirun_regeneration.ipynb` antes.
- **Vocabulário Code-DKT/srcML-DKT construído só do train:** `build_vocab` em `src/code_features.py:227` recebe apenas o cache do train. Construir do train+test causa data leakage sobre tokens/paths que aparecem apenas no test.
- **`problem_to_idx` é global train+test:** `build_problem_index` em `src/evaluation.py:16` escaneia ambos os splits para garantir que um problema visto apenas no test ainda tenha índice válido (M problemas por assignment, ~10 no CSEDM).
- **`Compile.Error` apenas para Code-DKT/srcML-DKT:** BKT e DKT não processam código, então `filter_for_bkt_dkt` (`src/data_loader.py:51`) descarta `Compile.Error`; Code-DKT (`:77`) os mantém como `correct=0`.
- **Multiprocessing requer `if __name__ == "__main__"`:** `build_cache` e `build_cache_srcml` usam `mp.Pool` — ao executar dentro de notebook, garantir que o caller respeita o protocolo (notebooks usam por consequência do Jupyter wrapper). Para pyBKT, ver MEMORY: E-step só rodava dentro de `__main__` em pyBKT 1.4.1, precisou de patch local.
- **Dataset gitignored:** `data/` inteiro está em `.gitignore` (linha 2). Pipelines não podem assumir dado versionado; cada checkout precisa baixar `MainTable.csv` e `CodeStates.csv` manualmente.
- **srcML é dependência de sistema (CLI):** `src/srcml_features.py:119` chama `subprocess.run(["srcml", "--language=Java"])`. Sem o binário instalado (`apt-get install srcml`), o notebook 09 falha.
- **Comparabilidade BKT vs DKT/Code-DKT:** BKT roda 1 vez (determinístico), DKT/Code-DKT/srcML-DKT rodam 10 vezes (seeds 42–51) por decisão metodológica documentada em `notebooks/08_multirun_regeneration.ipynb`. Comparação em `07_comparison.ipynb` reporta `mean ± std` para deep models e valor pontual para BKT.

## Anti-Patterns

### Construir vocabulário com cache combinado train+test

**What happens:** Chamar `build_vocab(cache_raw_all)` onde `cache_raw_all` contém CodeStateIDs de train e test.
**Why it's wrong:** Vaza informação do test set para o vocabulário e infla artificialmente a cobertura — o modelo aprende embeddings de tokens que só existem no test.
**Do this instead:** Filtrar `cache_raw` para conter apenas CodeStateIDs do train antes de chamar `build_vocab` (`src/code_features.py:227`). Tokens novos no test devem mapear para índice 0 (PAD/UNK) automaticamente via `paths_to_tensor` (`:258`).

### Reaplicar split nos notebooks downstream

**What happens:** Recalcular `train_test_split` em `04_bkt.ipynb`, `05_dkt.ipynb` etc. em vez de carregar `results/sequences_bkt_dkt.pkl`.
**Why it's wrong:** Pode introduzir splits inconsistentes entre modelos (mesmo `random_state=1` se a ordem dos estudantes diferir) e quebra a comparabilidade do notebook 07.
**Do this instead:** Sempre carregar `pickle.load(open("results/sequences_bkt_dkt.pkl"))` ou `sequences_code_dkt.pkl` e usar `seqs["train"][aid]` / `seqs["test"][aid]` (ver `notebooks/04_bkt.ipynb` célula 3).

### Calcular AUC com média por estudante

**What happens:** Computar `roc_auc_score` por estudante e tirar média aritmética.
**Why it's wrong:** Não é o protocolo do paper (Shi et al., 2022) nem de Piech et al. (2015). Penaliza estudantes com poucas tentativas e introduz instabilidade.
**Do this instead:** Usar `src/evaluation.py:38` `compute_auc(pred_df)` (pooled): concatena todas as linhas antes de chamar `roc_auc_score` uma única vez.

### Não fixar seed no notebook

**What happens:** Esquecer `np.random.seed(SEED)` / `torch.manual_seed(SEED)` no início do notebook.
**Why it's wrong:** Resultados não são reproduzíveis; cada execução produz AUCs diferentes e invalida o critério de conclusão 4 do CLAUDE.md.
**Do this instead:** Todo notebook começa com bloco padrão `SEED = 42; np.random.seed(SEED); torch.manual_seed(SEED)` (ver `notebooks/02_preprocessing.ipynb` célula 1, `notebooks/04_bkt.ipynb` célula 1).

### Usar `javalang` para `Compile.Error` events

**What happens:** Tentar parsear código de eventos `Compile.Error` com `extract_paths_javalang` (`src/code_features.py:88`).
**Why it's wrong:** `javalang` exige código sintaticamente válido — silenciosamente retorna lista vazia em `try/except`, fazendo o Code-DKT perder ~30% dos eventos (109k Compile.Error de 360k totais).
**Do this instead:** Para Code-DKT vanilla (Shi et al., 2022), filtrar `Compile.Error` antes (já é feito em `sequences_bkt_dkt.pkl`). Para srcML-DKT, usar `extract_paths_srcml` (`src/srcml_features.py:88`) que tolera código parcial.

## Error Handling

**Strategy:** "Falha silenciosa controlada" para parsing de AST + asserts agressivos em loaders de dados.

**Patterns:**
- Parsing AST com `try/except` retornando lista vazia em vez de propagar exceção (`src/code_features.py:113`, `src/srcml_features.py:119`): código que não compila vira "submissão sem features" em vez de quebrar o pipeline inteiro.
- `assert` em `src/data_loader.py:71` confirma que o filtro `Run.Program` é exclusivo (defesa contra `EventType` inesperado vazando para BKT/DKT).
- `subprocess.run(..., timeout=10)` em `src/srcml_features.py:122`: srcML pode travar em código patológico; timeout evita deadlock.
- `compute_auc` retorna `np.nan` quando `correct.nunique() < 2` (`src/evaluation.py:58`, `src/models/bkt.py:88`) em vez de levantar exceção — permite agregação em loops por assignment sem `try/except`.

## Cross-Cutting Concerns

**Logging:** `print()` direto nos notebooks/loops de treino (ex.: `f"  Época {epoch}/{epochs} — loss: {avg_loss:.4f}"` em `src/models/dkt.py:261` e `src/models/code_dkt.py:235`). Não há framework de logging (`logging` module) — pipeline orientado a notebook.

**Validation:** asserts em `data_loader.py` (`:71`, `:72`, `:100`) garantem invariantes de filtragem; notebooks têm seções "Validação de reprodutibilidade" com checks numéricos (ex.: `notebooks/02_preprocessing.ipynb` célula 4 valida taxa de corretos ≈ 23.68%).

**Authentication:** Não aplicável — projeto local sem rede (exceto chamadas à API Anthropic em `notebooks/03b_kc_generation.ipynb`, lidas via `.env` gitignored).

**Reprodutibilidade:** `SEED=42` em todos os notebooks; `random_state=1` no split (fidelidade ao paper); `random.Random(seed)` interno em `code_features.py:175` para amostragem de paths sem afetar estado global.

---

*Architecture analysis: 2026-05-27*
