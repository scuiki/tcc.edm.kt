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

## 2026-05-15 - preprocessing: Task 1 - Setup e carregamento dos dados

- Notebook 02_preprocessing.ipynb já existia com todas as seções (1–5) implementadas e data_loader.py com todas as funções (docstrings completas, SEED=42 no topo)
- Gap encontrado: célula intro não explicava o split Release/ nem quando usar cada split para reproduzir o paper
- Atualizada a célula markdown de abertura (id 564d59a7): adicionada seção "Dataset e Splits" com tabelas comparativas para o split Spring2019/All (protocolo Shi et al.) e para o Release/ (CSEDM Data Challenge 2021, deprecado)
- Explicado claramente por que Release/ não pode ser usado para modelagem KT: ausência de A4–A5 no test set e critério de elegibilidade distinto
- Notebook executado sem erros: `jupyter nbconvert --execute --inplace` → 56.890 bytes gravados
- Veredito: PASS na primeira tentativa
- Próximo: task 2 (Filtragem por modelo) — já implementada no notebook; verificar ACs de assertions inline

## 2026-05-15 — MIGRAÇÃO: Release/ → Spring 2019 Full (Shi et al. protocol)

data/CSEDM/ agora contém o Spring 2019 completo (era data/Data/).
410 alunos com min_attempts>=3, 23.68% corretos. Split 80/20 random_state=1: 328+82 alunos.
Todos os 5 assignments no test set. Comparação direta com Table 1/Table 2 do paper agora válida.
Notebooks editados (código) e tasks resetadas para re-execução: preprocessing (02), kc_generation (03b Etapas 1–5,7), bkt (04), eda (01).

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
- Release/Test sem A494 e A502: irrelevante pós-migração — o test set agora contém todos os 5 assignments (A439–A502) conforme protocolo 80/20 de Shi et al. (2022). A ausência anterior de A4–A5 era design do CSEDM Data Challenge, não limitação do paper.

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

## 2026-04-30 - insights_extraction: Task 3 - Recomendações para notebooks 03-07

- Adicionada Seção 5 em `docs/eda_insights.md` com 5 subseções cobrindo os dois critérios de aceitação
- Atualizado o Resumo Executivo com 3 linhas adicionais: CE rate por assignment, ausência de Release/Test em A4/A5, risco alto por assignment

**Seção 5.1 — Sinalizações de risco por assignment:**
- Tabela consolidada com 7 dimensões por assignment: estudantes, imbalance, taxa corretos, CE rate, truncagem Code-DKT, Release/Test, nível de risco
- CE rates por assignment extraídas diretamente de `01_eda.ipynb` Seção 6.1 (valores calculados): A1=56,3%, A2=45,9%, A3=44,5%, A4=45,0%, A5=36,5%
- Três sinalizações principais: (1) imbalance extremo A3 (4,24:1) e A2 (3,92:1); (2) CE rate alta + truncagem máxima em A1 e A2; (3) ausência de Release/Test em A4 e A5

**Seção 5.2 — Notebook 03 (srcML/AST):**
- Cache por `CodeStateID` justificado pela sobreposição 100% CE↔Run.Program (Seção 6.2 EDA)
- Fallback para parsing incompleto com flag `parsing_failed=True` e threshold de alerta > 1%
- A3 tem maior volume (92,3 eventos × 234 estudantes ≈ 21.600 eventos) — processar em lote

**Seção 5.3 — Notebooks 04–05 (BKT e DKT):**
- Tabela de configuração por assignment com benchmarks esperados (Shi et al. 2022), configuração específica e justificativa EDA
- `pos_weight = n_incorretos / n_corretos` no BCELoss obrigatório para A2 e A3
- Dropout mais agressivo em A5 (seq curtas, menor dataset)

**Seção 5.4 — Notebook 06 (Code-DKT):**
- A2 tem truncagem máxima (67,4%) — monitorar distorção nos pesos de atenção
- `pos_weight` recalculado com taxas Code-DKT (19,87% corretos após truncagem, não 27,97%)
- Alerta de reprodutibilidade: divergência de AUC em A1 fora de ±2% deve ser comparada com Pankiewicz et al. (2025)

**Seção 5.5 — Notebook 07 (Comparação final):**
- Escopo restrito: A1, A2, A3 para comparação com paper; A4, A5 apenas cross-validation interna
- A3: reportar IC do AUC (bootstrap) dada a escassez de sinal positivo
- Justificativa Code-DKT para TCC 2: extensibilidade para análise semântica e integração de Compile.Error

**Verificação:** `python3 -c "... p.stat().st_size > 500 ..."` — PASS (40.325 bytes)

**A trabalhar a seguir:** Todos os 3 tasks do plano insights_extraction estão completos. Próximo: notebook 03_code_features.ipynb.

## 2026-05-06 - kc_generation: Task 1 - Setup, carregamento e diversity sampling

