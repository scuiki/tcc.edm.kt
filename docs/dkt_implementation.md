# DKT — Plano de Implementação

Baseado em: Piech et al. (2015) *Deep Knowledge Tracing*; Shi et al. (2022) *Code-DKT*;
análise do repositório oficial Code-DKT (`src/`).

---

## 1. Contexto e dependências

| Artefato | Status | Localização |
|---|---|---|
| `sequences_bkt_dkt.pkl` | Pronto | `results/` |
| `bkt_results.pkl` | Pronto | `results/` |
| `src/data_loader.py` | Pronto | — |
| `src/evaluation.py` | **A criar antes do DKT** | — |
| `src/models/dkt.py` | **A criar** | — |
| `05_dkt.ipynb` | **A criar** | `notebooks/` |

`src/evaluation.py` deve ser criado primeiro para que `bkt.py` e `dkt.py` compartilhem a
mesma lógica de AUC — sem duplicar código entre modelos.

---

## 2. Definição de M (número de problemas por assignment)

Verificado por global scan sobre `sequences_bkt_dkt.pkl` (train + test, todos os estudantes):

| Assignment | M | ProblemIDs |
|---|---|---|
| A439 | 10 | 1, 3, 5, 12, 13, 232, 233, 234, 235, 236 |
| A487 | 10 | 17, 20, 21, 22, 24, 25, 28, 100, 101, 102 |
| A492 | 10 | 31, 32, 33, 34, 36, 37, 38, 39, 40, 128 |
| A494 | 10 | 41, 43, 44, 46, 49, 67, 104, 106, 107, 108 |
| A502 | 10 | 45, 48, 51, 56, 57, 64, 70, 71, 112, 118 |

**M=10 para todos os assignments.** Verificação empírica consistente com `config.py` do
repositório oficial (`self.questions = 10`). O mapeamento `problem_id → index` deve ser
construído a partir do scan global, não per-estudante (um estudante individual pode não ter
tentado todos os 10 problemas).

---

## 3. Codificação de entrada (one-hot 2M)

Para cada tentativa `(q_t, a_t)`, o vetor de entrada `x_t ∈ {0,1}^{2M}`:

```
Se a_t = 1 (acerto):  x_t[problem_to_idx[q_t]]     = 1  (posições 0..M-1)
Se a_t = 0 (erro):    x_t[problem_to_idx[q_t] + M]  = 1  (posições M..2M-1)
Demais posições: 0
```

Exemplo do Code-DKT (M=3): sucesso no problema 1 → `[1,0,0, 0,0,0]`;
falha no problema 1 → `[0,0,0, 1,0,0]`.

Sequências com menos de `max_len=50` passos são **zero-padded à esquerda** (conforme
`readdata.py` do repositório oficial — variável `extra`). A máscara de loss precisa ignorar
os passos de padding.

---

## 4. Saída e loss

O modelo produz `y_t ∈ (0,1)^M`: probabilidade de acerto em cada um dos M problemas no
próximo passo. A predição para `q_{t+1}` é lida como `y_t[problem_to_idx[q_{t+1}]]`.

**Loss (por estudante):**

```
L = Σ_t  BCE(y_t · δ(q_{t+1}),  a_{t+1})
```

onde `δ(q_{t+1})` é o one-hot do problema seguinte (seleciona a entrada relevante de `y_t`).
Implementação de referência em `evaluation.py` do repositório, função `lossFunc.forward`.

---

## 5. Arquitetura LSTM

```
input_dim  = 2 * M  = 20
hidden_dim = 200          # Piech et al. (2015); Code-DKT usa 128 — testar ambos
output_dim = M      = 10
n_layers   = 1
dropout    = aplicado em h_t ao calcular y_t (não na transição de estado)
```

Equações (Piech et al., Apêndice A):

```
i_t = σ(W_ix · x_t + W_ih · h_{t-1} + b_i)
g_t = σ(W_gx · x_t + W_gh · h_{t-1} + b_g)
f_t = σ(W_fx · x_t + W_fh · h_{t-1} + b_f)
o_t = σ(W_ox · x_t + W_oh · h_{t-1} + b_o)
m_t = f_t ⊙ m_{t-1} + i_t ⊙ g_t
h_t = o_t ⊙ m_t
y_t = σ(W_hy · h_t)
```

PyTorch: `nn.LSTM` já implementa isso. Camada de saída: `nn.Linear(hidden_dim, M)` + `nn.Sigmoid`.

**Gradient clipping:** norma máxima de gradiente = 10.0 (Piech et al.).

---

## 6. Protocolo de treinamento

### Splits
- **Treino:** `sequences_bkt_dkt.pkl['train'][aid]` (Release/Train)
- **Teste:** `sequences_bkt_dkt.pkl['test'][aid]` (Release/Test — apenas A439, A487, A492)
- Um modelo independente por assignment

