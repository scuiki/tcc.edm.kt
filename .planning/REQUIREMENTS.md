# Requirements: Apresentação TCC 1 — Análise do aprendizado de programação via EDM

**Defined:** 2026-05-27
**Core Value:** Slides HTML reveal.js funcionais e narrativamente claros, prontos para defesa em ~1 semana, com fidelidade científica às referências.

## v1 Requirements

Cada requirement representa um slide a ser entregue ou uma reformatação a aplicar em `apresentacao/index.html`. Categorias correspondem aos blocos narrativos da apresentação.

**Nota 2026-05-27 (consolidação por feedback da orientadora, 1ª e 2ª rodadas):** Reduções aplicadas para caber em 10 min, priorizar a retomada Martins (CLOSE-01/02/03), garantir ProgSnap2 único, TCC 2 sem repetir o pipeline já mostrado, e voz própria (paráfrase como padrão; citação direta apenas quando a frase é o argumento). Mudanças acumuladas:
- 1ª rodada: `MODEL-06` fundido em `MODEL-05` (Duan + pipeline); `TOOL-02` fundido em `TOOL-01` (proposta + pipeline mini-horizontal); `MODEL-08` e `PENDING-03` movidos para v2 (caso concreto de KC absorvido por CLOSE-01/02).
- 2ª rodada: `INTRO-02` fundido em `INTRO-01` (CSEDM + ProgSnap2 num único slide "nosso dataset"); `MODEL-02` fundido em `MODEL-01` (Code-DKT funcionamento + AST inset); `MODEL-07` cortado (lista de KCs redundante com slide-kcfig que já mostra o mapeamento).
- Política de voz: paráfrase indireta com autor parentético é o padrão; citação direta literal só onde a frase específica é o argumento (mantida em CLOSE-01/02 porque "13 autores" / "10 autores" são o argumento quantitativo).

v1: 37 → 33 → 30 reqs.

### REFORMAT — Reformatações de slides já existentes

- [x] **REFORMAT-01**: Slide Martins p1 reformatado com cabeçalho `> introdução` (substitui tópico "trabalhos correlatos" + título "Martins, Marin e Alves (2024)"); autor mantido apenas em rodapé "Fonte:" ✓ 2026-05-27 (plan 01-04, commit `c31658c`)
- [x] **REFORMAT-02**: Slide Zorić p3 (`slide-phases`) reformatado com cabeçalho `> as quatro fases da edm`; conteúdo preservado ✓ 2026-05-27 (plan 01-05, commit `23eed8b`)
- [x] **REFORMAT-03**: Slide Yağcí (consolidado de p1 + p2 se possível) reformatado com cabeçalho `> da edm ao knowledge tracing`; conteúdo precisa puxar o gancho "acompanha o conhecimento do estudante ao longo do tempo, a cada nova tentativa". **Voz:** substituir a citação direta atual (Yağcı, 2022, p. 2, tradução nossa) por paráfrase centrada em "nós seguimos o passo seguinte" (ex.: "Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar alunos em risco. Nós seguimos o passo seguinte: em vez de uma previsão única, acompanhamos o conhecimento ao longo do tempo via knowledge tracing."). ✓ 2026-05-27 (plan 01-03, commit `b60439e`)
- [ ] **REFORMAT-04**: Slides Martins p2 ("O problema") e Martins p3 ("Dentro dos conceitos técnicos") movidos para o bloco final da apresentação; cabeçalho da seção a definir (provavelmente `> retomando o problema` ou similar). **Voz:** **MANTER as citações diretas** atuais (Martins; Marin; Alves, 2024, p. 19 e p. 20) — os números "mencionada por 13 autores" e "citado por 10 autores" SÃO o argumento quantitativo do estudo; paráfrase enfraqueceria a força retórica. Esta é a exceção legítima à política de paráfrase como padrão.
- [ ] **REFORMAT-05**: Slides `slide-fig` (curva de aprendizado Code-DKT), `slide-code` (atenção Code-DKT) e `slide-kcfig` (KCs KCGen-KT) reformatados para o bloco de modelagem/fechamento com cabeçalhos novos

### MERGE — Consolidações de slides

- [x] **MERGE-01**: Fundir slide Zorić p1 (`slide-related` introdução de autor) + slide Zorić p2 (`slide-methods` ferramentas e metodologias da EDM) num único slide com cabeçalho `> mineração de dados educacionais`. **Voz:** substituir as 2 citações diretas atuais (Zorić, 2020, p. 12, tradução nossa) por paráfrase indireta com autor parentético, centrada em "nosso trabalho aplica EDM" (ex.: "Nosso trabalho aplica o processo de Mineração de Dados Educacionais, área que combina mineração de dados, estatística e aprendizado de máquina para apoiar decisões pedagógicas (Zorić, 2020)."). ✓ 2026-05-27 (commit `f9907b8`)

