# Code-DKT — Plano de Implementação

Baseado em: Shi et al. (2022) *Code-DKT: A Code-based Knowledge Tracing Model for Programming Tasks* (EDM 2022);
Piech et al. (2015) *Deep Knowledge Tracing* (NeurIPS 2015);
Pankiewicz, Shi & Baker (2025) *srcML-DKT* (EDM 2025) — motivação para inclusão de Compile.Error, não adotada aqui;
repositório oficial Code-DKT (`experiments/Code-DKT/src/`);
repositório code2vec (`experiments/code2vec/`) — aproveitado para vocabulário e conceito de path.

> **Nota sobre srcML**: A abordagem srcML (Pankiewicz et al., 2025) foi avaliada e descartada para este TCC. Adotamos o Code-DKT original de Shi et al. (2022): apenas eventos `Run.Program`, extração de paths via `javalang`. Consultar `docs/refs/pankiewicz2025_srcml_dkt.md` para referência futura.

---

## 1. Contexto e dependências

### 1.1 Artefatos já disponíveis

| Artefato | Status | Localização |
|---|---|---|
| `sequences_bkt_dkt.pkl` | Pronto | `results/` |
| `bkt_results.pkl` | Pronto | `results/` |
| `dkt_results.pkl` | Pronto | `results/` |
| `src/data_loader.py` | Pronto | — (funções `filter_for_bkt_dkt`, `build_sequences`, `truncate_sequences`) |
| `src/evaluation.py` | Pronto | — (funções `build_problem_index`, `compute_auc`) |
| `src/models/dkt.py` | Pronto | — (interface pública: referência para `code_dkt.py`) |
| CodeStates.csv | Pronto | `data/CSEDM/CodeStates/CodeStates.csv` (1.284.269 linhas, colunas: `CodeStateID`, `Code`) |
| code2vec JavaExtractor JAR | Disponível, mas inutilizável | `experiments/code2vec/JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar` (requer Java — não instalado) |

### 1.2 Artefatos a criar

| Artefato | Localização |
|---|---|
| `src/code_features.py` | Extração de paths AST, construção de vocab, tensorização |
| `src/models/code_dkt.py` | Modelo CodeDKTModel + funções de treino/predição |
| `notebooks/06_code_dkt.ipynb` | Pipeline completo |
| `results/code_features_cache.pkl` | Cache {CodeStateID: raw paths} |
| `results/code_dkt_results.pkl` | Resultados + modelos serializados |

### 1.3 Pré-requisito: instalar javalang

```bash
.venv/bin/pip install javalang==0.13.0
```

`javalang` é a biblioteca Python usada pelo repositório oficial Code-DKT (`path_extractor.py`) para parsear código Java em AST. Não requer Java instalado no sistema. O code2vec JavaExtractor (alternativa mais robusta com javaparser e retry logic) foi considerado, mas descartado por dependência de Java runtime ausente.

---

## 2. Pipeline de dados — Sequências

### 2.1 Reutilização de `sequences_bkt_dkt.pkl`

O Code-DKT de Shi et al. (2022) usa **apenas eventos `Run.Program`** — o mesmo subconjunto do DKT. Portanto, `sequences_bkt_dkt.pkl` é reutilizado diretamente, sem necessidade de gerar novas sequências.

Confirmação empírica (seção do notebook de verificação):

```
sequences_bkt_dkt.pkl:
  EventTypes em train A439: {'Run.Program': 9754}   ← apenas Run.Program
  Chaves top-level: ['train', 'test', 'assignment_ids', 'max_len', 'seed', 'description']
  Chaves por sequência: ['subject_id', 'assignment_id', 'events']
  Colunas de events: [..., 'CodeStateID', 'EventType', 'Score', 'correct', 'is_first_attempt']
```

A coluna `CodeStateID` já presente em cada evento permite o lookup direto no `CodeStates.csv`.

### 2.2 Por que não incluir Compile.Error

O `javalang` falha silenciosamente em código não-compilável (`try/except` retorna `"Uncompilable"` → zero paths). Para não introduzir ruído sistemático (todos os Compile.Error teriam representação nula), o Code-DKT original omite esses eventos. Extensão futura possível com srcML (Pankiewicz et al., 2025, Section 3).

