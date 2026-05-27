# Codebase Concerns

**Analysis Date:** 2026-05-27

Este documento cataloga riscos técnicos, dívidas e fragilidades identificadas no repositório `tcc.edm.kt`. A maioria reflete escolhas conscientes de um trabalho de graduação com escopo definido e prazo fixo (TCC 1, autor único). Onde aplicável, indica-se mitigação ou caminho para o TCC 2.

---

## Tech Debt

### Patches em `.venv/` para compatibilidade do pyBKT 1.4.1

- Issue: pyBKT 1.4.1 não funciona out-of-the-box com numpy 2.4 + sklearn 1.8 + Python 3.12. Três patches foram aplicados manualmente dentro de `.venv/lib/python3.12/site-packages/pyBKT/`.
- Files:
  - `.venv/lib/python3.12/site-packages/pyBKT/fit/EM_fit.py` (linhas 109-114) — bloco `if __name__ == "__main__"` faz o `Pool.map` paralelo só executar quando o módulo é script; a partir de notebook ou módulo importado, cai no fallback sequencial `x = [inner(tc) for tc in thread_counts]`. Sem esse fallback, o E-step não rodava.
  - `.venv/lib/python3.12/site-packages/pyBKT/models/Model.py` — ajustes para sklearn 1.8 (compat de API quebrada).
  - `.venv/lib/python3.12/site-packages/pyBKT/models/Roster.py` (linhas 545-557) — `dtype=np.int64` explícito onde numpy 2.4 ficou estrito.
- Impact:
  - `.venv/` está gitignored (`/.gitignore` linhas 17-19), portanto **nenhum patch está versionado**.
  - Em um clone fresco, `pip install pyBKT==1.4.1` produz biblioteca quebrada: EM falha silenciosamente (paralelo nunca executa fora de `__main__`) ou estoura `TypeError` no sklearn 1.8.
  - O notebook `04_bkt.ipynb` roda sem aviso até o ponto em que pyBKT retorna AUC degenerada ou exception obscura.
  - Tempo de fit BKT já documentado em `08_multirun_regeneration.ipynb` cell 0: ~45s por fit no fallback sequencial; 50 fits = 38min. Tentativa de regenerar multirun BKT estourou timeout de 40min sem salvar nada.
- Fix approach (TCC 2): congelar versões em `requirements.txt` ou `pyproject.toml`, criar script `scripts/patch_pybkt.sh` versionado que aplique os 3 diffs via `patch`/`sed` pós-instalação, e documentar em `README.md` como pré-requisito. Alternativa: fork de pyBKT com os patches aplicados, instalado via `pip install git+https://...`.

### Ausência de `requirements.txt`/`pyproject.toml`

- Issue: Não há lockfile nem manifest de dependências no repositório. README cita `pip install torch pyBKT scikit-learn pandas numpy matplotlib seaborn anthropic sentence-transformers scipy` sem versões.
- Files: nenhum (ausência é o problema). Verificado por `find . -name "requirements*.txt" -o -name "pyproject.toml" -o -name "Pipfile" -o -name "uv.lock"`.
- Impact: versões instaladas hoje podem não ser reproduzidas em outra máquina. Combinado com os patches do pyBKT acima, isso significa que **a reprodução exata do experimento depende da memória do autor**.
- Fix approach: gerar `pip freeze > requirements.txt` da `.venv` atual e commitar; para o TCC 2, migrar para `uv` ou `poetry` com lockfile commitado.

### Notebook utilitário não-versionado no root

- Issue: `create_notebook_07.py` é um script Python no root que provavelmente foi usado uma vez para gerar `07_comparison.ipynb` e nunca removido.
- Files: `/home/leokuntz/Documents/repositories/studies/tcc.edm.kt/create_notebook_07.py`.
- Impact: poluição visual do repositório; dúvida sobre se é descartável ou se o notebook depende dele para regeneração.
- Fix approach: mover para `scripts/` ou deletar se `07_comparison.ipynb` for editado diretamente daqui em diante.

### Caminho hardcoded no CLAUDE.md para repositório de referência externo

