---
source: docs/AutomatedKC.pdf
cite_as: Duan et al. (2025)
title: "Automated Knowledge Component Generation for Interpretable Knowledge Tracing in Coding Problems"
venue: Preprint, arXiv:2502.18632v3 [cs.AI], 20 Oct 2025. Under review.
---

## Resumo de uma linha
Pipeline LLM-based (KCGen-KT) que usa GPT-4o para gerar e tagear KCs automaticamente para problemas de programação, superando KCs escritos por humanos em KT.

## Fatos críticos para este projeto
- KCs gerados por LLM superam KCs humanos em previsão de desempenho futuro em programming KT
- Abordagem: GPT-4o gera KCs → clustering por similaridade semântica (Sentence-BERT + HAC) → rótulo final por GPT-4o
- Input no tempo `t`: `(p_t, {w_t^i}, c_t, a_t)` — statement do problema, KCs, código submetido, correção
- `a_t = 1` se código passa em todos os testes (alinha com CSEDM: `Score == 1.0`)
- Avaliado em 2 datasets de código (Java e outro) — **não o CSEDM**

## Metodologia relevante
- KCGen-KT: combina representação semântica dos KCs com perfil interpretável do aluno (mastery levels)
- Soft-token conversion para injetar mastery level no espaço de input do LLM
- Avalia learning curves — KCs gerados por LLM têm melhor fit com o modelo de análise de curvas de aprendizagem (PFA) do que KCs humanos

## Relevância para este TCC
Referência alternativa para definição de KCs. No CSEDM, usamos `ProblemID` como KC (mesma decisão do Shi et al. 2022 — footnote 1 do paper). Este paper mostra que KCs mais finos (gerados por LLM) poderiam melhorar KT — mas está fora do escopo do TCC 1.

## Citação BibTeX
```
@article{duan2025automatedkc,
  author    = {Zhangqi Duan and Nigel Fernandez and Arun Balajiee Lekshmi Narayanan and
               Mohammad Hassany and Rafaella Sampaio de Alencar and Peter Brusilovsky and
               Bita Akram and Andrew Lan},
  title     = {Automated Knowledge Component Generation for Interpretable Knowledge Tracing in Coding Problems},
  journal   = {arXiv preprint arXiv:2502.18632},
  year      = {2025}
}
```
