# EDA Insights — Síntese Pós-EDA e Pré-processamento

Síntese dos achados críticos dos notebooks `01_eda.ipynb` e `02_preprocessing.ipynb`.  
Cada seção reporta valores calculados diretamente a partir dos dados, com referência explícita à célula do notebook de origem. Este documento alimenta as decisões de modelagem dos notebooks 03–07.

Dataset utilizado: **Release/Train** (246 estudantes, 5 assignments, Spring 2019) para comparação reproduzível com Shi et al. (2022).

---

## 1 — Desbalanceamento de Classes (Imbalance Ratio)

### 1.1 — Imbalance Global e por Assignment

**Contexto:** Com ~76% de tentativas incorretas, o dataset apresenta desbalanceamento moderado (~3:1). Acurácia seria inflada pela classe majoritária — um classificador-baseline "sempre incorreto" atingiria 76.3% de acurácia sem nenhum poder preditivo. AUC (Area Under the ROC Curve) mede a capacidade discriminativa independentemente do threshold de decisão e é a métrica padrão na literatura de KT.

**Hipótese:** O imbalance global deve ser ~3.2:1 (76.3% incorretos / 23.7% corretos); A3 (492) deve ter o maior desequilíbrio (menor taxa de acerto, conforme Seção 3 do EDA) e A5 (502) o menor.

**Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

Calculado em: `01_eda.ipynb` — Seção 5.2, célula de código (cálculo do imbalance ratio por assignment) e célula markdown seguinte.  
Artefato visual: `results/sec5_imbalance.png`.

| Assignment | Total | Corretos (n) | Incorretos (n) | % correto | Imbalance ratio |
|---|---|---|---|---|---|
| A1 (439) | 8.761 | 2.389 | 6.372 | 27,27% | 2,67:1 |
| A2 (487) | 10.539 | 2.141 | 8.398 | 20,32% | 3,92:1 |
| A3 (492) | 11.977 | 2.284 | 9.693 | 19,07% | 4,24:1 |
| A4 (494) | 8.585 | 2.167 | 6.418 | 25,24% | 2,96:1 |
| A5 (502) | 6.963 | 2.117 | 4.846 | 30,40% | 2,29:1 |
| **— Global —** | **46.825** | **11.098** | **35.727** | **23,70%** | **3,22:1** |

**Achado:** O dataset Release/Train apresenta desbalanceamento global de **3,22:1** (76,3% incorretos vs 23,7% corretos). Por assignment, A3 (492) tem o maior desequilíbrio (**4,24:1**, 19,07% correto) e A5 (502) o menor (**2,29:1**, 30,40% correto) — consistente com o ranking de dificuldade da Seção 3 do EDA. Um classificador-baseline ("sempre incorreto") atingiria 76,3% de acurácia sem nenhum poder discriminativo, evidenciando que acurácia é inadequada para este problema.

**Implicação para modelagem:** AUC é a métrica primária adotada neste trabalho, seguindo Shi et al. (2022) e Abdelrahman et al. (2022). A métrica secundária (all-attempts AUC) complementa com maior estabilidade estatística. Assignments com imbalance extremo (A3: 4,24:1) requerem atenção especial durante a avaliação — resultados de AUC abaixo de 0,65 em A3 devem ser interpretados com cautela dado o sinal de treinamento mais escasso (apenas 19% de corretos).

### 1.2 — Imbalance no Contexto do Code-DKT (Com Compile.Error)

**Contexto:** Ao incluir eventos `Compile.Error` como `correct=0` (protocolo Code-DKT e srcML-DKT), o imbalance se agrava porque esses eventos contribuem exclusivamente com a classe negativa.

**Referência:** Pankiewicz, Shi & Baker (2025); Shi et al. (2022).

Calculado em: `02_preprocessing.ipynb` — Seção 2.1, célula de código (filtragem `filter_for_code_dkt`).

No split Release/Train: 40.858 eventos são `Compile.Error` (de 87.683 submissões totais no protocolo Code-DKT) — **taxa global de Compile.Error de 46,6%**. Isso reduz a taxa de corretos de 23,70% (BKT/DKT) para **12,66%** (Code-DKT), resultando em imbalance implícito de ~7:1 no Code-DKT antes da truncagem.

Após truncagem (últimas 50 tentativas por sequência):
- BKT/DKT: taxa de corretos sobe de 23,70% para **27,97%** (+4,27pp)
- Code-DKT: taxa de corretos sobe de 12,66% para **19,87%** (+7,21pp)