- Issue: `CLAUDE.md` linha 14 referencia `/home/leokuntz/Documents/repositories/experiments/Code-DKT/src/` como repositório-modelo do Code-DKT.
- Files: `CLAUDE.md`.
- Impact: contexto de implementação inacessível em qualquer outra máquina; quem ler o CLAUDE.md em um clone fresco não encontra o repositório referenciado.
- Fix approach: substituir por URL do repositório oficial (`https://github.com/YangAzure/Code-DKT`) e fixar o commit referenciado.

---

## Known Bugs

### `data_loader.load_main_table` referencia `_SPLITS` vazio

- Symptoms: chamar `load_main_table(split=...)` levanta `ValueError: split deve ser um de []`.
- Files: `src/data_loader.py` linhas 13, 34-36.
- Trigger: `_SPLITS = {}` no topo do módulo nunca é populado; só `load_spring2019_split()` funciona como caminho de entrada.
- Workaround: usar apenas `load_spring2019_split()`. As funções `load_main_table()` e `load_labels()` são dead code que ainda vivem na API pública do módulo.
- Fix approach: remover `load_main_table`/`load_labels` ou popular `_SPLITS` com mapeamento real (vestígio do design antigo que apontava para `Release/Train/` etc., obsoleto após a decisão documentada em `CLAUDE.md` linha 88).

### `bkt.py::compute_auc` duplica lógica de `evaluation.py::compute_auc`

- Symptoms: dois implementações funcionalmente idênticas. Risco de drift se uma for atualizada e outra não.
- Files: `src/models/bkt.py` linhas 74-92, `src/evaluation.py` linhas 38-61.
- Trigger: refactor incompleto — `evaluation.compute_auc` foi introduzido como utilitário compartilhado mas `bkt.py` ainda define a sua localmente e a usa em `train_and_evaluate`.
- Workaround: nenhum necessário enquanto ambas concordam.
- Fix approach: deletar `bkt.py::compute_auc` e importar de `src.evaluation`.

---

## Reproducibility Risks

### Saved-state coupling: `pred_df` só persistido para `seed=42`

- Risk: `08_multirun_regeneration.ipynb` (cells 11, 14) executa 10 runs (seeds 42-51) para DKT e Code-DKT, mas dentro do loop só armazena `pred_df` quando `seed == SEED_DEFAULT`; demais runs guardam `pred_df = None`. Apenas as AUCs escalares são salvas para todas as seeds.
- Files: `notebooks/08_multirun_regeneration.ipynb` (cells 11 linha "if seed == SEED_DEFAULT:", 14 mesma estrutura), `results/dkt_results_multirun.pkl`, `results/code_dkt_results_multirun.pkl`, `results/srcml_dkt_results_multirun.pkl`.
- Current mitigation: motivo provável é tamanho do pickle (10 runs × 5 assignments × ~5k linhas de pred_df = ~250k linhas/arquivo). `07_comparison.ipynb` cell 9 (`compute_pooled_auc`) calcula explicitamente "Filtrar apenas runs com pred_df nao-None" e pode terminar com `n_valid = 1` para análises pooled — o que reduz AUC pooled a um único ponto sem barra de erro.
- Recommendations: qualquer análise que precise de pred_df (bootstrap CI, recalibração de threshold, breakdown por KC, análise por estudante) **precisará re-treinar todas as 10 seeds**. Já aconteceu no notebook de KC difficulty (memory `project_codedkt_kc_difficulty.md`: "re-treino por desalinhamento do pred_df salvo"). Para o TCC 2, salvar pred_df de todas as runs (ou ao menos um sample reprodutível) é mandatório.

### Pipeline fragility: notebooks devem rodar em ordem; artefatos intermediários gitignored

