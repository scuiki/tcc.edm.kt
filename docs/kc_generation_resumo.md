# Geração de Knowledge Components (KCs) via LLM — Resumo do Pipeline

> Notebook: `notebooks/03b_kc_generation.ipynb`  
> Referência principal: Duan et al. (2025), *KCGen-KT*, arXiv:2502.18632v3

---

## O problema que precisávamos resolver

Um modelo de Knowledge Tracing (KT) precisa saber *o que* cada problema testa — os conceitos que o aluno precisa dominar. No dataset CSEDM, a gente não tem enunciados dos problemas. O que temos são apenas os códigos Java que os alunos submeteram. Então como identificar o que cada problema está avaliando?

A abordagem clássica, usada por Shi et al. (2022) como baseline, é simplesmente dizer: "cada problema é um KC diferente". Funciona, mas é cego — não captura nenhuma estrutura semântica do que está sendo aprendido. Se dois problemas exigem a mesma habilidade (digamos, usar um `for` com condição de saída), o modelo não sabe disso.

A alternativa que implementamos, baseada no pipeline **KCGen-KT de Duan et al. (2025)**, é usar um LLM para inferir os KCs diretamente das submissões dos alunos.

---

## Etapa 1 — Escolher os melhores exemplos de código para mostrar ao LLM

O LLM precisa ver código correto para entender o que cada problema pede. Mas qual código? Se mostrarmos só os alunos que acertaram de primeira, vemos apenas a solução mais óbvia. Se mostrarmos só quem demorou muito, vemos soluções contorcidas. A ideia é **diversity sampling**: estratificar os alunos por quantas tentativas precisaram antes de acertar e pegar um exemplo de cada grupo.

Os grupos foram:
- Bucket 1: acertou na 1ª tentativa
- Bucket 2: 2–3 tentativas
- Bucket 3: 4–6 tentativas
- Bucket 4: 7–10 tentativas
- Bucket 5: mais de 10 tentativas

Amostramos até 5 submissões por problema (uma por bucket disponível). Por que 5? Duan et al. (2025, Table 5) testaram sistematicamente: com 1 submissão AUC fica em 0.798, com 3 em 0.807, com **5 em 0.812** — e com 7 ou 10 não melhora mais. Ponto de saturação comprovado empiricamente. Na prática, a maioria dos problemas teve 5 amostras (47 dos 50 problemas), com 3 problemas tendo 4 (alguns buckets simplesmente não tinham alunos).

---

## Etapa 2 — Pedir ao LLM para gerar os KCs

Para cada problema, mandamos os 5 códigos de exemplo ao LLM com um prompt estruturado em chain-of-thought: "aqui estão soluções corretas — o que este problema está avaliando? Liste os Knowledge Components necessários."

Duas decisões de design importantes aqui:

**Por que mandamos o código bruto e não a árvore sintática (AST)?**
Isso parece contraintuitivo — afinal, a AST é mais estruturada. Mas Duan et al. (2025, Table 4) fizeram o experimento e descobriram que mandar XML de AST *piora* a qualidade dos KCs (AUC de 0.812 cai para 0.784). O motivo: LLMs são pré-treinados em código legível por humanos, não em XML de árvore sintática. Mandar AST é como pedir a alguém fluente em português para traduzir Morse — possível, mas ineficiente.

**Por que incluímos exemplos no prompt (few-shot)?**
Sem exemplos, o LLM tende a gerar KCs vagos demais ou genéricos demais. Duan et al. (Table 4, ablation) mostraram que remover os exemplos custa ~3 pontos de AUC. Usamos 2 exemplos adaptados do Apêndice B do paper — problemas introdutórios de Java com granularidade compatível com o CSEDM.

O output do LLM foi estruturado como JSON:
```json
{
  "problem_description": "Dado dois inteiros, retorna 20 se a soma está entre 10 e 19...",
  "kcs": [
    {"name": "Compound boolean condition with AND operator", "reasoning": "..."},
    ...
  ]
}
```

Resultado: entre 5.5 e 6.0 KCs por problema em média, por assignment. Total de ~292 KCs brutos gerados nos 5 assignments.

---

## Etapa 3 — Agrupar KCs similares (Clustering)

Com ~6 KCs por problema e 10 problemas por assignment, temos ~60 KCs brutos por assignment. Mas muitos deles são sinônimos ou variações do mesmo conceito. Por exemplo: "Conditional return in if-else" e "Returning values from conditional statements" — semanticamente iguais.

Para consolidar, usamos **Sentence-BERT** (modelo `all-MiniLM-L6-v2`) para transformar cada KC em um vetor numérico que captura seu significado semântico, e depois **HAC** (Hierarchical Agglomerative Clustering) com distância cosseno para agrupar os KCs parecidos.

Quantos clusters usar? Testamos 10, 12 e 15 por assignment e escolhemos pelo **silhouette score** (métrica que mede o quão bem separados os clusters estão):

| Assignment | n_clusters | Silhouette (10 / 12 / 15) |
|---|---|---|
| A439 | 15 | 0.298 / 0.308 / **0.323** |
| A487 | 15 | 0.197 / 0.204 / **0.262** |
| A492 | 15 | 0.194 / 0.226 / **0.228** |
| A494 | 15 | 0.199 / 0.202 / **0.222** |
| A502 | 12 | 0.166 / **0.179** / 0.155 |

