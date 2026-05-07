# TCC 1 — EDM & Knowledge Tracing sobre CSEDM/ProgSnap2

Trabalho de Conclusão de Curso (fase 1): aplicar Educational Data Mining ao dataset CSEDM,
comparar três modelos de Knowledge Tracing (BKT, DKT, Code-DKT com srcML) e justificar
a escolha do modelo base para o TCC 2.

**Metodologia:** EDM Process de 4 fases — Problem Definition → Data Preparation →
Modelling & Evaluation → Deployment (diferido ao TCC 2).

---

## Dataset

**CSEDM / ProgSnap2 v6** — Java introdutório, universidade americana, Spring 2019.

| Split | Estudantes | Eventos | Corretos |
|---|---|---|---|
| `Release/Train` | 246 | ~134k | 23,70% |
| `Release/Test` | 83 | ~45k | — |

> Usar sempre `Release/` para comparação reproduzível com Shi et al. (2022).
> Os splits `All/`, `Train/`, `Test/` são de um semestre diferente (Fall 2019, 506 estudantes)
> e não se sobrepõem com `Release/`.

**5 assignments Java introdutório:** A439, A487, A492, A494, A502 — ~10 problemas cada.

---

## Pipeline de Notebooks

| Notebook | Descrição | Status |
|---|---|---|
| `00_problem_definition.ipynb` | Definição do problema, KCs, métricas | Completo |
| `01_eda.ipynb` | EDA completa (seções 1–8) | Completo |
| `02_preprocessing.ipynb` | Filtragem, sequências KT, artefatos `.pkl` | Completo |
| `03b_kc_generation.ipynb` | Geração de KCs via LLM (KCGen-KT) | Em andamento |
| `03_code_features.ipynb` | Extração de codepaths via srcML | Planejado |
| `04_bkt.ipynb` | BKT baseline (pyBKT) | Planejado |
| `05_dkt.ipynb` | DKT — LSTM (PyTorch) | Planejado |
| `06_code_dkt.ipynb` | Code-DKT com srcML | Planejado |
| `07_comparison.ipynb` | Comparação 3×2: modelo × definição de KC | Planejado |

---

## Setup

```bash
# Dependências Python
pip install torch pyBKT scikit-learn pandas numpy matplotlib seaborn \
            anthropic sentence-transformers scipy

# srcML (CLI — necessário para Code-DKT e AST signatures)
# Ubuntu/Debian: sudo apt-get install srcml
# Ou: https://www.srcml.org/#download

# Verificar ambiente
python3 -c "import torch, pyBKT, sklearn; print('OK')"
srcml --version
```

```bash
# Executar qualquer notebook do zero
jupyter nbconvert --to notebook --execute notebooks/02_preprocessing.ipynb \
    --output notebooks/02_preprocessing.ipynb \
    --ExecutePreprocessor.timeout=600
```

> **Dados:** `data/CSEDM/` (gitignored). Baixar separadamente e manter a estrutura
> `data/CSEDM/Release/Train/` e `data/CSEDM/Release/Test/`.

---

## Interpretando os KCs gerados (`results/`)

O notebook `03b_kc_generation.ipynb` implementa o pipeline KCGen-KT (Duan et al., 2025):
LLM analisa submissões corretas e infere os conceitos necessários para resolver cada problema.
Os resultados ficam em `results/` e têm quatro camadas:

### 1. KCs brutos — `kc_raw_{assignment}.json`

Um objeto por problema. O LLM inferiu a descrição do problema a partir do código e gerou
os KCs necessários para resolvê-lo.

```json
{
  "1": {
    "problem_description": "Given two integers, return 20 if their sum is between 10 and 19, otherwise return the sum itself.",
    "kcs": [
      {"name": "Compound boolean condition with AND operator", "reasoning": "..."},
      {"name": "Numeric comparison for range validation", "reasoning": "..."}
    ]
  }
}
```

### 2. KCs canônicos — `kc_descriptions_{assignment}.json`

Os KCs brutos (~5 por problema) são agregados e clusterizados por similaridade semântica
(Sentence-BERT + HAC). Cada cluster recebe um rótulo canônico final.

