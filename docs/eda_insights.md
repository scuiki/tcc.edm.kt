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

## 4 — Implicações das Decisões de Pré-processamento

### 4.1 — Por que Compile.Error entra no Code-DKT (mas não em BKT nem DKT)

**Contexto:** O pipeline de pré-processamento mantém dois protocolos de filtragem distintos: `filter_for_bkt_dkt` retém apenas eventos `Run.Program`; `filter_for_code_dkt` adiciona `Compile.Error` com `correct=0`. A justificativa para essa assimetria é arquitetural: o Code-DKT incorpora features do código-fonte a cada passo da sequência LSTM. BKT e DKT padrão recebem apenas pares `(ProblemID, correct)` — sem acesso ao código — e portanto não têm mecanismo para processar o estado sintático de uma submissão não-compilável.

**Hipótese:** A inclusão de `Compile.Error` deve aumentar o sinal preditivo do Code-DKT em relação ao DKT padrão, pois esses eventos carregam informação sobre o processo de depuração do estudante (estado intermediário do código antes da execução bem-sucedida). O custo é o aumento do imbalance: `Compile.Error` contribui exclusivamente com `correct=0`.

**Referência:** Shi et al. (2022) — Code-DKT original exige código compilável, descarta `Compile.Error`; Pankiewicz, Shi & Baker (2025) — srcML-DKT inclui `Compile.Error` com `correct=0` e features srcML.

Calculado em: `02_preprocessing.ipynb` — Seção 2.1, célula `filter_for_bkt_dkt` / `filter_for_code_dkt` (assertions de EventType e contagem por tipo).

**Por que srcML habilita a inclusão de Compile.Error:**
O Code-DKT original (Shi et al., 2022) extraía features de código via `javalang`, que requer código **sintaticamente válido** — submissões com erro de compilação não são parseáveis e eram descartadas. O srcML-DKT (Pankiewicz et al., 2025) demonstrou que o parser srcML consegue extrair estrutura parcial de código Java não-compilável, representando-o como XML com marcações de erro. Com srcML, a mesma arquitetura LSTM + atenção do Code-DKT recebe features mesmo dos `Compile.Error`, viabilizando sua inclusão na sequência.

**Impacto quantitativo no CSEDM Release/Train:**

| Protocolo | Eventos totais | Run.Program | Compile.Error | Taxa corretos |
|-----------|---------------|-------------|---------------|---------------|
| BKT/DKT (apenas Run.Program) | 46.825 | 46.825 (100%) | 0 | **23,70%** |
| Code-DKT (Run.Program + Compile.Error) | 87.683 | 46.825 (53,4%) | 40.858 (46,6%) | **12,66%** |

Os 40.858 eventos `Compile.Error` (46,6% do total Code-DKT) contribuem **exclusivamente** com `correct=0`, reduzindo a taxa de corretos de 23,70% para 12,66%.

**Achado:** O imbalance no Code-DKT (~7:1 antes da truncagem, ~4:1 após) é consideravelmente maior que no BKT/DKT (~3:1). A justificativa empírica para aceitar esse custo é a correlação de Spearman ρ = −0,569 entre `n_compile_errors` e Label (`01_eda.ipynb`, Seção 8.1) — os eventos de compilação com erro carregam sinal preditivo relevante sobre o desempenho final do estudante. A justificativa teórica é que o processo de depuração (sequência de Compile.Error → eventual Run.Program correto) reflete a trajetória de aprendizado, e o srcML consegue capturar essa evolução sintática mesmo em código inválido.

**Implicação para modelagem:** BKT e DKT usam `sequences_bkt_dkt.pkl` (artefato sem `Compile.Error`); Code-DKT usa `sequences_code_dkt.pkl` (inclui `Compile.Error`). Os notebooks 04–06 **não devem** misturar esses artefatos. A first-attempt AUC permanece comparável entre modelos porque é calculada sobre `is_first_attempt` (primeira tentativa de `Run.Program` por problema) — os `Compile.Error` afetam o contexto histórico do LSTM mas não entram diretamente no conjunto de avaliação.

