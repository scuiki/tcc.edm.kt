# Code-DKT — Plano de Implementação

Baseado em: Shi et al. (2022) *Code-DKT: A Code-based Knowledge Tracing Model for Programming Tasks* (EDM 2022);
Piech et al. (2015) *Deep Knowledge Tracing* (NeurIPS 2015);
repositório oficial Code-DKT (`experiments/Code-DKT/src/`);
repositório code2vec (`experiments/code2vec/`) — aproveitado para vocabulário e conceito de path.

Escopo deste plano: Code-DKT vanilla conforme Shi et al. (2022) — apenas eventos `Run.Program`, extração de paths via `javalang`. Comparação direta de protocolo com o paper de referência.

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

### 1.4 Hardware e implicações de protocolo

O protocolo de 10 runs (Seção 8.3) é o gargalo de compute deste plano. Resumo:

| Etapa | Bottleneck | GPU acelera? |
|---|---|---|
| Extração javalang de paths (~69k CodeStateIDs) | CPU + Python | **Não** — paralelizar com `multiprocessing.Pool(n_workers=N_CPU)` |
| Construção do vocab | CPU single-thread | Não |
| Tensorização (lookup índices) | CPU single-thread | Não |
| **Treino do CodeDKTModel** | LSTM + embedding + attention | **Sim, 10–20×** sobre CPU |
| Predição | Mesmo do treino | Sim |

**Hardware-alvo**: NVIDIA RTX 4050 (6 GB VRAM). Para este modelo (input_dim=170, hidden ∈ {128, 200}, batch=128, seq=50), uso estimado < 1 GB VRAM — folgado.

**Estimativas com GPU**:
- 1 run de 40 épocas em A439 (~330 alunos treino): 1–3 min
- 10 runs × 5 assignments = 50–150 min total de treino final
- Cache de paths permanece CPU-bound: dezenas de minutos mesmo com paralelização

**Fallback documentado se GPU indisponível**: reduzir para 3 runs (seeds 42, 43, 44) e reportar mean ± std com a ressalva metodológica de que o paper usou 10 runs.

### 1.5 Reprodutibilidade

Checklist obrigatório a aplicar nos notebooks `06_code_dkt.ipynb` e em todo módulo que faça operações estocásticas:

