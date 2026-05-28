---
phase: 02-intro-dataset-e-problema-fase-1-edm
plan: 01
subsystem: presentation
tags: [reveal-js, css-component, slide-marker, phase2-edm, html, css]

requires:
  - phase: 01-reformatacao-da-base
    provides: theme-unifacens.css com STYLE.md atualizado (cabecalho .deck-topic uniforme) e index.html limpo com 12 sections + Fonte 18px padronizado
provides:
  - Componente CSS reutilizavel .slide-marker em theme-unifacens.css (modificadores --done e --pending) que sera consumido por MARKER-02/03/04 nas fases 3-5 sem alteracao adicional
  - Slide MARKER-01 em apresentacao/index.html sinalizando "Definicao do Problema" concluida sobre as 4 fases EDM
  - Inicio fisico do bloco da fase 2 EDM no deck (linha 149 do index.html); os INTRO-01 e INTRO-03 (plans 02-02/03/04) inserem-se ANTES deste section
affects: [phase-2-intro, phase-3-eda, phase-4-modelagem, phase-5-encerramento]

tech-stack:
  added: []
  patterns:
    - "Componente .slide-marker BEM-style (host + elementos __mark + modificadores --done/--pending) reusavel por 4 slides marcadores"
    - "Section marker sem .deck-topic (D-34d): o proprio componente visual e o cabecalho narrativo"

key-files:
  created: []
  modified:
    - apresentacao/assets/theme-unifacens.css
    - apresentacao/index.html

key-decisions:
  - "D-NN ad-hoc 2026-05-27: MARKER-01 entregue como STUB funcional aprovado; redesenho do componente .slide-marker DIFERIDO para o fim da fase 2 (apos plans 02-02/03/04 fluirem). Usuario aprovou o stub porque desbloqueia a fase, mas nao gostou do formato atual (progress bar com 4 caixas) e quer revisitar com vies de computacao (ex.: AST, pipeline, terminal) junto com MARKER-02/03/04. O componente atual continua valido como contrato de classes; sera reescrito visualmente sem quebrar callers."

patterns-established:
  - "Marcador de fase EDM concluida: section dedicado entre blocos narrativos, sem .deck-topic, com rodape Fonte: padronizado em Arial 18px #5b6472"
  - "Stub-first em componente compartilhado: validar contrato (classes/modificadores) primeiro em #/N do deck, deixar redesenho visual para depois quando os callers existirem"

requirements-completed: [MARKER-01]

duration: 2min
completed: 2026-05-27
---

# Phase 2 Plan 01: MARKER-01 (Definicao do Problema concluida) Summary

**Componente CSS reutilizavel `.slide-marker` (host + modificadores --done/--pending) e section MARKER-01 em index.html (progress bar das 4 fases EDM, "Definicao do Problema" sinalizada como concluida) entregues como STUB funcional aprovado pelo reviewer humano; redesenho do formato visual diferido para o fim da fase 2.**

## Performance

- **Duration:** ~2 min (entre commits `d37304d` 21:11:55 e `3d47be4` 21:12:37; checkpoint humano contabilizado fora do tempo de execucao)
- **Started:** 2026-05-27T21:11:55-03:00 (primeiro commit)
- **Completed:** 2026-05-27T21:12:37-03:00 (segundo commit) + aprovacao humana subsequente
- **Tasks:** 2 auto + 1 checkpoint humano (3 total)
- **Files modified:** 2 (`apresentacao/assets/theme-unifacens.css`, `apresentacao/index.html`)

## Accomplishments

