# EDA Insights — Síntese Pós-EDA e Pré-processamento

Síntese dos achados críticos dos notebooks `01_eda.ipynb` e `02_preprocessing.ipynb`.  
Cada seção reporta valores calculados diretamente a partir dos dados, com referência explícita à célula do notebook de origem. Este documento alimenta as decisões de modelagem dos notebooks 03–07.

Dataset utilizado: **CSEDM Spring 2019** (`data/CSEDM/MainTable.csv`), 413 estudantes brutos, 50 problemas, 5 assignments, 201.570 eventos.

- **EDA descritiva** (Seções 1, 2.1, 3, 4): calculada sobre o **Spring 2019 completo** (413 estudantes; 69.627 `Run.Program`), conforme `01_eda.ipynb`.
- **Pré-processamento e sequências** (Seção 2.2): calculado sobre o **train split** após filtro `min_attempts >= 3` e divisão 80/20 (`random_state=1`) → **328 estudantes** de treino / **82** de teste, conforme `02_preprocessing.ipynb`.

A taxa global de corretos do Spring 2019 (`Score == 1.0`) é **23,68%**, reproduzindo exatamente o benchmark de Shi et al. (2022).

---

## 1 — Desbalanceamento de Classes (Imbalance Ratio)

### 1.1 — Imbalance Global e por Assignment

**Contexto:** Com ~76% de tentativas incorretas, o dataset apresenta desbalanceamento moderado (~3:1). Acurácia seria inflada pela classe majoritária — um classificador-baseline "sempre incorreto" atingiria 76,3% de acurácia sem nenhum poder preditivo. AUC (Area Under the ROC Curve) mede a capacidade discriminativa independentemente do threshold de decisão e é a métrica padrão na literatura de KT.

**Hipótese:** O imbalance global deve ser ~3,2:1 (76,3% incorretos / 23,7% corretos); os assignments com menor taxa de acerto (A2 e A3) devem concentrar o maior desequilíbrio e A5 (502) o menor.

**Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

Calculado em: `01_eda.ipynb` — Seção 5.2, célula de código (cálculo do imbalance ratio por assignment) e célula markdown seguinte.  
Artefato visual: `results/sec5_imbalance.png`.

| Assignment | Total | Corretos (n) | Incorretos (n) | % correto | Imbalance ratio |
|---|---|---|---|---|---|
| A1 (439) | 14.614 | 3.821 | 10.793 | 26,15% | 2,82:1 |
| A2 (487) | 15.879 | 3.185 | 12.694 | 20,06% | 3,99:1 |
| A3 (492) | 17.191 | 3.497 | 13.694 | 20,34% | 3,92:1 |
| A4 (494) | 12.402 | 3.066 | 9.336 | 24,72% | 3,05:1 |
| A5 (502) | 9.541 | 2.921 | 6.620 | 30,62% | 2,27:1 |
| **— Global —** | **69.627** | **16.490** | **53.137** | **23,68%** | **3,22:1** |

**Achado:** O Spring 2019 apresenta desbalanceamento global de **3,22:1** (76,3% incorretos vs 23,68% corretos). Por assignment, **A2 (487) tem o maior desequilíbrio** (**3,99:1**, 20,06% correto), seguido de perto por A3 (492) (**3,92:1**, 20,34%); A5 (502) tem o menor (**2,27:1**, 30,62% correto) — consistente com o ranking de dificuldade da Seção 3 do EDA. Um classificador-baseline ("sempre incorreto") atingiria 76,3% de acurácia sem nenhum poder discriminativo, evidenciando que acurácia é inadequada para este problema.

**Implicação para modelagem:** AUC é a métrica primária adotada neste trabalho, seguindo Shi et al. (2022) e Abdelrahman et al. (2022). A métrica secundária (all-attempts AUC) complementa com maior estabilidade estatística. Os dois assignments mais desbalanceados (A2: 3,99:1; A3: 3,92:1) requerem atenção especial durante a avaliação — resultados de AUC abaixo de 0,60 devem ser interpretados com cautela dado o sinal de treinamento mais escasso (~20% de corretos).

### 1.2 — Imbalance no Contexto do Code-DKT (Com Compile.Error)

**Contexto:** Ao incluir eventos `Compile.Error` como `correct=0` (protocolo Code-DKT e srcML-DKT), o imbalance se agrava porque esses eventos contribuem exclusivamente com a classe negativa.

**Referência:** Pankiewicz, Shi & Baker (2025); Shi et al. (2022).

Calculado em: `02_preprocessing.ipynb` — Seção 2.1, célula de código (filtragem `filter_for_code_dkt`).

No train split: 51.338 eventos são `Compile.Error` (de 107.761 submissões totais no protocolo Code-DKT) — **taxa de Compile.Error de 47,6%**. Isso reduz a taxa de corretos de 23,79% (BKT/DKT) para **12,46%** (Code-DKT), resultando em imbalance implícito de ~7:1 no Code-DKT antes da truncagem.

Após truncagem (últimas 50 tentativas por sequência):
- BKT/DKT: taxa de corretos sobe de 23,79% para **28,68%** (+4,89pp)
- Code-DKT: taxa de corretos sobe de 12,46% para **20,27%** (+7,81pp)

**Achado:** O Code-DKT opera com imbalance consideravelmente maior que BKT/DKT (12,46% vs 23,79% de corretos antes da truncagem). Após truncagem, ambos melhoram porque os eventos mais recentes refletem o aprendizado acumulado. A justificativa empírica para incluir `Compile.Error` apesar do imbalance adicional é a correlação de Spearman ρ = −0,564 entre `n_compile_errors` e Label (`01_eda.ipynb`, Seção 8.1) — esses eventos carregam sinal preditivo relevante.