---

### 4.2 — Justificativa do Threshold Score == 1.0

**Contexto:** O Score do CSEDM não é puramente binário — cada `Run.Program` produz um Score contínuo em [0, 1] correspondente à fração de testes automatizados que passaram. A escolha do threshold para converter em label binário (`correct = 1` ou `correct = 0`) afeta diretamente a definição de "acerto" no problema de KT.

**Hipótese:** A distribuição do Score deve ser trimodal (concentrada em 0, em 1 e com pico em scores parciais de alto valor), com ~34–37% de scores parciais. O threshold `Score == 1.0` deve capturar apenas execuções onde o estudante passou em **todos** os testes — um critério claro de maestria do problema.

**Referência:** Shi et al. (2022) — Section 3.1, "`correct=1` when all tests pass"; Price et al. (2020) — ProgSnap2 v6, definição de Score como fração de testes passados.

Calculado em: `01_eda.ipynb` — Seção 5.1, célula de código (distribuição de Score em Release/Train) e célula markdown seguinte (célula 72).

**Distribuição do Score (Release/Train, 46.825 Run.Program):**

| Categoria | Contagem | % total |
|-----------|----------|---------|
| Score = 0.0 (falhou todos os testes) | 19.802 | **42,3%** |
| 0 < Score < 1 (acerto parcial) | 15.925 | **34,0%** |
| Score = 1.0 (passou todos os testes) | 11.098 | **23,7%** |
| **Total** | **46.825** | **100%** |

Valores únicos de Score: 200 — todos correspondem a frações racionais discretas (e.g., 3/11 ≈ 0,273; 1/2 = 0,500; 6/7 ≈ 0,857), confirmando que o Score reflete contagem de testes com resolução por assignment.

**Raciocínio analítico para Score == 1.0:**

1. **Separação natural de classes:** A distribuição é trimodal com massa clara em 0 e 1. Não há threshold intermediário óbvio entre 0 e 1 que seja justificável sem conhecimento das rúbricas de cada assignment.

2. **Consistência com o conceito de maestria:** KT modela a probabilidade de o estudante *dominar* o conhecimento (KC). Passar 6/7 testes pode refletir um detalhe específico não dominado — usar Score < 1.0 como `correct=1` introduziria ruído em vez de sinal de maestria.

3. **Reprodutibilidade:** Shi et al. (2022) adotam explicitamente `Score == 1.0` como `correct = 1`. Usar o mesmo threshold garante que os 23,70% de corretos em Release/Train correspondam exatamente ao benchmark de 23,68% do paper (divergência < 0,02pp).

4. **Impacto dos parciais:** Os 34,0% de scores parciais são classificados como `correct=0`. Essa perda de granularidade é o custo da binarização — mas é necessária porque BKT, DKT e Code-DKT modelam distribuições Bernoulli.

**Achado:** A distribuição do Score em Release/Train é trimodal: 42,3% em 0,0; 23,7% em 1,0; 34,0% parciais (200 valores únicos). O threshold `Score == 1.0` é o único ponto naturalmente justificado pela semântica dos testes automatizados (passou/falhou todos). Scores parciais representam execuções onde subconjuntos de casos de teste passaram — tratados como `correct=0` por ausência de maestria completa.

**Implicação para modelagem:** O threshold `Score == 1.0` é aplicado uniformemente nos três modelos (BKT, DKT e Code-DKT). Para o Code-DKT, os eventos `Compile.Error` são sempre `correct=0` por definição (código não executou), sem necessidade de threshold. A coluna `correct` nos artefatos serializados já incorpora essa decisão — notebooks 04–06 não precisam re-implementar o threshold.

---

### 4.3 — Rationale para Usar Release/ em vez de All/

**Contexto:** O CSEDM oferece dois semestres distintos: `All/` (Fall 2019, set–dez, 506 estudantes) e `Release/` (Spring 2019, fev–mai, 246 train + 83 test = 329 estudantes). Para TCC 1, o objetivo é **replicar** os resultados de Shi et al. (2022) (Table 1 e Table 2); a escolha do split é crítica para que a comparação seja válida.

