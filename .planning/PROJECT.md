# Apresentação TCC 1 — Análise do aprendizado de programação via EDM

## What This Is

Apresentação de defesa do TCC 1 em reveal.js (HTML/CSS), com cerca de 10 minutos de duração, mostrando a aplicação do processo de Educational Data Mining (EDM) ao dataset CSEDM e a comparação de três modelos de Knowledge Tracing (BKT, DKT, Code-DKT). A apresentação fecha com uma proposta de ferramenta para o TCC 2 baseada em `docs/tcc2_prototipo.html`.

Público: banca avaliadora do TCC 1 no curso de Engenharia de Computação (UniFacens).

## Core Value

Slides funcionais e narrativamente claros, prontos para a defesa marcada para a próxima semana, com fidelidade científica às referências citadas. Se tudo mais falhar, o que precisa estar de pé é: HTML reveal.js abre no browser, navegação funciona, citações estão corretas e a história "problema → método → resultados → ferramenta" fecha em 10 minutos.

## Requirements

### Validated

Slides já implementados em `apresentacao/index.html` (16 sections, validados visualmente em sessões anteriores):

- ✓ Slide capa (`slide-cover-brand`)
- ✓ Slide título do TCC (`slide-title-tcc`)
- ✓ Slide Agenda (`slide-agenda`) — lista atual a revisar
- ✓ Slide Martins p1 (`slide-related` — introdução do autor)
- ✓ Slide Martins p2 ("O problema", `slide-problem`)
- ✓ Slide Martins p3 ("Dentro dos conceitos técnicos", `slide-problem`)
- ✓ Slide Zorić p1 (`slide-related` — introdução do autor)
- ✓ Slide Zorić p2 (`slide-related slide-methods` — Ferramentas e metodologias da EDM)
- ✓ Slide Zorić p3 (`slide-phases` — As quatro fases da EDM)
- ✓ Slide Yağcı p1 (`slide-related` — introdução do autor)
- ✓ Slide Yağcı p2 (`slide-related slide-bridge` — Da predição ao knowledge tracing)
- ✓ Slide Corbett & Anderson p1 (`slide-related slide-corbett`)
- ✓ Slide Corbett & Anderson p2 (`slide-related slide-corbett`)
- ✓ Slide KCGen-KT (`slide-kcfig` — KCs e dificuldades)
- ✓ Slide Code-DKT curva (`slide-fig` — curva de aprendizado)
- ✓ Slide Code-DKT atenção (`slide-code` — o que o Code-DKT "olha")
- ✓ Tema visual em `assets/theme-unifacens.css`
- ✓ Guia de estilo em `apresentacao/STYLE.md`
- ✓ Gráfico `assets/fig-codedkt-martins-curves.png`

### Active

Hipóteses até serem implementadas e validadas no browser.

**Reformatações de slides existentes:**
- [ ] **REFORMAT-01**: Martins p1 vira `> introdução` (novo padrão de cabeçalho)
- [ ] **REFORMAT-02**: Zorić p3 vira `> as quatro fases da edm` (mantém conteúdo)
- [ ] **REFORMAT-03**: Yağcı p1+p2 (consolidar se cabe) vira `> da edm ao knowledge tracing`
- [ ] **REFORMAT-04**: Martins p2 e p3 movidos para o bloco final, com cabeçalho novo (retomada problema → evidência)
- [ ] **REFORMAT-05**: Slides Code-DKT existentes (`slide-fig`, `slide-code`, `slide-kcfig`) reformatados para o bloco de modelagem/fechamento

**Consolidações:**
- [ ] **MERGE-01**: Fundir Zorić p1 + p2 num único slide com cabeçalho `> mineração de dados educacionais`

**Remoções:**
- [ ] **REMOVE-01**: Remover os 2 slides de Corbett & Anderson (1995); referenciar apenas em citação dentro do slide de cronologia que leva ao Code-DKT

