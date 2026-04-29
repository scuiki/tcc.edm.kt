# Critérios de Validação — 02_preprocessing.ipynb

Este documento define os critérios de pesquisa para validação independente do notebook de
pré-processamento. Os critérios avaliam a **integridade das decisões metodológicas** que
afetam diretamente a reproduzibilidade dos experimentos de KT.

---

## 1. Filtragem por Modelo

**1.1 filter_for_bkt_dkt usa apenas Run.Program**
A função de filtragem para BKT e DKT usa exclusivamente eventos do tipo Run.Program?
Há assertion ou log verificando que nenhum evento Compile.Error ou outro tipo passou pelo
filtro? A label `correct = (Score == 1.0)` é aplicada?

**1.2 filter_for_code_dkt inclui Compile.Error**
A função para Code-DKT inclui tanto Run.Program quanto Compile.Error? Os eventos Compile.Error
recebem `correct = 0`? A decisão está documentada no markdown com referência a
Pankiewicz et al. (2025)?

**1.3 Justificativa do threshold Score==1.0**
A decisão de usar `Score == 1.0` como threshold para "correto" (em vez de Score > 0 ou outra
definição) está documentada com justificativa explícita? O notebook menciona que ~37% das
execuções têm scores parciais e explica por que foram tratados como incorretos?

---

## 2. Construção de Sequências

**2.1 Ordenação temporal garantida**
As sequências são construídas ordenadas por ServerTimestamp? O notebook verifica ou afirma
explicitamente essa propriedade?

**2.2 Flag de primeira tentativa presente**
Cada evento na sequência inclui um indicador de que é a primeira tentativa de (SubjectID,
ProblemID)? Esse flag é necessário para o cálculo de first-attempt AUC — sua ausência tornaria
a métrica primária incorreta.

**2.3 Estrutura das sequências documentada**
O markdown descreve a estrutura de dados das sequências: quais campos cada evento contém,
tipos de dados, e um exemplo concreto?

---

## 3. Truncagem e Integridade

**3.1 Truncagem em 50 implementada corretamente**
A lógica de truncagem mantém as **últimas** 50 tentativas (não as primeiras)? Há assertion ou
verificação explícita de que nenhuma sequência excede 50 elementos após a truncagem? A referência
a Shi et al. (2022) está presente?

**3.2 Impacto da truncagem reportado**
A proporção de sequências que foram truncadas é calculada e reportada? O notebook explica o
impacto no dataset (quantos eventos foram descartados)?

---

## 4. Split e Reproduzibilidade

**4.1 Split correto documentado**
O notebook usa Release/Train para treinamento e documenta claramente qual split é usado?
A distinção entre All/ (506 estudantes, Fall-2019) e Release/ (329 estudantes, Spring-2019)
está documentada?

**4.2 Taxa de corretos pós-processamento reportada**
A taxa de corretos do split processado é calculada e comparada com o valor esperado para
Release/Train (~23.70%)? Se divergir, há explicação da diferença?

---

## 5. Artefatos e Rastreabilidade

**5.1 Artefatos gerados e documentados**
Os arquivos `results/sequences_bkt_dkt.pkl` e `results/sequences_code_dkt.pkl` são gerados
pelo notebook? O schema de cada artefato (estrutura, campos, tipos) está documentado?

**5.2 Estatísticas dos artefatos reportadas**
O notebook reporta estatísticas dos artefatos gerados: número total de sequências, número de
estudantes únicos, distribuição de comprimentos (mínimo, média, máximo)? Os valores são
calculados dos artefatos, não hardcoded?

**5.3 SEED fixo presente**
SEED = 42 está definido e usado em qualquer operação não-determinística?

---

## 6. Qualidade da Implementação

**6.1 Ausência de placeholders**
Todas as funções estão completamente implementadas? Não há `pass`, `TODO`, `NotImplementedError`
nem `raise NotImplementedError` como placeholder?

**6.2 Código reproduzível**
O notebook, executado do zero em um ambiente com os dados CSEDM, produz os mesmos artefatos?
(Verificar se há dependências de estado externo não documentadas.)
