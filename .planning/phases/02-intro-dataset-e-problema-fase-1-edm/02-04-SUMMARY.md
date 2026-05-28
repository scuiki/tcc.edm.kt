---
phase: 02-intro-dataset-e-problema-fase-1-edm
plan: 04
subsystem: presentation
tags: [reveal-js, intro-slide, knowledge-tracing, shi-2022, style-doc, phase2-edm, abnt, close-phase]

# Dependency graph
requires:
  - phase: 02
    provides: "INTRO-01 (#/7 dataset CSEDM), INTRO-03a (#/8 problema do KT binário), MARKER-01 stub (#/10 progress bar 4 fases)"
provides:
  - "Section INTRO-03b em apresentacao/index.html linhas 183-198, slide #/9 do deck"
  - "Cabeçalho `> sinal pedagógico perdido` (D-34c) com caret piscando"
  - "Paráfrase autoral consequencial em 3 parágrafos (cenário concreto → consequência pedagógica → pivô para oportunidade) sem nomear Code-DKT"
  - "STYLE.md §Gaps reservados reescrito por inteiro (D-32 + RESEARCH §5.2)"
  - "Deck final: 16 sections (#/0 → #/15), fase 2 oficialmente fechada"
  - "INTRO-03 requirement completo (03a + 03b)"
affects: [02-CLOSE, 03-EDA, 03-EDA-02]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Reuso direto do template .slide-related + .rel-lead + .rel-cite (zero CSS novo)"
    - "Padrão > [seção] em .deck-topic + caret blink (D-42)"
    - "Padrão `<i>et al.</i>` ABNT já estabelecido em 02-03 mantido em INTRO-03b rodapé"
    - "Termo estrangeiro `<i>gap</i>` em itálico minúsculas (D-46 estendido)"

key-files:
  created: []
  modified:
    - "apresentacao/index.html (INTRO-03b inserido linhas 183-198; reescrita após iteração)"
    - "apresentacao/STYLE.md (§Gaps reservados, linhas 127-132 reescritas por inteiro)"

key-decisions:
  - "D-56: INTRO-03b inserido como section autônomo entre INTRO-03a (#/8) e MARKER-01 (deslocou para #/10); deck final 16 sections"
  - "D-57: cenário concreto em vez de citação direta (Report 4 do TCC inspirou voz). Após iteração com usuário, evolução de \"80% do código\" (número arbitrário) para \"acerta parte do código, mas erra em algum dos passos\" + observação técnica \"pode não compilar, ou compilar e estar errada\""
  - "D-58: termo estrangeiro `<i>gap</i>` em itálico minúsculas (D-46 estendido). Substitui \"Abre-se uma lacuna\" pelo padrão computacional \"Isso abre um <i>gap</i>\" mantendo `<i>knowledge tracing</i>` na mesma frase para consistência de tipografia"
  - "D-59: STYLE.md §Gaps reservados reescrito por inteiro (RESEARCH §5.2). Linha 129 obsoleta substituída + linha 130 ajustada para \"Após MARKER-01 e antes do trio Martins+fig\" porque agora MARKER-01 ocupa o gap"

patterns-established:
  - "Slide INTRO de consequência: 3 parágrafos (cenário → perda → pivô), sem nomear Code-DKT, sem citação parentética nova do autor já citado no slide anterior"
  - "Iteração textual pós-checkpoint legítima quando reviewer humano propõe fraseado específico: aplicar como novo commit do mesmo plan com micro-fixes ortográficos de Claude documentados em commit message"

requirements-completed: [INTRO-03]  # INTRO-03 fica fechado SOMENTE após este plan (03a entregou diagnóstico; 03b entregou consequência)

# Metrics
duration: "~80min (incluindo iteração textual pós-checkpoint visual + checkpoint final fim a fim)"
completed: 2026-05-27
---

# Phase 2 Plan 04: INTRO-03b (sinal pedagógico perdido) + STYLE.md fix + close fase 2 Summary