**Achado:** O Code-DKT opera com imbalance consideravelmente maior que BKT/DKT (12,66% vs 23,70% de corretos antes da truncagem). Após truncagem, ambos melhoram porque os eventos mais recentes refletem o aprendizado acumulado. A justificativa empírica para incluir `Compile.Error` apesar do imbalance adicional é a correlação de Spearman ρ = −0,569 entre `n_compile_errors` e Label (`01_eda.ipynb`, Seção 8.1) — esses eventos carregam sinal preditivo relevante.

**Implicação para modelagem:** O Code-DKT deve ser avaliado principalmente por first-attempt AUC (não acurácia) para isolar o sinal preditivo do imbalance. A inclusão de `Compile.Error` é justificada empiricamente (correlação com Label) e teoricamente (srcML parseia código não-compilável, Pankiewicz et al., 2025), apesar de agravar o desbalanceamento.

---

## 2 — Distribuição de Sequências e Impacto da Truncagem

### 2.1 — Distribuição de Tamanho de Sequências (BKT/DKT)

**Contexto:** O DKT e o Code-DKT processam sequências de tentativas ordenadas cronologicamente. Shi et al. (2022) truncam cada sequência nas **últimas 50 tentativas** para limitar o custo computacional do LSTM e reduzir o viés de estudantes com históricos muito longos. Entender a distribuição real de tamanhos é essencial para avaliar o impacto dessa decisão.

**Hipótese:** A mediana de tentativas por estudante por assignment deve estar abaixo de 50 (truncagem afeta apenas a cauda). A proporção de (estudante, assignment) com seq_len > 50 deve ser < 30%.

**Referência:** Shi et al. (2022) — Section 3, "We truncate student sequences to the last 50 attempts".

Calculado em: `01_eda.ipynb` — Seção 4.2, célula de código (estatísticas de `seq_len`) e célula markdown seguinte.

**Distribuição global (Release/Train, Run.Program, 1.134 pares estudante × assignment):**

| Estatística | Valor |
|---|---|
| count | 1.134 |
| min | 1 |
| P25 | 17 |
| mediana (P50) | **32** |
| P75 | 53 |
| P90 | 83,7 |
| P95 | **109,3** |
| P99 | 154 |
| max | **272** |
| média (±dp) | 41,3 (±32,9) |

Pares (estudante, assignment) com seq_len > 50: **321 de 1.134 (28,3%)**  
Estudantes com ≥ 1 assignment afetado: **143 de 246 (58,1%)**

**Por assignment:**

| Assignment | Estudantes | seq_len > 50 | % afetados | Mediana | P95 | Máx |
|---|---|---|---|---|---|---|
| A1 (439) | 233 | 56 | 24,0% | 30 | 88 | 155 |
| A2 (487) | 224 | 81 | 36,2% | 42 | 110 | 224 |
| A3 (492) | 234 | 92 | **39,3%** | 38 | 135 | **272** |
| A4 (494) | 221 | 54 | 24,4% | 34 | 91 | 130 |
| A5 (502) | 222 | 38 | **17,1%** | 24 | 88 | 144 |

**Achado:** A distribuição de tamanho de sequência (Release/Train, Run.Program) é assimétrica à direita: mediana = **32 tentativas**, média = **41,3 (±32,9)**, P95 = **109,3**, máximo = **272**. **28,3% dos pares** (estudante, assignment) têm seq_len > 50, afetando **58,1% dos estudantes** (143 de 246) em ao menos um assignment. A3 (492) é o mais afetado (39,3%, mediana 38); A5 (502) o menos (17,1%, mediana 24).

**Implicação para modelagem:** A truncagem em 50 tentativas é conservadora para a maioria dos estudantes (mediana global em 32, abaixo do limite). Para os 28,3% de pares afetados, descartar as tentativas mais antigas preserva o estado de habilidade mais recente — o mais informativo para prever a próxima tentativa. A decisão de Shi et al. (2022) é reproduzida sem modificação.

### 2.2 — Impacto da Truncagem nas Sequências (Preprocessing)

**Contexto:** Após a construção das sequências via `build_sequences`, a função `truncate_sequences` aplica o corte nas últimas 50 tentativas. O impacto difere entre BKT/DKT (apenas `Run.Program`) e Code-DKT (inclui `Compile.Error`), pois a adição de `Compile.Error` aumenta o comprimento médio das sequências.

**Referência:** Shi et al. (2022); Pankiewicz, Shi & Baker (2025).

Calculado em: `02_preprocessing.ipynb` — Seção 4.1, célula de código (tabelas de truncagem) e célula markdown seguinte.

**BKT/DKT (apenas Run.Program):**

