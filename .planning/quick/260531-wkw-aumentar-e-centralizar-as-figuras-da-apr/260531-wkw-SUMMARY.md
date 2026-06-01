---
phase: quick-260531-wkw
plan: 01
subsystem: apresentacao
tags: [abnt, figuras, tabelas, css, fonte]
requires:
  - apresentacao/index.html (estado pos-d40a4c4, sem rodapes Fonte:)
  - apresentacao/assets/theme-unifacens.css (.eda-source e .fig-fonte ja existentes)
provides:
  - 9 rodapes Fonte: ABNT abaixo de figuras e tabelas
  - 4 figuras de imagem maiores e centralizadas
  - hack margin-bottom -100px removido do slide-fig
  - STYLE.md com regra matizada de Fonte
affects:
  - apresentacao/index.html
  - apresentacao/assets/theme-unifacens.css
  - apresentacao/STYLE.md
tech-stack:
  added: []
  patterns:
    - reuso das classes CSS existentes .eda-source e .fig-fonte (zero CSS novo para Fonte)
    - regra matizada de citacao ABNT (texto sem Fonte; figuras/tabelas com Fonte)
key-files:
  created: []
  modified:
    - apresentacao/index.html
    - apresentacao/assets/theme-unifacens.css
    - apresentacao/STYLE.md
decisions:
  - Reusar .eda-source para 8 rodapes (Tabela 1, Fig 1, Fig 2, AST, Tabela 2, Pipeline, Mapa KCs, Fluxo) e .fig-fonte para Curvas Martins
  - AST aumentada de 620px para 760px (max-height 440px); Figura 2 (compact) de 72/340 para 88/430; Figura 1 (wide) de 150% para 160%; Curvas Martins de 92/488 para 96/520
  - Hack -100px substituido por margin-bottom 6px (espacamento normal)
metrics:
  duration: ~12 min
  completed: 2026-05-31
---

# Quick Task 260531-wkw: Aumentar e centralizar as figuras da apresentacao Summary

Restauracao dos 9 rodapes `Fonte:` ABNT abaixo de cada figura e tabela do deck (removidos em `d40a4c4`), com aumento e centralizacao das 4 figuras de imagem e remocao do hack `margin-bottom: -100px` do `.slide-fig`.

## O que foi feito

### Task 1 — Rodapes Fonte ABNT (commit `2e001c9`)
9 paragrafos de `Fonte:` re-adicionados em `apresentacao/index.html`, um abaixo de cada figura e tabela, com texto literal do mapa do CONTEXT.md e `<i>et al.</i>` preservado nos 5 que o usam:

| Elemento | Slide | Classe | Texto |
|---|---|---|---|
| Tabela 1 | EDA-01 (#/10) | `.eda-source` | elaborado pelo autor sobre CSEDM (Spring 2019). |
| Figura 1 | EDA-03 (#/11) | `.eda-source` | elaborado pelo autor sobre CSEDM (Spring 2019). |
| Figura 2 | EDA-04 (#/12) | `.eda-source` | elaborado pelo autor sobre CSEDM (Spring 2019). |
| AST | MODEL-01b (#/17) | `.eda-source` | adaptado de Shi *et al.* (2022). |
| Tabela 2 | MODEL-04 (#/19) | `.eda-source` | elaborado pelo autor (10 seeds); Shi *et al.* (2022) Table 2. |
| Pipeline KCs | MODEL-05 (#/20) | `.eda-source` | elaborado pelo autor; adaptado de Duan *et al.* (2025). |
| Mapa KCs | slide-kcfig (#/23) | `.eda-source` | elaborado pelos autores, com base em Duan *et al.* (2025) e Martins, Marin e Alves (2024). |
| Curvas Martins | slide-fig (#/24) | `.fig-fonte` | elaborado pelos autores (estimativa do Code-DKT...). |
| Fluxo aplicacao | TOOL-01 (#/26) | `.eda-source` | elaborado pelo autor; baseado em *docs/tcc2_prototipo.html*. |

Nenhuma classe CSS nova foi criada (reuso de `.eda-source` e `.fig-fonte` ja existentes). Nenhum slide de texto recebeu `Fonte:`.

### Task 2 — Aumentar e centralizar figuras + remover hack (commit `4eba34e`)
- `.slide-fig` (Curvas Martins): `margin-bottom: -100px` no `.eda-title` substituido por `6px` (espacamento normal); imagem ampliada via CSS `.slide-fig .fig-wrap img` de `max-width: 92% / max-height: 488px` para `96% / 520px`.
- Figura 2 (`.eda-fig--compact`, a menor): de `max-width: 72% / img 340px` para `88% / 430px`.
- Figura 1 (`.eda-fig--wide`): de `max-width: 150%` para `160%`.
- AST (`ast_codedkt_ptbr.svg`, MODEL-01b): `max-width` inline de `620px` para `760px` + `max-height: 440px`.
- Centralizacao preservada (flex justify-center ja presente em `.eda-fig` e `.fig-wrap`).
- Tabelas NAO redimensionadas (fora de escopo).

### Task 3 — STYLE.md regra matizada (commit `4a0ca45`)
Substituidas as 3 afirmacoes obsoletas ("rodapes Fonte: removidos de todos os slides") nas secoes "Cabecalho de todo slide", "Convencoes de citacao" e "Regras de redacao" pela regra matizada: slides de texto sem `Fonte:`; figuras e tabelas com `Fonte:` abaixo via `.eda-source` ou `.fig-fonte`.

## Deviations from Plan

None - plan executado exatamente como escrito. Magnitudes de aumento das figuras escolhidas a discricao do executor (validacao visual no checkpoint).

## Verificacao automatizada

- `grep -c 'eda-source\|fig-fonte' apresentacao/index.html` => 9 (PASS)
- `grep -c 'margin-bottom: -100px' apresentacao/index.html` => 0 (PASS)
- `grep -i 'figuras e tabelas levam' STYLE.md` => presente (PASS)
- `grep -c 'removidos de todos os slides' STYLE.md` => 0 (PASS)
- `curl http://127.0.0.1:8011/` => HTTP 200 (PASS)

## Revisao pos-checkpoint (commit `e17c04e`)

O usuario revisou no browser apos o checkpoint e pediu ajustes finos. Aplicados em `apresentacao/index.html` (somente HTML; nenhuma regra CSS nova ou alterada, a troca de classe `.fig-fonte`->`.eda-source` e feita no markup):

| # | Slide | Delta |
|---|---|---|
| 1 | MODEL-05 Pipeline (#/20) | `Fonte:` movida para logo abaixo do `.bridge-seq` (antes dos paragrafos finais); `margin-top` do paragrafo "Como o CSEDM..." 44px->18px. Fonte agora colada na figura, nada estoura 720px. |
| 2 | TOOL-01 Fluxo (#/26) | `Fonte:` movida para logo abaixo do `.bridge-seq`; `margin-top` exagerados 110px->22px no `.eda-title` e no paragrafo "A ideia e o professor...". |
| 3 | slide-fig Curvas Martins (#/24) | classe `.fig-fonte` (18px) -> `.eda-source` (14px), texto literal identico (mantidos `<i>et al.</i>`). |
| 4 | MODEL-01b AST (#/17) | `<img>` ampliado de `max-width:760px; max-height:440px` para `900px / 500px`, centralizado. |
| 5 | varios | Figuras renumeradas em ordem de aparicao: Fig 3 (AST), Fig 4 (Pipeline), Fig 5 (Mapa KCs), Fig 6 (Curvas Martins), Fig 7 (Fluxo). Fig 1, Fig 2, Tabela 1 e Tabela 2 inalteradas. |

Fora de escopo (nao feito): negrito nos eixos dos PNG; nenhum `Fonte:` em slide de texto; `ROADMAP.md` nao tocado; `theme-unifacens.css` nao alterado (todas as correcoes couberam no HTML inline).

### Verificacao da revisao
- `grep -o 'Figura[^<]*&ndash;'` => Figura 1..7 sequenciais; `grep -c 'Figura &ndash;'` => 0 (PASS)
- `grep -c 'class="fig-fonte"'` => 0 (PASS); `grep -c 'class="eda-source"'` => 9 (PASS)

## Checkpoint pendente

Task 4 (`checkpoint:human-verify`, gate blocking) AGUARDANDO nova verificacao humana no browser apos a revisao. Preview ativo em `http://127.0.0.1:8015`. A tarefa NAO esta 100% concluida ate o "approved" humano.

## Self-Check: PASSED
- apresentacao/index.html: FOUND (9 rodapes + figuras ajustadas)
- apresentacao/assets/theme-unifacens.css: FOUND (regras de tamanho ajustadas)
- apresentacao/STYLE.md: FOUND (regra matizada)
- Commit 2e001c9: FOUND
- Commit 4eba34e: FOUND
- Commit 4a0ca45: FOUND