### 2.3 Truncamento e is_first_attempt

Idêntico ao DKT: últimas 50 tentativas (Shi et al., 2022, Section 3). A flag `is_first_attempt` já está calculada nas sequências e é usada para `first_auc`.

---

## 3. Extração de paths AST (code2vec methodology)

### 3.1 Conceito de path (Shi et al., 2022, Section 3; Alon et al., 2019)

Um path AST conecta dois nós folha via seu ancestral comum mais baixo (LCA):

```
p_r = (s_r, o_r, q_r)
```

onde:
- `s_r` = token do nó folha de partida (nome do nó AST, ex.: `MemberReference`, `Literal`)
- `o_r` = sequência de nós intermediários da subida + descida, separados por `@`
  ex.: `BinaryOperation@MethodInvocation@BlockStatement`
- `q_r` = token do nó folha de chegada

Restrições de filtragem (Code-DKT `config.py`):
- `max_path_length = 8`: comprimento máximo do path (número de nós no caminho)
- `max_path_width = 2`: largura máxima (diferença de posição entre os nós folha na árvore)

### 3.2 Pseudo-algoritmo de extração (adaptado de `path_extractor.py`)

```
função extract_paths(codigo_java: str) -> list[Tuple[str, str, str]]:
    tentar:
        tree = javalang.parse.parse_member_declaration(codigo_java)
    exceto qualquer_erro:
        retornar []    # "Uncompilable" → zero paths

    head = construir_arvore(tree)           # Node tree via anytree
    leaf_nodes = encontrar_folhas(head)     # nós sem filhos
    max_depth = profundidade_maxima(leaf_nodes)

    walker = Walker()
    paths = []
    para cada par (leaf_i, leaf_j) com i < j:
        (upstream, lca, downstream) = walker.walk(leaf_i, leaf_j)
        walk_path = [tokens dos nós upstream] + [token lca] + [tokens dos nós downstream]

        # Filtrar por comprimento e largura
        se length(walk_path) > max_path_length: continuar
        se abs(posicao(leaf_i) - posicao(leaf_j)) > max_path_width: continuar

        start_token = walk_path[0]
        end_token   = walk_path[-1]
        path_str    = "@".join(walk_path)   # sequência completa incluindo start e end
        paths.append((start_token, path_str, end_token))

    retornar paths
```

**Formato de saída**: cada path é uma tripla `(start_token, path_str, end_token)`. O `path_str` inclui todos os nós do caminho (inclusive os extremos). Este formato é compatível com o code2vec e com o `path_extractor.py` do Code-DKT.

### 3.3 Amostragem R = 50 paths por submissão

Shi et al. (2022) testaram R ∈ {30, 50, 100, 300} e selecionaram **R = 50** (Table 3 do paper, hiperparâmetros finais). Quando uma submissão tem mais de 50 paths extraídos, amostrar aleatoriamente 50 com `random.sample(paths, 50)` usando `random.seed(SEED)`. Quando tem menos de 50, usar os disponíveis e preencher o restante com `(PAD, PAD, PAD)`.

### 3.4 Cache de features

Para evitar re-extração de 69.627 CodeStateIDs:

```
Fase 1 — Extrair raw paths (strings):
  cache_raw: dict{CodeStateID: list[Tuple[str,str,str]]}
  Salvo em results/code_features_cache.pkl

  Iterar sobre todos CodeStateIDs únicos no train + test de sequences_bkt_dkt.pkl.
  Para cada CodeStateID: lookup em CodeStates.csv → extrair paths → amostrar R=50.

Fase 2 — Converter para índices (após construir vocabulário):
  cache_idx: dict{CodeStateID: np.array de shape (R, 3), dtype=int64}
  Armazenado em memória durante o treinamento; não salvo em arquivo separado.
```

---

## 4. Vocabulário

### 4.1 Estrutura (inspirada em `code2vec/vocabularies.py`)

Duas tabelas Python puras (sem TensorFlow), construídas **apenas dos paths do train set**:

| Tabela | Conteúdo | Índices especiais |
|---|---|---|
| `token_to_idx: dict[str, int]` | start e end tokens (leaf node names do AST) | 0 = PAD/UNK |
| `path_to_idx: dict[str, int]` | path strings (sequência completa de nós) | 0 = PAD/UNK |

