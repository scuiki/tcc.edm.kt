# Roadmap: Apresentação TCC 1 — Análise do aprendizado de programação via EDM

**Created:** 2026-05-27
**Mode:** Vertical MVP (cada fase entrega slides funcionais ponta a ponta no browser)
**Total phases:** 5
**Total v1 requirements mapped:** 30 / 30 (reduzido de 37 em 2026-05-27 em duas rodadas, ver REQUIREMENTS.md "Nota 2026-05-27")

## Visão geral

Cinco fases organizadas em ordem narrativa (do reuso ao encerramento), cada uma entregando um conjunto de slides que carrega no browser sem quebra. A fase 1 prepara a base (slides existentes ajustados); fases 2 a 5 cobrem as 4 fases da EDM na ordem da apresentação. Validação visual no browser a cada fase concluída.

| # | Fase | Goal | Reqs | Mode | Status |
|---|---|---|---|---|---|
| 1 | Reformatação da base | Slides existentes ajustados ao novo padrão de cabeçalho, com Zorić fundido e Corbett removido | 7 | mvp | Complete ✓ 2026-05-27 |
| 2 | Intro, Dataset e Problema (Fase 1 EDM) | Novos slides da abertura narrativa: Yağcí ponte → "nosso dataset" (CSEDM em ProgSnap2 fundido) → Shi problema, fechando com marcador da Fase 1 EDM | 3 | mvp | Complete ✓ 2026-05-27 |
| 3 | EDA e Pré-processamento (Fase 2 EDM) | Slides de análise exploratória, pré-processamento e um insight visual sobre os estudantes, fechando com marcador da Fase 2 EDM | 5 | mvp | Pending |
| 4 | Modelagem e Avaliação (Fase 3 EDM) | Code-DKT (funcionamento + AST inset, fundidos) + KCs semânticos via Duan + retomada de Martins (problema → evidência, eixo prioritário da defesa), fechando com marcador da Fase 3 EDM | 9 | mvp | Pending |
| 5 | Implantação, Agenda e Encerramento (Fase 4 EDM) | Proposta da ferramenta TCC 2 (espelha as fases anteriores sem repetir), dashboard, marcador final, agradecimento e revisão da Agenda | 6 | mvp | Pending |

## Detalhamento das fases

### Phase 1: Reformatação da base
**Goal:** Slides existentes (16) ajustados para o novo padrão narrativo: cabeçalho `> [seção]` no lugar de tópico + título, Zorić p1+p2 fundido, Corbett & Anderson removidos. Resultado: a base atual reorganizada serve como ponto de partida limpo para as fases seguintes.
**Mode:** mvp
**Requirements**: REFORMAT-01, REFORMAT-02, REFORMAT-03, REFORMAT-04, REFORMAT-05, MERGE-01, REMOVE-01
**Success Criteria**:
1. `apresentacao/index.html` abre no browser sem erro de console e a navegação reveal.js funciona do primeiro ao último slide
2. Slide Martins p1 exibe cabeçalho `> introdução` (caret piscando); autor aparece apenas em "Fonte:" no rodapé
3. Slide Zorić p3 exibe cabeçalho `> as quatro fases da edm` com o conteúdo das fases preservado
4. Slide Yağcí exibe cabeçalho `> da edm ao knowledge tracing` com gancho explícito sobre acompanhamento ao longo do tempo
5. Slide Zorić fundido (p1+p2) tem cabeçalho `> mineração de dados educacionais` e mostra Zorić como autor + ferramentas/metodologias num único slide
6. Os 2 slides de Corbett & Anderson removidos; busca por `slide-corbett` no `index.html` retorna 0 ocorrências
7. Slides Martins p2/p3 movidos para posição próxima ao final do deck (ordem preliminar dos `<section>` reflete a estrutura nova)
8. Slides `slide-fig`, `slide-code` e `slide-kcfig` reformatados ao novo padrão de cabeçalho

