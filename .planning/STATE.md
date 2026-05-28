---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: executing
last_updated: "2026-05-27T21:15:00.000Z"
progress:
  total_phases: 5
  completed_phases: 1
  total_plans: 11
  completed_plans: 9
  percent: 82
---

# State: Apresentação TCC 1

**Last updated:** 2026-05-27 após fechamento do plan 02-01 (MARKER-01 como stub funcional aprovado; redesenho diferido para fim da fase 2)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-05-27)

**Core value:** Slides HTML reveal.js funcionais, narrativamente claros e cientificamente fiéis, prontos para defesa em ~1 semana.

**Current focus:** Phase 2 — Intro, Dataset e Problema (Fase 1 EDM)

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | Reformatação da base | Complete (7 / 7 plans) ✓ 2026-05-27 |
| 2 | Intro, Dataset e Problema (Fase 1 EDM) | In progress (1 / 4 plans) |
| 3 | EDA e Pré-processamento (Fase 2 EDM) | Pending |
| 4 | Modelagem e Avaliação (Fase 3 EDM) | Pending |
| 5 | Implantação, Agenda e Encerramento (Fase 4 EDM) | Pending |

## Plans concluídos

| Plan | Requirement | Commits | Resumo |
|---|---|---|---|
| 01-01 | REMOVE-01 | `ed03327`, `91b9675` | Working tree snapshot (commit-wip) + delete dos 2 slides Corbett |
| 01-02 | MERGE-01 | `f9907b8` | Fundir Zorić p1+p2 num único slide com cabeçalho `> mineração de dados educacionais`; 2 citações diretas substituídas por paráfrase única em voz própria (D-26); section count cai de 14 para 13 |
| 01-03 | REFORMAT-03 | `b60439e` | Fundir Yağcı p1+p2 num único slide `slide-related slide-bridge` com cabeçalho `> da edm ao knowledge tracing`; citação direta p.2 substituída por paráfrase D-27 ("acompanhamos o conhecimento ao longo do tempo"); `.bridge-seq` (3 passos) preservada literalmente; section count cai de 13 para 12 |
| 01-04 | REFORMAT-01 | `c31658c` | Reformatar slide Martins p1 (`slide-related`): par `.rel-kicker.kicker` + `<h2 class="rel-title">Martins, Marin e Alves (2024)</h2>` substituído por `<p class="deck-topic">> introdução</p>` único com caret blink (D-04); 3 `.rel-lead` preservados (D-29); rodapé `Fonte: Martins, Marin e Alves (2024).` mantido (D-23); último `.rel-kicker` do arquivo eliminado; section count permanece em 12 |
| 01-05 | REFORMAT-02 | `23eed8b` | Reformatar slide-phases (Zorić p3): `<p class="deck-topic">` interno trocado de `> trabalhos correlatos` para `> as quatro fases da edm` (D-05) e `<h2 class="phases-title">As quatro fases do processo de EDM</h2>` removido por inteiro (D-03); wrapper `<div class="phases-head">` preservado por decisão conservadora (efeito visual a validar em browser); `.phases-list` (4 itens), `.phases-note` e rodapé `Fonte: Zorić (2020).` preservados intactos (D-29, D-23); comentário HTML atualizado de `SLIDE 5 · ... fluxo horizontal formal` para `SLIDE · As 4 fases da EDM (Zorić, 2020)`; section count permanece em 12 |
| 01-06 | REFORMAT-04, REFORMAT-05 | `590ae34`, `2a86049` | Reformatar + mover 5 slides finais em duas passadas atômicas. Task 1 (`590ae34`): cabeçalhos dos 5 slides reformatados in-place (Martins p2/p3 `> retomando o problema` D-07, slide-kcfig `> kcs semânticos extraídos` D-08, slide-fig `> evolução por dificuldade` D-09, slide-code `> o que o code-dkt olha` D-10); `<h2>` deletados (D-03); 2 citações diretas Martins preservadas (D-28). Task 2 (`2a86049`): 5 sections movidos para o fim de `<div class="slides">` na ordem D-16 (slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig); D-17a/b/c validados. Discretion D-16: slide-code antes de slide-kcfig. Section count: 12 |
| 01-07 | (consolidação) | `907a4b5`, `30ba911`, `9224d5f` | Fechamento da fase 1. Task 1-3 (`907a4b5`): STYLE.md reescrito (D-21) com 3 seções (cabeçalho `.deck-topic` único; regras de redação com "Apresentação de autores" + "Voz própria como padrão" no lugar da "Regra dos correlatos"; inventário de 12 slides pós-fase 1 + gaps reservados para fases 2-5). Task 4 (`30ba911`, Branch A): 4 regras CSS órfãs `.rel-kicker`/`.rel-title`/`.rel-sub` deletadas de theme-unifacens.css; demais classes do template `.slide-related` preservadas. Task 5: checkpoint humano fim-a-fim no browser APPROVED; 13/13 automated gates + 8 Success Criteria do ROADMAP confirmados. Tweaks tipográficos pós-checkpoint (`9224d5f`): `.deck-topic` em Arial bold uppercase preto; `.slide-title-tcc .tcc-label` Arial explícito; 6 classes Fonte: padronizadas em 18px Arial; slide Zorić fundido reescrito com sigla EDM padrão ABNT. Task 6: PHASE-SUMMARY agregando os 7 plans criado |
| 02-01 | MARKER-01 | `d37304d`, `3d47be4` | Componente CSS reutilizável `.slide-marker` (host + modificadores `--done`/`--pending`, sem `border-radius`, variáveis existentes) anexado a theme-unifacens.css (linhas 358-408); section MARKER-01 inserido em index.html linhas 149-179 entre slide Yağcí fundido (linha 147) e slide-code; 4 caixas na ordem D-40 (1ª em `--done` com `&check;`, 2-4 em `--pending` com números), 3 setas, rodapé `Fonte: adaptado de Zorić (2020).`; sem `.deck-topic` (D-34d); sem em-dash (D-44); sections do deck: 12 → 13; slide acessível em `#/7`. Checkpoint humano APPROVED como stub funcional; usuário pediu redesenho do formato visual com viés de computação (AST/pipeline/terminal) DIFERIDO para fim da fase 2 ou em batch com MARKER-02/03/04 — contrato de classes preservado, callers não quebram |

