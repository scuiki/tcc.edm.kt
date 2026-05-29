---
phase: 04-modelagem-e-avalia-o-fase-3-edm
plan: 04
subsystem: apresentacao
tags: [reveal.js, html, abnt, close-03, pending-04, codedkt-curves, martins-2024]

requires:
  - phase: 04-modelagem-e-avalia-o-fase-3-edm
    provides: "Plans 04-01/02/03 entregues; slide-fig agora em #/24 (deslocado por insertions)"
  - phase: 01-reformata-o-da-base
    provides: "Martins p2/p3 reformatados (CLOSE-01/02); slide-fig reformatado para CLOSE-03"

provides:
  - "CLOSE-03 (#/24): PNG canônico `curves_by_martins` confirmado como pick visual; PENDING-04 resolvido"
  - "Comentário HTML linha 653 corrigido (Pitfall 9): aponta ao filename real `curves_by_martins.png` em vez do obsoleto `difficulty_martins.png`"
  - "Cobertura no-op de CLOSE-01 (Martins p2) + CLOSE-02 (Martins p3) confirmada via grep D-82"

affects: ["04-05 MARKER-03 (último plan da fase)"]

tech-stack:
  added: []
  patterns:
    - "Ciclo pick visual: inserir N candidatos temporários + checkpoint humano + cleanup (3 slides removidos do HTML + 3 PNGs removidos do disco) em um único plan"

key-files:
  created:
    - ".planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-04-SUMMARY.md"
  modified:
    - "apresentacao/index.html (apenas 1 linha alterada no comentário linha 653; 25 → 28 → 25 sections via insert+remove)"

key-decisions:
  - "Pick: 1 (curves_by_martins) — usuário manteve o gráfico atual após comparação visual dos 4 candidatos. Razão: 'Estruturas de controle aprende rápido; Vetores/Funções planos' é a leitura mais legítima e diretamente apoia o eixo prioritário Martins → Code-DKT. Os 3 candidatos rejeitados (difficulty_martins, kc_curves, level_vs_slope) ficam disponíveis em results/ para uso eventual no TCC 2."
  - "Fig-read atual ('Estruturas de controle parte do nível mais baixo mas tem a maior inclinação; Vetores e Funções ficam planos (mais difíceis de aprender)') mantido sem refraseio."

patterns-established:
  - "Pick visual com slides temporários numerados (slide-fig-pick-N) + cleanup em uma única passada"

requirements-completed: [CLOSE-01, CLOSE-02, CLOSE-03, PENDING-04]

duration: 10min
completed: 2026-05-28
---

# Phase 04, Plan 04: CLOSE-03 + PENDING-04 — pick visual mantém curves_by_martins

**PENDING-04 resolvido: usuário escolheu visualmente o candidato 1 (curves_by_martins) após comparar 4 PNGs candidatos; nenhuma alteração no PNG canônico; apenas correção do comentário HTML obsoleto (Pitfall 9). CLOSE-01/02 confirmados intactos via grep D-82.**

## Performance

- **Duration:** ~10min (ciclo inserir+checkpoint+cleanup)
- **Started:** 2026-05-28 ~23:50 BRT
- **Completed:** 2026-05-29 ~00:00 BRT
- **Tasks:** 4/4 (insert 3 temp slides + copy 3 PNGs + checkpoint pick + cleanup + commit)
- **Files modified:** 1 (apresentacao/index.html) — apenas 1 linha alterada (comentário); 3 PNGs temporários copiados e depois removidos

## Accomplishments

- PNG canônico `apresentacao/assets/fig-codedkt-martins-curves.png` validado visualmente como melhor opção entre os 4 candidatos
- Pitfall 9 resolvido: comentário HTML agora aponta corretamente a `curves_by_martins.png` (era `difficulty_martins.png` mas o `<img>` apontava ao outro PNG desde commit anterior)
- CLOSE-01/02 D-82 honrado: 0 linhas Martins p2/p3 modificadas em todo o plan
- Working tree limpo (3 PNGs temporários removidos do disco; 3 slides temporários removidos do HTML)

