---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: in_progress
last_updated: "2026-05-29T05:57:12.063Z"
progress:
  total_phases: 5
  completed_phases: 4
  total_plans: 26
  completed_plans: 23
  percent: 88
---

# State: Apresentação TCC 1

**Last updated:** 2026-05-29 após fechamento da fase 4 inteira (5/5 plans + 2 adendos INTRO-KC e slide-code CSS; deck final em 27 sections; commits finais `ccc7a4f` MARKER-03 + `3ea83d3` STYLE.md inventário pós-fase 4)

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-05-27)

**Core value:** Slides HTML reveal.js funcionais, narrativamente claros e cientificamente fiéis, prontos para defesa em ~1 semana.

**Current focus:** Phase 04 — modelagem-e-avalia-o-fase-3-edm

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | Reformatação da base | Complete (7 / 7 plans) ✓ 2026-05-27 |
| 2 | Intro, Dataset e Problema (Fase 1 EDM) | Complete (4 / 4 plans) ✓ 2026-05-27 |
| 3 | EDA e Pré-processamento (Fase 2 EDM) | Pending |
| 4 | Modelagem e Avaliação (Fase 3 EDM) | Complete (5 / 5 plans + 2 adendos) ✓ 2026-05-29 |
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
| 04-01 | MODEL-01, MODEL-03 | `4f2bc3f` | Plan dividido em 2 slides durante checkpoint visual. MODEL-01a (#/16) `> o modelo escolhido`: frase de justificativa 1ª pessoa do plural (Shi <i>et al.</i>, 2022) + cronologia horizontal com 3 marcadores (1995 Corbett e Anderson, 2015 Piech <i>et al.</i>, 2022 Shi <i>et al.</i>, último dot em azul UniFacens). MODEL-01b (#/17) `> dentro do code-dkt`: frase conceitual + pipeline esquerda-alinhado com setas em 1 linha (`<b><i>Pipeline</i> Code-DKT:</b> javalang → AST → code2vec → atenção → LSTM`) + AST limpa max 460px com título ABNT en-dash + Fonte 14px cinza. SVG da AST trimado (viewBox `0 0 560 620` → `0 0 560 410`, legenda "Figura 2:" embutida removida). MODEL-03 absorvido como no-op (slide-code reaproveitado adiante). Decisões ad-hoc D-79g (split do plan), D-79h (cronologia sem chips), D-79i (pipeline setas em vez de prosa), D-79j (SVG trim em vez de wrapper), D-79k (header `> o modelo escolhido`) registradas em 04-01-SUMMARY. Sections do deck: 21 → 23 (+2); slide-code desloca de #/16 para #/18; checkpoint visual APPROVED após 5 iterações (3 textuais + 1 split estrutural + 1 ajuste final) |
| 04-02 | MODEL-04 | `7a9ae9a` | Section MODEL-04 inserida entre slide-code (#/18) e slide-kcfig (que desloca para #/20). Cabeçalho `> code-dkt no csedm`; intro `.rel-lead` em 1ª pessoa do plural ("Comparamos os três modelos..."); título `Tabela 2 – <i>First-attempt</i> AUC...` em `.eda-title`; tabela `.eda-grid` 4 linhas (BKT, DKT, Code-DKT, Shi (2022)*) × 6 colunas (Modelo + A439..A502) com vírgula decimal pt-BR; 4 células Shi em `&ndash;` exceto A439=75,74%; caption discreto pós-tabela (Pitfall 8 + Shi §5); rodapé `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.` em `.eda-source`. Plan executado autônomo (sem checkpoint humano) por se tratar de tabela determinística D-78g; 14/14 acceptance criteria passaram (incluindo HTTP 200 smoke test na porta 8003). Sections do deck: 23 → 24; Code-DKT vence DKT em 4/5 assignments (A439 -2,29pp é inversão conhecida); delta Code-DKT A439 vs Shi paper = -2,47pp (dentro ±3pp do CLAUDE.md) |
| 04-03 | MODEL-05 | `f093a9b` | Section MODEL-05 inserida entre MODEL-04 (#/18) e slide-kcfig (que desloca para #/20). Cabeçalho `> extração automática de kcs`; abertura cita Duan na 1ª frase ("Construímos um <i>pipeline</i> de cinco etapas, baseado em Duan <i>et al.</i> (2025), para extrair <i>knowledge components</i> do CSEDM."); pipeline como Figura ABNT com `.eda-title` "Figura – Pipeline de extração automática de KCs" + 5 caixas `.bridge-seq` com flex-direction column inline (verbo / descrição empilhados, sem bold, preto #000) na ordem Sampling n=5 → LLM → Clustering → Rotulagem → Q-matrix + `.eda-source` "elaborado pelo autor; adaptado de Duan <i>et al.</i> (2025)"; parágrafo final substitui "código bruto vs AST" do PLAN.md por explicação sobre por que extraímos KCs das respostas corretas (CSEDM sem enunciados; n=5 amostragem). Decisões ad-hoc D-79l (rejeição do fallback CSS narrow), D-79m (Duan na abertura), D-79n (parágrafo CSEDM substitui código-vs-AST), D-79o (pipeline como Figura), D-79p (preto puro #000 inline), D-79q (knowledge components minúsculo). 4 iterações de design durante checkpoint. Sections do deck: 24 → 25 |
| 04-04 | CLOSE-01, CLOSE-02, CLOSE-03, PENDING-04 | `7e67b74` | Pick visual de 4 PNGs candidatos para o slide-fig (CLOSE-03) via checkpoint humano. Usuário escolheu pick: 1 (curves_by_martins, o PNG canônico atual) após comparação visual dos 4 candidatos em #/24..#/27 temporários. Razão: "Estruturas de controle aprende rápido; Vetores e Funções planos" é leitura mais legítima e direta para o eixo prioritário Martins → Code-DKT da defesa. Único delta: comentário HTML linha 653 corrigido de `<!-- figura: results/fig_codedkt_difficulty_martins.png (...) -->` para `<!-- figura: results/fig_codedkt_curves_by_martins.png (= assets/fig-codedkt-martins-curves.png; PENDING-04 resolved em 04-04) -->` (Pitfall 9 resolvido). `<img>` e `<p class="fig-read">` permanecem intactos. CLOSE-01 (Martins p2 linhas 608-629) e CLOSE-02 (Martins p3 linhas 631-650) confirmados intactos via grep D-82 (0 linhas modificadas em todo o plan). Cleanup: 3 PNGs temporários removidos do disco + 3 sections temporárias removidas do HTML. Sections do deck: 25 → 28 (temp) → 25 (final). Working tree limpo após cleanup |
| adendo INTRO-KC | adendo conceitual | `271beff` | Slide adendo INTRO-KC inserido entre MARKER-02 (#/15) e MODEL-01a, posição #/16. Definição de Knowledge Components com origem em Corbett e Anderson (1995) no ACT Programming Tutor; explicação da relevância (granularidade do diagnóstico); declaração da nossa escolha "KC = ProblemID, 1 modelo por assignment seguindo protocolo Shi et al. (2022)". 3 parágrafos com citações ABNT, sem em-dash. Pesquisado o paper Corbett & Anderson PDF para precisão histórica (termo "KC" formalizado depois; CA usaram "regras" e "habilidades"). 2 iterações de texto durante checkpoint. Sections do deck: 25 → 26 |
| adendo slide-code CSS | UX fix | `ef10154` | Reformulação do `.slide-code` CSS para consistência com `.slide-related`: padding 34px 56px 24px → 52px 64px 24px (título alinhado horizontal/vertical com demais slides); `.code-lead` 17px → 21px; `.code-take` 16px → 18px; bolds `.code-lead b`/`.code-take b` mudaram de `--uni-blue-d` para `--uni-ink` (preto, consistente com demais slides); `.code-fonte` text-align center → left. Syntax highlighting do código Java (`.devcpp__code .kw`) preservado em azul (highlight de sintaxe, não bold de prosa). 2 iterações de checkpoint (1 para fontes/cores/alignment + 1 para padding-top do título). Sem mudanças no markup do slide-code |
| 04-05 | MARKER-03 | `ccc7a4f`, `3ea83d3` | Section MARKER-03 inserida ao FIM do deck (após slide-fig CLOSE-03), posição #/26. Copy-paste de MARKER-02 com 4 deltas: classe `slide-marker--phase3`; pill 3 (Modelagem e Avaliação) vira `marker-pill--done` com `&check;` e badge `[done]`; pill 4 (Implantação) vira `marker-pill--running` com `&#x21BB;` e badge `[running]` + animação `marker-spin`; comentário HTML atualizado para "fase 3 concluida". 1 reposicionamento durante checkpoint (assistente moveu para após MODEL-05 baseado em pedido literal; usuário corrigiu para fim do deck porque a próxima fase é TCC 2 ferramenta). STYLE.md §Inventário reescrito para 27 slides finais com posições verificadas; §Gaps reservados realocado para fase 5 (TOOL-01, TOOL-03, MARKER-04, END-01, AGENDA-01). Sections do deck: 26 → 27. Phase 4 = COMPLETE |

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

- `3ea83d3` docs(style): atualizar STYLE.md §Inventário e §Gaps reservados pós-fase 4
- `ccc7a4f` apresentacao: slide MARKER-03 - modelagem e avaliação concluída + implantação running (Zorić, 2020)
- `ef10154` apresentacao: CSS .slide-code consistência com .slide-related
- `271beff` apresentacao: slide INTRO-KC - conhecimento como componentes (Corbett e Anderson, 1995; Shi et al., 2022)
- `7e67b74` apresentacao: slide CLOSE-03 - PENDING-04 mantém curves_by_martins + fix comentário linha 653
- `f093a9b` apresentacao: slide MODEL-05 - extração automática de kcs (pipeline 5 etapas, Duan et al. 2025)
- `7a9ae9a` apresentacao: slide MODEL-04 - code-dkt no csedm (tabela ABNT 4 modelos x 5 assignments vs Shi)
- `4f2bc3f` apresentacao: slides MODEL-01a/01b - o modelo escolhido + dentro do code-dkt (Shi et al., 2022)
- `b501800` docs(apresentacao): editorial tweaks pré-fase 4
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

Fase 4 FECHADA com 5/5 plans + 2 adendos (INTRO-KC + slide-code CSS). Deck final em 27 sections. Próximo passo: `/gsd-discuss-phase 5` ou `/gsd-plan-phase 5` para a fase 5 (Implantação, Agenda e Encerramento) — TOOL-01 (proposta ferramenta TCC 2 com pipeline mini-horizontal), TOOL-03 (dashboard), MARKER-04 (fim da fase 4 EDM = Implantação ✓), END-01 (agradecimento), AGENDA-01 revisado.

**Fase 4 — Resumo agregado:** ver 04-05-SUMMARY.md seção "Phase 4 — Resumo agregado" (5 plans + 2 adendos + 9/9 REQ-IDs cobertos + 11 decisões ad-hoc D-79g..D-79q registradas; deck 21 → 27 sections com 6 adições líquidas + reposicionamentos + CSS slide-code reformulado).

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
