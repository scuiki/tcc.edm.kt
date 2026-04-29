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