**Plans:** 7 plans (executar via `/gsd-execute-phase 1`)
- [x] 01-01-PLAN.md — Triage do working tree + REMOVE-01 (Corbett ×2) ✓ 2026-05-27
- [x] 01-02-PLAN.md — MERGE-01: fundir Zorić p1+p2 com paráfrase D-26 ✓ 2026-05-27 (commit `f9907b8`)
- [x] 01-03-PLAN.md — REFORMAT-03: fundir Yağcı p1+p2 com paráfrase D-27 ✓ 2026-05-27 (commit `b60439e`)
- [x] 01-04-PLAN.md — REFORMAT-01: cabeçalho > introdução no Martins p1 ✓ 2026-05-27 (commit `c31658c`)
- [x] 01-05-PLAN.md — REFORMAT-02: cabeçalho > as quatro fases da edm no slide-phases ✓ 2026-05-27 (commit `23eed8b`)
- [x] 01-06-PLAN.md — REFORMAT-04 + REFORMAT-05: reformatar e mover os 5 slides finais (D-15..D-17) ✓ 2026-05-27 (commits `590ae34`, `2a86049`)
- [x] 01-07-PLAN.md — STYLE.md (D-21) + CSS cleanup opcional + checkpoint humano final ✓ 2026-05-27 (commits `907a4b5`, `30ba911`, `9224d5f`)

### Phase 2: Intro, Dataset e Problema (Fase 1 EDM)
**Goal:** Adicionar os novos slides da abertura narrativa que estabelecem o problema: o gancho do Yağcí leva ao slide "nosso dataset" (CSEDM armazenado em ProgSnap2, fundidos), depois ao problema apontado por Shi (KT binário ignora código). Fecha com o marcador da Fase 1 EDM concluída. Voz: paráfrase indireta com autor parentético; sem citação direta literal nestes 3 slides novos.
**Mode:** mvp
**Requirements**: INTRO-01, INTRO-03, MARKER-01
**Success Criteria**:
1. Slide INTRO-01 (fundido) carrega, apresenta o dataset CSEDM (CS1 Java, coleta 2019, competição CSEDM 2021) armazenado em ProgSnap2 (Price, 2020), e explica o diferencial de múltiplas tentativas do mesmo estudante; voz em primeira pessoa do plural ("nosso dataset é...")
2. Slide(s) Shi e o problema apresentam, em paráfrase indireta com `(Shi et al., 2022)` parentético, que modelos KT atuais usam classificação binária e ignoram código; texto conferido em `docs/Code-DKT.pdf`; modelo Code-DKT NÃO é apresentado neste slide
3. Slide MARKER-01 mostra as 4 fases da EDM com "Definição do Problema" sinalizado como concluído, com estética computação-themed definida durante execução
4. Sequência completa do deck (REFORMAT base + nova abertura) navega do início ao slide MARKER-01 sem quebra

**Plans:** 4/4 plans complete
- [x] 02-01-PLAN.md, MARKER-01: componente reutilizável .slide-marker + slide "Definição do Problema ✓" (D-39..D-41, D-34d) ✓ 2026-05-27 (commits `d37304d`, `3d47be4`; aprovado como STUB, redesenho visual diferido)
- [x] 02-02-PLAN.md, INTRO-01: slide "o dataset csedm" (CSEDM em ProgSnap2, 413/50/201 mil, voz 1ª pessoa) (D-34a, D-35, D-38) ✓ 2026-05-27 (commits `c362e9d`, `e07e37b`, `3835336`)
- [x] 02-03-PLAN.md, INTRO-03a: slide "o problema do kt binário" (Shi et al. 2022, BKT+DKT, sem Code-DKT) (D-34b, D-36, D-43) ✓ 2026-05-27 (commits `6f0ae3d`, `53b46e8`, `f7e042a`, `4a9af6e`)
- [x] 02-04-PLAN.md, INTRO-03b: slide "sinal pedagógico perdido" + STYLE.md fix linha 129 + validação fim a fim (D-34c, D-37, D-32, D-47) ✓ 2026-05-27 (commits `c92b9ff`, `6a70b7f`, `f4dde9c`)

