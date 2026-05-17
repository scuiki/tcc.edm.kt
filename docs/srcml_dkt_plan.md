# Plano: srcML-DKT como 4º modelo no TCC 1

> **Cópia de:** `~/.claude/plans/vamos-tra-ar-um-plano-squishy-shamir.md`
> **Salvo em:** 2026-05-17
> **Status:** aprovado, aguardando execução em duas conversas separadas (ver "Plano de execução em 2 conversas" abaixo).

## Context

O TCC 1 hoje compara **3 modelos** (BKT, DKT, Code-DKT) com Code-DKT já validado em 10 runs (commit `07f7b3b`). A literatura mais recente (Pankiewicz, Shi & Baker, 2025 — EDM short paper em `docs/2025.EDM.short-papers.83.pdf`) propõe **srcML-DKT** como extensão direta do Code-DKT que substitui o parser javalang (frágil em código não-compilável) por srcML (CLI XML-based que degrada graciosamente). O paper demonstra ganho de **+1.65pp first-attempt AUC** sobre Code-DKT em dataset CS1 de condicionais C# (610 alunos).

**Decisão:** incluir srcML-DKT já no TCC 1 como **4º modelo da comparação final**, em vez de adiar para o TCC 2. Justificativa:
1. O binário `srcml` 1.1.0 já está instalado (`/usr/bin/srcml`).
2. As sequências com Compile.Error já existem (`results/sequences_code_dkt.pkl`, 53k eventos vs 43k do `sequences_bkt_dkt.pkl`).
3. A arquitetura PyTorch é **idêntica** ao Code-DKT — só o parser muda. Reúso máximo de código.
4. Paper de referência fornece resultados publicados para discussão comparativa.
5. Compromete-se a documentar TODAS as decisões de design (paper não especifica o algoritmo de extração).

**Decisões já tomadas pelo usuário:**
- Sequências: `sequences_code_dkt.pkl` (Run.Program + Compile.Error) — fiel ao paper
- Hiperparâmetros: reusar BEST_CDKT_CONFIG (hidden=200, dropout=0.1, lr=0.0005, 40 épocas) — consistência interna
- Pipeline de execução: monolítico em **um único notebook** (`09_srcml_dkt.ipynb`), sem subagentes nem paralelização entre processos

## Plano de execução em 2 conversas

Embora o pipeline técnico seja monolítico (um notebook só), o trabalho humano de **implementação** será dividido em duas conversas com modelos otimizados para cada fase:

| Chat | Modelo | Escopo | Outputs |
|---|---|---|---|
| **Chat 1 (execução)** | Sonnet 4.6 | `src/srcml_features.py`, `notebooks/09_srcml_dkt.ipynb`, execução end-to-end, validação, commits dos artefatos técnicos | Código + pickles + cache + commits |
| **Chat 2 (documentação)** | Opus 4.7 | `docs/srcml_dkt_implementation.md` lendo os artefatos do Chat 1, com voz de estudante de eng. computação | Documento de decisões + commit final |

Justificativa: Sonnet 4.6 é mais econômico e rápido para o trabalho mecânico (espelhar padrão estabelecido, debugar, rodar notebook). Opus 4.7 oferece prosa mais reflexiva e nuance — ideal para o documento de decisões que vira material direto do TCC.

## Approach

**3 arquivos novos** + **reúso total** dos módulos do Code-DKT:

```
src/srcml_features.py            (novo) — análogo a src/code_features.py com parser srcML
notebooks/09_srcml_dkt.ipynb     (novo) — espelha o 06_code_dkt.ipynb
docs/srcml_dkt_implementation.md (novo) — registra decisões de design não cobertas pelo paper
```

**Reúso:**
- `src/models/code_dkt.py::CodeDKTModel` — **arquitetura idêntica**, sem nova classe
- `src/models/code_dkt.py::train_and_evaluate` — aceita qualquer `cache_raw` (parser-agnostic)
- `src/code_features.py::build_vocab` — mesma assinatura (recebe `dict[csid → list[(start, path, end)]]`)
- `src/code_features.py::paths_to_tensor`, `::build_code_input_tensor` — agnósticas ao parser

## Design do extractor srcML (decisões a documentar)

O paper (Pankiewicz et al. 2025, Section 3.4 + Figure 1) **não especifica o algoritmo de extração de codepaths**. Mostra apenas um exemplo: `[input, method, body, doSomething, input]`. Decisões de design ad-hoc, todas em `docs/srcml_dkt_implementation.md`:

1. **Fonte da árvore:** subprocess `srcml --language=Java` lê via stdin, retorna XML. Parse com `xml.etree.ElementTree` (stdlib).
2. **Tokens:**
   - Folhas (sem filhos) → `.text.strip()` se não-vazio, caso contrário tag local (sem namespace)
   - Interiores → tag local (e.g., `if_stmt`, `block`, `expr_stmt`)