**Hipótese:** O split `Release/` deve reproduzir o benchmark de 23,68% de corretos do paper. As populações de `All/` e `Release/` não se sobrepõem — usar `All/` produziria resultados não comparáveis com a literatura.

**Referência:** Shi et al. (2022) — "We use the CSEDM dataset (Spring 2019)"; Price et al. (2020) — ProgSnap2 v6, documentação dos splits.

Calculado em: `01_eda.ipynb` — Seção 1.1.4 (consistência entre splits, células 16–18) e Seção 1.2.3 (benchmark de reprodutibilidade); `02_preprocessing.ipynb` — Seção 1.2 (benchmark, células `a41fa13b`).

**Comparação direta entre splits:**

| Característica | All/ (Fall 2019) | Release/ (Spring 2019) |
|----------------|------------------|------------------------|
| Semestre | set–dez 2019 | fev–mai 2019 |
| Estudantes (train) | — | **246** |
| Estudantes (test) | — | **83** |
| Estudantes totais | **506** | **329** |
| Sobreposição de SubjectIDs | 0 (populações distintas) | 0 (populações distintas) |
| Taxa corretos (Run.Program) | 19,65% | **23,70%** |
| Benchmark paper Shi et al. (2022) | — | **23,68%** (divergência < 0,02pp) |
| Assignments com dados em test | — | **3 de 5** (A439, A487, A492) |

**Três razões para usar Release/ em vez de All/:**

1. **Reprodutibilidade:** A taxa de 23,70% de corretos em `Release/Train` reproduz o benchmark de 23,68% de Shi et al. (2022) com divergência < 0,02pp (arredondamento). Usar `All/` produziria 19,65% — diferença de 4,05pp que evidencia populações distintas.

2. **Separação de populações:** Os 506 SubjectIDs de `All/` e os 329 de `Release/` são completamente distintos (0 sobreposição, confirmado em `01_eda.ipynb`, Seção 1.1.4). Não há como misturar os splits sem violar a integridade do protocolo experimental.

3. **Protocolo de avaliação:** O paper avalia nos assignments presentes em `Release/Test` (A439, A487, A492). O split `All/Test` não contém as mesmas divisões de estudantes e assignments — um modelo treinado em `All/Train` e avaliado em `All/Test` não é comparável com os resultados de Table 1 do paper.

**Achado:** `Release/` e `All/` têm populações completamente distintas (0 sobreposição de SubjectIDs) e taxas de corretos significativamente diferentes (23,70% vs 19,65%). O benchmark de reprodutibilidade do paper (23,68%) é replicado em `Release/Train` com divergência < 0,02pp — confirmando que Shi et al. (2022) usaram exatamente este split. Usar `All/` produziria resultados não comparáveis com a literatura.

**Implicação para modelagem:** Todos os notebooks de modelagem (04–06) carregam os artefatos `sequences_bkt_dkt.pkl` e `sequences_code_dkt.pkl`, que já usam exclusivamente `Release/Train` (treino) e `Release/Test` (avaliação). O split `All/` é mantido disponível no `data_loader.py` apenas para EDA exploratória. A comparação de performance com Shi et al. (2022) Table 1 e Table 2 é válida apenas nos 3 assignments com dados em `Release/Test` (A439, A487, A492).

---

## 5 — Recomendações para Notebooks 03–07

### 5.1 — Sinalizações de Risco por Assignment

**Contexto:** Antes de implementar os notebooks de modelagem (04–06), é essencial mapear os riscos operacionais por assignment: desequilíbrio extremo de classes, conjunto de treinamento reduzido, alta taxa de `Compile.Error` e disponibilidade de dados no split de avaliação. Esses fatores determinam configurações específicas de regularização, métricas prioritárias e o escopo de comparação com o paper de referência.

**Hipótese:** A3 (492) deve concentrar os maiores riscos por imbalance; A2 (487) deve apresentar risco alto por imbalance combinado com alta taxa de truncagem no Code-DKT; A5 (502) deve ter menor risco global. A4 e A5 são invisíveis para comparação com Shi et al. (2022) por não terem dados em Release/Test.

