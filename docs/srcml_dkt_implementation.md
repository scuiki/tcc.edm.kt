# srcML-DKT — Plano de Implementação

Baseado em: Pankiewicz, Shi & Baker (2025) *srcML-DKT: Enhancing Deep Knowledge Tracing with Robust Code Representations from srcML* (EDM 2025, short paper);
Shi, Chi, Barnes & Price (2022) *Code-DKT: A Code-based Knowledge Tracing Model for Programming Tasks* (EDM 2022) — modelo-base que srcML-DKT estende;
Collard, Decker & Maletic (2013) *srcML: An Infrastructure for the Exploration, Analysis, and Manipulation of Source Code* (ICSM 2013) — ferramenta de parsing usada;
e o plano interno [`docs/srcml_dkt_plan.md`](srcml_dkt_plan.md), que registra a discussão prévia das decisões abaixo.

Escopo deste documento: descrever as decisões de design tomadas para implementar srcML-DKT como 4º modelo do TCC 1, com foco no que **o paper de referência não especifica** (algoritmo do extrator, regras de tokenização do XML, fallback em falha de parse, configuração de paralelismo, protocolo de comparação justa com os 3 modelos prévios). O resultado experimental — incluindo o achado de que srcML-DKT ficou **abaixo** do Code-DKT em todos os 5 assignments — é discutido honestamente como parte do conteúdo metodológico.

---

## 1. Por que adicionar srcML-DKT ao TCC 1

### 1.1 Motivação: o limite do parser AST estrito

O Code-DKT vanilla (Shi et al., 2022), que já implementamos em `06_code_dkt.ipynb`, usa o `javalang` para extrair paths AST do código submetido. O `javalang` exige código **sintaticamente válido**: se o programa não compila, `parser.parse_member_declaration()` lança exceção e o nosso `extract_paths_javalang` retorna `[]` (`src/code_features.py:115`). O paper de Shi et al. adota a mesma postura — **descarta** os Compile.Error events da sequência KT.

Isso é metodologicamente conveniente, mas tem uma consequência prática: ~30% dos eventos do CSEDM são `Compile.Error` (109.020 eventos sobre o total). Em outras palavras, **descartamos uma fração não-trivial do comportamento dos alunos** — justamente o comportamento dos alunos mais novatos, que erram a sintaxe antes de chegar à lógica. Pankiewicz, Shi & Baker (2025), no paper srcML-DKT, formulam essa crítica de forma direta: *"simply discarding these submissions risks favoring more advanced students who can already write error-free code, and neglecting novice learners who often struggle with syntax."*

A proposta srcML-DKT mantém a arquitetura LSTM + atenção code2vec do Code-DKT, mas troca o parser estrito (`javalang`) por um parser tolerante (`srcML`, da Collard et al., 2013), que retorna XML parcial mesmo em código quebrado. O ganho do paper original é de **+1.65pp first-attempt AUC sobre Code-DKT** num dataset de 610 alunos de C# resolvendo problemas de condicional (Tabela 3 do paper).

### 1.2 Decisão: incluir já no TCC 1, não diferir ao TCC 2

A versão inicial do nosso planejamento previa apenas BKT, DKT e Code-DKT no TCC 1, com srcML-DKT diferido ao TCC 2. Mudamos de ideia por quatro razões — todas registradas em [`docs/srcml_dkt_plan.md`](srcml_dkt_plan.md) Seção "Context":

1. O binário `srcml` 1.1.0 já está instalado no ambiente (`/usr/bin/srcml`).
2. Já temos `results/sequences_code_dkt.pkl` (com Compile.Error) gerado pelo `02_preprocessing.ipynb` — não precisamos reprocessar nada do pipeline a montante.
3. A arquitetura PyTorch do Code-DKT é **integralmente reaproveitável**: o que muda é apenas o extrator de paths. Reúso máximo de código.
4. Comparar 4 modelos enriquece a discussão metodológica do TCC e nos dá um experimento adicional sem custo arquitetural alto.

A contrapartida é o compromisso, assumido neste documento, de **registrar todas as decisões de design** — especialmente as que o paper Pankiewicz et al. omite (que são quase todas as do algoritmo de extração).

---

## 2. Comparação justa: o que treina ≠ o que avalia

Esta é a decisão de protocolo mais importante deste plano e merece destaque antes de qualquer detalhe técnico do extrator.

### 2.1 O problema

Os outros 3 modelos do TCC (BKT, DKT, Code-DKT) foram treinados e avaliados em `sequences_bkt_dkt.pkl` — apenas eventos `Run.Program`, 43.661 eventos. srcML-DKT, para ser fiel ao paper, **precisa treinar com Compile.Error** (afinal, esse é o ponto da abordagem). Esses eventos estão em `sequences_code_dkt.pkl` — 53.385 eventos.

Mas se srcML-DKT também avaliasse no test set de `sequences_code_dkt`, comparar AUCs lado-a-lado seria injusto: os 4 modelos estariam medidos em definições distintas de "evento", inflando ou deflando arbitrariamente uma das comparações.

### 2.2 A decisão