**Implicação para modelagem:** O Code-DKT deve ser avaliado principalmente por first-attempt AUC (não acurácia) para isolar o sinal preditivo do imbalance. A inclusão de `Compile.Error` é justificada empiricamente (correlação com Label) e teoricamente (srcML parseia código não-compilável, Pankiewicz et al., 2025), apesar de agravar o desbalanceamento.

---

## 2 — Distribuição de Sequências e Impacto da Truncagem

### 2.1 — Distribuição de Tamanho de Sequências (BKT/DKT)

**Contexto:** O DKT e o Code-DKT processam sequências de tentativas ordenadas cronologicamente. Shi et al. (2022) truncam cada sequência nas **últimas 50 tentativas** para limitar o custo computacional do LSTM e reduzir o viés de estudantes com históricos muito longos. Entender a distribuição real de tamanhos é essencial para avaliar o impacto dessa decisão.

**Hipótese:** A mediana de tentativas por estudante por assignment deve estar abaixo de 50 (truncagem afeta apenas a cauda). A proporção de (estudante, assignment) com seq_len > 50 deve ser < 30%.

**Referência:** Shi et al. (2022) — Section 3, "We truncate student sequences to the last 50 attempts".

Calculado em: `01_eda.ipynb` — Seção 4.2, célula de código (estatísticas de `seq_len`) e célula markdown seguinte.

**Distribuição global (Spring 2019, Run.Program, 1.708 pares estudante × assignment):**

| Estatística | Valor |
|---|---|
| count | 1.708 |
| min | 1 |
| P25 | 17 |
| mediana (P50) | **31** |
| P75 | 52 |
| P90 | 80 |
| P95 | **108** |
| P99 | 170,9 |
| max | **307** |
| média (±dp) | 40,8 (±34,7) |

Pares (estudante, assignment) com seq_len > 50: **457 de 1.708 (26,8%)**  
Estudantes com ≥ 1 assignment afetado: **216 de 413 (52,3%)**

**Por assignment:**

| Assignment | Estudantes | seq_len > 50 | % afetados | Mediana | P95 | Máx |
|---|---|---|---|---|---|---|
| A1 (439) | 386 | 86 | 22,3% | 30 | 90 | 209 |
| A2 (487) | 340 | 122 | **35,9%** | 40 | 109 | 287 |
| A3 (492) | 361 | 120 | 33,2% | 31 | 135 | 299 |
| A4 (494) | 315 | 78 | 24,8% | 34 | 91 | **307** |
| A5 (502) | 306 | 51 | **16,7%** | 24 | 82 | 146 |

**Achado:** A distribuição de tamanho de sequência (Spring 2019, Run.Program) é assimétrica à direita: mediana = **31 tentativas**, média = **40,8 (±34,7)**, P95 = **108**, máximo = **307**. **26,8% dos pares** (estudante, assignment) têm seq_len > 50, afetando **52,3% dos estudantes** (216 de 413) em ao menos um assignment. A2 (487) é o mais afetado (35,9%, mediana 40); A5 (502) o menos (16,7%, mediana 24).

**Implicação para modelagem:** A truncagem em 50 tentativas é conservadora para a maioria dos estudantes (mediana global em 31, abaixo do limite). Para os 26,8% de pares afetados, descartar as tentativas mais antigas preserva o estado de habilidade mais recente — o mais informativo para prever a próxima tentativa. A decisão de Shi et al. (2022) é reproduzida sem modificação.

### 2.2 — Impacto da Truncagem nas Sequências (Preprocessing)

**Contexto:** Após a construção das sequências via `build_sequences`, a função `truncate_sequences` aplica o corte nas últimas 50 tentativas. O impacto difere entre BKT/DKT (apenas `Run.Program`) e Code-DKT (inclui `Compile.Error`), pois a adição de `Compile.Error` aumenta o comprimento médio das sequências. Os valores abaixo são calculados sobre o **train split (328 estudantes)**, população que alimenta os modelos.

**Referência:** Shi et al. (2022); Pankiewicz, Shi & Baker (2025).

Calculado em: `02_preprocessing.ipynb` — Seção 4.1, célula de código (tabelas de truncagem) e célula markdown seguinte.

**BKT/DKT (apenas Run.Program):**

| AssignmentID | Sequências | Truncadas | % truncadas | Len média (antes) | Len média (depois) |
|---|---|---|---|---|---|
| 439 | 307 | 76 | 24,8% | 39,0 | 31,8 |
| 487 | 272 | 93 | 34,2% | 47,2 | 34,9 |
| 492 | 290 | 96 | 33,1% | 48,0 | 31,7 |
| 494 | 253 | 60 | 23,7% | 39,6 | 32,5 |
| 502 | 245 | 42 | 17,1% | 31,3 | 26,4 |

**Code-DKT (Run.Program + Compile.Error):**

| AssignmentID | Sequências | Truncadas | % truncadas | Len média (antes) | Len média (depois) |
|---|---|---|---|---|---|
| 439 | 307 | 175 | **57,0%** | 93,2 | 40,6 |
| 487 | 272 | 176 | **64,7%** | 89,5 | 42,7 |
| 492 | 290 | 159 | 54,8% | 85,5 | 38,0 |
| 494 | 253 | 142 | 56,1% | 70,9 | 40,2 |
| 502 | 245 | 84 | 34,3% | 49,3 | 32,7 |

Taxa de corretos após truncagem (train split, todos os assignments):

| Modelo | Antes truncagem | Após truncagem | Δ |
|---|---|---|---|
| BKT/DKT | 23,79% | **28,68%** | +4,89pp |
| Code-DKT | 12,46% | **20,27%** | +7,81pp |

