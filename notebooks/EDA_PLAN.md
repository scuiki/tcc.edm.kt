# Plano de Análise Exploratória de Dados (EDA)
## Dataset CSEDM / ProgSnap2 v6

> **Enquadramento metodológico:** A EDA compõe a fase de *Data Preparation and Gathering* do EDM Process (Kalita et al., 2025), executada antes da modelagem. Seu objetivo não é apenas descrever o dataset, mas revelar padrões de comportamento de aprendizagem que orientem a definição de features, a escolha de métricas e a interpretação dos modelos de Knowledge Tracing.

---

## 1. Visão Geral do Dataset e Integridade

**Objetivo:** Caracterizar o dataset e identificar problemas de qualidade antes de qualquer análise.

### 1.1 Estatísticas básicas
- Total de eventos em `MainTable.csv` por tipo (`EventType`)
- Número de estudantes únicos (`SubjectID`), assignments (`AssignmentID`), problemas (`ProblemID`)
- Distribuição de estudantes por assignment (todos participaram de todos os 5?)
- Verificar consistência entre splits: `Release/Train/` vs `Release/Test/` vs `All/`

### 1.2 Qualidade dos dados e anatomia dos splits
- **Anatomia dos splits:** `All/`, `Train/`, `Test/` compartilham a mesma população de estudantes; `Release/` é uma população separada (diferentes SubjectIDs, diferente cobertura de assignments). Identificar qual split foi usado no paper Code-DKT comparando metadados e tamanhos.
- Valores ausentes por coluna (especialmente `Score`, `CodeStateID`)
- Eventos sem `CodeStateID` associado — qual fração e quais `EventType`s
- Nota: não existe `EventType = Submit` neste dataset — submissões são `Run.Program` com `Score` não-nulo. Todos os filtros de pré-processamento devem usar `Run.Program` com `Score >= 0`.
- Submissões com `Score` fora do intervalo [0, 1]
- Registros duplicados (mesmo `SubjectID` + `ProblemID` + `ServerTimestamp`)
- Cobertura temporal: período de coleta por split (comparar timestamps entre `All/` e `Release/`)

### 1.3 Consistência entre tabelas
- `CodeStateID`s referenciados em `MainTable` mas ausentes em `CodeStates.csv`
- `SubjectID`s em `early.csv`/`late.csv` sem correspondência em `MainTable`
- Verificar `DatasetMetadata.csv`: `IsEventOrderingConsistent = TRUE` (validar na prática)

---

## 2. Análise da População de Estudantes

**Fundamentação:** Yağcı (2022) identifica *"student participation"* e *"learning strategies"* como preditores de desempenho — o comportamento de tentativa é o proxy disponível neste dataset para essas dimensões.

### 2.1 Distribuição de desempenho geral
- Histograma de `X-Grade` (nota final, `Subject.csv`) — distribuição bimodal ou contínua?
- Boxplot de `X-Grade` por assignment (alunos com melhor desempenho geral performam consistentemente?)
- Percentual de estudantes que completaram todos os 5 assignments vs abandonaram

### 2.2 Padrões de tentativa por estudante
- Distribuição do número total de tentativas (`Attempts`) por estudante (identificar outliers: ≥ 200 tentativas?)
- Distribuição de tentativas por problema por estudante
- Fração de estudantes que nunca acertaram nenhum problema (`CorrectEventually = False` em todos)
- Correlação entre número de tentativas e `X-Grade` — mais tentativas = melhor ou pior aluno?

### 2.3 Perfis de estudante (clustering exploratório)
- Construir vetor de features por estudante: `[taxa_acerto_A1, ..., taxa_acerto_A5, tentativas_médias, grade]`
- K-Means com k=3–5 para identificar perfis: *"alto desempenho"*, *"médio"*, *"em risco"*
- Referência: Kalita et al. (2025) cita clustering como técnica central em EDM para *"grouping"* de estudantes

---

## 3. Estrutura de Assignments e Problemas

**Objetivo:** Entender a organização do dataset e validar a escolha de `AssignmentID` como Knowledge Component.