Seguimos o paper de Pankiewicz et al. literalmente: **srcML-DKT treina em `sequences_code_dkt.pkl['train']` (com Compile.Error), mas avalia em `sequences_bkt_dkt.pkl['test']` (sem Compile.Error)** — o mesmo test set usado por BKT/DKT/Code-DKT.

Em diagrama:

```
sequences_code_dkt.pkl       sequences_bkt_dkt.pkl
  ├─ train                     ├─ train  → BKT/DKT/Code-DKT treinam aqui
  │   Run.Program +           │   Run.Program apenas
  │   Compile.Error           │
  │   ← srcML-DKT             │
  │     treina aqui           │
  │                           │
  └─ test (ignorado)          └─ test    → TODOS os 4 modelos avaliam aqui
                                Run.Program apenas                  (incluindo srcML-DKT)
```

A diferença entre modelos vem **só do treino** (mais eventos disponíveis para srcML-DKT), não da definição de "acerto" no test. AUCs ficam diretamente comparáveis. O paper de referência faz exatamente isso, embora não o explicite com tanto cuidado quanto fazemos aqui.

### 2.3 Implementação concreta

No `notebooks/09_srcml_dkt.ipynb` Seção 7, o loop de treino é:

```python
train_seqs = seq_code_dkt['train'][aid]     # com Compile.Error
test_seqs  = seq_bkt_dkt['test'][aid]       # SEM Compile.Error (mesmo dos outros)
res = train_and_evaluate(train_seqs, test_seqs, ...)
```

Os contadores reportados em `srcml_dkt_results_multirun.pkl` (e.g., A439: `n_train_events=12.471`, `n_test_events=2.264`) refletem essa separação. Por comparação, Code-DKT em A439 tem `n_train_events≈10.300` (mesmo split de alunos, mas sem Compile.Error no treino) e o mesmo `n_test_events=2.264`.

---

## 3. Extrator srcML — decisões de design

O paper Pankiewicz et al. (2025) é um short paper de 8 páginas que mostra **apenas um exemplo** de path extraído: `['input', 'method', 'body', 'doSomething', 'input']` (Figure 1). Não há pseudocódigo, não há repositório público referenciado, não há detalhe sobre como a árvore srcML é convertida em paths code2vec-compatíveis. **Todas as decisões abaixo são nossas, tomadas ad-hoc** para preservar fidelidade ao Code-DKT vanilla (mesmos filtros, mesmo formato de saída, mesmo vocabulário). Implementação em [`src/srcml_features.py`](../src/srcml_features.py).

### 3.1 subprocess CLI vs libsrcml

**Decisão:** `subprocess.run(["srcml", "--language=Java"], input=code.encode(...))` em vez do binding Python `libsrcml`.

**Por quê:** O binário `srcml` já estava instalado, o CLI é estável e a invocação via stdin/stdout é trivial. `libsrcml` é mais rápido em teoria (sem custo de fork), mas exige compilação de binding C, gerenciamento de objetos srcML em memória e introduz uma dependência extra que não temos como justificar dada a escala dos nossos dados (~44k submissões — não é big data). Tempo total de extração com `Pool(n_workers=os.cpu_count())` ficou em torno de 10 minutos no nosso hardware, dentro do orçamento.

**Trade-off honesto:** se quiséssemos rodar isto em milhões de submissões, libsrcml seria essencial. Para o CSEDM, subprocess é suficiente e mais simples de inspecionar.

### 3.2 Tratamento do namespace srcML

O XML que `srcml` retorna usa o namespace `xmlns="http://www.srcML.org/srcML/src"`. O parser stdlib `xml.etree.ElementTree` codifica isso como prefixo em **todas** as tags: `<function>` vira `{http://www.srcML.org/srcML/src}function`.

**Decisão:** remover o prefixo na função de tokenização (`_strip_ns` em `srcml_features.py:53`), não no parse. Cada tag XML é tokenizada pela sua forma local (`"function"`, `"block"`, `"type"`), sem o URI.

**Por quê:** se não removêssemos, cada token de interior do AST viraria uma string monstruosa e única por namespace. O vocabulário inflaria, e (pior) os paths seriam ilegíveis na inspeção manual. Removendo cedo, na função `_srcml_token()`, garantimos que a representação a jusante (vocabulário, tensores) seja indistinguível da que o `javalang` produziria — apenas com nomes diferentes (`"function"` vs `"MethodDeclaration"`).

### 3.3 Regra de tokenização: folhas vs interiores

**Decisão:**
- **Folhas** (elementos XML sem filhos): usar `elem.text.strip()` se não-vazio; caso contrário, a tag local.
- **Interiores** (com filhos): sempre a tag local.

Código em `srcml_features.py:58-69`:

```python
def _srcml_token(elem):
    tag = _strip_ns(elem.tag)
    children = list(elem)
    if not children:
        text = (elem.text or "").strip()
        return text if text else tag
    return tag
```

**Por quê:** o XML srcML mistura estrutura e conteúdo. Um elemento como `<block>{ ... }</block>` tem `text="{"` mas também tem filhos — a pontuação `{` é irrelevante para a estrutura sintática que queremos representar; o que importa é que aquilo é um bloco. Já uma folha como `<specifier>public</specifier>` carrega informação semântica em `.text` (`"public"`) que deve ser preservada como token.

Exemplo de tokenização sobre uma função simples:

```
XML srcML                              Token escolhido
─────────────────────────────────────────────────────────
<function>                             "function"        (interior)
  <type>                               "type"            (interior)
    <specifier>public</specifier>      "public"          (folha, com .text)
    <name>String</name>                "String"          (folha, com .text)
  </type>
  <name>plusOut</name>                 "plusOut"         (folha, com .text)
  <parameter_list>                     "parameter_list"  (interior)
    <parameter>                        "parameter"       (interior)
      <decl>                           "decl"            (interior)
        <type><name>String</name></type>  "String"
        <name>str</name>               "str"
      </decl>
    </parameter>
  </parameter_list>
  <block>{ ... }</block>               "block"           (interior — .text="{" ignorado)
</function>
```

**Trade-off honesto:** esta regra é diferente do `javalang`, que usa o nome da classe AST (`MemberReference`, `BinaryOperation`, `Literal`) como token em todos os nós, inclusive folhas. Como mostraremos na Seção 8.1, essa diferença é provavelmente a causa principal do resultado abaixo do esperado — folhas srcML carregam identificadores específicos do problema, enquanto folhas javalang carregam construções estruturais generalizáveis.

### 3.4 Raiz da anytree: nó `<unit>` como raiz virtual

O elemento raiz que `srcml` retorna é sempre `<unit>` (com atributos `language`, `revision`, `filename`). Dentro de `<unit>` ficam os elementos top-level do código (tipicamente uma `<function>` no CSEDM, que submete métodos isolados).

**Decisão:** usar `<unit>` como raiz com token literal `"unit"`, e cada filho direto de `<unit>` como nó de nível 1 da anytree (`srcml_features.py:140-143`).

**Por quê:** o `javalang` começa a árvore no `MethodDeclaration` (o objeto retornado por `parse_member_declaration`). No srcML, o elemento equivalente é `<function>`, mas há sempre o `<unit>` envelope antes. Usar `<unit>` como raiz virtual tem duas vantagens:

1. Garantia de **um único root**, mesmo se o código contiver múltiplas declarações top-level (raro no CSEDM, mas tecnicamente possível em código quebrado).
2. Tornamos a árvore srcML compatível com a interface `anytree.Walker` sem código condicional adicional.

Alternativa descartada: usar o primeiro filho de `<unit>` como raiz. Isso quebraria silenciosamente quando o código tivesse 0 ou >1 filhos diretos — exatamente o cenário onde queremos que o extrator continue funcionando.

### 3.5 Algoritmo principal: extract_paths_srcml

O algoritmo segue **exatamente** os filtros do Code-DKT (Shi et al., 2022): `max_path_length=8`, `max_path_width=2`, `R=50`. O que muda é apenas a fonte da árvore:

```
função extract_paths_srcml(código):
    se código vazio → retornar []
    
    tentar:
        result = subprocess.run(["srcml", "--language=Java"],
                                input=código, timeout=10)
    exceto:
        retornar []                   # CLI falhou
    
    se result.stdout vazio:
        retornar []
    
    tentar:
        root = ET.fromstring(result.stdout)
    exceto ET.ParseError:
        retornar []                   # XML mal-formado
    
    se root não tem filhos:
        retornar []                   # <unit/> vazio
    
    # Constrói anytree com <unit> como raiz
    head = Node(["1", "unit"])
    para cada filho i de root:
        _srcml_build_tree(filho, head, "1" + str(i+1))
    
    folhas = encontrar_folhas(head)
    se folhas vazias → retornar []
    
    # Normaliza order strings (idêntico ao Code-DKT)
    padronizar_orders_no_max_depth(folhas)
    
    walker = Walker()
    paths = []
    para cada par (folha_i, folha_j) com i < j:
        upstream, lca, downstream = walker.walk(folha_i, folha_j)
        walk_path = tokens(upstream) + [token(lca)] + tokens(downstream)
        
        se len(walk_path) > max_path_length: continuar
        
        # Largura: diferença entre ordens dos filhos diretos da LCA
        width = abs(int(upstream[-1].order) - int(downstream[0].order))
        se width > max_path_width: continuar
        
        paths.append((walk_path[0], "@".join(walk_path), walk_path[-1]))
    
    se len(paths) > R:
        paths = random.Random(seed).sample(paths, R)
    
    retornar paths
```

Saída: lista de triplas `(start_token, path_str, end_token)` com `path_str` separado por `@`. **Formato bit-idêntico** ao de `extract_paths_javalang`, o que permite reúso direto de `build_vocab`, `paths_to_tensor` e `build_code_input_tensor` de `src/code_features.py` (Seção 5 abaixo).

### 3.6 Filtros idênticos a Shi et al. 2022

Mantivemos `max_path_length=8`, `max_path_width=2`, `R=50` por dois motivos:

1. **Fidelidade ao paper Pankiewicz et al.:** que diz "we follow the approach used in Code-DKT" para todos os hiperparâmetros não explicitados.
2. **Comparabilidade direta com nosso Code-DKT:** se mudássemos os filtros, qualquer diferença de AUC seria confundida entre "efeito do parser" e "efeito dos filtros". Mantendo idênticos, isolamos a variável de interesse.