- Risk: pipeline 00 → 09 produz artefatos intermediários em `results/` (sequências serializadas, vocabulários, caches de paths AST). `.gitignore` linha 38-40 ignora `results/code_features_cache.pkl` e `results/srcml_features_cache.pkl`; commit recente "removed `results/*.csv` and `*.pkl` exclusion" (linhas 31-34 comentadas) indica que demais `.pkl`/`.csv` voltaram a ser commitados, mas modelos PyTorch (`*.pt`/`*.pth`) e HDF5 (`*.h5`) continuam ignorados (linhas 42-44).
- Files: `notebooks/02_preprocessing.ipynb` → produz `results/sequences_bkt_dkt.pkl`; `notebooks/03_code_features.ipynb` (planejado) → `code_features_cache.pkl`; `notebooks/08_multirun_regeneration.ipynb` cell 3 lê ambos. `07_comparison.ipynb` cell 4 carrega 4 pickles multirun obrigatórios (`bkt_results_multirun.pkl`, `dkt_results_multirun.pkl`, `code_dkt_results_multirun.pkl`, `srcml_dkt_results_multirun.pkl`).
- Current mitigation: README documenta a ordem implicitamente via tabela de notebooks. Caches de paths AST custosos (`code_features_cache.pkl`, `srcml_features_cache.pkl`) estão explicitamente gitignored com a justificativa "regenerável via notebooks" — porém regenerar leva tempo significativo (build_cache via multiprocessing.Pool sobre 69.627 CodeStates).
- Recommendations: adicionar checagem `if not RESULTS_DIR.glob("*.pkl"): raise` no início de cada notebook downstream; documentar tempo de regeneração de cada cache; considerar `make` ou `dvc` para o TCC 2.

### Data dependency: `data/CSEDM/` gitignored, requer download manual

- Risk: `/.gitignore` linha 2 (`data/`) exclui todo o dataset. README seção "Setup" instrui "`Dados:` `data/CSEDM/` (gitignored). Baixar separadamente e manter a estrutura `data/CSEDM/Release/Train/` e `data/CSEDM/Release/Test/`." Mas: o protocolo atual usa `data/CSEDM/MainTable.csv` (não `Release/`), conforme `CLAUDE.md` linhas 81-86. Há **divergência entre README e CLAUDE.md** sobre a estrutura esperada do dataset.
- Files: `README.md` (instrução desatualizada), `CLAUDE.md` (fato verdadeiro), `data/CSEDM/` (no host atual contém `MainTable.csv`, `CSEDM/`, `early.csv`, `late.csv`).
- Current mitigation: o autor sabe a fonte; CSEDM/ProgSnap2 está em https://pslcdatashop.web.cmu.edu/Files?datasetId=3458 (registro obrigatório).
- Recommendations: atualizar README seção "Setup" para refletir o esquema `data/CSEDM/MainTable.csv + data/CSEDM/CodeStates/CodeStates.csv`; adicionar nota sobre licença CC-BY-NC e necessidade de cadastro no PSLC DataShop.

### Seed coupling: três sementes diferentes coexistem

- Risk: o repositório usa simultaneamente: `seed=1` (split estudante via `train_test_split`, `src/data_loader.py:280`), `seed=42` (treino dos modelos, `bkt.py:39`, `dkt.py:183`, `code_dkt.py:152`), `seed=42..51` (multirun em `08_multirun_regeneration.ipynb`). Trocar qualquer uma muda quem está em train/test ou os pesos iniciais do LSTM.
- Files: `src/data_loader.py:246`, `src/models/{bkt,dkt,code_dkt}.py`, `notebooks/08_multirun_regeneration.ipynb`.
- Current mitigation: convenção documentada em `CLAUDE.md` linha 84 ("random_state=1" para o split, alinhamento com Shi et al. 2022) e linha 119 ("Seed fixo obrigatório em todos os notebooks").
- Recommendations: centralizar em `src/config.py` com constantes `SPLIT_SEED = 1`, `TRAIN_SEEDS = list(range(42, 52))`, `DEFAULT_SEED = 42` e importar em todo lugar.

### `torch.backends.cudnn.deterministic` setado só nos notebooks, não nos módulos de treino