- Bloco CSS `.slide-marker` (host + `.marker-track` + `.marker-step` + `.marker-step__mark` + `.marker-step--done` + `.marker-step--pending` + `.marker-arr` + `.slide-marker .marker-fonte`) anexado ao fim do `theme-unifacens.css` com cabecalho de bloco no padrao do arquivo, usando apenas variaveis existentes (`--uni-blue`, `--uni-light`, `--uni-gray`, `--mono`).
- Section MARKER-01 inserido entre o slide Yagci fundido e o slide-code, 4 caixas na ordem D-40 ("Definicao do Problema" em `--done` com `&check;`; "Preparacao dos Dados", "Modelagem e Avaliacao", "Implantacao" em `--pending` com numeros 2/3/4), 3 setas `&rarr;`, rodape `Fonte: adaptado de Zoric (2020).`
- Total de sections do deck subiu de 12 para 13 (slide acessivel temporariamente em `#/7`; deslocara para `#/10` quando os 3 INTRO da fase 2 forem inseridos antes dele).
- Componente reusable validado em browser pelo reviewer humano: stub aprovado, pronto para ser consumido por MARKER-02/03/04 sem alteracao adicional no CSS (basta trocar qual caixa fica `--done`).

## Task Commits

Cada task foi commitada atomicamente:

1. **Task 1: Bloco CSS .slide-marker reutilizavel em theme-unifacens.css** - `d37304d` (feat)
2. **Task 2: Section MARKER-01 em apresentacao/index.html** - `3d47be4` (feat)
3. **Task 3: Checkpoint human-verify (validacao visual em #/7)** - APPROVED (sem commit; ajustes visuais aplicados: NENHUM)

**Plan metadata:** (a ser registrado neste mesmo commit final, junto de STATE.md / ROADMAP.md / REQUIREMENTS.md)

## Files Created/Modified

### `apresentacao/assets/theme-unifacens.css`
- **Tipo:** modificacao (append puro; nenhuma regra existente alterada).
- **Intervalo das linhas inseridas:** linhas **358-408** do arquivo final (51 linhas adicionadas; o arquivo crescer de 357 para 408 linhas no total). Bloco delimitado pelo comentario de cabecalho `=========================================================================== / SLIDE - Marker / ===========================================================================` ate a regra `.slide-marker .marker-fonte`.
- **Classes definidas:** `.slide-marker`, `.slide-marker .wm`, `.marker-track`, `.marker-step`, `.marker-step__mark`, `.marker-step--done`, `.marker-step--done .marker-step__mark`, `.marker-step--pending`, `.marker-step--pending .marker-step__mark`, `.marker-arr`, `.slide-marker .marker-fonte`.

### `apresentacao/index.html`
- **Tipo:** modificacao (insercao apos linha 147; nenhum slide existente alterado).
- **Intervalo das linhas inseridas:** linhas **149-179** do arquivo final (31 linhas adicionadas; o arquivo cresceu de 468 para 499 linhas). Comentario `<!-- ============ SLIDE - MARKER - Definicao do Problema concluida (Zoric, 2020) ============ -->` em 149; `<section>` aberto em 150; conteudo (4 caixas + 3 setas + rodape) entre 151-177; `</section>` em 179.
- **Ponto de insercao verificado:** entre o `</section>` do slide Yagci fundido (linha 147 pre-insercao, agora 147) e o comentario `<!-- ============ SLIDE -code- ============ -->` (que era a primeira linha apos a linha em branco e agora foi empurrado para 181). Linha 148 permanece em branco como separador entre sections.
- **Markup novo:** `<section data-background-color="#F1F6FB"><div class="deck-slide slide-marker slide-marker--phase1">...</div></section>`; svg de marca dagua preservado (`<use href="#sym"/>`); sem `.deck-topic` (D-34d); rodape em `<p class="marker-fonte">Fonte: adaptado de Zoric (2020).</p>` (com cedilha e acento conforme D-40).

## Decisions Made

### D-NN ad-hoc (2026-05-27): MARKER-01 aceito como stub, redesenho diferido

- **Contexto:** No checkpoint human-verify de Task 3, o reviewer humano abriu `#/7` no browser e confirmou que: (a) o componente renderiza sem layout quebrado, (b) o contrato de classes (`--done`/`--pending`/`__mark`) funciona, (c) rodape Fonte: centralizado, sem em-dash, sem `.deck-topic`, marca dagua presente. Todos os criterios automatizados do plano (D-31, D-44, D-45, D-46, D-47) batem.
- **Feedback adicional do reviewer:** o formato atual (progress bar com 4 caixas horizontais, estilo "stepper de checkout") nao agrada visualmente; quer redesenhar com **vies de computacao** (referencias possiveis: AST, terminal/CLI, pipeline com setas tipograficas, blocos de codigo, indicador de progresso de build). Mas o redesenho EXIGE ver o componente no fluxo real da fase 2 (depois que INTRO-01 e INTRO-03 estiverem no deck antes dele).
- **Decisao:** STUB aceito. Redesenho do `.slide-marker` postponed para apos plan 02-04 (fim da fase 2) ou consolidado junto com MARKER-02/03/04 (uma rodada visual unica que beneficia os 4 marcadores). O componente atual continua valido como contrato de classes; sera reescrito apenas no nivel visual sem quebrar os callers.
- **Implicacao:** plans 02-02/03/04 (INTRO-01, INTRO-03a/b) seguem sem dependencia bloqueante. MARKER-02/03/04 nas fases 3-5 herdam o stub atual e serao redesenhados em conjunto quando o redesenho ocorrer.

Demais decisoes do plano (D-31 posicao DOM, D-34d sem `.deck-topic`, D-39 estetica, D-40 textos literais, D-41 reuso, D-44 sem em-dash, D-45 rodape Fonte, D-46 sem italico em nomes EDM, D-47 validacao visual) foram seguidas como especificadas, sem alteracao.

## Deviations from Plan

None - plan executed exactly as written. A unica nuance foi a captura explicita, em decisao, do feedback humano "stub aceito, redesenhar depois". O criterio de exito original (validacao visual no browser em `#/7`) foi atendido; o feedback sobre formato visual e item de iteracao futura, nao gap do plan executado.

## Issues Encountered

Nenhum. Tasks 1 e 2 passaram em todos os criterios automatizados na primeira tentativa. Checkpoint humano aprovou sem necessidade de ajustes ao vivo (font-size, min-height, quebra de linha em "Modelagem e Avaliacao": nenhum precisou ser alterado).

## User Setup Required

None - alteracoes puramente em HTML/CSS estatico. `apresentacao/index.html` continua navegavel servido por `python3 -m http.server 8000` em `apresentacao/`.

## Next Phase Readiness

- Plan 02-02 (INTRO-01: slide "o dataset csedm") esta liberado para execucao. O ponto de insercao previsto para os 3 INTRO da fase 2 esta antes do section MARKER-01 (que hoje ocupa `#/7`). Apos os 3 INTRO entrarem, MARKER-01 desloca para `#/10` conforme planejado.
- Componente `.slide-marker` esta validado e pronto para ser consumido por MARKER-02/03/04 (fases 3/4/5) sem alteracao adicional no CSS. A unica mudanca por marcador subsequente sera trocar qual caixa carrega o modificador `--done`.
- Backlog visual: redesenhar `.slide-marker` com vies de computacao no fim da fase 2 ou consolidado em fase posterior junto com MARKER-02/03/04. Sem bloqueio imediato; o stub atual atende.

## Self-Check: PASSED

Verificacoes apos escrita do SUMMARY:

- Files referenciados existem no working tree:
  - `apresentacao/assets/theme-unifacens.css` (408 linhas) - FOUND
  - `apresentacao/index.html` (499 linhas) - FOUND
- Commits referenciados existem na historia git:
  - `d37304d` - FOUND (apresentacao: componente .slide-marker reutilizavel (fase 2))
  - `3d47be4` - FOUND (apresentacao: slide MARKER-01 - definicao do problema (fase 2))
- Componente verificavel por grep:
  - `grep -c '\.slide-marker {' apresentacao/assets/theme-unifacens.css` retorna >= 1
  - `grep -c 'slide-marker--phase1' apresentacao/index.html` retorna 1

---
*Phase: 02-intro-dataset-e-problema-fase-1-edm*
*Plan: 01 (MARKER-01)*
*Completed: 2026-05-27*
