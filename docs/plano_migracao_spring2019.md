# Plano: Migração para Spring 2019 Full Dataset (410 alunos) + Reexecução do Pipeline

## Context

`data/Data/MainTable.csv` é o dataset Spring 2019 completo que Shi et al. (2022) usaram:
- Com filtro `min_attempts >= 3`: exatamente **410 alunos**, **23.68% de corretos** — match exato com o paper
- Split `train_test_split(students, test_size=0.2, random_state=1)` → **328 treino + 82 teste**
- Teste tem **todos os 5 assignments** (A439, A487, A492, A494, A502)
- `data/Data/CodeStates/CodeStates.csv`: 69.627 registros, cobertura 100% do novo train split

`Release/` (329 alunos, 75/25) é o CSEDM Data Challenge — não é o que o paper usa.

**Objetivo:** consolidar `data/CSEDM/` com o dataset do paper, reexecutar o pipeline completo
(preprocessing → KC generation → BKT) e corrigir todos os insights gerados pelo harness.

**Nota sobre `min_attempts`:** o filtro conta `Run.Program` globalmente (todos os assignments
somados). Um estudante com ≥3 Run.Program no semestre inteiro passa — mesmo distribuídos entre
assignments diferentes. Essa é a definição que produz o match exato de 410 alunos e 23.68%.

---

## Passo 0 — Pré-condições e reorganização do diretório `data/`

### 0a — Verificações antes de remover diretórios

**Verificar referências a `CodeWorkout` em código** (a pasta existe em `data/CSEDM/CodeWorkout/`):
```bash
grep -r 'CodeWorkout' notebooks/ src/ docs/ --include='*.py' --include='*.ipynb' --include='*.md'
```
Se retornar zero resultados em código — remoção segura. Referências em markdown de análise
(e.g., "Java 8; CodeWorkout" em outputs de células) são safe — não são paths de arquivo.

**Verificar que `F19_Release_All_05_23_22/` é idêntico a `All/`** antes de remover:
```bash
diff <(head -1 data/CSEDM/All/Data/MainTable.csv) \
     <(head -1 data/F19_Release_All_05_23_22/Data/MainTable.csv)
```
Se colunas idênticas — remoção segura.

### 0b — Deletar artefatos stale antes de re-executar notebooks

```bash
rm -f results/sequences_bkt_dkt.pkl results/sequences_code_dkt.pkl results/bkt_results.pkl
```
**Motivo:** se `04_bkt.ipynb` ler um pkl antigo (Release/Train) por execução parcial ou acidente,
os resultados ficam errados sem qualquer mensagem de erro. Deletar força a regeneração.

### 0c — Reorganização do diretório `data/`

**Problema:** atualmente os dados do paper estão em `data/Data/` e o diretório `data/CSEDM/`
contém o Release/ (CSEDM Challenge) e o All/ (Fall 2019). Queremos que `data/CSEDM/` seja
o diretório único com o Spring 2019 completo.

**Ações (operações de sistema de arquivos):**
1. Mover `data/Data/MainTable.csv` → `data/CSEDM/MainTable.csv`
2. Mover `data/Data/CodeStates/CodeStates.csv` → `data/CSEDM/CodeStates/CodeStates.csv`
3. Mover `data/Data/DatasetMetadata.csv` → `data/CSEDM/DatasetMetadata.csv`
4. Mover `data/Data/LinkTables/Subject.csv` → `data/CSEDM/LinkTables/Subject.csv`
5. Remover `data/CSEDM/Release/` (CSEDM Challenge — não usar para modelagem KT)
6. Remover `data/CSEDM/All/` (Fall 2019 — não é nosso dataset)
7. Remover `data/CSEDM/CodeWorkout/`, `data/CSEDM/Test/`, `data/CSEDM/Test_Solution/`, `data/CSEDM/Train/`
8. Remover `data/Data/` (após mover conteúdo)
9. Remover `data/F19_Release_All_05_23_22/` (snapshot arquivado, idêntico ao All/)
10. Manter: `data/early.csv`, `data/late.csv` (labels do challenge — úteis para referência)

