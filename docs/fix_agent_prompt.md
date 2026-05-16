# Prompt: Fix Agent — Pipeline TCC EDM (pós-migração Spring 2019)

## Contexto do projeto

TCC 1 de Engenharia de Computação aplicando Educational Data Mining ao dataset CSEDM (ProgSnap2 v6). Pipeline de notebooks Jupyter implementa três modelos de Knowledge Tracing (BKT, DKT, Code-DKT) para comparação. O código-fonte usa Python 3.10+ com PyTorch, pyBKT, scikit-learn, srcML.

**Antes de qualquer ação, leia os dois arquivos abaixo em ordem:**

1. `CLAUDE.md` — fonte da verdade sobre o projeto: dataset, splits, definições de modelagem, critérios de conclusão
2. `docs/pipeline_review_2026-05-15.md` — relatório completo da revisão que originou este prompt: lista todos os problemas encontrados, evidências, localização exata e contexto de cada bloqueador

## O que aconteceu

Em 2026-05-15, o dataset foi migrado de Release/ (329 alunos, CSEDM Data Challenge) para **Spring 2019 completo** (410 alunos, protocolo Shi et al. 2022). O artefato central (`results/sequences_bkt_dkt.pkl`) foi regenerado corretamente por `02_preprocessing.ipynb` (328 train + 82 test, 5 assignments no test set). Porém, dois notebooks ficaram com saídas stale da versão anterior e precisam ser corrigidos.

## Bloqueadores que você deve resolver

### BLOQUEADOR 1 — `04_bkt.ipynb` nunca re-executado após migração

**Situação atual:**
- `results/sequences_bkt_dkt.pkl` contém dados Spring 2019: A439 train=307 alunos, 9,754 eventos; todos os 5 assignments têm dados de teste (A494=62 test, A502=61 test)
- `notebooks/04_bkt.ipynb` tem saídas stale de Release/: cell 7 mostra `n_train events = 7,417`; cell 20 mostra A494/A502 como "n/a (sem teste)"
- Cells 3-4 do notebook (assertions anti-stale adicionadas pós-migração) não têm nenhum output — nunca foram executadas
- `bkt.json` tasks 1-5 marcadas como `"pending"`; bkt_results.pkl contém resultados de Release/

**O que fazer:**
1. Executar o notebook do zero com o PKL atual:
   ```bash
   .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
     notebooks/04_bkt.ipynb --ExecutePreprocessor.timeout=600
   ```
2. Verificar que o notebook executou sem erros e que os outputs agora mostram:
   - Cell 3: tabela com 5 assignments, todos com n_test > 0
   - Cell 4: `EVAL_AIDS = [439, 487, 492, 494, 502]` (assertion passa)
   - Cell 7: `n_train events ≈ 9,754` para A439 (não 7,417)
   - Cell 16: 5 assignments na tabela de all-attempts AUC (não 3)
   - Cell 20: nenhum assignment com "n/a (sem teste)"
3. Após execução bem-sucedida, atualizar `bkt.json`: marcar tasks 1-5 como `"complete"` (task 6 já está `"complete"`)
4. Se o notebook falhar por qualquer razão:
   - Verifique se os patches do pyBKT estão aplicados no `.venv` (3 patches em `pyBKT/util/metrics.py` e `pyBKT/fit/EM_fit.py` — veja `.claude/projects/*/memory/feedback_pybkt_compat.md`)
   - Verifique se `results/sequences_bkt_dkt.pkl` existe e tem o schema correto: chaves `train`, `test`, `assignment_ids`, `max_len`, `seed`, `description`

**NÃO modifique o código do notebook** — apenas re-execute. Se encontrar erro de execução, investigue o erro e corrija apenas o necessário para fazer o notebook rodar com os dados corretos.

---

### BLOQUEADOR 2 — `kc_correctness_A487/A492/A494.json` são arquivos vazios

**Situação atual:**
- `results/kc_correctness_A487.json`: 2 bytes, contém `{}`
- `results/kc_correctness_A492.json`: 2 bytes, contém `{}`
- `results/kc_correctness_A494.json`: 2 bytes, contém `{}`
- `results/kc_correctness_A439.json`: 1.6MB, 5103 entries (de Release/Train, mai/8) — válido para verificação de estrutura
- `results/kc_correctness_A502.json`: 1.1MB, 3940 entries (de Release/Train, mai/8) — válido para verificação de estrutura

O harness marcou Task 6 como "complete" pois o AC só verifica existência dos arquivos, não o conteúdo. A tarefa 6 no `notebooks/03b_kc_generation.ipynb` é o "KC Correctness Labeling": para cada submissão **incorreta** de `Run.Program` no train split, chama o LLM (claude-haiku-4-5-20251001) para identificar quais KCs o estudante não dominou.