### Hiperparâmetros fixos (do paper)
| Parâmetro | Valor | Fonte |
|---|---|---|
| Otimizador | Adam | Shi et al. (2022) |
| Learning rate | 0.0005 | Shi et al. (2022) |
| Loss | BCE | Piech et al. (2015) |
| max_seq_len | 50 | Shi et al. (2022) |
| Épocas | 40 | Shi et al. (2022) `config.py` |
| Batch size | 128 | Shi et al. (2022) `config.py` |
| Seed | 42 | CLAUDE.md |

### Hiperparâmetros a buscar (random search)
| Parâmetro | Range | Referência |
|---|---|---|
| `hidden_dim` | {64, 128, 200} | Piech=200, Code-DKT=128 |
| `dropout` | [0.0, 0.5] | — |

**Nota sobre random search:** O paper descreve 100 amostras × 10-fold CV para Code-DKT.
Para o DKT baseline (sem code features), usar um grid reduzido é aceitável — o objetivo do
TCC 1 é comparação, não tuning exaustivo. Sugestão: testar `hidden_dim ∈ {128, 200}` com
`dropout ∈ {0.0, 0.2}` (4 combinações × 1 run com seed fixo), selecionar pelo AUC de
validação em Release/Train (hold-out 20% dos estudantes do treino).

---

## 7. Protocolo de avaliação

Idêntico ao BKT para comparação justa:

- **All-attempts AUC:** `compute_auc(pred_df, first_attempt_only=False)`
- **First-attempt AUC:** `compute_auc(pred_df, first_attempt_only=True)`
- Ambas usando `roc_auc_score` pooled (mesma metodologia do repositório oficial —
  `evaluation.py` linhas 72–104: `first_total_gts.extend(...)` → um único `roc_auc_score`)

### Diferença sutil na definição de first_attempt

O repositório oficial usa:
```python
if i == 0 or delta[i-1, j] != 1:  # primeiro em cada run consecutivo
```

Nossa implementação usa `is_first_attempt` (flag da `build_sequences`): primeira tentativa
**absoluta** do estudante no problema dentro do assignment. Nossa definição é mais correta
semanticamente. Manter a nossa.

---

## 8. Estrutura de `src/evaluation.py` (a criar primeiro)

```python
def build_problem_index(sequences: list[dict]) -> dict:
    """Mapeia ProblemID → índice inteiro, via global scan de todas as sequências."""
    ...

def compute_auc(pred_df: pd.DataFrame, first_attempt_only: bool = False) -> float:
    """AUC-ROC pooled. Extraída de bkt.py para ser compartilhada entre modelos."""
    ...
```

`bkt.py` deve ser refatorado para importar `compute_auc` de `evaluation.py` em vez de
defini-la localmente.

---

## 9. Estrutura de `src/models/dkt.py`

```python
class DKTModel(nn.Module):
    """LSTM DKT — Piech et al. (2015)."""
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers, dropout): ...
    def forward(self, x): ...  # x: (batch, seq_len, 2M) → (batch, seq_len, M)

def train_dkt(train_sequences, problem_to_idx, config, seed=42) -> DKTModel: ...
def predict_dkt(model, sequences, problem_to_idx) -> pd.DataFrame: ...
def train_and_evaluate(train_sequences, test_sequences, problem_to_idx, config, seed=42) -> dict: ...
```

Interface análoga ao `bkt.py` para que `07_comparison.ipynb` consuma os dois uniformemente.

---

## 10. Estrutura de `05_dkt.ipynb`

| Seção | Conteúdo |
|---|---|
| 1 — Setup | Imports, SEED, paths, carregar `sequences_bkt_dkt.pkl` |
| 2 — Smoke test | `train_and_evaluate` em A439 com config default; verificar forward pass |
| 3 — Definição de M | `build_problem_index` para todos os 5 assignments; assert M=10 |
| 4 — Seleção de hiperparâmetros | Grid reduzido em subconjunto de A439; escolher melhor config |
| 5 — Treinamento | Um modelo por assignment (A439, A487, A492, A494, A502) |
| 6 — Avaliação | All-attempts AUC + first-attempt AUC; tabela vs BKT |
| 7 — Serialização | `results/dkt_results.pkl` — schema idêntico ao `bkt_results.pkl` |
| 8 — Sumário | Tabela comparativa DKT vs BKT; análise de curvas de loss |

---

## 11. Artefato de saída

`results/dkt_results.pkl` — mesmo schema de `bkt_results.pkl`:

```python
{
  int assignment_id: {
    'all_auc':   float | None,
    'first_auc': float | None,
    'n_train':   int,
    'n_test':    int,
    'model':     DKTModel,      # adicional em relação ao BKT
    'config':    dict,          # hiperparâmetros usados
  }
}
```

---

## 12. Ponto em aberto — split

O repositório oficial do Code-DKT usa **80/20 aleatório de todos os estudantes**
(`train_test_split(students, test_size=0.2, random_state=1)` em `preprocessing.py`),
não o Release/Train + Release/Test oficial. Nós usamos o split oficial.

**Implicações para a comparação com os valores do paper:**
os números da Table 1 e Table 2 não são diretamente comparáveis com os nossos. Ver
discussão separada antes de finalizar o protocolo de avaliação do DKT.
