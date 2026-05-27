# Requirements: Apresentação TCC 1 — Análise do aprendizado de programação via EDM

**Defined:** 2026-05-27
**Core Value:** Slides HTML reveal.js funcionais e narrativamente claros, prontos para defesa em ~1 semana, com fidelidade científica às referências.

## v1 Requirements

Cada requirement representa um slide a ser entregue ou uma reformatação a aplicar em `apresentacao/index.html`. Categorias correspondem aos blocos narrativos da apresentação.

### REFORMAT — Reformatações de slides já existentes

- [ ] **REFORMAT-01**: Slide Martins p1 reformatado com cabeçalho `> introdução` (substitui tópico "trabalhos correlatos" + título "Martins, Marin e Alves (2024)"); autor mantido apenas em rodapé "Fonte:"
- [ ] **REFORMAT-02**: Slide Zorić p3 (`slide-phases`) reformatado com cabeçalho `> as quatro fases da edm`; conteúdo preservado
- [ ] **REFORMAT-03**: Slide Yağcí (consolidado de p1 + p2 se possível) reformatado com cabeçalho `> da edm ao knowledge tracing`; conteúdo precisa puxar o gancho "acompanha o conhecimento do estudante ao longo do tempo, a cada nova tentativa"
- [ ] **REFORMAT-04**: Slides Martins p2 ("O problema") e Martins p3 ("Dentro dos conceitos técnicos") movidos para o bloco final da apresentação; cabeçalho da seção a definir (provavelmente `> retomando o problema` ou similar)
- [ ] **REFORMAT-05**: Slides `slide-fig` (curva de aprendizado Code-DKT), `slide-code` (atenção Code-DKT) e `slide-kcfig` (KCs KCGen-KT) reformatados para o bloco de modelagem/fechamento com cabeçalhos novos

### MERGE — Consolidações de slides

- [ ] **MERGE-01**: Fundir slide Zorić p1 (`slide-related` introdução de autor) + slide Zorić p2 (`slide-methods` ferramentas e metodologias da EDM) num único slide com cabeçalho `> mineração de dados educacionais`

### REMOVE — Slides a remover

- [ ] **REMOVE-01**: Remover os 2 slides de Corbett & Anderson (1995) (`slide-related slide-corbett`); referenciar apenas em citação dentro do slide de cronologia que leva ao Code-DKT

### INTRO — Slides novos de introdução e dataset (Fase 1 EDM)

- [ ] **INTRO-01**: Slide ProgSnap2 — Price (2020) como fonte; explicar o formato e o diferencial de armazenar múltiplas tentativas do mesmo estudante (gancho com o que Yağcí cita sobre acompanhamento ao longo do tempo)
- [ ] **INTRO-02**: Slide dataset CSEDM — origem (curso introdutório CS1 em Java), uso na competição CSEDM 2021, período de coleta (2019); contextualizar para a banca
- [ ] **INTRO-03**: Slide Shi e o problema — modelos de KT atuais usam classificação binária e ignoram o código; aluno pode ter acertado parcialmente e o modelo vê como errado (0); 1 a 2 slides conforme cabimento; NÃO apresenta o modelo Code-DKT aqui

### MARKER — Marcadores de fase EDM concluída

- [ ] **MARKER-01**: Slide marcador após INTRO-03 sinalizando "Definição do Problema ✓" sobre as 4 fases da EDM; estética com referência a computação (a definir)
- [ ] **MARKER-02**: Slide marcador após EDA sinalizando "Preparação dos Dados ✓"

### EDA — Slides novos de Fase 2 EDM (Preparação dos dados)

- [ ] **EDA-01**: Slide EDA — distribuição e organização do dataset CSEDM; referenciar formato ProgSnap2 quando cabível; mencionar que encontramos a base via Shi
- [ ] **EDA-02**: Slide pré-processamento — justificar aproximação ao protocolo de Shi como parâmetro de comparação ("benchmark") mas com ênfase em EDM e análise; apresentar etapas de pré-processamento aplicadas
- [ ] **EDA-03**: Slide gráfico com insight sobre estudantes (qual gráfico será decidido durante execução, ver PENDING-02)

### MODEL — Slides novos de Fase 3 EDM (Modelagem)