**Achado:** A truncagem afeta BKT/DKT em 17–34% das sequências por assignment; no Code-DKT, a adição de `Compile.Error` infla o comprimento médio (70–93 eventos antes da truncagem vs 31–48 no BKT/DKT), fazendo com que 34–65% das sequências sejam truncadas. A taxa de corretos **aumenta após a truncagem** porque os eventos mais recentes refletem o aprendizado acumulado (fase pós-familiarização, menor taxa de erros). A flag `is_first_attempt` é recalculada corretamente na janela truncada — a assertion `(first_counts == 1).all()` passa em todos os assignments e modelos.

**Implicação para modelagem:** A truncagem não distorce a métrica first-attempt AUC (calculada sobre `is_first_attempt`, recalculado na janela truncada). O efeito principal é reduzir o custo de memória do LSTM (sequências ≤ 50) e eliminar o viés de estudantes com históricos muito longos. Os artefatos serializados (`results/sequences_bkt_dkt.pkl` e `results/sequences_code_dkt.pkl`) já incorporam a truncagem — os notebooks 04–06 carregam diretamente.

---

## 3 — Perfis de Estudante

### 3.1 — Clustering Exploratório (K-Means, k=3)

**Contexto:** Identificar grupos naturais de estudantes com base em taxa de acerto eventual, número médio de tentativas por assignment e nota final (X-Grade) é essencial para avaliar se os modelos KT precisam capturar heterogeneidade estrutural ou se um modelo único por assignment é suficiente. O BKT com parâmetros compartilhados por KC não distingue perfis de estudante; DKT e Code-DKT capturam implicitamente a heterogeneidade via estado oculto do LSTM.

**Hipótese:** Esperamos encontrar ao menos dois clusters bem definidos (alto vs baixo desempenho). A heterogeneidade deve se manifestar na taxa de acerto eventual e no número de tentativas.

**Referência:** Shi et al. (2022) — protocolo de avaliação por assignment; Abdelrahman et al. (2022) — survey KT.

Calculado em: `01_eda.ipynb` — Seção 2.3, células de código (K-Means com k=3, SEED=42) e célula markdown seguinte.

**K-Means k=3, SEED=42, 239 estudantes com features completas** (174 excluídos por features faltantes; X-Grade na escala normalizada 0–1):

Silhouette scores por k:
- k=2: **0,480** (máximo observado)
- k=3: **0,256** (escolhido pela interpretabilidade do perfil intermediário)
- k=4: 0,245; k=5: 0,232; k=6: 0,227

| Perfil | N | % | X-Grade médio | Taxa acerto eventual | Tentativas médias/assignment |
|---|---|---|---|---|---|
| **Alto desempenho** | 96 | **40,2%** | **0,80** | 88–98% | 3,7–8,6 |
| **Médio** | 19 | 7,9% | 0,65 | 32–65% (mínimo em A492) | 4,6–8,1 |
| **Em risco** | 124 | **51,9%** | 0,60 | 96–99% (inesperadamente alto) | **1,7–3,5** (muito baixo) |

**Achado:** K-Means com k=3 (SEED=42) sobre 239 estudantes revela três perfis ordenados por X-Grade médio. O silhouette score favorece k=2 (0,480) sobre k=3 (0,256), mas k=3 é preferido pela interpretabilidade do perfil intermediário. Resultado inesperado: o cluster "Em risco" (51,9% da turma) apresenta taxas de acerto eventual tão altas quanto o "Alto desempenho" (~96–99%), mas número médio de tentativas muito menor (1,7–3,5/assignment). O cluster "Médio" é o que exibe menor taxa de acerto eventual (32–65%) e mais tentativas — padrão de dificuldade persistente real. O perfil "Em risco" (X-Grade médio 0,60) parece representar estudantes com **baixo engajamento** (poucos problemas tentados), não estudantes que erram muito.

**Implicação para modelagem:** A heterogeneidade não se organiza na estrutura esperada (dificuldade ↔ tentativas ↔ grade). O perfil "Em risco" evidencia que baixo engajamento é o padrão dominante (51,9%), não dificuldade persistente. O DKT e Code-DKT, ao modelar sequências individualizadas, capturam implicitamente esse comportamento; o BKT com parâmetros compartilhados por KC não diferencia engajamento seletivo de baixa maestria. O silhouette forte em k=2 (0,480) sugere uma separação primária nítida (engajados vs não-engajados), mas a granularidade de três perfis exige tratar o KT como um **contínuo de habilidades**, não grupos discretos. Em assignments com sequências curtas (e.g., A5 com mediana de apenas 24 tentativas), o BKT pode ter vantagem por ser mais simples e menos suscetível a overfitting.

### 3.2 — Participação e Dropout por Assignment

**Contexto:** Dropout ao longo do semestre reduz o número de estudantes avaliáveis nos assignments finais, podendo introduzir viés de seleção (os estudantes que persistem até A5 podem ser os de maior desempenho).

**Referência:** Shi et al. (2022) — avaliação por assignment.

Calculado em: `01_eda.ipynb` — Seção 1.1.3, célula de código (participação por assignment) e célula markdown seguinte.

| Assignment | Estudantes (Spring 2019, 413 total) | % participação |
|---|---|---|
| A1 (439) | 386 | 93,5% |
| A2 (487) | 340 | 82,3% |
| A3 (492) | 361 | 87,4% |
| A4 (494) | 315 | 76,3% |
| A5 (502) | 306 | **74,1%** |

58,4% dos estudantes (241/413) participaram de todos os 5 assignments. A participação cai de 93,5% (A1) para 74,1% (A5) ao longo do semestre (~19pp).

