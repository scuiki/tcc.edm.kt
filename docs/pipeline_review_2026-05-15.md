# Pipeline Review — TCC EDM (2026-05-15)

Revisão crítica do estado dos notebooks após a migração Release/ → Spring 2019 (Shi et al. 2022 protocol).

---

## 1. Sumário Executivo

O artefato central — `sequences_bkt_dkt.pkl` / `sequences_code_dkt.pkl` — foi gerado corretamente com Spring 2019 (328+82 alunos, 5 assignments no test set). `02_preprocessing.ipynb` está sólido e correto.

**Dois bloqueadores ativos impedem o avanço para DKT:**

1. `04_bkt.ipynb` **nunca foi re-executado após a migração** de 2026-05-15 — todas as saídas visíveis são de Release/ data (A439 n_train=7,417 vs 9,754 real; A494/A502 mostrados como "n/a" sem teste).
2. `kc_correctness_A487/A492/A494.json` são **arquivos vazios (`{}`)** — o harness marcou Task 6 como complete sem verificar o conteúdo; 3/5 assignments sem labeling de correctness.

Adicionalmente, `01_eda.ipynb` tem saídas stale de Release/Train e precisa re-execução.

---

## 2. Status por Notebook

### 02_preprocessing.ipynb — `preprocessing.json`

| Task | AC | Status | Evidência |
|---|---|---|---|
| 1 — Setup e split | 328 train + 82 test, 5 assignments, SEED=42 | ✓ | cell 3: 164k eventos; cell 4: assert 328/82/5 passa; taxa 23.79% |
| 2 — Filtragem | filter_for_bkt_dkt, filter_for_code_dkt, assertions EventType | ✓ | cell 13: BKT/DKT 56,423 / Code-DKT 107,761 eventos; assertions OK |
| 3 — Sequências KT | build_sequences, is_first_attempt, ordem cronológica | ✓ | cell 16: A439=307 estudantes; assert is_first_attempt único por (subj, prob) |
| 4 — Truncagem | truncate_sequences, assert ≤50, taxa corretos | ✓ | cell 19: assertion passa todos assignments; BKT/DKT 27.97% pós-truncagem |
| 5 — Serialização | sequences_bkt_dkt.pkl, sequences_code_dkt.pkl, schema, stats | ✓ | cell 22: ambos gerados; assert 5 assignments no test; schema documentado |

**Resultado: 5/5 tasks corretas e executadas com Spring 2019. Sem pendências.**

---

### 01_eda.ipynb — `eda.json`

| Task | AC | Status | Evidência |
|---|---|---|---|
| 1 — Seção 1 | Template didático, ProgSnap2 citado, duplicatas explicadas | ⚠ | Código provavelmente correto; saídas stale |
| 2 — Seção 2 | Template, SEED=42, 3 perfis nomeados | ⚠ | cell 44: "453/506" usa ALL split — número correto para esse escopo |
| 3 — Seção 3 | Plot dificuldade, ranking, citação Shi 2022 | ⚠ | cell 31 mostra "~410 estudantes" correto; demais outputs stale |
| 4 — Seção 4 | Curvas aprendizado, distribuição sequências, truncagem 50 | ✗ | cell 61: **"143 de 246 (58.1%)"** — 246 = Release/Train; Spring2019 train = 328 |
| 5 — Seção 5 | Histograma Score, parciais, imbalance, AUC justificada | ✗ | `runs_rel` baseado em Release/Train nos outputs |
| 6 — Seção 6 | Compile.Error rate, CodeStateIDs únicos, citação Pankiewicz 2025 | ✗ | cell 75: "46,825 únicos em 134,508 eventos" = Release/Train counts |
| 7 — Seção 7 | Atividade semanal, correlação timing-desempenho | ✗ | outputs de Release/ data |
| 8 — Seção 8 | Spearman, DT SEED=42, top-5 features, nota first-attempt | ✗ | cell 35: "early.csv (14317 linhas), assignments [439,487,492]" = Release/ |

**Resultado: código foi atualizado (cell 16 usa `load_spring2019_split`; cell 51 carrega Spring 2019 `MainTable.csv`), mas as saídas das seções 4-8 são stale de Release/Train. Notebook nunca re-executado pós-migração. Todos os status `"pending"` em `eda.json` estão corretos.**

---

### 03b_kc_generation.ipynb — `kc_generation.json`

