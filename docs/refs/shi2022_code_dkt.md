---
source: docs/Code-DKT.pdf
cite_as: Shi et al. (2022)
title: "Code-DKT: A Code-based Knowledge Tracing Model for Programming Tasks"
venue: Proceedings of the 15th International Conference on Educational Data Mining (EDM 2022), pp. 50–61, Durham, United Kingdom, July 2022
doi: https://doi.org/10.5281/zenodo.6853105
repo: https://github.com/YangAzure/Code-DKT
---

## Resumo de uma linha
Propõe Code-DKT: extensão do DKT que incorpora features de código via code2vec e atenção, superando DKT em +3.07–4.00pp AUC em todos os 5 assignments do CSEDM Spring 2019.

## Fatos críticos para este projeto

**Dataset:**
- CSEDM — introductory Java programming, large US university, **Spring 2019** (fev–mai 2019)
- **410 students**, 50 problems, **5 assignments** (A1–A5)
- Armazenado em formato ProgSnap2 (Price et al., 2020)
- **23.68% de tentativas corretas** ← benchmark de reprodutibilidade
- Média de 6.1 tentativas por problema
- `correct = 1` quando todos os testes passam (Score == 1.0); `correct = 0` caso contrário

**Definições de modelagem:**
- **KC = ProblemID** (footnote 1: "We use problemIDs for KCs in this work")
  - Na prática, com 5 assignments = 5 grupos de problemas — equivalente a usar AssignmentID como KC de alto nível
- Input por tentativa no tempo `t`: `(q_t, a_t, c_t)` = problem ID, correctness, código submetido
- DKT base usa apenas `(q_t, a_t)` — Code-DKT adiciona `c_t`
- **Sequências truncadas nas últimas 50 tentativas** (descarta submissões mais antigas quando aluno tem >50)

**Configuração experimental:**
- Split: 4:1 treino/teste **por assignment** (modelo independente por assignment, sem cross-assignment)
- 1/4 do treino reservado para hyperparameter tuning e validação
- **10 repetições** por configuração (controla variabilidade de inicialização aleatória)
- Métrica primária: **AUC** (dataset desbalanceado ~23.68% corretos; AUC adequado vs acurácia)

## Resultados quantitativos

### Table 1 — AUC Overall em todos os assignments
| Modelo | A1 | A2 | A3 | A4 | A5 |
|--------|----|----|----|----|-----|
| DKT | 71.24% | 73.09% | 76.84% | 69.16% | 75.14% |
| **Code-DKT** | **74.31%** | **76.56%** | **80.40%** | **72.75%** | **79.14%** |

Code-DKT supera DKT em **+3.07pp a +4.00pp AUC** em todos os 5 assignments.

### Table 2 — A1: AUC Overall e First Attempts (com desvio padrão de 10 runs)
| Modelo | Overall AUC (STD) | First Attempts AUC (STD) |
|--------|-------------------|--------------------------|
| **Code-DKT** | **74.31% (0.90%)** | **75.74% (0.69%)** |
| DKT-TFIDF | 69.94% (0.88%) | 72.77% (0.79%) |
| DKT-Expert | 69.52% (0.68%) | 69.53% (0.72%) |
| DKT | 71.24% (2.54%) | 72.26% (3.69%) |
| BKT | 63.78% (4.68%) | 50.22% (2.86%) |

- Code-DKT tem STD menor que DKT (mais estável com código que sem)
- DKT-TFIDF e DKT-Expert (features simples de código) **pioram** o DKT — requer arquitetura Code-DKT
- BKT tem AUC muito baixo para first attempts (50.22% ≈ chance)

### Table 4 — Ablation Study em A1 (Overall AUC)
| Configuração | AUC |
|-------------|-----|
| Code-DKT Final | **74.31%** |
| Correctness: Attention Only (sem correctness no trace LSTM) | 73.81% |
| Correctness: Trace Only (sem correctness no vetor atenção) | 73.84% |
| Model: RNN (em vez de LSTM) | 73.63% |
| Embedding: Static (code2vec pré-treinado, fixo) | 68.74% |

LSTM > RNN; embedding aprendido > estático; correctness em ambos os pontos é ligeiramente melhor.

## Arquitetura — detalhes completos de implementação

**Representação de código (code2vec):**
- Extrai paths folha-a-folha da AST Java: `p_r = (s_r, o_r, q_r)` = (nó início, path textual, nó fim)
- R paths amostrados aleatoriamente de `c_t` (range {30, 50, 100, 300} no tuning → selecionado 50 top)
- Cada path embedado: `e_r = [e_{s,r}; e_{o,r}; e_{q,r}; x_t]` — inclui correctness `x_t`

**Score-Attended Path Selection (atenção):**
- Embedding matrix E = {e_0, e_1, …, e_R}
- Pesos: `α = SoftMax(E · W_a)` — escalar por path
- Vetor de código: `z = W_0(Σ αᵢ eᵢ)`

**LSTM:**
- Input: `[z_t; x_t]` — código + correctness concatenados
- `h_t = tanh(W_{xh} · x_t + W_{hh} · h_{t-1})`
- `y_t = σ(W_{hy} · h_t)`
- LSTM rende mais que RNN (ver Table 4)

**Hiperparâmetros selecionados (100 configurações testadas, val set):**
| Hiperparâmetro | Valor selecionado | Range testado |
|----------------|-------------------|---------------|
| Embedding size | **300** | {50, 100, 150, 300, 350} |
| Learning rate | **0.0005** | {0.00005, 0.0005, 0.005, 0.01} |
| Epochs | **40** | {20, 40, 100} |
| Sequence length | **50** (últimas 50) | fixo |
| Optimizer | Adam | — |
| Loss | Binary Cross-Entropy | — |
| Implementação | PyTorch | — |
| BKT | pyBKT | — |

## Limitações relevantes (motivam srcML-DKT)
- Requer código **parsável** — submissões com erros de compilação descartadas (não entram na sequência)
- Dataset pequeno (410 alunos) — deep models podem ser sub-ótimos
- Modelo treinado independentemente por assignment — sem transferência cross-assignment
- Best baseline ~73%, Code-DKT ~74.3% — "considerable room for improvement"

## Análise qualitativa (Section 5.2)
- Code features mais úteis para problemas que **compartilham estruturas de código** com outros (loops, condicionais)
- Menos úteis para problemas com conceitos únicos (ex.: `Math.abs()`)
- Útil para first attempts: Code-DKT identifica padrões de código de problemas anteriores para prever novo problema
- DKT recall em A1 = 31.4%, precisão = 46.5% — falha em identificar 2/3 das tentativas incorretas

## Citação BibTeX
```
@inproceedings{shi2022codedkt,
  author    = {Yang Shi and Min Chi and Tiffany Barnes and Thomas W. Price},
  title     = {{Code-DKT}: A Code-based Knowledge Tracing Model for Programming Tasks},
  booktitle = {Proceedings of the 15th International Conference on Educational Data Mining},
  pages     = {50--61},
  year      = {2022},
  address   = {Durham, United Kingdom},
  doi       = {10.5281/zenodo.6853105}
}
```
