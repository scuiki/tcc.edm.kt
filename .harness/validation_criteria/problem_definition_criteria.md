# Critérios de Validação — 00_problem_definition.ipynb

Este documento define os critérios de pesquisa para validação independente do notebook de
definição do problema. Os critérios avaliam se as **decisões metodológicas fundamentais** do
projeto de KT estão documentadas com justificativa suficiente para um revisor externo entender
e reproduzir os experimentos.

---

## 1. Definição de Knowledge Component (KC)

**1.1 KC=ProblemID documentado com justificativa**
O notebook documenta que o Knowledge Component é definido como ProblemID? A justificativa
inclui pelo menos dois dos seguintes elementos:
- Um modelo KT separado é treinado por assignment (não um único modelo para todos os problemas)
- Essa granularidade é o protocolo adotado por Shi et al. (2022)
- A escolha permite comparação direta com os resultados do paper

**1.2 Escopo de modelagem claro**
O notebook explica que os 9-10 problemas de cada assignment constituem os KCs do modelo
treinado naquele assignment? Essa estrutura é visualizada ou exemplificada?

---

## 2. Definição de Métricas

**2.1 First-attempt AUC como métrica primária**
O notebook define first-attempt AUC como a métrica primária? A justificativa menciona pelo
menos um dos seguintes:
- Evita autocorrelação temporal (múltiplas tentativas do mesmo estudante no mesmo problema
  inflariam artificialmente a AUC)
- É a métrica reportada por Shi et al. (2022), permitindo comparação direta
- É menos sensível ao imbalance de tentativas por estudante

**2.2 All-attempts AUC como métrica secundária**
O notebook define all-attempts AUC como métrica secundária? O papel complementar está
explicado: comparação com literatura DKT mais ampla (Piech et al., 2015), maior estabilidade
estatística por usar mais amostras?

**2.3 Definição operacional de "first attempt"**
O notebook explica o que "primeira tentativa" significa operacionalmente: a primeira ocorrência
de (SubjectID, ProblemID) na sequência temporal de cada estudante?

---

## 3. Decisões de Modelagem Consolidadas

**3.1 Tabela ou seção summary presente**
Há uma tabela ou seção que consolida as decisões de modelagem do projeto? A tabela deve cobrir
pelo menos: definição de KC, splits usados, métricas, modelos comparados, seed?

**3.2 Os três modelos referenciados**
BKT, DKT e Code-DKT são mencionados e comparados em alto nível? O notebook explica o que cada
modelo incorpora como informação de entrada (BKT: tentativas por KC; DKT: sequência de KCs;
Code-DKT: código-fonte + sequência)?

---

## 4. Rastreabilidade de Pesquisa

**4.1 Citações presentes e corretas**
Shi et al. (2022) é citado no contexto da definição de KC e da métrica first-attempt AUC?
Pankiewicz et al. (2025) é citado no contexto do Code-DKT / srcML? As citações estão nos
markdowns das seções relevantes (não apenas em uma lista de referências ao final)?

**4.2 Seed fixo documentado**
SEED = 42 está definido e documentado como requisito de reproduzibilidade para todos os
notebooks subsequentes?