```python
import random, numpy as np, torch

SEED = 42

def set_global_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

Pontos específicos:
- **Multiprocessing**: ao usar `Pool` para extração de paths, propagar seed via `initializer=set_global_seed` e seed derivada do `worker_id` para diversificar amostragem dentro de cada submissão sem perder reprodutibilidade global.
- **Split de validação intra-treino** (Seção 8.2): `train_test_split(..., random_state=SEED, stratify=...)` — fixar seed separadamente.
- **Multi-run** (Seção 8.3): seeds 42, 43, ..., 51. Antes de cada run, chamar `set_global_seed(seed_i)`.
- **CUDA não-determinístico em alguns kernels LSTM**: documentar no notebook se `torch.use_deterministic_algorithms(True)` causar erros conhecidos do PyTorch para LSTM em GPU; nesse caso, aceitar não-determinismo mínimo e reportar.

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

O `javalang` falha silenciosamente em código não-compilável (`try/except` retorna `"Uncompilable"` → zero paths). Para não introduzir ruído sistemático (todos os Compile.Error teriam representação nula), o Code-DKT original (Shi et al., 2022) omite esses eventos. Adotamos o mesmo critério para fidelidade ao protocolo de referência.

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

### 3.5 Métricas de transparência a reportar

Durante a extração, registrar e incluir no notebook:

1. **Taxa de parsing javalang** sobre Run.Program (% submissões com ≥1 path extraído vs % "Uncompilable")
2. **Distribuição de paths por submissão** antes da amostragem R=50 (mediana, p95, p99)
3. **Tempo médio de extração por submissão**

Esses números são *características descritivas do dataset sob o protocolo Code-DKT*, não gates de decisão. Shi et al. (2022) usaram exatamente o mesmo `javalang` no mesmo CSEDM e reportaram AUC 74.31% — qualquer perda por não-parsing está embutida no número de referência. Reportar nossos valores serve para transparência metodológica e enriquece a discussão (eventualmente motivando a Fase 2 de srcML).

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
| `hidden_dim` | {128, 200} | Code-DKT usa 128; nosso DKT (`05_dkt.ipynb`) selecionou 200 — incluir ambos para comparação justa |
| `dropout` | {0.0, 0.1} | `c2vRNNModel.py` linha 28: `p=0.1` |

4 combinações × 1 run com seed=42 (seleção). Seleção pelo `first_auc` no subconjunto de validação de A439 (hold-out 20% dos estudantes do treino, `train_test_split(..., random_state=SEED, stratify_by=class_or_first_attempt_outcome)`). A escolha de A439 reflete que é o assignment-âncora do critério de conclusão do TCC 1 (CLAUDE.md).

### 8.3 Protocolo multi-run (avaliação final)

Após selecionada a melhor configuração de hiperparâmetros, **rodar 10 runs com seeds 42–51** por assignment, conforme Shi et al. (2022): *"each configuration was evaluated 10 times to account for random initialization variance"*.

Para cada assignment × seed:
1. `set_global_seed(seed)` antes de instanciar o modelo
2. Treinar com hiperparâmetros selecionados (40 épocas)
3. Predizer no test set
4. Persistir: `(all_auc, first_auc, model_state_dict, pred_df)`

Reportar para cada assignment: `mean ± std` de `all_auc` e `first_auc` sobre os 10 runs. Comparar com `mean ± std` do DKT (idêntico protocolo, 10 runs) e BKT (idem).

**Custo estimado** (GPU): 5 assignments × 10 runs × ~2 min/run = ~100 min de treino.

**Fallback CPU/sem GPU**: 3 runs (seeds 42–44) com nota metodológica explícita de divergência do paper.

---

## 9. Protocolo de avaliação

Idêntico ao BKT e DKT para comparação justa:

- **All-attempts AUC**: `compute_auc(pred_df, first_attempt_only=False)`
- **First-attempt AUC**: `compute_auc(pred_df, first_attempt_only=True)`
- AUC pooled (todas as predições concatenadas — metodologia Shi et al., 2022 e Piech et al., 2015)
- **Multi-run**: `mean ± std` sobre 10 runs (Seção 8.3) por assignment

### 9.1 Valores alvo (Shi et al., 2022)

| Assignment | Overall AUC (Table 1) | First-Attempt AUC (Table 2) |
|---|---|---|
| A439 (A1) | 74.31% (STD=0.90%) | 75.74% (STD=0.69%) |
| A487 (A2) | 76.56% | — |
| A492 (A3) | 80.40% | — |
| A494 (A4) | 72.75% | — |
| A502 (A5) | 79.14% | — |

Os valores do paper são médias de 10 runs. Nosso protocolo (Seção 8.3) replica esse N — comparação direta de `mean ± std` é válida.

### 9.2 Teste de significância (Wilcoxon signed-rank)

Critério 3 do CLAUDE.md: comparação estatística entre modelos.

Para cada par de modelos (BKT vs DKT, DKT vs Code-DKT, BKT vs Code-DKT):
1. Para cada assignment × seed (5 × 10 = 50 observações), coletar `(first_auc_modelo_A, first_auc_modelo_B)`
2. Aplicar `scipy.stats.wilcoxon(auc_A, auc_B, alternative='less')` (hipótese: A < B)
3. Reportar estatística W, p-valor e tamanho de efeito (r = Z / √N)

Decisão: p < 0.05 → diferença significativa. Para Code-DKT vs DKT, esperar p < 0.05 favorecendo Code-DKT em todos os assignments (consistente com +3.07–4.00pp de Shi et al., 2022, Table 1).

Reportar também: tabela com `mean(diff) ± std(diff)` por par, intervalo de confiança 95% via bootstrap (1000 resamples) sobre os 50 pares.

### 9.3 Critério de conclusão do TCC 1

`first_auc` do Code-DKT próximo a 74% para A439 (CLAUDE.md critério 1: ±3%), superior ao DKT com significância estatística (Wilcoxon p < 0.05).

---

## 10. Schema de `code_dkt_results.pkl`

Compatível com `dkt_results.pkl` para que `07_comparison.ipynb` consuma os dois uniformemente. Estendido para multi-run (Seção 8.3):

```python
{
  int assignment_id: {
    # Agregado dos 10 runs (chaves principais — consumidas por 07_comparison)
    'all_auc_mean':     float,          # media sobre 10 runs
    'all_auc_std':      float,
    'first_auc_mean':   float,
    'first_auc_std':    float,

    # Detalhe por run (para Wilcoxon e analises adicionais)
    'runs': [
        {
            'seed':              int,
            'all_auc':           float,
            'first_auc':         float,
            'pred_df':           pd.DataFrame,   # predicoes do test set
            'model_state_dict':  dict,           # torch state_dict (nao o modelo completo)
        },
        ...   # 10 entradas
    ],

    'n_train_events':   int,
    'n_test_events':    int,
    'config':           dict,           # hiperparametros selecionados (Secao 8.2)
    'vocab': {                          # adicional em relacao ao DKT
        'token_to_idx': dict[str, int],
        'path_to_idx':  dict[str, int],
        'node_count':   int,
        'path_count':   int,
    },
  }
}
```

**Nota sobre tamanho**: 10 `pred_df` + 10 `model_state_dict` por assignment × 5 assignments pode gerar arquivo de ~100–300 MB. Se exceder limite gitignore-friendly, considerar serializar `model_state_dict` em arquivos separados (`results/code_dkt_models/{assignment}_{seed}.pt`) e manter apenas referências no pickle.

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
| 1 — Setup | Imports, `set_global_seed(42)`, device (CUDA), paths; carregar `sequences_bkt_dkt.pkl` |
| 2 — CodeStates | Carregar `CodeStates/CodeStates.csv`; verificar cobertura de CodeStateID |
| 3 — Extração de paths | `extract_paths_javalang` em sample de 100 submissões; **medir taxa de parsing, distribuição de paths, tempo médio** (métricas de transparência da Seção 3.5); inspecionar 3 exemplos de paths extraídos |
| 4 — Cache de features | Extrair paths para todos os CodeStateIDs únicos (train + test); salvar `code_features_cache.pkl`. Paralelizar com `multiprocessing.Pool` |
| 5 — Vocabulário | `build_vocab` sobre train CodeStateIDs; reportar `node_count`, `path_count`, **% OOV no test set** |
| 6 — Tensorização | `build_code_input_tensor` para A439; verificar shapes; smoke test forward pass |
| 7 — Smoke test | `train_and_evaluate` em A439 com config default (5 épocas, seed=42); verificar loss decresce; reportar `first_auc` smoke como sanity check |
| 8 — Seleção de hiperparâmetros | Grid search 4 combinações × A439 (Seção 8.2); escolher melhor config por `first_auc` no validation set |
| 9 — Treinamento completo (10 runs) | 5 assignments × 10 runs (seeds 42–51) × 40 épocas com melhor config (Seção 8.3); barra de progresso |
| 10 — Avaliação | `mean ± std` de all-attempts AUC + first-attempt AUC por assignment; tabela vs BKT e DKT (Seção 9) |
| 11 — Teste de significância | Wilcoxon signed-rank entre pares de modelos (Seção 9.2); reportar W, p-valor, intervalo de confiança 95% bootstrap |
| 12 — Análise qualitativa de paths | **Deliverable concreto**: tabela com top-5 paths de maior atenção em 3 problemas selecionados (1 baixa, 1 média, 1 alta taxa de acerto) × {predição correta, predição errada} = 30 paths anotados com (start_token, path_str, end_token, peso_atenção). Discussão de 2 parágrafos relacionando paths salientes à dificuldade do problema |
| 13 — Serialização | `results/code_dkt_results.pkl` — schema multi-run da Seção 10 |
| 14 — Sumário | Tabela comparativa BKT vs DKT vs Code-DKT com `mean ± std` + significância; conclusão para TCC 1 |

---

## 14. Pontos em aberto

Os itens abaixo precisam de investigação empírica durante a implementação. **Nenhum é gate de decisão** — todos viram métricas reportadas no notebook (transparência metodológica).

1. **Cobertura de parsing por javalang**: Quantas submissões Run.Program do CSEDM resultam em zero paths (`"Uncompilable"`)? O `program_parser` usa `parse_member_declaration` (adequado para métodos Java isolados, formato típico do CSEDM). Medir na Seção 3 (sample de 100) e na Seção 4 (cache completo). Reportar como descritor do dataset sob o protocolo Code-DKT — Shi et al. (2022) usaram exatamente o mesmo javalang no mesmo dataset, qualquer perda está embutida no AUC de referência (74.31%).

2. **Custo de extração**: A extração de paths javalang para ~69.627 CodeStateIDs únicos pode levar dezenas de minutos (CPU-bound, GPU não acelera — Seção 1.4). Medir o tempo por submissão na Seção 3 (sample) e estimar tempo total antes de rodar o cache completo (Seção 4). Paralelização com `multiprocessing.Pool(n_workers=N_CPU)` é esperada.

3. **OOV em teste**: Tokens e paths presentes no test set mas ausentes no train set são mapeados para índice 0 (PAD/UNK). O impacto no AUC depende da frequência de OOV. Reportar percentual de OOV na Seção 5 como verificação de sanidade.

4. **Vocabulário por assignment ou global**: O plano recomenda vocabulário por assignment (cada assignment tem padrões de código distintos e problemas diferentes). Se o vocabulário por assignment for muito grande, considerar limitação por frequência mínima (ex.: descartar tokens com contagem < 3), seguindo o code2vec (vocabularies.py, `create_from_freq_dict`).

---

## 15. Handoff document — Chat 1 → Chat 2

Este plano é executado em **dois chats sequenciais** (decisão registrada em discussão com o usuário):

- **Chat 1 (Implementação + Smoke test)**: cobre Seções 1.3, 11, 12 do plano (módulos `src/code_features.py`, `src/models/code_dkt.py`) e Seções 1–7 do notebook (até smoke test passar).
- **Chat 2 (Experimentação + Análise)**: cobre Seções 8–14 do notebook (grid search, 10 runs × 5 assignments, Wilcoxon, análise qualitativa, serialização, sumário).

Ao final do Chat 1, gerar `docs/code_dkt_handoff.md` com o template abaixo. O Chat 2 entra com contexto fresco e consulta este handoff para retomar.

### Template `docs/code_dkt_handoff.md`

```markdown
# Code-DKT — Handoff Chat 1 → Chat 2