**Novos slides — Fase 1 EDM (Definição do problema):**
- [ ] **NEW-01**: Slide ProgSnap2 (Price, 2020) — formato e diferencial (múltiplas tentativas do mesmo estudante)
- [ ] **NEW-02**: Slide dataset CSEDM — origem (CS1 Java), período de coleta (2019), uso na competição CSEDM 2021
- [ ] **NEW-03**: Slide Shi e o problema — modelos KT atuais usam classificação binária, ignoram código; importância da análise estrutural; 1 a 2 slides

**Marcador de fase 1 concluída:**
- [ ] **NEW-04**: Slide marcador "Definição do Problema ✓" sobre as 4 fases EDM (estilo computação a definir)

**Novos slides — Fase 2 EDM (Preparação dos dados):**
- [ ] **NEW-05**: Slide EDA — distribuição e organização do CSEDM (n estudantes, n problemas, n eventos); NÃO repete formato ProgSnap2 (já introduzido em NEW-01/INTRO-01)
- [ ] **NEW-06**: Slide pré-processamento — aproximação ao protocolo de Shi como parâmetro de comparação, com ênfase em EDM/análise
- [ ] **NEW-07**: Slide gráfico com insight sobre estudantes (qual gráfico será definido durante execução)

**Marcador de fase 2 concluída:**
- [ ] **NEW-08**: Slide marcador "Preparação dos Dados ✓"

**Novos slides — Fase 3 EDM (Modelagem):**
- [ ] **NEW-09**: Slide Code-DKT — funcionamento sucinto (sem aprofundar), predecessores (Piech DKT, BKT), vetorização code2vec via javalang
- [ ] **NEW-10**: Slide exemplo de AST (.svg já existente no projeto)
- [ ] **NEW-11**: Slide resultados Code-DKT + comparação com Shi (paper)
- [ ] **NEW-12**: Slide Duan (2025) + pipeline KCs semânticos — Duan introduz LLM-para-KC; nosso pipeline (Report 4 em `/home/leokuntz/Documents/Facens/TCC/Reports/Report 4/...pdf`, prompts inspirados no apêndice de Duan) implementa a ideia em 3 etapas; tudo num único slide (funde NEW-12 e NEW-13 originais)
- [ ] **NEW-14**: Slide gráfico ou imagem dos KCs semânticos gerados

**Fechamento (retomada problema → evidência):**
- [ ] **NEW-16**: Slide retomando Martins p2 — comparar dificuldades reportadas com KCs semânticos gerados
- [ ] **NEW-17**: Slide retomando Martins p3 — relacionar com nossos KCs
- [ ] **NEW-18**: Slide com gráfico Code-DKT (`slide-fig` existente, validar e reformatar) mostrando progressão por dificuldade

**Fase 4 EDM (Implantação no TCC 2):**
- [ ] **NEW-19**: Slide proposta da ferramenta TCC 2 + pipeline mini-horizontal — baseada em `docs/tcc2_prototipo.html`; sequência (entrada de submissões dos alunos → extração de KCs → professor valida → preparação → Code-DKT → dashboard) sem detalhar cada etapa; pipeline espelha o que já foi mostrado nas fases 2-4 (funde NEW-19 e NEW-20 originais)
- [ ] **NEW-21**: Slide dashboard — respostas de código por aluno, predição de conhecimento por estudante, dificuldade da turma por KC

**Encerramento:**
- [ ] **NEW-22**: Slide de agradecimento

**Decisões pendentes:**
- [ ] **PENDING-01**: Decidir conteúdo e forma do slide Agenda (provavelmente as 4 fases da EDM como sumário, mas a definir depois de montar os slides do meio)
- [ ] **PENDING-02**: Definir qual gráfico de insight de estudantes entra no slide NEW-07
- [ ] **PENDING-04**: Validar o gráfico Code-DKT antes do NEW-18 (memória `project_codedkt_kc_difficulty` indica re-treino por desalinhamento do `pred_df` salvo)