**Resultado:** `data/CSEDM/` terá apenas `MainTable.csv`, `CodeStates/`, `DatasetMetadata.csv`,
`LinkTables/`. A variável `DATA_ROOT = Path("../data/CSEDM")` existente em todos os notebooks
passa a apontar diretamente para o dataset do paper.

---

## Passo 1 — `src/data_loader.py` — nova função + limpeza de entradas obsoletas

### 1a — Limpar `_SPLITS` (todas as 5 entradas apontam para paths que serão deletados)

```python
# ANTES (5 entradas — todos os paths serão deletados no Passo 0)
_SPLITS = {
    "all":           ("All/Data/MainTable.csv", None),
    "all_train":     ("Train/Data/MainTable.csv", "Train/early.csv"),
    "all_test":      ("Test/Data/MainTable.csv",  "Test/early.csv"),
    "release_train": ("Release/Train/Data/MainTable.csv", "Release/Train/early.csv"),
    "release_test":  ("Release/Test/Data/MainTable.csv",  "Release/Test/early.csv"),
}

# DEPOIS — vazio; qualquer chamada load_main_table('all', ...) levanta ValueError imediatamente
_SPLITS = {}
```
A função `load_main_table` permanece (pode ser útil futuramente), mas falha cedo com mensagem
clara em vez de `FileNotFoundError` difícil de rastrear.

### 1b — Atualizar docstring do módulo (linhas 1–10)

```python
# ANTES
"""
data_loader.py — carregamento do dataset CSEDM (ProgSnap2 v6)

Splits disponíveis:
  - All/  : semestre Fall-2019 (set–dez 2019), 506 estudantes; usar para EDA completa
  - Release/ : semestre Spring-2019 (fev–mai 2019), 329 estudantes; ...
"""

# DEPOIS
"""
data_loader.py — carregamento do dataset CSEDM (ProgSnap2 v6)

Dataset principal: data/CSEDM/MainTable.csv (Spring 2019, protocolo Shi et al. 2022)
  - 410 alunos após filtro min_attempts >= 3 (Run.Program globais); 23.68% corretos
  - Split 80/20: train_test_split(students, test_size=0.2, random_state=1)
  - Usar load_spring2019_split() para carregamento com split reproduzível.
"""
```

### 1c — Remover nota stale do docstring de `load_main_table`

Linha ~44: remover "Release/Train correto-rate ≈ 23.70% (Shi et al. (2022) reporta 23.68%...)" —
essa nota pertence ao docstring de `load_spring2019_split`.

### 1d — Adicionar `load_spring2019_split` ao final do arquivo

```python
def load_spring2019_split(
    data_dir: Path | str,
    test_size: float = 0.2,
    random_state: int = 1,
    min_attempts: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega MainTable.csv, filtra min_attempts e split 80/20 por SubjectID.

    Replica o protocolo de Shi et al. (2022): 410 alunos, split random_state=1.
    min_attempts é contado em Run.Program globais (todos os assignments somados).

    Retorna o DataFrame completo (todos os EventTypes) — usar filter_for_bkt_dkt()
    ou filter_for_code_dkt() nas células subsequentes.

    Taxa de corretos no train split ≈ 23.68% (tolerância ±0.5pp). O assert no notebook
    compara contra a taxa global dos 410 alunos — não é a taxa train-específica.

    Parameters
    ----------
    data_dir : Path | str
        data/CSEDM/ após reorganização — contém MainTable.csv diretamente.
    """
    from sklearn.model_selection import train_test_split as _split

    data_dir = Path(data_dir)
    df = pd.read_csv(data_dir / "MainTable.csv")
    df["ServerTimestamp"] = pd.to_datetime(df["ServerTimestamp"], utc=True, errors="coerce")
    if "AssignmentID" in df.columns:
        df["AssignmentID"] = pd.to_numeric(df["AssignmentID"], errors="coerce").astype("Int64")
    if "ProblemID" in df.columns:
        df["ProblemID"] = pd.to_numeric(df["ProblemID"], errors="coerce").astype("Int64")

    run = df[df["EventType"] == "Run.Program"]
    attempts = run.groupby("SubjectID").size()
    eligible = attempts[attempts >= min_attempts].index
    df_filtered = df[df["SubjectID"].isin(eligible)]

    students = df_filtered["SubjectID"].unique()
    train_s, test_s = _split(students, test_size=test_size, random_state=random_state)

    train_df = df_filtered[df_filtered["SubjectID"].isin(train_s)].reset_index(drop=True)
    test_df  = df_filtered[df_filtered["SubjectID"].isin(test_s)].reset_index(drop=True)
    return train_df, test_df
```

