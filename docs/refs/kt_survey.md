---
source: docs/Knowledge Tracing: A Survey
cite_as: Abdelrahman et al. (2022)
title: "Knowledge Tracing: A Survey"
venue: ACM (arXiv:2201.06953v1, 8 Jan 2022) — 36 pages
doi: https://doi.org/10.1145/nnnnnnn.nnnnnnn
---

## Resumo de uma linha
Survey sistemático de métodos de Knowledge Tracing desde BKT até modelos de Deep Learning com atenção e memória, cobrindo fundamentos teóricos e benchmarks.

## Fatos críticos para este projeto
- KT problem: dado histórico de interações `(questão, acerto)` até `t`, prever acerto em `t+1`
- Três desafios centrais: (1) questão pode exigir mais de uma skill; (2) dependência entre skills; (3) comportamento de esquecimento do aluno
- BKT (Corbett & Anderson, 1994): modelo probabilístico com 4 parâmetros — P(L₀), P(T), P(G), P(S)
- DKT (Piech et al., 2015): LSTM que aprende automaticamente relações entre problemas sem q-matrix explícita
- Avanços pós-DKT: DKVMN (memória), SAKT (self-attention), AKT (attention + decay)

## Tipologia de modelos de KT (relevante para justificativa de escolha de modelo)
| Categoria | Exemplos | Vantagem |
|-----------|----------|----------|
| Probabilístico | BKT, PFA | Interpretável, poucos parâmetros |
| Deep Learning (RNN/LSTM) | DKT, Code-DKT | Captura dependências sequenciais |
| Attention-based | SAKT, AKT | Contexto global, sem recorrência |
| Memory-augmented | DKVMN | Estado de conhecimento explícito |

## Metodologia relevante
- Survey cobre 2 abordagens de avaliação: **next-attempt prediction** (padrão — prever t+1) vs. **future performance** (prever desempenho futuro genérico)
- Métrica padrão do campo: AUC-ROC
- Benchmark datasets: ASSISTments (09, 12, 15, 17), EdNet, Junyi Academy

## Citação BibTeX
```
@article{abdelrahman2022ktsurvey,
  author    = {Ghodai Abdelrahman and Qing Wang and Bernardo Pereira Nunes},
  title     = {Knowledge Tracing: A Survey},
  journal   = {ACM Computing Surveys},
  year      = {2022},
  note      = {arXiv:2201.06953v1}
}
```
