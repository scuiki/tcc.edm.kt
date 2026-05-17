# srcML-DKT Chat 1 — Notas de Implementação para o Chat 2

> **Gerado em:** 2026-05-17 (Sonnet 4.6)
> **Consumidor:** Chat 2 (Opus 4.7) para escrever `docs/srcml_dkt_implementation.md`

---

## Decisões de implementação surgidas durante o desenvolvimento

### 1. Tratamento de namespace srcML no XML

**Decisão:** Strip do prefixo `{http://www.srcML.org/srcML/src}` diretamente no momento de tokenização, em `_srcml_token()`.

**Como implementado:**
```python
_NS_PREFIX = "{http://www.srcML.org/srcML/src}"

def _srcml_token(elem):
    tag = _strip_ns(elem.tag)   # ex: "{...}function" → "function"
    children = list(elem)
    if not children:
        text = (elem.text or "").strip()
        return text if text else tag
    return tag
```

**Por quê:** `xml.etree.ElementTree` inclui o URI do namespace em todas as tags (ex: `{http://...}function`). Se não for removido, os tokens de interior ficam ilegíveis e únicos por namespace. Optou-se por strip na função de tokenização em vez de no parse — mais limpo e localizado.

---

### 2. Regra de tokenização: folhas vs interiores

**Decisão:**
- **Folhas** (sem filhos XML): usar `.text.strip()` se não-vazio, senão tag local
- **Interiores** (com filhos): usar tag local

**Exemplo concreto do XML srcML:**
```xml
<function>          → interior → token = "function"
  <type>            → interior → token = "type"
    <specifier>     → folha, text="public"   → token = "public"
    <name>          → folha, text="String"   → token = "String"
  <name>            → folha, text="plusOut"  → token = "plusOut"
  <block>           → interior (text="{", mas tem filhos) → token = "block"
```

**Por quê:** Nós interiores como `<block>` têm texto de pontuação (`{`) que não carrega semântica AST. Usar o tag captura a estrutura sintática sem ruído de pontuação. Folhas sem texto (ex: `<parameter_list>` vazio) também caem para tag — situação rara mas coberta.

---

### 3. Raiz da anytree: nó `<unit>` como raiz virtual

**Decisão:** Usar o elemento `<unit>` (raiz do XML srcML) como raiz da anytree com token "unit" e seus filhos diretos como nível 1.

**Como implementado:**
```python
children_of_unit = list(root_elem)   # ex: [<function>]
head = Node(["1", "unit"], order="1")
for i, child_elem in enumerate(children_of_unit):
    _srcml_build_tree(child_elem, head, "1" + str(i + 1))
```

**Por quê:** Javalang inicia o tree no nó da declaração do método (ex: `MethodDeclaration`). srcML tem sempre um elemento `<unit>` envelope. Usar `<unit>` como raiz garante que haja sempre um único root e que múltiplos elementos de top-level sejam suportados (raro no CSEDM, mas possível).

**Alternativa descartada:** usar o primeiro filho de `<unit>` como raiz — quebraria quando o código tivesse múltiplas declarações ou estivesse muito mal-formado.

---

### 4. Estrutura do subprocess e tratamento de falhas

**Decisão:** `subprocess.run` com `input=code.encode('utf-8', errors='replace')`, `capture_output=True`, `timeout=10`.

**Por quê do `errors='replace'`:** Alguns CodeStates do CSEDM têm caracteres especiais (ex: `\r\n` do Windows, chars não-ASCII em comentários). `errors='replace'` evita `UnicodeEncodeError` silencioso que poderia retornar XML vazio.

**Casos de fallback para `[]`:**
- Código vazio ou só whitespace (verificado antes do subprocess)
- `subprocess.run` lança exceção (timeout, arquivo não encontrado)
- `result.stdout` vazio (srcML retornou exit code != 0 sem output)
- `ET.fromstring` falha em XML malformado
- `children_of_unit` vazio (código tão quebrado que srcML produziu apenas `<unit/>`)

**Taxa observada:** 0 falhas em 43,661 CSIDs — srcML degrada graciosamente mesmo em código muito quebrado.

---

### 5. srcML com código não-compilável (Compile.Error events)

**Observação:** srcML processa código com sintaxe quebrada e retorna XML parcial válido. Teste com `public int foo(int x { return x +` retornou XML com `<decl>`, `<argument_list>` etc. — estrutura reconhecível, sem erro.

**Impacto:** Compile.Error events entram no cache e na sequência de treino com `correct=0` (fixo, pelo preprocessing) e paths srcML extraídos normalmente. O modelo vê esses eventos como "tentativa incorreta com features de código".

**Diferença do paper:** Pankiewicz et al. (2025) mencionam que srcML "handles incomplete code" — confirmado em 100% dos CSIDs do CSEDM, incluindo Compile.Error.

---

## Surpresas e observações na extração

### Vocabulário srcML menor que javalang (achado crítico)

**Observação:** Apesar de cobrir mais CSIDs, o vocabulário srcML tem **menos paths únicos** que javalang:

| Assignment | srcML paths únicos | javalang paths únicos |
|---|---|---|
| A439 | 8,013 | 21,717 |
| A487 | 14,255 | 29,768 |

**Causa:** Os tokens interiores do srcML são tags XML genéricas (`function`, `type`, `block`, `name`) que se repetem em praticamente todos os métodos. Javalang usa nomes de classe AST (`MethodDeclaration`, `BinaryOperation`, `LocalVariableDeclaration`) que são mais específicos e geram paths mais diversificados.