### 1e — `src/models/bkt.py` — atualizar docstrings (sem alterações de código)

3 locais que referenciam "Release/Train":
- Linha 3: `# Treinado em Release/Train` → `# Treinado no Spring 2019 train split (80/20)`
- Linha 43: troca "Release/Train" → "Spring 2019 train split"
- Linhas 103–104: troca "Release/Train" / "Release/Test" → "train split" / "test split"

---

## Passo 2 — `notebooks/02_preprocessing.ipynb` — seção de carregamento

### Escopo das mudanças (expandido em relação ao rascunho anterior)

O plano original cobria apenas `release_train`/`release_test`. São necessárias também:
- Substituir `all_main = load_main_table('all', DATA_ROOT)` — `All/` será deletado
- Remover as 4 chamadas `load_labels()` — `Release/` será deletado
- Renomear variáveis `release_train`/`release_test` → `train_df`/`test_df` nas células subsequentes
- Atualizar células de markdown com "246 estudantes", "83 estudantes", "Release/Train"

### Célula de carregamento de splits — substituição completa

```python
# ANTES
all_main        = load_main_table('all',           DATA_ROOT)
release_train   = load_main_table('release_train', DATA_ROOT)
release_test    = load_main_table('release_test',  DATA_ROOT)
early_train = load_labels('release_train', DATA_ROOT, which='early')
late_train  = load_labels('release_train', DATA_ROOT, which='late')
early_test  = load_labels('release_test',  DATA_ROOT, which='early')
late_test   = load_labels('release_test',  DATA_ROOT, which='late')

# DEPOIS
from data_loader import load_spring2019_split
train_df, test_df = load_spring2019_split(DATA_ROOT, test_size=0.2, random_state=1, min_attempts=3)
# load_labels() removido: Release/ eliminado; labels do challenge em data/early.csv se necessário
```

### Célula de validação (nova, inserir imediatamente após o split)

```python
train_run = train_df[train_df['EventType']=='Run.Program']
print(f"Train: {train_df['SubjectID'].nunique()} alunos | corretos: {(train_run['Score']==1.0).mean()*100:.2f}%")
print(f"Test:  {test_df['SubjectID'].nunique()} alunos")
print(f"Assignments test: {sorted(test_df['AssignmentID'].dropna().unique().tolist())}")
assert train_df['SubjectID'].nunique() == 328
assert test_df['SubjectID'].nunique() == 82
assert set(test_df['AssignmentID'].dropna().unique()) == {439, 487, 492, 494, 502}
train_rate = (train_run['Score']==1.0).mean()
assert abs(train_rate - 0.2368) < 0.005, f"Taxa inesperada: {train_rate:.4f}"
```

### Células subsequentes — renomear variáveis

`filter_for_bkt_dkt(release_train)` → `filter_for_bkt_dkt(train_df)`
`filter_for_bkt_dkt(release_test)` → `filter_for_bkt_dkt(test_df)`
`filter_for_code_dkt(release_train)` → `filter_for_code_dkt(train_df)`
`filter_for_code_dkt(release_test)` → `filter_for_code_dkt(test_df)`

Todas as demais células (`build_sequences`, `truncate_sequences`, serialização pkl) permanecem
inalteradas em lógica — apenas nomes de variáveis.

---

## Passo 3 — `notebooks/03b_kc_generation.ipynb` — path do CodeStates + re-execução

### Célula de setup — única alteração de path