**Referência:** Shi et al. (2022); Pankiewicz, Shi & Baker (2025).

Fontes: taxa de corretos e imbalance da Seção 1.1 (01_eda.ipynb); CE rate da Seção 6.1 (01_eda.ipynb, valores calculados); truncagem da Seção 2.2 (02_preprocessing.ipynb); disponibilidade de Release/Test da Seção 1.2 (01_eda.ipynb) e Seção 5 (02_preprocessing.ipynb).

| Assignment | Estudantes (train) | Imbalance BKT/DKT | Taxa corretos | CE rate | Truncagem Code-DKT | Release/Test | Risco |
|---|---|---|---|---|---|---|---|
| **A1 (439)** | 233 | 2,67:1 | 27,3% | **56,3%** | 57,5% | ✓ Disponível | Moderado |
| **A2 (487)** | 224 | **3,92:1** | 20,3% | 45,9% | **67,4%** | ✓ Disponível | **Alto** |
| **A3 (492)** | 234 | **4,24:1** | **19,1%** | 44,5% | 59,8% | ✓ Disponível | **Alto** |
| A4 (494) | **221** | 2,96:1 | 25,2% | 45,0% | 56,1% | ✗ Sem dados | Moderado |
| A5 (502) | 222 | 2,29:1 | 30,4% | 36,5% | 35,1% | ✗ Sem dados | Baixo |

**Achado:** Três sinalizações de risco principais emergem da análise combinada:

1. **Imbalance extremo — A3 (492) e A2 (487):** A3 tem o maior desequilíbrio (4,24:1, apenas 19,1% de corretos) e A2 é o segundo pior (3,92:1, 20,3%). Em ambos, DKT e BKT podem colapsar para prever sempre `correct=0` sem nenhum poder discriminativo — AUC ≈ 0,5 indicaria colapso de classe.

2. **Alta CE rate combinada com truncagem máxima — A1 (439) e A2 (487):** A1 tem a maior CE rate (56,3%), indicando que mais da metade das submissões de A1 são `Compile.Error`. A2 combina CE rate moderada (45,9%) com a maior taxa de truncagem no Code-DKT (67,4%) — a janela de 50 eventos captura menos de metade do histórico médio (87,0 eventos antes da truncagem), com potencial perda de contexto inicial relevante.

3. **Ausência de Release/Test — A4 (494) e A5 (502):** Os dois assignments finais do semestre não têm sequências de avaliação no split de teste. Os modelos podem ser treinados e validados internamente (cross-validation no treino), mas os resultados não são comparáveis com Shi et al. (2022) Table 1 e Table 2.

**Implicação para modelagem:** Os notebooks 04–06 devem: (a) reportar resultados separados por assignment com número de estudantes e taxa de corretos; (b) incluir verificação de colapso de classe antes de interpretar AUC < 0,60 em A2/A3; (c) limitar a comparação com o paper aos assignments A1, A2 e A3 (Release/Test disponível). A4 e A5 servem como validação interna via cross-validation apenas.

---

### 5.2 — Notebook 03: Code Features e Extração de ASTs (srcML)

**Contexto:** O notebook 03 extrai features de código-fonte via srcML para alimentar o Code-DKT. Cada evento na sequência (tanto `Run.Program` quanto `Compile.Error`) precisa de um vetor de features extraído do `CodeState` associado. A arquitetura do Code-DKT usa embeddings de caminhos AST (code2vec): `pr = (nó_início, caminho_textual, nó_fim)`, dimensão 300, com mecanismo de atenção.

**Hipótese:** A maior dificuldade operacional será o parsing de código não-compilável (eventos `Compile.Error`), especialmente em A1 (CE rate 56,3%) e A2 (45,9%), onde a proporção de submissões não-compiláveis é mais alta. O notebook deve implementar cache por `CodeStateID` para evitar re-parsear o mesmo estado de código (937 CodeStateIDs únicos por problema em média — Seção 6.2 do EDA).