## Workflow

- Mode: interactive
- Granularity: coarse
- Parallelization: true
- Commit docs: true
- Model profile: quality
- Research: on (per-phase before planning)
- Plan check: on (verify plan achieves phase goal)
- Verifier: off (visual validation in browser)

## Recent commits

Top commits funcionais (cronológicos):

- `3d47be4` apresentacao: slide MARKER-01 - definicao do problema (fase 2)
- `d37304d` apresentacao: componente .slide-marker reutilizavel (fase 2)
- `9224d5f` apresentacao: ajustes tipográficos pós-checkpoint fase 1
- `30ba911` apresentacao: limpar regras CSS órfãs (.rel-kicker/.rel-title/.rel-sub)
- `907a4b5` apresentacao: atualizar STYLE.md para padrão > [seção] (D-21, D-25)
- `2a86049` apresentacao: mover trio Martins+fig e slide-code/slide-kcfig para o fim (REFORMAT-04 + REFORMAT-05, D-16/D-17)
- `590ae34` apresentacao: reformatar cabeçalhos dos 5 slides do bloco final (REFORMAT-04 + REFORMAT-05)
- `23eed8b` apresentacao: reformatar slide-phases com > as quatro fases da edm (REFORMAT-02, D-05)
- `c31658c` apresentacao: reformatar Martins p1 com > introdução (REFORMAT-01, D-04)
- `b60439e` apresentacao: fundir slides Yağcı p1+p2 com paráfrase (REFORMAT-03, D-27)
- `f9907b8` apresentacao: fundir slides Zorić p1+p2 com paráfrase (MERGE-01, D-26)
- `91b9675` apresentacao: remover slides Corbett (REMOVE-01)

## Next action

Continuar fase 2 com a próxima wave (plans 02-02, 02-03, 02-04):

```
/gsd-execute-phase 2
```

Plan 02-01 (MARKER-01) concluído como stub funcional aprovado. Próximos plans da fase 2:
- 02-02: INTRO-01 — slide "o dataset csedm" (CSEDM em ProgSnap2, voz 1ª pessoa)
- 02-03: INTRO-03a — slide "o problema do kt binário" (Shi et al. 2022, BKT+DKT, sem Code-DKT)
- 02-04: INTRO-03b — slide "sinal pedagógico perdido" + STYLE.md fix linha 129 + validação fim a fim

**Backlog visual (não bloqueante):** redesenhar `.slide-marker` com viés de computação (referências: AST, terminal, pipeline) no fim da fase 2 ou em batch com MARKER-02/03/04. Contrato de classes (`--done`/`--pending`/`__mark`) preservado; redesenho não quebra callers.
