# Plano TCC 1 — EDM & Knowledge Tracing sobre CSEDM/ProgSnap2

## Context

O TCC 1 tem como objetivo aplicar Educational Data Mining (EDM) e Learning Analytics ao
dataset CSEDM (formato ProgSnap2 v6), comparando três modelos de Knowledge Tracing —
BKT, DKT e Code-DKT (com srcML) — e justificando qual é o mais adequado como base da
ferramenta a ser desenvolvida no TCC 2. Não haverá entrega de ferramenta nesta fase; o
produto entregável é a análise, a comparação experimental dos modelos e as conclusões
sobre o uso de features de código para KT.

A metodologia adotada é o **EDM Process de 4 fases** (Problem Definition → Data
Preparation → Modelling & Evaluation → Deployment), sendo que a fase de Deployment é
diferida para o TCC 2.

---

## Dataset: CSEDM / ProgSnap2 v6

**Localização:** `data/CSEDM/`

**Estrutura dos dados:**
- `MainTable.csv` — tabela de eventos (SubjectID, AssignmentID, ProblemID, EventType,
  Score, CodeStateID, Timestamps)
- `CodeStates/CodeStates.csv` — snapshots de código (CodeStateID → código Java)
- `LinkTables/Subject.csv` — alunos e notas finais (SubjectID → X-Grade normalizado 0–1)
- `early.csv` / `late.csv` — labels binárias derivadas (SubjectID, AssignmentID, ProblemID,
  Attempts, CorrectEventually, Label)

**Splits disponíveis:**
- `Release/Train/` e `Release/Test/` — splits oficiais (usar para comparação reproduzível
  com o paper Code-DKT)
- `Train/` e `Test/` — splits alternativos maiores
- `All/` — dataset completo
- `CodeWorkout/` — dataset adicional (potencial generalização)

**Estatísticas-chave (Code-DKT paper, Shi et al. 2022):**
- ~410 estudantes, 50 problemas, 5 assignments Java introdutório
- 23,68% de tentativas corretas (desbalanceado → AUC como métrica primária)
- Média de 6,1 tentativas por problema
- **Release/Train: 23,70% de corretos** (match com o paper → usar Release/ para replicação)

**EventTypes relevantes:**
- `Run.Program` com `Score` definido → submissão avaliada; label `correct = (Score == 1.0)`
- `Compile.Error` → 30,27% dos eventos; código não-compilável; `correct = 0` para Code-DKT
- Não existe `EventType = Submit` neste dataset

---

## Fase 1 — Problem Definition

1. **KCs (baseline):** `AssignmentID` como KC — cada assignment = conceitos ensinados
   naquela semana (5 KCs)
2. **KCs (gerados):** fine-grained, gerados via AST (srcML) + LLM — ver Fase 2d (03b)
3. **Task de KT:** dado histórico `(problema, acerto/erro)` até `t`, prever resultado de `t+1`
4. **Métricas:** AUC (primária), Precision/Recall, F1 (secundárias)
5. **Labels-alvo:** `early.csv` (predição antecipada) e `late.csv` (predição tardia)
6. **Pergunta adicional:** KCs gerados por AST+LLM melhoram a predição vs KC=Assignment?

---

## Fase 2 — Data Preparation

### 2a. EDA — `notebooks/01_eda.ipynb`
- [Em andamento — seções 1–2 completas]
- Seção 3: estrutura de assignments e problemas, taxa de acerto por problema
- Seção 4: padrões de interação, curvas de aprendizagem, distribuição de tentativas
- Seção 5: análise de Score e desequilíbrio (justificativa de AUC)
- Seção 6: evolução do código (tamanho, AST fingerprints, diversidade de soluções)
- Seção 7: análise temporal (heatmaps, procrastinação, intervalos entre tentativas)
- Seção 8: correlações exploratórias para modelagem

### 2b. Pré-processamento — `notebooks/02_preprocessing.ipynb`
- Filtrar `MainTable`: `EventType in {Run.Program, Compile.Error}` com `Score` definido
  (apenas `Run.Program` tem Score; `Compile.Error` → `correct = 0`)
- Para BKT e DKT: usar apenas `Run.Program`, label `correct = (Score == 1.0)`
- Construir sequências por `(SubjectID, AssignmentID)` — KC=Assignment
- Construir sequências por `(SubjectID, ProblemID)` com Q-matrix — KC=gerado (ver 2d)
- Truncar em 50 tentativas (últimas 50, conforme Shi et al., 2022)
- Join com `CodeStates` via `CodeStateID`
- Separar treino/teste usando `Release/Train` e `Release/Test`

### 2c. Features de Código — `notebooks/03_code_features.ipynb` / `src/code_features.py`
Extração de codepaths via **srcML** (substitui javalang — srcML parseia código
não-compilável, preservando estrutura parcial em XML).