O índice 0 serve como PAD (para preenchimento de paths abaixo de R) e UNK (para tokens/paths fora do vocabulário do treino). Esta convenção segue `code2vec/config.py`, `SEPARATE_OOV_AND_PAD = False`.

**Construção:**

```
Coletar todos os (start_token, path_str, end_token) de todos os CodeStateIDs do TRAIN set.
token_vocab = {token: idx+1 for idx, token in enumerate(sorted(unique_tokens))}
path_vocab  = {path:  idx+1 for idx, path  in enumerate(sorted(unique_paths))}
# idx começa em 1; 0 reservado para PAD/UNK
```

Sem limite de tamanho do vocabulário (o CSEDM é um dataset pequeno; o code2vec usa limites de 1.3M apenas para datasets de grande escala como o Java-14M).

### 4.2 Serialização

```python
vocab = {
    'token_to_idx': token_to_idx,   # dict[str, int]
    'path_to_idx':  path_to_idx,    # dict[str, int]
    'node_count':   len(token_to_idx),
    'path_count':   len(path_to_idx),
}
```

Salvo como chave `'vocab'` em `code_dkt_results.pkl` para cada assignment (o vocabulário é construído por assignment — os problemas de cada assignment podem ter diferentes padrões de código).

---

## 5. Tensorização

### 5.1 Representação de cada evento na sequência

Para um estudante com sequência de L eventos (L ≤ 50):

```
Por evento t com problema q_t, acerto a_t, e CodeStateID c_t:

  x_t = one-hot 2M (idêntico ao DKT):
    x_t[idx(q_t)]    = 1  se a_t = 1  (posições 0..M-1)
    x_t[idx(q_t)+M]  = 1  se a_t = 0  (posições M..2M-1)

  code_t = matriz (R, 3) de índices:
    code_t[r] = [token_to_idx.get(s_r, 0),
                 path_to_idx.get(o_r, 0),
                 token_to_idx.get(q_r, 0)]

  Concatenação final para o passo t:
    input_t = concat(x_t, code_t.reshape(R*3)) ∈ R^{2M + R*3}
                                                 = R^{20 + 150}
                                                 = R^{170}
```

### 5.2 Tensores de batch

```
X:      (N, 50, 170)  — input concatenado, com left-zero-padding (readdata.py: variável 'extra')
Y_next: (N, 50, M)    — one-hot do próximo problema delta(q_{t+1}) (idêntico ao DKT)
mask:   (N, 50)       — bool, True onde há dado real
```

O shape `[maxstep, 2*numofques + MAX_CODE_LEN*3]` espelha exatamente a linha 113 de `readdata.py` do repositório oficial.

### 5.3 Separação no modelo

O modelo CodeDKTModel recebe `X` e internamente separa:

```
rnn_first_part = X[:, :, :2M]          # (B, L, 20) — parte DKT one-hot
c2v_input      = X[:, :, 2M:]          # (B, L, 150) — parte code2vec
               = c2v_input.reshape(B, L, R, 3).long()  # (B, L, R, 3)
```

Esta separação é idêntica a `c2vRNNModel.py`, linhas 39–42.

---

## 6. Arquitetura

### 6.1 Embeddings e representação de path

Cada path `p_r = (s_r, o_r, q_r)` em cada passo `t` é embeddado como (Shi et al., 2022, Section 3):

```
e_r = concat(embed_nodes(s_r), embed_paths(o_r), embed_nodes(q_r), x_t)
    = concat([100], [100], [100], [20])
    = vetor de dimensão 320 = input_dim + 300
```

onde:
- `embed_nodes`: tabela `nn.Embedding(node_count+2, 100)` — compartilhada para start e end tokens
- `embed_paths`: tabela `nn.Embedding(path_count+2, 100)` — exclusiva para path sequences
- `x_t`: one-hot 2M = 20 concatenado a cada path embed (Shi et al., 2022, ablation Table 4: correctness em ambos os pontos melhora o resultado)

O `+2` nas tabelas de embedding reserva slots para PAD e UNK, conforme implementação de `c2vRNNModel.py`, linha 14.