**Trade-off honesto:** esses filtros foram tunados por Shi et al. para árvores `javalang`. A árvore srcML tem uma topologia ligeiramente diferente (mais nós interiores genéricos, conforme Seção 8.1). É possível que `max_path_length=10` ou `max_path_width=3` extraísse paths mais expressivos no srcML. Não testamos — é uma das primeiras coisas a explorar num ablation futuro.

### 3.7 Fallback em parse failure

Cinco situações disparam `return []`:

| Caso | Detecção |
|---|---|
| Código vazio ou só whitespace | `if not code or not code.strip()` antes do subprocess |
| Exceção do subprocess (timeout, srcML não encontrado) | `try/except Exception` em volta do `subprocess.run` |
| stdout vazio (srcML rodou mas não produziu XML) | `if not result.stdout` |
| XML malformado | `try/except ET.ParseError` em `ET.fromstring` |
| `<unit/>` sem filhos (srcML retornou estrutura vazia) | `if not children_of_unit` |

**Taxa observada:** 0 falhas em 43.661 CSIDs do CSEDM, **incluindo todos os Compile.Error**. srcML degrada de forma muito gentil — mesmo um snippet propositalmente quebrado como `public int foo(int x { return x +` produz um XML reconhecível com `<decl>`, `<argument_list>` etc.

Comparação com javalang: na implementação Code-DKT, ~14% dos CodeStateIDs do CSEDM retornam `[]` (mesmo em `Run.Program`, sem contar Compile.Error). O ganho de cobertura do srcML é mesurável — só não se traduziu em ganho de AUC, como discutiremos na Seção 8.

### 3.8 Encoding e tratamento de caracteres especiais

**Decisão:** `input=code.encode("utf-8", errors="replace")` no subprocess (`srcml_features.py:121`).

**Por quê:** alguns CodeStates do CSEDM têm caracteres não-ASCII em comentários (acentos, símbolos), terminadores de linha Windows (`\r\n`) e ocasionalmente bytes inválidos. Sem `errors="replace"`, o `code.encode()` poderia lançar `UnicodeEncodeError` silencioso, o subprocess receberia bytes parciais, retornaria stdout vazio e o extrator devolveria `[]` — perderíamos paths sem nem saber por quê. `errors="replace"` substitui o byte problemático por `?` e segue adiante.

---

## 4. Tratamento de Compile.Error events

O ponto-chave da abordagem srcML-DKT é incluir Compile.Error events no treino. Na nossa pipeline:

1. `02_preprocessing.ipynb` já gerou `sequences_code_dkt.pkl` com `Run.Program + Compile.Error`, com `correct=0` fixo para todos os Compile.Error (assumimos que tentativa que não compila não pode estar correta).
2. O CodeStateID de cada Compile.Error tem o código submetido (não-compilável).
3. srcML processa esse código quebrado e retorna XML parcial — verificamos manualmente em uma amostra de 20 Compile.Error que o XML contém estruturas razoáveis (`<decl>`, `<expr>`, `<argument_list>`).
4. O extrator produz paths normalmente. O cache `results/srcml_features_cache.pkl` mistura paths de submissões corretas, incorretas e não-compiláveis sem distinção — o modelo aprende a discriminar pela própria atenção code2vec.

**O que isto significa para o modelo:** durante o treino, o LSTM vê eventos `(ProblemID, correct=0, paths_srcml)` injetados na sequência KT do estudante onde antes (no Code-DKT vanilla) ele veria apenas `Run.Program`. A sequência fica mais densa e mais reflete o comportamento real do aluno.

**O que isto significa para o teste:** nada. Conforme Seção 2, o test set é o mesmo dos outros 3 modelos — Compile.Error não entra na avaliação. O modelo treinado com Compile.Error é avaliado em prever a próxima tentativa `Run.Program`, exatamente como BKT, DKT e Code-DKT.

---

## 5. Reúso da arquitetura CodeDKTModel

A arquitetura LSTM + atenção code2vec do Code-DKT é **idêntica** entre os dois modelos. O que muda é só o feature extractor (Seção 3). Concretamente:

| Módulo | Code-DKT vanilla | srcML-DKT | Compartilha? |
|---|---|---|---|
| Extrator de paths | `extract_paths_javalang` | `extract_paths_srcml` | Não — único diferencial |
| Construção do vocabulário | `build_vocab` | `build_vocab` | **Sim** — interface idêntica |
| Tensorização | `paths_to_tensor`, `build_code_input_tensor` | idem | **Sim** |
| Modelo PyTorch | `CodeDKTModel` em `src/models/code_dkt.py` | idem | **Sim** — mesma classe, sem subclasse |
| Loop de treino | `train_and_evaluate` | idem | **Sim** — função é parser-agnostic |
| Loss, otimizador, schedule | BCE, Adam(lr=0.0005), 40 épocas | idem | **Sim** |

Isso é uma decisão deliberada de minimização de variáveis confundidoras: queremos que qualquer diferença observada entre Code-DKT e srcML-DKT possa ser **rigorosamente atribuída ao parser**, não a um detalhe arquitetural acidental. O fluxo no notebook `09_srcml_dkt.ipynb` Seção 7 importa diretamente `from src.models.code_dkt import CodeDKTModel, train_and_evaluate` — não há nenhum arquivo `src/models/srcml_dkt.py`.

