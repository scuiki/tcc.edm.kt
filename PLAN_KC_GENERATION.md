# Plano — Geração de KCs via LLM (notebook 03b)

Documento de referência para implementação do `notebooks/03b_kc_generation.ipynb`.  
Decisões tomadas com base na análise de Duan et al. (2025) — KCGen-KT.

---

## Contexto e motivação

O CSEDM não possui enunciados textuais dos problemas — apenas snapshots de código dos
alunos. A geração de KCs é feita exclusivamente a partir de submissões corretas, usando
LLM para interpretar semanticamente o que cada problema exige.

**Referência principal:** Duan et al. (2025), *Automated Knowledge Component Generation for
Interpretable Knowledge Tracing in Coding Problems*, arXiv:2502.18632v3.

**Decisão crítica (ablation de Duan et al., Table 4):** substituir código bruto por
representação AST como input ao LLM *piora* a qualidade dos KCs gerados — LLMs não são
pré-treinados em XML de AST. Portanto:

- **LLM recebe código bruto** → gera KCs
- **AST (srcML) é usado apenas por nós** para validação post-hoc dos KCs gerados
  (ex.: "o KC 'iteração sobre array' está ancorado em `ForStatement` + `ArrayAccess`
  presentes em 80% das corretas?") — nenhuma menção a AST nos prompts

---

## Escopo

- **Assignments:** todos os 5 (A439, A487, A492, A494, A502)
- **Split:** `Release/Train` exclusivamente (evitar data leakage)
- **Q-matrix:** per-assignment — vocabulário de KCs independente por assignment
- **Modelo LLM:** Claude Haiku (custo-benefício; ~$40–50 total para o pipeline completo)

---

## Pipeline

### Etapa 1 — Diversity sampling de submissões corretas

**Input:** `results/sequences_bkt_dkt.pkl` (train) + `Release/Train/Data/CodeStates/CodeStates.csv`

Para cada `(AssignmentID, ProblemID)`:
1. Filtrar eventos com `correct == 1`
2. Estratificar por número de tentativas antes do acerto (proxy de diversidade de abordagem):
   - bucket 1: acertou na 1ª tentativa
   - bucket 2: 2–3 tentativas
   - bucket 3: 4–6 tentativas
   - bucket 4: 7–10 tentativas
   - bucket 5: >10 tentativas
3. Amostrar 1 submission por bucket disponível, até n=5
4. Join com `CodeStates.csv` via `CodeStateID` para obter código Java

**Fundamento:** Duan et al. (2025, Table 5) — 5 submissões é o ponto ótimo; menos de 5
reduz cobertura de KCs; mais de 5 satura. Estratificação por tentativas garante diversidade
de estratégias de solução (solução direta vs. solução após erros).

**Output:** dict `{problem_id: [code_1, ..., code_5]}`

---

### Etapa 2 — Geração de KCs por problema (LLM)

**~50 chamadas LLM (1 por problema × 5 assignments × 10 problemas)**

**Prompt design:** chain-of-thought estruturado em único prompt — sem Stage separado para
inferência do problema. O modelo raciocina em contexto contínuo: código → descrição → KCs.

**In-context examples:** 2 exemplos do Apêndice B (Table 8) de Duan et al. (2025),
adaptados diretamente — problemas Java introdutórios de granularidade compatível com
o CSEDM. Citação explícita no notebook.

> Fundamento para citação: "We include a few carefully constructed in-context examples in
> our prompt as few-shot demonstrations" — Duan et al. (2025), Section 3.1.1.
> Ablation sem in-context examples: AUC 0.782 vs 0.812 base (−3pp) — Table 4.

**Estrutura do output (JSON):**
```json
{
  "problem_description": "Descrição inferida em 1-2 frases do que o problema pede",
  "kcs": [
    {"name": "Nome do KC", "reasoning": "Por que este KC é necessário (1 frase)"},
    ...
  ]
}
```

**Output salvo:** `results/kc_raw_{assignment_id}.json`  
**Cache obrigatório:** salvar após cada chamada — notebook re-executável sem re-chamar API.

---

### Etapa 3 — Clustering de KCs brutos (Sentence-BERT + HAC)

**Input:** todos os KCs brutos do assignment (~50 KCs por assignment, estimando ~5 por problema)

1. Embeddings com `sentence-transformers` (modelo: `all-MiniLM-L6-v2` ou similar)
2. Hierarchical Agglomerative Clustering com cosine distance
3. **n_clusters alvo: 10–15 por assignment** (nível médio de abstração para 10 problemas)
   - Testar 10, 12, 15; selecionar pelo melhor fit de curva de aprendizagem (ver Etapa 6)

**Fundamento:** Duan et al. encontraram que abstração média (50 clusters para 50 problemas)
supera alta abstração (10–20 clusters). Para 10 problemas por assignment, 10–15 clusters é
o equivalente proporcional de abstração média.

**Output:** `results/kc_clusters_{assignment_id}.json`

---

### Etapa 4 — Rotulagem de clusters (LLM)

**~60–75 chamadas LLM (12–15 clusters × 5 assignments)**

Para cada cluster: prompt chain-of-thought que decide se um KC do cluster representa o
grupo inteiro ou se é necessário sintetizar um novo rótulo.

**Prompt base:** Table 9 de Duan et al. (2025) — adaptado diretamente, citado.

**Output:** `results/kc_descriptions_{assignment_id}.json`

```json
{
  "kc_id": 0,
  "name": "Rótulo final do KC",
  "reasoning": "Por que este rótulo representa o cluster"
}
```

---

### Etapa 5 — Q-matrix

**Input:** mapeamento de cada KC bruto gerado (Etapa 2) → cluster label (Etapa 4)

Para cada problema: o conjunto de KCs é o conjunto de clusters a que seus KCs brutos pertencem.

**Output:** `results/qmatrix_{assignment_id}.csv`

```
ProblemID, kc_0, kc_1, ..., kc_14
1,          1,    0,   ...,  1
3,          0,    1,   ...,  0
...
```

---

### Etapa 6 — KC Correctness Labeling (LLM)

**~26.289 chamadas LLM (todos os eventos incorretos de Run.Program no train)**  
**Custo estimado: ~$39 com Claude Haiku**

Para cada submissão incorreta no `Release/Train`:
1. Input: descrição do problema (Etapa 2) + código incorreto + lista de KCs do problema
2. LLM identifica: (a) erros cometidos, (b) label binário por KC (0 = dominou, 1 = falhou)
3. Output per-submission: `{error_reasoning: [...], kc_errors: {kc_name: 0/1}}`

**Prompt base:** Table 10 de Duan et al. (2025) — adaptado diretamente, citado.

**Uso downstream:**
- Curvas de aprendizagem por KC: taxa de erro no KC no t-ésimo contato do estudante com
  ele → verificar power law of practice (R² via PFA)
- Análise interpretativa: quais KCs são mais difíceis, quais estudantes com baixo X-Grade
  têm mastery baixo em quais KCs

**Cache obrigatório:** salvar resultados por batch de assignment.

**Output:** `results/kc_correctness_{assignment_id}.json`

---

### Etapa 7 — Artefato de validação AST (post-hoc, sem LLM)

Para cada `(AssignmentID, ProblemID)`:
- Parsear submissões corretas com srcML
- Calcular frequência de nós AST (`ForStatement`, `IfStatement`, `ArrayAccess`, etc.)
- Output: `results/ast_signatures_{assignment_id}.json`

**Uso:** validação manual dos KCs gerados — verificar se KCs com "iteração" estão
ancorados em `ForStatement`/`WhileStatement` que aparecem em >50% das corretas.
Serve como evidência de qualidade no documento do TCC, não como etapa automática.

---

## Resumo de custo (Claude Haiku)

| Etapa | Chamadas | Custo estimado |
|---|---|---|
| Etapa 2 — KC generation | ~50 | ~$0.05 |
| Etapa 4 — Cluster labeling | ~60–75 | ~$0.10 |
| Etapa 6 — Correctness labeling | ~26.289 | ~$39 |
| **Total** | **~26.400** | **~$39–40** |

---

## Outputs finais

```
results/
├── kc_raw_{aid}.json            — KCs brutos + descrição do problema por ProblemID
├── kc_clusters_{aid}.json       — clusters Sentence-BERT
├── kc_descriptions_{aid}.json   — rótulos finais por cluster (KCs canônicos)
├── qmatrix_{aid}.csv            — ProblemID × KC_id (binário)
├── kc_correctness_{aid}.json    — labels KC por submissão incorreta
└── ast_signatures_{aid}.json    — frequência de nós srcML por ProblemID (validação)
```

---

## Referências

- **Duan et al. (2025)** — KCGen-KT: pipeline LLM completo, prompts (Tables 8–10),
  ablation studies (Tables 3–5). Fonte de: estrutura do pipeline, in-context examples,
  prompt de correctness labeling, número ótimo de submissões (n=5).
- **Rivers et al. (ICER 2016)** — AST node types como KCs em programação (background).
- **Shi et al. (EDM 2022)** — KC = ProblemID como baseline; protocolo per-assignment.