### 6.2 Mecanismo de atenção (Score-Attended Path Selection)

Shi et al. (2022), Section 3:

```
E = {e_1, e_2, ..., e_R}        shape: (B, L, R, 320)

# Transformação aprendível
E_hat = tanh(W_0 @ E + b_0)     shape: (B, L, R, 320)
    onde W_0 ∈ R^{320×320}

# Pesos de atenção (escalar por path)
alpha = SoftMax(W_a @ E_hat)     shape: (B, L, R, 1)
    onde W_a ∈ R^{320×1}

# Vetor de código: média ponderada dos path embeds
z = sum(alpha * E, dim=R)        shape: (B, L, 320)
```

**Nota de implementação**: a atenção usa o embedding ORIGINAL `E` (não transformado `E_hat`) na soma ponderada final, conforme `c2vRNNModel.py` linha 59: `code_vectors = torch.sum(torch.mul(full_embed, attention_weights), dim=2)`.

### 6.3 LSTM e camada de saída

Input do LSTM em cada passo `t` (Shi et al., 2022, Section 3):

```
rnn_input_t = concat(x_t, z_t)     ∈ R^{2M + 320} = R^{340}
h_t = LSTM(rnn_input_t, h_{t-1})   h_t ∈ R^{128}
y_t = sigmoid(W_fc @ h_t)          y_t ∈ (0,1)^M = (0,1)^{10}
```

Parâmetros do LSTM: `nn.LSTM(input_size=340, hidden_size=128, num_layers=1, batch_first=True)`.

**Dropout**: aplicado em `h_t` antes de `W_fc` (mesma posição do DKT — Piech et al., 2015, Section 3). Não aplicado na transição interna do LSTM.

**Gradient clipping**: norma máxima = 10.0 (Piech et al., 2015).

### 6.4 Loss (idêntica ao DKT)

```
L = sum_t BCE(y_t^T * delta(q_{t+1}), a_{t+1})
```

Piech et al. (2015), Eq. 3. Implementação em `src/models/dkt.py:dkt_loss` — reutilizar ou replicar com adaptação para o batch shape do Code-DKT.

---

## 7. Diferenças Code-DKT vs DKT

| Aspecto | DKT (Piech et al., 2015) | Code-DKT (Shi et al., 2022) |
|---|---|---|
| Input por passo | `x_t ∈ R^{2M=20}` | `concat(x_t, z_t) ∈ R^{2M+320=340}` |
| Módulo de código | Nenhum | Embedding + atenção Score-Attended |
| LSTM input dim | 20 | 340 |
| hidden_dim | 200 (Piech et al.) ou 128 (tuning) | 128 (config.py Code-DKT) |
| Embedding size | — | 300 total (100 por componente) |
| Parâmetros extras | — | `embed_nodes`, `embed_paths`, `path_transformation_layer`, `attention_layer` |
| Sequências | sequences_bkt_dkt.pkl | sequences_bkt_dkt.pkl + CodeStates.csv |
| Pré-requisito novo | — | `pip install javalang` |
| Interface pública | `train_dkt`, `predict_dkt`, `train_and_evaluate` | Idêntica (mesmo padrão) |

---

## 8. Protocolo de treinamento

### 8.1 Hiperparâmetros fixos (do paper)

| Parâmetro | Valor | Fonte |
|---|---|---|
| Otimizador | Adam | Shi et al. (2022), Table 3 |
| Learning rate | 0.0005 | Shi et al. (2022), Table 3 |
| Loss | BCE | Piech et al. (2015), Eq. 3 |
| max_seq_len | 50 | Shi et al. (2022), Section 3 |
| Épocas | 40 | Shi et al. (2022), `config.py` linha 6 |
| Batch size | 128 | Shi et al. (2022), `config.py` linha 4 |
| R (paths por submissão) | 50 | Shi et al. (2022), Table 3 |
| max_path_length | 8 | `config.py` Code-DKT, linha 11 |
| max_path_width | 2 | `config.py` Code-DKT, linha 12 |
| node_embed_dim | 100 | `c2vRNNModel.py`, linhas 14–15 (embedding_size=300/3) |
| path_embed_dim | 100 | `c2vRNNModel.py`, linhas 14–15 |
| Gradient clip norm | 10.0 | Piech et al. (2015) |
| Seed | 42 | CLAUDE.md |

