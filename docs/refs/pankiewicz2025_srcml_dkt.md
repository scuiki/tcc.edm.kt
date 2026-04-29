---
source: docs/2025.EDM.short-papers.83.pdf
cite_as: Pankiewicz, Shi & Baker (2025)
title: "srcML-DKT: Enhancing Deep Knowledge Tracing with Robust Code Representations from srcML"
venue: Proceedings of the 18th International Conference on Educational Data Mining (EDM 2025), Palermo, Italy, pp. 541–548
doi: https://doi.org/10.5281/zenodo.15870306
---

## Resumo de uma linha
Extensão do Code-DKT que substitui geração de AST por srcML, permitindo incluir submissões não-compiláveis na sequência de KT.

## Fatos críticos para este projeto
- srcML parseia código Java (e C, C++, C#) compilável **e** não-compilável — preserva estrutura parcial como XML
- 66% das submissões não-compiláveis do dataset deste paper são também não-parsáveis por AST padrão
- Arquitetura srcML-DKT é **idêntica ao Code-DKT** (LSTM + atenção); apenas a extração de features muda
- Code paths são extraídos da árvore srcML da mesma forma que do AST no Code-DKT original
- Este paper usa dataset **diferente do CSEDM**: RunCode (plataforma europeia, C#, N=610 alunos, 6 tarefas condicionais, 2020–2024) — resultados **não são diretamente comparáveis** com Shi et al. (2022)

## Resultados quantitativos (Table 3 — dataset RunCode, C#)
| Métrica | srcML-DKT | Code-DKT | DKT | Contexto |
|---------|-----------|----------|-----|---------|
| AUC (first attempts) | **0.8355** | 0.8190 | 0.7931 | Table 3 |
| F1 (first attempts) | **0.8278** | 0.8225 | 0.8132 | Table 3 |
| AUC (all attempts) | **0.8467** | 0.8306 | 0.8177 | Table 3 |
| F1 (all attempts) | **0.8053** | 0.7965 | 0.7921 | Table 3 |

srcML-DKT supera Code-DKT em ~1.6pp AUC e ~4.2pp sobre DKT baseline.

## Metodologia relevante
- Hiperparâmetros: learning rates {0.0001, 0.0005, 0.001, 0.005, 0.01}; epochs 80–180 (step 20); 10 runs por configuração
- Split: 3:1:1 treino/validação/teste ao nível do aluno (sem vazamento entre splits)
- Métrica de seleção: AUC média sobre 10 runs no validation set
- Avaliação final: média de 10 runs no test set (controla variabilidade de inicialização)
- Submissões não-compiláveis entram na sequência com `correct=0` e features srcML
- Dataset tem 6.472 submissões totais; 2.018 (31%) não-compiláveis

## Atenção para implementação no CSEDM
- No CSEDM (Java), Compile.Error events devem entrar na sequência como `correct=0` com features srcML
- A lógica de extração de code paths é a mesma: nós srcML XML → sequências de texto → embeddings via atenção
- O paper **não reporta** resultados no CSEDM — os valores de referência para este TCC são os de Shi et al. (2022) (Table 1 e Table 2)

## Citação BibTeX
```
@inproceedings{pankiewicz2025srcmldkt,
  author    = {Maciej Pankiewicz and Yang Shi and Ryan S. Baker},
  title     = {srcML-DKT: Enhancing Deep Knowledge Tracing with Robust Code Representations from srcML},
  booktitle = {Proceedings of the 18th International Conference on Educational Data Mining},
  pages     = {541--548},
  year      = {2025},
  address   = {Palermo, Italy},
  doi       = {10.5281/zenodo.15870306}
}
```