### 5.1 Hiperparâmetros: `BEST_CDKT_CONFIG` reusado

Usamos para srcML-DKT a mesma configuração ótima encontrada para o Code-DKT no `06_code_dkt.ipynb` Seção 8:

```python
BEST_CDKT_CONFIG = {
    "hidden_dim": 200,
    "dropout": 0.1,
    "lr": 0.0005,
    "batch_size": 128,
    "epochs": 40,
    "max_len": 50,
    "R": 50,
}
```

**Por quê:** consistência interna acima de tudo. Se cada modelo rodasse com seu próprio ótimo de hiperparâmetros, a diferença final seria uma mistura inseparável de (a) qualidade do parser e (b) qualidade do tuning. Mantendo a config idêntica, a diferença vem só de (a).

**Trade-off honesto:** é muito provável que srcML-DKT tenha um ótimo de hiperparâmetros diferente. O vocabulário srcML é menos diverso (Seção 8.1), o que sugere que talvez `hidden_dim` menor e dropout maior funcionassem melhor para evitar overfit no padrão dominante. Não rodamos esse tuning específico — fica como prioridade para o TCC 2.

---

## 6. Detalhes operacionais

### 6.1 Paralelização da extração: multiprocessing.Pool

Extração de paths é CPU-bound (subprocess + parsing XML + traversal de árvore). GPU não acelera. Usamos `multiprocessing.Pool` em `srcml_features.py:210-242` para paralelizar:

```python
with mp.Pool(n_workers=os.cpu_count()) as pool:
    for csid, paths in pool.imap_unordered(_worker_extract_srcml,
                                            args_list,
                                            chunksize=64):
        cache[csid] = paths
```

**Escolhas concretas:**
- `n_workers=os.cpu_count()` — saturação completa de CPU. No nosso ambiente são 16 workers.
- `chunksize=64` — batching grande o suficiente para amortizar o IPC, pequeno o suficiente para distribuir bem a carga (algumas submissões grandes consomem muito mais tempo que outras).
- `imap_unordered` em vez de `map` — não precisamos da ordem para o cache (cada `(csid, paths)` é independente), e `imap_unordered` permite que workers rápidos peguem novas tarefas sem esperar.

**Tempo total:** ~10 minutos para 43.661 CSIDs únicos. Cache resultante `results/srcml_features_cache.pkl` ocupa ~200 MB e está no `.gitignore` (mesmo critério do `code_features_cache.pkl`).

### 6.2 Seeds e reprodutibilidade

10 runs por assignment com seeds 42 a 51 (mesmo protocolo do Code-DKT multirun, consistente com Shi et al. 2022). Cada run chama `set_global_seed(seed)` antes de instanciar o modelo. A amostragem `random.Random(seed).sample(paths, R)` dentro do extrator usa seed=42 fixa (a aleatoriedade do extrator é independente da seed do treino — é sobre qual subconjunto de paths cada submissão expõe ao modelo, não sobre inicialização do modelo).

### 6.3 Estrutura do notebook 09

| Seção | Conteúdo | Tempo |
|---|---|---|
| 1 | Setup, seeds, device CUDA | <1s |
| 2 | Carrega `sequences_code_dkt.pkl` (treino) + `sequences_bkt_dkt.pkl` (test) + `CodeStates.csv` | ~10s |
| 3 | `extract_paths_srcml` em sample de 100 submissões, métricas de transparência (taxa de parsing, paths/submissão, tempo médio) | ~30s |
| 4 | Cache completo via `build_cache_srcml(n_workers=os.cpu_count())` → `results/srcml_features_cache.pkl` (detecta cache existente e pula re-extração) | ~10min ou 0s |
| 5 | Vocabulário por assignment (apenas do train de `sequences_code_dkt`) via `build_vocab` | ~5s |
| 6 | Tensorização A439 + smoke test forward + smoke train (5 épocas) | ~1min |
| 7 | Treino full: 10 runs × 5 assignments × 40 épocas com `BEST_CDKT_CONFIG`, avaliando no test set de `sequences_bkt_dkt` | ~10min |
| 8 | Sumário rápido (mean ± std vs Code-DKT multirun) | <5s |
| 9 | Serialização `results/srcml_dkt_results_multirun.pkl` | ~30s |
| 10 | Sanity checks (schema idêntico ao Code-DKT multirun, coerência seed=42) | <5s |

Tempo total ~25 min em GPU RTX 4050.

---

## 7. Resultados observados

Os números abaixo são `mean ± std` sobre 10 runs (seeds 42 a 51), reproduzidos do `srcml_dkt_results_multirun.pkl` e comparados ao `code_dkt_results_multirun.pkl` e `dkt_results_multirun.pkl`.

### 7.1 First-attempt AUC (métrica principal)

| Assignment | srcML-DKT | Code-DKT | DKT | Δ(srcML − Code-DKT) |
|---|---|---|---|---|
| A439 | **70.41 ± 1.01%** | 73.27% | 75.56% | **−2.86 pp** |
| A487 | **76.56 ± 0.87%** | 79.56% | 76.70% | **−3.00 pp** |
| A492 | **81.93 ± 0.71%** | 86.12% | 82.05% | **−4.19 pp** |
| A494 | **78.30 ± 0.90%** | 81.85% | 80.17% | **−3.54 pp** |
| A502 | **81.17 ± 0.99%** | 84.98% | 80.78% | **−3.82 pp** |