**Slide INTRO-03b inserido em apresentacao/index.html (linhas 183-198) como pivô consequencial: 3 parágrafos (cenário concreto de submissão parcialmente correta → perda pedagógica do sinal estrutural → `<i>gap</i>` entre KT clássico e o que pedagogicamente aconteceu), STYLE.md §Gaps reservados reescrito por inteiro, deck final navegado fim a fim (#/0 → #/15) com APPROVED do reviewer humano. Fase 2 oficialmente fechada.**

## Performance

- **Duration:** ~80 min (3 commits funcionais + 1 metadata; iteração textual pós-checkpoint do INTRO-03b)
- **Tasks:** 3 (1 auto INTRO-03b + iteração + 1 auto STYLE.md + 1 checkpoint:human-verify fim a fim APPROVED)
- **Files modified:** 2 (apresentacao/index.html, apresentacao/STYLE.md)

## Accomplishments

- Section INTRO-03b inserido entre INTRO-03a (#/8) e MARKER-01 (deslocou para #/10), slide acessível em `http://127.0.0.1:8000/#/9`
- Cabeçalho `> sinal pedagógico perdido` (D-34c) literal, com caret piscando, em Cascadia 24px cor `#5b6472`
- Paráfrase autoral em 3 parágrafos consequenciais:
  1. **Cenário:** "Considere o cenário em que um estudante resolvendo um problema acerta parte do código, mas erra em algum dos passos. Sua submissão pode não ser compilada, ou compilar e estar errada, mas de qualquer forma sua resposta é registrada como **incorreta**."
  2. **Perda pedagógica:** "Os modelos tratam essa tentativa de forma idêntica a uma **completamente errada**, e a previsão mais provável é de que o aluno não aprendeu nada do conteúdo abordado, mesmo tendo acertado parte da questão. O aprendizado parcial presente no código fica invisível."
  3. **Pivô:** "Isso abre um *gap* entre o que o *knowledge tracing* clássico enxerga e o que de fato aconteceu pedagogicamente. Essa lacuna motiva a criação de modelos sensíveis ao código submetido."
- Rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).` (D-45 + D-54)
- Code-DKT NÃO mencionado (gate forte; fase 4)
- Sem citação parentética nova de Shi no corpo (já citado em INTRO-03a)
- Sem em-dash, sem `<blockquote>`, sem `p. N` no rodapé
- STYLE.md §Gaps reservados reescrito por inteiro:
  - Linha 129 obsoleta `Após \`> introdução\` (slide 3): INTRO-01...` substituída por `Após \`> da edm ao knowledge tracing\` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).`
  - Linha 130 antiga (que dizia EDA após slide 6) ajustada para `Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3).`
- Total de sections no deck: **15 → 16** (INTRO-03b foi a 16ª section)
- Checkpoint fim a fim no browser APPROVED pelo reviewer humano

## Task Commits

Plan executado em 3 commits funcionais ao longo de uma iteração textual pós-checkpoint:

1. **Task 1 (versão inicial):** `c92b9ff` — `apresentacao: slide INTRO-03b - sinal pedagogico perdido` — Section inserido entre INTRO-03a e MARKER-01 com 3 parágrafos (cenário "80% do código" inspirado no Report 4 → perda pedagógica → "Abre-se uma lacuna" pivô). Total sections do deck: 15 → 16.

2. **Task 1 iteração (rewrite pós-feedback do usuário):** `6a70b7f` — `apresentacao: reescrever INTRO-03b com cenario expandido + gap` — Reescrita do slide com fraseado proposto pelo usuário durante o checkpoint visual:
   - Parágrafo 1: "80% do código" (número arbitrário) → "acerta parte do código, mas erra em algum dos passos"; adicionada observação técnica "pode não ser compilada, ou compilar e estar errada" cobrindo ambos os cenários de Compile.Error e Score parcial do CSEDM
   - Parágrafo 2: "O modelo trata" → "Os modelos tratam" (plural); "a maior parte" → "parte"; "embutido" → "presente"
   - Parágrafo 3: "Abre-se uma lacuna" → "Isso abre um `<i>gap</i>`" (termo estrangeiro em itálico, D-46 estendido); `<i>knowledge tracing</i>` mantido em itálico; quebra em 2 frases para fluxo melhor
   - Micro-fixes ortográficos aplicados por Claude em cima do texto proposto pelo usuário: "erra em algum um dos passos" → "erra em algum dos passos" (palavra "um" extra removida); "Essa lacuna que motiva..." → "Essa lacuna motiva..." (removido "que" para deixar a frase declarativa completa)
   - Bônus orgânico do mesmo commit: ajustes em INTRO-01 (parágrafo 1 reorganizado em 2 frases para legibilidade; stats "5 assignments com 50 problemas" → "5 assignments com 10 problemas cada, e 201 mil eventos" para granularidade aritmética explícita)

3. **Task 2:** `f4dde9c` — `docs(style): atualizar gaps reservados pos-fase 2` — STYLE.md §Gaps reservados reescrito por inteiro conforme RESEARCH §5.2. Frase obsoleta da linha 129 substituída; linha 130 (gap fase 3) ajustada para "Após MARKER-01"; demais linhas (fases 4 e 5) preservadas inalteradas.

4. **Task 3 (checkpoint:human-verify):** APPROVED pelo reviewer humano após a iteração textual (commit `6a70b7f`). Visual fim a fim do deck completo (#/0 → #/15) confirmado em browser por D-47. Reviewer aprovou: (a) INTRO-03b com layout coerente em 1280×720; (b) navegação reveal.js sem erro de console; (c) os 16 slides em sequência narrativa; (d) MARKER-01 em #/10 com primeira caixa em `--done`. Verifier subagent desabilitado por config (`workflow.verifier=false`); validação visual humana é o gate de saída.

**Plan metadata:** este SUMMARY + PHASE-SUMMARY + STATE/ROADMAP/REQUIREMENTS no commit `docs(phase-02): complete phase 2 — intro/dataset/problema (fase 1 EDM)`

## Files Created/Modified

### `apresentacao/index.html`
- **Tipo:** modificação (inserção + iteração textual).
- **INTRO-03b — Intervalo das linhas inseridas:** linhas **183-198** do arquivo final (16 linhas adicionadas; total do arquivo após plan: ~530 linhas).
- **Ponto de inserção verificado:** entre o `</section>` do INTRO-03a (linha 181) e o `<!-- ============ SLIDE · MARKER ` (linha 200). Linha 182 + 199 são linhas em branco como separadores.
- **Iteração textual (commit `6a70b7f`):** mesmo intervalo de linhas; 5 linhas substituídas (3 do INTRO-03b + 2 do INTRO-01).

### `apresentacao/STYLE.md`
- **Tipo:** modificação (reescrita do bloco "Gaps reservados para fases 2-5", linhas 127-132).
- **Linha 129 (substituída):** Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).
- **Linha 130 (ajustada):** Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3).
- **Linhas 131-132 (preservadas):** gaps das fases 4 e 5 inalterados.
- **Heading preservado:** `**Gaps reservados para fases 2-5:**`

