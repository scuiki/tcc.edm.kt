---
phase: 04-modelagem-e-avalia-o-fase-3-edm
plan: 03
subsystem: apresentacao
tags: [reveal.js, html, abnt, bridge-seq, pipeline, duan-2025, kcs]

requires:
  - phase: 04-modelagem-e-avalia-o-fase-3-edm
    provides: "Plans 04-01 e 04-02 entregues; slide-kcfig agora em #/20 após inserção"
  - phase: 03-eda-e-pr-processamento-fase-2-edm
    provides: "Componentes .eda-title + .eda-source para padrão ABNT de figura"

provides:
  - "MODEL-05 (#/19): slide '> extração automática de kcs' com pipeline horizontal de 5 caixas (Sampling n=5 → LLM → Clustering → Rotulagem → Q-matrix) tratado como Figura ABNT (título + fonte) + parágrafo explicativo sobre por que extraímos KCs das respostas corretas no CSEDM"
  - "Citação Duan et al. (2025) na frase de abertura (não na última, como originalmente)"

affects: ["04-04 CLOSE-03", "04-05 MARKER-03"]

tech-stack:
  added: []
  patterns:
    - "Pipeline ABNT: tratamento de pipeline horizontal como figura científica com .eda-title acima e .eda-source abaixo (em vez de rodapé .rel-cite)"
    - "Caixas .bridge-seq com 2 linhas verticais via flex-direction: column inline override (verbo em cima, descrição abaixo)"
    - "Preto puro #000 em todos os elementos do pipeline (texto, bordas, setas, título) via inline-style override por economia (sem CSS novo)"

key-files:
  created:
    - ".planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-03-SUMMARY.md"
  modified:
    - "apresentacao/index.html (+27 linhas; 1 nova <section>; 24 → 25 sections totais)"

key-decisions:
  - "D-79l (ad-hoc): rejeição do fallback CSS .bridge-seq--narrow durante checkpoint. Tentativa 1 (font 17px inline) cortou texto, tentativa 2 (.bridge-seq--narrow com font 16px) ainda cortou. Solução final: 2 linhas verticais por caixa com flex-direction column + microcópia mais curta (`Sentence-BERT` em vez de `Sentence-BERT + HAC`; `nos clusters` em vez de `LLM nos clusters`)."
  - "D-79m (ad-hoc): Duan et al. (2025) movido para frase de abertura ('baseado em Duan et al. (2025)') e fonte ABNT da figura ('elaborado pelo autor; adaptado de Duan et al. (2025)') em vez do PLAN.md original que tinha Duan na frase de fechamento + rodapé .rel-cite."
  - "D-79n (ad-hoc): substituição da frase de fechamento 'A decisão-chave foi alimentar o LLM com código bruto, não AST' por explicação narrativa sobre por que extraímos KCs das respostas corretas (CSEDM tem só respostas sem enunciados; vários caminhos para acertar → amostragem n=5)."
  - "D-79o (ad-hoc): pipeline tratado como Figura ABNT (.eda-title + .eda-source) em vez de elemento decorativo solto."
  - "D-79p (ad-hoc): cores preto puro #000 em todo o pipeline (texto, bordas, setas, título) via inline-style override em vez de criar nova classe CSS."
  - "D-79q (ad-hoc): 'Knowledge Components' → 'knowledge components' tudo minúsculo (termo estrangeiro em itálico)."

patterns-established:
  - "Pipeline como Figura ABNT no deck: título acima + .bridge-seq + .eda-source abaixo"
  - "Caixas .bridge-seq verticais (flex-direction: column): override inline em vez de variante de classe; mantém CSS limpo"
  - "Preto puro #000 para emphasis visual em elementos diagramáticos quando #1f1f1f não destaca o suficiente"

requirements-completed: [MODEL-05]

duration: 35min
completed: 2026-05-28
---

# Phase 04, Plan 03: MODEL-05 — Extração automática de KCs

**Slide MODEL-05 entregue com pipeline horizontal de 5 caixas (Sampling n=5 → LLM → Clustering → Rotulagem → Q-matrix) tratado como figura ABNT + parágrafo explicativo sobre por que extraímos KCs das respostas corretas no CSEDM; Duan et al. (2025) citado na abertura.**

## Performance

- **Duration:** ~35min (4 iterações de design durante checkpoint, incluindo rejeição do fallback CSS narrow)
- **Started:** 2026-05-28 ~23:10 BRT
- **Completed:** 2026-05-28 ~23:45 BRT
- **Tasks:** 4 do PLAN.md (1 inserção + 1 checkpoint + 1 fallback CSS rejeitado + 1 commit) → reduzido a 3 (1 inserção + 1 checkpoint com 4 iterações + 1 commit)
- **Files modified:** 1 (apresentacao/index.html)

