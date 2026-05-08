# Critérios de Validação — 04_bkt.ipynb

Estes critérios são usados pelo Content Validator (Layer 3) para avaliar a qualidade
de pesquisa do notebook `notebooks/04_bkt.ipynb` de forma independente do plano de
geração. O validador não tem acesso ao bkt.json nem aos prompts do gerador.

---

## 1. Investigação do Split A494/A502

**O que verificar:**
- O notebook investiga empiricamente (não assume) quais assignments estão presentes em Release/Test
- Confirma que A439, A487, A492 têm dados de teste; A494 e A502 têm 0 estudantes
- Documenta o motivo: corte de data — esses assignments foram realizados após o período do Release/Test
- **Não trata como bug de preprocessing** — a limitação é documentada como característica estrutural do dataset
- Compara com Shi et al. (2022): o paper reporta 5 assignments na Table 1 para DKT/Code-DKT; o notebook levanta a hipótese de divergência de split (não assume que o paper está errado)
- Documenta explicitamente que métricas de teste são reportadas apenas para 3 assignments (A439, A487, A492) e que BKT é treinado em todos os 5

**Critério de falha:** O notebook não investiga o issue A494/A502 ou simplesmente filtra sem justificar.

---

## 2. Implementação pyBKT

**O que verificar:**
- Usa `pyBKT.models.Model` (não implementação manual do BKT)
- Um modelo por assignment (não um modelo global)
- KC = `skill_name = str(ProblemID)` — os 4 parâmetros BKT são estimados por ProblemID
- Treinamento com `model.fit(data=train_df)` onde `train_df` tem colunas `user_id, skill_name, correct`
- Parâmetros exibidos via `model.params()` — DataFrame MultiIndex com (skill, param, class)
- Parâmetros válidos verificados: todos em [0, 1], P(G) + P(S) < 1 por KC
- Markdown conecta parâmetros às equações de Corbett & Anderson (1995): P(C) = P(L)*(1-S) + (1-P(L))*G

**Critério de falha:** Modelo global (sem separação por assignment), KC diferente de ProblemID, parâmetros não validados.

---

## 3. Avaliação Correta — First-Attempt vs All-Attempts

**O que verificar:**
- **AUC-ROC** usado como métrica (não accuracy, não RMSE) — justificado pelo desequilíbrio ~23.7% correto
- **All-attempts AUC**: calculado sobre todas as predições `correct_predictions` vs `correct` (excluindo NaN)
- **First-attempt AUC**: calculado filtrando as linhas com `is_first_attempt=True`; a coluna `is_first_attempt` vem dos sequences gerados em 02_preprocessing.ipynb
- Distinção entre as duas métricas documentada e justificada no markdown
- Markdown explica por que first-attempt AUC ≈ 50% para BKT: predição na primeira tentativa é constante por KC (função apenas de P(L0), G, S), sem distinção entre estudantes
- Markdown explica por que all-attempts AUC é inflado por autocorrelação temporal (BKT aprende o histórico e passa a prever tentativas repetidas corretamente)

**Critério de falha:** Confusão entre as duas métricas, uso de accuracy em vez de AUC, filtro `is_first_attempt` ausente ou incorreto.

---

## 4. Targets Numéricos e Comparação com Paper

**O que verificar:**
- A439 **all-attempts AUC** no intervalo [58%, 70%] — referência: 63.78% ± 4.68% (Shi et al. 2022, Table 2)
- A439 **first-attempt AUC** no intervalo [45%, 56%] — referência: 50.22% ± 2.86%
- Shi et al. (2022) Table 2 citado explicitamente como fonte dos targets
- Se os valores ficarem fora dos intervalos, o notebook deve discutir a causa (diferença de split, threshold Score, etc.) — não apenas reportar o número sem contexto
- Tabela comparativa presente: nossos valores vs paper, por assignment

**Critério de falha:** A439 all-attempts AUC < 55% ou > 72%, ou first-attempt AUC < 40% ou > 60%; ausência de comparação com o paper.

---

## 5. Rastreabilidade Metodológica

**O que verificar:**
- `SEED = 42` definido explicitamente no código (não apenas como comentário)
- Split usado: `Release/Train` para treino, `Release/Test` para avaliação (não `All/`)
- `results/bkt_results.pkl` existe após execução com schema documentado: `{int: {all_auc, first_auc, n_train, n_test, params}}`
- Corbett & Anderson (1995) citados na discussão dos parâmetros BKT
- Shi et al. (2022) citados como fonte dos targets numéricos e protocolo de avaliação (KC=ProblemID, 4:1 split, 10 repetições no paper vs nosso split oficial)
- Padrão didático do harness respeitado: cada célula de código precedida por markdown (Contexto/Hipótese/Referência) e seguida por markdown (Achado/Implicação para modelagem)
- Ausência de placeholders (TODO, pass, NotImplementedError, ...)

**Critério de falha:** SEED ausente no código, split errado (All/ em vez de Release/), bkt_results.pkl ausente, ausência do padrão didático em ≥2 células de código.