### Phase 3: EDA e Pré-processamento (Fase 2 EDM)
**Goal:** Adicionar os slides de análise exploratória e pré-processamento do dataset, incluindo um gráfico que comunica um insight legítimo sobre os estudantes. Fecha com o marcador da Fase 2 EDM concluída. ProgSnap2 NÃO é citado aqui (já introduzido em INTRO-01).
**Mode:** mvp
**Requirements**: EDA-01, EDA-02, EDA-03, MARKER-02, PENDING-02
**Success Criteria**:
1. Slide EDA-01 apresenta distribuição e organização do CSEDM (n estudantes, n problemas, n eventos) com números corretos (validados em notebook ou memórias); sem repetir formato ProgSnap2
2. Slide EDA-02 justifica a aproximação ao protocolo de Shi como parâmetro de comparação, listando etapas concretas de pré-processamento aplicadas
3. Slide EDA-03 exibe um gráfico com insight sobre os estudantes; gráfico escolhido junto com o autor (PENDING-02 resolvido) e fonte de dados validada
4. Slide MARKER-02 mostra "Preparação dos Dados" sinalizado como concluído
5. Deck navega do início até MARKER-02 sem quebra

**Plans:** 4 plans (executar via `/gsd-execute-phase 3`)
- [x] 03-01-PLAN.md — MARKER-02: slide marcador "Preparação dos Dados ✓" (zero CSS novo, D-67 deltas mecânicos)
- [x] 03-02-PLAN.md — EDA-02: aproximação ao protocolo Shi (ponte 413 → 410 → 328/82, truncagem 50; D-65)
- [x] 03-03-PLAN.md — EDA-01: como navegamos o csedm (parágrafo + tabela A1..A5 MainTable; D-64 + .eda-grid)
- [x] 03-04-PLAN.md — EDA-03: três jeitos de aprender (scatter PCA com SEED=42; resolve PENDING-02; script + PNG + slide + STYLE.md update)

### Phase 4: Modelagem e Avaliação (Fase 3 EDM)
**Goal:** Apresentar Code-DKT (funcionamento + AST como inset visual no mesmo slide), atenção em código real, resultados vs Shi. Em seguida, apresentar a extração automática de KCs semânticos via LLM (Duan, com pipeline em 3 etapas no MESMO slide); a saída do pipeline aparece no slide-kcfig (já posicionado na fase 1). Encerrar retomando Martins (CLOSE-01/02/03, EIXO PRIORITÁRIO DA DEFESA) para amarrar problema → evidência, e fechar com o marcador da Fase 3 EDM concluída. NÃO repetir lista de KCs gerados nem aplicação concreta de KC antes do CLOSE (absorvido em slide-kcfig e CLOSE-01/02).
**Mode:** mvp
**Requirements**: MODEL-01, MODEL-03, MODEL-04, MODEL-05, CLOSE-01, CLOSE-02, CLOSE-03, MARKER-03, PENDING-04
**Success Criteria**:
1. Slide MODEL-01 (fundido) cita predecessores na cronologia (Corbett & Anderson 1995 BKT, Piech 2015 DKT) e introduz Code-DKT (Shi 2022) sucintamente; vetorização code2vec via javalang mencionada; inclui inset visual da `.svg` de AST de exemplo já existente no projeto
2. Slide MODEL-03 reaproveita o `slide-code` ("O que o Code-DKT olha") com cabeçalho novo (slide já reformatado na fase 1)
3. Slide MODEL-04 mostra os resultados que tivemos lado a lado com os resultados de Shi (memória `project_codedkt_results`: A439 first_auc=72.55%, dentro da margem ±3% do paper)
4. Slide MODEL-05 (fundido) introduz Duan (2025) e o pipeline de KCs semânticos baseado em Report 4 (`/home/leokuntz/Documents/Facens/TCC/Reports/Report 4/...pdf`) num único slide; voz em primeira pessoa do plural ("nosso pipeline implementa..."); citação Duan conferida em `docs/AutomatedKC.pdf` ou `docs/2025.EDM.short-papers.83.pdf`; nota privada sobre ausência de ASTs nos prompts mantida fora do slide. A saída do pipeline aparece em seguida no slide-kcfig (REFORMAT-05a, já posicionado na fase 1)
5. Slides CLOSE-01 (Martins p2 reposicionado), CLOSE-02 (Martins p3 reposicionado) e CLOSE-03 (gráfico Code-DKT por dificuldade) fecham a sequência de modelagem amarrando o problema do Martins com a evidência dos nossos KCs e do Code-DKT; estes 3 slides são o eixo prioritário da defesa (30-40s cada). CLOSE-01/02 MANTÊM citação direta atual (Martins; Marin; Alves, 2024) porque os números "13/10 autores" são o argumento quantitativo
6. Gráfico do CLOSE-03 validado antes da inclusão (PENDING-04 resolvido); se o `pred_df` existente não estiver alinhado, decidir entre regerar ou usar gráfico alternativo
7. Slide MARKER-03 mostra "Modelagem e Avaliação" sinalizado como concluído
8. Deck navega do início até MARKER-03 sem quebra