**Achado:** A participação é máxima em A1 (93,5%) e mínima em A5 (74,1%), uma queda de ~19pp entre os extremos do semestre, embora não monotônica (A3, 87,4%, supera A2, 82,3%). A redução afeta principalmente os estudantes com pior desempenho (o cluster "Em risco"). **58,4% dos estudantes** (241 de 413) completaram todos os 5 assignments. No train split (328 estudantes), o número de sequências por assignment varia de 245 (A5) a 307 (A1).

**Implicação para modelagem:** A variação de participação não invalida o protocolo de treinamento por assignment, mas os notebooks 04–06 devem reportar o número de estudantes por assignment (não assumir que todos os 328 estudantes de treino participaram de todos os assignments). Diferentemente da iteração anterior (que usava o split do Data Challenge 2021), o split 80/20 atual possui sequências de teste para **todos os 5 assignments** (A439, A487, A492, A494, A502 — ver Seção 4.3), tornando os cinco avaliáveis.

---

## 4 — Implicações das Decisões de Pré-processamento

### 4.1 — Por que Compile.Error entra no Code-DKT (mas não em BKT nem DKT)

**Contexto:** O pipeline de pré-processamento mantém dois protocolos de filtragem distintos: `filter_for_bkt_dkt` retém apenas eventos `Run.Program`; `filter_for_code_dkt` adiciona `Compile.Error` com `correct=0`. A justificativa para essa assimetria é arquitetural: o Code-DKT incorpora features do código-fonte a cada passo da sequência LSTM. BKT e DKT padrão recebem apenas pares `(ProblemID, correct)` — sem acesso ao código — e portanto não têm mecanismo para processar o estado sintático de uma submissão não-compilável.

**Hipótese:** A inclusão de `Compile.Error` deve aumentar o sinal preditivo do Code-DKT em relação ao DKT padrão, pois esses eventos carregam informação sobre o processo de depuração do estudante (estado intermediário do código antes da execução bem-sucedida). O custo é o aumento do imbalance: `Compile.Error` contribui exclusivamente com `correct=0`.

**Referência:** Shi et al. (2022) — Code-DKT original exige código compilável, descarta `Compile.Error`; Pankiewicz, Shi & Baker (2025) — srcML-DKT inclui `Compile.Error` com `correct=0` e features srcML.

Calculado em: `02_preprocessing.ipynb` — Seção 2.1, célula `filter_for_bkt_dkt` / `filter_for_code_dkt` (assertions de EventType e contagem por tipo).

**Por que srcML habilita a inclusão de Compile.Error:**
O Code-DKT original (Shi et al., 2022) extraía features de código via `javalang`, que requer código **sintaticamente válido** — submissões com erro de compilação não são parseáveis e eram descartadas. O srcML-DKT (Pankiewicz et al., 2025) demonstrou que o parser srcML consegue extrair estrutura parcial de código Java não-compilável, representando-o como XML com marcações de erro. Com srcML, a mesma arquitetura LSTM + atenção do Code-DKT recebe features mesmo dos `Compile.Error`, viabilizando sua inclusão na sequência.

**Impacto quantitativo no CSEDM (train split):**

| Protocolo | Eventos totais | Run.Program | Compile.Error | Taxa corretos |
|-----------|---------------|-------------|---------------|---------------|
| BKT/DKT (apenas Run.Program) | 56.423 | 56.423 (100%) | 0 | **23,79%** |
| Code-DKT (Run.Program + Compile.Error) | 107.761 | 56.423 (52,4%) | 51.338 (47,6%) | **12,46%** |

Os 51.338 eventos `Compile.Error` (47,6% do total Code-DKT no train split) contribuem **exclusivamente** com `correct=0`, reduzindo a taxa de corretos de 23,79% para 12,46%. No Spring 2019 completo, são 62.316 `Compile.Error` em 131.943 submissões (47,2% — `01_eda.ipynb`, Seção 6.1).

**Achado:** O imbalance no Code-DKT (~7:1 antes da truncagem, ~4:1 após) é consideravelmente maior que no BKT/DKT (~3:1). A justificativa empírica para aceitar esse custo é a correlação de Spearman ρ = −0,564 entre `n_compile_errors` e Label (`01_eda.ipynb`, Seção 8.1) — os eventos de compilação com erro carregam sinal preditivo relevante sobre o desempenho final do estudante. A justificativa teórica é que o processo de depuração (sequência de Compile.Error → eventual Run.Program correto) reflete a trajetória de aprendizado, e o srcML consegue capturar essa evolução sintática mesmo em código inválido.

**Implicação para modelagem:** BKT e DKT usam `sequences_bkt_dkt.pkl` (artefato sem `Compile.Error`); Code-DKT usa `sequences_code_dkt.pkl` (inclui `Compile.Error`). Os notebooks 04–06 **não devem** misturar esses artefatos. A first-attempt AUC permanece comparável entre modelos porque é calculada sobre `is_first_attempt` (primeira tentativa de `Run.Program` por problema) — os `Compile.Error` afetam o contexto histórico do LSTM mas não entram diretamente no conjunto de avaliação.

---

### 4.2 — Justificativa do Threshold Score == 1.0

**Contexto:** O Score do CSEDM não é puramente binário — cada `Run.Program` produz um Score contínuo em [0, 1] correspondente à fração de testes automatizados que passaram. A escolha do threshold para converter em label binário (`correct = 1` ou `correct = 0`) afeta diretamente a definição de "acerto" no problema de KT.