### REMOVE — Slides a remover

- [x] **REMOVE-01**: Remover os 2 slides de Corbett & Anderson (1995) (`slide-related slide-corbett`); referenciar apenas em citação dentro do slide de cronologia que leva ao Code-DKT ✓ 2026-05-27 (commit `91b9675`)

### INTRO — Slides novos de introdução e dataset (Fase 1 EDM)

- [ ] **INTRO-01**: Slide "nosso dataset" (fundido) — dataset **CSEDM** (curso introdutório CS1 em Java, coleta 2019, competição CSEDM 2021) armazenado no formato **ProgSnap2** (Price, 2020), que preserva múltiplas tentativas do mesmo estudante; gancho com o que Yağcí mostrou sobre acompanhamento ao longo do tempo. Voz própria: "Nosso dataset é o CSEDM, armazenado em ProgSnap2 (Price, 2020), formato que...". (Funde INTRO-01 e INTRO-02 originais.)
- [ ] **INTRO-03**: Slide Shi e o problema — paráfrase indireta: "Shi et al. (2022) apontaram que modelos de KT clássicos (BKT, DKT) usam apenas acerto/erro e ignoram a estrutura do código; um aluno pode acertar parcialmente e o modelo ver como erro completo." 1 a 2 slides conforme cabimento; NÃO apresenta o modelo Code-DKT aqui

### MARKER — Marcadores de fase EDM concluída

- [ ] **MARKER-01**: Slide marcador após INTRO-03 sinalizando "Definição do Problema ✓" sobre as 4 fases da EDM; estética com referência a computação (a definir)
- [ ] **MARKER-02**: Slide marcador após EDA sinalizando "Preparação dos Dados ✓"
- [ ] **MARKER-03**: Slide marcador após CLOSE-03 sinalizando "Modelagem e Avaliação ✓" (fim da fase 3 da EDM, antes de entrar na proposta da ferramenta TCC 2)
- [ ] **MARKER-04**: Slide marcador após TOOL-03 sinalizando "Implantação ✓" (fim da fase 4 da EDM, antes do agradecimento)

### EDA — Slides novos de Fase 2 EDM (Preparação dos dados)

- [ ] **EDA-01**: Slide EDA — distribuição e organização do dataset CSEDM (n estudantes, n problemas, n eventos); mencionar que encontramos a base via Shi. NÃO repetir formato ProgSnap2 (já introduzido em INTRO-01).
- [ ] **EDA-02**: Slide pré-processamento — justificar aproximação ao protocolo de Shi como parâmetro de comparação ("benchmark") mas com ênfase em EDM e análise; apresentar etapas de pré-processamento aplicadas
- [ ] **EDA-03**: Slide gráfico com insight sobre estudantes (qual gráfico será decidido durante execução, ver PENDING-02)

### MODEL — Slides novos de Fase 3 EDM (Modelagem)

- [ ] **MODEL-01**: Slide Code-DKT funcionamento + AST como inset visual — citar predecessores (Corbett & Anderson 1995 BKT, Piech 2015 DKT) na cronologia que leva ao Code-DKT; mostrar inset com a `.svg` de AST de exemplo já existente no projeto demonstrando "o Code-DKT parseia o código como árvore"; vetorização code2vec via javalang; sem aprofundar tecnicamente. (Funde MODEL-01 e MODEL-02 originais.)
- [ ] **MODEL-03**: Slide visualização Code-DKT em código (a partir do `slide-code` existente, reformatado)
- [ ] **MODEL-04**: Slide resultados Code-DKT + comparação direta com Shi et al. (2022)
- [ ] **MODEL-05**: Slide Duan (2025) + pipeline de KCs semânticos — Duan introduz extração automática de KCs via LLM; nosso pipeline (baseado em Report 4 em `/home/leokuntz/Documents/Facens/TCC/Reports/Report 4/...pdf`, prompts inspirados no apêndice de Duan) implementa essa ideia em 3 etapas; importância dos KCs semânticos para interpretabilidade. Voz própria: "Duan et al. (2025) propuseram X. Nosso pipeline implementa essa ideia em 3 etapas: ...". Nota privada (NÃO no slide): ASTs não inclusas nos prompts, falar apenas se a banca perguntar. (Funde MODEL-05 e MODEL-06 originais.) A saída do pipeline (KCs gerados + mapeamento com dificuldades) é mostrada no slide-kcfig (REFORMAT-05a) que aparece em seguida no deck.