| AssignmentID | Sequências | Truncadas | % truncadas | Len média (antes) | Len média (depois) |
|---|---|---|---|---|---|
| 439 | 233 | 56 | 24,0% | 37,6 | 31,8 |
| 487 | 224 | 81 | 36,2% | 47,0 | 35,8 |
| 492 | 234 | 92 | 39,3% | 51,2 | 33,6 |
| 494 | 221 | 54 | 24,4% | 38,8 | 32,8 |
| 502 | 222 | 38 | 17,1% | 31,4 | 26,8 |

**Code-DKT (Run.Program + Compile.Error):**

| AssignmentID | Sequências | Truncadas | % truncadas | Len média (antes) | Len média (depois) |
|---|---|---|---|---|---|
| 439 | 233 | 134 | **57,5%** | 86,0 | 40,6 |
| 487 | 224 | 151 | **67,4%** | 87,0 | 43,1 |
| 492 | 234 | 140 | **59,8%** | 92,3 | 39,5 |
| 494 | 221 | 124 | 56,1% | 70,6 | 40,1 |
| 502 | 222 | 78 | 35,1% | 49,4 | 32,8 |

Taxa de corretos após truncagem (Release/Train, todos os assignments):

| Modelo | Antes truncagem | Após truncagem | Δ |
|---|---|---|---|
| BKT/DKT | 23,70% | **27,97%** | +4,27pp |
| Code-DKT | 12,66% | **19,87%** | +7,21pp |

**Achado:** A truncagem afeta BKT/DKT em 17–39% das sequências por assignment; no Code-DKT, a adição de `Compile.Error` infla o comprimento médio (86–92 eventos antes da truncagem vs 31–51 no BKT/DKT), fazendo com que 35–67% das sequências sejam truncadas. A taxa de corretos **aumenta após a truncagem** porque os eventos mais recentes refletem o aprendizado acumulado (fase pós-familiarização, menor taxa de erros). A flag `is_first_attempt` é recalculada corretamente na janela truncada — a assertion `(first_counts == 1).all()` passa em todos os assignments e modelos.

**Implicação para modelagem:** A truncagem não distorce a métrica first-attempt AUC (calculada sobre `is_first_attempt`, recalculado na janela truncada). O efeito principal é reduzir o custo de memória do LSTM (sequências ≤ 50) e eliminar o viés de estudantes com históricos muito longos. Os artefatos serializados (`results/sequences_bkt_dkt.pkl` e `results/sequences_code_dkt.pkl`) já incorporam a truncagem — os notebooks 04–06 carregam diretamente.

---

## 3 — Perfis de Estudante

### 3.1 — Clustering Exploratório (K-Means, k=3)

**Contexto:** Identificar grupos naturais de estudantes com base em taxa de acerto eventual, número médio de tentativas por assignment e nota final (X-Grade) é essencial para avaliar se os modelos KT precisam capturar heterogeneidade estrutural ou se um modelo único por assignment é suficiente. O BKT com parâmetros compartilhados por KC não distingue perfis de estudante; DKT e Code-DKT capturam implicitamente a heterogeneidade via estado oculto do LSTM.

**Hipótese:** Esperamos encontrar ao menos dois clusters bem definidos (alto vs baixo desempenho) com silhouette > 0,3. A heterogeneidade deve se manifestar na taxa de acerto eventual e no número de tentativas.

**Referência:** Shi et al. (2022) — protocolo de avaliação por assignment; Abdelrahman et al. (2022) — survey KT.

Calculado em: `01_eda.ipynb` — Seção 2.3, células de código (K-Means com k=3, SEED=42) e célula markdown seguinte (célula 54).

**K-Means k=3, SEED=42, 453 estudantes com features completas** (53 excluídos por features faltantes):

Silhouette scores por k:
- k=2: **0,285** (máximo observado)
- k=3: **0,237** (escolhido pela interpretabilidade do perfil intermediário)
- k=4: < 0,237

| Perfil | N | % turma | X-Grade médio | Taxa acerto eventual | Tentativas médias/assignment |
|---|---|---|---|---|---|
| **Alto desempenho** | 139 | **30,7%** | **73,8** | 94–99% | 4,4–10,9 |
| **Médio** | 66 | 14,6% | 64,9 | 56–89% (mínimo em A492) | 5,1–9,7 |
| **Em risco** | 248 | **54,7%** | 55,9 | 97–99% (inesperadamente alto) | **2,0–4,6** (muito baixo) |