| Assignment | KCs canônicos | Exemplos |
|---|---|---|
| A439 | 15 | Range validation with logical operators · Compound boolean expressions |
| A487 | 15 | String indexing and substring extraction · Helper methods for code organization |
| A492 | 15 | String building with StringBuilder · String comparison methods |
| A494 | 15 | Loop bounds and counter control · Accumulator pattern for aggregating values |
| A502 | 12 | Modulo operator applications · String conversion of integers |

### 3. Q-matrix — `qmatrix_{assignment}.csv`

Matriz binária `ProblemID × KC`. Um `1` indica que aquele problema requer aquele KC.

```
ProblemID  kc_0  kc_1  kc_2  ...  kc_14
1             1     0     0  ...      0
3             1     0     0  ...      0
5             0     0     0  ...      0
```

**Estatísticas (A439):** 10 problemas × 15 KCs · densidade 32% · média de 4,8 KCs/problema.

Para carregar e inspecionar:

```python
import pandas as pd, json

qm = pd.read_csv("results/qmatrix_A439.csv", index_col=0)
print(qm)                          # matriz completa
print(qm.sum(axis=1))              # KCs por problema
print(qm.sum(axis=0).sort_values()) # problemas que exigem cada KC

with open("results/kc_descriptions_A439.json") as f:
    kcs = {kc["kc_id"]: kc["name"] for kc in json.load(f)}

qm.rename(columns=kcs)             # substituir kc_0..N por nomes legíveis
```

### 4. Artefatos intermediários

| Arquivo | Conteúdo |
|---|---|
| `kc_clusters_{aid}.json` | Mapeamento `kc_name → cluster_id` (pré-rotulagem) |
| `kc_correctness_{aid}.json` | Label KC-level por submissão incorreta (Task 6, ~$39 Haiku) |
| `ast_signatures_{aid}.json` | Frequência de nós srcML por problema (validação post-hoc) |

> **Nota metodológica:** o LLM recebe código bruto, não AST. Enviar AST ao LLM piora a
> qualidade dos KCs gerados (ablação de Duan et al. 2025, Table 4: AUC 0,784 vs 0,812).
> As assinaturas AST são usadas apenas por nós para verificar post-hoc se os KCs gerados
> correspondem às estruturas de código que realmente aparecem nas soluções corretas.

---

## Artefatos de Pré-processamento

| Arquivo | Conteúdo |
|---|---|
| `sequences_bkt_dkt.pkl` | Sequências KT para BKT/DKT (apenas `Run.Program`, `correct = Score == 1.0`) |
| `sequences_code_dkt.pkl` | Sequências para Code-DKT (inclui `Compile.Error` com `correct = 0`) |

```python
import pickle

with open("results/sequences_bkt_dkt.pkl", "rb") as f:
    data = pickle.load(f)

# data["train"]["A439"] → lista de sequências do assignment A439
# cada sequência: {"subject_id", "assignment_id", "events": DataFrame}
# eventos: colunas correct, is_first_attempt, ProblemID, CodeStateID, ...
```

---

## Métricas e Protocolo Experimental

- **First-attempt AUC** (primária) — predição na primeira tentativa por problema por
  estudante; menos inflada por autocorrelação; métrica principal de Shi et al. (2022)
- **All-attempts AUC** (secundária) — todas as tentativas; comparável com literatura DKT
- Um modelo por assignment, KC = ProblemID (baseline) e KC = gerado por LLM
- Reproduzibilidade: `SEED = 42` em todos os notebooks; `Release/Train` e `Release/Test`
- Benchmark de referência: Code-DKT AUC ~74,3% no A1 (Shi et al., 2022, Table 2)

---

## Referências

- **Shi et al. (2022)** — Code-DKT: code2vec + atenção sobre AST paths; KC=ProblemID; benchmark CSEDM
- **Pankiewicz, Shi & Baker (2025)** — srcML-DKT: substitui javalang por srcML; inclui Compile.Error
- **Duan et al. (2025)** — KCGen-KT: geração automática de KCs por LLM para programação
- **Piech et al. (2015)** — DKT original (LSTM)
- **Corbett & Anderson (1994)** — BKT