### 3.1 Distribuição por assignment
- Número de problemas por assignment (confirmação: 10 por assignment?)
- Número de estudantes por assignment
- Taxa de acerto média por assignment — identificar assignments mais difíceis
- Boxplot de `Score` por assignment

### 3.2 Análise por problema
- Taxa de acerto (`CorrectEventually = True`) por `ProblemID` — heatmap problema × assignment
- Número médio de tentativas até o primeiro acerto por problema
- Problemas com taxa de conclusão < 20% (potencialmente mal formulados ou muito difíceis)
- Correlação entre dificuldade do problema e posição no assignment (problemas finais são mais difíceis?)

### 3.3 Validação da granularidade de KC
- Os problemas dentro do mesmo assignment têm padrões de dificuldade similares?
- Comparar com os clusters estruturais (Etapa B do pipeline de KCs): os clusters AST respeitam os boundaries de assignment?
- Referência: a escolha de `AssignmentID` como KC segue Shi et al. (2022) — *"each assignment focusing on a specific topic (e.g., conditionals, loops)"*

---

## 4. Padrões de Interação e Tentativas

**Objetivo:** Caracterizar o comportamento de submissão — base direta para a construção das sequências de input dos modelos KT.

### 4.1 Distribuição de tentativas por problema
- Histograma de `Attempts` (de `early.csv`) — distribuição exponencial? Cauda longa?
- Percentual de tentativas truncadas pelo limite de 50 (conforme Shi et al., 2022)
- Distribuição por assignment: problemas de A1 têm menos tentativas que A5?

### 4.2 Padrão de acerto/erro ao longo da sequência
- Para cada problema, plotar a taxa de acerto em função do índice da tentativa (tentativa 1, 2, 3, ..., 10+)
- Isso gera as **curvas de aprendizagem por problema**, análogas às *"error rate curves"* citadas em Rivers et al. (apud Kalita et al., 2025)
- Perguntas a responder: o estudante converge para o acerto? Há platôs? Em qual tentativa a maioria acerta pela primeira vez?

### 4.3 Distribuição de EventType
- Proporção de `Run.Program` vs `Compile` vs `Compile.Error` no total de eventos (não existe `Submit` neste dataset — submissões são `Run.Program` com `Score` definido)
- Taxa de erros de compilação por assignment — decresce ao longo do semestre? (indicador de aprendizagem)
- Fração de eventos `Compile.Error` que antecedem um `Run.Program` correto (`Score == 1.0`)

### 4.4 Análise early vs late labels
- Comparar distribuição de `Label` em `early.csv` vs `late.csv` por problema
- Para quantos estudantes o Label muda de `False` para `True` (aprenderam no processo)?
- Distribuição do número de tentativas no ponto de corte *early* vs *late*

---

## 5. Análise de Score e Desequilíbrio de Classes

**Fundamentação:** Kalita et al. (2025) dedica seção ao problema de *"imbalanced datasets"* em EDM. Shi et al. (2022) reporta 23,68% de tentativas corretas e justifica AUC como métrica por esse desequilíbrio.

### 5.1 Distribuição global de Score
- Histograma de `Score` — é bimodal (0 ou 1) ou contínuo?
- Proporção de `Score == 1.0` vs `Score < 1.0` (replicar o 23,68% do paper)
- Distribuição de Scores parciais (0 < Score < 1): frequentes ou raros?

### 5.2 Desequilíbrio por granularidade
- Taxa de acerto (`Score == 1.0`) por assignment — o desequilíbrio é uniforme ou concentrado?
- Taxa de acerto por problema — heatmap `ProblemID × taxa_acerto`
- Identificar problemas outliers: taxa < 10% (muito difícil) ou > 80% (trivial)

### 5.3 Implicações para modelagem
- O desequilíbrio justifica AUC como métrica primária (em vez de acurácia)
- Avaliar se SMOTE seria aplicável ou se o desequilíbrio é inerente ao processo de aprendizagem (tentativas incorretas são informativas, não ruído)

---

## 6. Análise de Evolução do Código

**Objetivo:** Explorar a dimensão única do dataset ProgSnap2 — o código-fonte das submissões — caracterizando como o estudante modifica seu programa ao longo das tentativas.