**Removidos de v1 em 2026-05-27 (feedback orientadora):** NEW-13 (pipeline KCs, fundido em NEW-12), NEW-15 (KCs aplicados a caso concreto, absorvido em CLOSE-01/02 via Martins return), NEW-20 (pipeline ferramenta, fundido em NEW-19), PENDING-03 (vinculado a NEW-15 cortado).

### Out of Scope

- **Texto formal do TCC (escrita ABNT)** — fora do escopo desta iteração. O foco é defesa; texto é trabalho paralelo.
- **Notebook 10 completo (KC difficulty)** — fora do escopo. Os insights necessários para os slides serão extraídos de notebooks já executados; sem rodar notebook 10 do zero.
- **Análise srcML-DKT Chat 2** — fora do escopo. Resultados do srcML já estão consolidados nas memórias; não vamos aprofundar nessa apresentação (Code-DKT é o modelo escolhido para a narrativa).
- **Export PDF dos slides** — entregável é o HTML reveal.js navegável no browser. PDF não pedido.
- **Speaker notes formais** — sem texto separado do que falar. Slides são autoexplicativos para a banca.
- **Ensaio cronometrado dentro do GSD** — validação manual no browser; cronometragem é responsabilidade do apresentador, não do roadmap.
- **Implementação da ferramenta TCC 2** — apenas a proposta visual e o pipeline são apresentados. Implementação é o TCC 2.
- **Re-execução de modelos (BKT, DKT, Code-DKT, srcML)** — resultados existentes nas memórias e em `results/` são reutilizados. Sem retreino exceto se o slide NEW-18 exigir.

## Context

- **Defesa em ~1 semana** (semana de 2026-06-01 a 2026-06-07 aproximadamente). Prazo apertado, escopo precisa ser disciplinado.
- **Apresentação atual** já tem trabalho significativo: 16 slides em `apresentacao/index.html`, tema visual em `assets/theme-unifacens.css`, manual de citações em PDF (`apresentacao/4. MSGQ-21.01...pdf`), guia de estilo em `apresentacao/STYLE.md`.
- **Pesquisa e modelagem completas**: fases anteriores do projeto produziram resultados Code-DKT, DKT, BKT, srcML-DKT, KCGen-KT e comparação final (ver memórias `project_codedkt_results`, `project_multirun_results`, `project_srcml_results`, `project_comparison_results`).
- **Memórias auto-salvas relevantes** (em `~/.claude/.../memory/MEMORY.md`):
  - `project_codedkt_kc_difficulty` — pendência de re-treino do `pred_df` para o gráfico do Code-DKT por dificuldade, 2 slides novos ligados ao Martins
  - `feedback_no_em_dashes` — sem travessões em prosa
  - `feedback_tcc_writing_style` — ABNT + prosa acessível
  - `feedback_correlatos_antes` — introduzir autor como slide correlato antes de usar resultados (revisado agora: novo padrão de cabeçalho substitui essa convenção)
  - `reference_manual_citacoes` — manual Facens, "tradução nossa" só em direta literal estrangeira
- **Material disponível em `docs/`** (papers e relatórios):
  - `Code-DKT.pdf` — Shi et al. (2022), referência principal
  - `ProgSnap2.pdf` — Price (2020), formato do dataset
  - `AutomatedKC.pdf` / `2025.EDM.short-papers.83.pdf` — Duan (2025), extração de KCs via LLM
  - `Artigo+2+Desafios+na+aprendizagem...pdf` — Martins, Marin e Alves (2024)
  - `893CorbettAnderson1995.pdf` — Corbett e Anderson (1995), citado em cronologia
  - `deepKnowledgeTracing.pdf` — Piech et al. (2015), DKT
  - `edm_review.pdf` — provavelmente Zorić (2020)
  - `edm_prediction.pdf` — provavelmente Yağcı (2022)
  - `Master_Thesis_-_Colin_Busropan.pdf`, `kt_survey.pdf`, `Benefits_of_Educational_Data_Mining.pdf`
