---
source: docs/893CorbettAnderson1995.pdf
cite_as: Corbett & Anderson (1995)
title: "Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge"
venue: User Modeling and User-Adapted Interaction 4(4): 253–278, 1995 (Kluwer Academic Publishers)
doi: https://doi.org/10.1007/BF01099821
---

## Resumo de uma linha
Introduz o BKT (Bayesian Knowledge Tracing): modelo de dois estados (aprendido/não-aprendido) com 4 parâmetros por KC para rastrear o conhecimento do aluno e implementar aprendizado por domínio (mastery learning) em tutores inteligentes.

## Fatos críticos para este projeto

**Modelo BKT — 4 parâmetros por KC (Fig. 4 do paper):**
| Parâmetro | Nome | Definição |
|-----------|------|-----------|
| P(L₀) | Initial Learning | Probabilidade de o KC estar no estado aprendido antes da primeira oportunidade de aplicação |
| P(T) | Acquisition | Probabilidade de transição de não-aprendido → aprendido a cada oportunidade de aplicação |
| P(G) | Guess | Probabilidade de resposta correta mesmo com o KC não-aprendido |
| P(S) | Slip | Probabilidade de resposta incorreta mesmo com o KC aprendido |

**Equação de atualização (Eq. 1):**
```
p(Lₙ) = p(Lₙ₋₁ | evidência) + (1 − p(Lₙ₋₁ | evidência)) × p(T)
```
- `p(Lₙ₋₁ | evidência)`: posterior bayesiana da n-ésima oportunidade (contingente a acerto/erro)
- Sem forgetting: o modelo não admite transição de aprendido → não-aprendido

**Critério de domínio (mastery):** p(L) ≥ 0.95 por KC — tutor continua exercícios até atingir esse limiar

**Definição de KC:** regra de produção no *ideal student model* (ACT-R); cada regra é um símbolo individual de programa (e.g., uso de `car`, definição de `defun`); parâmetros estimados empiricamente por regra

**Equação de predição de acerto (Eq. 2):**
```
p(C_is) = p(L_rs) × (1 − p(S_r)) + (1 − p(L_rs)) × p(G_r)
```
- `p(L_rs)`: probabilidade estimada de o KC estar aprendido para o estudante s na regra r
- Probabilidade de acerto = P(aprendido) × P(não-slip) + P(não-aprendido) × P(guess)
- Usada a cada passo para gerar a predição; pyBKT aplica essa fórmula internamente

**Contexto experimental:** ACT Programming Tutor — estudantes aprendem Lisp/Prolog/Pascal; 21 regras de produção no primeiro capítulo do Lisp Tutor (Experiment 1); modelo cresceu para 55 regras nas versões subsequentes; curva de erro média cai de ~0.42 na primeira oportunidade até ~0.12 após ~12 oportunidades de prática (Fig. 3)

## Relevância para implementação com pyBKT

- pyBKT implementa exatamente este modelo de 4 parâmetros com EM para estimação
- KC = ProblemID (protocolo Shi et al., 2022) → um conjunto de 4 parâmetros por problema por assignment
- `correct = (Score == 1.0)` mapeia diretamente a acerto/erro binário requerido pelo BKT
- Limitação relevante (reconhecida no paper): BKT assume independência entre KCs — problemas de programação raramente satisfazem isso; motiva extensões como DKT

## Resultados quantitativos (contexto histórico)
- Sem AUC reportada (métrica não era padrão em 1995); avaliação via taxa de erro e previsão de desempenho em testes
- BKT **não-individualizado** prediz performance em teste com r = 0.69 (Experiment 2, Table I, Test 3 — modelo com parâmetros iguais para todos os alunos)
- BKT com **parâmetros individualizados dinamicamente**: r = 0.81 em Test 3 (Experiment 3, Table III) e r = 0.66 em Test 3 (Experiment 4, Table IV — currículo expandido, 25 alunos)
- Referência comparativa no CSEDM — Shi et al. (2022) Table 2: BKT atinge **63.78% AUC** (overall) e **50.22%** (first attempts) em A1, significativamente abaixo do DKT (71.24%) e Code-DKT (74.31%)

## Citação BibTeX
```
@article{corbett1995kt,
  author    = {Albert T. Corbett and John R. Anderson},
  title     = {Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge},
  journal   = {User Modeling and User-Adapted Interaction},
  volume    = {4},
  number    = {4},
  pages     = {253--278},
  year      = {1995},
  doi       = {10.1007/BF01099821}
}
```
