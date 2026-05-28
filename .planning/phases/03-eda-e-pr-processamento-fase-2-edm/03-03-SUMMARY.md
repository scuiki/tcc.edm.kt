---
phase: 03-eda-e-pr-processamento-fase-2-edm
plan: 03
status: complete
requirements:
  - EDA-01
key-files:
  modified:
    - apresentacao/index.html
    - apresentacao/assets/theme-unifacens.css
  created:
    - scripts/build_eda_correct_rate_by_assignment.py
    - results/sec3_correct_rate_by_assignment.png
commits:
  - aa69eb1
  - 2944567
---

## What Was Built

Slide EDA-01 ("como navegamos o csedm") inserido em `apresentacao/index.html`
após o INTRO-01 movido, posição final #/12. Estrutura:
- Cabeçalho `> como navegamos o csedm` (variante (a) do 03-RESEARCH §7.1)
- Parágrafo descritivo neutro de abertura (1 linha)
- Título da tabela em padrão ABNT/IBGE 1993: "Tabela 1 – Taxa de acerto por
  *assignment* (Spring 2019)" com en-dash (`&ndash;`)
- Tabela `.eda-grid` (5 linhas × 5 colunas): Assignment | Alunos | Participação |
  Problemas | Taxa de acerto
- Fonte abaixo da tabela: "Fonte: elaborado pelo autor sobre CSEDM (Spring 2019)."

Bloco CSS `.eda-grid` adicionado em `theme-unifacens.css` (~30 linhas, padrão
ABNT/IBGE: 3 bordas horizontais, sem grade fechada, fundo transparente, última
coluna em azul UniFacens).

Script reproducible `scripts/build_eda_correct_rate_by_assignment.py` cria
PNG de barras horizontais por assignment a partir de `MainTable.csv`. PNG
gerado em `results/sec3_correct_rate_by_assignment.png` (não usado pelo
slide final; ver Deviations).

## Reorganização narrativa (decisão pós-checkpoint, importante)

O Plan 03-03 original previa inserir um EDA-01 com cabeçalho idêntico após
MARKER-01 e antes do EDA-02. Durante o checkpoint visual, o reviewer apontou
3 ajustes que alteraram a estrutura do plan:

1. **INTRO-01 movido**: O slide "O dataset CSEDM em ProgSnap2 (Price, 2020)"
   estava em #/8 (seção Introdução). Foi movido para depois do MARKER-01
   (posição #/11), tornando-se o slide de abertura da Fase 2 EDM. Justificativa:
   "dataset" pertence narrativamente à Preparação dos Dados, não à Introdução.

2. **Afirmação sobre dificuldade removida**: O phrasing original do
   03-RESEARCH §2.4 dizia "os 5 assignments cobrem dificuldades muito
   diferentes". Foi removido porque KCs ainda não foram introduzidos na
   apresentação (chegará na Fase 3 — Modelagem). Substituído por descrição
   neutra: "observamos como a participação e a taxa de acerto se distribuem
   entre os 5 assignments do curso."

3. **Tabela refatorada para ABNT/IBGE**: Versão original tinha grade fechada
   (estética de Quadro). Manual MSGQ-21.01 p. 22 prescreve apenas 3 bordas
   horizontais (Normas de Apresentação Tabular, IBGE 1993). CSS atualizado.

Ajustes adicionais (segunda iteração de checkpoint):
- Coluna nova "Participação" entre Alunos e Problemas (% sobre 413 total,
  revela dropout natural sem interpretar como dificuldade)
- Tabela com fundo transparente (não branco)
- Primeira coluna (A1..A5) centralizada e sem negrito (negrito mantido só
  em "Taxa de acerto")
- Título: dois pontos `:` → en-dash `–` (conforme manual ABNT)
- Header "% do total" → "Participação"
- Fonte da tabela: "Fonte: elaborado pelo autor sobre CSEDM (Spring 2019)."
  (padrão ABNT abaixo da tabela; `.rel-cite` do rodapé do slide removida
  para evitar duplicação)

## Linhas CSS adicionadas

`apresentacao/assets/theme-unifacens.css` linha 454-486 (33 linhas):
- `.eda-title` (Arial 18px bold centralizado)
- `.eda-grid` (border-top + border-bottom 1.5px preto)
- `.eda-grid th, td` (border none, padding 9px 18px, center)
- `.eda-grid th` (border-bottom 1.5px, fundo transparente)
- `.eda-grid td` (fundo transparente)
- `.eda-grid tr td:last-child` (azul UniFacens negrito)
- `.eda-source` (Arial 14px cinza centralizado)
- `.eda-fig` + `.eda-fig img` (container de imagem, max-height 220px)

`var(--uni-blue)` total no CSS subiu de 29 para 30. `var(--uni-ink)` subiu
de 29 para 31. Sem variáveis novas. Sem border-radius positivo.

## Acceptance Criteria — passaram (com 2 ressalvas)

- Header da tabela: 5 colunas ✓
- 5 linhas A1..A5 com números MainTable Spring 2019 ✓
- Coluna Participação com 93,46% / 82,32% / 87,41% / 76,27% / 74,09% (calculados
  como n_students / 413) ✓
- Vírgula decimal pt-BR ✓
- Tabela ABNT: 3 bordas horizontais, sem grade fechada, transparente ✓
- Última coluna em azul UniFacens negrito ✓
- Título com en-dash (`&ndash;`) ✓
- Fonte "elaborado pelo autor" abaixo da tabela ✓
- ProgSnap2 só aparece no INTRO-01 movido (Pitfall 2) ✓ (refinado: 2 ocorrências
  totais incluem comentário HTML invisível; corpo visível = 1)
- Code-DKT, Release/Train, em-dash, blockquote/h2 — todos 0 dentro do EDA-01 ✓

Ressalvas conhecidas:
- Critério `<i>et al.</i>` 10-11 do plan original foi calculado pre-EDA-02;
  baseline real era 11 antes do EDA-01. Pós-EDA-01 ficou em 12.
- PNG em `apresentacao/assets/eda-taxa-acerto-por-assignment.png` foi gerado
  durante uma iteração de checkpoint (versão com gráfico abaixo da tabela)
  e depois removido do filesystem após o reviewer decidir que a tabela
  comunica melhor sem o gráfico. Script + PNG em `results/` permanecem;
  re-execução do script restaura o asset se necessário.

## Checkpoint visual — APPROVED

Reviewer aprovou após 3 iterações no checkpoint (média esperada para fase 3
era 2 iterações; uma iteração extra foi devido ao retrabalho de mover o
INTRO-01 e remover o gráfico). Estado final aprovado em 2026-05-28.

## Deviations

- **D-66e (nova decisão ad-hoc)**: Slide do dataset CSEDM (texto INTRO-01)
  pertence à Fase 2 EDM, não à Introdução. INTRO-01 movido de #/8 para #/11.
  Aplicar nas próximas fases: se for criar novos slides INTRO sobre dataset,
  inseri-los após o MARKER da fase correspondente, não antes.
- **D-66f (nova decisão ad-hoc)**: Slides EDA não devem afirmar dificuldade
  entre assignments antes da Fase 3 (Modelagem) introduzir KCs. Descrição
  neutra (participação + taxa de acerto) é suficiente.
- **D-66g (nova decisão ad-hoc)**: Padrão ABNT para tabelas em slides:
  título acima com en-dash, 3 bordas horizontais sem grade fechada,
  fundo transparente, fonte centralizada abaixo ("Fonte: elaborado pelo
  autor sobre [base de dados] ([recorte])."). Componente `.eda-grid`
  reutilizável estabelecido neste plan para futuros slides EDA-* / MODEL-*.

## Self-Check: PASSED