```python
# ANTES
CODE_STATES_PATH = DATA_ROOT / "Release" / "Train" / "Data" / "CodeStates" / "CodeStates.csv"

# DEPOIS (após reorganização do diretório)
CODE_STATES_PATH = DATA_ROOT / "CodeStates" / "CodeStates.csv"
# 69.627 registros — superset do Release/Train (46.825)
```

### Docstring de `load_correct_samples`

```
# ANTES: "Carrega submissões corretas do Release/Train com código Java associado."
# DEPOIS: "Carrega submissões corretas do Spring 2019 train split com código Java associado."
```

### Assert de cobertura CodeStates (inserir após o join com CodeStates.csv)

```python
# Cobertura de CodeStates — nenhum CodeStateID das sequências pode estar ausente
cs_ids_in_codestates = set(code_states['CodeStateID'].astype(str))
sequences_code_state_ids = {
    str(e['CodeStateID'])
    for seqs in artifact['train'].values()
    for seq in seqs
    for _, e in seq['events'].iterrows()
    if pd.notna(e.get('CodeStateID'))
}
missing = sequences_code_state_ids - cs_ids_in_codestates
assert len(missing) == 0, f"{len(missing)} CodeStateIDs das sequências ausentes no novo CodeStates.csv"
```

### Sobre re-execução das Etapas LLM

Os KCs são **fixos por problema** (problem-level), independentes de quais estudantes estão no treino.
A Etapa 2 usa diversity sampling de 5 exemplos corretos **por problema** — com 328 alunos a pool
de exemplos é maior e alguns buckets antes vazios passam a ter amostras. Os exemplos enviados ao
LLM mudam → os KCs gerados podem diferir ligeiramente, mas o protocolo Duan et al. é robusto a
isso. Reexecutar é **necessário** para consistência com o novo split, não apenas precaução.

- **Etapas 1–5 (incluindo Etapas 2+4 com LLM):** Reexecutar. Custo estimado: ~$0.03–0.07 Haiku.
- **Etapa 6 (`label_kc_correctness`):** Ainda não foi executada. Execução futura, com Code-DKT.
  Custo: ~$2–3 com cache ephemeral (26k submissões). Não bloqueia BKT nem DKT baseline.
- **Etapa 7 (validação srcML):** Determinística, sem custo de API.

---

## Passo 4 — `notebooks/04_bkt.ipynb` — correção de path hardcoded + re-execução

**O plano original dizia "sem alterações de código". Isso está errado.**

### Cell 4 — remover path Release/ hardcoded

Cell 4 lê `DATA_ROOT / 'Release' / 'Test' / 'Data' / 'MainTable.csv'` diretamente — esse path
não existirá após o Passo 0. A célula deve ser **removida e substituída** por verificação no pkl:

```python
# ANTES (Cell 4 — lê Release/Test hardcoded, quebrará após Passo 0)
main_test = pd.read_csv(
    DATA_ROOT / 'Release' / 'Test' / 'Data' / 'MainTable.csv',
    usecols=['AssignmentID'],
    dtype={'AssignmentID': 'Int64'},
)
test_aids = sorted(main_test['AssignmentID'].dropna().unique().tolist())
EVAL_AIDS = [aid for aid in ASSIGNMENT_IDS if aid in test_aids]
TRAIN_ONLY_AIDS = [aid for aid in ASSIGNMENT_IDS if aid not in test_aids]

# DEPOIS — verificar diretamente no pkl já carregado (Cell 3)
EVAL_AIDS = [aid for aid in ASSIGNMENT_IDS if len(seqs['test'].get(aid, [])) > 0]
TRAIN_ONLY_AIDS = [aid for aid in ASSIGNMENT_IDS if aid not in EVAL_AIDS]
assert set(EVAL_AIDS) == {439, 487, 492, 494, 502}, \
    f"Esperado todos os 5 assignments no test set; encontrado: {EVAL_AIDS}"
print(f'Assignments com dados de teste: {EVAL_AIDS}')
print(f'Assignments apenas treino: {TRAIN_ONLY_AIDS}')
```

### Cell 3 — assert anti-stale (inserir após carregar o pkl)