Gerado por: Chat 1 em <YYYY-MM-DD HH:MM>
Status do Chat 1: <CONCLUÍDO | BLOQUEADO>

## 1. Artefatos produzidos

| Artefato | Caminho | Status |
|---|---|---|
| Módulo extração | `src/code_features.py` | <pronto / parcial> |
| Módulo modelo | `src/models/code_dkt.py` | <pronto / parcial> |
| Notebook | `notebooks/06_code_dkt.ipynb` (seções 1–7) | <pronto / parcial> |
| Cache de paths | `results/code_features_cache.pkl` | <pronto / pendente> |
| Vocab (apenas A439) | embutido no notebook | <pronto / pendente> |

## 2. Métricas de transparência (Seção 3.5 do plano)

- **Taxa de parsing javalang** sobre Run.Program: <X%> sucesso, <Y%> "Uncompilable"
- **Distribuição de paths por submissão** (antes de R=50): mediana=<>, p95=<>, p99=<>
- **Tempo médio de extração por submissão**: <ms>
- **Tempo total do cache** (com `Pool(n=<>)`): <min>
- **Tamanho de `code_features_cache.pkl`**: <MB>

## 3. Vocabulário A439

- `node_count`: <>
- `path_count`: <>
- **OOV em test set**: tokens=<X%>, paths=<Y%>

