# Code-DKT — Handoff Chat 1 → Chat 2

Gerado por: Chat 1 em 2026-05-17 (madrugada)
Status do Chat 1: **CONCLUÍDO**

---

## 1. Artefatos produzidos

| Artefato | Caminho | Status |
|---|---|---|
| Módulo extração | `src/code_features.py` | pronto |
| Módulo modelo | `src/models/code_dkt.py` | pronto |
| Notebook | `notebooks/06_code_dkt.ipynb` (seções 1–7) | pronto |
| Cache de paths | `results/code_features_cache.pkl` | pronto (gitignored) |
| Vocab A439 | embutido no notebook (Seção 5) | pronto |

Commits:
- `91aa726` — `src/code_features.py` + `src/models/code_dkt.py`
- `ee4c3de` — `notebooks/06_code_dkt.ipynb` + `docs/code_dkt_implementation.md`

---

## 2. Métricas de transparência (Seção 3.5 do plano)

- **Taxa de parsing javalang** sobre Run.Program (cache completo): **86.0% sucesso**, 14.0% "Uncompilable"
  - Amostra de 20 submissões A439: 75% — variação esperada por amostra pequena
- **Distribuição de paths por submissão** (antes de R=50): mediana=117, p95=293
  - Valores bem acima de R=50 → amostragem aleatória sempre ativa
- **Tempo total do cache** (16 CPUs, `multiprocessing.Pool`): **37.2s** para 53.990 CodeStateIDs únicos
- **Tamanho de `code_features_cache.pkl`**: **206.2 MB**

---

## 3. Vocabulário A439

Construído **apenas** dos CodeStateIDs do train set A439 (Seção 4.1 do plano — por assignment).

- `node_count` (tokens únicos, start+end): **494**
- `path_count` (path strings únicas): **21.717**
- **OOV no test set**: tokens=0.6%, paths=6.0%
  - OOV bem abaixo de 30% → critério go/no-go OK

---

## 4. Smoke test (A439, 5 épocas, seed=42)

| Métrica | Valor |
|---|---|
| Loss época 1 | 0.6966 |
| Loss época 5 | 0.5964 |
| `all_auc` (smoke) | 0.6405 |
| `first_auc` (smoke) | 0.6307 |
| Tempo de treino (5 épocas) | 4.0s |
| Pico de VRAM | **2221 MB** (~2.2 GB de 6 GB disponíveis) |

**Loss decrescente confirmado** (0.697 → 0.596).  
**first_auc smoke > 0.50** → critério go/no-go PASSOU.

Estimativa para 10 runs × 40 épocas: ~10 × 8× o smoke = ~320s ≈ **5 min por assignment**, ~25 min para 5 assignments.

---

## 5. Decisões tomadas no Chat 1

1. **Softmax sobre R (dim=2), não sobre L (dim=1)**: o repositório oficial (`c2vRNNModel.py`) usa `nn.Softmax(dim=1)` (sobre o comprimento de sequência), mas o paper (Shi et al., 2022, Section 3) descreve atenção sobre os R paths. Implementamos `dim=2` (semântica correta do paper). Isso pode gerar diferença de ~1–2pp de AUC vs a implementação exata do repositório.

2. **embed_dropout (0.2) aplicado via `nn.Dropout`**: automático em `model.train()`/`model.eval()` — não precisa de flag `evaluating` explícita como no repositório original.

3. **FC dropout configurável**: o repositório comenta a linha com dropout antes da camada FC; mantivemos como parâmetro (`dropout ∈ {0.0, 0.1}`) para grid search da Seção 8.

4. **Interface `cache_raw` em vez de `code_states`**: `train_code_dkt`, `predict_code_dkt` e `train_and_evaluate` recebem `cache_raw` (pre-extracted) em vez de `code_states` (raw text) — evita re-extração desnecessária.

5. **Vocabulário por assignment**: construído apenas dos train CodeStateIDs de cada assignment, conforme Seção 4.1 do plano. Chat 2 precisará construir vocab para cada assignment antes do loop de 10 runs.

6. **anytree 2.13.0 + javalang 0.13.0** instalados no `.venv` durante o Chat 1.

---

## 6. Issues conhecidas / TODO para Chat 2

- **Vocabulário global vs por assignment**: atualmente a função `build_vocab` recebe `cache_raw` filtrado do train de cada assignment. Chat 2 deve construir um vocab por assignment antes de entrar no loop `(assignment × 10 seeds)`. O notebook tem exemplo para A439; Chat 2 generaliza para todos os 5 assignments.
- **Tempo estimado de 50 runs**: ~25 min total (5 assignments × 10 runs × ~30s/run com 40 épocas). Bem dentro das 4h.
- **VRAM**: 2.2 GB de pico para batch_size=128 com 307 sequências de treino. Para assignments maiores ou hidden_dim=200, pode chegar a 3 GB — ainda dentro dos 6 GB disponíveis.
- **Schema `code_dkt_results.pkl`**: seguir exatamente a Seção 10 do plano para compatibilidade com `07_comparison.ipynb`.

---

## 7. Comando para Chat 2 retomar

O notebook está executável até a Seção 7. Para Chat 2:

```bash
# 1. Verificar dependências
.venv/bin/python -c "import javalang; print(javalang.__version__)"    # deve ser 0.13.0
.venv/bin/python -c "from anytree import Node; print('anytree OK')"
.venv/bin/python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"

# 2. Verificar cache
.venv/bin/python -c "
import pickle
with open('results/code_features_cache.pkl', 'rb') as f:
    cache = pickle.load(f)
print(f'Cache OK: {len(cache):,} CodeStateIDs')
"

# 3. Instrução para Chat 2
# Ler este handoff + docs/code_dkt_implementation.md Seções 8-14
# Prosseguir da Seção 8 do notebook (grid search)
```

Prompt sugerido para Chat 2:
```
Contexto: Code-DKT Chat 1 concluído. Handoff em docs/code_dkt_handoff.md.
Plano completo: docs/code_dkt_implementation.md.

Sua tarefa é a PARTE 2 (Chat 2 do plano):
- Seção 8: grid search 4 configs × A439 (hidden_dim ∈ {128,200}, dropout ∈ {0.0,0.1})
- Seção 9: 10 runs × 5 assignments × 40 épocas com melhor config
- Seções 10-11: AUC mean±std e Wilcoxon signed-rank
- Seção 12: análise qualitativa de paths (top-5 atenção)
- Seções 13-14: serialização code_dkt_results.pkl + sumário final

Restrições: seeds 42-51, cache_raw de results/code_features_cache.pkl (não re-extrair),
vocab por assignment (train set de cada assignment), schema da Seção 10 do plano.
```

---

## 8. Confirmações go/no-go para Chat 2

- [x] Smoke test convergiu (loss decrescente, `first_auc` smoke > 0.55)? **SIM** (first_auc=0.6307)
- [x] OOV em test set < 30%? **SIM** (tokens=0.6%, paths=6.0%)
- [x] Tempo estimado de 50 runs viável (< 4h)? **SIM** (~25 min estimado com GPU)
- [x] Cache de paths persistido e re-carregável sem erros? **SIM** (206 MB, 53.990 IDs)

**Todos os critérios go/no-go satisfeitos. Chat 2 pode prosseguir.**