| Task | AC | Status | Evidência |
|---|---|---|---|
| 1 — Diversity sampling | SEED=42, load_correct_samples, diversity_sample, 50/50 cobertura | ✓ | cell 4: mean pool=276 (Spring2019 ✓); cell 5: 11,337 CodeStateIDs verificados |
| 2 — KC generation LLM | generate_kcs_for_problem, cache, 5 JSON, código bruto | ⚠ | Cache de mai/6 (Release/Train); "cache hit" sem regenerar |
| 3 — Clustering SBERT+HAC | embeddings, HAC, silhouette, 5 JSON | ⚠ | Depende de Task 2; cache antigo; 4/5 n=15, A502 n=12 |
| 4 — Rotulagem clusters | label_cluster, cache, 5 JSON, tabela A439 | ⚠ | Cache de mai/6; KCs semanticamente válidos |
| 5 — Q-matrix | build_qmatrix, 5 CSV, density, ≥1 KC por problema | ✓ | density 0.26–0.32; assertion ≥1 KC passa; arquivos existem |
| 6 — KC Correctness | label_kc_correctness, cache, 5 JSON | ✗ | **A487/A492/A494: `{}` (0 entries)**; A439: 5103, A502: 3940 entries |
| 7 — AST signatures | extract_ast_signature, 5 JSON, comparação KC-AST | ✓ | Usa sampled_codes de Spring2019; validação A494 KC↔AST correta |

**Resultado: Task 1 e 7 corretas com Spring2019. Tasks 2-5 usam caches de Release/ (severidade baixa). Task 6 é BLOQUEADOR — 3/5 arquivos vazios.**

---

### 04_bkt.ipynb — `bkt.json`

| Task | AC | Status | Evidência |
|---|---|---|---|
| 1 — Investigação split + setup | Assert 328+82+5 assignments, tabela por split | ✗ | **cells 3-4: sem nenhum output** — adicionadas pós-migração, nunca executadas |
| 2 — Smoke test bkt.py | Import, train_and_evaluate A439 | ✗ | cell 7: `n_train=7,417` ← Release/A439 (233 alunos); Spring2019 teria ~9,754 |
| 3 — Treinamento 5 assignments | bkt_models, params, assertions | ✗ | outputs de Release/ |
| 4 — All-attempts AUC | 3 assignments avaliados (Release/ test), tabela | ✗ | cell 16: A439/A487/A492 apenas; Spring2019 teria 5 EVAL_AIDS |
| 5 — First-attempt AUC | First-attempt AUC, tabela comparativa | ✗ | cell 21: A439 63.82%; A494/A502 "n/a" — stale + discrepância metodológica |
| 6 — Serialização e sumário | bkt_results.pkl, 5 keys, schema | ✗ | pkl gerado com Release/ data; A494/A502 n_test=0 (hardcoded) |

**Resultado: BLOQUEADOR. Nenhuma task está correta. O notebook tem saídas de Release/ e nunca foi re-executado com Spring 2019.**

---

## 3. Problemas Encontrados

### BLOQUEADORES

**B1 — `04_bkt.ipynb`: saídas stale de Release/ data**
- **Localização:** notebook inteiro; cells 3-4 sem output; cells 7–25 com saídas de Release/
- **Evidência:**
  - `sequences_bkt_dkt.pkl` atual: A439 train=307 alunos, 9,754 eventos
  - cell 7 output: `n_train events = 7,417` (Release/A439 = 233 alunos)
  - cell 20: A494/A502 mostrados como "n/a (sem teste)" — pkl atual tem A494=62 e A502=61 estudantes de teste
  - cells 3-4 (assertions anti-stale adicionadas pós-migração) sem nenhum output
- **Causa:** notebook editado com novas assertions mas não re-executado; `bkt.json` tasks 1-5 permanecem `"pending"`
- **Impacto:** `bkt_results.pkl` contém AUC de Release/; comparação com Shi et al. é inválida

**B2 — `kc_correctness_A487/A492/A494.json`: arquivos vazios**
- **Localização:** `results/kc_correctness_A487.json` (2 bytes = `{}`), `A492.json` (2 bytes), `A494.json` (2 bytes)
- **Evidência:** `json.load` retorna dict vazio para os 3; A439=5103 entries (mai/8), A502=3940 entries (mai/8); A487/A492/A494 sobreescritos em mai/15 com `{}`
- **Causa provável:** durante re-execução de Task 6 em mai/15 com Spring2019 data, os caches antigos de A487/A492/A494 estavam ausentes (ou foram invalidados), e a nova execução escreveu `{}` em vez de chamar a API — possível bug no branch de escrita quando a API retorna resposta vazia ou ocorre erro silencioso
- **Impacto:** harness marcou Task 6 como "complete" pois o AC só verifica existência dos arquivos, não conteúdo; 3/5 assignments sem labeling de correctness

