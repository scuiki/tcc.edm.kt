# Harness Progress Notes

Appended automatically after each task completes. Do not edit manually.

<!-- Entry format:

## YYYY-MM-DD - {slug}: Task {id} - {title}

- O que foi implementado
- Decisões-chave e por quê
- Veredito do Format Evaluator (PASS na primeira | PASS após N retries | issues encontrados)
- Bugs ou inconsistências encontrados no dataset (se houver)
- O que trabalhar a seguir

-->

## 2026-04-29 - problem_definition: Task 1 - Aplicar template didático em todas as seções existentes

- Adicionados campos **Contexto**, **Hipótese**, **Referência** às células markdown pré-código das seções 1 (KCs) e 3 (Splits do Dataset) — únicas seções com células de código
- Inseridas duas novas células markdown pós-código com **Achado** e **Implicação para modelagem**: após o código KC e após o plot de distribuição de Label
- Conteúdo analítico original (tabelas, textos, gráficos) mantido sem alteração substancial
- Notebook executado com sucesso via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Bug/inconsistência anotada:** A tabela de KC em cell [3] mantém "KC = AssignmentID" como definição baseline — diverge de CLAUDE.md e Shi et al. (2022) que definem KC=ProblemID com modelos por assignment. Corrigir em Task 2.

**A trabalhar a seguir:** Task 2 — corrigir KC=ProblemID, adicionar first-attempt AUC vs all-attempts AUC, atualizar tabela de Resumo com coluna Justificativa.

## 2026-04-29 - problem_definition: Task 2 - Validar e documentar decisões de modelagem

- **Seção 1 (KC=ProblemID):** corrigida a definição de KC — removida a tabela incorreta "KC baseline = AssignmentID"; substituída por texto explícito KC=ProblemID com fonte em Shi et al. (2022) footnote 1. Código atualizado: print agora exibe "5 assignments → 5 modelos independentes (KC = ProblemID)". Pós-código reescrito para reforçar 50 KCs totais e dimensão do input DKT.
- **Seção 4 (Métricas):** reescrita com template didático completo (Contexto, Hipótese, Referência). Inserida célula de código que calcula distribuição de tentativas por par (estudante, problema) a partir de early/late.csv e exibe histograma. Inserida célula pós-código com Achado (64.6% com >1 tentativa, mediana=2, máx=177) e Implicação que define first-attempt AUC como métrica primária e all-attempts AUC como secundária.
- **Seção 6 (Resumo):** tabela "Resumo das Decisões" atualizada para 3 colunas (Decisão, Valor, Justificativa) com 10 linhas cobrindo KC, estrutura de treinamento, splits, métricas, labels, threshold, Compile.Error, truncamento e seed.
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Bug/inconsistência anotada:** Pergunta de Pesquisa (Seção 5) ainda referencia "KC = AssignmentID" no texto — diverge de KC=ProblemID adotado. Fora do escopo de Task 2; corrigir em revisão futura se necessário.

**A trabalhar a seguir:** Próxima fase — notebook 01_eda.ipynb (Data Preparation — EDA).

## 2026-04-29 - eda: Task 1 - Revisar Seção 1 — Estatísticas básicas e qualidade dos dados

- Modificadas 9 células markdown de seção/subseção para seguir o template didático (Contexto, Hipótese, Referência): cabeçalho geral "## 1", subseções 1.1.1–1.1.4 e 1.2.1–1.2.5
- Inseridas 9 células markdown pós-código com Achado e Implicação para modelagem em cada subseção analítica
- Citações a Price et al. (2020) e Shi et al. (2022) presentes em todas as subseções relevantes
- Registros duplicados (236.024) documentados na seção 1.2.4 com explicação explícita: par Run.Program/Compile com mesmo timestamp via ParentEventID — comportamento esperado do ProgSnap2, não erro de coleta
- Conteúdo analítico original (código, outputs, gráficos) mantido integralmente; apenas markdown adicionado/ajustado
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Bug/inconsistência anotada:** Splits `Test` e `Release/Test` contêm apenas A1–A3 (não os 5 assignments completos) — provável design intencional do dataset para avaliação temporal, mas diverge da documentação. Anotado na seção 1.2.1; sem impacto na modelagem (usar Release/Train/Test).

**A trabalhar a seguir:** Task 2 — aplicar template didático na Seção 2 (Análise de Estudantes e Clustering): verificar SEED=42 explícito, adicionar Contexto/Hipótese/Referência e Achado/Implicação em 2.1–2.3.