**Hipótese:** A distribuição do Score deve ser trimodal (concentrada em 0, em 1 e com pico em scores parciais de alto valor), com ~33–37% de scores parciais. O threshold `Score == 1.0` deve capturar apenas execuções onde o estudante passou em **todos** os testes — um critério claro de maestria do problema.

**Referência:** Shi et al. (2022) — Section 3.1, "`correct=1` when all tests pass"; Price et al. (2020) — ProgSnap2 v6, definição de Score como fração de testes passados.

Calculado em: `01_eda.ipynb` — Seção 5.1, célula de código (distribuição de Score no Spring 2019) e célula markdown seguinte.

**Distribuição do Score (Spring 2019, 69.627 Run.Program):**

| Categoria | Contagem | % total |
|-----------|----------|---------|
| Score = 0.0 (falhou todos os testes) | 29.839 | **42,9%** |
| 0 < Score < 1 (acerto parcial) | 23.298 | **33,5%** |
| Score = 1.0 (passou todos os testes) | 16.490 | **23,7%** |
| **Total** | **69.627** | **100%** |

Valores únicos de Score: 205 — todos correspondem a frações racionais discretas (e.g., 3/11 ≈ 0,273; 1/2 = 0,500; 6/7 ≈ 0,857), confirmando que o Score reflete contagem de testes com resolução por assignment.

**Raciocínio analítico para Score == 1.0:**

1. **Separação natural de classes:** A distribuição é trimodal com massa clara em 0 e 1. Não há threshold intermediário óbvio entre 0 e 1 que seja justificável sem conhecimento das rúbricas de cada assignment.

2. **Consistência com o conceito de maestria:** KT modela a probabilidade de o estudante *dominar* o conhecimento (KC). Passar 6/7 testes pode refletir um detalhe específico não dominado — usar Score < 1.0 como `correct=1` introduziria ruído em vez de sinal de maestria.

3. **Reprodutibilidade:** Shi et al. (2022) adotam explicitamente `Score == 1.0` como `correct = 1`. Usar o mesmo threshold garante que os 23,68% de corretos no Spring 2019 correspondam exatamente ao benchmark do paper (divergência < 0,01pp).

4. **Impacto dos parciais:** Os 33,5% de scores parciais são classificados como `correct=0`. Essa perda de granularidade é o custo da binarização — mas é necessária porque BKT, DKT e Code-DKT modelam distribuições Bernoulli.

**Achado:** A distribuição do Score no Spring 2019 é trimodal: 42,9% em 0,0; 23,7% em 1,0; 33,5% parciais (205 valores únicos). O threshold `Score == 1.0` é o único ponto naturalmente justificado pela semântica dos testes automatizados (passou/falhou todos). Scores parciais representam execuções onde subconjuntos de casos de teste passaram — tratados como `correct=0` por ausência de maestria completa.

**Implicação para modelagem:** O threshold `Score == 1.0` é aplicado uniformemente nos três modelos (BKT, DKT e Code-DKT). Para o Code-DKT, os eventos `Compile.Error` são sempre `correct=0` por definição (código não executou), sem necessidade de threshold. A coluna `correct` nos artefatos serializados já incorpora essa decisão — notebooks 04–06 não precisam re-implementar o threshold.

---

### 4.3 — Rationale do Split de Modelagem (MainTable.csv, 410 alunos, 80/20)

**Contexto:** A modelagem usa `data/CSEDM/MainTable.csv` (Spring 2019), aplicando o filtro `min_attempts >= 3` (contado em `Run.Program` globais) e a divisão `train_test_split(students, test_size=0.2, random_state=1)`. O objetivo do TCC 1 é **replicar** os resultados de Shi et al. (2022) (Table 1 e Table 2); a escolha do split é crítica para que a comparação seja válida.

**Hipótese:** O filtro `min_attempts >= 3` sobre o Spring 2019 deve reproduzir os ~410 estudantes e a taxa de 23,68% de corretos do paper. O split 80/20 deve preservar essa taxa no conjunto de treino e expor todos os 5 assignments no conjunto de teste.

**Referência:** Shi et al. (2022) — "We use the CSEDM dataset (Spring 2019)"; Price et al. (2020) — ProgSnap2 v6, documentação dos splits.

Calculado em: `01_eda.ipynb` — Seção 1.2.3 (benchmark de reprodutibilidade); `02_preprocessing.ipynb` — Seção 1.2 (benchmark) e Seção 5 (cobertura de assignments no test split).

**Parâmetros do split (verificados):**

| Característica | Valor |
|----------------|-------|
| Arquivo | `data/CSEDM/MainTable.csv` (Spring 2019) |
| Estudantes brutos | 413 |
| Filtro | `min_attempts >= 3` (Run.Program globais) → **410 alunos** |
| Split | `train_test_split(test_size=0.2, random_state=1)` |
| Estudantes (train) | **328** |
| Estudantes (test) | **82** |
| Sobreposição train ∩ test | **0** |
| Taxa corretos train (Run.Program) | **23,79%** |
| Benchmark paper Shi et al. (2022) | **23,68%** (divergência 0,11pp) |
| Assignments com dados em test | **5 de 5** (A439, A487, A492, A494, A502) |

**Três razões para este split:**

1. **Reprodutibilidade:** O filtro `min_attempts >= 3` sobre o Spring 2019 produz 410 estudantes com 23,68% de corretos globais, reproduzindo o benchmark de Shi et al. (2022). A taxa no train split (23,79%) diverge do paper em apenas 0,11pp.

2. **Cobertura completa de assignments:** Diferentemente do split do Data Challenge 2021 (pasta `Release/`, usado em iteração anterior e desde então removido), que expunha apenas 3 dos 5 assignments no conjunto de teste por design do desafio (A4 e A5 eram alvos de predição ocultos), o split 80/20 aleatório por `SubjectID` garante sequências de teste para **todos os 5 assignments**. Isso torna a comparação por assignment completa.