```python
# Garantir que o pkl foi regenerado com o novo split (não é o pkl Release/ antigo)
for aid in ASSIGNMENT_IDS:
    n_test = len(seqs['test'].get(aid, []))
    assert n_test > 0, \
        f"A{aid} sem dados de teste — pkl provavelmente stale (Release/). Re-executar 02_preprocessing."
```

### Célula de markdown após Cell 4 e sumário final

Atualizar o "Achado" que dizia "Release/Test cobre apenas A439, A487, A492 — A494 e A502 ausentes"
para refletir que com o Spring 2019 completo todos os 5 assignments têm dados de teste.

Cell 22 (sumário final): a tabela com `n/a (sem teste)` para A494/A502 deve ser substituída pelos
resultados reais após a re-execução.

---

## Passo 5 — `notebooks/01_eda.ipynb` — atualização de paths + re-execução

**O plano original dizia "re-executar". Isso falha na Cell 2 sem atualização prévia de código.**

### Células com paths que serão deletados (atualizar antes de re-executar)

| Cell | Path atual (quebrado após Passo 0) | Substituição |
|---|---|---|
| Cell 2 | `DATA_ROOT / 'All/Data/MainTable.csv'` | `DATA_ROOT / 'MainTable.csv'` |
| Cell 16 | `DATA_ROOT / 'Release/Train/Data/MainTable.csv'` | `train_df` via `load_spring2019_split` |
| Cell 16 | `DATA_ROOT / 'Release/Test/Data/MainTable.csv'` | `test_df` via `load_spring2019_split` |
| Cell 21 | `DATA_ROOT / 'Train/Data/MainTable.csv'` | Remover (era Fall 2019, não existe pós-migração) |
| Cell 21 | `DATA_ROOT / 'Test/Data/MainTable.csv'` | Remover (era Fall 2019, não existe pós-migração) |
| Cell 41 | `DATA_ROOT / 'All/early.csv'` | Remover ou usar `ROOT / 'data' / 'early.csv'` |
| Cell 57 | `DATA_ROOT / 'Release/Train/Data/MainTable.csv'` | `DATA_ROOT / 'MainTable.csv'` |
| Cell 91 | `DATA_ROOT / 'Release/Train/early.csv'` | `ROOT / 'data' / 'early.csv'` |
| Cell 91 | `DATA_ROOT / 'Release/Train/late.csv'` | `ROOT / 'data' / 'late.csv'` |

### Seção "Consistência entre Splits" (Cells 15–21)

Esta seção comparava All/ vs Release/Train vs Release/Test — análise que perde sentido após a
migração. Substituir por uma comparação `train_df` vs `test_df` (328 vs 82 alunos, 5 assignments
em ambos). A estrutura da análise é equivalente; apenas os dados de origem mudam.

### Nota sobre `eda_insights.md`

O harness regenera `eda_insights.md` automaticamente após re-execução. Os valores numéricos
nas células de markdown (246, 83, taxas, clusters, etc.) serão recalculados. As seções que
precisam de recálculo com o novo split (328 alunos):
- Seção 1: imbalance global e por assignment
- Seção 2: distribuição de sequências (mediana, P95, máx)
- Seção 3: clustering de perfis (K-Means)
- Seção 5.1: tabela de risco por assignment

---

## Passo 6 — Documentação

### `CLAUDE.md`

**Seção "Dataset CSEDM — Fatos Críticos", subseção "Splits":**

Remover menção a Release/ como dataset principal. Substituir por:

```
**Dataset primário para modelagem (Shi et al. protocol):**
- Arquivo: `data/CSEDM/MainTable.csv` (Spring 2019, 413 alunos brutos)
- Filtro: `min_attempts >= 3` (Run.Program globais) → 410 alunos (23.68% corretos — match paper)
- Split: `train_test_split(students, test_size=0.2, random_state=1)` → 328 treino + 82 teste
- Todos os 5 assignments disponíveis no test set
- CodeStates: `data/CSEDM/CodeStates/CodeStates.csv`

**Release/ (removido — era CSEDM Data Challenge 2021):**
- Spring 2019, 329 alunos (criteria "completed course"), 75/25 split
- Release/Test tinha apenas A1–A3 por design (A4–A5 eram prediction targets do challenge)
- Não usar para modelagem KT
```