### Phase 5: Implantação, Agenda e Encerramento (Fase 4 EDM)
**Goal:** Apresentar a proposta da ferramenta TCC 2 (baseada em `docs/tcc2_prototipo.html`) com pipeline mini-horizontal num único slide e o dashboard. A ferramenta ESPELHA o que já foi mostrado nas fases anteriores; não detalha cada etapa. Fechar com o marcador da Fase 4 EDM, agradecimento, e revisar a Agenda inicial para refletir a estrutura final entregue.
**Mode:** mvp
**Requirements**: TOOL-01, TOOL-03, MARKER-04, END-01, AGENDA-01, PENDING-01
**Success Criteria**:
1. Slide TOOL-01 (fundido) apresenta a ferramenta proposta para o TCC 2 (baseada em `docs/tcc2_prototipo.html`) E o pipeline mini-horizontal (entrada de submissões dos alunos → extração de KCs → professor valida → preparação → Code-DKT → dashboard) num único slide; sem detalhar cada etapa (já apareceram nas fases 2-4); sem mencionar ProgSnap2 nominalmente
2. Slide TOOL-03 mostra o dashboard com respostas de código da turma, predição por estudante e dificuldade por KC
3. Slide MARKER-04 mostra "Implantação" sinalizado como concluído
4. Slide END-01 de agradecimento encerra a apresentação
5. Slide AGENDA-01 revisado reflete a estrutura final (PENDING-01 resolvido); decisão entre "4 fases EDM como sumário" ou outra estrutura formalizada
6. Deck inteiro navega do primeiro ao último slide sem quebra; em ritmo natural de defesa, tempo estimado dentro de 10 minutos

## Traceability — atualização

| Requirement | Phase |
|---|---|
| REFORMAT-01 | Phase 1 |
| REFORMAT-02 | Phase 1 |
| REFORMAT-03 | Phase 1 |
| REFORMAT-04 | Phase 1 |
| REFORMAT-05 | Phase 1 |
| MERGE-01 | Phase 1 |
| REMOVE-01 | Phase 1 |
| INTRO-01 | Phase 2 |
| INTRO-03 | Phase 2 |
| MARKER-01 | Phase 2 |
| EDA-01 | Phase 3 |
| EDA-02 | Phase 3 |
| EDA-03 | Phase 3 |
| MARKER-02 | Phase 3 |
| PENDING-02 | Phase 3 |
| MODEL-01 | Phase 4 |
| MODEL-03 | Phase 4 |
| MODEL-04 | Phase 4 |
| MODEL-05 | Phase 4 |
| CLOSE-01 | Phase 4 |
| CLOSE-02 | Phase 4 |
| CLOSE-03 | Phase 4 |
| MARKER-03 | Phase 4 |
| PENDING-04 | Phase 4 |
| TOOL-01 | Phase 5 |
| TOOL-03 | Phase 5 |
| MARKER-04 | Phase 5 |
| END-01 | Phase 5 |
| AGENDA-01 | Phase 5 |
| PENDING-01 | Phase 5 |

**Coverage:** 30 / 30 requirements mapped (100%; v1 reduzido de 37 para 30 em 2026-05-27, duas rodadas)

## Próximos passos

Após aprovação deste roadmap:
1. Rodar `/gsd-discuss-phase 1` para entrar na fase 1 (reformatação da base) com discussão e plano detalhado
2. Cada fase gera seu próprio `.planning/PHASE-N/PLAN.md` antes de executar
3. Conforme cada fase é concluída, REQUIREMENTS.md tem itens movidos para "Validated" em PROJECT.md e a tabela de Traceability acima é atualizada com o status

---
*Roadmap criado: 2026-05-27*