3. **Integridade do protocolo experimental:** O split por `SubjectID` (não por evento) garante que nenhum estudante apareça simultaneamente em treino e teste (sobreposição 0), evitando vazamento de informação entre os conjuntos.

**Achado:** O split `MainTable.csv` + `min_attempts >= 3` + `train_test_split(random_state=1)` reproduz o benchmark de 23,68% de Shi et al. (2022) com divergência inferior a 0,2pp e, ao contrário do split do Data Challenge 2021, disponibiliza os cinco assignments no conjunto de teste. Essa configuração é a base de todos os notebooks de modelagem.

**Implicação para modelagem:** Todos os notebooks de modelagem (04–06) carregam os artefatos `sequences_bkt_dkt.pkl` e `sequences_code_dkt.pkl`, gerados a partir do train/test split via `load_spring2019_split` (`src/data_loader.py`). A comparação de performance com Shi et al. (2022) Table 1 e Table 2 é válida nos cinco assignments, com A1 (439) como benchmark primário (target first-attempt AUC ≈ 74% para Code-DKT).

---

## 5 — Recomendações para Notebooks 03–07

### 5.1 — Sinalizações de Risco por Assignment

**Contexto:** Antes de implementar os notebooks de modelagem (04–06), é essencial mapear os riscos operacionais por assignment: desequilíbrio de classes, alta taxa de `Compile.Error` e alta proporção de truncagem no Code-DKT. Esses fatores determinam configurações específicas de regularização e métricas prioritárias.

**Hipótese:** A2 (487) e A3 (492) devem concentrar os maiores riscos por imbalance; A2 deve apresentar risco alto adicional pela maior taxa de truncagem no Code-DKT; A5 (502) deve ter menor risco global.

**Referência:** Shi et al. (2022); Pankiewicz, Shi & Baker (2025).

Fontes: taxa de corretos e imbalance da Seção 1.1 (01_eda.ipynb); CE rate da Seção 6.1 (01_eda.ipynb); truncagem da Seção 2.2 (02_preprocessing.ipynb); cobertura do test split da Seção 4.3.

| Assignment | Seqs (train) | Imbalance BKT/DKT | Taxa corretos | CE rate | Truncagem Code-DKT | Test split | Risco |
|---|---|---|---|---|---|---|---|
| **A1 (439)** | 307 | 2,82:1 | 26,15% | **57,6%** | 57,0% | ✓ Disponível | Moderado |
| **A2 (487)** | 272 | **3,99:1** | 20,06% | 46,9% | **64,7%** | ✓ Disponível | **Alto** |
| **A3 (492)** | 290 | **3,92:1** | **20,34%** | 43,3% | 54,8% | ✓ Disponível | **Alto** |
| A4 (494) | 253 | 3,05:1 | 24,72% | 44,1% | 56,1% | ✓ Disponível | Moderado |
| A5 (502) | 245 | 2,27:1 | 30,62% | 36,5% | 34,3% | ✓ Disponível | Baixo |

**Achado:** Duas sinalizações de risco principais emergem da análise combinada:

1. **Imbalance mais alto — A2 (487) e A3 (492):** A2 tem o maior desequilíbrio (3,99:1, 20,06% de corretos) e A3 é o segundo (3,92:1, 20,34%), praticamente empatados. Em ambos, DKT e BKT podem colapsar para prever sempre `correct=0` sem nenhum poder discriminativo — AUC ≈ 0,5 indicaria colapso de classe.

2. **Alta CE rate e truncagem máxima — A1 (439) e A2 (487):** A1 tem a maior CE rate (57,6%), indicando que mais da metade das submissões de A1 são `Compile.Error`. A2 combina CE rate moderada (46,9%) com a maior taxa de truncagem no Code-DKT (64,7%) — a janela de 50 eventos captura menos de 60% do histórico médio (89,5 eventos antes da truncagem), com potencial perda de contexto inicial relevante.

Diferentemente da iteração anterior, **todos os 5 assignments têm dados no conjunto de teste**, eliminando a restrição que limitava a comparação com o paper a A1–A3.

**Implicação para modelagem:** Os notebooks 04–06 devem: (a) reportar resultados separados por assignment com número de estudantes e taxa de corretos; (b) incluir verificação de colapso de classe antes de interpretar AUC < 0,60 em A2/A3; (c) reportar os cinco assignments na comparação, com A1 como benchmark primário contra Shi et al. (2022) Table 1 e Table 2.

---

### 5.2 — Notebook 03: Code Features e Extração de ASTs

**Contexto:** O notebook 03 extrai features de código-fonte para alimentar o Code-DKT. Cada evento na sequência (tanto `Run.Program` quanto `Compile.Error`) precisa de um vetor de features extraído do `CodeState` associado. A arquitetura do Code-DKT usa embeddings de caminhos AST (code2vec): `pr = (nó_início, caminho_textual, nó_fim)`, dimensão 300, com mecanismo de atenção. O pipeline principal usa `javalang` + code2vec (`src/code_features.py`), fiel ao Code-DKT original; o extrator srcML (`src/srcml_features.py`) é a variante exploratória para código não-compilável.

**Hipótese:** A maior dificuldade operacional será o parsing de código não-compilável (eventos `Compile.Error`), especialmente em A1 (CE rate 57,6%) e A2 (46,9%), onde a proporção de submissões não-compiláveis é mais alta. O notebook deve implementar cache por `CodeStateID` para evitar re-parsear o mesmo estado de código (média de 1.392 CodeStateIDs únicos por problema — Seção 6.2 do EDA).

