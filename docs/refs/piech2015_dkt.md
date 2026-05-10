---
source: docs/deepKnowledgeTracing.pdf
cite_as: Piech et al. (2015)
title: "Deep Knowledge Tracing"
venue: Advances in Neural Information Processing Systems 28 (NeurIPS 2015), MIT Press
repo: https://github.com/chrispiech/DeepKnowledgeTracing
---

## Resumo de uma linha
Introduz o DKT (Deep Knowledge Tracing): aplica RNNs (LSTM) ao rastreamento de conhecimento, eliminando a necessidade de anotação humana de KCs e obtendo ganho de 25% em AUC sobre BKT no Assistments benchmark.

## Fatos críticos para este projeto

**Arquitetura (Section 3):**
- O paper testa **dois modelos**: (1) vanilla RNN com unidades sigmoid e (2) LSTM. A coluna "DKT" da Table 1 reporta especificamente o resultado do **LSTM**, que supera o RNN vanilla na maioria dos datasets.
- Input por passo t: one-hot encoding do par `(q_t, a_t)` → `x_t ∈ {0,1}^{2M}` onde M = número de exercícios
  - **Combinado** em um único vetor de dimensão 2M — separar `q_t` e `a_t` em vetores distintos **piora** performance (ablação no paper)
  - Para M grande: o paper propõe projeção aleatória `n_{q,a} ~ N(0,I)` de dimensão N << M em vez de one-hot; não aplicável ao CSEDM (M ≈ 10 por assignment)
- `h_t = tanh(W_hx · x_t + W_hh · h_{t-1} + b_h)` — hidden state LSTM
- `y_t = σ(W_yh · h_t + b_y)` — vetor de probabilidades, dimensão M (uma por exercício)
- Predição para exercício `q_{t+1}`: lê a entrada `y_t[q_{t+1}]` correspondente
- Dropout aplicado em `h_t` ao computar `y_t`, **não** ao computar `h_{t+1}`
- Gradient clipping para evitar exploding gradients

**Função de perda (Eq. 3):**
```
L = Σ_t l(y^T δ(q_{t+1}), a_{t+1})
```
onde `δ(q_{t+1})` é o one-hot do exercício seguinte e `l` é binary cross-entropy

**Hiperparâmetros (usados por Piech et al.):**
- Hidden dimensionality: 200
- Mini-batch size: 100
- Otimização: SGD com minibatches

## Resultados quantitativos (Table 1)

| Dataset | Marginal | BKT | BKT* | DKT (LSTM) |
|---------|---------|-----|------|------------|
| Simulated-5 (4K students, 50 exercises) | — | 0.54 | — | **0.75** |
| Khan Math (47.5K students, 69 exercise tags) | 0.63 | 0.68 | — | **0.85** |
| Assistments (15.9K students, 124 exercise tags) | 0.62 | 0.67 | 0.69 | **0.86** |

- DKT supera BKT em **25% AUC** no Assistments (0.86 vs 0.69 do melhor BKT reportado na literatura)
- Métrica: AUC; avaliação: 5-fold cross-validation

## Relevância para implementação no CSEDM

- Este é o **modelo base** que Shi et al. (2022) extendem com code2vec → Code-DKT
- Input identico ao nosso: one-hot (ProblemID, correct) com dimensão 2×10 por assignment (10 problemas/assignment no CSEDM)
- Resultado de referência no CSEDM: **DKT ~71.24% AUC overall** em A1 (Table 1, Shi et al., 2022)
- Limitação relevante para este TCC: CSEDM tem apenas ~329 alunos em Release/Train — dataset pequeno para deep models; explica por que margem DKT→Code-DKT (~3pp) é menor que nos datasets de Piech et al.

## Aplicação adicional: descoberta de relações entre exercícios (Section 4.2)
- Influence function: `J_ij = y(j|i) / Σ_k y(j|k)` — probabilidade de acertar j dado que acertou i no primeiro passo
- Relevante para TCC 2: pode guiar sequenciamento de problemas para o docente

## Nota sobre pyBKT
O paper cita [33] Yudelson et al. (2013) como referência para BKT individualizado — a mesma abordagem implementada pelo pyBKT. Para citação do pyBKT na implementação, usar Yudelson et al. (2013) junto com Corbett & Anderson (1995) como fundamento teórico.

## Citação BibTeX
```
@inproceedings{piech2015dkt,
  author    = {Chris Piech and Jonathan Bassen and Jonathan Huang and Surya Ganguli and
               Mehran Sahami and Leonidas Guibas and Jascha Sohl-Dickstein},
  title     = {Deep Knowledge Tracing},
  booktitle = {Advances in Neural Information Processing Systems 28 (NeurIPS 2015)},
  pages     = {505--513},
  year      = {2015}
}
```
