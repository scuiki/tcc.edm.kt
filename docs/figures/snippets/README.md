# Snippets selecionados para figuras F4, F6 e F7

Os dois snippets abaixo são submissões reais do dataset CSEDM (Spring 2019), usadas como exemplos didáticos nas figuras do documento `docs/METODOLOGIA_FERRAMENTAS.md`. Ambas resolvem o problema `makeChocolate` (clássico do CodingBat), com enunciado: dadas barras de chocolate de 5 kg (`big`) e 1 kg (`small`), retornar o número exato de barras pequenas para atingir um objetivo `goal`, ou `-1` se impossível.

## `snippet_correct.java` (usado em F4 e F6)

| Campo | Valor |
|---|---|
| `CodeStateID` | `5f88190418323ba32cc75962121c5ff15f4b0460` |
| `SubjectID` | `e3edca0f6e68bfb76eaf26a8eb6dd94b` |
| `AssignmentID` | 487 |
| `ProblemID` | 101 |
| `EventType` | `Run.Program` |
| `Score` | 1.0 |
| LOC | 9 |
| Estruturas | `while`, `if`, atribuição composta, decremento |
| Parsing javalang | OK (50 paths leaf-to-leaf após truncagem) |
| Parsing srcML | OK (50 paths leaf-to-leaf após truncagem) |

## `snippet_compile_error.java` (usado em F7)

| Campo | Valor |
|---|---|
| `CodeStateID` | `ba79b6055bb66f076ccefc0f4398e4b44b7fc7c8` |
| `AssignmentID` | 487 |
| `ProblemID` | 101 |
| `EventType` | `Compile.Error` |
| LOC | 7 |
| Erro pedagógico | ponto-e-vírgula faltando em `return -1` e ausência de `return` no caminho principal |
| Parsing javalang | FALHA (`JavaSyntaxError` por token `}` inesperado após `return -1`) |
| Parsing srcML | OK (1149 bytes XML, árvore parcial preservada) |

Esses dois snippets foram escolhidos para que F4 e F6 mostrem o **mesmo aluno e mesmo problema** em forma compilável, e F7 evidencie o **caso central da motivação do srcML**: código sintaticamente quebrado que o parser tradicional (javalang) descarta mas o srcML representa parcialmente.