- Risk: `08_multirun_regeneration.ipynb` cell 2 define `torch.backends.cudnn.deterministic = True`, mas `train_dkt` e `train_code_dkt` (`src/models/dkt.py:197`, `src/models/code_dkt.py:167`) só chamam `torch.manual_seed(seed)` e `np.random.seed(seed)`. Se alguém invocar essas funções fora do notebook 08, pode obter resultados ligeiramente diferentes em GPU mesmo com seed igual.
- Files: `src/models/dkt.py:197-198`, `src/models/code_dkt.py:167-168`, `notebooks/08_multirun_regeneration.ipynb` cell 2.
- Current mitigation: comentário em `notebooks/08_multirun_regeneration.ipynb` cell 10 reconhece isso explicitamente: "`set_global_seed(seed)` chamado externamente antes de cada run (compensa que `dkt.py::train_dkt` não chama `torch.cuda.manual_seed_all` nem `cudnn.deterministic`)".
- Recommendations: mover `torch.cuda.manual_seed_all(seed)` e os flags cudnn para dentro de `train_dkt`/`train_code_dkt`, ou criar um `src/seeding.py::set_global_seed(seed)` importado em todos os pontos de entrada.

---

## Statistical / Methodological Concerns

### Wilcoxon com N=5 assignments tem poder estatístico baixo

- Risk: Wilcoxon signed-rank com N=5 pares produz p-valor mínimo de 0.0625 (se todos os 5 pares têm mesmo sinal). Memory `project_multirun_results.md` documenta: Code-DKT vence DKT em 4/5 assignments mas Wilcoxon dá **p=0.31**. Mesmo a vitória sistemática não cruza o limiar de significância clássico.
- Files: `notebooks/07_comparison.ipynb` cell 2 (import `scipy.stats.wilcoxon`), `AIDS = [439, 487, 492, 494, 502]`.
- Current mitigation: o multirun (`08_multirun_regeneration.ipynb`) regera DKT/Code-DKT com 10 seeds × 5 assignments = 50 pares; `07_comparison.ipynb` cell 13 implementa Holm-Bonferroni e bootstrap CI sobre essas 50 amostras. Resultado documentado em memory `project_comparison_results.md`: "Wilcoxon Code-DKT>DKT p=0.002" — significativo no multirun pareado, **não** no by-assignment.
- Recommendations: relatar **ambos** resultados no TCC. By-assignment (N=5) é a comparação que o paper de referência reporta; multirun pareado (N=50) é a que dá significância. Discutir abertamente que N=5 é a limitação inerente ao número de assignments disponíveis no CSEDM Spring 2019.

### Code-DKT vs srcML-DKT performance gap

- Risk: srcML-DKT ficou abaixo do Code-DKT em todos os 5 assignments, com Δ entre −2.9pp e −4.2pp em first-attempt AUC (memory `project_srcml_results.md`). A hipótese inicial — "srcML parseia 100% dos códigos, javalang só ~86%, portanto srcML-DKT deveria ganhar" — não se sustentou.
- Files: `src/srcml_features.py` (extrator), `src/code_features.py` (extrator javalang), `notebooks/09_srcml_dkt.ipynb`, `results/srcml_dkt_results_multirun.pkl`.
- Cause: vocabulário srcML é menos discriminativo. Tags XML são genéricas (`expr`, `name`, `call`, `block`) enquanto javalang produz nomes de classes Java (`MethodInvocation`, `LocalVariableDeclaration`, `BinaryOperation`) que carregam mais informação semântica. A maior cobertura de parsing não compensou o vocabulário menos rico.
- Current mitigation: documentado como achado negativo em `project_srcml_results.md`; será discutido no TCC como contribuição secundária (validação empírica da decisão de Pankiewicz et al. 2025 e identificação de limite do approach).
- Recommendations (TCC 2): combinar srcML estrutural com tokens identifier-aware (nomes de variáveis/métodos), ou usar tree-sitter Java grammar que preserva nomes de classe semelhantes ao javalang mas com a robustez do srcML.

### TODO comment isolado em `01_eda.ipynb`

- Files: `notebooks/01_eda.ipynb` cell 13 — único hit de TODO/FIXME/HACK/XXX no código-fonte. Conteúdo: `print(f'\nEstudantes que participaram de TODOS os {n_assignments} assignments: ...')`. **Falso positivo**: "TODOS" como literal português, não marcador.
- Impact: nenhum. Código limpo desse ponto de vista.

