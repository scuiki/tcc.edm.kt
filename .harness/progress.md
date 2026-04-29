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