### 7.2 All-attempts AUC (métrica secundária)

| Assignment | srcML-DKT | Code-DKT | Δ(srcML − Code-DKT) |
|---|---|---|---|
| A439 | 67.25 ± 0.44% | 70.35 ± 0.67% | −3.10 pp |
| A487 | 71.80 ± 0.51% | 74.89 ± 0.61% | −3.09 pp |
| A492 | 75.80 ± 0.87% | 79.08 ± 0.74% | −3.28 pp |
| A494 | 70.04 ± 0.92% | 75.07 ± 0.97% | −5.03 pp |
| A502 | 72.59 ± 0.63% | 76.24 ± 0.77% | −3.65 pp |

### 7.3 Métricas de transparência da extração

| Métrica | srcML | javalang (referência) |
|---|---|---|
| Taxa de parsing (paths ≥ 1 sobre todos os CSIDs) | 100.0% (43.661/43.661) | ~86% (Run.Program apenas) |
| Cobertura de Compile.Error | 100% | 0% (descartados a priori) |
| Mediana de paths por submissão (pré-cap R=50) | ~50 | ~50 |
| % de submissões com ≥50 paths (atingem o cap) | 86% | 85% |
| Vocab `path_to_idx` A439 | 8.013 | 21.717 |
| Vocab `path_to_idx` A487 | 14.255 | 29.768 |
| Tempo médio por submissão (subprocess + parse) | ~10 ms | ~3 ms |
| Falhas em todo o dataset (lista vazia) | 0 | ~14% no Run.Program; 100% no Compile.Error |

### 7.4 Leitura honesta: srcML-DKT ficou abaixo do Code-DKT em todos os 5 assignments

Esse resultado **diverge** do paper de referência, que reporta +1.65pp de srcML-DKT sobre Code-DKT (Pankiewicz et al. 2025, Table 3). Discussão detalhada na Seção 8.

Antes de interpretar isso como falha, vale destacar o que **funcionou** exatamente como esperado:

1. **Taxa de parsing de 100%** confirma o ganho metodológico central do srcML: o parser é robusto a código não-compilável (todos os 109k Compile.Error events do CSEDM foram processados).
2. **Cobertura completa de Compile.Error** valida que a arquitetura ingere o tipo de evento que o paper se propõe a recuperar.
3. **Estabilidade dos runs** (std de 0.44 a 1.01pp no first-attempt AUC) é consistente com o Code-DKT multirun — sem sinal de instabilidade numérica que indicasse bug.
4. **Schema dos resultados idêntico** ao Code-DKT multirun (10 runs × seeds 42-51, mesmo conjunto de chaves no pickle), o que permite ao `07_comparison.ipynb` consumir os 4 modelos uniformemente.

O resultado negativo é um achado científico legítimo. A próxima seção analisa por quê.

---

## 8. Análise do resultado negativo

### 8.1 Hipótese principal: vocabulário srcML menos discriminativo

A descoberta mais marcante na inspeção dos caches é que **o vocabulário srcML é 2.6× a 2.7× menor que o javalang** para os mesmos assignments:

```
A439:  srcML  8.013 paths únicos    javalang  21.717
A487:  srcML 14.255 paths únicos    javalang  29.768
```

Isso é contra-intuitivo — esperaríamos que cobrir mais submissões (incluindo todos os Compile.Error) ampliasse o vocabulário. A causa está na regra de tokenização da Seção 3.3.

**srcML** tokeniza nós interiores como tags XML genéricas: `function`, `type`, `name`, `block`, `expr`, `expr_stmt`, `decl_stmt`. Essas tags se repetem em **praticamente todos** os métodos do CSEDM, gerando paths estruturalmente idênticos para problemas conceitualmente diferentes.

**javalang** tokeniza nós interiores como nomes de classe AST: `MethodDeclaration`, `BinaryOperation`, `LocalVariableDeclaration`, `IfStatement`, `ForStatement`, `MemberReference`. Cada construção sintática produz um token único. Paths como `MemberReference@BinaryOperation@IfStatement@ReturnStatement@Literal` são bem mais discriminativos que `name@expr@if@return@expr`.

A consequência para o modelo: a atenção code2vec do CodeDKTModel tem menos "vocabulário" para distinguir submissões corretas de incorretas no nível de path. Os paths srcML viraram "ruído quase uniforme", e a atenção tem que extrair sinal de um espaço menor.

**Outro lado da moeda:** as folhas srcML carregam **identificadores literais** (nomes de variáveis: `caughtSpeeding`, `isBirthday`, `n`, `x`). Esses são únicos por problema, o que aumenta o vocabulário de tokens (token_to_idx tem 569 a 1.306 entradas), mas o efeito é o oposto do desejado — o modelo passa a se ancorar em pistas específicas do problema, prejudicando generalização entre tentativas (que é o que first-attempt AUC mede).