**Referência:** Shi et al. (2022) — code2vec embeddings, dimensão 300; Pankiewicz, Shi & Baker (2025) — srcML sobre código não-compilável, fallback para estados com parsing parcial.

**Decisões de implementação ancoradas na EDA:**

1. **Cache por `CodeStateID`:** A Seção 6.2 (`01_eda.ipynb`) reporta 100% de sobreposição entre os CodeStateIDs de `Compile.Error` e `Run.Program` — estados de código com erro de compilação coincidem com estados submetidos por outros estudantes. Um único dicionário `{CodeStateID: vetor_features}` serve para todos os eventos de todos os assignments. Artefato de saída: `results/code_features.pkl`.

2. **Fallback para parsing incompleto:** srcML pode retornar XML com tags de erro para código muito incompleto ou com encoding inválido. Implementar fallback para vetor zero com flag `parsing_failed=True`; reportar taxa de fallback por assignment — se > 1% dos eventos de qualquer assignment, investigar antes de prosseguir.

3. **Volume por assignment:** A3 (492) tem o maior volume de eventos Code-DKT antes da truncagem (média 92,3 eventos × 234 estudantes ≈ 21.600 eventos). Processar em lote por assignment para evitar pico de memória no srcML.

4. **A4 e A5 incluídos:** Extrair features para todos os 5 assignments apesar de A4/A5 não terem Release/Test. Os artefatos de sequência (`sequences_code_dkt.pkl`) cobrem todos os assignments.

---

### 5.3 — Notebooks 04–05: BKT e DKT

**Contexto:** BKT e DKT usam exclusivamente `sequences_bkt_dkt.pkl` (sem `Compile.Error`). O protocolo de Shi et al. (2022) treina um modelo por assignment com KC = ProblemID. A avaliação primária é first-attempt AUC; a secundária é all-attempts AUC. Com 10 KCs por assignment, o BKT tem 40 parâmetros por assignment (4 parâmetros × 10 KCs) — naturalmente regularizado. O DKT (LSTM hidden=200, como em Shi et al.) tem ordens de grandeza mais parâmetros.

**Hipótese:** BKT deve ter performance inferior ao DKT em A2 e A3 (maior imbalance, padrões temporais mais complexos). Em A5 (mediana 24 tentativas, menor imbalance), o BKT pode ser competitivo por ser mais simples e menos suscetível a overfitting em sequências curtas.

**Referência:** Shi et al. (2022) — Table 1 (first-attempt AUC): BKT A1≈0.714, DKT A1≈0.730; Abdelrahman et al. (2022) — parâmetros BKT e treinamento LSTM DKT.

**Decisões de implementação por assignment:**

| Assignment | Benchmarks esperados (Shi et al.) | Configuração específica | Justificativa (EDA) |
|---|---|---|---|
| **A1 (439)** | BKT ~0.714 / DKT ~0.730 | Benchmark primário; reportar AUC first-attempt vs paper | Release/Test disponível; imbalance moderado (2,67:1); 233 estudantes |
| **A2 (487)** | A2 disponível em Release/Test | Monitorar colapso de classe; aplicar `pos_weight` no BCELoss | Imbalance 3,92:1; apenas 2.141 corretos em 10.539 tentativas |
| **A3 (492)** | A3 disponível em Release/Test | Monitorar colapso; reportar IC do AUC (bootstrap) | Imbalance máximo 4,24:1; 19,07% corretos; maior % truncagem (39,3%) |
| **A4 (494)** | Sem benchmark externo | Cross-validation interna apenas | Sem dados em Release/Test; menor número de estudantes (221) |
| **A5 (502)** | Sem benchmark externo | Dropout mais agressivo no DKT (0,3–0,5) | Sem Release/Test; menor imbalance (2,29:1); mediana curta (24 tentativas); BKT pode ser competitivo |