## Decisions Made

### D-56 — INTRO-03b como section autônomo entre INTRO-03a e MARKER-01

INTRO-03 (requirement do ROADMAP) ficou dividido em 2 sub-slides: INTRO-03a (diagnóstico, plan 02-03) + INTRO-03b (consequência, este plan). O markup é 2 sections separados, não um único section com múltiplos parágrafos, porque (a) cada um tem seu próprio cabeçalho temático `> [seção]`, (b) separação dá ritmo à apresentação (10s + 30s + transição visual), (c) MARKER-01 fica imediatamente após o pivô consequencial, fechando a Fase 1 EDM em uma narrativa "problema → consequência → ✓".

### D-57 — Cenário concreto via Report 4, fraseado iterado com o usuário

A versão inicial (commit `c92b9ff`) usou "80% do código correto" inspirado no Report 4 do TCC. O reviewer apontou que "80%" é um número arbitrário sem ancoragem no dataset CSEDM (que tem `Score` parcial mas não 80% específico). O fraseado alternativo proposto pelo usuário: "acerta parte do código, mas erra em algum dos passos" + observação técnica "pode não ser compilada, ou compilar e estar errada, mas de qualquer forma sua resposta é registrada como incorreta". A observação técnica conecta com dois fatos do CSEDM (CLAUDE.md "Dataset CSEDM — Fatos Críticos"): (a) 30,27% dos eventos são `Compile.Error` (não-compilável → registrado como incorreto), (b) ~37% dos `Run.Program` têm Score parcial (0 < Score < 1, agrupado como `correct=0` quando `Score == 1.0` é o threshold de acerto). A frase "pode não compilar, ou compilar e estar errada" cobre ambos os casos sem precisar nomear os tipos de evento.

### D-58 — `<i>gap</i>` como termo estrangeiro (D-46 estendido)