---

## Fragile Areas

### `CodeDKTModel` força concordância entre training e inference em `max_len` e `R`

- Files: `src/models/code_dkt.py:240-304`, `src/code_features.py:286-361`.
- Why fragile: `predict_code_dkt` aceita `max_len` e `R` como parâmetros, mas se diferirem dos usados em `train_code_dkt` o tensor de entrada terá forma incompatível com a `nn.Linear` interna. Não há validação — o erro vem como `RuntimeError` opaco do PyTorch.
- Safe modification: sempre passar os mesmos `config["max_len"]` e `config["R"]` na predição. `train_and_evaluate` faz isso corretamente; chamadas externas podem errar.
- Test coverage: nenhuma — não há `tests/` no repositório. Confiança baseada em re-execução manual dos notebooks.

### Vocabulário construído só do train, com fallback silencioso para UNK em test

- Files: `src/code_features.py:227-251` (`build_vocab`), `paths_to_tensor` linhas 280-283 (`token_to_idx.get(start, 0)`).
- Why fragile: tokens/paths AST que aparecem só no test set são mapeados para índice 0 (PAD/UNK). Não há contagem nem aviso. Se a taxa de UNK for alta, Code-DKT vira efetivamente DKT com ruído.
- Safe modification: instrumentar `predict_code_dkt` para reportar `% de paths UNK no test set` por assignment.
- Test coverage: nenhuma instrumentação atual. Foi assumido implicitamente que a sobreposição train/test é alta.

### Vocabulário srcML compartilha o mesmo problema, agravado

- Files: `src/srcml_features.py` (todo o módulo).
- Why fragile: tags srcML são genéricas, então a sobreposição deveria ser maior — mas a memória `project_srcml_results.md` identifica que isso pode estar **degradando** discriminação. Cobertura ≠ qualidade.
- Safe modification: avaliar contagem de tokens UNK em produção, comparar com Code-DKT vanilla.

### Ausência de tests/

- Files: nenhum `tests/` ou `test_*.py` em todo o repositório (`find . -name "test_*.py" -not -path '*/.venv/*'` retorna vazio).
- Why fragile: refactors no `data_loader.py` (ex: mudar `min_attempts`, mudar ordem de truncate vs is_first_attempt) podem mudar AUC sem aviso. A única "validação" é o critério de conclusão "first_auc do Code-DKT próximo a 74% para A1" (CLAUDE.md linha 140).
- Risk: alterações no `truncate_sequences` ou no recálculo de `is_first_attempt` dentro da janela truncada (`src/data_loader.py:198-203`) são especialmente sensíveis. Bug aqui inflaria/deflacionaria first-attempt AUC silenciosamente.
- Test coverage: zero. Confiança baseada em comparar AUC observada com a do paper.
- Recommendations (TCC 2): adicionar pelo menos `tests/test_data_loader.py` com fixtures sintéticas pequenas validando: filtros corretos, `is_first_attempt` recalculado corretamente após truncate, contagem de estudantes pós-filtro min_attempts.

---

## Saved-Artifact Coupling

### `bkt_results.pkl` vs `bkt_results_multirun.pkl`

- Files: `results/bkt_results.pkl` (1 run, formato antigo), `results/bkt_results_multirun.pkl` (re-embalado em schema multirun com 1 run).
- Why fragile: `08_multirun_regeneration.ipynb` cell 9 não treina BKT novamente — apenas re-empacota o pickle antigo no schema esperado por `07_comparison.ipynb`. Se alguém deletar `bkt_results.pkl`, `08` quebra mesmo se rodar do início (não há regeneração canônica do BKT no notebook 08; presume-se que `04_bkt.ipynb` foi rodado antes).
- Recommendations: documentar dependência implícita 04 → 08 no docstring de `08_multirun_regeneration.ipynb`.

### `dkt_results.pkl`/`code_dkt_results.pkl` consumidos para extrair `best config`