- Parsear Java com `srcml` para gerar XML
- Extrair caminhos folha-a-folha da árvore srcML:
  `pr = (nó_início, caminho_textual, nó_fim)` — mesmo formato do code2vec
- Construir vocabulário de nós e caminhos a partir do treino
- Representar cada submissão como conjunto de `R` caminhos (embeddings dim=300)
- Inclui `Compile.Error`: srcML parseia código não-compilável → features parciais

> **Nota arquitetural:** nossa implementação do Code-DKT usa srcML em vez de javalang,
> equivalente ao srcML-DKT (Pankiewicz, Shi & Baker, EDM 2025). A arquitetura
> LSTM + atenção é idêntica ao Code-DKT original (Shi et al., 2022); apenas o extrator
> de árvore é trocado para suportar código não-compilável. srcML-DKT IS Code-DKT com
> suporte a unparsable code.

### 2d. Geração de KCs via AST + LLM — `notebooks/03b_kc_generation.ipynb`

Pipeline híbrido: srcML fornece sinal estrutural objetivo; LLM interpreta semanticamente.

**Motivação:** o CSEDM não possui enunciados textuais dos problemas — apenas códigos
dos alunos. O AST serve como substituto: se 80% das submissões corretas de um ProblemID
usam `ForStatement` + `ArrayAccess`, o problema requer iteração sobre arrays,
independente do enunciado textual.

Abordagem embasada em:
- Rivers et al. (ICER 2016): "AST node types (for, if) como KCs" — citado pelo Code-DKT paper
- KCGen-KT (Duan et al., 2025): pipeline LLM para KC generation em problemas de programação
  usando submissões corretas como sinal principal

**Etapas:**

1. **Coleta:** filtrar `Run.Program` com `Score == 1.0` por `ProblemID`

2. **AST signature (srcML):** para cada `ProblemID`:
   - Parsear submissões corretas com srcML
   - Calcular frequência de tipos de nó (`ForStatement`, `IfStatement`, `ArrayAccess`, etc.)
   - Identificar constructs em >50% das corretas (required) e 20–50% (optional)
   - Output: `results/ast_signatures.json`

3. **Stage 1 — Inferência do problema (LLM + AST):**
   - Prompt: 5 submissões corretas representativas + resumo AST
   - LLM infere em 1–2 frases o que o problema provavelmente pede
   - Output: `results/problem_descriptions.json`

4. **Stage 2 — Geração de KCs ancorados em AST (LLM):**
   - Prompt: descrição inferida + constructs AST + código bruto
   - Restrição no prompt: cada KC deve corresponder a ≥1 construct AST (anti-alucinação)
   - Gera 3–8 KCs por problema → ~300–500 KCs brutos totais
   - Output: KCs brutos com constructs associados

5. **Clustering (Sentence-BERT + HAC):**
   - Embeddings Sentence-BERT dos textos de KC
   - Hierarchical Agglomerative Clustering com cosine distance
   - Experimentar 20, 30, 50 clusters
   - Output: `results/kc_clusters.json`

6. **Rotulagem de clusters (LLM):**
   - Um rótulo por cluster → KC final com constructs AST associados
   - Output: `results/kc_descriptions.json`

7. **Q-matrix:** `ProblemID × KC_id` (binário) → `results/qmatrix.csv`

**Custo estimado:** ~150 calls Claude Sonnet ≈ $1–3 USD

---

## Fase 3 — Modelling & Evaluation

### 3a. BKT (baseline) — `notebooks/04_bkt.ipynb` / `src/models/bkt.py`
- Biblioteca **`pyBKT`**
- Parâmetros por KC: prior, learn, guess, slip (EM)
- Variante A: KC=Assignment (5 KCs)
- Variante B: KC=gerado (Q-matrix de 2d)
- Avaliação: AUC no split de teste

### 3b. DKT — `notebooks/05_dkt.ipynb` / `src/models/dkt.py`
- **PyTorch**, LSTM
- Input: one-hot `(ProblemID, correctness)` — dimensão `2 × n_problemas`
- LSTM → Linear → Sigmoid, Binary Cross-Entropy, Adam (lr=0.0005)
- 100 random samples para hyperparameter tuning, 10-fold cross-validation
- Variante A: KC=Assignment | Variante B: KC=gerado

### 3c. Code-DKT (com srcML) — `notebooks/06_code_dkt.ipynb` / `src/models/code_dkt.py`
- Estende DKT com embeddings de caminhos srcML (tamanho 300)
- Mecanismo de atenção: `α = SoftMax(E · Wa)`, vetor de código `z = W0(Σ αᵢ eᵢ)`
- Concatenar `z` com vetor de acerto/erro a cada passo LSTM
- Inclui `Compile.Error`: srcML parseia e fornece features parciais → `correct = 0`
- Variante A: KC=Assignment | Variante B: KC=gerado
- Referência: Code-DKT (Shi et al., EDM 2022); srcML-DKT (Pankiewicz et al., EDM 2025)

