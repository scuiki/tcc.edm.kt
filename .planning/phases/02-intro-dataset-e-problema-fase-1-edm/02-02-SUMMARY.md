---
phase: 02-intro-dataset-e-problema-fase-1-edm
plan: 02
subsystem: presentation
tags: [reveal-js, intro-slide, dataset, csedm, progsnap2, phase2-edm, abnt]

# Dependency graph
requires:
  - phase: 02-intro-dataset-e-problema-fase-1-edm/02-01
    provides: "Section MARKER-01 inserido após Yağcí em index.html; serve de âncora inferior para INTRO-01."
provides:
  - "Section INTRO-01 (slide `> o dataset csedm`) em apresentacao/index.html, posicionado entre Yağcí (#/6) e MARKER-01 (deslocado para #/8)"
  - "Phrasing-âncora do dataset CSEDM: voz 1ª pessoa do plural, citação parentética (Price, 2020), rodapé canônico Fonte: Price (2020); CSEDM 2021."
  - "Granularidade ampliada (vs PLAN): 5 assignments com 50 problemas e Spring 2019 explícito; 6 colunas-chave do ProgSnap2 listadas (SubjectID, ProblemID, EventType, Score, ServerTimestamp, CodeStateID)"
affects: [02-03, 02-04, 03, 04]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Reuso direto do template .slide-related + .rel-lead + .rel-cite (sem CSS novo)"
    - "Padrão > [seção] em .deck-topic + caret blink (D-42)"
    - "Stats inline em .rel-lead.intro-stats-line e features inline em .rel-lead.intro-cols-line (classes cosméticas extras, herdam .rel-lead sem CSS novo)"

key-files:
  created: []
  modified:
    - "apresentacao/index.html (linhas 149-164: section INTRO-01)"

key-decisions:
  - "Formato dos números: opção C do RESEARCH (413 estudantes, 50 problemas, 201 mil eventos) — pt-BR, sem separador decimal de milhar"
  - "D-50 (ad-hoc, registrada neste plan): granularidade '5 assignments com 50 problemas' acrescentada via feedback do checkpoint; não estava no PLAN original"
  - "D-51 (ad-hoc, registrada neste plan): lista de 6 colunas-chave do ProgSnap2 (SubjectID, ProblemID, EventType, Score, ServerTimestamp, CodeStateID) acrescentada via feedback do checkpoint; reforça que ProgSnap2 não é só um nome, é uma estrutura de evento+contexto"
  - "Fraseado do período de coleta: 'coletado durante a primavera de 2019 e divulgado na competição CSEDM 2021' (após 2 iterações: 'coleta de 2019' → 'coleta da primavera de 2019' → fraseado final)"

patterns-established:
  - "Iteração pós-checkpoint legítima: ajustes de microcópia (não estrutural) feitos APÓS aprovação visual do reviewer ficam como commits adicionais do mesmo plan, documentados como decisões ad-hoc no SUMMARY"
  - "Classes cosméticas extras (.intro-stats-line, .intro-cols-line) que apenas herdam .rel-lead sem CSS novo são aceitáveis para diferenciar parágrafos semanticamente"

requirements-completed: [INTRO-01]

# Metrics
duration: ~17min
completed: 2026-05-27
---

# Phase 02 Plan 02: INTRO-01 (slide "o dataset csedm") Summary

**Slide INTRO-01 inserido em apresentacao/index.html (linhas 149-164) apresentando o CSEDM em ProgSnap2 com 3 números brutos do MainTable Spring 2019 (413 estudantes, 5 assignments com 50 problemas, 201 mil eventos); rodapé canônico `Fonte: Price (2020); CSEDM 2021.`**

## Performance

- **Duration:** ~17 min (3 commits: c362e9d 21:32 → e07e37b 21:37 → 3835336 21:39)
- **Started:** 2026-05-27T21:28:00Z (Task 1 validação Python)
- **Completed:** 2026-05-28T00:43:46Z (close do plan)
- **Tasks:** 3 (1 validação, 1 inserção, 1 checkpoint visual com 2 iterações)
- **Files modified:** 1 (apresentacao/index.html)

## Accomplishments