**Referência:** Shi et al. (2022) — code2vec embeddings, dimensão 300; Pankiewicz, Shi & Baker (2025) — srcML sobre código não-compilável, fallback para estados com parsing parcial.

**Decisões de implementação ancoradas na EDA:**

1. **Cache por `CodeStateID`:** A Seção 6.2 (`01_eda.ipynb`) reporta 100% de cobertura de CodeStateID e 1.392 estados únicos por problema em média (até 3.391 em A1/P13). Um único dicionário `{CodeStateID: vetor_features}` serve para todos os eventos de todos os assignments. Artefatos de saída: `results/code_features_cache.pkl` (javalang) e `results/srcml_features_cache.pkl` (srcML).

2. **Fallback para parsing incompleto:** o parser pode retornar estrutura parcial para código muito incompleto ou com encoding inválido. Implementar fallback para vetor zero com flag de falha; reportar taxa de fallback por assignment — se > 1% dos eventos de qualquer assignment, investigar antes de prosseguir.

3. **Volume por assignment:** A3 (492) tem o maior volume de eventos Code-DKT antes da truncagem (média 85,5 eventos × 290 estudantes ≈ 24.800 eventos). Processar em lote por assignment para evitar pico de memória.

4. **Todos os 5 assignments incluídos:** extrair features para todos os 5 assignments. Os artefatos de sequência (`sequences_code_dkt.pkl`) cobrem todos os assignments no train e no test split.

---

### 5.3 — Notebooks 04–05: BKT e DKT

**Contexto:** BKT e DKT usam exclusivamente `sequences_bkt_dkt.pkl` (sem `Compile.Error`). O protocolo de Shi et al. (2022) treina um modelo por assignment com KC = ProblemID. A avaliação primária é first-attempt AUC; a secundária é all-attempts AUC. Com 10 KCs por assignment, o BKT tem 40 parâmetros por assignment (4 parâmetros × 10 KCs) — naturalmente regularizado. O DKT (LSTM) tem ordens de grandeza mais parâmetros.

**Hipótese:** BKT deve ter performance inferior ao DKT em A2 e A3 (maior imbalance, padrões temporais mais complexos). Em A5 (mediana 24 tentativas, menor imbalance), o BKT pode ser competitivo por ser mais simples e menos suscetível a overfitting em sequências curtas.

**Referência:** Shi et al. (2022) — Table 1 (first-attempt AUC): BKT A1 ≈ 0,714, DKT A1 ≈ 0,730; Abdelrahman et al. (2022) — parâmetros BKT e treinamento LSTM DKT.

**Decisões de implementação por assignment:**

| Assignment | Benchmarks esperados (Shi et al.) | Configuração específica | Justificativa (EDA) |
|---|---|---|---|
| **A1 (439)** | BKT ~0,714 / DKT ~0,730 | Benchmark primário; reportar AUC first-attempt vs paper | Imbalance moderado (2,82:1); 307 sequências de treino |
| **A2 (487)** | A2 disponível em test split | Monitorar colapso de classe; aplicar `pos_weight` no BCELoss | Imbalance máximo 3,99:1; apenas 20,06% de corretos |
| **A3 (492)** | A3 disponível em test split | Monitorar colapso; reportar IC do AUC (bootstrap) | Imbalance 3,92:1; 20,34% corretos |
| **A4 (494)** | A4 disponível em test split | Avaliar normalmente; imbalance moderado | 253 sequências; imbalance 3,05:1 |
| **A5 (502)** | A5 disponível em test split | Dropout mais agressivo no DKT (0,3–0,5) | Menor imbalance (2,27:1); mediana curta (24 tentativas); BKT pode ser competitivo |

**Configurações técnicas obrigatórias:**
- `SEED = 42` em todos os notebooks (reprodutibilidade)
- `pos_weight = n_incorretos / n_corretos` por assignment no `nn.BCEWithLogitsLoss` do DKT — particularmente importante para A2 (3,99:1) e A3 (3,92:1)
- Cross-validation sobre o train split para seleção de hiperparâmetros; reportar AUC por fold
- Célula de verificação de colapso de classe antes do treinamento: se a loss converge para `−log(1−p)` com `p ≈ 0` (sempre prevendo incorreto), aplicar `pos_weight` e re-treinar
- Avaliação final no test split para todos os 5 assignments

---

### 5.4 — Notebook 06: Code-DKT (e variante srcML-DKT)

**Contexto:** O Code-DKT usa `sequences_code_dkt.pkl` (inclui `Compile.Error`) e os caches de features de código. O alvo de reprodutibilidade é first-attempt AUC ≈ 74% em A1 (±3%), replicando Table 1 de Shi et al. (2022).

**Hipótese:** O Code-DKT deve superar o DKT em assignments onde o sinal do código-fonte é mais informativo. Dado que n_compile_errors tem Spearman ρ = −0,564 com Label (`01_eda.ipynb`, Seção 8.1), o ganho deve ser mais pronunciado em A1 (CE rate 57,6%) do que em A5 (CE rate 36,5%).

**Referência:** Shi et al. (2022) — Code-DKT A1: AUC ~74,3%; arquitetura LSTM + atenção sobre embeddings de caminhos AST; Pankiewicz, Shi & Baker (2025) — srcML-DKT com Compile.Error incluso.

**Decisões de implementação ancoradas na EDA:**

1. **A2 (487) — truncagem máxima no Code-DKT (64,7%):** a janela de 50 eventos captura ~56% do histórico médio de A2 (89,5 eventos antes da truncagem). O mecanismo de atenção verá sequências mais curtas em proporção. Se AUC de A2 no Code-DKT divergir do esperado, investigar se o padding ou a janela truncada está distorcendo os pesos de atenção.