3. **Construção da anytree:** mesmo `Walker` do Code-DKT (`src/code_features.py::_build_tree`), mas alimentado pelo XML em vez de `javalang.ast.Node`.
4. **Filtros:** `max_path_length=8`, `max_path_width=2`, `R=50` (idênticos ao Shi et al. 2022 — fidelidade ao Code-DKT).
5. **Tratamento de namespace:** strip prefixo `{http://www.srcML.org/srcML/src}` de toda tag antes de tokenizar.
6. **Fallback em parse failure:** srcML CLI raramente falha (degrada graciosamente). Se subprocess retornar erro ou XML vazio, retornar `[]` (mesmo critério do `extract_paths_javalang`).
7. **Compile.Error events:** entram no cache como qualquer outro CodeStateID. srcML produz XML parcial mesmo com sintaxe quebrada.

## Pipeline de avaliação (decisão crítica de comparação justa)

**Problema:** BKT/DKT/Code-DKT atuais foram avaliados em `sequences_bkt_dkt.pkl` (só Run.Program). srcML-DKT vai TREINAR em `sequences_code_dkt.pkl` (com Compile.Error), mas se também AVALIAR em sequences_code_dkt, o test set é diferente — AUCs não são comparáveis lado-a-lado.

**Solução:** seguir o padrão do paper Pankiewicz et al. — srcML-DKT TREINA com Compile.Error mas AVALIA no **mesmo test set dos outros 3 modelos** (`sequences_bkt_dkt.pkl['test'][aid]`). Diferença vem só do TREINO (mais eventos disponíveis), não da definição de "acerto".

Documentar essa decisão em `docs/srcml_dkt_implementation.md` Seção "Comparação justa".

## Estrutura do notebook 09

| Seção | Conteúdo | Tempo est. |
|---|---|---|
| 1 | Setup, `set_global_seed`, device, paths | 5s |
| 2 | Carregar `sequences_code_dkt.pkl` (train) + `sequences_bkt_dkt.pkl` (test) + CodeStates.csv | 10s |
| 3 | `extract_paths_srcml` em sample de 100 submissões + métricas de transparência (taxa parsing, paths/sub, tempo) | 30s |
| 4 | Cache completo via `build_cache_srcml(n_workers=os.cpu_count())` → `results/srcml_features_cache.pkl` | ~10 min |
| 5 | Vocab por assignment (do train de `sequences_code_dkt`) — reusa `build_vocab` | 5s |
| 6 | Tensorização A439 + smoke test forward + smoke train (5 épocas) | 1 min |
| 7 | Treino full: 10 runs × 5 assignments × 40 épocas com BEST_CDKT_CONFIG. **Avaliação no test set do `sequences_bkt_dkt`** | ~10 min |
| 8 | Sumário rápido (mean ± std vs Code-DKT multirun) | 5s |
| 9 | Serialização `results/srcml_dkt_results_multirun.pkl` | 30s |
| 10 | Sanity checks (schema, coerência seed=42) | 5s |

**Tempo total estimado: ~25-30 min**.

## Schema do `srcml_dkt_results_multirun.pkl`

Idêntico ao `code_dkt_results_multirun.pkl`:

```python
{aid: {
  'all_auc_mean', 'all_auc_std', 'first_auc_mean', 'first_auc_std',
  'runs': [{seed, all_auc, first_auc, pred_df}, ...],   # 10 entradas
  'n_train_events', 'n_test_events', 'config', 'vocab', 'problem_to_idx',
  'model_state_dict_seed42',
}}
```

## Critérios de sucesso

1. ✓ `notebooks/09_srcml_dkt.ipynb` executa end-to-end sem erros em <40 min
2. ✓ `results/srcml_dkt_results_multirun.pkl` criado, schema idêntico aos outros multirun
3. ✓ srcML extrai ≥1 path para >95% dos CodeStateIDs (incluindo Compile.Error — vs ~86% do javalang)
4. ✓ Coerência interna: seed=42 reproduzível bit-exact em re-runs do mesmo notebook
5. ✓ `docs/srcml_dkt_implementation.md` registra todas as decisões de design (≥10 itens)

## Critérios de não-sucesso (rollback)

- Cache srcML > 30 min → reduzir n_workers ou paralelizar via subagentes (escapar do plano monolítico)
- AUC do srcML-DKT < Code-DKT em todos 5 assignments → investigar bug no extractor antes de prosseguir; pode indicar paths mal-formados
- Taxa de parsing srcML < 80% → reportar como limitação metodológica mas continuar (o paper não exige 100%)

## Arquivos a criar

- `src/srcml_features.py` (~150 linhas, espelha `code_features.py`) — **Chat 1**
- `notebooks/09_srcml_dkt.ipynb` (~25 cells, espelha `06_code_dkt.ipynb`) — **Chat 1**
- `results/srcml_features_cache.pkl` (gerado, ~200 MB — adicionar ao `.gitignore` como o cache javalang) — **Chat 1**
- `results/srcml_dkt_results_multirun.pkl` (gerado, ~80 MB) — **Chat 1**
- `docs/srcml_dkt_implementation.md` (decisões de design — análogo a `docs/code_dkt_implementation.md`) — **Chat 2**