**Tokens srcML** incluem identificadores reais do código (nomes de variáveis, funções) como folhas — ex: `caughtSpeeding`, `isBirthday`. Isso torna os paths sensíveis à semântica do problema específico, não da estrutura de controle.

**Tokens javalang** usam tokens estruturais como folhas — ex: literais numéricos `65`, operadores `>=`. Esses capturam padrões de controle de fluxo mais generalizáveis.

### Taxa de parsing: 100% srcML vs ~86% javalang

Em amostra de 200 CSIDs: 20 casos onde javalang retornou `[]` mas srcML extraiu paths. Zero casos do contrário. Taxa global: 100% (43,661/43,661).

**Contexto:** javalang exige código sintaticamente válido para parsear qualquer método (`parse_member_declaration`). srcML produz XML parcial mesmo com graves erros de sintaxe.

### Número de paths por submissão: similar

- srcML: mean=48.2, std=5.8 (86% atingem cap R=50)
- javalang: mean=44.1, std=15.5 (85% atingem cap R=50)

srcML tem std menor — extrai caminhos mais uniformemente (árvore mais "balanceada" em termos de pares de folhas acessíveis com filtros max_path_length=8, max_path_width=2).

---

## Métricas-chave dos resultados

### First-attempt AUC (10 runs × seeds 42-51):

| Assignment | srcML-DKT | Code-DKT | DKT | Δ(srcML−Code-DKT) |
|---|---|---|---|---|
| A439 | 70.41±1.01% | 73.27% | 75.56% | **-2.86pp** |
| A487 | 76.56±0.87% | 79.56% | 76.70% | **-3.00pp** |
| A492 | 81.93±0.71% | 86.12% | 82.05% | **-4.19pp** |
| A494 | 78.30±0.90% | 81.85% | 80.17% | **-3.54pp** |
| A502 | 81.17±0.99% | 84.98% | 80.78% | **-3.82pp** |

**srcML-DKT ficou abaixo do Code-DKT em todos os 5 assignments.** Isso diverge do paper de referência (Pankiewicz et al., 2025), que reporta +1.65pp sobre Code-DKT.

### Hipóteses para o resultado abaixo do esperado:

1. **Vocabulário menos discriminativo:** paths srcML têm menos diversidade (tags genéricas) → atenção code2vec tem menos informação para distinguir subproblemas de KT.

2. **Noise de Compile.Error no treino:** treinar com Compile.Error (sempre `correct=0`) injeta eventos de erro que podem criar viés nas sequências KT — os outros modelos não veem esse ruído.

3. **Hiperparâmetros não tunados para srcML:** `BEST_CDKT_CONFIG` foi otimizado para javalang. É provável que srcML tenha um ótimo diferente (ex: hidden_dim menor, mais dropout para compensar vocabulário menos diverso).

4. **Generalização do paper:** Pankiewicz et al. usam C#, CS1 condicionais, 610 alunos — condições muito diferentes do CSEDM Java/Spring 2019. O ganho pode não se transferir.

**O extractor foi verificado como correto** — paths têm estrutura semântica coerente, número de paths por submissão compatível com javalang, 0 falhas em 43,661 CSIDs. O resultado reflete as propriedades do extrator, não um bug.

---

## Caminhos exatos dos artefatos gerados

| Artefato | Path | Tamanho est. | Gitignored? |
|---|---|---|---|
| Código extractor | `src/srcml_features.py` | ~8 KB | Não |
| Notebook executado | `notebooks/09_srcml_dkt.ipynb` | ~316 KB | Não |
| Cache srcML | `results/srcml_features_cache.pkl` | ~200 MB | **Sim** |
| Resultados multirun | `results/srcml_dkt_results_multirun.pkl` | ~70 MB | Não |
| Notas Chat 1 | `docs/srcml_dkt_chat1_notes.md` | este arquivo | Não |

**Regenerar o cache:** `notebooks/09_srcml_dkt.ipynb` Seção 4 (detecta automaticamente se o arquivo existe).

---

## Pontos que merecem destaque na documentação final

1. **Cobertura srcML vs javalang:** o ganho mais claro do srcML não é AUC — é a taxa de parsing (100% vs ~86%). Isso tem valor metodológico mesmo com AUC menor.

2. **Resultado negativo é válido e honesto:** reportar que srcML-DKT não superou Code-DKT no CSEDM, com hipóteses bem fundamentadas, é contribuição metodológica — especialmente útil para trabalhos futuros que queiram adaptar a abordagem.

3. **Decisão de avaliação no test set bkt_dkt:** documentar claramente que o test set de avaliação é idêntico aos outros 3 modelos (`sequences_bkt_dkt.pkl`), mesmo o treino usando sequências diferentes. Isso garante comparabilidade.

4. **Paper não especifica o extractor:** Pankiewicz et al. (2025) mostram apenas um exemplo de path `[input, method, body, doSomething, input]` — não há algoritmo publicado. Todas as decisões de implementação (regra folha/interior, raiz virtual `<unit>`, encoding do namespace) foram tomadas ad-hoc e devem ser documentadas como tais.

5. **Possível ablation para TCC 2:** treinar srcML-DKT SEM Compile.Error (igual ao Code-DKT, só com Run.Program) para isolar o efeito do parser vs o efeito dos eventos extras. Dado o tempo do TCC 1, não foi feito.