- **Report 4** (documento de projeto EDM + KT) em `/home/leokuntz/Documents/Facens/TCC/Reports/Report 4/Report 4 - Documento de Projeto - EDM e KT.pdf`
- **Protótipo da ferramenta TCC 2** em `docs/tcc2_prototipo.html`

## Constraints

- **Timeline**: defesa em ~1 semana (deadline absoluto). Cortar antes de adicionar.
- **Duração da apresentação**: 10 minutos máximo. ~32 slides projetados (após reduções de 2026-05-27) implicam ritmo médio de ~18s por slide; CLOSE-01/02/03 (Martins return) ganham 30-40s cada por serem eixo prioritário; correlatos e MARKERs ficam abaixo da média para compensar.
- **Stack**: reveal.js + HTML/CSS puro (sem build system). Conforme `apresentacao/STYLE.md`.
- **Estilo visual obrigatório** (definido em `apresentacao/STYLE.md`):
  - Slides 1280×720
  - Cada slide em `<section><div class="deck-slide slide-XYZ">...</div></section>`
  - Paleta: `--uni-blue #2667FF`, `--uni-dark #202124`, `--uni-light #F1F6FB`, `--uni-ink #111317`
  - Tipografia: Arial para títulos/corpo, Cascadia mono para tópicos `>`
  - Marca d'água Facens nos slides de conteúdo (`<svg class="wm">`)
- **Citação ABNT** (manual MSGQ-21.01 em `apresentacao/`):
  - Direta curta entre aspas + `(Sobrenome, ano, p. X)`
  - Direta longa em parágrafo independente, sem aspas, fonte menor
  - Traduções literais de artigo estrangeiro: `(Autor, ano, p. X, tradução nossa)`
  - Paráfrase = indireta, sem "tradução nossa"
  - Legenda "Fonte:" no rodapé de cada slide com conteúdo derivado
  - Sobrenome em parênteses: inicial maiúscula; dois autores com `;`
- **Regras de redação**:
  - Termos estrangeiros em itálico minúsculas (`*knowledge tracing*`, `*code2vec*`, `*srcML*`)
  - Nomes de modelos preservados (BKT, DKT, Code-DKT)
  - **Sem em-dash** (`—`) em prosa; usar vírgula, dois-pontos ou parênteses
- **Novo padrão de cabeçalho** (esta iteração):
  - Tópico `>` + título do h2 substituídos por `> [nome da seção]` com caret piscando
  - Única menção ao autor fica no rodapé "Fonte:" (já implementado)
  - Aplica-se a todos os slides reformatados e novos

## Process Principles

Este é um trabalho científico. Os princípios abaixo são vinculantes durante a execução; violá-los compromete o rigor da defesa.

1. **Ler a referência completa antes de escrever sobre ela.** Toda vez que um slide for adicionado ou ajustado citando um autor (Martins, Zorić, Yağcí, Shi, Price, Duan, Corbett & Anderson, Piech, etc.), o agente ou o autor humano deve abrir e ler o PDF correspondente em `docs/` (ou o caminho indicado) antes de redigir ou alterar a fala. Memórias e CLAUDE.md são pistas, não substituem a fonte primária.
2. **Verificar dados antes de gravá-los nos slides.** Números, percentuais, AUCs, tamanhos de amostra e datas devem vir de notebook executado, paper conferido ou memória cruzada com fonte. Sem inventar.
3. **Citações ABNT corretas e completas.** Sobrenome, ano, página. "Tradução nossa" só em direta literal de artigo estrangeiro. Paráfrase não leva "tradução nossa".
4. **Validar visualmente cada slide no browser** após edição. Layout do reveal.js é sensível à estrutura `<section><div class="deck-slide slide-XYZ">`; quebras silenciosas existem.
5. **Versionar a cada slide concluído.** Commit atômico permite reverter slides individuais se necessário.

## Key Decisions