## Arquivos a NÃO tocar

- `src/code_features.py`, `src/models/code_dkt.py` (reúso direto)
- `notebooks/06_code_dkt.ipynb` e demais notebooks (intactos)
- `results/*_multirun.pkl` existentes (BKT, DKT, Code-DKT) — srcML-DKT entra como pickle adicional

## Verificação (end-to-end)

```bash
# 1. Sanity inicial — srcml e dataset prontos
srcml --version | head -1
.venv/bin/python -c "
import pickle
with open('results/sequences_code_dkt.pkl', 'rb') as f: s = pickle.load(f)
with open('results/sequences_bkt_dkt.pkl', 'rb') as f: t = pickle.load(f)
print('train(code_dkt):', sum(len(s['train'][a]) for a in s['assignment_ids']))
print('test(bkt_dkt):',   sum(len(t['test'][a])  for a in t['assignment_ids']))
"

# 2. Executar notebook
.venv/bin/jupyter nbconvert --to notebook --execute --inplace \
    notebooks/09_srcml_dkt.ipynb --ExecutePreprocessor.timeout=2700

# 3. Schema check + cross-model coherence
.venv/bin/python -c "
import pickle
import numpy as np
with open('results/srcml_dkt_results_multirun.pkl', 'rb') as f: r = pickle.load(f)
with open('results/code_dkt_results_multirun.pkl',  'rb') as f: c = pickle.load(f)
for aid in [439, 487, 492, 494, 502]:
    assert len(r[aid]['runs']) == 10, f'A{aid}: {len(r[aid][\"runs\"])} runs'
    seeds = sorted([x['seed'] for x in r[aid]['runs']])
    assert seeds == list(range(42, 52)), f'A{aid}: seeds={seeds}'
    delta = r[aid]['first_auc_mean'] - c[aid]['first_auc_mean']
    print(f'A{aid}: srcML={r[aid][\"first_auc_mean\"]*100:.2f}% vs Code-DKT={c[aid][\"first_auc_mean\"]*100:.2f}% (Δ={delta*100:+.2f}pp)')
"
```

## Compromisso de documentação

`docs/srcml_dkt_implementation.md` deve ser escrito **com a voz de um estudante de engenharia de computação trabalhando no TCC** — não de um pesquisador sênior nem de um manual API. Isso significa:

- **Tom:** primeira pessoa do plural ocasional ("optamos por", "decidimos manter"), explicando o porquê de cada escolha como se fosse para um colega de turma ou orientador. Sem jargão desnecessário, mas sem simplificações que escondam trade-offs reais.
- **Estrutura:** começar pelo "porquê" (motivação) antes do "como" (algoritmo). Cada decisão técnica seguida de uma justificativa em 1-2 frases acessíveis.
- **Honestidade metodológica:** quando o paper de referência não especificar algo, dizer explicitamente "o paper não detalha X, optamos por Y porque Z". Isso vira material direto para a seção de Metodologia/Decisões do TCC.
- **Concisão:** ~400-600 linhas. Equilibrar rigor com legibilidade. Diagramas ASCII simples quando ajudarem.

Como o paper Pankiewicz et al. (2025) é um short paper (8 páginas) que **não especifica detalhes do extractor**, `docs/srcml_dkt_implementation.md` deve documentar pelo menos:

1. Mapeamento srcML XML → anytree (regra para folhas, regra para interiores)
2. Tratamento de namespace
3. Decisão sobre `.text` vs tag para folhas
4. Hiperparâmetros idênticos ao Shi et al. 2022 (max_path_length=8, R=50)
5. subprocess CLI vs libsrcml (justificativa pela simplicidade)
6. Decisão de avaliar no test set do `sequences_bkt_dkt` (não do `code_dkt`)
7. Tratamento de Compile.Error events (correct=0 fixo, srcML produz XML parcial)
8. Reúso de `CodeDKTModel` (arquitetura idêntica, só feature extractor muda)
9. Fallback em parse failure (subprocess error ou XML vazio → `[]`)
10. Configuração de multiprocessing.Pool (n_workers, chunksize)

## Commits previstos

**Chat 1 (Sonnet 4.6):**
1. `srcml-dkt fase 1: src/srcml_features.py + .gitignore para cache`
2. `srcml-dkt fase 1: notebooks/09_srcml_dkt.ipynb (executado end-to-end)`
3. `srcml-dkt fase 1: results/srcml_dkt_results_multirun.pkl`

**Chat 2 (Opus 4.7):**
4. `srcml-dkt fase 1: docs/srcml_dkt_implementation.md`

## Fora deste plano (futuros)

- `notebooks/07_comparison.ipynb`: consolida BKT + DKT + Code-DKT + srcML-DKT (plano separado, próximo)
- Análise qualitativa de atenção srcML-DKT (análoga à Seção 12 do `06_code_dkt`)
- Ablation pure vs full (srcML-DKT sem Compile.Error)
