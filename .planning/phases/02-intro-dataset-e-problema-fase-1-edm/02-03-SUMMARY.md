---
phase: 02-intro-dataset-e-problema-fase-1-edm
plan: 03
subsystem: presentation
tags: [reveal-js, intro-slide, knowledge-tracing, shi-2022, abnt]

# Dependency graph
requires:
  - phase: 02
    provides: "INTRO-01 (slide #/7, dataset CSEDM em ProgSnap2); MARKER-01 stub (slide #/9 pré-INTRO-03b)"
provides:
  - "Section INTRO-03a em apresentacao/index.html linhas 166-181, slide #/8 do deck"
  - "Cabeçalho `> o problema do kt binário` (D-34b) com caret piscando"
  - "Diagnóstico em paráfrase indireta de Shi et al. (2022): BKT e DKT tratam respostas só como corretas/incorretas, ignorando o conteúdo"
  - "Ponte explícita KT → trabalho → CSEDM antes da crítica (3 parágrafos no slide)"
  - "Padrão ABNT `et al.` em itálico (`<i>et al.</i>`) normalizado em todo o deck (8 ocorrências)"
affects: [02-04, 04-modelagem, 04-MODEL-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Reuso de `.slide-related` + `.rel-lead` + `.rel-cite` (zero CSS novo)"
    - "Voz híbrida: ponte autoral em 1ª pessoa do plural → crítica autor-prominente (Shi et al.) → contextualização em domínios com respostas estruturadas"
    - "`<i>et al.</i>` ABNT em itálico aplicado consistentemente ao deck inteiro"

key-files:
  modified:
    - "apresentacao/index.html (INTRO-03a inserido linhas 166-181; normalização de `et al.` em todo o deck)"

key-decisions:
  - "D-52: paráfrase do Report 4 + Shi 2022 (mais fiel ao paper que a versão inicial; texto polido em 3 iterações pós-checkpoint)"
  - "D-53: ponte explícita KT → trabalho → CSEDM antes da crítica; primeiro parágrafo define o que é KT e ancora no nosso trabalho, depois Shi entra como crítica"
  - "D-54: padrão ABNT `<i>et al.</i>` em todo o deck (8 ocorrências); drive-by sweep aplicado na mesma iteração para evitar inconsistência visual"
  - "D-55: terceiro parágrafo abre escopo para domínios com respostas estruturadas (programação, matemática, ciências, escrita) sem nomear Code-DKT (gate forte; fase 4)"

patterns-established:
  - "Slide INTRO de diagnóstico: 3 parágrafos (ponte → crítica → contexto), sem citação direta literal, sem Code-DKT"
  - "Normalização `et al.` ABNT: aplicar em batch quando uma iteração tocar o padrão, não slide a slide"

requirements-completed: []  # INTRO-03 só fica completo após INTRO-03b no plan 02-04

# Metrics
duration: ~45min (incluindo 3 iterações pós-checkpoint)
completed: 2026-05-27
---

# Phase 2 Plan 03: INTRO-03a (problema do KT binário) Summary

**Slide INTRO-03a inserido em apresentacao/index.html como diagnóstico do problema do KT binário, com 3 parágrafos (ponte KT → crítica Shi et al. → escopo de domínios com respostas estruturadas) e padrão ABNT `<i>et al.</i>` normalizado em todo o deck.**

## Performance

- **Duration:** ~45 min (4 commits, 3 iterações pós-checkpoint visual)
- **Tasks:** 2 (1 auto + 1 checkpoint:human-verify APPROVED após 3 iterações)
- **Files modified:** 1 (apresentacao/index.html)

## Accomplishments

- Section INTRO-03a inserido entre INTRO-01 (#/7) e MARKER-01 (deslocou para #/9), slide acessível em `http://127.0.0.1:8000/#/8`
- Cabeçalho `> o problema do kt binário` (D-34b) com caret piscando, em padrão Cascadia 24px cor `#5b6472`
- Paráfrase de 3 parágrafos:
  1. **Bridge:** "Modelos de *knowledge tracing* estimam, a partir do histórico de tentativas, a probabilidade de um estudante acertar o próximo problema. No nosso trabalho, eles são o instrumento central para representar o aprendizado em programação a partir dos eventos do CSEDM."
  2. **Crítica Shi:** "Shi *et al.* (2022) apontam que a maioria desses modelos, incluindo **BKT** e **DKT**, tratam as respostas dos estudantes apenas como corretas ou incorretas, ignorando seu conteúdo."
  3. **Escopo:** "Daí a necessidade de modelos voltados a áreas com respostas estruturadas, como programação, matemática, ciências ou escrita, em que a forma da resposta importa tanto quanto o resultado final."
- Rodapé `Fonte: Shi <i>et al.</i> (2022).` (D-45)
- Padrão ABNT `<i>et al.</i>` aplicado em batch (8 ocorrências em todo o deck, drive-by) na quarta iteração
- Code-DKT NÃO mencionado (gate forte; fase 4)
- Total de sections do deck: 14 → 15 (após Task 1)

## Task Commits

Plan executado em 4 commits funcionais ao longo de 3 iterações pós-checkpoint:

1. **Task 1 (inicial):** `6f0ae3d` — `apresentacao: slide INTRO-03a - problema do kt binario (Shi et al. 2022)` — Markup do plano original (2 parágrafos: paráfrase indireta + reforço "Toda a riqueza do código submetido fica fora do modelo").
2. **Iteração 1 (reviewer feedback):** `53b46e8` — `apresentacao: reescrever INTRO-03a com fraseado do Report 4 + Shi 2022` — Reescrita usando phrasing do Report 4 do TCC + reaproximação ao Shi 2022 (mais fiel ao paper).
3. **Iteração 2 (reviewer feedback):** `f7e042a` — `apresentacao: adicionar ponte KT-trabalho-CSEDM em INTRO-03a` — Adicionado primeiro parágrafo explicando o que é KT e ancorando no nosso trabalho com o CSEDM, antes da crítica Shi.
4. **Iteração 3 (reviewer feedback):** `4a9af6e` — `apresentacao: italizar "et al." conforme ABNT no deck` — `<i>et al.</i>` aplicado no INTRO-03a + drive-by sweep nas demais 7 ocorrências do deck (Martins p1 inclusive).

**Task 2 (checkpoint:human-verify):** APPROVED após 3 iterações no #/8. Reviewer humano confirmou layout coerente em 1280×720, leitura fluente em pt-BR, sem em-dash, sem Code-DKT, padrão ABNT consistente.

## Files Created/Modified

- `apresentacao/index.html` — INTRO-03a inserido (linhas 166-181); normalização de `et al.` em todo o deck (8 ocorrências em `<i>et al.</i>`).

## Decisions Made

- **D-52 (paráfrase Report 4 + Shi 2022):** A versão inicial do slide (commit `6f0ae3d`) usava o phrasing-alvo do RESEARCH §1.3 (paráfrase indireta com reforço "Toda a riqueza do código submetido fica fora do modelo"). Após o checkpoint, o reviewer pediu prosa mais fiel ao paper Code-DKT e ao Report 4 do TCC (documento de projeto), o que disparou a reescrita para "tratam as respostas... apenas como corretas ou incorretas, ignorando seu conteúdo" (vocabulário mais próximo do Abstract Shi 2022 p.50).
- **D-53 (ponte KT → trabalho → CSEDM):** O slide original entrava direto na crítica Shi. Reviewer apontou descontinuidade narrativa entre o INTRO-01 (dataset CSEDM) e a crítica isolada. Solução: parágrafo de ponte que (a) define KT em uma linha, (b) ancora KT como instrumento central do nosso trabalho, (c) liga aos eventos do CSEDM. Trade-off: slide com 3 parágrafos em vez de 2, mas leitura fica natural e a transição para INTRO-03b ("sinal pedagógico perdido") fica menos abrupta.
- **D-54 (`<i>et al.</i>` ABNT):** Manual MSGQ-21.01 (apresentacao/) determina itálico em "et al." em pt-BR. O slide INTRO-03a recebeu o tratamento, e a inconsistência com os demais slides do deck ficou evidente. Drive-by sweep aplicado na mesma iteração para evitar duas passadas: 8 ocorrências em `<i>et al.</i>` (Martins p1, ambos slides Martins do bloco final, INTRO-03a corpo, INTRO-03a rodapé, e demais).
- **D-55 (3º parágrafo escopo):** O reviewer também pediu que o slide não terminasse no diagnóstico isolado de Shi 2022, mas abrisse para o motivo conceitual (domínios com respostas estruturadas). Solução: terceiro parágrafo lista programação, matemática, ciências, escrita, sem nomear Code-DKT (gate forte; fase 4). O argumento "a forma da resposta importa tanto quanto o resultado final" prepara INTRO-03b sem antecipar.

## Deviations from Plan

### Auto-fixed Issues (Rule 1 / scope expansion via 3 iterações pós-checkpoint)

**1. [Iteração pós-checkpoint — texto] Reescrita com fraseado do Report 4 + Shi 2022**
- **Found during:** Task 2 (checkpoint:human-verify)
- **Issue:** Reviewer humano avaliou o phrasing inicial como menos fiel ao Code-DKT.pdf e ao Report 4 do TCC (vocabulário "estrutura do código produzido" + "riqueza fica fora do modelo" era leitura autoral). O paper Shi 2022 diz literalmente "ignoring its content" (p.50) e o Report 4 enfatiza "tratam as respostas como corretas/incorretas".
- **Fix:** Reescrito segundo parágrafo do slide para "tratam as respostas dos estudantes apenas como corretas ou incorretas, ignorando seu conteúdo".
- **Files modified:** apresentacao/index.html
- **Verification:** Reviewer aprovou texto na iteração 2.
- **Committed in:** `53b46e8`

**2. [Iteração pós-checkpoint — narrativa] Ponte KT → trabalho → CSEDM**
- **Found during:** Task 2 (checkpoint:human-verify, segunda passada)
- **Issue:** A transição INTRO-01 (dataset) → INTRO-03a (crítica Shi) ficou abrupta. O slide INTRO-03a entrava direto em "Shi et al. apontam que..." sem situar KT nem ancorar no trabalho do TCC. Reviewer pediu parágrafo de abertura.
- **Fix:** Adicionado primeiro parágrafo: "Modelos de *knowledge tracing* estimam... No nosso trabalho, eles são o instrumento central para representar o aprendizado em programação a partir dos eventos do CSEDM."
- **Files modified:** apresentacao/index.html
- **Verification:** Reviewer aprovou narrativa na iteração 3.
- **Committed in:** `f7e042a`

**3. [Iteração pós-checkpoint — ABNT] `<i>et al.</i>` ABNT + sweep do deck**
- **Found during:** Task 2 (checkpoint:human-verify, terceira passada)
- **Issue:** Manual MSGQ-21.01 (apresentacao/) determina itálico em "et al." em pt-BR. O slide INTRO-03a tinha "Shi et al. (2022)" sem itálico (corpo + rodapé). Reviewer pediu correção. Auditoria revelou que outros 6 slides do deck também não usavam itálico em `et al.`, inclusive Martins p1 (que já estava no padrão padrão `> introdução` da fase 1).
- **Fix:** `<i>et al.</i>` aplicado em INTRO-03a (corpo + rodapé) E drive-by sweep nas demais 7 ocorrências do deck (Martins p1 corpo + rodapé, slide-code rodapé Shi, slide-kcfig rodapé Duan, ambos Martins p2/p3 rodapé, slide-fig rodapé). 8 ocorrências totais normalizadas.
- **Files modified:** apresentacao/index.html
- **Verification:** Reviewer aprovou consistência tipográfica final; deck inteiro com `et al.` em itálico ABNT.
- **Committed in:** `4a9af6e`

---

**Total deviations:** 3 iterações pós-checkpoint (todas Rule 1 categoria "user feedback during human-verify gate")
**Impact on plan:** Plano original (1 commit Task 1 + checkpoint Task 2) virou 4 commits funcionais. Sem scope creep: o requirement INTRO-03 (metade diagnóstico) não mudou; o que mudou foi a qualidade do texto e a consistência ABNT, dentro do escopo do checkpoint humano. As 3 iterações são naturais para um slide que precisa equilibrar fidelidade ao paper, narrativa do TCC e padrão de citação.

## Issues Encountered

Nenhum. As 3 iterações são feedback estruturado do reviewer humano em checkpoint, não issues técnicos.

## Auth Gates

Nenhum.

## Self-Check: PASSED

- `git log --oneline --all | grep 6f0ae3d` → FOUND
- `git log --oneline --all | grep 53b46e8` → FOUND
- `git log --oneline --all | grep f7e042a` → FOUND
- `git log --oneline --all | grep 4a9af6e` → FOUND
- `grep -c '>o problema do kt binário<' apresentacao/index.html` → 1 (cabeçalho D-34b)
- `grep -c 'Fonte: Shi <i>et al.</i>' apresentacao/index.html` → 1 (rodapé ABNT)
- `awk '/SLIDE · INTRO-03a/,/<\/section>/' apresentacao/index.html | grep -ci 'code-dkt'` → 0 (gate D-36)

## Next Phase Readiness

- **INTRO-03 ainda PARCIAL:** metade diagnóstico entregue (INTRO-03a); falta INTRO-03b ("sinal pedagógico perdido") no plan 02-04 para fechar requirement INTRO-03 do ROADMAP.
- **STYLE.md fix (D-32) pendente:** linha 129 ainda diz "Após `> introdução` (slide 3)..."; será corrigida no plan 02-04 Task 2.
- **Padrão `<i>et al.</i>` ABNT:** trava precedente para fase 2 plan 02-04 e fases 3-5; novo texto que mencione "et al." deve usar `<i>`.
- **Voz híbrida ponte → crítica → escopo:** padrão para slides INTRO que apresentem crítica/diagnóstico de literatura; aplicar ao INTRO-03b consequência se ficar abrupto.

---
*Phase: 02-intro-dataset-e-problema-fase-1-edm*
*Plan: 02-03 (INTRO-03a)*
*Completed: 2026-05-27*