Para A502, aumentar de 12 para 15 clusters *piorou* o silhouette — indicando que os KCs deste assignment têm um espaço semântico naturalmente mais compacto.

---

## Etapa 4 — Nomear os clusters com o LLM

Cada cluster tem vários KCs brutos. Pedimos ao LLM para examinar os KCs do cluster e decidir: "Este KC representa o grupo inteiro, ou precisamos sintetizar um novo rótulo?"

O prompt foi adaptado da Table 9 de Duan et al. (2025). O output é o KC canônico de cada cluster — o rótulo final que vai para a Q-matrix.

Exemplos dos KCs canônicos do assignment **A439** (condicionais básicos):
- KC 0: Range validation with logical operators
- KC 6: Conditional branching with multiple paths
- KC 8: Compound boolean expressions with logical operators
- KC 13: Method parameter usage in computation

KCs canônicos do **A487** (problemas de String):
- KC 0: String indexing and substring extraction
- KC 1: String length validation and edge cases
- KC 12: Integer division and modulo arithmetic

---

## Etapa 5 — Construir a Q-matrix

A Q-matrix é a tabela que relaciona problemas a KCs: entrada (problema P, KC k) = 1 se o problema P requer o KC k, 0 caso contrário.

Para construí-la, mapeamos cada KC bruto gerado (Etapa 2) para o cluster a que pertence (Etapas 3/4). O conjunto de KCs de um problema é a união dos clusters de todos os seus KCs brutos.

| Assignment | Problemas | KCs | Densidade | KCs/problema |
|---|---|---|---|---|
| A439 | 10 | 15 | 32% | 3–6 |
| A487 | 10 | 15 | 29% | 3–6 |
| A492 | 10 | 15 | 26% | 3–6 |
| A494 | 10 | 15 | 32% | 3–6 |
| A502 | 10 | 12 | 30% | 3–6 |

Nenhum problema com 0 KCs (validado explicitamente). Um fragmento da Q-matrix do A439 mostra como o KC 8 ("Compound boolean expressions") aparece em quase todos os problemas — faz sentido, é um assignment de condicionais básicos em Java.

---

## Etapa 7 — Assinaturas AST (validação post-hoc)

Para verificar se os KCs gerados fazem sentido, usamos o srcML para parsear as submissões corretas e extrair a frequência de cada tipo de nó da árvore sintática (`if_stmt`, `return`, `function`, etc.). Feito para todos os 5 assignments.

A ideia é: se o LLM disse que o Problema 1 exige "Compound boolean expressions with AND operator", devemos conseguir confirmar que `if_stmt` aparece em praticamente 100% das submissões corretas desse problema. Essa validação é qualitativa, serve como evidência metodológica no documento do TCC.

---

## Etapa 6 — KC Correctness Labeling (concluída)

A etapa mais cara do pipeline, **KC Correctness Labeling**, foi concluída para os 5 assignments em maio de 2026. Para cada submissão *incorreta* de `Run.Program` no Spring 2019 train, pedimos ao LLM (Claude Haiku 4.5) que identificasse quais KCs o estudante falhou em demonstrar naquela tentativa (rótulo 1 = falhou, 0 = demonstrou apesar do erro). O resultado são sequências de erro por KC (não apenas por problema), que permitem curvas de aprendizagem PFA observadas no nível de conceito e análises interpretativas de onde os estudantes têm mais dificuldade.

Total rotulado: **30.747 submissões** (apenas train, sem tocar no test para evitar vazamento de dados). Custo real: ~$0,000554 por chamada, totalizando ~$8,6 na etapa. A estimativa inicial de ~$39 ficou cerca de 3 vezes inflada, o prompt caching ajuda pouco porque o contexto cacheado (descrição do problema mais nomes de KC) é pequeno perto do código submetido (até 3000 caracteres), que não é cacheado.

Os arquivos são gerados com checkpoint por problema e resume idempotente, então execuções interrompidas (por exemplo, esgotamento de créditos) retomam de onde pararam sem repagar pelo que já foi rotulado.

---

## Resumo dos artefatos gerados

```
results/
├── kc_raw_A*.json           — KCs brutos + descrição do problema por ProblemID    [5/5]
├── kc_clusters_A*.json      — agrupamento Sentence-BERT + HAC                     [5/5]
├── kc_descriptions_A*.json  — KCs canônicos (rótulos finais por cluster)           [5/5]
├── qmatrix_A*.csv           — Q-matrix ProblemID × KC_id (binário)                [5/5]
├── ast_signatures_A*.json   — frequência de nós srcML por ProblemID               [5/5]
└── kc_correctness_A*.json   — labels KC por submissão incorreta (train-only)      [5/5]
```

---

## Referências

- **Duan et al. (2025)** — KCGen-KT: pipeline LLM completo, prompts (Tables 8–10), ablation studies (Tables 3–5). Fonte de: estrutura do pipeline, in-context examples, prompt de correctness labeling, número ótimo de submissões (n=5).
- **Shi et al. (EDM 2022)** — KC = ProblemID como baseline; protocolo per-assignment. Replicado em `04_bkt.ipynb` e `05_dkt.ipynb`.
- **Rivers et al. (ICER 2016)** — AST node types como KCs em programação (background para Etapa 7).
