# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

TCC 1 de graduação: aplicar Educational Data Mining (EDM) ao dataset CSEDM (ProgSnap2 v6), comparar três modelos de Knowledge Tracing (BKT, DKT, Code-DKT) e justificar a escolha do modelo base para o TCC 2.

Metodologia: EDM Process de 4 fases — Problem Definition → Data Preparation → Modelling & Evaluation → Deployment (diferido ao TCC 2, não implementar aqui).

## Repositório Modelo (Code-DKT)

Referência de implementação para o Code-DKT e DKT (Shi et al., 2022):
- **Path:** `/home/leokuntz/Documents/repositories/experiments/Code-DKT/src/`
- `c2vRNNModel.py` — arquitetura LSTM + mecanismo de atenção code2vec
- `run.py` — protocolo de treinamento (10-fold CV, Adam lr=0.0005)
- `config.py` — hiperparâmetros de referência (hidden=128, length=50, questions=10)
- `path_extractor.py` — extração de caminhos AST (adaptar para srcML neste projeto)
- **Atenção:** usa seed=0 e Python 2/3 misto — adaptar para SEED=42 e Python 3.10+

## Stack

Python 3.10+, Jupyter Notebooks. Dependências principais:
- `pandas`, `numpy` — manipulação de dados
- `srcml` (CLI, sistema) — parsing de ASTs Java; substitui `javalang` por suportar código não-compilável
- `torch` (PyTorch) — modelos DKT e Code-DKT
- `pyBKT` — modelo BKT
- `scikit-learn` — AUC, cross-validation
- `matplotlib`, `seaborn` — visualizações

## Common Commands

```bash
# Executar Jupyter
jupyter notebook notebooks/

# Executar notebook sem interface (para CI/reprodução)
jupyter nbconvert --to notebook --execute notebooks/01_eda.ipynb --output notebooks/01_eda_executed.ipynb

# Verificar ambiente Python
python -c "import torch, pyBKT, sklearn; print('OK')"

# Verificar srcML (deve retornar versão)
srcml --version
```

## Estrutura do Repositório

```
tcc.edm.kt/
├── data/CSEDM/          # gitignored — dataset local
├── docs/                # papers de referência
├── notebooks/           # pipeline sequencial (01→07)
├── src/                 # módulos Python reutilizáveis
│   ├── data_loader.py
│   ├── code_features.py
│   ├── evaluation.py
│   └── models/
│       ├── bkt.py
│       ├── dkt.py
│       └── code_dkt.py
└── results/             # gitignored (*.csv, *.pkl, *.pt)
```

## Pipeline de Notebooks

| Notebook | Fase | Status |
|---|---|---|
| `01_eda.ipynb` | Data Preparation — EDA | Em andamento |
| `02_preprocessing.ipynb` | Data Preparation — pré-processamento | Planejado |
| `03_code_features.ipynb` | Data Preparation — features AST | Planejado |
| `04_bkt.ipynb` | Modelling — BKT baseline | Planejado |
| `05_dkt.ipynb` | Modelling — DKT (LSTM) | Planejado |
| `06_code_dkt.ipynb` | Modelling — Code-DKT | Planejado |
| `07_comparison.ipynb` | Evaluation — comparação final | Planejado |

## Dataset CSEDM — Fatos Críticos

**Splits:**

**Dataset primário para modelagem (Shi et al. protocol):**
- Arquivo: `data/CSEDM/MainTable.csv` (Spring 2019, 413 alunos brutos)
- Filtro: `min_attempts >= 3` (Run.Program globais) → 410 alunos (23.68% corretos — match paper)
- Split: `train_test_split(students, test_size=0.2, random_state=1)` → 328 treino + 82 teste
- Todos os 5 assignments disponíveis no test set (A439, A487, A492, A494, A502)
- CodeStates: `data/CSEDM/CodeStates/CodeStates.csv` (69.627 registros)

**Release/ (removido — era CSEDM Data Challenge 2021):**
- Spring 2019, 329 alunos (critério "completed course"), split 75/25
- Release/Test tinha apenas A1–A3 por design (A4–A5 eram prediction targets do challenge)
- Não usar para modelagem KT

