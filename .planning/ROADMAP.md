# Roadmap: Apresentação TCC 1 — Análise do aprendizado de programação via EDM

**Created:** 2026-05-27
**Mode:** Vertical MVP (cada fase entrega slides funcionais ponta a ponta no browser)
**Total phases:** 5
**Total v1 requirements mapped:** 37 / 37

## Visão geral

Cinco fases organizadas em ordem narrativa (do reuso ao encerramento), cada uma entregando um conjunto de slides que carrega no browser sem quebra. A fase 1 prepara a base (slides existentes ajustados); fases 2 a 5 cobrem as 4 fases da EDM na ordem da apresentação. Validação visual no browser a cada fase concluída.

| # | Fase | Goal | Reqs | Mode |
|---|---|---|---|---|
| 1 | Reformatação da base | Slides existentes ajustados ao novo padrão de cabeçalho, com Zorić fundido e Corbett removido | 7 | mvp |
| 2 | Intro, Dataset e Problema (Fase 1 EDM) | Novos slides da abertura narrativa: Yağcí ponte → ProgSnap2 → CSEDM → Shi problema, fechando com marcador da Fase 1 EDM | 4 | mvp |
| 3 | EDA e Pré-processamento (Fase 2 EDM) | Slides de análise exploratória, pré-processamento e um insight visual sobre os estudantes, fechando com marcador da Fase 2 EDM | 5 | mvp |
| 4 | Modelagem e Avaliação (Fase 3 EDM) | Code-DKT + KCs semânticos via Duan + retomada de Martins (problema → evidência), fechando com marcador da Fase 3 EDM | 14 | mvp |
| 5 | Implantação, Agenda e Encerramento (Fase 4 EDM) | Proposta da ferramenta TCC 2, dashboard, marcador final, agradecimento e revisão da Agenda | 7 | mvp |

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

### Phase 2: Intro, Dataset e Problema (Fase 1 EDM)
**Goal:** Adicionar os novos slides da abertura narrativa que estabelecem o problema: o gancho do Yağcí leva ao formato ProgSnap2 (Price 2020), depois ao dataset CSEDM (CS1 Java, competição 2021, 2019), depois ao problema apontado por Shi (KT binário ignora código). Fecha com o marcador da Fase 1 EDM concluída.
**Mode:** mvp
**Requirements**: INTRO-01, INTRO-02, INTRO-03, MARKER-01
**Success Criteria**:
1. Slide ProgSnap2 carrega, cita Price (2020) em "Fonte:" e explica o diferencial de múltiplas tentativas do mesmo estudante (citação ABNT conferida em `docs/ProgSnap2.pdf`)
2. Slide dataset CSEDM apresenta origem (CS1 Java), período de coleta (2019) e contexto da competição CSEDM 2021
3. Slide(s) Shi e o problema apresentam que modelos KT atuais usam classificação binária e ignoram código; texto conferido em `docs/Code-DKT.pdf`; modelo Code-DKT NÃO é apresentado neste slide
4. Slide MARKER-01 mostra as 4 fases da EDM com "Definição do Problema" sinalizado como concluído, com estética computação-themed definida durante execução
5. Sequência completa do deck (REFORMAT base + nova abertura) navega do início ao slide MARKER-01 sem quebra

### Phase 3: EDA e Pré-processamento (Fase 2 EDM)
**Goal:** Adicionar os slides de análise exploratória e pré-processamento do dataset, incluindo um gráfico que comunica um insight legítimo sobre os estudantes. Fecha com o marcador da Fase 2 EDM concluída.
**Mode:** mvp
**Requirements**: EDA-01, EDA-02, EDA-03, MARKER-02, PENDING-02
**Success Criteria**:
1. Slide EDA-01 apresenta distribuição e organização do CSEDM com números corretos (validados em notebook ou memórias)
2. Slide EDA-02 justifica a aproximação ao protocolo de Shi como parâmetro de comparação, listando etapas concretas de pré-processamento aplicadas
3. Slide EDA-03 exibe um gráfico com insight sobre os estudantes; gráfico escolhido junto com o autor (PENDING-02 resolvido) e fonte de dados validada
4. Slide MARKER-02 mostra "Preparação dos Dados" sinalizado como concluído
5. Deck navega do início até MARKER-02 sem quebra