- [ ] **MODEL-01**: Slide Code-DKT funcionamento sucinto — citar predecessores (Piech 2015 DKT, Corbett & Anderson 1995 BKT) na cronologia que leva ao Code-DKT; vetorização code2vec via javalang; sem aprofundar tecnicamente
- [ ] **MODEL-02**: Slide exemplo de AST (.svg já existente no projeto)
- [ ] **MODEL-03**: Slide visualização Code-DKT em código (a partir do `slide-code` existente, reformatado)
- [ ] **MODEL-04**: Slide resultados Code-DKT + comparação direta com Shi et al. (2022)
- [ ] **MODEL-05**: Slide Duan (2025) como fonte — extração automática de KCs via LLM; importância dos KCs semânticos para interpretabilidade
- [ ] **MODEL-06**: Slide pipeline de extração de KCs semânticos — baseado em Report 4 (`/home/leokuntz/Documents/Facens/TCC/Reports/Report 4/...pdf`); prompts inspirados no apêndice de Duan; nota privada (NÃO no slide): ASTs não inclusas nos prompts, falar apenas se a banca perguntar
- [ ] **MODEL-07**: Slide gráfico ou imagem dos KCs semânticos gerados pela pipeline
- [ ] **MODEL-08**: Slide aplicando KCs semânticos a um caso concreto (estudante, assignment ou problema); formato a pensar juntos durante execução, ver PENDING-03

### CLOSE — Fechamento (retomada problema → evidência)

- [ ] **CLOSE-01**: Slide Martins p2 (existente, reformatado) — retomar dificuldades reportadas em conceitos técnicos e comparar com os KCs semânticos gerados
- [ ] **CLOSE-02**: Slide Martins p3 (existente, reformatado) — relacionar subcategorias de dificuldades com nossos KCs
- [ ] **CLOSE-03**: Slide com gráfico Code-DKT por dificuldade (do `slide-fig` existente, reformatado) — validar o gráfico antes de incluir, ver PENDING-04

### TOOL — Fase 4 EDM (Implantação, proposta TCC 2)

- [ ] **TOOL-01**: Slide proposta da ferramenta — baseada em `docs/tcc2_prototipo.html`
- [ ] **TOOL-02**: Slide pipeline da ferramenta — entrada ProgSnap2 do professor → extração automática de KCs → professor valida (adicionar, modificar, excluir) → preparação dos dados → aplicação Code-DKT → dashboard
- [ ] **TOOL-03**: Slide dashboard — respostas de código da turma, predição de conhecimento por estudante, dificuldade da turma por KC; auxilia o professor a direcionar aulas

### END — Encerramento

- [ ] **END-01**: Slide de agradecimento

### AGENDA — Sumário da apresentação

- [ ] **AGENDA-01**: Slide Agenda revisado refletindo a estrutura final (provavelmente as 4 fases da EDM como sumário); conteúdo definitivo decidido após os demais slides estarem prontos, ver PENDING-01

### PENDING — Decisões pendentes

- [ ] **PENDING-01**: Decidir conteúdo e forma do slide Agenda
- [ ] **PENDING-02**: Definir qual gráfico de insight de estudantes entra no slide EDA-03
- [ ] **PENDING-03**: Definir formato do slide MODEL-08 (valor de KCs semânticos em caso concreto)
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
| REFORMAT-01 | TBD | Pending |
| REFORMAT-02 | TBD | Pending |
| REFORMAT-03 | TBD | Pending |
| REFORMAT-04 | TBD | Pending |
| REFORMAT-05 | TBD | Pending |
| MERGE-01 | TBD | Pending |
| REMOVE-01 | TBD | Pending |
| INTRO-01 | TBD | Pending |
| INTRO-02 | TBD | Pending |
| INTRO-03 | TBD | Pending |
| MARKER-01 | TBD | Pending |
| MARKER-02 | TBD | Pending |
| EDA-01 | TBD | Pending |
| EDA-02 | TBD | Pending |
| EDA-03 | TBD | Pending |
| MODEL-01 | TBD | Pending |
| MODEL-02 | TBD | Pending |
| MODEL-03 | TBD | Pending |
| MODEL-04 | TBD | Pending |
| MODEL-05 | TBD | Pending |
| MODEL-06 | TBD | Pending |
| MODEL-07 | TBD | Pending |
| MODEL-08 | TBD | Pending |
| CLOSE-01 | TBD | Pending |
| CLOSE-02 | TBD | Pending |
| CLOSE-03 | TBD | Pending |
| TOOL-01 | TBD | Pending |
| TOOL-02 | TBD | Pending |
| TOOL-03 | TBD | Pending |
| END-01 | TBD | Pending |
| AGENDA-01 | TBD | Pending |
| PENDING-01 | TBD | Pending |
| PENDING-02 | TBD | Pending |
| PENDING-03 | TBD | Pending |
| PENDING-04 | TBD | Pending |

**Coverage:**
- v1 requirements: 35 total
- Mapped to phases: 0
- Unmapped: 35 (a preencher no ROADMAP)

---
*Requirements defined: 2026-05-27*
*Last updated: 2026-05-27 after initialization*