### 8.2 Hiperparâmetros a buscar (grid reduzido)

O paper testa 100 configurações × 10 runs com CV. Para o TCC 1 (objetivo: comparação, não tuning exaustivo), usar grid reduzido:

| Parâmetro | Range | Referência |
|---|---|---|
| `hidden_dim` | {64, 128} | Code-DKT usa 128; DKT usa 200 |
| `dropout` | {0.0, 0.1} | `c2vRNNModel.py` linha 28: `p=0.1` |

4 combinações × 1 run com seed=42. Seleção pelo `first_auc` no subconjunto de validação de A439 (hold-out 20% dos estudantes do treino).

---

## 9. Protocolo de avaliação

Idêntico ao BKT e DKT para comparação justa:

- **All-attempts AUC**: `compute_auc(pred_df, first_attempt_only=False)`
- **First-attempt AUC**: `compute_auc(pred_df, first_attempt_only=True)`
- AUC pooled (todas as predições concatenadas — metodologia Shi et al., 2022 e Piech et al., 2015)

### 9.1 Valores alvo (Shi et al., 2022)

| Assignment | Overall AUC (Table 1) | First-Attempt AUC (Table 2) |
|---|---|---|
| A439 (A1) | 74.31% (STD=0.90%) | 75.74% (STD=0.69%) |
| A487 (A2) | 76.56% | — |
| A492 (A3) | 80.40% | — |
| A494 (A4) | 72.75% | — |
| A502 (A5) | 79.14% | — |

Os valores do paper são médias de 10 runs; com 1 run e seed=42, esperar variabilidade de ±3pp.

### 9.2 Critério de conclusão do TCC 1

`first_auc` do Code-DKT próximo a 74% para A439 (±3%), superior ao DKT (CLAUDE.md).

---

## 10. Schema de `code_dkt_results.pkl`

Compatível com `dkt_results.pkl` para que `07_comparison.ipynb` consuma os dois uniformemente:

```python
{
  int assignment_id: {
    'all_auc':          float | None,
    'first_auc':        float | None,
    'n_train_events':   int,
    'n_test_events':    int,
    'model':            CodeDKTModel,   # nn.Module treinado
    'config':           dict,           # hiperparâmetros usados
    'vocab': {                          # adicional em relação ao DKT
        'token_to_idx': dict[str, int],
        'path_to_idx':  dict[str, int],
        'node_count':   int,
        'path_count':   int,
    },
  }
}
```

---

## 11. Estrutura de `src/code_features.py`

```python
def load_code_states(data_dir: Path) -> dict[str, str]:
    """Carrega CodeStates.csv como dict {CodeStateID: code_string}."""
    ...

def extract_paths_javalang(
    code: str,
    max_path_length: int = 8,
    max_path_width: int = 2,
    R: int = 50,
    seed: int = 42,
) -> list[tuple[str, str, str]]:
    """Extrai R paths AST do código Java via javalang. Retorna lista de (start, path, end)."""
    ...

def build_vocab(
    cache_raw: dict[str, list[tuple[str, str, str]]],
) -> tuple[dict[str, int], dict[str, int]]:
    """Constrói token_to_idx e path_to_idx a partir do cache de paths de treino."""
    ...

def paths_to_tensor(
    paths: list[tuple[str, str, str]],
    token_to_idx: dict[str, int],
    path_to_idx: dict[str, int],
    R: int = 50,
) -> np.ndarray:
    """Converte lista de paths em array (R, 3) de índices. Padding com zeros."""
    ...

def build_code_input_tensor(
    sequences: list[dict],
    code_states: dict[str, str],
    token_to_idx: dict[str, int],
    path_to_idx: dict[str, int],
    max_len: int = 50,
    R: int = 50,
) -> tuple[Tensor, Tensor]:
    """Constrói X_code (N, max_len, R*3) e X_dkt (N, max_len, 2M) para um assignment."""
    ...
```

---

## 12. Estrutura de `src/models/code_dkt.py`

