---
source: docs/ProgSnap2.pdf
cite_as: Price et al. (2020)
title: "ProgSnap2: A Flexible Format for Programming Process Data"
venue: ITiCSE '20 — Proceedings of the 2020 ACM Conference on Innovation and Technology in Computer Science Education, Trondheim, Norway, pp. 356–362
doi: https://doi.org/10.1145/3341525.3387373
---

## Resumo de uma linha
Especificação de formato padronizado para dados de processo de programação — define a estrutura de tabelas, EventTypes e colunas que o CSEDM segue.

## Fatos críticos para este projeto
- O CSEDM dataset usa ProgSnap2 **versão 6** (nota de rodapé 1 do paper)
- Estrutura: `MainTable.csv` (eventos) + `DatasetMetadata.csv` + `LinkTables/` + `CodeStates/` + `Resources/`
- Colunas obrigatórias do Main Event Table: `EventID`, `EventType`, `SubjectID`, `ToolInstances`, `CodeStateID`
- `CodeStateID` mapeia para snapshots de código em `CodeStates/`

## EventTypes predefinidos relevantes para o CSEDM
| EventType | Significado |
|-----------|-------------|
| `Compile.Error` | Compilação com erro — código não executável |
| `Compile.Warning` | Compilação com aviso |
| `Run.Program` | Execução do programa (com `Score` no CSEDM) |
| `Submit` | Submissão formal (NÃO presente no CSEDM) |

**Nota CSEDM:** `Submit` não existe no CSEDM. Submissões são `Run.Program` com `Score` não-nulo.

## Colunas opcionais relevantes para KT
- `Score` (Real): proporção de testes passados [0, 1]; presente em `Run.Program` do CSEDM
- `AssignmentID`, `ProblemID`: contexto da tarefa — usados para definir KCs
- `Attempt` (Integer): número da tentativa do aluno na questão
- `CompileResult` (Enum: Success / Warning / Error): resultado da compilação
- `CompileMessageData`: mensagem de erro do compilador

## Estrutura de Code States
ProgSnap2 suporta três formatos para código:
1. **Table** — arquivo CSV único mapeando CodeStateID → código (adequado para CSEDM, arquivos únicos)
2. **Directory** — diretório por CodeStateID (para projetos multi-arquivo)
3. **Git** — commits em repositório Git

## Citação BibTeX
```
@inproceedings{price2020progsnap2,
  author    = {Thomas W. Price and David Hovemeyer and Kelly Rivers and
               Ge Gao and Austin Cory Bart and Ayaan M. Kazerouni and
               Brett A. Becker and Andrew Petersen and Luke Gusukuma and
               Stephen H. Edwards and David Babcock},
  title     = {ProgSnap2: A Flexible Format for Programming Process Data},
  booktitle = {Proceedings of the 2020 ACM Conference on Innovation and Technology in Computer Science Education (ITiCSE '20)},
  pages     = {356--362},
  year      = {2020},
  address   = {Trondheim, Norway},
  doi       = {10.1145/3341525.3387373}
}
```
