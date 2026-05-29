---
phase: 04-modelagem-e-avalia-o-fase-3-edm
plan: 01
subsystem: apresentacao
tags: [reveal.js, html, abnt, ast, code-dkt, shi-2022]

requires:
  - phase: 01-reformata-o-da-base
    provides: ".slide-related template, .deck-topic header pattern, slide-code section preservado"
  - phase: 02-intro-dataset-e-problema-fase-1-edm
    provides: "INTRO-03a/b problema do KT binário (gancho narrativo que MODEL-01 fecha)"
  - phase: 03-eda-e-pr-processamento-fase-2-edm
    provides: "MARKER-02 (Preparação dos Dados ✓), .eda-source pattern (Arial 14px cinza), padrão ABNT de fonte sob figuras"

provides:
  - "MODEL-01a (#/16): slide '> o modelo escolhido' com justificativa em 1ª pessoa do plural (Shi et al., 2022) + cronologia horizontal BKT/DKT/Code-DKT em 3 marcadores"
  - "MODEL-01b (#/17): slide '> dentro do code-dkt' com 1 frase mecânica + pipeline esquerda-alinhado com setas (javalang → AST → code2vec → atenção → LSTM) + AST limpa (max 460px) com título ABNT en-dash e Fonte Arial 14px cinza"
  - "Asset apresentacao/assets/ast_codedkt_ptbr.svg (cópia trimada do docs/figures/, viewBox 0 0 560 410, legenda 'Figura 2:' embutida removida)"

affects: ["04-02 MODEL-04", "04-03 MODEL-05", "04-05 MARKER-03 (slot final do deck)"]

tech-stack:
  added: ["en-dash &ndash; em títulos de figura ABNT (consistente com .eda-grid)"]
  patterns:
    - "Slides 'narrativa em 1 paragrafo + visualizacao' em vez de 'corpo bullets + inset' (rejeitado durante checkpoint)"
    - "Cronologia horizontal com marcadores de ano + dot + autor + descrição (sem chips de bridge-seq) como template reaproveitável para slides historiográficos"
    - "Pipeline esquerda-alinhado com setas e label inline (`<b><i>Pipeline</i> Code-DKT:</b> a → b → c`) em vez de .bridge-seq com chips"
    - "SVG trimado: remoção de legenda embutida do paper + ajuste de viewBox preservando proporção dos nós/arestas"

key-files:
  created:
    - "apresentacao/assets/ast_codedkt_ptbr.svg (4302 → ~3900 bytes; viewBox 0 0 560 410)"
    - ".planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-01-SUMMARY.md"
  modified:
    - "apresentacao/index.html (+121 linhas; 2 novas <section>; 21 → 23 sections totais)"

key-decisions:
  - "D-79g (ad-hoc): MODEL-01 split em 2 slides (MODEL-01a + MODEL-01b) durante checkpoint para reduzir densidade. PLAN.md original previa 1 slide; planejamento estourou densidade conceitual aceitável."
  - "D-79h (ad-hoc): cronologia horizontal sem chips (rejeitado .bridge-seq). Razão: chips comprimiam descrições e quebravam a leitura narrativa esquerda→direita."
  - "D-79i (ad-hoc): pipeline mecânico volta a setas (em vez de prosa) para usar uma linha só. Esquerda-alinhado para casar com a sentença narrativa acima."
  - "D-79j (ad-hoc): SVG da AST trimado em vez de wrapper externo. Razão: a legenda 'Figura 2:' embutida no SVG estava em pt-BR mas pertencia ao paper de origem (não nosso), e a substituição por título ABNT externo deixa o slide consistente com o restante do deck."
  - "D-79k (ad-hoc): header MODEL-01a vira `> o modelo escolhido` (escolha pragmática do user durante iteração) em vez de `> como funciona o code-dkt` (PLAN.md original) ou `> como o code-dkt funciona` (alternativa intermediária)."

patterns-established:
  - "Timeline horizontal de papers: grid 3 colunas + line absoluta no topo (border 2px preto) + dots por marker (último em azul UniFacens para destacar a escolha)"
  - "Figura ABNT em slide-related: `Figura – Descrição` (16px bold centralizado) + img max 460px + `Fonte: ...` (14px cinza .eda-source style)"

requirements-completed: [MODEL-01, MODEL-03]

duration: 90min
completed: 2026-05-28
---

# Phase 04, Plan 01: MODEL-01 — O modelo escolhido + dentro do Code-DKT

**Slide MODEL-01 dividido em 2 slides durante o checkpoint visual (MODEL-01a + MODEL-01b), entregando a justificativa da escolha do Code-DKT, a linha do tempo BKT→DKT→Code-DKT em formato horizontal sem chips, e a mecânica interna (pipeline + AST inset) em slide separado.**

## Performance