**Critérios de Conclusão:**

Atualizar `~74% para A1 (±2%)` para:
`próximo a 74% para A1 (±3%), comparável com Table 1 de Shi et al.; data/CSEDM/ (410 alunos, 80/20, random_state=1)`

**Nova seção após "Stack" — Repositório Modelo:**

```markdown
## Repositório Modelo (Code-DKT)

Referência de implementação para o Code-DKT e DKT (Shi et al., 2022):
- **Path:** `/home/leokuntz/Documents/repositories/experiments/Code-DKT/src/`
- `c2vRNNModel.py` — arquitetura LSTM + mecanismo de atenção code2vec
- `run.py` — protocolo de treinamento (10-fold CV, Adam lr=0.0005)
- `config.py` — hiperparâmetros de referência (hidden=128, length=50, questions=10)
- `path_extractor.py` — extração de caminhos AST (adaptar para srcML neste projeto)
- **Atenção:** usa seed=0 e Python 2/3 misto — adaptar para SEED=42 e Python 3.10+
```

### `docs/ajustes_split.md`

Reescrever para refletir que:
- `data/CSEDM/MainTable.csv` **é** o dataset do paper
- Comparação direta com Table 1 e Table 2 **passa a ser válida**
- Release/ foi removido — era CSEDM Data Challenge (propósito diferente)

### `.harness/progress.md`

Adicionar ao topo:
```
## 2026-05-15 — MIGRAÇÃO: Release/ → Spring 2019 Full (Shi et al. protocol)

data/CSEDM/ agora contém o Spring 2019 completo (era data/Data/).
410 alunos com min_attempts>=3, 23.68% corretos. Split 80/20 random_state=1: 328+82 alunos.
Todos os 5 assignments no test set. Comparação direta com Table 1/Table 2 do paper agora válida.
Tarefas reexecutadas: preprocessing (02), kc_generation (03b Etapas 1–5), bkt (04), eda (01).
```

Corrigir linha ~287 (erro factual sobre split do paper):
```
# ANTES
"comportamento esperado — o split de avaliação do paper Shi et al. (2022) cobre apenas
os primeiros 3 assignments"

# DEPOIS
"Irrelevante pós-migração: o test set agora contém todos os 5 assignments (A439–A502)
conforme protocolo 80/20 de Shi et al. (2022). A ausência anterior de A4–A5 era design
do CSEDM Data Challenge, não limitação do paper."
```

### `.harness/runner.py` — instrução de voz e repositório modelo

Adicionar ao bloco de instruções do Generator em `build_prompt()`, logo após as regras de template:

```
## Voz e perspectiva

Escreva os textos analíticos (Contexto, Hipótese, Achado, Implicação) como um estudante
de Engenharia de Computação documentando sua própria pesquisa de TCC:
- Conecte achados com conceitos de CS relevantes (complexidade do EM, estrutura de grafos
  AST, convergência do LSTM, tradeoff bias-variância, etc.).
- Explique por que uma descoberta importa para as decisões de implementação do pipeline,
  não apenas descreva o número.
- Use vocabulário técnico preciso (sem jargão de negócio); o leitor é um colega de CS.
- Quando um achado valida ou contradiz uma hipótese do paper, explicite a conexão.

## Repositório modelo

Para dúvidas de arquitetura ou geração de código relacionado ao Code-DKT e DKT,
consultar o repositório de referência:
  /home/leokuntz/Documents/repositories/experiments/Code-DKT/src/

Arquivos-chave:
- c2vRNNModel.py  — arquitetura LSTM + mecanismo de atenção code2vec
- run.py          — protocolo de treinamento (10-fold CV, Adam lr=0.0005)
- config.py       — hiperparâmetros de referência (hidden=128, length=50, questions=10)
- path_extractor.py — extração de caminhos AST (adaptar para srcML neste projeto)

Nota: o paper usa seed=0 e código Python 2/3 misto; adaptar para SEED=42 e Python 3.10+.
```