## Task Commits

1. **Task 1: copy 3 PNGs + insert 3 temp slides** — staged temporariamente (não commitado)
2. **Task 2: checkpoint humano (pick: 1)** — usuário escolheu candidato 1 (curves_by_martins atual)
3. **Task 3: cleanup + fix comentário** — staged
4. **Task 4: commit funcional** — `7e67b74` (1 linha alterada no comentário; 0 linhas em código)

**Plan metadata:** SUMMARY.md + STATE.md + ROADMAP.md no próximo commit.

## Files Created/Modified

- `apresentacao/index.html` — linha 653 atualizada (comentário HTML): `<!-- figura: results/fig_codedkt_difficulty_martins.png (curvas de mastery prevista; oportunidade = problema distinto) -->` → `<!-- figura: results/fig_codedkt_curves_by_martins.png (= assets/fig-codedkt-martins-curves.png; PENDING-04 resolved em 04-04) -->`. Diff total: 1 linha alterada (+1 / -1). Sections totais 25 (sem mudança líquida).

## Verification Results

| Check | Esperado | Real | Status |
| --- | --- | --- | --- |
| sections total | 25 | 25 | ✓ |
| pick slides remanescentes | 0 | 0 | ✓ |
| TEMP marker remanescente | 0 | 0 | ✓ |
| comentário obsoleto difficulty_martins.png | 0 | 0 | ✓ |
| comentário corrigido curves_by_martins | 1 | 1 | ✓ |
| PENDING-04 resolved marker | 1 | 1 | ✓ |
| Martins p2 cabeçalho `> retomando o problema` | ≥1 | 1 | ✓ |
| Martins p2 citação `p. 19` | ≥1 | 1 | ✓ |
| Martins p3 citação `p. 20` | ≥1 | 1 | ✓ |
| D-82 no-op (linhas Martins modificadas via git diff) | 0 | 0 | ✓ |
| PNG canônico fig-codedkt-martins-curves.png em disco | sim | sim (145673 B, MD5 8982...) | ✓ |
| 3 PNGs temp removidos do disco | sim | sim | ✓ |

## No-op Coverage Confirmed

- **CLOSE-01 (Martins p2):** linhas 608-629 (deslocadas pelos plans 04-01/02/03; estavam em ~498 antes). Cabeçalho `> retomando o problema` + citação direta literal `(Martins; Marin; Alves, 2024, p. 19)` + argumento "13 autores" intactos.
- **CLOSE-02 (Martins p3):** linhas 631-650. Cabeçalho idem + citação `p. 20` + argumento "10 autores" intactos.
- **slide-kcfig:** linhas 513-545 (saída do MODEL-05). Intacto, sem duplicação de KCs.
- **MODEL-03:** slide-code linha 437. Intacto (no-op desde 04-01).

## Next Steps

- Wave 5 (plan 04-05 MARKER-03): pill 4 (Implantação) em estado running, badge `[running]`, animação spin; atualizar STYLE.md §Inventário para refletir 26 sections finais e §Gaps reservados para fase 5.

## Lessons Learned

- **Pick visual com slides temporários funciona bem para PNGs determinísticos** (4 candidatos, escolha humana, cleanup atômico). Ciclo total: ~10min do início ao commit.
- **Pitfall 9 (comentário HTML inconsistente com `<img>`)** é silencioso: não quebra renderização, mas confunde leitura futura do código. Fix mecânico de 1 linha; impossível detectar via testes — só inspeção visual ou auditoria de assets.
- **D-82 (não tocar CLOSE-01/02)** é uma regra vinculante que merece verificação automatizada explícita (git diff filtrado por linhas Martins). Catch via grep antes do commit evita touch acidental.