### 3d. Comparação — `notebooks/07_comparison.ipynb`
- **Tabela principal (3×2):** modelo × definição de KC, AUC por assignment

  | Modelo        | KC=Assignment | KC=LLM+AST |
  |---------------|---------------|------------|
  | BKT           |               |            |
  | DKT           |               |            |
  | Code-DKT (srcML) |            |            |

- Replicar Table 1 do Code-DKT paper (KC=Assignment, first-attempt predictions)
- Curvas de aprendizagem por KC gerado (power law of practice)
- Teste de significância Wilcoxon signed-rank (entre KC=Assignment e KC=LLM+AST)
- Análise qualitativa: 5–10 KCs gerados — são interpretáveis e consistentes com AST?

---

## Fase 4 — Justificação para TCC 2

| Modelo | Prós | Contras |
|---|---|---|
| BKT | Simples, interpretável, por KC | Menor AUC, sem sequências longas |
| DKT | Captura dependência temporal | Não usa código |
| Code-DKT (srcML) | Melhor AUC (+3–4%), usa código, inclui Compile.Error | Maior complexidade |

**Conclusão esperada:** Code-DKT (srcML) como modelo base para TCC 2; KCs gerados
como definição de KC se melhorarem AUC.

**Extensão natural para TCC 2:** KCGen-KT completo (Duan et al., 2025) — Llama 3 +
LoRA + LSTM + atenção sobre KCs gerados — candidato a modelo principal no TCC 2.

---

## Estrutura do Repositório

```
tcc.edm.kt/
├── PLAN_TCC1.md
├── .gitignore
├── data/               (gitignored)
│   └── CSEDM/
├── docs/
├── notebooks/
│   ├── 01_eda.ipynb              — EDA [em andamento]
│   ├── 02_preprocessing.ipynb   — pré-processamento
│   ├── 03_code_features.ipynb   — codepaths via srcML
│   ├── 03b_kc_generation.ipynb  — geração de KCs (AST + LLM) [novo]
│   ├── 04_bkt.ipynb             — BKT (KC=Assignment e KC=gerado)
│   ├── 05_dkt.ipynb             — DKT
│   ├── 06_code_dkt.ipynb        — Code-DKT (srcML)
│   └── 07_comparison.ipynb      — comparação 3×2
├── src/
│   ├── data_loader.py
│   ├── code_features.py         — extração srcML + KC signatures
│   ├── evaluation.py
│   └── models/
│       ├── bkt.py
│       ├── dkt.py
│       └── code_dkt.py          — LSTM + atenção sobre codepaths srcML
└── results/
    ├── comparison.csv
    ├── kc_descriptions.json     — KCs gerados com constructs AST
    ├── qmatrix.csv              — ProblemID × KC_id
    ├── ast_signatures.json      — assinatura estrutural por ProblemID
    └── problem_descriptions.json — enunciados inferidos por LLM
```

---

## Stack Técnica

- Python 3.10+, Jupyter Notebooks
- `pandas`, `numpy` — dados
- `srcml` (CLI, sistema) — AST Java; parseia compilável e não-compilável
- `torch` (PyTorch) — DKT, Code-DKT
- `pyBKT` — BKT
- `scikit-learn` — AUC, cross-validation
- `sentence-transformers` — embeddings Sentence-BERT para clustering de KCs
- `scipy` — HAC clustering (hierarchical agglomerative)
- `anthropic` — Claude API para geração de KCs
- `matplotlib`, `seaborn` — visualizações

---

## Critérios de Conclusão

1. EDA completa (seções 1–8) com visualizações do CSEDM
2. AUC do Code-DKT (srcML) ~74% para A1 com KC=Assignment (±2%, replicar Shi et al. 2022)
3. Tabela 3×2: BKT vs DKT vs Code-DKT × KC=Assignment vs KC=LLM+AST
4. Curvas de aprendizagem por KC gerado (power law of practice)
5. Teste Wilcoxon signed-rank entre KC=Assignment e KC=LLM+AST no melhor modelo
6. Inspeção qualitativa de 5–10 KCs: interpretáveis com constructs AST associados
7. Todos os notebooks executáveis do zero com seed fixo

---

## Referências dos Modelos

- **BKT:** Corbett & Anderson (1994); pyBKT (Badrinath et al., EDM 2021)
- **DKT:** Piech et al. (NeurIPS 2015)
- **Code-DKT:** Shi et al. (EDM 2022) — code2vec + atenção sobre AST paths
- **srcML-DKT:** Pankiewicz, Shi & Baker (EDM 2025) — Code-DKT com srcML para código não-compilável
- **KC generation:** Rivers et al. (ICER 2016) — AST node types como KCs;
  KCGen-KT (Duan et al., 2025) — LLM para geração automática de KCs em programação