### `.harness/HARNESS_PLAN.md` — nota de voz no template didático

Adicionar à seção "Didactic Template":

```
**Voz:** estudante de Engenharia de Computação documentando o próprio TCC.
Conectar achados com conceitos de CS/ML; explicar implicações de implementação;
vocabulário técnico preciso; leitor é colega de graduação em CS.
```

---

## Ordem de execução

| # | Ação | Tipo | Pré-requisito | Custo |
|---|---|---|---|---|
| 0a | Verificar refs a CodeWorkout; diff F19 | Shell | — | — |
| 0b | Deletar pkl stale | Shell | — | — |
| 0c | Reorganizar `data/` (mover/remover) | Filesystem | 0a, 0b | — |
| 1a | `src/data_loader.py`: limpar `_SPLITS` + atualizar docstrings + add `load_spring2019_split` | Código | — | — |
| 1b | `src/models/bkt.py`: atualizar docstrings | Código | — | — |
| 1c | `.harness/runner.py` + `HARNESS_PLAN.md`: voz CS + repo modelo | Harness | — | — |
| 1d | `CLAUDE.md`: seção Splits + seção Repositório Modelo | Docs | — | — |
| 2 | `02_preprocessing.ipynb`: atualizar código + re-executar | Notebook | 0c, 1a | — |
| 3 | `03b_kc_generation.ipynb`: atualizar path + re-executar Etapas 1–5 | Notebook | 2 | ~$0.05 Haiku |
| 4 | `04_bkt.ipynb`: corrigir Cell 4 + anti-stale assert + re-executar | Notebook | 2 | — |
| 5 | `01_eda.ipynb`: atualizar 9 células de path + re-executar | Notebook | 0c | — |
| 6 | `docs/ajustes_split.md`, `.harness/progress.md` | Docs | 4 | — |

**Dependências cruzadas:**
- Passos 1a–1d podem ser executados em qualquer ordem entre si (sem dependência)
- Passo 5 (01_eda) depende apenas de 0c — pode ser executado em paralelo com Passos 2–4
- Passo 3 (KC generation) depende do pkl gerado no Passo 2

**Nota sobre Etapa 6 do KC (`label_kc_correctness`):** pendente, execução junto com Code-DKT (06).
Custo estimado: ~$2–3 (com cache ephemeral).

---

## Verificação

```python
# Após Passo 2 (02_preprocessing):
assert train_df['SubjectID'].nunique() == 328
assert test_df['SubjectID'].nunique() == 82
assert set(test_df['AssignmentID'].dropna().unique()) == {439, 487, 492, 494, 502}
train_rate = (train_df[train_df['EventType']=='Run.Program']['Score']==1.0).mean()
assert abs(train_rate - 0.2368) < 0.005, f"Taxa inesperada: {train_rate:.4f}"
# Nota: 0.2368 é a taxa global dos 410 alunos; tolerância de 0.5pp cobre variação do split
```

```python
# Após Passo 2, no início do Passo 4 (04_bkt — verificação anti-stale):
for aid in ASSIGNMENT_IDS:
    n_test = len(seqs['test'].get(aid, []))
    assert n_test > 0, f"A{aid} sem dados de teste — pkl provavelmente stale (Release/). Re-executar 02."
```

```python
# Após Passo 3 (03b_kc_generation — cobertura CodeStates):
missing_cs = sequences_code_state_ids - cs_ids_in_codestates
assert len(missing_cs) == 0, f"{len(missing_cs)} CodeStateIDs ausentes no novo CodeStates.csv"
```

Após Passo 4 (BKT):
- AUC reportado para **todos os 5 assignments** (A439, A487, A492, A494, A502) — se A494/A502
  ainda retornarem `n/a`, o pkl é stale; re-executar Passo 2
- First-attempt AUC A439 deve estar próximo de ~50% (Table 2 do paper — BKT baseline)
- Discrepâncias acima de ±5% — investigar antes de prosseguir para DKT