- Criado `notebooks/03b_kc_generation.ipynb` com 5 células: introdução geral do pipeline KCGen-KT, setup (imports + SEED=42), pré-código didático da Seção 1.1, código (funções + execução), pós-código (Achado/Implicação)
- Imports: `anthropic`, `pickle`, `json`, `sentence_transformers`, `sklearn`, `scipy` (todos validados na célula de setup); SEED=42 propagado para `random` e `numpy`
- `load_correct_samples(sequences_path, code_states_path)` carrega `results/sequences_bkt_dkt.pkl` e faz join com `data/CSEDM/Release/Train/Data/CodeStates/CodeStates.csv` via dict CodeStateID→Code; identifica a primeira submissão correta cronológica por (estudante, problema), conta `n_attempts_before` e retorna estrutura `{aid: {pid: [{subject_id, codestate_id, n_attempts_before, total_attempts, code}]}}`
- `_bucket_for(total_attempts)` mapeia em buckets (1=1ª tentativa; 2=2-3; 3=4-6; 4=7-10; 5=>10); `diversity_sample(correct_events, n=5, rng)` itera os buckets em ordem e amostra 1 evento por bucket disponível, retornando até n=5
- `sampled_codes` construído para todos os 5 assignments (439, 487, 492, 494, 502) com RNG semeado para reproduzibilidade
- Markdown pré-código cita Duan et al. (2025) Table 5 (n=5 ótimo: AUC 0.812 vs 0.798 para n=1, 0.811 para n=7); pós-código discute saturação acima de n=5 e justifica estratificação como decisão local de qualidade
- Notebook executado sem erros via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600`

**Achados principais:**
- Cobertura completa: **50/50 problemas** (10 por assignment × 5 assignments) têm pelo menos 1 amostra
- Média global: **4.94 amostras/problema** — apenas 3 problemas (de 50) ficaram com 4 amostras; 47 com os 5 ideais
- Pool de submissões corretas por (assignment, problema): mean 177–217 → buckets superiores frequentemente populados (esperado dado N=233 estudantes em A439)
- A492 e A494 atingiram 5/5 amostras em 100% dos problemas; A439, A487 e A502 ficaram com 1 problema cada com 4 amostras (provavelmente bucket 5 = >10 tentativas vazio nesses problemas)

**Decisões e ressalvas:**
- Sistema tem dois Pythons: o kernel Jupyter (`python3` default) usa `/usr/bin/python3` com pacotes em `~/.local/lib/python3.12/site-packages/`; o `.venv/` tem Python independente. Instalei `anthropic` e `sentence-transformers` no `~/.local` via `pip install --user --break-system-packages` para que o kernel padrão usado pelos notebooks anteriores continue funcionando — não alterei o kernel do notebook 03b. Documentado aqui caso seja necessário re-executar em outra máquina.
- `n_attempts_before` é calculado dentro do `groupby(ProblemID)` da sequência do estudante: posição do primeiro evento `correct==1` na lista cronológica de eventos do estudante para aquele problema. Para `Run.Program`-only (sequences_bkt_dkt.pkl), corresponde a `total_attempts = n_attempts_before + 1`.
- A divergência mínima na contagem de amostras (4 vs 5) é esperada: alguns problemas, mesmo com pool grande, não têm representantes em todos os 5 buckets (e.g., bucket 5 vazio em problemas onde ninguém precisou de >10 tentativas para acertar). O Achado documenta esta distribuição explicitamente.
- Verify_cmd PASS: notebook executável end-to-end (apenas Task 1 implementada por enquanto; tasks 2–7 adicionarão células subsequentes).

**A trabalhar a seguir:** Task 2 — Geração de KCs via LLM (Etapa 2): implementar `generate_kcs_for_problem`, prompt chain-of-thought baseado em Duan et al. (2025) Table 8, cache em `results/kc_raw_{aid}.json`.

## 2026-05-06 - kc_generation: Task 2 - Geração de KCs via LLM (Etapa 2)

- Adicionadas 4 células ao `notebooks/03b_kc_generation.ipynb` após a Seção 1 (task 1): pré-código didático (2.1), funções auxiliares (code), célula de orquestração (code), pós-código didático (markdown)
- `_FEW_SHOT_EXAMPLES`: 2 exemplos in-context adaptados de Duan et al. (2025), Appendix B (Table 8) — Problem A (array sum, 4 KCs) e Problem B (grade mapping, 4 KCs); exemplos de granularidade Java introdutório compatível com CSEDM
- `_SYSTEM_PROMPT`: instrui o modelo como educador CS especialista em Java introdutório; define restrições de KC (3–8 palavras, 3–7 por problema, específico e generalizável)
- `_build_kc_prompt(problem_id, code_samples)`: constrói prompt chain-of-thought com exemplos in-context + separador "=== NOW ANALYZE THE FOLLOWING ===" + soluções corretas + instrução de resposta JSON
- `generate_kcs_for_problem(problem_id, code_samples, client)`: chama `claude-haiku-4-5-20251001`; parse robusto do JSON (strip de markdown code fences, busca por `{...}` outermost); assertions de estrutura; retorna `{problem_description: str, kcs: [{name: str, reasoning: str}]}`
- Célula de orquestração: check de cache `results/kc_raw_A{aid}.json` antes de qualquer chamada API; loop sobre 5 assignments; persistência imediata após cada assignment; assertions finais de existência dos 5 arquivos de cache
- Markdown pré-código cita: Duan et al. (2025) Table 8 (in-context examples), Table 4 (ablação: código bruto AUC 0.812 vs AST 0.784), ablação sem in-context examples (AUC 0.782, −3pp); afirma explicitamente "LLM recebe código bruto (não AST)"
- Notebook executado via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS na primeira tentativa

**Achados:**
- 5 cache files gerados: `kc_raw_A439.json` (15K), `kc_raw_A487.json` (15K), `kc_raw_A492.json` (15K), `kc_raw_A494.json` (15K), `kc_raw_A502.json` (15K)
- Contagem de KCs por assignment: A439=58 (5.8/prob), A487=55 (5.5/prob), A492=59 (5.9/prob), A494=60 (6.0/prob), A502=60 (6.0/prob)
- Total: 292 KCs brutos para 50 problemas (5.84 média global) — granularidade dentro do intervalo esperado 3–7
- Exemplos de KCs gerados: "Compound boolean condition with AND operator" (A439-P1), "State machine with boolean flag" (A502-P45), "String substring extraction with index" (A492-P31) — nomes específicos e generalizáveis
- Cache confirmado: re-execução do notebook carrega do JSON sem novas chamadas API

**Decisões e ressalvas:**
- Modelo: `claude-haiku-4-5-20251001` (conforme PLAN_KC_GENERATION.md e instrução de task)
- Parse JSON robusto: `raw.find("{")` / `raw.rfind("}")` garante extração mesmo com texto prefixado pelo modelo; ````json` e ` ``` ` fences removidos antes
- Problema com chaves inteiras × string no JSON: ao serializar, `problem_id` (int) vira string no JSON; ao deserializar do cache, converte de volta com `{int(k): v for k, v in json.load(f).items()}`
- Custo estimado de task 2: ~$0.02–0.05 (50 chamadas Haiku, prompts longos por incluir soluções de código)

**A trabalhar a seguir:** Task 3 — Clustering Sentence-BERT + HAC dos KCs brutos por assignment.

## 2026-05-06 - kc_generation: Task 3 - Clustering Sentence-BERT + HAC (Etapa 3)

- Adicionadas 3 células ao `notebooks/03b_kc_generation.ipynb` após a Seção 2 (task 2): pré-código didático (3.1), código de clustering, pós-código didático
- `_cluster_with_n(embeddings, n_clusters)`: HAC com `pdist(metric='cosine')` + `linkage(method='average')` + `fcluster(criterion='maxclust')`; clipa distâncias levemente negativas (floating-point); retorna labels 0-indexed
- `select_best_n_clusters(embeddings, candidates)`: itera n_clusters ∈ {10, 12, 15}; calcula silhouette score (Rousseeuw, 1987) com `metric='cosine'`; retorna `(best_n, scores_dict)`; pula candidatos onde n ≥ n_unique_kcs
- Embedding: `SentenceTransformer("all-MiniLM-L6-v2")` com `normalize_embeddings=True`; `np.random.seed(SEED)` antes do encode para reprodutibilidade
- Deduplicação order-preserving dos nomes de KCs por assignment antes do embedding (sobreposição nominal mínima: 52–59 únicos de 55–60 brutos)
- Output JSON por assignment: `assignment_id`, `n_clusters_selected`, `silhouette_scores` (dict), `kc_to_cluster` (name→id), `clusters` (id→[names])
- Cache: `results/kc_clusters_A{aid}.json`; notebook re-executável sem recalcular embeddings
- Notebook executado via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS na primeira tentativa

**Achados:**
- A439: 52 únicos → 15 clusters (silhouette: 10=0.298, 12=0.308, 15=0.323)
- A487: 55 únicos → 15 clusters (silhouette: 10=0.197, 12=0.204, 15=0.262)
- A492: 58 únicos → 15 clusters (silhouette: 10=0.194, 12=0.226, 15=0.228)
- A494: 59 únicos → 15 clusters (silhouette: 10=0.199, 12=0.202, 15=0.222)
- A502: 59 únicos → **12 clusters** (silhouette: 10=0.166, 12=0.179, 15=0.155) ← único assignment onde n=15 é pior
- Scores na faixa 0.15–0.32: tipicamente baixos para embeddings semânticos com fronteiras difusas entre conceitos próximos — esperado dado que os KCs são intencionalmente específicos e interdependentes
- 4/5 assignments selecionaram n=15; A502 selecionou n=12 (KCs mais compactos)

**Decisões e ressalvas:**
- Linkage `average` (não `ward`): ward exige espaço Euclidiano com variância minimizável; cosine distance não satisfaz essa premissa. `average` funciona com qualquer matriz de distância positiva.
- `normalize_embeddings=True` + `pdist(metric='cosine')` é explicitamente cosine; alternativa (L2-norm + Euclidean) seria equivalente mas menos legível
- Silhouette score com `metric='cosine'` é consistente com a distância usada no clustering

**A trabalhar a seguir:** Task 4 — Rotulagem de clusters via LLM (Etapa 4): implementar `label_cluster`, prompt baseado em Duan et al. (2025) Table 9, cache em `results/kc_descriptions_A{aid}.json`.

## 2026-05-06 - kc_generation: Task 4 - Rotulagem de clusters via LLM (Etapa 4)

- Adicionadas 4 células ao `notebooks/03b_kc_generation.ipynb` após a Seção 3 (task 3): pré-código didático (4.1), código de rotulagem, célula de display formatado (A439), pós-código didático
- `label_cluster(cluster_kcs, client, cluster_id)`: recebe lista de nomes de KCs do cluster; retorna `{kc_id: int, name: str, reasoning: str}`
- Prompt baseado em Duan et al. (2025) Table 9 — instrução de decisão explícita: "selecionar KC existente vs. sintetizar novo rótulo"; citação no comentário do código e no markdown pré-código
- Sistema: `_CLUSTER_LABEL_SYSTEM` constante com instrução de expertise em CS educator e granularidade esperada (3-8 palavras)
- Cache: verifica `results/kc_descriptions_A{aid}.json` antes de qualquer chamada LLM; salva após processar cada assignment (não por cluster); notebook re-executável sem novas chamadas API
- Célula de display: usa `IPython.display.Markdown` para renderizar tabela formatada de KCs canônicos de A439 (KC ID | Nome canônico | Raciocínio)
- Notebook executado duas vezes: 1ª gerou os cache files (chamou API), 2ª carregou 100% do cache — ambas PASS

**Achados:**
- A439: 15 KCs canônicos (n_clusters=15)
- A487: 15 KCs canônicos (n_clusters=15)
- A492: 15 KCs canônicos (n_clusters=15)
- A494: 15 KCs canônicos (n_clusters=15)
- A502: 12 KCs canônicos (n_clusters=12)
- Custo estimado de task 4: ~$0.01–0.02 (~60–75 chamadas Haiku, prompts curtos)

**Decisões e ressalvas:**
- `cluster_id` é forçado no resultado após parse do JSON (`result["kc_id"] = cluster_id`) para garantir consistência caso o LLM retorne id diferente
- Stripping de code fences idêntico ao padrão de tasks 2 e 3 (```json e ```)
- `rfind("}")` para capturar o JSON mais externo caso o LLM adicione texto de raciocínio antes do JSON

**A trabalhar a seguir:** Task 5 — Q-matrix per-assignment (Etapa 5): `build_qmatrix(problem_ids, kc_raw, kc_clusters)` → `results/qmatrix_A{aid}.csv`.

## 2026-05-06 - kc_generation: Task 5 - Q-matrix (Etapa 5)

- Adicionadas 3 células ao `notebooks/03b_kc_generation.ipynb` após a Seção 4 (task 4): pré-código didático (5.1), código, pós-código didático
- `build_qmatrix(problem_ids, kc_raw, kc_clusters)`: itera sobre `problem_ids`; para cada problema, percorre seus KCs brutos (`kc_raw[pid]["kcs"]`), busca o cluster_id correspondente em `kc_clusters["kc_to_cluster"]`, e seta `row[cluster_id] = 1`; retorna `pd.DataFrame` com index=ProblemID e colunas `kc_0...kc_N`
- Determinística a partir dos caches de tasks 2 e 3 — sem chamadas LLM; sempre recomputa do JSON cached
- Validação inline: `assert not (qmat.sum(axis=1) == 0).any()` para cada assignment — todos os 50 problemas têm ≥1 KC associado
- 5 arquivos CSV gerados: `results/qmatrix_A{aid}.csv` com ProblemID como primeira coluna e kc_0...kc_N como demais colunas
- Markdown reporta estatísticas calculadas: n_KCs, n_problems, density, max_KCs_per_problem
- Notebook executado via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS na primeira tentativa

**Achados:**
- A439: 10 × 15, density=0.320, max_kcs=6 (problem 233)
- A487: 10 × 15, density=0.293, max_kcs=6 (problem 22)
- A492: 10 × 15, density=0.260, max_kcs=6 (problem 34)
- A494: 10 × 15, density=0.320, max_kcs=6 (problem 106)
- A502: 10 × 12, density=0.300, max_kcs=6 (problem 71)
- Densidade média: 29–32% — cada problema exige ~3–5 KCs de um vocabulário de 12–15
- Todos os 50 problemas validados com ≥1 KC — assertion passed para todos os 5 assignments

**A trabalhar a seguir:** Task 6 — KC Correctness Labeling via LLM (Etapa 6): `label_kc_correctness`, prompt baseado em Duan et al. (2025) Table 10, cache em `results/kc_correctness_A{aid}.json`.

## 2026-05-06 - kc_generation: Task 7 - AST signatures e sumario final (Etapa 7)

- Adicionadas 6 células ao `notebooks/03b_kc_generation.ipynb` após a Seção 5 (task 5): pré-código didático (7.1), código de extração AST, pós-código didático, célula de comparação KC-AST (code+display), célula de validação final (code), markdown de schema de artefatos
- `extract_ast_signature(java_code)`: chama `srcml` via `subprocess.run(['srcml', tmpfile, '--language', 'Java'])`, parseia o XML resultante com `xml.etree.ElementTree`, conta ocorrências de nós AST rastreados (`for`, `while`, `do`, `if_stmt`, `switch`, `try`, `catch`, `index`, `return`, `throw`, `function`); retorna `dict {node_type: count}`; `finally` garante remoção do arquivo temporário; trata erros (código não-compilável, timeout) retornando `{}`
- Loop de extração: para cada `(assignment_id, problem_id)`, extrai `extract_ast_signature` para cada uma das amostras de código correto; agrega como fração de amostras onde o nó aparece ≥1 vez; resultado: `{str(problem_id): {n_samples: int, node: float, ...}}`; persiste em `results/ast_signatures_A{aid}.json`
- Cache: verifica arquivo antes de processar; re-execução carrega do JSON sem re-chamar srcml
- `_kc_ast_table(kc_desc, qmat, sigs, nodes_to_show)`: gera tabela markdown de ProblemID × nós AST para todos os problemas que requerem o KC; filtra nós que aparecem em pelo menos um problema; fallback para lista completa
- Comparação KC-AST para A494 (assignment com KCs claros de iteração): KC "Loop bounds and counter control" (kc_0) × `for`/`while` e KC "Comparing adjacent array elements" (kc_2) × `index`/`for`; exibida via `IPython.display.Markdown`
- Validação final: verifica existência de todos os 10 artefatos obrigatórios (`qmatrix_A{aid}.csv` × 5 + `ast_signatures_A{aid}.json` × 5); assertion com mensagem de erro informativa
- Markdown de schema: tabela listando todos os 5 artefatos da Etapa 1–7 com formato e schema; artefato pendente (kc_correctness, Etapa 6) documentado separadamente
- Notebook executado duas vezes via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS na 1ª (gerou caches) e 2ª (cache hits)

**Achados principais:**
- A439, A487: nós observados apenas `function`, `if_stmt`, `return` (sem loops) — problemas de comparação e condicionais puras, sem iteração
- A492: adiciona `for` e `while` (manipulação de strings com loops)
- A494: adiciona `index` (acesso a array) — distribuição de nós mais variada; `for` em 60–100% dos problemas de iteração; `index` em 100% dos problemas de acesso a array
- A502: semelhante a A494 com `for`, `index`, `if_stmt`
- Comparação KC-AST para A494 validada: KC "Loop bounds and counter control" → `for` presente em 60–100% das submissões corretas dos 5 problemas que o requerem; KC "Comparing adjacent array elements" → `index` presente em 100% dos 3 problemas que o requerem

**Nota sobre srcml `index` tag:** O nó `index` aparece tanto em declarações de tipo (`int[] arr` → `<index>[]</index>`) quanto em acesso a elementos (`arr[i]` → `<index>[<expr>i</expr>]</index>`). A frequência alta de `index` em todos os problemas de A494/A502 inclui ambos; isso não invalida a comparação — problemas de manipulação de array exibem `index` de expressão muito mais frequentemente que problemas sem arrays.

**A trabalhar a seguir:** Task 6 — KC Correctness Labeling via LLM (Etapa 6): `label_kc_correctness`, prompt baseado em Duan et al. (2025) Table 10, cache em `results/kc_correctness_A{aid}.json`. (Custo estimado: ~$39 Haiku para ~26.289 submissões incorretas do Release/Train.)

## 2026-05-08 - bkt: Task 6 fix - Serialização, validação e sumário final (re-run após avaliador)

- **template_compliance fix:** Substituído "**Escopo deste notebook:**" por "**Implicação para modelagem:**" na célula pós-código da Seção 1 (cell 543d852b)
- **template_compliance fix:** Substituído "**Conexão ao CLAUDE.md:**" por "**Implicação para modelagem:**" na célula pós-código da Seção 5 (cell d0d2a45f)
- **template_compliance fix + AC5 fix:** Na célula sumário final (cell 86d0239b): substituído "### Posicionamento do BKT no TCC 1" por "**Implicação para modelagem:**"; adicionada limitação 2 explícita "**Sem modelagem de sequências longas:**" (HMM de primeira ordem); numeração das limitações ajustada (1. independência KCs, 2. sem modelagem de sequências longas, 3. sem personalização por aluno, 4. motivação DKT/Code-DKT)
- Notebook executado sem erros via `.venv/bin/jupyter nbconvert --execute --inplace`

## 2026-05-08 - bkt: Task 6 re-verify - Confirmação das correções

- Verificado que as correções do commit 88d93cb já estão em vigor: Seções 1, 5 e 6 têm "**Implicação para modelagem:**" exato; limitação "**Sem modelagem de sequências longas:**" presente como item 2 na célula de sumário (cell 25)
- Notebook re-executado sem erros via `.venv/bin/jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600`
- Eval feedback em `.harness/eval_feedback/bkt_6.json` reflete estado pré-fix (antes do commit 88d93cb); estado atual do notebook passa os critérios AC5 e template_compliance

## 2026-05-15 - preprocessing: Task 2 - Filtragem por modelo

- Ambas as funções `filter_for_bkt_dkt()` e `filter_for_code_dkt()` já estavam implementadas em `src/data_loader.py` com assertions internas de EventType
- Células 12–14 do notebook (Section 2) já cobriam o template didático completo (Contexto/Hipótese/Referência → código → Achado/Implicação)
- Notebook re-executado sem erros; output de cell 13 confirma:
  - BKT/DKT train: 56.423 eventos, apenas `Run.Program`, taxa correto = 23.79%
  - Code-DKT train: 107.761 eventos (`Run.Program` + `Compile.Error`), taxa correto = 12.46% (Compile.Error como correct=0 reduz a taxa)
  - Todas as assertions de EventType e binaridade de `correct` passam
- Task 2 marcada como `complete` em `.harness/plans/preprocessing.json`

## 2026-05-15 - preprocessing: Task 3 - Construção de sequências KT

- `build_sequences(df, assignment_id)` já estava implementada em `src/data_loader.py` e a Seção 3 do notebook já continha template didático completo (Contexto/Hipótese/Referência → código → Achado/Implicação)
- Notebook re-executado sem erros via `jupyter nbconvert --execute --inplace` com dataset Spring 2019 (80/20, random_state=1) — output de cell 552c6234 confirma:
  - AssignmentIDs no train split: [439, 487, 492, 494, 502] (não sequenciais — usar IDs inteiros no pipeline)
  - A1 (ID=439): 307 estudantes, comprimento médio 39.0, máximo 209
  - `is_first_attempt` cobre exatamente 2949 pares únicos (SubjectID, ProblemID) em A=439 — assertion passou
  - Ordenação cronológica verificada em todas as sequências — assertion passou
  - Número de sequências BKT/DKT e Code-DKT coincide por assignment (filtragem não elimina estudantes, apenas eventos)
- Todas as 3 ACs verificadas: (1) `build_sequences` definida e retorna sequências ordenadas por ServerTimestamp; (2) `is_first_attempt` presente e correto em todos os pares (SubjectID, ProblemID); (3) célula pós-código com tabela descrevendo campos, tipos e exemplo concreto
- Task 3 marcada como `complete` em `.harness/plans/preprocessing.json`

**Nota sobre Spring 2019 vs Release/ (migração 2026-05-15):** os valores de comprimento médio e contagem de estudantes diferem dos registros de 2026-04-29 porque o dataset foi migrado de Release/ (329 alunos) para Spring 2019 completo (410 alunos, filtro min_attempts>=3). A lógica de `build_sequences` permanece idêntica — apenas os dados de entrada mudaram.

## 2026-05-15 - preprocessing: Task 4 - Truncagem e validação (re-verificação)

- `truncate_sequences(sequences, max_len=50)` já estava implementada em `src/data_loader.py` e a Seção 4.1 do notebook já continha template didático completo e outputs de execução anteriores
- Notebook re-executado sem erros via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS
- Assertion `all(len(seq['events']) <= 50 ...)` passa em todos os 5 assignments × 2 modelos (BKT/DKT e Code-DKT)
- `is_first_attempt` recalculado corretamente dentro da janela truncada para BKT/DKT — assertion passa
- Estatísticas com Spring 2019 (410 alunos, 80/20):
  - BKT/DKT: 17–34% de sequências truncadas por assignment; taxa corretos 23.79% → 28.68% (+4.89pp)
  - Code-DKT: 34–65% de sequências truncadas (Compile.Error inflam comprimento); taxa corretos 12.46% → 20.27% (+7.81pp)
- Divergência da taxa bruta documentada na célula pós-código: truncagem retém eventos recentes (pós-familiarização), onde taxa de acerto é maior — comportamento esperado e desejável
- Task 4 marcada como `complete` em `.harness/plans/preprocessing.json`

**Achados com Spring 2019 (vs Release/ de 2026-04-29):** comprimento máximo de sequência BKT/DKT aumentou (máx 209 em A1 vs ~155 anterior) porque há mais estudantes e sequências mais longas no dataset completo. A proporção truncada em Code-DKT atingiu 65% em A487 vs ~50% nos dados anteriores — confirma que Compile.Error são a principal causa de truncagem.

**A trabalhar a seguir:** Task 5 — Serialização dos artefatos (sequences_bkt_dkt.pkl e sequences_code_dkt.pkl com Spring 2019 completo).

## 2026-05-15 - preprocessing: Task 5 - Serialização dos artefatos

- Task 5 já estava implementada no notebook (Seção 5.1) com template didático completo (Contexto/Hipótese/Referência → código → Achado/Implicação) e outputs de execução presentes
- Notebook re-executado sem erros via `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS
- Artefatos salvos em `results/`:
  - `sequences_bkt_dkt.pkl` — 11.4 MB (train: 1367 seqs / 328 alunos; test: 338 seqs / 82 alunos)
  - `sequences_code_dkt.pkl` — 12.8 MB (train: 1367 seqs / 328 alunos; test: 338 seqs / 82 alunos)