- Files: `notebooks/08_multirun_regeneration.ipynb` cell 5 (`BEST_DKT_CONFIG = dkt_single[ASSIGNMENT_IDS[0]]["config"]`).
- Why fragile: pega o config do **primeiro** assignment (A439) e usa para todos. Assume implicitamente que o grid search dos notebooks 05/06 produziu o mesmo melhor config para todos os 5 assignments — não há checagem.
- Recommendations: assertar `assert all(dkt_single[aid]["config"] == BEST_DKT_CONFIG for aid in ASSIGNMENT_IDS)`.

---

## Project Management Concerns

### TCC deadline pressure: autor único, prazo fixo

- Risk: graduação com defesa marcada cria pressão por "rodou, ficou bom, segue". Algumas dívidas acima (sem tests, sem requirements.txt, sem CI) são consequência direta dessa pressão.
- Files: todo o repositório.
- Mitigation: o split em TCC 1 (modelagem comparativa) e TCC 2 (deployment + extensão srcML/KCGen) dá oportunidade de pagar dívidas no semestre seguinte com escopo já validado.
- Recommendations:
  - Antes da defesa do TCC 1: gerar `pip freeze > requirements.txt` e adicionar `scripts/setup_env.sh` que aplique os 3 patches do pyBKT após `pip install -r requirements.txt`. Sem isso, o avaliador não consegue reproduzir.
  - Documentar no TCC quais resultados são single-seed (`seed=42`, BKT, análises baseadas em `pred_df` salvo) e quais são multirun (DKT, Code-DKT, srcML-DKT métricas escalares).

### Notebooks de apresentação e scripts utilitários acumulando no root

- Files: `create_notebook_07.py`, `check-slide1.png`, `csedm_dataset_page.png`, `PLAN_KC_GENERATION.md`, `PLAN_TCC1.md` no root.
- Impact: dificulta enxergar a estrutura essencial do projeto na primeira vez que se abre o repositório.
- Recommendations: mover `PLAN_*.md` para `.planning/` ou `docs/plans/`; PNGs para `apresentacao/assets/` (já existe). Manter root limpo a CLAUDE.md, README.md, .gitignore, dependências.

---

## Test Coverage Gaps

### Pipeline de extração de paths AST não tem regression test

- What's not tested: `extract_paths_javalang` e `extract_paths_srcml` retornam estruturas complexas (lista de tuplas com strings) e seus filtros (`max_path_length=8`, `max_path_width=2`) reproduzem path_extractor.py do paper original. Não há fixture comparando contra output esperado.
- Files: `src/code_features.py:88-178`, `src/srcml_features.py:88-196`.
- Risk: qualquer ajuste no algoritmo (ex: mudar `walker.walk` ou a heurística de width) muda silenciosamente as features que alimentam o LSTM. AUC pode subir ou descer sem causa rastreável.
- Priority: Médio (TCC 2). Para TCC 1, basta congelar o código e comparar AUC com paper.

### `data_loader.build_sequences` não tem teste de borda

- What's not tested: comportamento quando estudante tem 0 eventos, quando timestamps são idênticos (a documentação diz "desambiguados pela ordem original do DataFrame", mas isso depende do sort estável), quando ProblemID é NaN.
- Files: `src/data_loader.py:108-165`.
- Risk: silently dropping rows ou criando sequências de tamanho 0 que quebram downstream em `build_input_tensor`.
- Priority: Baixo (assertions atuais no `filter_for_*` cobrem o caso típico).

### Métrica AUC não tem teste contra implementação de referência

- What's not tested: `compute_auc` com `first_attempt_only=True` deveria reproduzir exatamente o protocolo de `evaluation.py` do repositório Code-DKT oficial (acumular `first_total_gts` e chamar `roc_auc_score` uma vez). Não há teste comparando contra um caso conhecido.
- Files: `src/evaluation.py:38-61`.
- Risk: small divergence vs paper de referência pode explicar parte da diferença entre nosso AUC e o reportado por Shi et al. (2022).
- Priority: Médio. O critério de conclusão "first_auc A439 ≈ 74% ±3%" já é o proxy efetivo deste teste.

---

*Concerns audit: 2026-05-27*