### Phase 4: Modelagem e Avaliação (Fase 3 EDM)
**Goal:** Apresentar Code-DKT (modelo escolhido) com cronologia de antecessores, AST, atenção, resultados e comparação com Shi. Em seguida, apresentar a extração automática de KCs semânticos via LLM (Duan), pipeline e aplicação a caso concreto. Encerrar retomando Martins (CLOSE-01/02/03) para amarrar problema → evidência, e fechar com o marcador da Fase 3 EDM concluída.
**Mode:** mvp
**Requirements**: MODEL-01, MODEL-02, MODEL-03, MODEL-04, MODEL-05, MODEL-06, MODEL-07, MODEL-08, CLOSE-01, CLOSE-02, CLOSE-03, MARKER-03, PENDING-03, PENDING-04
**Success Criteria**:
1. Slide MODEL-01 cita predecessores na cronologia (Corbett & Anderson 1995 BKT, Piech 2015 DKT) e introduz Code-DKT (Shi 2022) sucintamente; vetorização code2vec via javalang mencionada
2. Slide MODEL-02 inclui a `.svg` de AST de exemplo já existente no projeto
3. Slide MODEL-03 reaproveita o `slide-code` ("O que o Code-DKT olha") com cabeçalho novo
4. Slide MODEL-04 mostra os resultados que tivemos lado a lado com os resultados de Shi (memória `project_codedkt_results`: A439 first_auc=72.55%, dentro da margem ±3% do paper)
5. Slide MODEL-05 introduz Duan (2025) e a importância dos KCs semânticos; citação conferida em `docs/AutomatedKC.pdf` ou `docs/2025.EDM.short-papers.83.pdf`
6. Slide MODEL-06 apresenta a pipeline de extração de KCs semânticos baseada no Report 4 (`/home/leokuntz/Documents/Facens/TCC/Reports/Report 4/...pdf`); nota privada sobre ausência de ASTs nos prompts mantida fora do slide (só falar se a banca perguntar)
7. Slides MODEL-07 e MODEL-08 mostram os KCs semânticos gerados (gráfico/imagem) e seu valor em caso concreto (estudante/assignment/problem); formato do MODEL-08 decidido durante execução (PENDING-03 resolvido)
8. Slides CLOSE-01 (Martins p2 reposicionado), CLOSE-02 (Martins p3 reposicionado) e CLOSE-03 (gráfico Code-DKT por dificuldade) fecham a sequência de modelagem amarrando o problema do Martins com a evidência dos nossos KCs e do Code-DKT
9. Gráfico do CLOSE-03 validado antes da inclusão (PENDING-04 resolvido); se o `pred_df` existente não estiver alinhado, decidir entre regerar ou usar gráfico alternativo
10. Slide MARKER-03 mostra "Modelagem e Avaliação" sinalizado como concluído
11. Deck navega do início até MARKER-03 sem quebra

### Phase 5: Implantação, Agenda e Encerramento (Fase 4 EDM)
**Goal:** Apresentar a proposta da ferramenta TCC 2 (baseada em `docs/tcc2_prototipo.html`), o pipeline e o dashboard. Fechar com o marcador da Fase 4 EDM, agradecimento, e revisar a Agenda inicial para refletir a estrutura final entregue.
**Mode:** mvp
**Requirements**: TOOL-01, TOOL-02, TOOL-03, MARKER-04, END-01, AGENDA-01, PENDING-01
**Success Criteria**:
1. Slide TOOL-01 apresenta a ferramenta proposta para o TCC 2, baseada em `docs/tcc2_prototipo.html`
2. Slide TOOL-02 mostra o pipeline completo: entrada ProgSnap2 do professor → extração automática de KCs → professor valida → preparação → Code-DKT → dashboard
3. Slide TOOL-03 mostra o dashboard com respostas de código da turma, predição por estudante e dificuldade por KC
4. Slide MARKER-04 mostra "Implantação" sinalizado como concluído
5. Slide END-01 de agradecimento encerra a apresentação
6. Slide AGENDA-01 revisado reflete a estrutura final (PENDING-01 resolvido); decisão entre "4 fases EDM como sumário" ou outra estrutura formalizada
7. Deck inteiro navega do primeiro ao último slide sem quebra; em ritmo natural de defesa, tempo estimado dentro de 10 minutos

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
| INTRO-02 | Phase 2 |
| INTRO-03 | Phase 2 |
| MARKER-01 | Phase 2 |
| EDA-01 | Phase 3 |
| EDA-02 | Phase 3 |
| EDA-03 | Phase 3 |
| MARKER-02 | Phase 3 |
| PENDING-02 | Phase 3 |
| MODEL-01 | Phase 4 |
| MODEL-02 | Phase 4 |
| MODEL-03 | Phase 4 |
| MODEL-04 | Phase 4 |
| MODEL-05 | Phase 4 |
| MODEL-06 | Phase 4 |
| MODEL-07 | Phase 4 |
| MODEL-08 | Phase 4 |
| CLOSE-01 | Phase 4 |
| CLOSE-02 | Phase 4 |
| CLOSE-03 | Phase 4 |
| MARKER-03 | Phase 4 |
| PENDING-03 | Phase 4 |
| PENDING-04 | Phase 4 |
| TOOL-01 | Phase 5 |
| TOOL-02 | Phase 5 |
| TOOL-03 | Phase 5 |
| MARKER-04 | Phase 5 |
| END-01 | Phase 5 |
| AGENDA-01 | Phase 5 |
| PENDING-01 | Phase 5 |

**Coverage:** 37 / 37 requirements mapped (100%)

## Próximos passos

Após aprovação deste roadmap:
1. Rodar `/gsd-discuss-phase 1` para entrar na fase 1 (reformatação da base) com discussão e plano detalhado
2. Cada fase gera seu próprio `.planning/PHASE-N/PLAN.md` antes de executar
3. Conforme cada fase é concluída, REQUIREMENTS.md tem itens movidos para "Validated" em PROJECT.md e a tabela de Traceability acima é atualizada com o status

---
*Roadmap criado: 2026-05-27*