- **Duration:** ~90min (com 5 iterações de design + 1 checkpoint visual humano)
- **Started:** 2026-05-28 (sessão atual, pós-fase 3)
- **Completed:** 2026-05-28
- **Tasks:** 4 do PLAN.md + 5 iterações intermediárias de design
- **Files modified:** 2 (apresentacao/index.html + apresentacao/assets/ast_codedkt_ptbr.svg)

## Accomplishments

- 2 slides funcionais (MODEL-01a #/16 + MODEL-01b #/17) substituem o slide único do PLAN.md, reduzindo densidade conceitual sem sacrificar conteúdo
- Cronologia BKT (Corbett e Anderson, 1995) → DKT (Piech et al., 2015) → Code-DKT (Shi et al., 2022) em linha do tempo horizontal com último marcador em azul UniFacens destacando a escolha
- Pipeline mecânico explícito (javalang → AST → code2vec → atenção → LSTM) esquerda-alinhado abaixo da frase conceitual em #/17
- AST do paper Shi et al. (2022) renderizada como figura ABNT (título com en-dash + fonte cinza 14px) em vez de inset com legenda interna; SVG trimado para tirar a legenda original e ajustar viewBox

## Task Commits

1. **Tasks 1+2 (consolidadas): copy + trim do SVG + inserção de 2 sections** — `4f2bc3f` (feat: apresentacao)
2. **Task 3: checkpoint visual humano** — 5 iterações textuais + 1 split estrutural; aprovado em v5d
3. **Task 4: commit funcional** — `4f2bc3f` (mesmo commit; SUMMARY pending neste arquivo)

**Plan metadata:** SUMMARY.md neste commit; STATE.md + ROADMAP.md atualizados pelo orquestrador no commit seguinte.

## Files Created/Modified

- `apresentacao/index.html` — +121 linhas; 2 novas `<section>` inseridas entre MARKER-02 (#/15) e slide-code (que desloca para #/18); 21 → 23 sections totais
- `apresentacao/assets/ast_codedkt_ptbr.svg` — cópia local trimada do `docs/figures/ast_codedkt_ptbr.svg`: viewBox `0 0 560 620` → `0 0 560 410`, legenda interna "Figura 2: Uma AST simples..." (lines 65-73 originais) removida

## Deviations from PLAN.md

| PLAN.md original | Realidade |
| --- | --- |
| 1 slide MODEL-01 com `.bridge-seq` 3-chip cronologia + 2 colunas (texto + AST inset) | 2 slides (#/16 escolha + timeline horizontal; #/17 mecânica + AST como figura ABNT centralizada) |
| Header `> como o code-dkt funciona` | `> o modelo escolhido` (#/16) + `> dentro do code-dkt` (#/17) |
| Sections 21 → 22 | Sections 21 → 23 (+2) |
| 4 tasks + 1 commit | 4 tasks + 5 iterações de design no checkpoint + 1 commit |
| AST como inset à direita do texto, max 420px | AST como figura centralizada protagonista, max 460px, em slide próprio |
| Rodapé Fonte único `.rel-cite` | Fonte da figura no estilo `.eda-source` (14px cinza), sem rodapé Fonte de slide |

**Razão estrutural do split:** durante o checkpoint visual, ficou claro que a combinação `cronologia + justificativa + 4 bullets do pipeline + AST` em 1 slide exigia comprimir tudo ao ponto de quebrar a hierarquia visual. Split em 2 slides permite que cada um respire (~12-14 elementos vs ~6-8) e mantém o discurso narrativo: primeiro JUSTIFICAR a escolha + situar na cronologia, depois DETALHAR a mecânica.

## Next Steps

- Plan 04-02 (Wave 2): MODEL-04 — tabela ABNT `.eda-grid` 4 modelos × 5 assignments vs Shi (D-78g números travados)
- Plan 04-03 (Wave 3): MODEL-05 — pipeline 5 etapas (Duan et al., 2025)
- Plan 04-04 (Wave 4): CLOSE-03 + PENDING-04 — pick visual do gráfico Code-DKT
- Plan 04-05 (Wave 5): MARKER-03 — pill 4 running + STYLE.md inventário pós-fase 4

## Lessons Learned

1. **Design density gate:** slides com 5+ elementos heterogêneos (cronologia + texto + lista + figura + rodapé) sinalizam split. Catch via checkpoint visual em vez de presumir no plan.
2. **Iteração textual ≠ rework estrutural:** as primeiras 3 iterações foram microcópia (header, abertura, etc.); a iteração 4 foi estrutural (split). Distinguir antes de iterar evita perder o sinal forte ("está tudo jogado" = sinal estrutural, não tipográfico).
3. **En-dash em título de figura é OK:** o gate "sem em-dash" do projeto se aplica a prosa; títulos ABNT de figura/tabela usam en-dash como separador title-descrição (consistente com `.eda-grid`).
4. **SVGs do paper precisam de cuidado dual-language:** o SVG vinha com "Figura 2:" embutida (pt-BR, mas pertencendo ao paper). Trim cirúrgico do SVG + título externo deixa o slide consistente com o resto do deck e evita citação numérica embutida do paper que não corresponde à nossa numeração.