### CLOSE — Fechamento (retomada problema → evidência)

- [ ] **CLOSE-01**: Slide Martins p2 (existente, reformatado) — retomar dificuldades reportadas em conceitos técnicos e comparar com os KCs semânticos gerados
- [ ] **CLOSE-02**: Slide Martins p3 (existente, reformatado) — relacionar subcategorias de dificuldades com nossos KCs
- [ ] **CLOSE-03**: Slide com gráfico Code-DKT por dificuldade (do `slide-fig` existente, reformatado) — validar o gráfico antes de incluir, ver PENDING-04

### TOOL — Fase 4 EDM (Implantação, proposta TCC 2)

- [ ] **TOOL-01**: Slide proposta da ferramenta TCC 2 — baseada em `docs/tcc2_prototipo.html`; inclui sequência mini-horizontal das etapas (entrada de submissões dos alunos → extração automática de KCs → professor valida → preparação → Code-DKT → dashboard) sem detalhar cada uma; pipeline espelha o que já foi mostrado nas fases 2-4, não repete conteúdo. (Funde TOOL-01 e TOOL-02 originais; "entrada de submissões dos alunos" substitui "entrada ProgSnap2 do professor" porque ProgSnap2 nominalmente só em INTRO-01.)
- [ ] **TOOL-03**: Slide dashboard — respostas de código da turma, predição de conhecimento por estudante, dificuldade da turma por KC; auxilia o professor a direcionar aulas

### END — Encerramento

- [ ] **END-01**: Slide de agradecimento

### AGENDA — Sumário da apresentação

- [ ] **AGENDA-01**: Slide Agenda revisado refletindo a estrutura final (provavelmente as 4 fases da EDM como sumário); conteúdo definitivo decidido após os demais slides estarem prontos, ver PENDING-01

### PENDING — Decisões pendentes

- [ ] **PENDING-01**: Decidir conteúdo e forma do slide Agenda
- [ ] **PENDING-02**: Definir qual gráfico de insight de estudantes entra no slide EDA-03
- [ ] **PENDING-04**: Validar o gráfico Code-DKT antes de incluir no CLOSE-03 (memória `project_codedkt_kc_difficulty` indica re-treino por desalinhamento do `pred_df` salvo; precisa conferir se é bloqueante ou se o gráfico existente serve)

## v2 Requirements

Deferidos para depois da defesa.

### TEXT — Texto formal do TCC

- **TEXT-01**: Escrita ABNT do capítulo de metodologia
- **TEXT-02**: Escrita ABNT do capítulo de resultados e discussão
- **TEXT-03**: Escrita ABNT da conclusão

### NB10 — Notebook 10 completo

- **NB10-01**: Re-treino do Code-DKT com `pred_df` alinhado para gerar curva de dificuldade por KC consistente
- **NB10-02**: Análise AFM (Additive Factor Model) como problema distinto de oportunidade, se decidido prosseguir

### FUSED — Removidos de v1 em 2026-05-27 (feedback orientadora)

**1ª rodada:**
- **MODEL-06 (fundido em MODEL-05)**: pipeline de extração de KCs semânticos baseado em Report 4. Conteúdo absorvido no MODEL-05 expandido.
- **MODEL-08 (cortado, eventualmente recoverable)**: caso concreto de KCs semânticos por estudante/assignment/problema. Aplicação dos KCs já aparece em CLOSE-01/02 via Martins return.
- **PENDING-03 (some com MODEL-08)**: definição do formato do slide MODEL-08.
- **TOOL-02 (fundido em TOOL-01)**: pipeline da ferramenta. Pipeline mini-horizontal absorvido no TOOL-01 expandido; detalhamento por etapa não repete porque já apareceu nas fases 2-4.

**2ª rodada:**
- **INTRO-02 (fundido em INTRO-01)**: dataset CSEDM (origem, período, competição). Absorvido no INTRO-01 expandido como "nosso dataset CSEDM armazenado em ProgSnap2".
- **MODEL-02 (fundido em MODEL-01)**: slide isolado da AST de exemplo. Vira inset visual no slide de funcionamento do Code-DKT.
- **MODEL-07 (cortado, redundante)**: gráfico/lista dos KCs gerados pela pipeline. Slide-kcfig (REFORMAT-05a) JÁ mostra todos os KCs no mapeamento com dificuldades de Martins, estritamente mais informativo.