**Configurações técnicas obrigatórias:**
- `SEED = 42` em todos os notebooks (reprodutibilidade)
- `pos_weight = n_incorretos / n_corretos` por assignment no `nn.BCEWithLogitsLoss` do DKT — particularmente importante para A2 (3,92:1) e A3 (4,24:1)
- 10-fold cross-validation sobre Release/Train para seleção de hiperparâmetros; reportar AUC por fold
- Célula de verificação de colapso de classe antes do treinamento: se a loss converge para `−log(1−p)` com `p ≈ 0` (sempre prevendo incorreto), aplicar `pos_weight` e re-treinar
- Avaliação final em Release/Test apenas para A1, A2, A3

---

### 5.4 — Notebook 06: Code-DKT (srcML-DKT)

**Contexto:** O Code-DKT usa `sequences_code_dkt.pkl` (inclui `Compile.Error`) e `results/code_features.pkl`. O alvo de reprodutibilidade é first-attempt AUC ≈ 74% em A1 (±2%), replicando Table 1 de Shi et al. (2022) com o protocolo srcML (Pankiewicz et al., 2025).

**Hipótese:** O Code-DKT deve superar o DKT em assignments onde o sinal do código-fonte é mais informativo. Dado que n_compile_errors tem Spearman ρ = −0,569 com Label (`01_eda.ipynb`, Seção 8.1), o ganho deve ser mais pronunciado em A1 (CE rate 56,3%) do que em A5 (CE rate 36,5%).

**Referência:** Shi et al. (2022) — Code-DKT A1: AUC ~74,3%; arquitetura LSTM + atenção sobre embeddings de caminhos AST; Pankiewicz, Shi & Baker (2025) — srcML-DKT com Compile.Error incluso.

**Decisões de implementação ancoradas na EDA:**

1. **A2 (487) — truncagem máxima no Code-DKT (67,4%):** A janela de 50 eventos captura ~57% do histórico médio de A2 (87,0 eventos antes da truncagem). O mecanismo de atenção verá sequências mais curtas em proporção. Se AUC de A2 no Code-DKT divergir do esperado, investigar se o padding ou a janela truncada está distorcendo os pesos de atenção.

2. **A1 (439) — CE rate mais alta (56,3%):** Apesar de ser o assignment mais fácil em termos de imbalance, A1 tem a maior proporção de Compile.Error. O Code-DKT deve se beneficiar mais desse sinal em A1 — o ganho sobre DKT padrão deve ser mais pronunciado em A1 do que em A5.

3. **Imbalance no Code-DKT (19,87% corretos após truncagem):** O mecanismo de atenção opera sobre vetores de código, não sobre labels — o imbalance afeta a função de loss. Calcular `pos_weight` com os valores do protocolo Code-DKT (não do BKT/DKT), pois as taxas de corretos diferem (19,87% vs 27,97% após truncagem).

4. **Alerta de reprodutibilidade:** O Code-DKT original (Shi et al., 2022) descartava `Compile.Error` (usava javalang). A versão srcML-DKT os inclui. Se o AUC em A1 ficar fora da faixa ±2% do target 74%, documentar a divergência e comparar com Pankiewicz et al. (2025), que usa o mesmo protocolo srcML.

5. **Padding e máscara de atenção:** O dataloader deve usar `collate_fn` com padding de zeros para sequências com menos de 50 eventos. O mecanismo de atenção deve receber máscara de padding para ignorar posições artificiais. `SEED=42` no DataLoader (shuffle com generator fixo).

---

### 5.5 — Notebook 07: Comparação Final e Análise Estatística

**Contexto:** O notebook 07 consolida os resultados de BKT, DKT e Code-DKT e responde à questão central do TCC 1: qual modelo é mais adequado como base para o TCC 2? A comparação deve ser ancorada em first-attempt AUC (métrica primária) e validada por teste de significância estatística.

**Hipótese:** Code-DKT deve superar BKT e DKT em first-attempt AUC nos 3 assignments com Release/Test (A1, A2, A3), especialmente em A1 (~74% vs ~73% DKT vs ~71% BKT). O teste de Wilcoxon signed-rank deve confirmar a significância em pelo menos A1 considerando os 10 folds de cross-validation.