## 2026-04-29 - eda: Task 2 - Revisar Seção 2 — Desempenho de estudantes e clustering

- **Cabeçalho "## 2"**: substituído texto descritivo por template completo (Contexto, Hipótese, Referência) — agora justifica explicitamente a necessidade de sequências individualizadas para KT
- **Seção 2.1 (X-Grade)**: inserida célula markdown pré-código com Contexto/Hipótese/Referência; inserida célula pós-código com Achado (média 60.6 ±19.9, mediana 61.2; 72.1% ≥ 50; 4.2% < 25; CorrectEventually 91–98% por assignment) e Implicação para modelagem
- **Seção 2.2 (Tentativas)**: substituída célula header minimalista por template completo; inserida célula pós-código com Achado (mediana 215 tentativas; 54.0% ≥ 200; 57.3% com ≥1 problema sem resolver; Spearman ρ = 0.296 positivo — contrariou hipótese de relação negativa) e Implicação
- **Seção 2.3 (Clustering)**: atualizado o pre-code para template exato (Contexto, Hipótese, Referência); substituída a célula de interpretação post-hoc por Achado e Implicação estruturados. Tabela de perfis atualizada com valores reais calculados: Alto desempenho (N=139, grade 73.8, rate 94–99%, att 4.4–10.9), Médio (N=66, grade 64.9, rate 56–89%, att 5.1–9.7), Em risco (N=248, grade 55.9, rate 97–99% — inesperadamente alto, att 2.0–4.6 — muito baixo)
- SEED=42 já estava explícito no código (`SEED = 42`; `KMeans(n_clusters=k, random_state=SEED, n_init=10)`) — não foi necessário alterar
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achado inesperado:** O cluster "Em risco" (grade ~55.9, 54.7% da turma) tem taxas de acerto eventual de 97–99% mas média de apenas 2–4.6 tentativas/assignment — perfil de baixo engajamento, não de dificuldade persistente. O cluster "Médio" (grade 64.9) é o que mostra dificuldade real (56–89% de acerto, mais tentativas). Correlação Spearman ρ=0.296 positiva (tentar mais → melhor nota) é coerente com este padrão. Documentado explicitamente no Achado para alertar notebooks subsequentes.

**A trabalhar a seguir:** Task 3 — Seção 3 (Estrutura de assignments e dificuldade por problema).

## 2026-04-29 - eda: Task 3 - Seção 3 — Estrutura de assignments e dificuldade

- Seção 3 já estava escrita no notebook como trabalho em progresso (células 3365699b–08b3e673); o código não havia sido executado ainda
- Executado notebook para verificar outputs reais; código funcionou sem erros
- Corrigida a única divergência encontrada: A4 amplitude hardcoded como 31.8pp → corrigido para 32.4pp calculado (P107 17.5% → P44 49.9% = 32.4pp); todos os demais valores estavam corretos
- Plot salvo em `results/sec3_correct_rate_by_problem.png` (137K, 5 subplots barplot por assignment)
- Ranking de dificuldade por assignment computado e exibido na saída da célula; discutido no markdown pós-código
- Citações a Shi et al. (2022) presentes em: header da Seção 3, pré-código de 3.1, pré-código de 3.2, pós-código de 3.2
- Notebook re-executado sem erros após correção do markdown
- Veredito: PASS (correção de 1 valor hardcoded incorreto)

**Achados principais:**
- Release/Train: exatamente 10 KCs por assignment × 5 assignments, 221–234 estudantes, 23.70% correto global (vs 23.68% no paper)
- A3 é o assignment mais difícil (19.07% correto); A5 o mais fácil (30.40%)
- Problema mais difícil: P102 em A2 (8.9%); mais fácil: P57 em A5 (62.5%)
- Amplitudes intra-assignment: A1=41.2pp, A2=43.7pp, A3=20.7pp, A4=32.4pp, A5=43.5pp — todas ≥ 20pp confirmando sinal discriminativo

**A trabalhar a seguir:** Task 4 — Seção 4 (Curvas de aprendizado e sequências).

## 2026-04-29 - eda: Task 4 - Seção 4 — Curvas de aprendizado e sequências

