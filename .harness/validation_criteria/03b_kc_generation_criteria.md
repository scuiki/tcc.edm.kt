# Critérios de Validação — 03b_kc_generation.ipynb

Este documento define os critérios de pesquisa para validação independente do notebook de
geração de KCs. Os critérios avaliam a **integridade das decisões metodológicas** baseadas
em Duan et al. (2025) — KCGen-KT — e a reproduzibilidade do pipeline LLM.

---

## 1. Diversity Sampling

**1.1 Estratificação por tentativas antes do acerto**
O diversity sampling estratifica submissões corretas por número de tentativas antes de
acertar (proxy de diversidade de estratégia de solução)? Os 5 buckets (1, 2–3, 4–6,
7–10, >10) estão implementados? A fundamentação em Duan et al. (2025) Table 5 está citada?

**1.2 Número correto de amostras**
O código extrai até 5 submissões por `(AssignmentID, ProblemID)` (1 por bucket
disponível)? O markdown justifica o n=5 com referência ao ponto ótimo de Duan et al.
(2025, Table 5)?

**1.3 Uso exclusivo do Release/Train**
Os samples são extraídos apenas de `results/sequences_bkt_dkt.pkl` (split Release/Train)?
O notebook não usa eventos do split All/ ou Test/ para gerar KCs?

---

## 2. Geração de KCs via LLM

**2.1 Código bruto como input (não AST)**
O LLM recebe código Java bruto nas submissões? O notebook declara explicitamente que AST
*não* é enviado ao LLM e cita a ablação de Duan et al. (2025, Table 4) como fundamento
(AST como input reduz AUC de 0.812 para 0.784)?

**2.2 In-context examples presentes**
O prompt de geração de KCs inclui in-context examples baseados em Duan et al. (2025)
Appendix B (Table 8)? A citação é explícita no markdown? Os exemplos são de problemas
Java introdutórios de granularidade compatível com o CSEDM?

**2.3 Output estruturado correto**
O output esperado do LLM inclui `problem_description` (descrição inferida) e `kcs` (lista
com `name` e `reasoning` por KC)? O parsing do JSON é robusto (trata erros de parse)?

**2.4 Cache obrigatório implementado**
O código verifica se `results/kc_raw_{assignment_id}.json` existe antes de chamar a API?
Se o arquivo existir, os dados são carregados do disco sem nova chamada LLM? A lógica
de cache está presente para todos os 5 assignments?

---

## 3. Clustering

**3.1 Embeddings semânticos usados**
Os nomes dos KCs brutos são embedados com Sentence-BERT (ou modelo equivalente)? O
modelo escolhido é documentado no markdown? Embeddings são calculados sobre os nomes dos
KCs (não sobre o código Java)?

**3.2 HAC com distância cosseno**
O clustering usa Hierarchical Agglomerative Clustering (HAC) com distância cosseno? A
implementação usa `scipy.cluster.hierarchy`? O critério de linkage está documentado?

**3.3 Granularidade alvo documentada**
O código testa 10, 12 e 15 clusters por assignment? O critério de seleção do número final
de clusters está explicado no markdown? O resultado é coerente com a escala do problema
(10 problemas por assignment → abstração média)?

**3.4 Reproduzibilidade**
SEED = 42 é usado em operações não-determinísticas do clustering? O resultado é
reproduzível com a mesma semente?

---

## 4. Rotulagem de Clusters via LLM

**4.1 Prompt de rotulagem baseado em Duan et al.**
O prompt de rotulagem de clusters é baseado em Duan et al. (2025) Table 9? A citação
é explícita no markdown? O prompt instrui o LLM a decidir se um KC do cluster representa
o grupo inteiro ou se é necessário sintetizar um novo rótulo?

**4.2 Cache implementado**
O código verifica se `results/kc_descriptions_{assignment_id}.json` existe antes de chamar
a API? Rótulos são calculados apenas uma vez e reutilizados em execuções subsequentes?