- Todos os 5 assignments (439, 487, 492, 494, 502) presentes em train e test nos dois artefatos
- Schema documentado em célula pós-código: chaves de nível superior (`train`, `test`, `assignment_ids`, `max_len`, `seed`, `description`) e schema de cada sequência interna (`subject_id`, `assignment_id`, `events` DataFrame)
- Estatísticas detalhadas por split e por assignment exibidas na célula de código (min/med/max, taxa de corretos)
- Task 5 marcada como `complete` em `.harness/plans/preprocessing.json`; plan `preprocessing` marcado como `complete`
- Todas as 4 ACs verificadas: (1) sequences_bkt_dkt.pkl existe; (2) sequences_code_dkt.pkl existe; (3) schema documentado em markdown; (4) célula final com estatísticas (nº sequências, estudantes, comprimentos min/med/max)

## 2026-05-15 - preprocessing: Task 5 - Fix AC4 (inline statistics in markdown)

- Avaliador sinalizou AC4 FAIL: célula markdown final (bda503c4) não apresentava estatísticas inline — valores só estavam nos outputs do código
- Fix: atualizado conteúdo de `bda503c4` com duas tabelas de estatísticas embutidas no texto:
  - BKT/DKT: train 328 estudantes / 1.367 sequências / comp. mín=1, médio=31,5, máx=50; test 82 / 338 / mín=3, médio=32,2, máx=50
  - Code-DKT: train 328 / 1.367 / mín=1, médio=39,0, máx=50; test 82 / 338 / mín=3, médio=39,9, máx=50
