---
source: docs/2309.04761v4.pdf
cite_as: Lin et al. (2024)
title: "A comprehensive survey on deep learning techniques in educational data mining"
venue: Preprint submitted to Elsevier (arXiv:2309.04761v4 [cs.LG], 11 Jun 2024)
---

## Resumo de uma linha
Survey sistemático de algoritmos de Deep Learning aplicados a EDM, cobrindo KT, detecção de comportamento, previsão de desempenho e recomendação personalizada.

## Fatos críticos para este projeto
- Categoriza KT em: Supervised (LSTM, RNN, Attention, Transformer), Unsupervised (Autoencoder), Reinforcement Learning
- DKT (Piech et al., 2015) é classificado como RNN/LSTM — baseline histórico do campo
- BKT (Corbett & Anderson, 1994) é tratado como Unsupervised (modelo probabilístico sem DL)
- SAKT (Self-Attentive KT) e AKT são variantes de Attention que superam DKT em benchmarks ASSIST
- Dataset de referência dominante no campo: ASSISTments (09, 12, 15, 17) — **diferente do CSEDM**

## Resultados quantitativos relevantes (Table 1 — benchmarks do campo, não CSEDM)
| Modelo | Método | Métrica | Dataset |
|--------|--------|---------|---------|
| DKT | RNN/LSTM | AUC | ASSISTment09/10 |
| SAKT | Attention | AUC | ASSISTment09/12 |
| AKT | Attention | AUC | ASSISTment09/12 |

*Valores exatos não extraídos — este paper é survey, não reporta números próprios no campo de KT para programação.*

## Metodologia relevante
- EDM divide-se em 4 cenários: Knowledge Tracing, Student Behavior Detection, Performance Prediction, Personalized Recommendation
- KT formula: dado histórico de interações `(exercício, acerto)` até `t`, prever `t+1`
- DL supera baselines tradicionais em ~67% dos estudos revisados
- Tendências emergentes: LLMs para EDM, explainabilidade, social network analysis

## Relevância para este TCC
Útil como background para justificar a escolha de DKT e suas variantes. Não contém benchmarks no CSEDM nem em tarefas de programação Java — usar Shi et al. (2022) para comparações diretas.

## Citação BibTeX
```
@article{lin2024dlsurvey,
  author    = {Yuanguo Lin and Hong Chen and Wei Xia and Fan Lin and Zongyue Wang and Yong Liu},
  title     = {A comprehensive survey on deep learning techniques in educational data mining},
  journal   = {Preprint (arXiv:2309.04761)},
  year      = {2024},
  note      = {Submitted to Elsevier}
}
```