2. **A1 (439) — CE rate mais alta (57,6%):** apesar de ser o assignment mais fácil em termos de imbalance, A1 tem a maior proporção de Compile.Error. O Code-DKT deve se beneficiar mais desse sinal em A1 — o ganho sobre DKT padrão deve ser mais pronunciado em A1 do que em A5.

3. **Imbalance no Code-DKT (20,27% corretos após truncagem):** o mecanismo de atenção opera sobre vetores de código, não sobre labels — o imbalance afeta a função de loss. Calcular `pos_weight` com os valores do protocolo Code-DKT (não do BKT/DKT), pois as taxas de corretos diferem (20,27% vs 28,68% após truncagem).

4. **Padding e máscara de atenção:** o dataloader deve usar `collate_fn` com padding de zeros para sequências com menos de 50 eventos. O mecanismo de atenção deve receber máscara de padding para ignorar posições artificiais. `SEED=42` no DataLoader (shuffle com generator fixo).

---

### 5.5 — Notebook 07: Comparação Final e Análise Estatística

**Contexto:** O notebook 07 consolida os resultados de BKT, DKT e Code-DKT e responde à questão central do TCC 1: qual modelo é mais adequado como base para o TCC 2? A comparação deve ser ancorada em first-attempt AUC (métrica primária) e validada por teste de significância estatística.

**Hipótese:** Code-DKT deve superar BKT e DKT em first-attempt AUC, especialmente em A1 (~74% vs ~73% DKT vs ~71% BKT). O teste de Wilcoxon signed-rank deve confirmar a significância considerando os assignments e/ou runs como amostras pareadas.

**Referência:** Shi et al. (2022) — Table 1 (first-attempt AUC) e Table 2 (all-attempts AUC); Abdelrahman et al. (2022) — protocolo de comparação e métricas de KT.

**Decisões de análise ancoradas na EDA:**

1. **Escopo de comparação:** reportar BKT vs DKT vs Code-DKT para os cinco assignments (439, 487, 492, 494, 502), todos com dados no test split. A1 (439) é o benchmark primário contra Shi et al. (2022).

2. **Interpretação de A2 (487) e A3 (492) com cautela:** os dois maiores imbalances (3,99:1 e 3,92:1). Reportar o intervalo de confiança de AUC (bootstrap ou desvio-padrão entre runs). AUC < 0,60 nesses assignments deve ser acompanhada de verificação de colapso de classe antes de ser interpretada como má performance do modelo.

3. **Teste Wilcoxon signed-rank:** usar os AUCs por assignment (e/ou por run) como amostras pareadas. Com n=5 assignments, o poder estatístico é limitado — preferir o protocolo multirun (10 runs × 5 assignments) para ampliar a amostra pareada e reportar p-value com magnitude do efeito.

4. **Engajamento seletivo vs aprendizado:** o cluster "Em risco" (51,9% dos estudantes, Seção 3.1) apresenta baixo engajamento (1,7–3,5 tentativas/assignment), não dificuldade persistente. Esses estudantes têm sequências mais curtas — um modelo KT com poucas observações por estudante tende a ser menos preciso. Considerar reportar AUC separadamente para sequências curtas (seq_len < 10) vs longas (seq_len ≥ 10) como análise complementar.

5. **Justificativa final para TCC 2:** a escolha do modelo base deve ser baseada em: (a) first-attempt AUC mais alta nos assignments; (b) magnitude do gap entre modelos; (c) extensibilidade para TCC 2 — o Code-DKT é diretamente extensível para análise semântica de código e integra `Compile.Error`, representando a direção mais promissora para sistemas adaptativos de programação.

---

## Resumo Executivo — Decisões para Notebooks 03–07

| Achado | Valor | Impacto |
|---|---|---|
| Imbalance global BKT/DKT | 3,22:1 (23,68% corretos) | Usar AUC como métrica primária |
| Imbalance máximo por assignment | 3,99:1 em A2 (20,06% corretos); A3 próximo (3,92:1) | Cautela ao interpretar AUC de A2/A3; verificar colapso de classe |
| Imbalance Code-DKT (pré-truncagem) | ~7:1 (12,46% corretos) | AUC indispensável; não usar acurácia |
| Mediana de sequências (BKT/DKT) | 31 tentativas | Truncagem em 50 conservadora para maioria |
| % pares afetados pela truncagem | 26,8% (BKT/DKT) / 34–65% (Code-DKT) | Code-DKT mais afetado por Compile.Error |
| Taxa corretos após truncagem | 28,68% (BKT/DKT) / 20,27% (Code-DKT) | Divergência esperada — eventos recentes têm mais acertos |
| Perfis de estudante (k=3) | 40,2% alto / 7,9% médio / 51,9% em risco | Modelar contínuo, não grupos discretos |
| Participação A1→A5 | 93,5% → 74,1% (58,4% completaram todos) | Reportar N por assignment |
| Compile.Error rate global (Spring 2019) | 47,2% das submissões | Sinal preditivo ρ=−0,564 com Label |
| CE rate A1 / A2 / A3 / A4 / A5 | 57,6% / 46,9% / 43,3% / 44,1% / 36,5% | A1 tem mais CE que qualquer outro assignment; ver Seção 5.1 |
| Cobertura do test split | 5 de 5 assignments | Comparação por assignment completa (sem restrição A4/A5) |
| Risco alto por assignment | A2 (3,99:1 + 64,7% truncagem Code-DKT) e A3 (3,92:1) | pos_weight obrigatório no BCELoss; ver Seção 5.3 e 5.4 |
</content>
</invoke>