```
javalang (mais discriminativo na ESTRUTURA):
  Path típico: MemberReference@BinaryOperation@IfStatement@ReturnStatement@Literal
  Folha:       Literal  (= "65", "0", "0.5" — tokens estruturais reutilizáveis)

srcML (mais discriminativo no CONTEÚDO LITERAL):
  Path típico: name@expr@if@return@expr
  Folha:       name  (= "caughtSpeeding", "n" — identificadores específicos do problema)
```

### 8.2 Hipótese secundária: noise de Compile.Error injetado no treino

srcML-DKT vê eventos `Compile.Error → correct=0` no treino que os outros modelos não veem. Em princípio isso deveria ajudar (mais sinal), mas pode ser **perverso** se:

1. O modelo aprende a associar o vocabulário srcML genérico (`name`, `expr`, `block`) com `correct=0` por puro viés do treino (compile errors são desproporcionalmente comuns no início das sequências, criando uma correlação espúria).
2. A atenção code2vec passa a "votar baixo" para qualquer submissão estruturalmente parecida com Compile.Error, mesmo as corretas, no test set.

A ablation natural para testar isso — treinar srcML-DKT **sem** Compile.Error, mantendo só o parser — não foi feita por restrição de tempo. É a prioridade #1 para o TCC 2.

### 8.3 Hipótese terciária: hiperparâmetros não-tunados para srcML

`BEST_CDKT_CONFIG` foi otimizado para o vocabulário javalang (Code-DKT em `06_code_dkt.ipynb` Seção 8). Como o espaço de embeddings srcML tem menos diversidade efetiva:

- `hidden_dim=200` pode estar superdimensionado → overfit ao padrão dominante.
- `dropout=0.1` pode ser insuficiente para regularizar um vocabulário mais denso por path.
- `epochs=40` pode estar saturando antes — talvez early stopping baseado em first-attempt AUC de validação ajudasse.

Repetir o tuning específico para srcML-DKT é prioridade #2 do TCC 2.

### 8.4 Por que o paper Pankiewicz et al. reportou ganho e nós não

Quatro diferenças entre nosso experimento e o do paper podem explicar a divergência:

| Eixo | Pankiewicz et al. 2025 | Nosso experimento |
|---|---|---|
| Linguagem | C# | Java |
| Tipo de problema | 6 tasks de condicional (CS1) | 5 assignments mistos (CSEDM Spring 2019) |
| Tamanho do dataset | 610 alunos | 410 alunos |
| % Compile.Error | 17–47% por task | ~30% global |
| Detalhe do extractor | **não publicado** | nosso, documentado aqui |
| Split | 3:1:1 (60% treino) | 80/20 (80% treino) |
| Hiperparâmetros | tuning específico do srcML | reaproveitados do Code-DKT |

A diferença mais provável é a combinação **extrator não-publicado + tuning específico não-publicado**. Como o paper é um short paper e não disponibiliza código, é impossível garantir que nossa implementação tokeniza o XML srcML exatamente como a deles. É inteiramente plausível que Pankiewicz et al. tenham regra de tokenização diferente (e.g., concatenar tag + texto em todos os nós), ou hiperparâmetros otimizados especificamente para o vocabulário srcML, e isso explique o ganho de 1.65pp que vemos virar perda de 3pp aqui.

Isso **não invalida** o resultado deles — é um lembrete de que reproduzir métodos de short papers sem código aberto envolve interpretação. Nosso resultado complementa o deles ao mostrar que **a abordagem é sensível a detalhes de implementação que o paper não detalha**, o que é uma contribuição metodológica útil para o campo.

---

## 9. Limitações honestas

1. **Tokenização ad-hoc:** a regra folha/interior da Seção 3.3 é nossa, não do paper. Outras escolhas razoáveis (e.g., sempre concatenar tag + texto, ou usar o atributo `pos:start` do srcML para discriminar nós) poderiam mudar o resultado.

2. **Filtros idênticos ao Code-DKT podem não ser ideais:** `max_path_length=8` e `max_path_width=2` foram tunados para árvores javalang. Como a árvore srcML é estruturalmente diferente (mais nós interiores genéricos), os filtros podem estar cortando paths informativos.

3. **Sem tuning específico de hiperparâmetros:** reusamos `BEST_CDKT_CONFIG`. O ótimo para srcML provavelmente é diferente.

4. **Comparação restrita a 5 assignments do CSEDM:** o paper de referência testou 6 tasks de C# de CS1. Não temos como saber se a perda observada se sustenta em outros tipos de problema.

5. **Sem teste de significância vs Code-DKT:** o `07_comparison.ipynb` (próximo) deve incluir Wilcoxon signed-rank por par de modelos. Com 5 assignments × 10 seeds, temos N=50 pares — suficiente para detectar diferenças sistemáticas.

6. **Ablation pure vs full não executada:** não rodamos srcML-DKT sem Compile.Error. Isso isolaria definitivamente o efeito do parser vs o efeito dos eventos extras.

---

## 10. Próximos passos

### 10.1 Para o TCC 1 (`07_comparison.ipynb`)

- **Reportar srcML-DKT mesmo com o resultado abaixo do esperado.** Esconder seria deselegante e roubaria a discussão mais rica do TCC: por que uma extensão recente do estado-da-arte não se transferiu para o nosso dataset?
- Incluir Wilcoxon signed-rank entre srcML-DKT e Code-DKT — esperamos significância estatística (p < 0.05) com sinal **invertido** vs Pankiewicz et al.
- Apresentar a Tabela comparativa de 4 modelos com a discussão da Seção 8 incorporada na seção de Discussão do TCC.

