---
phase: 04-modelagem-e-avalia-o-fase-3-edm
plan: 02
subsystem: apresentacao
tags: [reveal.js, html, abnt, eda-grid, tabela, code-dkt, shi-2022]

requires:
  - phase: 04-modelagem-e-avalia-o-fase-3-edm
    provides: "Plan 04-01 (MODEL-01a/01b) entregue; slide-code desloca para #/18, slide-kcfig para #/20"
  - phase: 03-eda-e-pr-processamento-fase-2-edm
    provides: "Componente .eda-grid + .eda-source + .eda-title (CSS L460-490) já validados em EDA-01"

provides:
  - "MODEL-04 (#/18 após inserção): slide '> code-dkt no csedm' com tabela ABNT .eda-grid 4 modelos × 5 assignments + caption explicando first-attempt AUC + rodapé Fonte ABNT"
  - "Números canônicos D-78g (multirun 10 seeds) transcritos com vírgula decimal pt-BR; 4 células Shi em &ndash; (paper só publica A1=A439=75,74%)"

affects: ["04-03 MODEL-05 (vem depois)", "04-04 CLOSE-03", "04-05 MARKER-03"]

tech-stack:
  added: []
  patterns:
    - "Tabela ABNT em slide-related: reuso direto do .eda-grid sem CSS novo, mesmo padrão de EDA-01"
    - "Caption discreto pós-tabela (.rel-lead font-size:18px) para nota explicativa abaixo do dado, sem competir visualmente com a tabela"

key-files:
  created:
    - ".planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-02-SUMMARY.md"
  modified:
    - "apresentacao/index.html (+28 linhas; 1 nova <section>; 23 → 24 sections totais)"

key-decisions: []

patterns-established:
  - "Tabela 2 (a primeira foi EDA-01 'Tabela 1') segue numeração crescente ABNT consistente no deck"
  - "En-dash &ndash; em células sem dado quando o paper de referência não publica esse campo (em vez de deixar branco ou marcar 'N/A')"

requirements-completed: [MODEL-04]

duration: 8min
completed: 2026-05-28
---

# Phase 04, Plan 02: MODEL-04 — Code-DKT no CSEDM

**Slide MODEL-04 entregue inline (autonomous=true) com tabela ABNT .eda-grid comparando BKT/DKT/Code-DKT/Shi(2022) por assignment; números D-78g exatos com vírgula decimal pt-BR.**

## Performance

- **Duration:** ~8min (autonomous, sem checkpoint humano por design do plan)
- **Started:** 2026-05-28 ~22:50 BRT
- **Completed:** 2026-05-28 ~22:58 BRT
- **Tasks:** 2/2 (insert section + smoke test http.server)
- **Files modified:** 1 (apresentacao/index.html)

## Accomplishments

- Tabela ABNT funcional em #/18 com 4 modelos × 5 assignments (A439, A487, A492, A494, A502)
- Code-DKT vence DKT em 4/5 assignments (A487 +2,86pp, A492 +4,07pp, A494 +1,68pp, A502 +4,20pp); A439 -2,29pp é a inversão conhecida da memória `project_multirun_results`
- Code-DKT A439=73,27% versus Shi (2022) Table 2 A1=75,74% → delta -2,47pp (dentro da margem ±3pp do CLAUDE.md "Critérios de Conclusão" item 1)
- Caption explicita first-attempt AUC como métrica primária e linka §5 do paper Shi; rodapé "elaborado pelo autor (10 seeds); Shi et al. (2022) Table 2." padrão ABNT

## Task Commits

1. **Task 1: insert section MODEL-04 + acceptance criteria** — `7a9ae9a` (apresentacao)
2. **Task 2: smoke test http.server + functional commit** — `7a9ae9a` (mesmo commit, autonomous)

**Plan metadata:** SUMMARY.md + STATE.md + ROADMAP.md no próximo commit (docs).

## Files Created/Modified

- `apresentacao/index.html` — +28 linhas; 1 nova `<section>` inserida entre slide-code (`</section>` linha 483 antes do plan) e slide-kcfig (`<!-- SLIDE · KCs semânticos extraídos -->` linha 485 antes do plan); 23 → 24 sections totais; slide-kcfig desloca de #/19 para #/19 (a inserção fica antes dele, então passa a ser #/20)

## Acceptance Criteria — Resultado

| Check | Esperado | Real | Status |
| --- | --- | --- | --- |
| sections | +1 vs HEAD (=24) | 24 | ✓ |
| grep 'code-dkt no csedm' | ≥1 | 1 | ✓ |
| grep 'MODEL-04' | ≥1 | 1 | ✓ |
| eda-grid tables | =2 | 2 | ✓ |
| 73,27 (Code-DKT A439) | ≥1 | 1 | ✓ |
| 75,74 (Shi A439) | ≥1 | 1 | ✓ |
| 75,56 (DKT A439) | ≥1 | 1 | ✓ |
| 63,21 (BKT A439) | ≥1 | 1 | ✓ |
| Shi <i>et al.</i> (2022) | aumentar ≥2 | 9 total (delta +2) | ✓ |
| ponto decimal na region MODEL-04 | 0 | 0 | ✓ |
| em-dash na region MODEL-04 | 0 | 0 | ✓ |
| &ndash; na region MODEL-04 | ≥5 | 5 (1 título + 4 células Shi) | ✓ |
| rodapé Fonte canônico | =1 | 1 | ✓ |
| HTTP 200 em index.html | sim | sim (porta 8003) | ✓ |

## Deviations from PLAN.md

- Smoke test rodou na porta 8003 em vez de 8000 (8000/8001/8002 ainda ocupados de tentativas anteriores). Substância idêntica; sem impacto no commit ou no resultado.
- Nenhum desvio textual ou estrutural; PLAN.md seguido literalmente.

## Next Steps

- Wave 3 (plan 04-03 MODEL-05): pipeline 5 etapas Duan et al. (2025), entre MODEL-04 e slide-kcfig. autonomous=false (checkpoint visual previsto).
- Wave 4 (plan 04-04 CLOSE-03 + PENDING-04): pick visual de 4 PNGs candidatos. autonomous=false.
- Wave 5 (plan 04-05 MARKER-03): pill 4 running + STYLE.md inventário pós-fase 4. autonomous=false.

## Lessons Learned

- Plans `autonomous=true` com números pré-validados (D-78g) são rápidos quando o reviewer já assinou os valores no CONTEXT. Tempo médio ~8min vs ~90min do plan 04-01 com checkpoint visual.
- Acceptance criteria com regex devem ser scoped (via `awk` na region do slide) — checagem global de "ponto decimal" pega coordenadas SVG da marca d'água Facens (`70.51`, `76.92`, etc.) e gera falsos positivos.
- Linha `Shi (2022)*` em ABNT com asterisco + nota explicativa funciona bem para tabelas comparativas onde nem todas as colunas existem no paper de referência.