O parágrafo 3 muda "Abre-se uma lacuna" (português) por "Isso abre um *gap*" (termo estrangeiro). Motivação: a frase imediatamente a seguir tem `<i>knowledge tracing</i>` em itálico (D-46 herdado de INTRO-03a); ter "lacuna" em português e "knowledge tracing" em itálico na mesma frase quebra a consistência tipográfica visual; itálico em ambos os termos estrangeiros (`<i>gap</i>` + `<i>knowledge tracing</i>`) reforça a marca computacional do slide. Trade-off: o uso de "gap" em vez de "lacuna" é decisão estilística (não estritamente ABNT); a frase final do parágrafo ainda usa "Essa lacuna motiva..." em português para amarrar com o sujeito pedagógico.

### D-59 — STYLE.md §Gaps reservados reescrito por inteiro

A frase obsoleta da linha 129 já mencionava INTRO-01/INTRO-03/MARKER-01 mas com posição errada (slide 3 em vez de slide 6). RESEARCH §5.2 (preparado pelo gsd-research na fase 2) sugeria reescrever o bloco inteiro para evitar uma segunda passada no STYLE.md ao iniciar a fase 3. Decisão: aplicar o bloco inteiro (linhas 127-132) substituindo a linha 129 + ajustando a linha 130, sem tocar nas linhas 131-132 (fases 4 e 5, ainda corretas). Resultado: a fase 3 lê o STYLE.md com "Após MARKER-01 e antes do trio Martins+fig" já consistente.

## Deviations from Plan

### 1. [Rule 1 — Iteração textual pós-checkpoint] Reescrita do INTRO-03b com cenário expandido + gap

- **Found during:** Task 3 (checkpoint:human-verify) — após o `c92b9ff` ser entregue, o reviewer humano abriu `#/9` no browser e propôs um fraseado mais rico, com o cenário ampliado para cobrir Compile.Error + Score parcial e com substituição de "Abre-se uma lacuna" por "Isso abre um `<i>gap</i>`".
- **Issue:** Versão inicial usava "80% do código correto" como número arbitrário; reviewer queria fraseado mais ancorado no dataset (cobrir Compile.Error + parcial) e a marca computacional `<i>gap</i>` em vez de "lacuna" no pivô.
- **Fix:** Reescrita do markup do INTRO-03b conforme proposta do usuário, com 2 micro-fixes ortográficos aplicados por Claude em cima ("algum um dos" → "algum dos"; "que motiva" → "motiva").
- **Files modified:** apresentacao/index.html (5 linhas: 3 do INTRO-03b + 2 do INTRO-01 ajustadas no mesmo commit como bônus orgânico do reviewer).
- **Verification:** Reviewer aprovou na 2ª passada do checkpoint visual.
- **Committed in:** `6a70b7f`

### 2. [Rule 1 — Drive-by ajuste em INTRO-01 no mesmo commit] Granularidade aritmética

- **Found during:** ao aplicar a iteração de INTRO-03b (commit `6a70b7f`), o reviewer também sugeriu ajustes em INTRO-01:
  - Parágrafo 1 do INTRO-01 reorganizado em 2 frases para legibilidade ("...CSEDM 2021. Armazenado em ProgSnap2 (Price, 2020), um formato de base de dados que registra...")
  - Stats "5 assignments com 50 problemas" → "5 assignments com 10 problemas cada, e 201 mil eventos" (granularidade aritmética explícita: 5 × 10 = 50; o leitor entende a estrutura assignments × problemas-por-assignment sem multiplicar mentalmente).
- **Issue:** Não é bug, é melhoria de legibilidade aproveitando que o reviewer já estava revisando o deck pós-INTRO-03b. Decisão D-50 de 02-02 já mencionava "5 assignments com 50 problemas"; o ajuste agora torna explícito que cada assignment tem 10 problemas.
- **Files modified:** apresentacao/index.html (2 linhas do INTRO-01 ajustadas no mesmo commit `6a70b7f`).
- **Verification:** Mesmo checkpoint visual aprovou as 2 alterações.
- **Committed in:** `6a70b7f` (mesmo commit da iteração INTRO-03b por economia de commit)

---