| Decisão | Racional | Status |
|---|---|---|
| Cabeçalho `> [seção]` substitui tópico + título h2; autor só em "Fonte:" | Reduz ruído visual e libera espaço; alinha apresentação como narrativa única, não como sequência de autores | — Pending (a aplicar) |
| Duan vem **depois** do Code-DKT | Code-DKT é o modelo core (substitui DKT/BKT). Duan é camada adicional que enriquece a interpretabilidade dos KCs. Narrativa flui melhor: "modelamos → para dar significado, extraímos KCs semânticos" | — Pending |
| Corbett & Anderson removidos como slides dedicados; citados apenas na cronologia que leva ao Code-DKT | 10 minutos não comportam 2 slides para Corbett. Citação na cronologia mantém o crédito histórico sem custo de tempo | — Pending |
| Martins p2 e p3 movidos para o bloco final (fechamento problema → evidência) | Retomar Martins ao fim amarra o problema (apontado na introdução) com a evidência (KCs semânticos e Code-DKT). História circular | — Pending |
| Yağcí é a **ponte EDM → Knowledge Tracing**; cabeçalho `> da edm ao knowledge tracing` | Yağcí trabalha predição de desempenho em EDM e cita o seguimento contínuo do estudante; serve de gancho para apresentar KT como evolução | ✓ Confirmado |
| ProgSnap2 (Price, 2020) introduzido **após o gancho do Yağcí**, antes do dataset CSEDM | Sequência didática: KT precisa de múltiplas tentativas → ProgSnap2 é o formato que armazena isso → CSEDM é a instância concreta | — Pending |
| Shi apresentado como **problema** (binário ignora código), não como modelo na primeira aparição | Foca o problema motivador. O modelo Code-DKT é apresentado depois, na fase 3 EDM (modelagem), conectando back ao problema do Shi | — Pending |
| Marcadores de fases EDM concluídas entre seções | Reforça a estrutura metodológica e dá ritmo à apresentação; estética com referência a computação a definir | — Pending |
| Agenda atual a refazer; conteúdo definitivo decidido depois | A agenda existente lista 8 seções genéricas (Introdução, Trabalhos Correlatos, etc.) que não casam mais com a nova estrutura | — Pending |
| Modo de trabalho `interactive`, granularidade `coarse`, plano e checagem habilitados, verifier desabilitado, perfil `quality` | Defesa próxima exige cuidado nos planos mas pouco overhead; verificação visual é mais rápida que agente verifier | ✓ Confirmado |
| Retomada Martins (CLOSE-01/02/03) é o eixo prioritário da defesa; TCC 2 espelha as fases anteriores sem repetir o pipeline; ProgSnap2 é nominalmente único em INTRO-01 | Feedback da orientadora 2026-05-27: 10 min é apertado, cortar detalhamentos, validar tudo no Martins antes de mostrar a ferramenta. Implicações: MODEL-06 fundido em MODEL-05 (Duan + pipeline), TOOL-02 fundido em TOOL-01 (proposta + pipeline mini-horizontal), MODEL-08 + PENDING-03 cortados, EDA-01 sem ProgSnap2, "entrada de submissões dos alunos" em vez de "entrada ProgSnap2" nas menções à ferramenta | ✓ Confirmado |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition` ou commit de fim de fase):
1. Requirements invalidados? → Mover para Out of Scope com razão
2. Requirements validados (slide aprovado no browser)? → Mover para Validated com referência da fase
3. Novos requirements emergiram? → Adicionar em Active
4. Decisões a registrar (ex.: conteúdo escolhido para Agenda, gráfico do NEW-07)? → Adicionar em Key Decisions
5. "What This Is" ainda preciso? → Atualizar se a narrativa migrou

**After milestone (defesa concluída):**
1. Revisão completa
2. Core Value ainda é a prioridade? Provavelmente migra para "iterar para o texto do TCC" — abrir novo milestone
3. Auditar Out of Scope: itens deferidos (texto do TCC, notebook 10, ferramenta TCC 2) sobem para próximo milestone

---
*Last updated: 2026-05-27 after initialization*