---

### AVISOS

**A1 — `01_eda.ipynb`: saídas stale de Release/Train**
- **Localização:** cells 61, 65, 68, 72, 75, 79, 81 (seções 4-8)
- **Evidência:** cell 61: "143 de 246 (58.1%)" — 246 = Release/Train; Spring2019 train = 328; cell 75: "46,825 únicos em 134,508 eventos" = Release/Train counts
- **Causa:** cell 51 foi atualizada para `pd.read_csv(DATA_ROOT / 'MainTable.csv')` (Spring2019), mas o notebook não foi re-executado
- **Impacto:** todas as análises de seções 4-8 reportam valores incorretos; `docs/eda_insights.md` baseado em Release/ data

**A2 — Metodologia de `is_first_attempt` após truncagem infla first-attempt AUC**
- **Localização:** `src/data_loader.py:196-202` (`truncate_sequences`); `notebooks/04_bkt.ipynb` cells 19-21
- **Problema:** `truncate_sequences` recalcula `is_first_attempt` como primeira ocorrência de `ProblemID` **na janela truncada** (últimas 50 tentativas). Para estudantes truncados (28.3% das sequências), um evento rotulado como "primeira tentativa na janela" é na verdade uma tentativa **posterior** ao verdadeiro primeiro encontro com o problema. Esses eventos tendem a ter: (a) resultado mais frequentemente correto (estudante já praticou); (b) P(L) mais alto no BKT (parâmetro atualizado em tentativas anteriores fora da janela). Isso infla artificialmente o first-attempt AUC.
- **Evidência:** A439 first-attempt AUC = 63.82% (Release/stale) vs paper 50.22% (+13.6pp). Para BKT, a predição na primeira tentativa de um KC é constante por KC (`P(L0)*(1-P(S)) + (1-P(L0))*P(G)`), e o AUC entre KCs diferentes pode ser acima de 0.5, mas +13.6pp é muito acima da faixa do paper.
- **Nota:** as saídas são stale; após re-executar com Spring2019 o valor pode mudar, mas o problema metodológico persiste
- **Ação:** documentar a discrepância explicitamente; calcular AUC apenas com sequências não-truncadas como sanity check; verificar se Shi et al. também recalculam is_first_attempt na janela truncada

**A3 — `predict_bkt`: alinhamento de predictions por posição pode ser frágil**
- **Localização:** `src/models/bkt.py:67-70`
- **Código crítico:**
  ```python
  df = df.reset_index(drop=True)
  preds = preds.reset_index(drop=True)
  df["correct_predictions"] = preds["correct_predictions"].values
  ```
- **Risco:** se pyBKT 1.4.1 reordenar o DataFrame internamente, `preds` não terá a mesma ordem de linhas que `df`. O join por posição (`.values`) seria silenciosamente errado.
- **Evidência mitigante:** `sequences_to_pyBKT_df` já ordena por `(user_id, skill_name, ServerTimestamp)` antes de `predict`; se pyBKT preservar essa ordem, o alinhamento é correto
- **Ação:** adicionar `assert len(df) == len(preds)` e validar empiricamente que AUC all-attempts coincide com cálculo manual

**A4 — KC correctness de A439/A502 são de Release/Train**
- **Localização:** `results/kc_correctness_A439.json` (1.6MB, mai/8), `A502.json` (1.1MB, mai/8)
- **Impacto:** gerados com submissões incorretas de Release/Train (246 alunos); Spring2019 train tem 328 alunos. Cria inconsistência entre assignments (A487/A492/A494 vazios vs A439/A502 de Release/).

---

### COSMÉTICOS

**C1** — `bkt.json` context (linha 17) menciona "Release/Test contém apenas A439/A487/A492 — A494/A502 ausentes por corte de data" — stale após migração; Spring2019 tem 5 assignments no test set

**C2** — `bkt.json` tasks 1-5 com `"pending"` enquanto notebook tem outputs (stale) — confunde estado do harness

**C3** — `docs/eda_insights.md` escrito com valores de Release/ (Release/Test com 3 assignments, 246 estudantes, etc.) — precisa ser re-gerado após EDA re-executado

**C4** — `kc_generation.json` context menciona "Use apenas Release/Train" e path `data/CSEDM/Release/Train/Data/CodeStates/CodeStates.csv` — stale; notebook já usa `data/CSEDM/CodeStates/CodeStates.csv`

---

