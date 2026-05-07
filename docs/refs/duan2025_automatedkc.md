---
source: docs/AutomatedKC.pdf
cite_as: Duan et al. (2025)
title: "Automated Knowledge Component Generation for Interpretable Knowledge Tracing in Coding Problems"
venue: Preprint, arXiv:2502.18632v3 [cs.AI], 20 Oct 2025. Under review.
---

## Resumo de uma linha
Pipeline LLM-based (KCGen-KT) que usa GPT-4o para gerar e tagear KCs automaticamente para problemas de programação, superando KCs escritos por humanos em KT.

## Referência primária do notebook 03b_kc_generation.ipynb
Este paper é a referência central para a implementação do notebook 03b. Antes de implementar
qualquer célula do 03b, leia também `PLAN_KC_GENERATION.md` para as decisões de design adaptadas
ao CSEDM.

---

## Fatos críticos para este projeto

- KCs gerados por LLM superam KCs humanos em previsão de desempenho futuro em programming KT
- Abordagem: LLM gera KCs → clustering (Sentence-BERT + HAC) → rótulo final por LLM
- Input no tempo `t`: `(p_t, {w_t^i}, c_t, a_t)` — statement do problema, KCs, código submetido, correção
- `a_t = 1` se código passa em todos os testes (alinha com CSEDM: `Score == 1.0`)
- Avaliado em 2 datasets de código Java — **não o CSEDM**; os resultados numéricos não são diretamente comparáveis

---

## Ablation Studies — Decisões críticas de implementação

### Table 4 — Ablação: representação do código como input ao LLM

| Configuração | AUC |
|---|---|
| Student Code (código bruto) | **0.812** ← melhor |
| Student Code + AST | 0.800 |
| AST only | 0.784 ← pior |
| No code | 0.790 |

**Conclusão:** LLM recebe código bruto — NÃO AST. Enviar AST XML ao LLM *piora* qualidade
dos KCs. LLMs não foram pré-treinados em XML de AST. AST deve ser usado apenas
por nós para validação post-hoc, nunca nos prompts.

### Table 4 — Ablação: in-context examples

| Configuração | AUC |
|---|---|
| Com in-context examples (base) | **0.812** |
| Sem in-context examples | 0.782 |

**Conclusão:** In-context examples são obrigatórios. Redução de ~3pp sem eles.
Usar exemplos do Appendix B (Table 8) do paper.

### Table 5 — Ablação: número de submissões por problema

| n submissões | AUC |
|---|---|
| 1 | 0.798 |
| 3 | 0.807 |
| **5** | **0.812** ← ótimo |
| 7 | 0.811 |
| 10 | 0.810 |

**Conclusão:** n=5 é o ponto ótimo. Estratificação por número de tentativas antes do
acerto garante diversidade de estratégias de solução.

---

## Pipeline KCGen-KT — Etapas e prompts

### Stage 1 — Inferência do problema + Geração de KCs (um único prompt)

**Estratégia:** chain-of-thought em prompt único. O modelo raciocina: código → descrição do
problema → KCs necessários. Não há Stage 1 e Stage 2 separados — tudo em uma chamada.

**Prompt (baseado em Table 8, Appendix B):**
```
You are an expert CS educator analyzing introductory Java programming problems.

You will be given {n} correct student solutions to the same programming problem.
Analyze these solutions to infer what knowledge is required to solve the problem.

[FEW-SHOT EXAMPLES from Table 8 — 2 Java problems with their KCs]

Now analyze these solutions for Problem {problem_id}:

Solution 1:
```java
{code_1}
```
...
Solution n:
```java
{code_n}
```

Respond with a JSON object:
{
  "problem_description": "1-2 sentence description of what this problem requires",
  "kcs": [
    {"name": "KC name (3-8 words)", "reasoning": "Why this KC is needed (1 sentence)"},
    ...
  ]
}
```

**In-context examples (Table 8 — Appendix B):** 2 exemplos de problemas Java introdutórios
com seus KCs esperados. Exemplos devem ser de granularidade compatível com o CSEDM
(estruturas de controle, operações com arrays, métodos básicos).

### Stage 2 — Clustering (sem LLM)

1. Coletar todos os KCs brutos do assignment (~50 KCs por assignment)
2. Embeddings: Sentence-BERT `all-MiniLM-L6-v2`
3. HAC com cosine distance
4. n_clusters alvo: 10–15 por assignment (abstração média para 10 problemas)
   - Testar 10, 12, 15; selecionar pelo silhouette score ou inspeção manual
5. Output: `{kc_name → cluster_id}` + lista de KCs por cluster

### Stage 3 — Rotulagem de clusters (Table 9)

**Prompt (baseado em Table 9):**
```
You are labeling a cluster of related Knowledge Components for a programming course.

The following KCs were grouped together based on semantic similarity:
{list of KC names in the cluster}

Decide: does one of these KCs represent the entire cluster, or should you synthesize
a new label that captures the common concept?

Respond with a JSON object:
{
  "kc_id": {cluster_index},
  "name": "Final KC label (3-8 words)",
  "reasoning": "Why this label represents the cluster (1 sentence)"
}
```

### Stage 4 — KC Correctness Labeling (Table 10)

**Prompt (baseado em Table 10):**
```
You are assessing which Knowledge Components a student failed to demonstrate in their
incorrect submission.

Problem: {problem_description}

Required Knowledge Components for this problem:
{list of KC names}

Student's incorrect submission:
```java
{incorrect_code}
```

For each KC, determine if the student failed to demonstrate it (1 = failed, 0 = demonstrated).

Respond with a JSON object:
{
  "error_reasoning": ["Explanation of error 1", "Explanation of error 2", ...],
  "kc_errors": {
    "KC name 1": 0,
    "KC name 2": 1,
    ...
  }
}
```

---

## Metodologia relevante

- KCGen-KT: combina representação semântica dos KCs com perfil interpretável do aluno (mastery levels)
- Soft-token conversion para injetar mastery level no espaço de input do LLM
- Learning curves: KCs gerados por LLM têm melhor fit com PFA (power law of practice) do que KCs humanos
- Avalia: AUC, RMSE, interpretabilidade (learning curve shape), e correlação KC difficulty × human judgment

---

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