**4.3 KCs finais interpretáveis**
O markdown apresenta os KCs finais de ao menos um assignment? Os nomes são semânticos e
interpretáveis (ex.: "Iteração com For-Each", "Condicional com múltiplos ramos")? O número
final de KCs por assignment está entre 10 e 15?

---

## 5. Q-matrix

**5.1 Formato correto**
A Q-matrix tem `ProblemID` como índice/primeira coluna e KCs como colunas binárias
(`kc_0, kc_1, ..., kc_N`)? Os valores são 0 ou 1?

**5.2 Cobertura completa**
Cada problema do assignment tem ao menos 1 KC associado na Q-matrix? Não há problema
com linha de zeros?

**5.3 Estatísticas reportadas**
O markdown reporta: número de KCs por assignment, densidade média da Q-matrix (proporção
de 1s), problema com maior número de KCs? Esses valores são calculados dos dados,
não hardcoded?

**5.4 Per-assignment independente**
Há 5 arquivos separados (`qmatrix_A439.csv`, ..., `qmatrix_A502.csv`), cada um com
vocabulário de KCs independente? As colunas de um assignment não aparecem em outro?

---

## 6. KC Correctness Labeling

**6.1 Escopo correto das submissões**
O labeling processa apenas submissões incorretas de `Run.Program` do Release/Train?
O notebook declara explicitamente que submissões corretas e eventos Compile.Error não são
labelados nesta etapa?

**6.2 Prompt baseado em Duan et al. Table 10**
O prompt de correctness labeling é baseado em Duan et al. (2025) Table 10? A citação
é explícita no markdown? O output inclui `error_reasoning` e `kc_errors` ({kc_name: 0|1})?

**6.3 Cache por assignment**
O código verifica se `results/kc_correctness_{assignment_id}.json` existe antes de
processar? O processamento é feito por assignment, permitindo retomada parcial?

**6.4 Custo e escala documentados**
O markdown declara: o número aproximado de submissões processadas (~26.289), o custo
estimado (~$39 com Claude Haiku), e o modelo LLM utilizado?

---

## 7. AST Signatures (Validação Post-Hoc)

**7.1 srcML invocado corretamente**
A função de extração de signatures chama `srcml` via subprocess? O retorno inclui
frequências de nós AST relevantes para Java introdutório (`ForStatement`, `IfStatement`,
`WhileStatement`, `ArrayAccess`, `MethodCall`, etc.)?

**7.2 Uso como validação, não como input LLM**
O markdown esclarece que as assinaturas AST são usadas *por nós* para validação post-hoc,
e *não* como input ao LLM? A distinção está alinhada com a decisão metodológica do plano?

**7.3 Análise de interpretabilidade presente**
O notebook compara ao menos 2 KCs gerados com suas assinaturas AST correspondentes?
A análise responde: o KC está ancorado nas estruturas de código que aparecem nas
submissões corretas daquele problema?

---

## 8. Artefatos e Rastreabilidade

**8.1 Todos os artefatos obrigatórios gerados**
Os 10 artefatos obrigatórios existem após execução completa: `qmatrix_{aid}.csv` (5 arquivos)
e `ast_signatures_{aid}.json` (5 arquivos)? Os intermediários (`kc_raw_*.json`,
`kc_clusters_*.json`, `kc_descriptions_*.json`, `kc_correctness_*.json`) também existem?

**8.2 Schemas documentados**
O notebook documenta o schema de cada artefato: campos, tipos, exemplo de valor?
O documento final descreve a estrutura completa dos outputs?

**8.3 Reproduzibilidade com cache**
O notebook, ao ser re-executado com os arquivos de cache presentes, completa sem
fazer novas chamadas API e produz os mesmos artefatos? O padrão de cache é uniforme
em todas as etapas LLM?

**8.4 Ausência de placeholders**
Todas as funções estão completamente implementadas? Não há `pass`, `TODO`,
`NotImplementedError` nem `...` como placeholder?