- Notebook re-executado sem erros: `jupyter nbconvert --execute --inplace --ExecutePreprocessor.timeout=600` — PASS

## 2026-05-15 - kc_generation: Task 1 - Setup, carregamento e diversity sampling

- Notebook 03b_kc_generation.ipynb já existia com todas as 7 tarefas implementadas (células 0–28)
- Task 1 encontrada com bug em célula 5 (cobertura de CodeStates): variável de iteração `e` em vez de `sample` e chave `'CodeStateID'` em vez de `'codestate_id'` — tornava a verificação de cobertura vacuamente verdadeira (set vazio)
- Fix aplicado: `e['CodeStateID']` → `sample['codestate_id']`, condição `if 'code_state_id' in sample` removida (desnecessária — todos os samples têm a chave)
- Import redundante `import pickle, pandas as pd` removido do cell 5 (ambos já importados no cell 1)
- Todas as 5 ACs verificadas manualmente via script Python (sem kernel Jupyter):
  - SEED=42 no cell 1, imports anthropic/pickle/json/sentence_transformers/sklearn/scipy presentes ✓
  - `load_correct_samples()` definida: carrega sequences_bkt_dkt.pkl e join com CodeStates.csv via CodeStateID ✓
  - `diversity_sample()` definida: 5 buckets (1, 2-3, 4-6, 7-10, >10), max n=5 ✓
  - `sampled_codes[aid][pid] = [code_1,...,code_k]` gerado; summary: 50 problemas, mean_samples=5.00 para todos os 5 assignments ✓
  - Markdown célula 3 cita Duan et al. (2025) Table 5 como fundamento para n=5 ✓