## 4. Smoke test (A439, 5 épocas, seed=42)

- Loss inicial → final: <> → <>
- `first_auc` (smoke): <>
- Tempo de treino: <min>
- Tempo de inferência no test: <s>
- Pico de VRAM (se GPU): <MB>

## 5. Decisões tomadas no Chat 1

<lista de decisões de design que divergiram do plano ou exigiram interpretação>

## 6. Issues conhecidas / TODO para Chat 2

<lista de pontos de atenção ou bugs menores deixados para resolver>

## 7. Comando para Chat 2 retomar

O notebook está em estado executável até a Seção 7. Para Chat 2:

1. Verificar que `.venv` tem javalang instalado: `.venv/bin/python -c "import javalang; print(javalang.__version__)"`
2. Verificar GPU: `.venv/bin/python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"`
3. Carregar `code_features_cache.pkl` (já existe — não re-extrair)
4. Prosseguir da Seção 8 do notebook (grid search)

## 8. Confirmações go/no-go para Chat 2

- [ ] Smoke test convergiu (loss decrescente, `first_auc` smoke > 0.55)? <SIM/NÃO>
- [ ] OOV em test set < 30%? <SIM/NÃO>
- [ ] Tempo estimado de 50 runs (5 assignments × 10 seeds) com hardware atual é viável (< 4h)? <SIM/NÃO>
- [ ] Cache de paths persistido e re-carregável sem erros? <SIM/NÃO>

Se algum NÃO, Chat 2 deve ler a seção "Decisões tomadas" e ajustar protocolo (ex.: fallback de 3 runs se hardware limitar tempo).
```