**EventType:**
- Não existe `EventType = Submit` neste dataset
- Submissões são `Run.Program` com `Score` não-nulo (100% dos Run.Program têm Score)
- `Compile.Error`: 109.020 eventos (30.27% do total) — código não-compilável com CodeStateID disponível
- Para Code-DKT (srcML): incluir `Compile.Error` na sequência KT como `correct=0`; extrair features via srcML
- Para BKT e DKT: usar apenas `Run.Program`, label `correct = (Score == 1.0)`

**Score:**
- Não é puramente binário: ~37% das execuções têm Score parcial (0 < Score < 1)
- Para KT binário, usar threshold `Score == 1.0` como "correto"
- `Score` fora de [0, 1]: 0 registros (dataset limpo nessa dimensão)

**Duplicatas:**
- 236.024 registros com mesmo (SubjectID, ProblemID, ServerTimestamp) — comportamento esperado: cada `Run.Program` gera um evento filho `Compile` com o mesmo timestamp

**Cobertura de CodeStateID:** 100% dos eventos têm CodeStateID (sem missing)

## Definições de Modelagem

- **Knowledge Component (KC):** `ProblemID` — 9–10 problemas por assignment; um modelo treinado por assignment (mesmo protocolo de Shi et al., 2022)
- **Task de KT:** dado histórico `(ProblemID, acerto/erro)` até `t`, prever resultado em `t+1`
- **Labels-alvo:** `early.csv` e `late.csv` — coluna `Label` (binária)
- **Métricas:**
  - **First-attempt AUC** (primária) — predição na primeira tentativa de cada problema por estudante; métrica principal do paper Shi et al. (2022); menos inflada por autocorrelação temporal
  - **All-attempts AUC** (secundária) — todas as tentativas; comparável com literatura DKT (Piech et al., 2015); mais estável estatisticamente
- **Sequências:** truncar em 50 tentativas (últimas 50, conforme Shi et al., 2022)
- **Seed fixo obrigatório** em todos os notebooks (reprodutibilidade)

## Code-DKT — Arquitetura (referência para implementação)

- Embeddings de caminhos AST (code2vec, tamanho 300): `pr = (nó_início, caminho_textual, nó_fim)`
- Mecanismo de atenção: `α = SoftMax(E · Wa)`, vetor de código `z = W0(Σ αᵢ eᵢ)`
- Concatenar `z` com vetor de acerto/erro a cada passo LSTM
- Input DKT base: one-hot `(ProblemID, correctness)` — dimensão `2 × n_problemas_por_assignment` (tipicamente `2 × 10`)
- Otimizador: Adam (lr=0.0005), Binary Cross-Entropy
- Hyperparameter tuning: 100 random samples, 10-fold cross-validation

### Decisão de implementação: srcML em vez de javalang

- **Extrator de AST:** srcML (XML-based, CLI) em vez de javalang
- **Motivo:** javalang exige código sintaticamente válido e falha silenciosamente em `Compile.Error`; srcML parseia Java compilável e não-compilável, preservando estrutura parcial
- **Impacto na sequência:** `Compile.Error` events entram na sequência KT com `correct=0` e features srcML; `Run.Program` com `Score == 1.0` → `correct=1`
- **Arquitetura inalterada:** mesma estrutura LSTM + atenção do Code-DKT original (Shi et al., 2022)
- **Referência:** Pankiewicz, Shi & Baker (2025). *srcML-DKT*, EDM 2025 — extensão direta do Code-DKT pelo mesmo grupo

## Critérios de Conclusão do TCC 1

1. First-attempt AUC do Code-DKT próximo a 74% para A1 (±3%), comparável com Table 1 de Shi et al.; data/CSEDM/ (410 alunos, 80/20, random_state=1)
2. Tabela comparativa BKT vs DKT vs Code-DKT por assignment, reportando first-attempt AUC e all-attempts AUC
3. Teste de significância Wilcoxon signed-rank entre modelos
4. Todos os notebooks executáveis do zero com seed fixo