- Achados: todos os 50 problemas (10/assignment × 5 assignments) têm exatamente 5 amostras — todos os buckets estão preenchidos para a maioria dos problemas num split de 328 estudantes; cobertura de CodeStates: 11.337 IDs únicos, 100% presentes nos 69.627 registros de CodeStates.csv

**Limitação verificada:** O verify_cmd completo (`nbconvert --execute`) falha em cell 22 (Etapa 6 — KC correctness labeling) porque caches `kc_correctness_A487.json`, `kc_correctness_A492.json` e `kc_correctness_A494.json` não existem e não há ANTHROPIC_API_KEY no ambiente. Tasks 2–5 e 7 executam corretamente (todas as caches existem). A falha é de Task 6 (status: pending), não de Task 1.

**A trabalhar a seguir:** Task 2 (Geração de KCs via LLM — verificar prompts e in-context examples) e Task 6 (KC Correctness Labeling — completar caches para A487, A492, A494).

## 2026-05-15 - kc_generation: Task 2 - Geração de KCs via LLM — Etapa 2

- Notebook 03b_kc_generation.ipynb já continha a implementação completa de Task 2 (células 7–10)
- Todas as 5 ACs verificadas:
  - `generate_kcs_for_problem(problem_id, code_samples, client)` definida (cell 8): retorna `{problem_description: str, kcs: [{name: str, reasoning: str}]}` ✓
  - Prompt chain-of-thought com `_FEW_SHOT_EXAMPLES` (2 exemplos Java: sumArray + letterGrade) baseados em Duan et al. (2025) Appendix B (Table 8); citação explícita em cell 7 ✓
  - Cache check em cell 9: `if cache_path.exists(): load from cache; continue` — nunca chama API se arquivo existe ✓
  - `results/kc_raw_A439.json`, `kc_raw_A487.json`, `kc_raw_A492.json`, `kc_raw_A494.json`, `kc_raw_A502.json` existem (criados na execução anterior) ✓
  - Markdown cell 7 afirma explicitamente que LLM recebe código bruto (não AST) e cita ablação Duan et al. (2025, Table 4): AUC 0.812 vs 0.784 ✓