**O que fazer:**
1. Leia o código da Task 6 no `notebooks/03b_kc_generation.ipynb` (seção 6.x) para entender a lógica de cache
2. Identifique se a célula considera `{}` como "cache hit válido" — se sim, isso é o bug: arquivos vazios não devem ser tratados como cache válido
3. Delete os 3 arquivos vazios:
   ```bash
   rm results/kc_correctness_A487.json results/kc_correctness_A492.json results/kc_correctness_A494.json
   ```
4. Re-execute apenas a célula da Task 6 (ou o notebook completo com `--ExecutePreprocessor.timeout=600`):
   ```bash
   .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
     notebooks/03b_kc_generation.ipynb --ExecutePreprocessor.timeout=600
   ```
   **ATENÇÃO:** A execução da Task 6 faz chamadas à API Claude Haiku para processar submissões incorretas. Ela deve ser custosa (~$39 conforme estimativa do plano). ANTES de executar, confirme com o usuário se ele quer pagar esse custo agora. Se o usuário não quiser pagar, apenas corrija o bug de cache e deixe documentado.
5. Se o notebook executar sem erros, verificar que os 3 arquivos agora têm conteúdo:
   ```python
   import json
   for aid in [487, 492, 494]:
       d = json.load(open(f'results/kc_correctness_A{aid}.json'))
       print(f'A{aid}: {len(d)} entries')
   ```
   Esperar: centenas a milhares de entries por assignment.

**Se a Task 6 não puder ser re-executada agora:** apenas corrija o bug de cache (para que `{}` não seja tratado como cache válido) e atualize `kc_generation.json` task 6 para `"pending"`. Não marque como complete se os arquivos estiverem vazios.

---

## Tarefa adicional — Re-executar `01_eda.ipynb` (AVISO, não bloqueador)

**Situação atual:**
- O código foi atualizado (cell 16 usa `load_spring2019_split`; cell 51 carrega `DATA_ROOT / 'MainTable.csv'`), mas o notebook não foi re-executado
- Saídas stale: cell 61 mostra "246 estudantes" (Release/Train) em vez dos 328/410 do Spring 2019
- `eda.json` tasks 1-8 estão todas em `"pending"` — correto

**O que fazer:**
1. Re-executar o notebook:
   ```bash
   .venv/bin/jupyter nbconvert --to notebook --execute --inplace \
     notebooks/01_eda.ipynb --ExecutePreprocessor.timeout=600
   ```
2. Verificar que cell 61 agora mostra contagens compatíveis com Spring 2019 (não "246 estudantes")
3. Se o notebook executar sem erros, atualizar `eda.json` tasks 1-8 para `"complete"`
4. Se o notebook falhar, investigue o erro — pode ser que alguma célula ainda referencie um path de Release/ que não existe mais

---

## O que NÃO fazer

- **Não modifique `src/data_loader.py`** sem entender o impacto no pipeline completo
- **Não regenere os caches KC** (`kc_raw_A*.json`, `kc_clusters_A*.json`, `kc_descriptions_A*.json`) — eles são de Release/Train mas são funcionalmente equivalentes para Spring 2019 (mesmos problemas, mesmas soluções corretas). Isso é opcional e caro.
- **Não altere o código de `compute_auc` ou `predict_bkt`** sem consultar o usuário — há uma questão metodológica em aberto sobre `is_first_attempt` pós-truncagem que está sendo investigada separadamente
- **Não force o re-treino do BKT** se o notebook executar mas produzir AUC diferente do paper — documente a divergência (já prevista), não tente "corrigir" o resultado
- **Não cometa** nada sem confirmar com o usuário

## Fontes de referência dentro do projeto

- `CLAUDE.md` — instruções, fatos críticos do dataset, definições de modelagem (lido no início)
- `docs/pipeline_review_2026-05-15.md` — relatório completo desta revisão (lido no início)
- `.harness/HARNESS_PLAN.md` — padrão didático de células (Contexto/Hipótese/Referência → código → Achado/Implicação)
- `results/sequences_bkt_dkt.pkl` — artefato correto (Spring 2019, 328+82, 5 assignments)
- `.claude/projects/*/memory/feedback_pybkt_compat.md` — 3 patches pyBKT obrigatórios se o venv for recriado

## Critérios de conclusão

A tarefa está completa quando:
1. `notebooks/04_bkt.ipynb` executa sem erros e mostra Spring 2019 data (5 EVAL_AIDS, A439 n_train≈9,754)
2. `results/bkt_results.pkl` contém AUC calculadas dos dados Spring 2019
3. `kc_correctness_A487.json`, `A492.json`, `A494.json` têm conteúdo (ou o bug de cache foi corrigido e está documentado)
4. `notebooks/01_eda.ipynb` executa sem erros com saídas de Spring 2019