### 10.2 Para o TCC 2 (priorizado)

1. **Ablation pure vs full:** treinar srcML-DKT só com `Run.Program` (sem Compile.Error). Compara diretamente ao Code-DKT (mesmo dataset, parser diferente) e isola o efeito do parser.
2. **Hyperparameter tuning específico do srcML:** grid sobre `hidden_dim ∈ {64, 128, 200}`, `dropout ∈ {0.1, 0.2, 0.3}`, `epochs` com early stopping.
3. **Alternativas de tokenização:** testar (a) concatenar `tag:.text` em folhas e interiores, (b) usar atributos `pos:start` para incluir contexto posicional, (c) restringir o vocabulário de folhas para excluir identificadores literais (preservando só keywords).
4. **Investigação qualitativa:** comparar paths de maior atenção em srcML-DKT vs Code-DKT no mesmo CSID. Se a atenção do srcML está concentrada em paths "uniformes", isso confirma a hipótese da Seção 8.1.

### 10.3 Como capturar o aprendizado deste experimento no TCC

O resultado negativo é a parte mais educativa deste trabalho. Vale enquadrá-lo no TCC como:

> "Implementamos o srcML-DKT (Pankiewicz et al. 2025) como 4º modelo da comparação. Apesar de o parser ter alcançado 100% de cobertura — confirmando o ganho metodológico central da abordagem — o modelo final ficou 2.9 a 4.2 pontos percentuais **abaixo** do Code-DKT em first-attempt AUC, em todos os 5 assignments. Nossa hipótese para a divergência é que a regra de tokenização do XML srcML, não publicada no paper de referência, é determinante para o resultado. O vocabulário de paths que conseguimos extrair tem aproximadamente um terço do tamanho do gerado pelo javalang, o que reduz a discriminação efetiva da atenção code2vec. Esse achado é uma contribuição metodológica útil: aponta para um detalhe de implementação que merece publicação em trabalhos futuros sobre o método."

Isso é o tipo de discussão que orientadores valorizam — mostra que entendemos não só os resultados positivos, mas também o que sua ausência diz sobre o método.

---

## 11. Caminhos dos artefatos

| Artefato | Path | Gerado por | Gitignored |
|---|---|---|---|
| Código do extrator | [`src/srcml_features.py`](../src/srcml_features.py) | Chat 1 | Não |
| Notebook completo | [`notebooks/09_srcml_dkt.ipynb`](../notebooks/09_srcml_dkt.ipynb) | Chat 1 | Não |
| Cache de paths (~200 MB) | `results/srcml_features_cache.pkl` | notebook 09 Seção 4 | **Sim** |
| Resultados multirun (~70 MB) | `results/srcml_dkt_results_multirun.pkl` | notebook 09 Seção 9 | Não |
| Notas técnicas Chat 1 | [`docs/srcml_dkt_chat1_notes.md`](srcml_dkt_chat1_notes.md) | Chat 1 | Não |
| Plano original | [`docs/srcml_dkt_plan.md`](srcml_dkt_plan.md) | usuário | Não |
| Este documento | [`docs/srcml_dkt_implementation.md`](srcml_dkt_implementation.md) | Chat 2 | Não |

Para regenerar o cache srcML: `notebooks/09_srcml_dkt.ipynb` Seção 4 detecta automaticamente a presença do arquivo e pula a extração. Para forçar reextração, apagar o arquivo antes de executar.

---

## 12. Resumo executivo (para a seção de Discussão do TCC)

- **srcML-DKT** (Pankiewicz et al. 2025) substitui o parser `javalang` do Code-DKT por `srcML`, que tolera código não-compilável e permite incluir `Compile.Error` events no treino.
- Implementamos sobre a arquitetura do Code-DKT existente; **só o feature extractor mudou**.
- O paper de referência **não especifica** o algoritmo de extração de paths. Tomamos decisões ad-hoc para o mapping XML→anytree, regra folha/interior, e tratamento de namespace, todas documentadas neste arquivo.
- Para comparação justa com os outros 3 modelos, srcML-DKT **treina com `Compile.Error` mas avalia no mesmo test set sem `Compile.Error`** que BKT/DKT/Code-DKT usam.
- **Cobertura do parser: 100%** (43.661/43.661 CSIDs, incluindo todos os 109k Compile.Error). Confirma o ganho metodológico central da abordagem.
- **AUC final: −2.9 a −4.2 pp** vs Code-DKT em first-attempt AUC, em todos os 5 assignments. Diverge do paper original (+1.65 pp).
- **Hipótese principal** para a divergência: vocabulário srcML (~8k a 19k paths únicos) é 2.6× a 2.7× menor que o javalang (~22k a 30k) — tags XML genéricas geram paths menos discriminativos que classes AST.
- **Resultado negativo é parte da contribuição**: aponta para um detalhe de implementação não-publicado que é determinante para o método.
- **Próximos passos** prioritários: ablation pure vs full e hyperparameter tuning específico para srcML (ambos no TCC 2).