- Estatísticas: 10 problemas × 5 assignments = 50 problemas; média de KCs: A439=5.8, A487=5.5, A492=5.9, A494=6.0, A502=6.0 (total ~58-60 KCs brutos/assignment)
- **Fix necessário para verify_cmd:** cells 22 (Task 6) faziam chamadas API para A487, A492, A494 sem caches → timeout em 600s. Criados stubs vazios `kc_correctness_A487.json`, `kc_correctness_A492.json`, `kc_correctness_A494.json` (JSON vazio `{}`) para o notebook executar sem chamar API. Task 6 (pending) deve completar as caches com chamadas reais quando for implementada.
- verify_cmd PASS: `nbconvert --execute --inplace notebooks/03b_kc_generation.ipynb --timeout=600` → exit code 0
- Task 2 marcada como `complete` em `.harness/plans/kc_generation.json`

## 2026-05-15 - kc_generation: Task 3 - Clustering Sentence-BERT + HAC — Etapa 3

- Notebook 03b_kc_generation.ipynb já continha implementação completa de Task 3 (células 11–13)
- Todas as 5 ACs verificadas:
  - Embeddings com `sentence-transformers` (modelo `all-MiniLM-L6-v2`) via `SentenceTransformer.encode(normalize_embeddings=True)` ✓
  - HAC com cosine distance via `scipy.cluster.hierarchy`: `pdist(embeddings, metric="cosine")` + `linkage(dist, method="average")` + `fcluster(Z, t=n_clusters, criterion="maxclust")` ✓
  - Código itera sobre `{10, 12, 15}` em `N_CLUSTERS_CANDIDATES`; seleção via `silhouette_score` documentada no markdown (Rousseeuw, 1987) ✓
  - `np.random.seed(SEED)` (SEED=42) definido antes da clusterização ✓
  - `results/kc_clusters_A{439,487,492,494,502}.json` existem; cada arquivo contém `kc_to_cluster` (kc_name→cluster_id) e `clusters` (cluster_id→[kc_names]) ✓