```python
class CodeDKTModel(nn.Module):
    """Code-DKT — Shi et al. (2022). LSTM + code2vec attention."""
    def __init__(self, input_dim, hidden_dim, output_dim, node_count, path_count,
                 n_layers=1, dropout=0.0, R=50, node_embed_dim=100, path_embed_dim=100): ...
    def forward(self, x): ...  # x: (B, L, 2M+R*3) → (B, L, M)

def train_code_dkt(train_sequences, problem_to_idx, vocab, config, code_states, seed=42) -> CodeDKTModel: ...
def predict_code_dkt(model, sequences, problem_to_idx, vocab, code_states) -> pd.DataFrame: ...
def train_and_evaluate(train_sequences, test_sequences, problem_to_idx, vocab,
                        config, code_states, seed=42) -> dict: ...
```

Interface idêntica ao `dkt.py` para que `07_comparison.ipynb` consuma os dois uniformemente.

---

## 13. Estrutura de `notebooks/06_code_dkt.ipynb`

| Seção | Conteúdo |
|---|---|
| 1 — Setup | Imports, SEED=42, device (CUDA), paths; carregar `sequences_bkt_dkt.pkl` |
| 2 — CodeStates | Carregar `CodeStates/CodeStates.csv`; verificar cobertura de CodeStateID |
| 3 — Extração de paths | `extract_paths_javalang` em sample de 10 submissões; inspecionar paths extraídos |
| 4 — Cache de features | Extrair paths para todos os CodeStateIDs únicos (train + test); salvar `code_features_cache.pkl` |
| 5 — Vocabulário | `build_vocab` sobre train CodeStateIDs; reportar `node_count`, `path_count` |
| 6 — Tensorização | `build_code_input_tensor` para A439; verificar shapes; smoke test forward pass |
| 7 — Smoke test | `train_and_evaluate` em A439 com config default (5 épocas); verificar loss decresce |
| 8 — Seleção de hiperparâmetros | Grid search 4 combinações × A439; escolher melhor config por `first_auc` |
| 9 — Treinamento completo | 5 assignments × 40 épocas com melhor config |
| 10 — Avaliação | All-attempts AUC + first-attempt AUC; tabela vs BKT e DKT |
| 11 — Análise qualitativa de paths | Inspecionar paths com maiores pesos de atenção para exemplos corretos vs errados |
| 12 — Serialização | `results/code_dkt_results.pkl` — schema com `vocab` adicional |
| 13 — Sumário | Tabela comparativa BKT vs DKT vs Code-DKT; conclusão para TCC 1 |

---

## 14. Pontos em aberto

Os itens abaixo precisam de investigação empírica antes ou durante a implementação:

1. **Cobertura de parsing por javalang**: Quantas submissões Run.Program do CSEDM resultam em zero paths (`"Uncompilable"`)? O `program_parser` usa `parse_member_declaration` (adequado para métodos Java isolados, formato típico do CSEDM). Verificar no início do notebook (Seção 3) com uma amostra de 1000 CodeStateIDs.

2. **Custo de extração srcML**: A extração de paths javalang para ~69.627 CodeStateIDs únicos pode levar dezenas de minutos. Medir o tempo por submissão na Seção 3 e estimar tempo total antes de rodar o cache completo (Seção 4). Considerar paralelização com `multiprocessing.Pool`.

3. **OOV em teste**: Tokens e paths presentes no test set mas ausentes no train set são mapeados para índice 0 (PAD/UNK). O impacto no AUC depende da frequência de OOV. Reportar percentual de OOV na Seção 5 como verificação de sanidade.

4. **Vocabulário por assignment ou global**: O plano recomenda vocabulário por assignment (cada assignment tem padrões de código distintos e problemas diferentes). Se o vocabulário global for muito grande, considerar limitação por frequência mínima (ex.: descartar tokens com contagem < 3), seguindo o code2vec (vocabularies.py, `create_from_freq_dict`).

5. **Compatibilidade do code2vec JavaExtractor para uso futuro**: O JAR em `experiments/code2vec/JavaExtractor/JPredict/target/` usa javaparser com retry logic mais robusto que javalang. Se Java JDK for instalado futuramente (`sudo apt install default-jdk`), o `extractor.py` pode ser adaptado para o pipeline deste TCC com melhor cobertura de código não-compilável.