**Total deviations:** 2 ajustes via iteração pós-checkpoint (Rule 1 categoria "user feedback during human-verify gate"). Sem scope creep: o requirement INTRO-03 (consequência pedagógica) não mudou; a granularidade aritmética em INTRO-01 reforça a decisão D-50 do plan anterior. Os 2 micro-fixes ortográficos de Claude foram aplicados em cima do texto proposto pelo usuário sem alteração de semântica.

## Issues Encountered

Nenhum. O slide passou em todos os gates automatizados em ambas as iterações. Iteração textual é feedback estruturado do reviewer, não issue.

## Auth Gates

Nenhum.

## Self-Check: PASSED

- `git log --oneline | grep c92b9ff` → FOUND ("apresentacao: slide INTRO-03b - sinal pedagogico perdido")
- `git log --oneline | grep 6a70b7f` → FOUND ("apresentacao: reescrever INTRO-03b com cenario expandido + gap")
- `git log --oneline | grep f4dde9c` → FOUND ("docs(style): atualizar gaps reservados pos-fase 2")
- `grep -c '>sinal pedagógico perdido<' apresentacao/index.html` → 1 (cabeçalho D-34c)
- `grep -c 'Fonte: adaptado de Shi <i>et al.</i> (2022).' apresentacao/index.html` → 1 (rodapé D-45 + D-54)
- `awk '/SLIDE · INTRO-03b/,/<\/section>/' apresentacao/index.html | grep -ci 'code-dkt'` → 0 (gate forte fase 4)
- `awk '/SLIDE · INTRO-03b/,/<\/section>/' apresentacao/index.html | grep -c '(Shi et al., 2022)'` → 0 (sem citação parentética nova de Shi no corpo)
- `awk '/SLIDE · INTRO-03b/,/<\/section>/' apresentacao/index.html | grep -c '—'` → 0 (sem em-dash D-44)
- `grep -cE '<section data-background-(color|gradient)' apresentacao/index.html` → 16 (deck final fase 2)
- `grep -c 'Após \`> da edm ao knowledge tracing\` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).' apresentacao/STYLE.md` → 1 (D-59 STYLE.md fix)
- `grep -cF 'Após \`> introdução\` (slide 3): INTRO-01' apresentacao/STYLE.md` → 0 (frase obsoleta REMOVIDA)
- Checkpoint humano: APPROVED fim a fim no #/0 → #/15

## Next Phase Readiness

**Fase 2 oficialmente fechada.** Requirements INTRO-01 (plan 02-02), MARKER-01 (plan 02-01), e INTRO-03 (plans 02-03 + 02-04) todos completos. Deck navega de Capa (#/0) a slide-fig (#/15) em 16 sections.

**Backlog para fases futuras:**

- **Redesenho visual do componente `.slide-marker`** (decisão de 02-01, mantida em backlog): formato atual de progress bar com 4 caixas horizontais foi aceito como stub funcional pelo reviewer mas não casa com viés computacional desejado (AST/pipeline/terminal). Decisão: revisitar antes da defesa ou em fase futura quando MARKER-02/03/04 forem implementados em batch. Contrato de classes (`--done`/`--pending`/`__mark`) preservado; redesenho não quebra callers.
- **D-58 termo `<i>gap</i>`:** estabelece padrão estilístico para futuros slides que precisem de marca computacional via termos estrangeiros. Aplicar em INTRO-* ou MODEL-* da fase 4 se ficar natural.

**Fase 3 (EDA e Pré-processamento, Fase 2 EDM) pronta para começar:**
- Âncora superior: MARKER-01 (#/10) ✓ 
- Âncora inferior: slide-code (#/11) ✓
- STYLE.md §Gaps reservados já indica posição correta: "Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3)" ✓
- D-38b: EDA-02 deve fazer ponte explícita "do CSEDM bruto (413) seguimos o protocolo de Shi et al. (2022) com filtro `min_attempts >= 3` → 410 estudantes" — INTRO-01 já mostrou o dataset cru, EDA-02 mostra o pós-filtro.
- D-50/D-51: vocabulário "5 assignments × 10 problemas cada" e 6 colunas-chave do ProgSnap2 já introduzidos em INTRO-01; EDA-01 pode partir desse vocabulário sem redefinir.

---

*Phase: 02-intro-dataset-e-problema-fase-1-edm*
*Plan: 04 (INTRO-03b + STYLE.md + close fase 2)*
*Completed: 2026-05-27*