**Referência:** Shi et al. (2022) — Table 1 (first-attempt AUC) e Table 2 (all-attempts AUC); Abdelrahman et al. (2022) — protocolo de comparação e métricas de KT.

**Decisões de análise ancoradas na EDA:**

1. **Escopo de comparação com o paper:** Reportar BKT vs DKT vs Code-DKT APENAS para A1 (439), A2 (487) e A3 (492). Para A4 e A5, reportar resultados de cross-validation interna sem comparação com benchmarks externos.

2. **Interpretação de A3 (492) com cautela especial:** A3 tem o maior imbalance (4,24:1) e a faixa de AUC esperada é mais estreita. Reportar o intervalo de confiança de AUC (bootstrap 1000 iterações ou desvio-padrão dos 10 folds) para A3. AUC < 0,60 em A3 deve ser acompanhada de verificação de colapso de classe antes de ser interpretada como má performance do modelo.

3. **Teste Wilcoxon signed-rank:** Usar os AUCs por fold (10 folds × 3 assignments comparáveis = 30 pares) ou por assignment como amostras pareadas. Com n=3 assignments comparáveis, o poder estatístico é limitado — reportar p-value sem afirmar conclusividade forte.

4. **Engajamento seletivo vs aprendizado:** O cluster "Em risco" (54,7% dos estudantes, Seção 3.1) apresenta baixo engajamento (2,0–4,6 tentativas/assignment), não dificuldade persistente. Esses estudantes têm sequências mais curtas — um modelo KT com poucas observações por estudante tende a ser menos preciso. Considerar reportar AUC separadamente para sequências curtas (seq_len < 10) vs longas (seq_len ≥ 10) como análise complementar.

5. **Justificativa final para TCC 2:** A escolha do modelo base deve ser baseada em: (a) first-attempt AUC mais alta nos assignments com Release/Test; (b) magnitude do gap entre modelos; (c) extensibilidade para TCC 2 — o Code-DKT com srcML é diretamente extensível para análise semântica de código e integra `Compile.Error`, o que representa a direção mais promissora para sistemas adaptativos de programação.

---

## Resumo Executivo — Decisões para Notebooks 03–07

| Achado | Valor | Impacto |
|---|---|---|
| Imbalance global BKT/DKT | 3,22:1 (23,70% corretos) | Usar AUC como métrica primária |
| Imbalance máximo por assignment | 4,24:1 em A3 (19,07% corretos) | Cautela ao interpretar AUC de A3; verificar colapso de classe |
| Imbalance Code-DKT (pré-truncagem) | ~7:1 (12,66% corretos) | AUC indispensável; não usar acurácia |
| Mediana de sequências (BKT/DKT) | 32 tentativas | Truncagem em 50 conservadora para maioria |
| % pares afetados pela truncagem | 28,3% (BKT/DKT) / 35–67% (Code-DKT) | Code-DKT mais afetado por Compile.Error |
| Taxa corretos após truncagem | 27,97% (BKT/DKT) / 19,87% (Code-DKT) | Divergência esperada — eventos recentes têm mais acertos |
| Perfis de estudante (k=3) | 30,7% alto / 14,6% médio / 54,7% em risco | Modelar contínuo, não grupos discretos |
| Dropout A1→A5 | ~4,7pp (89,9% completaram todos) | Não requer ajuste especial por dropout |
| Compile.Error rate global (Release/Train) | 46,6% das submissões Code-DKT | Sinal preditivo ρ=−0,569 com Label |
| CE rate A1 / A2 / A3 / A4 / A5 | 56,3% / 45,9% / 44,5% / 45,0% / 36,5% | A1 tem mais CE que qualquer outro assignment; ver Seção 5.1 |
| Assignments sem Release/Test | A4 (494) e A5 (502) | Cross-validation interna apenas; não comparar com Shi et al. (2022) |
| Risco alto por assignment | A2 (3,92:1 + 67,4% truncagem Code-DKT) e A3 (4,24:1) | pos_weight obrigatório no BCELoss; ver Seção 5.3 e 5.4 |