### 6.1 Métricas básicas de código
- Distribuição do tamanho do código (linhas de código) em submissões corretas vs incorretas
- Evolução do tamanho do código ao longo das tentativas por problema (o estudante expande ou refatora?)
- Fração de `CodeStates` que são idênticos a submissões anteriores do mesmo estudante (resubmissão sem modificação)

### 6.2 Fingerprints estruturais por problema
- Para cada `ProblemID`, extrair frequência de construções Java (via `javalang`) em submissões corretas
- Comparar fingerprints entre submissões corretas e incorretas: qual construção está ausente nos erros?
- Visualizar heatmap `ProblemID × construção_Java` (base para o pipeline de KCs)

### 6.3 Diversidade de soluções
- Para cada problema, quantas soluções estruturalmente distintas (clusters de fingerprint AST) existem nas submissões corretas?
- Problemas com solução única dominante vs problemas com múltiplas abordagens válidas
- Relevância: problemas com solução única são mais previsíveis pelo Code-DKT?

### 6.4 Trajetória de modificação
- Para uma amostra de estudantes, visualizar a sequência de CodeStates de um mesmo problema como *diff* simplificado
- Identificar padrões: correção pontual (1-2 linhas) vs reescrita completa
- Correlação entre magnitude da modificação e probabilidade de acerto na próxima tentativa

---

## 7. Análise Temporal

**Objetivo:** Verificar se há padrões temporais relevantes que impactem a validade do dataset.

### 7.1 Distribuição de atividade ao longo do semestre
- Heatmap de eventos por semana do semestre × assignment
- Picos de atividade próximos a deadlines (comportamento de procrastinação)
- Sessões de estudo: identificar agrupamentos temporais de eventos por estudante

### 7.2 Tempo entre tentativas
- Distribuição do intervalo entre tentativas consecutivas (`ServerTimestamp` delta)
- Diferença entre tentativas dentro de uma sessão (< 5 min) vs entre sessões (> 1h)
- O tempo de resposta decresce ao longo das tentativas? (indicador de aquecimento cognitivo)

---

## 8. Análise de Correlação para Modelagem

**Objetivo:** Identificar quais features exploratórias mais se correlacionam com o Label alvo — antecipando a seleção de features dos modelos.

### 8.1 Correlação com Label (early/late)
- Correlação de Spearman entre `Attempts` e `Label`
- Correlação entre taxa de acerto anterior no assignment e `Label`
- Correlação entre `X-Grade` (nota final) e `Label` — os melhores alunos têm Label = True mais cedo?

### 8.2 Feature importance exploratória
- Treinar um Decision Tree simples com features básicas (tentativas, taxa_acerto, assignment_id) para prever `Label`
- Extrair importância de features como proxy rápido antes dos modelos completos
- Referência: Yağcı (2022) usa feature selection explícita antes dos modelos ML

---

## Entregáveis do Notebook `01_eda.ipynb`

| Seção | Visualização principal | Insight esperado |
|---|---|---|
| 1. Integridade | Tabela de missing values | % de CodeStates ausentes |
| 2. Estudantes | Histograma X-Grade + clusters | Identificar alunos em risco |
| 3. Assignments | Heatmap taxa de acerto por problema | KC mais difíceis |
| 4. Tentativas | Curvas de aprendizagem | Convergência por problema |
| 5. Score | Histograma + desequilíbrio por assignment | Justificar AUC |
| 6. Código | Heatmap fingerprint AST | Base para KC híbrido |
| 7. Temporal | Heatmap atividade × semana | Detectar procrastinação |
| 8. Correlação | Decision Tree feature importance | Antecipar features relevantes |

---

## Referências

- Kalita, E. et al. (2025). *Educational Data Mining: a 10 year review*. Discover Computing, 28:81.
- Yağcı, M. (2022). *Educational data mining: prediction of students' academic performance using machine learning algorithms*. Smart Learning Environments, 9:11.
- Shi, Y. et al. (2022). *Code-DKT: A Code-based Knowledge Tracing Model for Programming Tasks*. NCSU.
- Rivers, K. & Koedinger, K. (apud Kalita et al., 2025). *Learning curves from AST-based KC extraction*.