- Inseridas 7 novas células após a Seção 3: cabeçalho "## 4", pré-código 4.1, código 4.1, pós-código 4.1, pré-código 4.2, código 4.2, pós-código 4.2
- **Seção 4.1 (Curvas de aprendizado):** calcula tentativa ordinal por estudante × assignment (sorted por ServerTimestamp), agrega taxa de acerto por tentativa ordinal, plota primeiras 30 tentativas de cada assignment; tabela de tendência (tentativas 1–5 vs 26–30) gerada automaticamente
- **Seção 4.2 (Distribuição de sequências):** calcula tamanho de sequência (Run.Program) por estudante × assignment, plota histograma com linha de truncagem = 50 e boxplot por assignment; tabela com % de estudantes afetados por assignment
- Plots salvos: `results/sec4_learning_curves.png`, `results/sec4_sequence_distribution.png`
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`; Achado cells atualizadas com valores reais calculados
- Veredito: PASS na primeira tentativa

**Achados principais:**
- A1 é o único assignment com curva crescente (+6.6pp de tentativas 1–5 para 26–30): sinal de aprendizagem detectável
- A2–A5 mostram curvas decrescentes (A4: −25.8pp, A5: −23.5pp): artefato de ordenação intra-assignment (problemas fáceis tentados primeiro), não regressão de aprendizagem
- Distribuição de sequências: mediana = 32, P95 = 109.3, max = 272 tentativas por estudante × assignment
- 28.3% dos pares (estudante, assignment) têm seq_len > 50; 58.1% dos estudantes têm ≥1 assignment afetado pela truncagem
- A3 (assignment mais difícil) é o mais afetado: 39.3% dos estudantes com seq_len > 50 (mediana 38, max 272)
- A5 (mais fácil) tem menor taxa de afetados: 17.1% (mediana 24)
- Truncagem em 50 é conservadora: mediana global 32 < 50; apenas a cauda é afetada

**A trabalhar a seguir:** Task 5 — Seção 5 (Análise do Score e desbalanceamento).

## 2026-04-29 - eda: Task 5 - Seção 5 — Análise do Score e desbalanceamento

- Inseridas 7 novas células após Seção 4: cabeçalho "## 5", pré-código 5.1, código 5.1, pós-código 5.1, pré-código 5.2, código 5.2, pós-código 5.2
- **Seção 5.1 (Distribuição do Score):** calcula proporção de Score=0 / parcial / Score=1 a partir de `runs_rel`; plota histograma com bins alinhados aos três intervalos + zoom em scores parciais; reporta 200 valores únicos de Score
- **Seção 5.2 (Imbalance ratio):** calcula n_correto / n_incorreto / imbalance_ratio por assignment e global; plota stacked bar (proporção) + bar chart (imbalance ratio); justifica AUC como métrica primária
- Plots salvos: `results/sec5_score_distribution.png`, `results/sec5_imbalance.png`
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achados principais:**
- Score = 0.0: 19.802 (42.3%); Score = 1.0: 11.098 (23.7%); 0 < Score < 1: 15.925 (34.0%)
- 200 valores únicos de Score — frações racionais de testes passados (e.g., 0.2727 ≈ 3/11, 0.50 = 1/2)
- CLAUDE.md estimava ~37% parcial; dado real é 34.0% — divergência mínima (3pp), documentada no Achado
- Imbalance global: 3.22:1 (76.3% incorretos); A3 tem o maior (4.24:1), A5 o menor (2.29:1)
- Um classificador-baseline "sempre incorreto" atingiria 76.3% de acurácia — comprova inadequação da acurácia

**A trabalhar a seguir:** Task 6 — Seção 6 (Evolução do código e Compile.Error).

## 2026-04-29 - eda: Task 6 - Seção 6 — Evolução do código e Compile.Error

- Inseridas 7 novas células após Seção 5: cabeçalho "## 6", pré-código 6.1, código 6.1, pós-código 6.1, pré-código 6.2, código 6.2, pós-código 6.2
- **Seção 6.1 (Taxa de Compile.Error):** filtra `Compile.Error` e `Run.Program` de `rel_train_main`; calcula n e taxa CE/(RP+CE) por assignment; plota barplot com linha de média global; tabela de summary gerada via `display()`
- **Seção 6.2 (Diversidade de CodeStateID):** agrupa `Run.Program + Compile.Error` por (AssignmentID, ProblemID), conta `CodeStateID.nunique()`; plota boxplot de diversidade por assignment; reporta top-5 problemas mais diversos e cobertura total de CodeStateID
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achados principais:**
- Release/Train: 40.858 Compile.Error em 87.683 submissões de usuário — taxa global de 46.6%
- Por assignment: A1=56.3% (mais alto, estudantes adaptando ambiente), A2=45.9%, A4=45.0%, A3=44.5%, A5=36.5% (mais baixo)
- Taxa Release/Train (46.6%) é maior que All (30.27%) porque o All inclui os eventos Compile (filhos 1:1 de Run.Program) no denominador
- Média de 937 CodeStateIDs únicos por problema (σ=403); variação 349 (P31-A5) a 2.114 (P102-A2)
- Curiosidade dataset: 100% dos CodeStateIDs de Compile.Error já aparecem em Run.Program — snapshots de código com erro de compilação coincidem com estados submetidos via Run.Program por outros estudantes
- Markdown conecta explicitamente Compile.Error → decisão srcML com citação a Pankiewicz, Shi & Baker (2025)

**Bug/inconsistência anotada:** 100% de sobreposição entre CodeStateIDs de Compile.Error e Run.Program é inesperado — pode indicar que o dataset CSEDM reutiliza CodeStateIDs entre estudantes para snapshots idênticos (deduplicação no nível do conteúdo, não da instância), ou que a coincidência é artefato do split Release/Train específico. Não impacta a modelagem; CodeStateID continua sendo o link correto para o código.

**A trabalhar a seguir:** Task 7 — Seção 7 (Padrões temporais e procrastinação).

## 2026-04-29 - eda: Task 7 - Seção 7 — Padrões temporais e procrastinação

- Inseridas 6 novas células após Seção 6: cabeçalho "## 7", pré-código 7.1, código 7.1, pré-código 7.2, código 7.2, pós-código unificado
- **Seção 7.1 (Atividade semanal):** adiciona coluna `ts` (datetime) a `rel_train_main`, calcula semana relativa ao início do semestre, plota (a) eventos por semana com linhas de deadline por assignment e (b) eventos por dia da semana; reporta atividade noturna (0h–3h) e dia mais ativo
- **Seção 7.2 (Procrastinação):** define deadline observada por assignment (último Run.Program), calcula `days_before_deadline` para cada Run.Program, agrega volume e taxa de acerto por dias de antecedência, plota barplot (volume) e lineplot (acurácia); calcula correlação de Spearman (ρ=-0.046) entre antecedência e acerto
- Variável intermediária `runs_rel7` criada para evitar sobrescrever `runs_rel` usado em seções anteriores
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achados principais:**
- Atividade em apenas 7 de 11 semanas do semestre — bursts de 5–6 dias por assignment, sem atividade entre assignments
- Domingo mais ativo (23.8% dos eventos); atividade noturna 0h–3h responde por 33.4% dos eventos
- 58.4% das tentativas de Run.Program ocorrem nos 2 últimos dias (D-0 + D-1): forte procrastinação
- Taxa de acerto maior no dia do prazo (D-0: 27.6%) do que 3+ dias antes (22.1%) — contraintuitivo
- Correlação Spearman ρ=-0.046 (p<10⁻²³): antecedência não melhora desempenho neste dataset

**Implicação documentada no markdown:** A estrutura em janelas por assignment valida o protocolo treino-por-assignment do Code-DKT; a procrastinação favorece DKT/Code-DKT (modelagem sequencial) sobre BKT estacionário.

**A trabalhar a seguir:** Task 8 — Seção 8 (Correlação de features com Label).

## 2026-04-29 - eda: Task 8 - Seção 8 — Correlação de features com Label

- Inseridas 7 novas células após Seção 7: cabeçalho "## 8", pré-código 8.1, código 8.1, pós-código 8.1, pré-código 8.2, código 8.2, pós-código 8.2
- **Seção 8.1 (Spearman):** carrega `early.csv` de Release/Train, constrói features por (SubjectID, ProblemID): `first_score` (Score da 1ª tentativa), `n_attempts`, `score_mean`, `score_max`, `n_compile_errors`; merge com `Attempts` de early.csv; calcula Spearman ρ vs Label para 6 features; plota barplot de ρ e heatmap de correlação entre features
- **Seção 8.2 (Decision Tree):** ajusta `DecisionTreeClassifier(max_depth=5, random_state=42)` com as mesmas 6 features; extrai Gini importances; plota barplot de importância e barplot de |ρ| Spearman lado a lado para comparação; imprime Top-5 features
- Nota sobre First-attempt AUC presente em parágrafo introdutório da Seção 8
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achados principais:**
- Top-5 por Spearman |ρ|: Attempts (−0.678), n_attempts (−0.668), score_mean (+0.587), n_compile_errors (−0.569), first_score (+0.462) — todas p < 10⁻¹⁰⁰
- Top-5 por DT Gini: Attempts (0.792), score_max (0.192), n_attempts (0.007), score_mean (0.004), n_compile_errors (0.003)
- `Attempts` domina ambos os rankings — principal proxy de dificuldade por problema no cenário early
- Forte multicolinearidade entre `Attempts` e `n_attempts` (ρ > 0.99): medem o mesmo construct
- `n_compile_errors` tem Spearman alto (0.569) mas Gini baixo (0.003) — sinal capturado por `Attempts` quando este está disponível; relevante como feature independente no Code-DKT onde Compile.Error são eventos separados
- Confirmação empírica: incluir Compile.Error na sequência KT (Pankiewicz et al., 2025) é justificado pelos dados

**A trabalhar a seguir:** Todas as 8 tarefas do plano EDA estão completas. Próximo notebook: 02_preprocessing.ipynb.

## 2026-04-29 - eda: Task 8 (fix) - Seção 8 — Correlação de features com Label (late Label adicionada)

**Problema encontrado pelo evaluator:** Cell 91 carregava `late_rel` mas nunca calculava a correlação de Spearman para o Label late — apenas o Label early era analisado.

**Correção aplicada:**
- Adicionado bloco de código ao final de cell 91: merge de `late_rel` com `feats_df` (features de runs_rel8) para criar `late_feat`; cálculo de Spearman ρ para 5 features (`first_score`, `n_attempts`, `score_mean`, `score_max`, `n_compile_errors`) vs Label late; tabela impressa via `display()` e barplot exibido
- Cell 92 (markdown Achado) atualizada para incluir seção "Achado — late Label" com magnitudes de correlação para o cenário late, além do "Achado — early Label" já existente
- `late.csv` não contém coluna `Attempts` (apenas Label e IDs), então análise late usa as 5 features de runs em vez de 6 (sem `Attempts`)
- Notebook re-executado sem erros via `jupyter nbconvert --execute --inplace`

## 2026-04-29 - preprocessing: Task 1 - Setup e carregamento dos dados

- Criado `src/data_loader.py` com `load_main_table(split, data_root)` e `load_labels(split, data_root, which)`, com docstrings e suporte aos 5 splits do CSEDM
- Criado `notebooks/02_preprocessing.ipynb` com estrutura inicial: célula markdown de introdução explicando os dois splits (All/ vs Release/) e quando usar cada um, célula de setup (imports, SEED=42, paths, sys.path para src/), e 3 seções analíticas (1.1–1.3) seguindo o template didático (Contexto, Hipótese, Referência / Achado, Implicação)
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Benchmark de reprodutibilidade confirmado: Release/Train correto-rate = 23.70% vs 23.68% do paper (divergência < 0.02pp, apenas arredondamento)

**Achados principais:**
- All/Data: 360.176 eventos, 506 estudantes, 5 assignments
- Release/Train: 134.508 eventos, 246 estudantes; correto-rate 23.70%
- Release/Test: 32.372 eventos, 83 estudantes
- Todas as colunas críticas presentes; Score nulo fora de Run.Program (0 eventos errôneos)
- ServerTimestamp convertido para datetime64[UTC] no load_main_table — ordenação cronológica correta garantida

**A trabalhar a seguir:** Task 2 — Filtragem por modelo (filter_for_bkt_dkt e filter_for_code_dkt).

## 2026-04-29 - preprocessing: Task 2 - Filtragem por modelo

- Adicionadas `filter_for_bkt_dkt(df)` e `filter_for_code_dkt(df)` a `src/data_loader.py` com docstrings e assertions internas de EventType
- `filter_for_bkt_dkt`: filtra `EventType == 'Run.Program'`, cria `correct = (Score == 1.0).astype(int)`, assertiva garante que apenas `{'Run.Program'}` passou
- `filter_for_code_dkt`: filtra `EventType in {'Run.Program', 'Compile.Error'}`, `correct = (Run.Program AND Score == 1.0).astype(int)`, ordena por (SubjectID, AssignmentID, ServerTimestamp), assertiva garante que apenas o conjunto permitido passou
- Adicionada Seção 2 ao notebook (3 células: pré-código, código, pós-código) seguindo o template didático
- Célula de código aplica os filtros nos 4 splits relevantes e executa 6 assertions inline + log de estatísticas
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achados principais:**
- BKT/DKT — Release/Train: 46.825 eventos (apenas Run.Program), 23.70% corretos
- BKT/DKT — Release/Test: 10.845 eventos, 21.18% corretos
- Code-DKT — Release/Train: 87.683 eventos (46.825 Run.Program + 40.858 Compile.Error), 12.66% corretos
- Code-DKT — Release/Test: 21.527 eventos (10.845 + 10.682), 10.67% corretos
- Todas as 6 assertions passaram: EventType, binaridade de `correct`

**Nota:** A taxa de corretos do Code-DKT (12.66%) é inferior à do BKT/DKT (23.70%) porque os 40.858 Compile.Error entram como `correct=0`, diluindo a proporção. A Hipótese original previa ~13.49% — o valor real é 12.66% (diferença de ~0.83pp). Não é bug: resulta da contagem exata de 40.858 Compile.Error vs estimativa da Seção 1.

**A trabalhar a seguir:** Task 3 — Construção de sequências KT (build_sequences).

## 2026-04-29 - preprocessing: Task 3 - Construção de sequências KT

- `build_sequences(df, assignment_id)` já estava implementada em `src/data_loader.py` (adicionada junto com as funções de filtragem na Task 2)
- Seção 3 do notebook já continha célula pré-código (Contexto/Hipótese/Referência), célula de código com chamadas a `build_sequences`, e célula pós-código com esquema de dados completo
- Notebook executado via `jupyter nbconvert --execute --inplace` — sem erros
- Todos os assertions passaram: `is_first_attempt` cobre exatamente 1 True por (SubjectID, ProblemID), ordenação cronológica verificada em todas as sequências

**Achados principais:**
- AssignmentIDs reais em Release/Train: [439, 487, 492, 494, 502] (não são 1–5 sequenciais)
- A1 (ID=439): 233 estudantes, comprimento médio 37.6, máximo 155
- is_first_attempt cobre 2271 pares únicos (SubjectID, ProblemID) em A=439
- Contagem de sequências BKT/DKT e Code-DKT coincide por assignment (as diferenças de filtragem não eliminam estudantes, apenas eventos)

**Nota:** AssignmentIDs não são sequenciais (439, 487, 492, 494, 502) — referência ao longo do projeto deve usar esses IDs inteiros, não posições 1–5.

**A trabalhar a seguir:** Task 4 — Truncagem e validação (últimas 50 tentativas, Shi et al. 2022).

## 2026-04-29 - preprocessing: Task 4 - Truncagem e validação

- Adicionada `truncate_sequences(sequences, max_len=50)` a `src/data_loader.py` com docstring completa
- Lógica: mantém os últimos `max_len` eventos (tail cronológico); recalcula `is_first_attempt` dentro da janela truncada via `duplicated(subset=['ProblemID'], keep='first')`; índice resetado
- Adicionadas 3 células ao notebook (pré-código, código, pós-código) seguindo o template didático, formando a Seção 4.1
- Célula de código: constrói sequências completas para todos os 5 assignments (BKT/DKT + Code-DKT), trunca, executa assertions `all(len(seq['events']) <= 50 ...)` para todos os modelos/assignments, e verifica `is_first_attempt` pós-truncagem
- Estatísticas de truncagem reportadas: % de sequências afetadas, comprimento médio antes/depois
- Taxa de corretos calculada antes e depois da truncagem; divergência explicada no Achado
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na primeira tentativa

**Achados principais:**
- BKT/DKT: 17–39% das sequências truncadas por assignment (A5 menos afetado 17.1%, A3 mais afetado 39.3%)
- Code-DKT: 35–67% das sequências truncadas (muito mais afetadas pela adição de Compile.Error que infla o comprimento)
- Taxa de corretos BKT/DKT: 23.70% antes → 27.97% após truncagem (+4.27pp)
- Taxa de corretos Code-DKT: 12.66% antes → 19.87% após truncagem (+7.21pp)
- Divergência em relação ao valor bruto é esperada e explicada: os eventos mais recentes refletem o aprendizado acumulado (fase pós-familiarização), por isso têm maior taxa de acerto
- is_first_attempt recalculado corretamente na janela truncada; assertions passam

**A trabalhar a seguir:** Task 5 — Serialização dos artefatos.

## 2026-04-29 - preprocessing: Task 5 - Serialização dos artefatos

- Adicionadas 3 células ao notebook (pré-código, código, pós-código) formando a Seção 5.1
- Construção e truncagem das sequências de teste para todos os 5 assignments (BKT/DKT + Code-DKT)
- Artefatos serializados: `results/sequences_bkt_dkt.pkl` (9.4 MB) e `results/sequences_code_dkt.pkl` (10.4 MB) via `pickle.dump`
- Célula de código imprime estatísticas detalhadas: número de sequências, comprimento (min/média/max), eventos total, taxa de corretos — para train e test, por assignment
- Markdown Achado documenta: tabela de estatísticas consolidadas, nota sobre Release/Test ter apenas 3 assignments com dados, schema completo dos artefatos (chaves, tipos, descrição), colunas do events DataFrame
- Bug identificado e corrigido: `Release/Test` tem apenas 3 assignments (A439, A487, A492) — A494 e A502 retornam listas vazias; a função `artifact_stats` foi ajustada para pular listas vazias com `if not seqs: continue`
- Notebook executado 2× sem erros via `jupyter nbconvert --execute --inplace`
- Veredito: PASS na segunda tentativa (primeira falhou por `ValueError: min() iterable argument is empty`)

**Achados principais:**
- BKT/DKT train: 1.134 sequências (5 assignments), len médio 32.2, máx 50, taxa corretos 27.97%
- BKT/DKT test:  236 sequências (apenas A439, A487, A492), len médio 33.3, taxa corretos 26.70%
- Code-DKT train: 1.134 sequências (5 assignments), len médio 39.2, taxa corretos 19.87%
- Code-DKT test:  236 sequências (apenas A439, A487, A492), len médio 41.5, taxa corretos 18.94%
- Comprimento médio Code-DKT > BKT/DKT (39.2 vs 32.2) confirma que Compile.Error inflam o comprimento das sequências
- Release/Test sem A494 e A502: comportamento esperado — o split de avaliação do paper Shi et al. (2022) cobre apenas os primeiros 3 assignments

**Dataset inconsistency note:** A ausência de A494 e A502 em Release/Test é documentada no Achado. Os artefatos mantêm as listas vazias para esses assignments para preservar compatibilidade de indexação; os notebooks de modelagem devem filtrar `{aid: seqs for aid, seqs in artifact['test'].items() if seqs}` antes de avaliar.

**A trabalhar a seguir:** pipeline preprocessing completo — todas as 5 tarefas concluídas.

## 2026-04-29 - preprocessing: Task 5 (fix) - Serialização dos artefatos — adicionar número de estudantes

**Problema apontado pelo evaluator:** A célula markdown final (bda503c4) apresentava apenas contagens de sequências (1.134 para train, 236 para test), que somam sequências por assignment e sobrestimam o número de estudantes únicos. A estatística "número de estudantes" estava ausente.

**Correção aplicada:**
- `artifact_stats()` (célula c154834c) atualizada para calcular `unique_students = len({seq['subject_id'] for seqs in seqs_by_aid.values() for seq in seqs})` e imprimir `Estudantes únicos: N` antes de `Sequências total`
- Célula markdown final (bda503c4) atualizada: tabela de estatísticas consolidadas ganhou coluna "Estudantes" explicitando 246 estudantes no train e 83 no test para ambos os artefatos
- Notebook re-executado sem erros via `jupyter nbconvert --execute --inplace`

## 2026-04-29 - insights_extraction: Task 1 - Síntese: imbalance, sequências e perfis de estudante

- Criado `docs/eda_insights.md` (15.949 bytes) com 3 seções analíticas cobrindo os achados críticos da EDA
- Cada achado referenciado à célula específica do notebook (e.g., "01_eda.ipynb — Seção 5.2, célula de código")
- Valores extraídos das saídas das células dos notebooks executados (não hardcoded)

**Achados documentados:**

**Seção 1 — Imbalance:**
- Global BKT/DKT: 3,22:1 (76,3% incorretos, 23,7% corretos) — Release/Train
- Por assignment: A3 (492) pior (4,24:1, 19,07% corretos), A5 (502) melhor (2,29:1, 30,40%)
- Code-DKT (com Compile.Error): 12,66% corretos antes da truncagem → 19,87% após
- Compile.Error rate: 46,6% das submissões (40.858 de 87.683 eventos Code-DKT)
- Justificativa para AUC como métrica primária: acurácia trivial de 76,3% seria alcançada por classificador "sempre incorreto"

**Seção 2 — Sequências:**
- Distribuição BKT/DKT (1.134 pares estudante × assignment): mediana=32, média=41,3 (±32,9), P95=109,3, máx=272
- 28,3% dos pares afetados pela truncagem em 50 (58,1% dos estudantes em ao menos 1 assignment)
- A3 mais afetado (39,3%), A5 menos (17,1%)
- Code-DKT: 35–67% das sequências truncadas (vs 17–39% no BKT/DKT) — Compile.Error infla comprimento médio para 70–92 eventos
- Taxa de corretos aumenta após truncagem: BKT/DKT +4,27pp (→27,97%), Code-DKT +7,21pp (→19,87%)
- is_first_attempt recalculado corretamente na janela truncada (assertion confirmada em 02_preprocessing.ipynb)

**Seção 3 — Perfis de estudante:**
- K-Means k=3 (SEED=42), 453 estudantes com features completas
- Silhouette k=2=0,285 (máximo) vs k=3=0,237 (escolhido por interpretabilidade)
- Perfis: Alto desempenho (139, 30,7%, X-Grade 73,8), Médio (66, 14,6%, X-Grade 64,9), Em risco (248, 54,7%, X-Grade 55,9)
- Achado inesperado: "Em risco" tem acerto eventual 97–99% mas apenas 2,0–4,6 tentativas/assignment — indica baixo engajamento, não dificuldade
- Dropout A1→A5: ~4,7pp (89,9% completaram todos os 5 assignments)
- Release/Test: apenas 3 assignments com dados (A439, A487, A492); A494 e A502 sem sequências de teste

**Verificação:** `python3 -c "... p.stat().st_size > 500 ..."` — PASS (15.949 bytes)

## 2026-04-29 - insights_extraction: Task 2 - Implicações das decisões de pré-processamento

- Adicionada Seção 4 em `docs/eda_insights.md` com 3 subseções cobrindo os três critérios de aceitação

**Seção 4.1 — Por que Compile.Error entra no Code-DKT (mas não em BKT/DKT):**
- Justificativa arquitetural: BKT/DKT recebem apenas (ProblemID, correct) — sem mecanismo para processar código não-compilável; Code-DKT extrai features via srcML a cada passo do LSTM, inclusive de Compile.Error
- Citação a Pankiewicz, Shi & Baker (2025): srcML-DKT inclui Compile.Error com correct=0 e features srcML; arquitetura LSTM+atenção idêntica ao Code-DKT original
- Citação a Shi et al. (2022): Code-DKT original requeria código compilável (javalang), descartava Compile.Error
- Impacto quantitativo documentado: 40.858 Compile.Error / 87.683 total Code-DKT = 46,6%; taxa corretos 23,70% → 12,66%
- Justificativa empírica: Spearman ρ=−0,569 entre n_compile_errors e Label (Seção 8.1 do EDA)
- Implicação: artefatos separados (sequences_bkt_dkt.pkl vs sequences_code_dkt.pkl); notebooks 04–06 não devem misturá-los

**Seção 4.2 — Justificativa do threshold Score == 1.0:**
- Dados quantitativos de Release/Train (01_eda.ipynb, Seção 5.1): Score=0.0 → 42,3%; Score=1.0 → 23,7%; parcial → 34,0%; 200 valores únicos
- Raciocínio analítico em 4 pontos: separação natural de classes, consistência com conceito de maestria, reprodutibilidade (benchmark 23,70% vs 23,68% do paper), binarização necessária para Bernoulli (BKT/DKT/Code-DKT)
- Partial scores explicados como frações racionais de testes automatizados

**Seção 4.3 — Rationale para usar Release/ em vez de All/:**
- Tabela comparativa: Fall 2019 vs Spring 2019; 506 vs 329 estudantes; taxa corretos 19,65% vs 23,70%
- 0 sobreposição de SubjectIDs confirmada (01_eda.ipynb, Seção 1.1.4)
- Três razões: reprodutibilidade (23,70% vs 23,68%), separação de populações (0 overlap), protocolo de avaliação (Release/Test tem os 3 assignments do paper)

**Verificação:** `python3 -c "... p.stat().st_size > 500 ..."` — PASS (26.573 bytes)

**A trabalhar a seguir:** Task 3 — Recomendações para notebooks 03-07 (sinalização de risco por assignment).