## 4. Coesão entre Notebooks

| Fluxo de artefatos | Status | Observação |
|---|---|---|
| `02_preprocessing` → `sequences_bkt_dkt.pkl` | ✓ | Spring 2019; A439 train=307/test=77; todos 5 assignments no test |
| `02_preprocessing` → `sequences_code_dkt.pkl` | ✓ | Spring 2019; Code-DKT com Compile.Error correto |
| `sequences_bkt_dkt.pkl` → `03b` Task 1 | ✓ | load_correct_samples usa novo pkl; 11,337 CodeStateIDs verificados |
| `sequences_bkt_dkt.pkl` → `04_bkt` | ✗ | 04 não re-executado; cell 7 reflete Release/ (7,417 eventos) |
| `03b` caches (kc_raw/clusters/descriptions) → Tasks 3-5 | ⚠ | caches de Release/ (mai/6); pipeline executa mas KC source é Release/ |
| `03b` ast_signatures → futuro Code-DKT (06) | ✓ | usa sampled_codes de Spring2019; comparação KC-AST validada |
| `bkt_results.pkl` → notebook 07 (comparação final) | ✗ | stale de Release/; não pode ser usado para comparação com paper |
| `01_eda` → contexto analítico geral | ✗ | EDA reporta Release/ (246 alunos); preprocessing usa Spring2019 (328) |

---

## 5. Alinhamento com Shi et al. (2022)

| Dimensão do paper | Implementado | Alinhado? |
|---|---|---|
| Spring 2019, 410 alunos, min_attempts≥3 | `load_spring2019_split` com assert 328+82 | ✓ |
| Split 80/20, random_state=1 | `train_test_split(test_size=0.2, random_state=1)` | ✓ |
| KC = ProblemID, modelo por assignment | `skill_name = str(ProblemID)`; 5 modelos BKT independentes | ✓ |
| 5 assignments no test set | Confirmado no pkl; stale em 04_bkt (mostra 3) | ✓ (pkl) / ✗ (04) |
| Truncagem nas últimas 50 tentativas | `truncate_sequences(max_len=50)` + assertion | ✓ |
| Score == 1.0 como threshold "correto" | `filter_for_bkt_dkt` e `filter_for_code_dkt` | ✓ |
| First-attempt AUC como métrica primária | `compute_auc(first_attempt_only=True)` definida | ✓ (definição) / ⚠ (metodologia) |
| BKT A439 all-attempts AUC ≈ 63.78% ±4.68% | 65.88% stale (Release/) — dentro da margem | ⚠ stale |
| BKT A439 first-attempt AUC ≈ 50.22% ±2.86% | 63.82% stale (Release/) — **+13.6pp acima** | ✗ stale + metodologia suspeita |
| SEED=42 fixo | Presente em 02, 03b, 04 | ✓ |

---

## 6. Próximos Passos (em ordem de prioridade)

### Pré-requisito para DKT (05)

**P1 — Re-executar `04_bkt.ipynb` (resolve B1)**
```bash
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  notebooks/04_bkt.ipynb --ExecutePreprocessor.timeout=600
```
Verificar: cells 3-4 produzem output; `EVAL_AIDS = [439, 487, 492, 494, 502]`; `n_train events` para A439 ≈ 9,754.

**P2 — Investigar e corrigir kc_correctness vazio (resolve B2)**

Checar se a célula de Task 6 trata corretamente o caso em que o arquivo de cache existe mas está vazio (`{}` é considerado "cache hit válido"?). Re-rodar com `--fix 6` ou limpar manualmente os 3 arquivos e re-executar.

**P3 — Re-executar `01_eda.ipynb` (resolve A1)**
```bash
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
  notebooks/01_eda.ipynb --ExecutePreprocessor.timeout=600
```
Valores das seções 4-8 devem refletir Spring2019 (328 train students).

### Após re-execução do BKT

**P4 — Investigar discrepância de first-attempt AUC (resolve A2)**

Após re-executar 04_bkt com Spring2019 data:
- Se first-attempt AUC ainda ≥ 58%, investigar metodologia de is_first_attempt na janela truncada
- Calcular AUC apenas com sequências NÃO truncadas como sanity check
- Documentar no notebook com hipótese de causa

### Opcional (rigor reprodutível)

**P5 — Regenerar caches KC de Spring2019 (resolve A3/A4)**

Descomentar célula 2 do `03b_kc_generation.ipynb`, executar uma vez para limpar caches, re-executar o notebook completo. Custo estimado: ~$0.05-0.10 Haiku. Não bloqueia DKT.