### SRC — srcML-DKT Chat 2

- **SRC-01**: Análise pendente do déficit do srcML (vocabulário de tags XML genéricas) versus Code-DKT

### EXPORT — Entregáveis adicionais

- **EXPORT-01**: PDF exportado dos slides para envio à banca
- **EXPORT-02**: Speaker notes formais por slide

### TCC2 — Implementação do TCC 2

- **TCC2-01**: Implementar pipeline da ferramenta (toda a TOOL-* desta apresentação)

## Out of Scope

Explicitamente fora desta iteração.

| Item | Razão |
|---|---|
| Texto do TCC (capítulos ABNT) | Foco é defesa; texto é trabalho paralelo, vira milestone próprio |
| Notebook 10 completo | Insights necessários extraídos de notebooks já executados; sem rodar do zero |
| Análise srcML-DKT Chat 2 | Code-DKT é o modelo escolhido para a narrativa; srcML fica como linha lateral nas memórias |
| Export PDF dos slides | Entregável é HTML reveal.js navegável; PDF não solicitado |
| Speaker notes formais | Slides autoexplicativos; cronometragem é responsabilidade do apresentador |
| Ensaio cronometrado dentro do GSD | Validação manual no browser; fora do roadmap automatizado |
| Implementação da ferramenta TCC 2 | Apenas a proposta visual é apresentada; código é o próximo TCC |
| Retreino de modelos BKT/DKT/Code-DKT/srcML | Resultados existentes nas memórias e em `results/` são reutilizados |

## Traceability

Mapeamento requirement → fase do roadmap. Preenchido durante a criação do `ROADMAP.md`.

| Requirement | Phase | Status |
|---|---|---|
| REFORMAT-01 | Phase 1 | Completed (`c31658c`, 2026-05-27) |
| REFORMAT-02 | Phase 1 | Completed (`23eed8b`, 2026-05-27) |
| REFORMAT-03 | Phase 1 | Completed (`b60439e`, 2026-05-27) |
| REFORMAT-04 | Phase 1 | Pending |
| REFORMAT-05 | Phase 1 | Pending |
| MERGE-01 | Phase 1 | Completed (`f9907b8`, 2026-05-27) |
| REMOVE-01 | Phase 1 | Completed (`91b9675`, 2026-05-27) |
| INTRO-01 | Phase 2 | Pending (funde antigo INTRO-01+INTRO-02) |
| INTRO-03 | Phase 2 | Pending |
| MARKER-01 | Phase 2 | Pending |
| MARKER-02 | Phase 3 | Pending |
| MARKER-03 | Phase 4 | Pending |
| MARKER-04 | Phase 5 | Pending |
| EDA-01 | Phase 3 | Pending |
| EDA-02 | Phase 3 | Pending |
| EDA-03 | Phase 3 | Pending |
| MODEL-01 | Phase 4 | Pending (funde antigo MODEL-01+MODEL-02) |
| MODEL-03 | Phase 4 | Pending |
| MODEL-04 | Phase 4 | Pending |
| MODEL-05 | Phase 4 | Pending (funde antigo MODEL-05+MODEL-06) |
| CLOSE-01 | Phase 4 | Pending |
| CLOSE-02 | Phase 4 | Pending |
| CLOSE-03 | Phase 4 | Pending |
| TOOL-01 | Phase 5 | Pending (funde antigo TOOL-01+TOOL-02) |
| TOOL-03 | Phase 5 | Pending |
| END-01 | Phase 5 | Pending |
| AGENDA-01 | Phase 5 | Pending |
| PENDING-01 | Phase 5 | Pending |
| PENDING-02 | Phase 3 | Pending |
| PENDING-04 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 30 total (era 37, reduzido em 2026-05-27 em duas rodadas de feedback da orientadora)
- Mapped to phases: 30
- Unmapped: 0 ✓
- Removidos / fundidos (1ª rodada): MODEL-06 (fundido em MODEL-05), MODEL-08 (movido para v2), PENDING-03 (movido para v2 com MODEL-08), TOOL-02 (fundido em TOOL-01)
- Removidos / fundidos (2ª rodada): INTRO-02 (fundido em INTRO-01), MODEL-02 (fundido em MODEL-01), MODEL-07 (cortado, redundante com slide-kcfig)

---
*Requirements defined: 2026-05-27*
*Last updated: 2026-05-27 after initialization*