- Section INTRO-01 vivo no deck entre Yağcí (#/6) e MARKER-01 (deslocado para #/8); navegação reveal.js OK
- 3 números brutos do MainTable Spring 2019 validados (413 / 50 / 201570) e escritos no slide no formato pt-BR opção C ("201 mil eventos")
- Voz 1ª pessoa do plural ("Nosso dataset é o CSEDM..."), citação parentética `(Price, 2020)`, rodapé literal `Fonte: Price (2020); CSEDM 2021.`
- Após feedback do checkpoint, granularidade adicional ("5 assignments com 50 problemas", Spring 2019, 6 colunas-chave do ProgSnap2) acrescentada SEM quebrar o template `.slide-related` e SEM CSS novo
- Total de sections no deck: 14 (era 13 após plan 02-01; +1 com INTRO-01)

## Task Commits

Each task was committed atomically:

1. **Task 1: Validar números do dataset (D-38)** — validação Python (sem commit; verificação pré-implementação)
2. **Task 2: Inserir section INTRO-01 em apresentacao/index.html** — `c362e9d` (feat) — insere as 15 linhas iniciais do INTRO-01 (linhas 149-163 originalmente)
3. **Task 3: Validação visual no browser (checkpoint:human-verify)** — APPROVED após 2 iterações com ajustes adicionais:
   - **Iteração 1:** `e07e37b` (feat) — "primavera 2019, 5 assignments, colunas ProgSnap2" (adiciona .intro-cols-line e ajusta stats)
   - **Iteração 2:** `3835336` (fix) — "fraseado da coleta" (microajuste de prosa: "coletado durante a primavera de 2019 e divulgado")

**Plan metadata:** este SUMMARY + STATE/ROADMAP/REQUIREMENTS no commit `docs(02-02): record INTRO-01 close + tracking update`

## Files Created/Modified

- `apresentacao/index.html` — section INTRO-01 inserido entre as linhas 149 e 164 (15 linhas iniciais + 1 linha do `.intro-cols-line` adicionada na iteração 1, total 16 linhas no estado final)

## Decisions Made

### Decisões já no PLAN (D-31..D-46)
- D-31: section entre Yağcí (#/6) e MARKER-01 — OK
- D-34a: cabeçalho `> o dataset csedm` — OK
- D-35: voz 1ª pessoa do plural — OK
- D-38: números brutos do MainTable Spring 2019 (413/50/201 mil) — validados via pandas, OK
- D-42..D-46: padrões herdados da fase 1 — OK

### Decisões ad-hoc desta execução (registradas para histórico)

- **D-50 (ad-hoc, sub-feedback do checkpoint):** mencionar explicitamente os **5 assignments** quando citar os 50 problemas. Razão narrativa: o número "50 problemas" sozinho aparece como um pool monolítico, e o leitor da banca precisa entender que o curso CSEDM está estruturado em 5 unidades didáticas (assignments A439, A487, A492, A494, A502) com 10 problemas cada. Markup: `<b>413</b> estudantes, <b>5</b> assignments com <b>50</b> problemas, <b>201 mil</b> eventos.`

- **D-51 (ad-hoc, sub-feedback do checkpoint):** listar as **6 colunas-chave do ProgSnap2** num parágrafo dedicado. Razão narrativa: "armazenado em ProgSnap2" sem instanciar o esquema soa abstrato; explicitar SubjectID/ProblemID/EventType/Score/ServerTimestamp/CodeStateID mostra que ProgSnap2 é uma estrutura concreta de evento+contexto. Classe `.intro-cols-line` (cosmética, herda `.rel-lead`, sem CSS novo). `<code>` para os nomes das colunas distingue do prosa.

- **Microajuste de fluxo prosaico:** "coleta de 2019" → "coleta da primavera de 2019" (iteração 1) → "coletado durante a primavera de 2019 e divulgado na competição CSEDM 2021" (iteração 2). Sujeito implícito coerente (o dataset) ao longo da oração; substitui a justaposição "coleta..., divulgado..." que tinha sujeitos diferentes.

## Deviations from Plan

### Ajustes pós-checkpoint (feedback do reviewer, NÃO bugs)

O checkpoint humano em Task 3 aprovou o slide MAS solicitou ajustes adicionais. Esses ajustes foram aplicados como commits independentes do mesmo plan (não como bugs), porque (a) acrescentam **granularidade narrativa** sem violar nenhum gate do PLAN (cabeçalho LITERAL preservado, 3 números preservados, voz 1ª pessoa preservada, citação parentética preservada, rodapé LITERAL preservado, sem em-dash preservado), e (b) refletem decisão do reviewer (orientadora) sobre o que torna o slide mais útil para a banca.

**Iteração 1 (e07e37b) — granularidade dataset + colunas:**
- **Found during:** Task 3 (checkpoint visual no browser)
- **Mudanças:**
  - `coleta de 2019` → `coleta da primavera de 2019` (Spring 2019 explícito, casa com "Spring 2019" da memória `project_split_discovery`)
  - `<b>50</b> problemas` → `<b>5</b> assignments com <b>50</b> problemas` (granularidade pedagógica)
  - +1 parágrafo: `<p class="rel-lead intro-cols-line">Cada evento traz aluno (<code>SubjectID</code>), problema (<code>ProblemID</code>), tipo (<code>EventType</code>), nota (<code>Score</code>), timestamp (<code>ServerTimestamp</code>) e snapshot do código (<code>CodeStateID</code>).</p>`
- **Files modified:** apresentacao/index.html (+4, -2)
- **Verification:** ./CLAUDE.md "Dataset CSEDM — Fatos Críticos" confirma 5 assignments × 10 problemas e as 6 colunas; D-44 (sem em-dash) preservado; rodapé inalterado
- **Committed in:** `e07e37b`

**Iteração 2 (3835336) — fluxo prosaico:**
- **Found during:** após iteração 1, releitura no browser
- **Mudança:** `coleta da primavera de 2019, divulgado na competição CSEDM 2021` → `coletado durante a primavera de 2019 e divulgado na competição CSEDM 2021`
- **Razão:** sujeito implícito coerente (o dataset coleta-se, não "a coleta divulga-se")
- **Files modified:** apresentacao/index.html (+1, -1)
- **Verification:** D-44 (sem em-dash) preservado; semântica do fato inalterada (Spring 2019 + CSEDM 2021 ambos preservados)
- **Committed in:** `3835336`

---

**Total deviations:** 2 ajustes pós-checkpoint (não são bugs; são iterações de fidelidade narrativa solicitadas pelo reviewer humano no momento do checkpoint visual)
**Impact on plan:** zero scope creep. Nenhum gate do PLAN foi violado. Granularidade adicional fortalece a fidelidade científica do slide (assignments e colunas são fatos críticos do CSEDM, presentes no CLAUDE.md "Dataset CSEDM — Fatos Críticos"). Decisões D-50 e D-51 registradas acima para que fases futuras (EDA-01, EDA-02 da fase 3; MODEL-01..05 da fase 4) saibam que (a) o número "5 assignments × 10 problemas" já foi introduzido aqui e não precisa repetir, (b) as colunas ProgSnap2 já foram listadas aqui e não precisam repetir.

## Issues Encountered

Nenhum bug, nenhum bloqueador. O slide passou em todos os gates automatizados na primeira tentativa (Task 2); o checkpoint visual aprovou no primeiro round e o reviewer pediu ajustes incrementais que foram aplicados em 2 commits adicionais.

## User Setup Required

None — apresentação reveal.js estática, sem backend.

## Next Phase Readiness

**Plano 02-03 (INTRO-03a) está pronto para executar:**
- Âncora superior: INTRO-01 (linhas 149-164, recém-criado) ✓
- Âncora inferior: MARKER-01 (linhas 166-195) ✓
- Espaço de inserção: entre `</section>` do INTRO-01 (linha 164) e `<!-- ============ SLIDE · MARKER ` (linha 166)
- Após 02-03, MARKER-01 desloca de `#/8` para `#/9`
- Phrasing Shi (2022) já travado em 02-RESEARCH.md §1.1 e em 02-PATTERNS.md "INTRO-03a"
- Sem CSS novo necessário (reuso direto de `.slide-related` + `.rel-lead` + `.rel-cite`)

**Sem blockers para 02-03.** D-50 e D-51 (decisões ad-hoc desta execução) NÃO afetam 02-03 porque INTRO-03a fala de Shi (BKT/DKT), não do dataset.

## Self-Check

- [x] `apresentacao/index.html` linhas 149-164 contêm o INTRO-01 (`grep -n '>o dataset csedm<'` retornou linha 154) ✓
- [x] Commit `c362e9d` existe (`git log --oneline | grep c362e9d`) ✓
- [x] Commit `e07e37b` existe (iteração 1 pós-checkpoint) ✓
- [x] Commit `3835336` existe (iteração 2 pós-checkpoint) ✓
- [x] Total de sections no deck = 14 (`grep -cE '<section data-background-(color|gradient)' apresentacao/index.html` retornou 14) ✓

## Self-Check: PASSED

---
*Phase: 02-intro-dataset-e-problema-fase-1-edm*
*Plan: 02 (INTRO-01)*
*Completed: 2026-05-27*