**Achado:** K-Means com k=3 (SEED=42) sobre 453 estudantes revela três perfis ordenados por X-Grade médio. O silhouette score favorece k=2 (0,285) sobre k=3 (0,237), mas k=3 é preferido pela interpretabilidade do perfil intermediário. Resultado inesperado: o cluster "Em risco" (54,7% da turma) apresenta taxas de acerto eventual tão altas quanto o "Alto desempenho" (~97–99%), mas número médio de tentativas muito menor (2,0–4,6/assignment). O cluster "Médio" é o que exibe menor taxa de acerto eventual (56–89%) e mais tentativas — padrão de dificuldade persistente real. O perfil "Em risco" (X-Grade médio 55,9) parece representar estudantes com **baixo engajamento** (poucos problemas tentados), não estudantes que erram muito.

**Implicação para modelagem:** A heterogeneidade não se organiza na estrutura esperada (dificuldade ↔ tentativas ↔ grade). O perfil "Em risco" evidencia que baixo engajamento é o padrão dominante (54,7%), não dificuldade persistente. O DKT e Code-DKT, ao modelar sequências individualizadas, capturam implicitamente esse comportamento; o BKT com parâmetros compartilhados por KC não diferencia engajamento seletivo de baixa maestria. Silhouette < 0,30 confirma fronteiras suaves entre perfis — o KT deve modelar um **contínuo de habilidades**, não grupos discretos. Em assignments com poucos estudantes ou sequências curtas (e.g., A5 com mediana de apenas 24 tentativas), o BKT pode ter vantagem por ser mais simples e menos suscetível a overfitting.

### 3.2 — Participação e Dropout por Assignment

**Contexto:** Dropout ao longo do semestre reduz o número de estudantes avaliáveis nos assignments finais, podendo introduzir viés de seleção (os estudantes que persistem até A5 podem ser os de maior desempenho).

**Referência:** Shi et al. (2022) — avaliação por assignment.

Calculado em: `01_eda.ipynb` — Seção 1.1.3, célula de código (participação por assignment) e célula markdown seguinte (célula 14).

| Assignment | Estudantes (All/Data, 506 total) | % participação |
|---|---|---|
| A1 (439) | 499 | 98,8% |
| A2 (487) | 487 | 96,2% |
| A3 (492) | 478 | 94,5% |
| A4 (494) | 477 | 94,3% |
| A5 (502) | 476 | **94,1%** |

89,9% dos estudantes (455/506) participaram de todos os 5 assignments. Dropout total ao longo do semestre: ~4,7pp (98,8% → 94,1%).

**Achado:** O dropout ao longo do semestre é moderado (~4,7pp de A1 para A5) e afeta principalmente os estudantes com pior desempenho (o "Em risco" cluster). **89,9% dos estudantes** completaram todos os 5 assignments, confirmando que o dataset é adequado para treinamento por assignment sem ajuste especial por dropout. No split Release/Train (246 estudantes), a participação por assignment varia de 221 (A4) a 234 (A3) estudantes.

**Implicação para modelagem:** O dropout moderado não invalida o protocolo de treinamento por assignment. Os notebooks 04–06 devem reportar o número de estudantes por assignment (não assumir que todos os 246 estudantes participaram de todos os assignments). Para Release/Test, apenas 3 assignments têm sequências disponíveis (A439, A487, A492) — A494 e A502 têm 0 sequências no split de teste, comportamento consistente com Shi et al. (2022).

---

## Resumo Executivo — Decisões para Notebooks 03–07

| Achado | Valor | Impacto |
|---|---|---|
| Imbalance global BKT/DKT | 3,22:1 (23,70% corretos) | Usar AUC como métrica primária |
| Imbalance máximo por assignment | 4,24:1 em A3 (19,07% corretos) | Cautela ao interpretar AUC de A3 |
| Imbalance Code-DKT (pré-truncagem) | ~7:1 (12,66% corretos) | AUC indispensável; não usar acurácia |
| Mediana de sequências (BKT/DKT) | 32 tentativas | Truncagem em 50 conservadora para maioria |
| % pares afetados pela truncagem | 28,3% (BKT/DKT) / 35–67% (Code-DKT) | Code-DKT mais afetado por Compile.Error |
| Taxa corretos após truncagem | 27,97% (BKT/DKT) / 19,87% (Code-DKT) | Divergência esperada — eventos recentes têm mais acertos |
| Perfis de estudante (k=3) | 30,7% alto / 14,6% médio / 54,7% em risco | Modelar contínuo, não grupos discretos |
| Dropout A1→A5 | ~4,7pp (89,9% completaram todos) | Não requer ajuste especial por dropout |
| Compile.Error rate (Release/Train) | 46,6% das submissões Code-DKT | Sinal preditivo ρ=−0,569 com Label |
