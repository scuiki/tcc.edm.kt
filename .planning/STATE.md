---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: ready_to_plan
last_updated: "2026-05-28T00:30:00.000Z"
progress:
  total_phases: 5
  completed_phases: 2
  total_plans: 11
  completed_plans: 11
  percent: 40
---

# State: Apresentação TCC 1

**Last updated:** 2026-05-28 após fechamento da fase 2 (INTRO-03b entregue após 1 iteração textual; STYLE.md §Gaps reservados reescrito; checkpoint fim a fim APPROVED; deck final 16 sections com INTRO-01/03a/03b + MARKER-01 cobrindo a Fase 1 EDM)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-05-27)

**Core value:** Slides HTML reveal.js funcionais, narrativamente claros e cientificamente fiéis, prontos para defesa em ~1 semana.

**Current focus:** Phase 3 — EDA e Pré-processamento (Fase 2 EDM)

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | Reformatação da base | Complete (7 / 7 plans) ✓ 2026-05-27 |
| 2 | Intro, Dataset e Problema (Fase 1 EDM) | Complete (4 / 4 plans) ✓ 2026-05-27 |
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
| 02-02 | INTRO-01 | `c362e9d`, `e07e37b`, `3835336` | Section INTRO-01 inserido em index.html linhas 149-164, entre Yağcí (#/6) e MARKER-01 (que desloca para #/8); reusa template `.slide-related` + `.rel-lead` + `.rel-cite` (zero CSS novo); cabeçalho `> o dataset csedm` (D-34a); voz 1ª pessoa do plural ("Nosso dataset é o CSEDM..."); 3 números brutos validados via pandas (413 estudantes, 50 problemas, 201.570 eventos) escritos como "413 estudantes, 5 assignments com 50 problemas, 201 mil eventos"; citação parentética `(Price, 2020)`; rodapé literal `Fonte: Price (2020); CSEDM 2021.`; sem em-dash (D-44); sections do deck: 13 → 14. Após checkpoint visual APPROVED, reviewer pediu 2 iterações pós-checkpoint: `e07e37b` adicionou granularidade (Spring 2019 explícito, "5 assignments com 50 problemas", parágrafo `.intro-cols-line` listando 6 colunas-chave do ProgSnap2: SubjectID, ProblemID, EventType, Score, ServerTimestamp, CodeStateID); `3835336` ajustou fraseado da coleta ("coletado durante a primavera de 2019 e divulgado") para sujeito implícito coerente. Decisões ad-hoc D-50 (5 assignments com 50 problemas) e D-51 (listar colunas-chave do ProgSnap2) registradas no 02-02-SUMMARY para fases futuras |
| 02-03 | INTRO-03 (parcial: 03a) | `6f0ae3d`, `53b46e8`, `f7e042a`, `4a9af6e` | Section INTRO-03a inserido em index.html linhas 166-181, entre INTRO-01 (#/7) e MARKER-01 (que desloca para #/9); reusa template `.slide-related` + `.rel-lead` + `.rel-cite` (zero CSS novo); cabeçalho `> o problema do kt binário` (D-34b); 3 parágrafos (ponte KT → crítica Shi → escopo de domínios estruturados); rodapé literal `Fonte: Shi <i>et al.</i> (2022).`; sem em-dash (D-44); sem Code-DKT (gate forte D-36 / Pitfall 3); sections do deck: 14 → 15. Após checkpoint visual APPROVED, reviewer pediu 3 iterações pós-checkpoint: `53b46e8` reescreveu paráfrase com phrasing do Report 4 + Shi 2022 (mais fiel ao paper que a versão inicial); `f7e042a` adicionou primeiro parágrafo de ponte (KT como instrumento central → eventos do CSEDM) antes da crítica Shi para evitar transição abrupta; `4a9af6e` normalizou `<i>et al.</i>` ABNT em todo o deck (8 ocorrências em drive-by sweep). Decisões ad-hoc D-52 (paráfrase Report 4 + Shi 2022), D-53 (ponte KT → trabalho → CSEDM), D-54 (`<i>et al.</i>` ABNT no deck), D-55 (3º parágrafo escopo de domínios sem nomear Code-DKT) registradas no 02-03-SUMMARY |
| 02-04 | INTRO-03 (fechado: 03b) | `c92b9ff`, `6a70b7f`, `f4dde9c` | Section INTRO-03b inserido em index.html linhas 183-198, entre INTRO-03a (#/8) e MARKER-01 (que desloca para #/10); reusa template `.slide-related` + `.rel-lead` + `.rel-cite` (zero CSS novo); cabeçalho `> sinal pedagógico perdido` (D-34c); 3 parágrafos consequenciais (cenário concreto: aluno acerta parte do código mas erra em algum passo, submissão pode não compilar ou compilar e estar errada → perda pedagógica: tratada idêntica a completamente errada, aprendizado parcial fica invisível → pivô: gap entre KT clássico e o que pedagogicamente aconteceu, motiva modelos sensíveis ao código); rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`; sem em-dash, sem Code-DKT, sem citação parentética nova de Shi no corpo. STYLE.md §Gaps reservados reescrito por inteiro (linha 129 obsoleta substituída + linha 130 ajustada para "Após MARKER-01"). Iteração pós-checkpoint: `6a70b7f` substituiu "80% do código" (arbitrário) por "acerta parte do código, mas erra em algum dos passos" + observação técnica cobrindo Compile.Error + Score parcial; substituiu "Abre-se uma lacuna" por "Isso abre um <i>gap</i>" (D-58 termo estrangeiro D-46 estendido); bônus orgânico em INTRO-01 (granularidade aritmética "5 assignments com 10 problemas cada", reorganização do parágrafo 1 em 2 frases). Decisões ad-hoc D-56 (INTRO-03b autônomo), D-57 (cenário via Report 4 + observação Compile.Error), D-58 (`<i>gap</i>`), D-59 (STYLE.md §Gaps reescrito por inteiro) registradas. Sections do deck: 15 → 16; checkpoint humano fim a fim APPROVED (#/0 → #/15) |

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

- `f4dde9c` docs(style): atualizar gaps reservados pos-fase 2
- `6a70b7f` apresentacao: reescrever INTRO-03b com cenario expandido + gap
- `c92b9ff` apresentacao: slide INTRO-03b - sinal pedagogico perdido
- `4a9af6e` apresentacao: italizar "et al." conforme ABNT no deck
- `f7e042a` apresentacao: adicionar ponte KT-trabalho-CSEDM em INTRO-03a
- `53b46e8` apresentacao: reescrever INTRO-03a com fraseado do Report 4 + Shi 2022
- `6f0ae3d` apresentacao: slide INTRO-03a - problema do kt binario (Shi et al. 2022)
- `3835336` apresentacao: ajustar fraseado da coleta no slide INTRO-01
- `e07e37b` apresentacao: ajustar INTRO-01 - primavera 2019, 5 assignments, colunas ProgSnap2
- `c362e9d` apresentacao: slide INTRO-01 - dataset CSEDM (Price, 2020)
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

Fase 2 oficialmente fechada. Próximo passo da iteração da apresentação:

```
/gsd-discuss-phase 3
```

**Fase 3: EDA e Pré-processamento (Fase 2 EDM).** Adiciona 4 slides novos (EDA-01, EDA-02, EDA-03 + MARKER-02). Inserção após MARKER-01 (#/10) e antes do slide-code (#/11). Ler `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/PHASE-SUMMARY.md` para vocabulário e decisões herdadas da fase 2.

Decisões ad-hoc das waves da fase 2 (registradas para fases futuras):
- D-50 (02-02): "5 assignments com 10 problemas cada" (atualizado para granularidade aritmética em 02-04) introduzido em INTRO-01; fases 3 (EDA-01) e 4 (MODEL-01..05) não precisam reintroduzir
- D-51 (02-02): 6 colunas-chave do ProgSnap2 (SubjectID, ProblemID, EventType, Score, ServerTimestamp, CodeStateID) listadas em INTRO-01; EDA-02 pode partir desse vocabulário sem redefinir
- D-52 (02-03): paráfrase Shi 2022 + Report 4 (mais fiel ao paper que o phrasing-alvo inicial do RESEARCH §1.3); ancorar no vocabulário "tratam respostas como corretas/incorretas, ignorando seu conteúdo"
- D-53 (02-03): ponte explícita KT → trabalho → CSEDM antes da crítica em slides INTRO de diagnóstico; padrão aplicado também em INTRO-03b
- D-54 (02-03): `<i>et al.</i>` ABNT normalizado no deck (8 ocorrências); precedente para fases 3-5
- D-55 (02-03): 3º parágrafo de escopo (domínios com respostas estruturadas) sem nomear Code-DKT mantém gate forte fase 4
- D-56 (02-04): INTRO-03b autônomo entre INTRO-03a e MARKER-01; INTRO-03 dividido em 2 sub-slides (diagnóstico + consequência) como padrão para futuros pivots narrativos
- D-57 (02-04): cenário concreto via Report 4 + observação "pode não compilar, ou compilar e estar errada" cobrindo Compile.Error + Score parcial do CSEDM; vocabulário disponível para EDA-02 + MODEL-04
- D-58 (02-04): `<i>gap</i>` como termo estrangeiro em INTRO-03b (D-46 estendido); precedente para outros termos computacionais em itálico (`<i>pipeline</i>`, `<i>benchmark</i>`)
- D-59 (02-04): STYLE.md §Gaps reservados reescrito por inteiro; "Após MARKER-01 e antes do trio Martins+fig" é o ponto de inserção canônico para fase 3

**Backlog visual (não bloqueante):** redesenhar `.slide-marker` com viés de computação (referências: AST, terminal, pipeline) em batch com MARKER-02/03/04 ou em sessão dedicada de polimento antes da defesa. Contrato de classes (`--done`/`--pending`/`__mark`) preservado; redesenho não quebra callers. MARKER-02 da fase 3 herda o stub atual.