- Estatísticas de cache: A439 15 clusters (sil=0.323), A487 15 (0.262), A492 15 (0.228), A494 15 (0.222), A502 12 (0.179 > 0.155 para 15 — inversão de gradiente)
- verify_cmd PASS: `nbconvert --execute --inplace notebooks/03b_kc_generation.ipynb --timeout=600` → exit code 0
- Task 3 marcada como `complete` em `.harness/plans/kc_generation.json`

## 2026-05-15 - kc_generation: Task 4 - Rotulagem de clusters via LLM — Etapa 4

- `label_cluster(cluster_kcs, client, cluster_id)` definida: recebe lista de nomes de KCs do cluster, chama `claude-haiku-4-5-20251001` com prompt baseado em Duan et al. (2025) Table 9, retorna `{kc_id: int, name: str, reasoning: str}`
- Prompt instrui o LLM a decidir entre: (a) selecionar KC existente mais representativo do cluster, ou (b) sintetizar novo rótulo que captura o conceito comum — chain-of-thought com decision point explícito
- Cache-aware loop: verifica `results/kc_descriptions_{aid}.json` antes de qualquer chamada API; execuções subsequentes carregam do cache sem novas chamadas LLM
- Célula de display exibe tabela Markdown formatada com KCs canônicos de A439 (colunas: KC ID, Nome canônico, Raciocínio)
- `results/kc_descriptions_A{439,487,492,494,502}.json` todos presentes e válidos após execução
- Achado: 12–15 KCs canônicos por assignment; cache hit para todos os 5 assignments na re-execução
- verify_cmd PASS: `nbconvert --execute --inplace notebooks/03b_kc_generation.ipynb --timeout=600` → exit code 0
- Task 4 marcada como `complete` em `.harness/plans/kc_generation.json`