## Accomplishments

- Pipeline horizontal funcional em #/19 sem fallback CSS (rejeitado em favor de redesign com 2 linhas verticais por caixa + microcópia mais curta)
- Frase de abertura cita Duan et al. (2025) explicitamente, integrando a referência ao argumento de adoção
- Parágrafo final explica a decisão metodológica de extrair KCs das respostas corretas (CSEDM tem só respostas sem enunciados; n=5 amostragem para cobrir caminhos alternativos)
- Pipeline tratado como Figura ABNT (.eda-title + .eda-source), consistente com tabela do MODEL-04

## Task Commits

1. **Task 1+2+3 consolidados: insert section + checkpoint + fallback rejeitado** — `f093a9b` (apresentacao)
2. **Task 4: commit funcional** — `f093a9b` (mesmo commit)

**Plan metadata:** SUMMARY.md + STATE.md + ROADMAP.md no próximo commit.

## Files Created/Modified

- `apresentacao/index.html` — +27 linhas; 1 nova `<section>` MODEL-05 entre MODEL-04 (linha 511 pós-04-02, agora desloca) e slide-kcfig (que vira #/20); 24 → 25 sections totais

## Design Iterations During Checkpoint

1. **v1 (PLAN.md literal):** 5 caixas com font 17px + `<br>` simples + frase de fechamento sobre código bruto vs AST + rodapé Duan no `.rel-cite`. → Texto cortado dentro das caixas (Pitfall 7 confirmado).
2. **v2 (fallback CSS `.bridge-seq--narrow`):** font 16px + padding 14px 12px + gap 6px. → Ainda cortava texto. CSS reverted (não comprometido).
3. **v3 (redesign):** Duan na abertura; pipeline como figura ABNT; parágrafo explicativo final substituindo "código bruto vs AST"; "knowledge components" minúsculo. → Caixas ainda renderizavam em 2 colunas em vez de 2 linhas (flex row direction).
4. **v4 final aprovada:** flex-direction column inline; verbo+descrição empilhados verticalmente; cores preto puro #000 em texto, bordas, setas, título.

## Deviations from PLAN.md

| PLAN.md original | Realidade |
| --- | --- |
| Frase de fechamento "decisão-chave foi código bruto, não AST" | Substituída por parágrafo explicativo sobre extração de KCs das respostas corretas (CSEDM sem enunciados; n=5 amostragem) |
| Duan et al. (2025) na fechamento + rodapé `.rel-cite` | Duan na abertura + Fonte ABNT da figura (`elaborado pelo autor; adaptado de Duan et al., 2025`) |
| Pipeline solto + rodapé .rel-cite | Pipeline como Figura ABNT com `.eda-title` acima + `.eda-source` abaixo |
| 2 linhas por caixa via `<br>` simples + bold verb | 2 linhas via flex-direction column inline (caixas renderizavam em 2 colunas com `<br>` em row) + sem bold (cor preto puro) |
| Fallback CSS `.bridge-seq--narrow` opcional | Rejeitado; redesign com microcópia mais curta resolveu (`Sentence-BERT + HAC` → `Sentence-BERT`; `LLM nos clusters` → `nos clusters`) |
| Knowledge Components em maiúscula | knowledge components minúsculo (termo estrangeiro em itálico) |

## Next Steps

- Wave 4 (plan 04-04 CLOSE-03 + PENDING-04): pick visual de 4 PNGs candidatos. autonomous=false, checkpoint visual.
- Wave 5 (plan 04-05 MARKER-03): pill 4 running + STYLE.md inventário pós-fase 4. autonomous=false, checkpoint final.

## Lessons Learned

1. **Flex `<br>` armadilha:** `display: flex` em row direction trata children como itens horizontais; `<br>` entre eles não cria quebra de linha visual — children ficam em colunas. Para multi-linha em flex item, usar `flex-direction: column` no container OU `display: block` num wrapper interno.
2. **Microcópia vence CSS apertado:** quando texto corta, encurtar conteúdo (4 chars salvos por palavra × 5 caixas = ~80px) costuma resolver melhor que apertar font/padding (que sacrifica legibilidade).
3. **ABNT figura > rodapé .rel-cite:** elementos visuais diagramáticos (pipeline, AST) ganham peso narrativo quando tratados como Figura formal (título + fonte), além de manter consistência ABNT.
4. **Preto puro #000 ≠ #1f1f1f ≠ #111317:** em diagramas com bordas finas e setas, #000 transmite mais peso visual que os tons "ink" do tema (que são para corpo de prosa).