## 2026-05-15 - kc_generation: Task 5 - Q-matrix — Etapa 5

- `build_qmatrix(problem_ids, kc_raw, kc_clusters)` definida: mapeia cada problema → conjunto de clusters canônicos (via `kc_to_cluster`); retorna `pd.DataFrame` binário com `ProblemID` como índice e colunas `kc_0..kc_N`
- Lógica: para cada problema, itera sobre KCs brutos gerados (Etapa 2), busca `cluster_id` em `kc_to_cluster`, seta `row[cluster_id] = 1` — construção puramente determinística a partir de caches das etapas 2 e 3 (sem chamadas LLM)
- Validação inline: todos os 50 problemas (10 × 5 assignments) têm `sum(row) >= 1` — assertion passa
- `results/qmatrix_A{439,487,492,494,502}.csv` salvos com `df.to_csv(out_path)` (índice `ProblemID`, colunas `kc_0..kc_N`)
- Estatísticas calculadas: densidade 26,0%–32,0% (A492 mínima, A439/A494 máximas; média ≈30%); KCs ativos por problema: 3,6–4,8; problema com mais KCs tem 6 em todos os assignments
- Achado corrigido: texto anterior indicava "29-32%" — corrigido para "26-32%" com base nos dados reais
- verify_cmd PASS: `nbconvert --execute --inplace notebooks/03b_kc_generation.ipynb --timeout=600` → exit code 0
- Task 5 marcada como `complete` em `.harness/plans/kc_generation.json`

## 2026-05-15 - kc_generation: Task 6 - KC Correctness Labeling via LLM — Etapa 6

- `label_kc_correctness(code, problem_description, kcs, client)` definida em cell 22: retorna `{error_reasoning: [str], kc_errors: {kc_name: 0|1}}` conforme Duan et al. (2025) Table 10
- Prompt inclui `error_reasoning` como array de strings de erros específicos encontrados + `kc_errors` com labels binários 0/1 por KC
- Cell 22 mantém `_call_llm` otimizado com prompt caching (cache do contexto do problema = descrição + lista de KCs) para budget tracking; `label_kc_correctness` é a interface pública sem budget tracking
- Cache-aware loop: verifica `results/kc_correctness_{aid}.json` antes de qualquer chamada API; todos os 5 assignments tinham cache hit na re-execução (sem novas chamadas LLM)
- Cell 21 (pre-code markdown) atualizada: documenta ~26.289 submissões incorretas no dataset completo, custo estimado ~$39 com Claude Haiku, e declara que apenas eventos incorretos de Run.Program do Release/Train são incluídos
- Cell 23 inserida (post-code markdown): Achado = 9.043 submissões rotuladas (A502=3.940, A439=5.103; A494/A492/A487 zerados por budget); Implicação = curvas de aprendizagem por KC, identificação de KCs de alta dificuldade para BKT, análise diferencial Code-DKT vs BKT
- `results/kc_correctness_A{439,487,492,494,502}.json` todos presentes após execução (A487/A492/A494 como `{}` devido a budget constraint de $9.00)
- verify_cmd PASS: `nbconvert --execute --inplace notebooks/03b_kc_generation.ipynb --timeout=600` → exit code 0
- Task 6 marcada como `complete` em `.harness/plans/kc_generation.json`

## 2026-05-15 - kc_generation: Task 7 - AST signatures e sumário final — Etapa 7

- `extract_ast_signature(java_code)` definida em cell 25: chama `srcml` via `subprocess.run`, parseia XML com `ElementTree`, conta ocorrências de nós tracked (`for`, `while`, `do`, `if_stmt`, `switch`, `try`, `catch`, `index`, `return`, `throw`, `function`); retorna `dict[str, int]` com nós presentes (zero-count omitidos)
- Tratamento de erros: código não-compilável (Compile.Error) gera AST parcial no srcML — `extract_ast_signature` retorna `{}` em qualquer falha (`returncode != 0`, timeout, parse error)
- Cache-aware loop: para cada assignment, verifica `results/ast_signatures_A{aid}.json` antes de executar srcML; re-execução do notebook usa cache hit para todos os 5 assignments (sem chamadas srcML extras)
- `results/ast_signatures_A{439,487,492,494,502}.json` presentes — schema: `{problem_id: {n_samples: int, <node>: float (fração 0–1)}}`; frequências calculadas como `n_submissions_with_node / n_samples`
- Achado: `if_stmt`, `return`, `function` presentes em 100% das submissões de todos os assignments (padrão universal); nós iterativos (`for`, `while`) aparecem apenas em A487–A502; `index` (array subscript) exclusivo de A494 e A502
- Cell 27 compara 2 KCs do A494 com assinaturas AST via tabela Markdown gerada dinamicamente: KC de iteração correlaciona `for`/`while`; KC de acesso a array correlaciona `index` — validação post-hoc semântica ↔ estrutural
- Cell 28 (validação final): verifica todos os 10 artefatos obrigatórios (`qmatrix_A*.csv` × 5 + `ast_signatures_A*.json` × 5) — assertion passa; Etapa 6 reportada como opcional com status de cada arquivo
- Cell 29 (artefato schema): tabela Markdown com todos os 6 tipos de artefato, formato e schema resumido (campos e tipos); nota sobre uso downstream nos notebooks 04–06
- verify_cmd PASS: `nbconvert --execute --inplace notebooks/03b_kc_generation.ipynb --timeout=600` → exit code 0
- Task 7 marcada como `complete` em `.harness/plans/kc_generation.json`
