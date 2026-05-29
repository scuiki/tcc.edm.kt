# Phase 5: Implantação, Agenda e Encerramento (Fase 4 EDM) — Research

**Researched:** 2026-05-29
**Domain:** apresentação reveal.js 4.x (HTML/CSS puros, sem build), 5 slides (1 refator + 4 novos), 1 modificador CSS aditivo
**Confidence:** HIGH em tudo que toca componentes já estabelecidos (`.slide-marker`, `.bridge-seq`, `.deck-topic`, `.slide-related`); MEDIUM em decisões visuais ainda em discretion (`--planned` estética, ilustração interna TOOL-03, END-01 layout).

**Foco deste RESEARCH:** o CONTEXT.md já tem 13 decisões D-92..D-104 travadas e markup-alvo rascunhado. Este documento NÃO repete o CONTEXT — preenche os 9 GAPS técnicos que o planner precisa resolver: localização exata de classes no CSS, comparação de alternativas concretas para os pontos em discretion, ordem ótima de execução, cross-cutting de cleanup STYLE.md, checklist de validação final.

## Summary

Fase mecânica em conteúdo (zero CSS estrutural novo no fluxo de slides existentes) e cirúrgica em CSS aditivo (1 modificador `.marker-pill--planned` + possivelmente `.dash-card` + classes mínimas para `.slide-end`/`.end-thanks`/`.end-credits`/`.agenda-edm-list`). 4 plans funcionais (1 plan por slide novo: MARKER-04, AGENDA-01, END-01, TOOL-03, TOOL-01) + 1 plan de fechamento (STYLE.md + PROJECT.md). Total: 5 plans alinhado com fases 2-4.

Ordem ótima: **MARKER-04 → AGENDA-01 → END-01 → TOOL-03 → TOOL-01 → fechamento**. Razão: começa pelo mais mecânico que entrega o componente CSS aditivo (`--planned`) que pode informar a estética visual dos próximos; AGENDA-01 logo depois porque exige update em STYLE.md §"Cabeçalho..." (D-93b override) que serve de gabarito de cabeçalho para os 3 slides subsequentes; END-01 simples e minimal; TOOL-03 antes de TOOL-01 contra-intuitivamente porque define se `.bridge-seq` adaptado serve para layout de 3 painéis grandes (decisão que NÃO afeta TOOL-01, que reusa `.bridge-seq` sem dúvida) — mas se houver risco de retrabalho (ex.: ajuste visual do `.bridge-seq` que afete ambos), inverter; TOOL-01 por último porque é o slide com mais densidade textual e maior chance de iterar no checkpoint.

**Primary recommendation:** seguir a ordem MARKER-04 → AGENDA-01 → END-01 → TOOL-03 → TOOL-01 → fechamento; reusar componentes existentes ao máximo (zero CSS novo exceto `--planned` mandatório + classes mínimas opcionais); validar visualmente cada slide em checkpoint humano antes do commit; fechar a fase com plan de meta-arquivos (STYLE.md §Cabeçalho reescrito, §Inventário para 31 sections, §Gaps removido; PROJECT.md Active → Validated, novas Key Decisions).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions (D-92..D-104)

**D-92 (vocabulário "aplicação" vs "ferramenta"):** Nos slides e na fala da fase 5 usa-se "aplicação" no lugar de "ferramenta". REQ-IDs TOOL-01/TOOL-03 NÃO são renomeados; ROADMAP/REQUIREMENTS/PROJECT.md mantêm a redação histórica "ferramenta TCC 2". Apenas o conteúdo dos slides usa "aplicação".

**D-92.1 (ordem no DOM):** TOOL-01 → TOOL-03 → MARKER-04 → END-01. Marker fecha as 4 fases EDM ANTES do agradecimento. END-01 é o último slide.
**D-92.2:** Slide-agenda permanece em `#/2`; refatoração interna não desloca nada.
**D-92.3 (justificativa narrativa):** MARKER-03 fechou "Modelagem ✓" com Implantação `--running`; TOOL-01 abre a proposta; TOOL-03 mostra dashboard; MARKER-04 fecha as 4 fases (pill 4 em `--planned`); END-01 encerra.

**D-93 (AGENDA-01):**
- D-93a: 4 fases EDM como sumário (Definição do Problema, Preparação dos Dados, Modelagem e Avaliação, Implantação).
- D-93b: cabeçalho `> agenda` com caret piscando, padrão `.deck-topic`. **OVERRIDE explícito do STYLE.md linha 39-42** que exclui a AGENDA do padrão. STYLE.md §"Cabeçalho de todo slide após a AGENDA" reescrito dentro desta fase.
- D-93c: refatorar para template `.slide-related` com cabeçalho + 4 itens vertical, Arial 21-23px. Remover `agenda-side` (logo grande) e `agenda-main`. Marca d'água `<svg class="wm">` aplicada.
- D-93d: caret blink só no último item (Implantação).
- D-93e: sem "Fonte:" (Agenda é estrutural, não derivada).
- D-93f: classes `.slide-agenda`, `.agenda-side`, `.agenda-main`, `.agenda-list` órfãs — DELETAR de theme-unifacens.css se sem outros callers.

**D-94 (TOOL-01):**
- D-94a: cabeçalho `> proposta da aplicação`.
- D-94b: abertura 1ª pessoa do plural (phrasing-alvo no CONTEXT).
- D-94c: pipeline `.bridge-seq` 6 etapas (Submissões dos estudantes → Extração de KCs → Professor valida → Preparação dos dados → Code-DKT → Dashboard).
- D-94d: todas as 6 caixas neutras (sem azul UniFacens).
- D-94e: NÃO detalhar cada etapa; microcópia verbo + 1 linha curta.
- D-94f: fechamento textual opcional (corta se apertado).
- D-94g: rodapé `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.`
- D-94h: etapa 1 do pipeline diz "Submissões dos estudantes", NÃO "ProgSnap2" (gate herdado PROJECT.md Key Decision linha 183).

**D-95 (TOOL-03):**
- D-95a: cabeçalho `> dashboard da aplicação` (ou `> o dashboard`, discretion).
- D-95b: wireframe estático 3 painéis lado a lado, estilo Word/ABNT monocromático (borda 1.5px preta, cantos retos, fundo branco). SEM screenshot do `docs/tcc2_prototipo.html`. SEM cards 2x2.
- D-95c: 3 painéis nomeados (Respostas de código da turma, Predição de conhecimento por estudante, Dificuldade da turma por KC).
- D-95d: preferência `.bridge-seq` adaptado; fallback `.dash-card` se 3 caixas grandes verticais não casarem.
- D-95e: fechamento 1 frase (foco no professor).
- D-95f: rodapé `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.`

**D-96 (MARKER-04):**
- D-96a: **pill 4 (Implantação) em `--planned`**, NÃO `--done`. Razão: defesa apresenta a proposta mas o TCC 2 não foi feito; `--planned` reconhece honestamente que a Fase 4 EDM está prevista.
- D-96b: override do Deferred Idea da fase 4 (linha 349) que tinha como default "todas 4 pills `--done`".
- D-96c: CSS novo necessário: adicionar modificador **`--planned`** ao `.marker-pill` em theme-unifacens.css. Restrições: zero animação; cor cinza azulada `#5b6472` ou borda tracejada; ícone `⋯` (etc), `◯` (círculo vazio), ou calendário/relógio sem girar; badge `[planned]`.
- D-96d: aditivo (não quebra MARKER-01/02/03).
- D-96e: título `> AS QUATRO FASES DA EDM`; rodapé `Fonte: adaptado de Zorić (2020).` (idêntico ao MARKER-01/02/03).
- D-96f: pill 4 `--planned` NÃO gira (≠ `--running` da pill 4 no MARKER-03).

**D-97 (END-01):**
- D-97a: slide minimal. Fundo `#F1F6FB`. "Obrigado." centralizado vertical+horizontal, grande, Arial bold ou Cascadia.
- D-97b: sem cabeçalho (sem `.deck-topic`).
- D-97c: rodapé discreto sem "Fonte:". Conteúdo defere ao checkpoint.
- D-97d: default sem marca d'água.
- D-97e: paleta texto principal `--uni-ink` ou `--uni-blue` destaque sutil.

**D-98..D-103 (herdado):** padrão `> [seção]`, paráfrase indireta autor parentético, sem em-dash, `<i>et al.</i>` ABNT, "estudantes" não "alunos", "Fonte:" em rodapé conforme regras.

**D-104 (validação visual):** browser `cd apresentacao && python3 -m http.server 8000`; percorrer `#/0` a `#/30`. Sucesso: navegação sem erro de console, cada slide novo legível, MARKER-04 com pill 4 `--planned` sem animação distinguível de `--running`/`--pending`, END-01 minimal centralizado.

### Claude's Discretion

- **Ordem de implementação:** sugestão neutra MARKER-04 → AGENDA-01 → END-01 → TOOL-03 → TOOL-01. Alternativa: TOOL-01 primeiro porque é o mais "pesado".
- **Granularidade dos commits:** 1 plan por slide (5 plans).
- **Componente exato do wireframe TOOL-03:** `.bridge-seq` adaptado vs `.dash-card` novo. Default: tentar `.bridge-seq` primeiro.
- **Modificador `--planned`:** estética exata (cor, ícone, borda) defere ao checkpoint visual do MARKER-04.
- **Ilustração interna dos 3 painéis TOOL-03:** barras stub, scatter stub, ou só caixa-texto. Default: caixa-texto minimalista.
- **Frase de fechamento de TOOL-01 (D-94f):** opcional; corta se apertado.
- **Cabeçalho exato do TOOL-03:** `> dashboard da aplicação` vs `> o dashboard`.
- **END-01 rodapé:** minimal puro vs com créditos discretos.
- **Atualização do STYLE.md ao fim:** §"Cabeçalho..." reescrito; §Inventário para 31 sections; §Gaps reservados removido; §Classes reutilizáveis atualizado.
- **PROJECT.md ao fim:** mover REQ-IDs Active → Validated; adicionar D-92, D-93b em Key Decisions.

### Deferred Ideas (OUT OF SCOPE)

- Renomear "ferramenta" → "aplicação" em ROADMAP/REQUIREMENTS/PROJECT.md: NÃO renomear.
- Speaker notes / cronometragem (Out of Scope PROJECT.md linha 103-104).
- Bracket narrativo END-01 ↔ slide-cover-brand: opcional, não criar requirement.
- Documentar modificador `--planned` na memória `feedback_marker_design`: defere ao fim da fase.

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TOOL-01 | Proposta da aplicação + pipeline 6 etapas | Gap #2 (`.bridge-seq` com 6 etapas vs 5: análise de viabilidade visual em 1280px). Gap #6 (ordem de execução). |
| TOOL-03 | Dashboard (wireframe 3 painéis) | Gap #3 (`.bridge-seq` adaptado vs `.dash-card` novo: trade-offs; estilo Word/ABNT monocromático; ilustração interna). |
| MARKER-04 | Fase 4 EDM (pill 4 `--planned`, sem animação) | Gap #1 (modificador `--planned`: 3 alternativas concretas comparadas com base no CSS atual; critério de distinção visual `--running`/`--pending`). |
| END-01 | "Obrigado." minimal | Gap #5 (slides minimais existentes; layout flex column 1280×720; questões para checkpoint humano). |
| AGENDA-01 | Refatoração in-place de slide-agenda (`#/2`) | Gap #4 (override D-93b ao STYLE.md linha 39-42; remoção de classes órfãs; nova `.agenda-edm-list`). Resolve PENDING-01. |
| PENDING-01 | Decisão de conteúdo e forma do slide Agenda | Resolvido por D-93a (4 fases EDM como sumário). Coberto por AGENDA-01. |

</phase_requirements>

## Architectural Responsibility Map

Apresentação reveal.js é uma stack monolítica simples (HTML estático + CSS). A "responsabilidade arquitetural" mapeia onde cada capability vive:

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Conteúdo de slide (texto, citações ABNT, estrutura semântica) | `apresentacao/index.html` (markup) | — | Reveal.js consome `<section>` diretamente; sem template engine. |
| Estética / componentes reusáveis (paleta, tipografia, modificadores) | `apresentacao/assets/theme-unifacens.css` | — | CSS único; toda alteração de aparência mora aqui. |
| Convenções de citação, voz, regras de redação | `apresentacao/STYLE.md` (documentação) | — | Texto humano-legível; auditado por reviewer em cada fase. |
| Inventário de slides | `apresentacao/STYLE.md` §Inventário | `.planning/STATE.md` (cronologia) | STYLE.md é a fonte canônica; STATE.md espelha apenas o status de plans. |
| Persistência de decisões de fase | `.planning/phases/05-*/05-CONTEXT.md` (locked) | `.planning/PROJECT.md` Key Decisions (top-level) | Phase CONTEXT.md é o detalhe; PROJECT.md guarda as duas-três mais relevantes para o projeto inteiro. |
| Validação visual | browser local (`python3 -m http.server`) | — | Sem CI/test runner; reviewer humano é o gate. |
| Gates de compliance (sem em-dash, ABNT, "estudantes") | CLAUDE.md (vinculante) + STYLE.md (operacional) + memórias auto-feedback | — | Cross-cutting: cada plan herda. |

**Implicação para o planner:** cada plan da fase 5 toca 1-3 arquivos no máximo (index.html sempre; theme-unifacens.css apenas em MARKER-04 + AGENDA-01 + END-01 com classes mínimas + TOOL-03 condicionalmente; STYLE.md em AGENDA-01 D-93b + plan de fechamento; PROJECT.md apenas no plan de fechamento). Sem cross-tier work.

## Standard Stack

Não se aplica `Standard Stack` no sentido de bibliotecas — stack já travada nas fases 1-4. Para esta fase, as **classes CSS reusáveis travadas** funcionam como o stack equivalente:

### Componentes prontos (zero CSS novo necessário)
| Classe / componente | Localização | Onde reusa nesta fase | Por que é padrão |
|---|---|---|---|
| `.deck-topic` + `.caret.blink` | theme-unifacens.css linhas 42-51 | AGENDA-01, TOOL-01, TOOL-03 | Padrão `> [seção]` único travado em D-04..D-11 (fase 1); D-93b estende à AGENDA |
| `.slide-related` (template + `.wm` + `.rel-lead` + `.rel-cite`) | theme-unifacens.css linhas 162-182 | AGENDA-01 refatorado, TOOL-01, TOOL-03 wrapper | Template canônico de slide de conteúdo desde fase 1 |
| `.slide-marker` + `.marker-track` + `.marker-stage` + `.marker-pill` + `.marker-pill-icon` + `.marker-pill-name` + `.marker-arrow` + `.marker-badge` + `.marker-title` | theme-unifacens.css linhas 364-448 | MARKER-04 | Componente CI/CD ABNT travado pelo redesign commit `5d44606` (D-67, D-84) |
| `.marker-pill--done` / `.marker-pill--running` / `.marker-pill--pending` | theme-unifacens.css linhas 408-428 | MARKER-04 reusa `--done` (×3); `--planned` é NOVO (D-96c) | Modificadores adicionam estado sem quebrar pill base |
| `.bridge-seq` + `.step` + `.arr` | theme-unifacens.css linhas 197-206 (inicial `.slide-bridge`); MODEL-05 mostra reuso via `.slide-related slide-bridge` + inline-style | TOOL-01 (6 etapas), candidato para TOOL-03 (3 painéis adaptado) | Padrão Word/ABNT monocromático estabelecido (D-79l..p) |
| Marca d'água `<svg class="wm">` + symbol `#sym` | index.html linhas 16-21 + CSS `.wm` em vários slides | AGENDA-01, TOOL-01, TOOL-03 | Identidade Facens em todos os slides de conteúdo |

### Classes/modificadores NOVOS desta fase (CSS aditivo)
| Classe / modificador | Mandatório? | Localização sugerida no CSS | Why |
|---|---|---|---|
| `.marker-pill--planned` | **Sim** (D-96c) | Após `.marker-pill--pending` em linhas 422-428, antes de `.marker-arrow` linha 430 | MARKER-04 não pode renderizar sem ele |
| `.agenda-edm-list` (lista numerada vertical) | **Sim** (D-93c) | Após bloco `.slide-agenda` legacy ou bloco `.slide-related` | Lista 4 fases EDM padronizada |
| `.slide-end` + `.end-thanks` + `.end-credits` | **Sim** (D-97a) | Bloco novo separado | END-01 não cabe no template `.slide-related` (sem cabeçalho, layout centralizado) |
| `.dash-card` | **Opcional** (D-95d fallback) | Bloco novo após `.bridge-seq` se necessário | Apenas se `.bridge-seq` adaptado não casar para 3 painéis grandes em TOOL-03 |

### Versionamento e dependências (verificado)
- reveal.js 5.1.0 carregado via CDN (jsdelivr) — index.html linhas 8-10. Não atualizar nesta fase.
- @fontsource/cascadia-code 5 (400 + 700) — index.html linhas 9-10.
- Sem npm/build system. Servir com `python3 -m http.server`.

**Stack verification:** zero novos CDNs; zero novos arquivos JS; zero JS animation além do existente (`marker-spin` permanece para `--running`, NÃO para `--planned`).

## Architecture Patterns

### Estrutura padrão de slide (canônica, NUNCA mudar)

```html
<!-- ============ SLIDE · descrição curta ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-XYZ">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>nome da seção<span class="caret blink"></span></p>

    <!-- corpo do slide -->

    <p class="rel-cite">Fonte: ...</p>
  </div>
</section>
```

### Padrão de slide marcador (template para MARKER-04)

Idêntico ao MARKER-03 (index.html linhas 687-730), com 3 deltas:
1. classe modificadora `slide-marker--phase3` → `slide-marker--phase4`
2. pill 3 mantém `--done` (não muda)
3. pill 4 muda de `marker-pill--running` (ícone `&#x21BB;`, badge `[running]`) para **`marker-pill--planned`** (ícone defere ao checkpoint, badge `[planned]`)

### Padrão de pipeline `.bridge-seq` (template para TOOL-01)

Referência MODEL-05 (index.html linhas 540-550): `.slide-related slide-bridge` wrapper + `.bridge-seq` parágrafo com 5 `.step` (flex-direction column inline) + 4 `.arr` setas. Para TOOL-01 com 6 etapas: mesma estrutura, +1 `.step` + +1 `.arr`.

### Anti-Patterns to Avoid

- **Adicionar `<h2>` interno em slide com `.deck-topic`** — viola D-03 herdado (fase 1). Cabeçalho é único.
- **Aplicar animação a `--planned`** — viola D-96f. Não deve girar nem pulsar.
- **Tentar embutir "ProgSnap2" em TOOL-01** — gate forte D-94h herdado de PROJECT.md Key Decision linha 183.
- **Renomear REQ-IDs TOOL-01/TOOL-03 para algo com "aplicação"** — IDs são identificadores estáveis, D-92 deixou claro.
- **Usar em-dash (—) em qualquer prosa nova** — gate D-100, memória `feedback_no_em_dashes`.
- **Usar "alunos" em vez de "estudantes"** — gate D-102, memória `feedback_estudantes_nao_alunos`.
- **Mudar `<section><div class="deck-slide ...">` para variações exóticas** — reveal.js força `display:block` na section; layout precisa do div interno (STYLE.md linha 12-13).
- **Importar CSS externo ou adicionar classes utilitárias estilo Tailwind** — manter coesão visual; toda regra mora em theme-unifacens.css.

## Don't Hand-Roll

| Problema | Don't Build | Use Instead | Why |
|---|---|---|---|
| Estado visual de fase (done/running/planned/pending) | CSS de cores manualmente por slide | Modificador novo na linha de `.marker-pill--done`/`--running`/`--pending` | Padrão CI/CD ABNT estabelecido (commit `5d44606`); mais 1 modificador é aditivo |
| Pipeline horizontal de N etapas com setas | flex/grid manual ou desenhar SVG | `.bridge-seq` + `.step` + `.arr` | Componente canônico desde fase 1 (Yağcí) e fase 4 (MODEL-05); 5 etapas já validado |
| Tabela ABNT em slide | tabela com bordas todas + cor de fundo | `.eda-grid` + `.eda-title` + `.eda-source` | Padrão IBGE 1993 (Manual MSGQ-21.01 p.22) já no CSS — porém esta fase NÃO usa tabela |
| Cabeçalho de seção do slide | `<h2>` + tópico kicker separado | `.deck-topic` único com caret blink | D-04..D-11 fase 1; D-93b estende a AGENDA |
| Lista numerada de seções | `<ol>` com `list-style: decimal` simples | `.agenda-edm-list` ou reuso de `.phases-list` (slide Zorić p3) | `.phases-list` já tem contador numerado azul + Arial 23px; pode servir de gabarito CSS |
| Marca d'água Facens em slide novo | importar logo PNG | `<svg class="wm"><use href="#sym"/></svg>` + classe `.wm` | Symbol `#sym` definido uma vez no topo do index.html |
| Caret piscante | implementar animation custom | `<span class="caret blink"></span>` | CSS travado em linhas 45-51 |

**Key insight:** quase 100% desta fase é composição de componentes já existentes; a única "construção" mandatória é o modificador `.marker-pill--planned` (CSS aditivo de ~5 linhas).

## Common Pitfalls

### Pitfall 1: subestimar o impacto visual de 6 etapas no `.bridge-seq` (Gap #2)
**What goes wrong:** assumir que `.bridge-seq` com `flex: 1 1 0` "auto-adapta" e 6 etapas + 5 setas cabem confortavelmente em 1280px.
**Why it happens:** o template MODEL-05 tem 5 etapas com texto Arial 19px + `padding: 16px 14px`; com `display:flex; gap: 0; justify-content: center`, o conteúdo se distribui na largura disponível do `.slide-related` (max-width `.rel-lead` 1060px, slide útil ~1152px após padding 64+64). Com 5 etapas: cada step tem ~190-200px disponíveis para o conteúdo (descontando 4 setas ~26px × 4 = 104px + padding interno 28px × 5 = 140px → ~600px de margem para texto em 5 boxes = ~120px/box). Com 6 etapas: 5 setas (~130px) + padding 168px → ~830px para texto em 6 boxes = ~138px de média; menos espaço por caixa.
**How to avoid:** durante o plan TOOL-01, validar no browser com microcópia compacta (Submissões / Extração KCs / Professor valida / Preparação / Code-DKT / Dashboard — todas curtas: 1-2 palavras + 1 linha de descrição). Se houver overflow horizontal: opções (em ordem de preferência):
  1. Reduzir fonte do `.step` de 19px para 17px inline (`style="font-size:17px"`)
  2. Reduzir padding inline `padding: 12px 10px`
  3. Comprimir microcópia (remover descrição secundária para algumas etapas)
  4. (último recurso) anexar `.bridge-seq--6step` em CSS com regras específicas
**Warning signs:** texto quebrando em mais de 2 linhas, setas comprimidas, scrollbar horizontal aparecendo.

### Pitfall 2: `.marker-pill--planned` colidir visualmente com `--pending` (Gap #1)
**What goes wrong:** escolher cinza neutro `#5b6472` (idêntico ao `--pending`) para `--planned`; reviewer não consegue distinguir no MARKER-04.
**Why it happens:** `--pending` (linhas 422-428) usa `color: #5b6472` no texto + `border: 1.5px solid #5b6472` + ícone `&#x25CB;` (círculo vazio). Se `--planned` usar a mesma cor, fica idêntico.
**How to avoid:** criar 1 dos 3 padrões distinguíveis (3 alternativas a comparar no checkpoint, ver §"Code Examples" abaixo):
  - **Alt A (recomendada):** cor cinza azulado `#5b6472` + **borda tracejada** `border-style: dashed` + ícone `&#x25CB;` (mesmo do pending, mas dashed); badge `[planned]`. Comunica "estado futuro previsto" sem inventar nova cor.
  - **Alt B:** cor `--uni-blue` em opacity 0.5 + borda sólida + ícone `&#x21BB;` (mesmo do running mas SEM animação). Risco: pode confundir com `--running` se animação for sutil.
  - **Alt C:** cor cinza azulado + borda sólida + ícone novo (calendário, relógio, ou `⋯`); badge `[planned]`. Risco: ícone novo agrega ruído visual.
**Recomendação:** Alt A (borda tracejada). Menor risco, máxima distinção, aditivo puro.
**Warning signs:** no checkpoint do MARKER-04, pedir ao reviewer para olhar a tela de longe (3m) e identificar qual pill é qual.

### Pitfall 3: remover classes `.slide-agenda` / `.agenda-side` / `.agenda-main` / `.agenda-list` sem confirmar que não há caller externo
**What goes wrong:** deletar do CSS e descobrir que algum outro slide usa.
**Why it happens:** falsa premissa de que grep encontra 100% dos casos (e.g., se houver `<div class="agenda-side">` em outro arquivo HTML não rastreado).
**How to avoid:** o grep documentado abaixo confirma que essas 4 classes só aparecem no slide-agenda (linhas 62-80 do index.html) e no próprio CSS (4 declarações). Após refatorar AGENDA-01 (que remove o markup interno), as 4 declarações ficam órfãs. Mesmo paralelo do cleanup `.rel-kicker/.rel-title/.rel-sub` da fase 1 (commit `30ba911`). **Confirmar grep no plan AGENDA-01 antes do commit de remoção.**

### Pitfall 4: STYLE.md §Cabeçalho não atualizado e CONTEXT.md/D-93b vira regra invisível
**What goes wrong:** D-93b aplica o padrão `.deck-topic` à AGENDA mas STYLE.md continua dizendo "Cabeçalho de todo slide após a AGENDA". Próximo agente lê STYLE.md, segue regra antiga, gera inconsistência.
**Why it happens:** STYLE.md é a fonte canônica de regras; CONTEXT.md é específico da fase. Decisão de fase precisa migrar para STYLE.md.
**How to avoid:** plan AGENDA-01 (ou plan de fechamento) MUST atualizar STYLE.md linhas 37-60. Mudanças concretas: (1) §título "Cabeçalho de todo slide após a AGENDA" → "Cabeçalho de todo slide (incluindo AGENDA)"; (2) lista de exemplos travados inclui `> agenda`; (3) nota "Aplica a TODOS os slides de conteúdo (após a AGENDA)" muda para "Aplica a TODOS os slides de conteúdo, incluindo AGENDA". Listar isso explicitamente no checklist do plan.

### Pitfall 5: tentar embutir título "Obrigado." em `.deck-topic` (END-01)
**What goes wrong:** seguir o padrão dos outros slides e colocar `<p class="deck-topic">` em END-01, mesmo D-97b dizendo "sem cabeçalho".
**Why it happens:** consistência mecânica com fases anteriores.
**How to avoid:** END-01 é deliberadamente fora do padrão (encerramento). Slides minimais existentes: `slide-cover-brand` (linhas 27-34) e `slide-title-tcc` (linhas 37-57) também não têm `.deck-topic`. END-01 segue essa categoria. Não forçar.

### Pitfall 6: o número total de sections esperado não bate (validação)
**What goes wrong:** após inserir 4 sections novas, deck tem != 31 sections; navegação para após `#/N` errado.
**Why it happens:** contar AGENDA-01 como "novo" (é refator in-place, não nova section); ou esquecer de remover um stub temporário.
**How to avoid:** estado HEAD = 27 sections (confirmado em STATE.md "27 sections"). Após fase 5: 27 + 4 novos (TOOL-01, TOOL-03, MARKER-04, END-01) = **31 sections**. AGENDA-01 já existe em `#/2`, refator NÃO conta. Comando de verificação: `grep -c "<section " apresentacao/index.html` deve retornar 31 ao fim da fase.

### Pitfall 7: deslocar `#/2` ou MARKER-01..03 inadvertidamente
**What goes wrong:** inserir TOOL-01..END-01 antes do MARKER-03 em vez de depois; quebra a contagem de slides documentada em STATE.md e STYLE.md.
**Why it happens:** copy-paste de section + posicionamento errado.
**How to avoid:** D-92.1 deixa claro: TOOL-01 → TOOL-03 → MARKER-04 → END-01 ENTRE MARKER-03 (`#/26`) e o fim do deck. AGENDA-01 refatora `#/2` SEM alterar posição. Verificar com `grep -c "marker--phase" apresentacao/index.html` (deve ser 4 ao fim) e `grep -n "<section" apresentacao/index.html` (linha de cada section).

## Runtime State Inventory

Não aplicável: esta fase é mudança de markup HTML + CSS estático. Não há banco, serviço externo, registro OS, secret ou pacote instalado afetado.

| Category | Items Found | Action Required |
|---|---|---|
| Stored data | Nenhum — verificado: sem DB, sem cache, sem localStorage referenciado em apresentacao/ | — |
| Live service config | Nenhum — slides são estáticos servidos por `http.server` ad-hoc | — |
| OS-registered state | Nenhum — `http.server` é spawned manualmente, sem systemd/launchd | — |
| Secrets/env vars | Nenhum — slides são públicos, sem credenciais | — |
| Build artifacts | Nenhum — sem build system, sem `node_modules`, sem `.cache` | — |

## Code Examples

### Exemplo 1: modificador `.marker-pill--planned` (3 alternativas)

**Localização sugerida:** após linha 428 (após `.marker-pill--pending .marker-pill-icon`), antes de `.marker-arrow` linha 430.

**Alt A — Borda tracejada (recomendada):**
```css
/* Planned: ainda nao executada (TCC 2); circulo cinza vazio com borda tracejada,
   sem animacao; visualmente diferente de --pending (sólido) e --running (anima). */
.marker-pill--planned {
  color: #5b6472;
  border-style: dashed;
}
.marker-pill--planned .marker-pill-icon {
  color: #5b6472;
  border: 1.5px dashed #5b6472;
}
```

**Alt B — Azul atenuado, ícone reload sem animação:**
```css
.marker-pill--planned {
  color: var(--uni-blue);
  opacity: 0.7;
}
.marker-pill--planned .marker-pill-icon {
  color: var(--uni-blue);
  border: 1.5px solid var(--uni-blue);
  /* SEM animation; ícone &#x21BB; estático */
}
```

**Alt C — Ícone novo (calendário/relógio):**
```css
.marker-pill--planned {
  color: #5b6472;
}
.marker-pill--planned .marker-pill-icon {
  color: #5b6472;
  border: 1.5px solid #5b6472;
  /* ícone HTML entity: &#x231A; (relógio) ou &#x1F4C5; (calendário) — testar render no browser */
}
```

**Markup HTML (vale para todas as alternativas):**
```html
<div class="marker-pill marker-pill--planned">
  <span class="marker-pill-icon">&#x25CB;</span>   <!-- ou &#x21BB; (Alt B) ou &#x231A; (Alt C) -->
  <span class="marker-pill-name">Implantação</span>
</div>
<span class="marker-badge">[planned]</span>
```

**Critério de seleção no checkpoint:** olhar o MARKER-04 a 3m de distância. A pill 4 deve ser distinguível das pills 1-3 (done) E não pode ser confundida com `--pending` (que não aparece neste slide, mas aparece em MARKER-01/02/03). Aplicar `--planned` ao MARKER-01/02/03 temporariamente e ver se a estética não conflita visualmente com `--pending`.

### Exemplo 2: AGENDA-01 refatorado (markup completo)

Substitui linhas 60-80 do index.html:

```html
<!-- ============ SLIDE · Agenda · 4 fases da EDM ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>agenda<span class="caret blink"></span></p>

    <ol class="agenda-edm-list">
      <li>Definição do Problema</li>
      <li>Preparação dos Dados</li>
      <li>Modelagem e Avaliação</li>
      <li>Implantação<span class="caret blink"></span></li>
    </ol>
  </div>
</section>
```

**Nota:** o `data-background-gradient` da agenda atual (linha 61) é REMOVIDO; volta a ser `data-background-color="#F1F6FB"` para harmonizar com os demais slides de conteúdo.

**CSS sugerido para `.agenda-edm-list` (~10 linhas, anexar perto do bloco `.slide-related` para coesão):**

```css
.agenda-edm-list {
  list-style: none; counter-reset: agenda;
  margin: 32px 0 0; padding: 0; max-width: 900px;
  --caret-color: var(--uni-blue);
}
.agenda-edm-list li {
  counter-increment: agenda; position: relative;
  padding: 10px 0 10px 50px;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 23px; line-height: 1.4; color: var(--uni-ink);
}
.agenda-edm-list li::before {
  content: counter(agenda) ".";
  position: absolute; left: 12px; top: 10px;
  color: var(--uni-blue); font-weight: 700;
}
```

**Alternativa:** reusar `.phases-list` do slide Zorić p3 (linhas 142-153) — ele já tem contador numerado azul + Arial 23px + line-height 1.5. Trade-off: `.phases-list` é específico de `.slide-phases` (`.slide-phases .phases-list li`), então seria preciso refatorar o seletor ou copiar regras. **Recomendação:** criar `.agenda-edm-list` separada (mais limpo, não acopla 2 slides).

### Exemplo 3: END-01 markup + CSS mínimo

**Markup:**
```html
<!-- ============ SLIDE · Obrigado ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-end">
    <p class="end-thanks">Obrigado.</p>
    <p class="end-credits">Léo Kuntz · TCC 1 · UniFacens · 2026</p>
  </div>
</section>
```

**CSS mínimo (anexar após bloco `.slide-marker` ou no fim do arquivo):**
```css
/* ===========================================================================
   SLIDE · Encerramento · "Obrigado." minimal (END-01)
   =========================================================================== */
.slide-end {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  background: var(--uni-light);
  padding: 0;
}
.end-thanks {
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 96px; font-weight: 700; color: var(--uni-ink);
  margin: 0;
}
.end-credits {
  margin-top: 28px;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 18px; color: #5b6472;
}
```

**Decisão no checkpoint:**
- Variante "minimal puro": remover `.end-credits` inteiro; ficar só "Obrigado.".
- Variante "com créditos": manter `.end-credits` com nome + TCC + ano.
- Cor: `--uni-ink` preto puro vs `--uni-blue` (defere ao checkpoint; default preto).
- Tamanho fonte: 96px (proposta) vs 120px (mais impactante) vs 72px (mais sóbrio).

### Exemplo 4: MARKER-04 (deltas vs MARKER-03)

Copy-paste de MARKER-03 (index.html linhas 687-730); aplicar 4 deltas listados em CONTEXT.md "MARKER-04 markup-alvo". Aqui o markup completo:

```html
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 4 concluida (Zoric, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase4">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="marker-title"><span class="ps1">&gt;</span>AS QUATRO FASES DA EDM<span class="caret blink"></span></p>

    <div class="marker-track">
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Definição do Problema</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Preparação dos Dados</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Modelagem e Avaliação</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--planned">
          <span class="marker-pill-icon">&#x25CB;</span>
          <span class="marker-pill-name">Implantação</span>
        </div>
        <span class="marker-badge">[planned]</span>
      </div>
    </div>

    <p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

### Exemplo 5: TOOL-01 markup (estrutura, microcópia defere ao checkpoint)

Wrapper segue MODEL-05 (`.slide-related slide-bridge`). Cabeçalho `> proposta da aplicação`. Pipeline 6 etapas no padrão Word/ABNT monocromático (preto, sem azul UniFacens em nenhuma):

```html
<!-- ============ SLIDE · TOOL-01 · Proposta da aplicação + pipeline 6 etapas ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>proposta da aplicação<span class="caret blink"></span></p>

    <p class="rel-lead">O processo apresentado pode ser instrumentalizado para professores. Propomos uma aplicação docente que organiza esse fluxo em seis etapas.</p>

    <p class="eda-title" style="margin-top: 22px; color: #000;">Figura &ndash; Aplicação docente em seis etapas</p>
    <p class="bridge-seq" style="margin-top: 10px;">
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400;">Submissões<span style="margin-top: 4px;">dos estudantes</span></span>
      <span class="arr" style="color: #000;">&rarr;</span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400;">Extração<span style="margin-top: 4px;">de KCs</span></span>
      <span class="arr" style="color: #000;">&rarr;</span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400;">Professor<span style="margin-top: 4px;">valida</span></span>
      <span class="arr" style="color: #000;">&rarr;</span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400;">Preparação<span style="margin-top: 4px;">dos dados</span></span>
      <span class="arr" style="color: #000;">&rarr;</span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400;">Code-DKT<span style="margin-top: 4px;">treinado</span></span>
      <span class="arr" style="color: #000;">&rarr;</span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400;">Dashboard<span style="margin-top: 4px;">para o professor</span></span>
    </p>
    <p class="eda-source">Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.</p>

    <p class="rel-lead" style="margin-top: 18px;">O dashboard fecha o ciclo e é o que detalhamos no próximo slide.</p>

    <p class="rel-cite">Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.</p>
  </div>
</section>
```

**Nota:** dois "Fonte:" — um `.eda-source` (legenda da Figura) e um `.rel-cite` (rodapé do slide). MODEL-05 segue o mesmo padrão (linha 551 + ausência de `.rel-cite` ao final do MODEL-05 porque o slide é dominado pela Figura). Para TOOL-01, manter ambos é redundante; sugestão: **omitir `.rel-cite` final** ou consolidar como em MODEL-05 (1 só `.eda-source` ao final do pipeline). Defere ao checkpoint visual.

### Exemplo 6: TOOL-03 markup (estrutura `.bridge-seq` adaptada para 3 painéis grandes)

Opção primária — `.bridge-seq` adaptado com `.step` de altura maior:

```html
<!-- ============ SLIDE · TOOL-03 · Dashboard (wireframe 3 painéis) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>dashboard da aplicação<span class="caret blink"></span></p>

    <p class="eda-title" style="margin-top: 26px; color: #000;">Figura &ndash; Painéis principais do dashboard</p>
    <p class="bridge-seq" style="margin-top: 14px; gap: 16px;">
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400; min-height: 280px; padding: 24px 18px; font-size: 18px;"><b>Respostas de código<br>da turma</b><span style="margin-top: 22px; font-size: 14px; color: #5b6472;">[ilustração esquemática]</span></span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400; min-height: 280px; padding: 24px 18px; font-size: 18px;"><b>Predição de conhecimento<br>por estudante</b><span style="margin-top: 22px; font-size: 14px; color: #5b6472;">[ilustração esquemática]</span></span>
      <span class="step" style="flex-direction: column; color: #000; border-color: #000; font-weight: 400; min-height: 280px; padding: 24px 18px; font-size: 18px;"><b>Dificuldade da turma<br>por KC</b><span style="margin-top: 22px; font-size: 14px; color: #5b6472;">[ilustração esquemática]</span></span>
    </p>
    <p class="eda-source">Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.</p>

    <p class="rel-lead" style="margin-top: 18px;">O dashboard auxilia o professor a direcionar intervenções por estudante e por dificuldade.</p>
  </div>
</section>
```

**Notas:**
- 3 painéis em vez de N etapas: NÃO usar `.arr` (setas) entre eles; painéis são paralelos, não sequenciais.
- `min-height: 280px` cria a sensação visual de "painel" em vez de "etapa de pipeline".
- `gap: 16px` em vez de 0 (default `.bridge-seq`) cria espaçamento entre painéis.
- A "ilustração esquemática" inline é placeholder; defere ao checkpoint visual a escolha entre:
  - **Caixa-texto minimalista** (default, conforme CONTEXT discretion): só o título do painel + descrição em pequeno cinza
  - **Barras stub**: 3-4 retângulos pretos de alturas variadas representando barras
  - **Scatter stub**: 5-8 pontos pretos em um quadradinho representando scatter
- Complexidade de implementação:
  - Caixa-texto: 0 markup extra (já no exemplo acima)
  - Barras stub: ~8 linhas de `<span>` com `width`/`height`/`display:inline-block`
  - Scatter stub: idem (~8 linhas com `position:absolute`)

**Fallback `.dash-card`:** se o `.bridge-seq` adaptado não casar (e.g., painéis ficarem com altura visualmente desigual ou `flex: 1 1 0` resultar em larguras estranhas), criar:

```css
/* ===========================================================================
   SLIDE · TOOL-03 · Dashboard wireframe (3 painéis lado a lado, ABNT)
   =========================================================================== */
.dash-card-row {
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px;
  margin-top: 22px; max-width: 1180px;
}
.dash-card {
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0;
  padding: 24px 20px;
  font-family: Arial, "Helvetica Neue", sans-serif;
  display: flex; flex-direction: column; align-items: center; text-align: center;
  min-height: 280px;
}
.dash-card .dash-card-title {
  font-size: 19px; font-weight: 700; color: #000; line-height: 1.3;
}
.dash-card .dash-card-illu {
  margin-top: 24px; font-size: 14px; color: #5b6472;
}
```

E o markup correspondente:

```html
<div class="dash-card-row">
  <div class="dash-card">
    <span class="dash-card-title">Respostas de código<br>da turma</span>
    <span class="dash-card-illu">[ilustração]</span>
  </div>
  <!-- × 3 painéis -->
</div>
```

Vantagem `.dash-card`: grid 1fr × 3 garante painéis idênticos de tamanho; CSS dedicado é mais legível que inline-style intensivo.

## Plan-Level Execution Order (Gap #6 + #7)

| Ordem | Plan | Slide | Cross-cutting | Por que esta posição |
|---|---|---|---|---|
| 1 | 05-01 | MARKER-04 (`#/29`) | CSS aditivo: `.marker-pill--planned` (mandatory) | Mais mecânico; entrega o componente CSS aditivo cedo, calibra ambiente. Se animação ou cor não funcionar, descobre-se logo. |
| 2 | 05-02 | AGENDA-01 (`#/2` refator) | STYLE.md §Cabeçalho reescrito (D-93b); cleanup `.slide-agenda/.agenda-side/.agenda-main/.agenda-list`; novo `.agenda-edm-list` | Antes dos outros 3 novos slides porque o override D-93b ao STYLE.md "Cabeçalho de todo slide..." vai redefinir o gabarito que TOOL-01/TOOL-03/END-01 herdam. Fazer este update primeiro evita que TOOL-01/TOOL-03 sejam validados contra uma versão obsoleta de STYLE.md. |
| 3 | 05-03 | END-01 (`#/30`) | CSS novo: `.slide-end`, `.end-thanks`, `.end-credits` | Minimal; baixíssimo risco; entrega o slide final cedo para validar bracket narrativo de fim a fim (#/0 cover → #/30 end). |
| 4 | 05-04 | TOOL-03 (`#/28`) | CSS condicional: `.dash-card` se `.bridge-seq` não casar | Antes de TOOL-01 porque TOOL-03 testa a viabilidade do `.bridge-seq` para layout NÃO-sequencial (3 painéis paralelos); se resultar em `.dash-card`, TOOL-01 ainda usa o `.bridge-seq` puro. Se invertido (TOOL-01 primeiro), o `.bridge-seq` é validado para 6 etapas mas não esclarece TOOL-03. |
| 5 | 05-05 | TOOL-01 (`#/27`) | nenhum CSS novo (reusa `.bridge-seq` + `.slide-related`) | Slide mais denso em conteúdo; aproveita a calibragem dos 4 anteriores; pode iterar mais no checkpoint sem bloquear outros. |
| 6 | 05-06 (fechamento) | n/a — meta-arquivos | STYLE.md §Inventário 27→31; §Gaps removido; §Classes reutilizáveis adicionar `--planned`/`.agenda-edm-list`/possivelmente `.dash-card`/`.slide-end`. PROJECT.md Active → Validated; novas Key Decisions D-92, D-93b. Possível update da memória `feedback_marker_design` com `--planned`. | Plan final consolidador, análogo ao 01-07 da fase 1 e 04-05 da fase 4. Sem mexer em slide novo. |

**Total: 6 plans** — alinhado com fases anteriores (fase 1 teve 7, fase 4 teve 5 + 2 adendos). Granularidade coarse mantida.

### Dependências entre plans (paralelização?)

Workflow está em modo `interactive` (CONTEXT) e `coarse`, então paralelismo é raro. Mas para clareza:

- 05-01 (MARKER-04) é **independente** de 05-02..05-05; só toca CSS + 1 section.
- 05-02 (AGENDA-01) **deve preceder** 05-03/04/05 porque atualiza STYLE.md §Cabeçalho. Concorrentemente: independente de 05-01 (CSS de marker é separado).
- 05-03 (END-01) é **independente** de 05-04 e 05-05; só toca CSS novo isolado + 1 section.
- 05-04 (TOOL-03) **opcionalmente precede** 05-05 (TOOL-01) para validar `.bridge-seq` no caso 3 painéis (se virar `.dash-card`, isso informa decisões em TOOL-01, embora TOOL-01 use `.bridge-seq` original).
- 05-06 (fechamento) **depende de todos** anteriores.

**Wave plausível se paralelização for ativada:**
- Wave 1: [05-01 MARKER-04 + 05-02 AGENDA-01] (paralelos; CSS distinto, HTML distinto)
- Wave 2: [05-03 END-01 + 05-04 TOOL-03] (paralelos; CSS isolado, HTML após MARKER-03)
- Wave 3: [05-05 TOOL-01] (após calibragem da Wave 2)
- Wave 4: [05-06 fechamento]

Como `parallelization: true` está em config mas workflow é coarse interactive, recomendo **sequencial mesmo** seguindo a ordem 1-6 acima. Cada plan termina com checkpoint visual, que é gargalo humano natural.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|---|---|---|---|---|
| reveal.js (CDN jsdelivr) | index.html | ✓ (via internet) | 5.1.0 | — |
| @fontsource/cascadia-code | index.html | ✓ (via CDN) | 5 (400+700) | font system mono fallback |
| python3 | servir slides localmente | ✓ (Linux) | 3.10+ | `npx http-server` ou outro |
| browser moderno (Chrome/Firefox/Edge) | reviewer validation | ✓ (host) | atual | — |
| `grep` | verificar callers de classe + contar sections | ✓ | — | — |

**Missing dependencies with no fallback:** nenhum.
**Missing dependencies with fallback:** nenhum.

## Validation Architecture

`workflow.nyquist_validation` não está explicitamente em config (lido CONTEXT.md). Trato como **enabled** com adaptação: este projeto não tem framework de teste automatizado (validação é visual no browser, conforme STATE.md Workflow). Reporte mesmo assim:

### Test Framework
| Property | Value |
|---|---|
| Framework | n/a (visual validation no browser) |
| Config file | n/a |
| Quick run command | `cd apresentacao && python3 -m http.server 8000` |
| Full suite command | navegar `#/0` → `#/30` no browser; consultar console (F12) |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Comando | File Exists? |
|---|---|---|---|---|
| TOOL-01 | section #/27 com pipeline 6 etapas cabe em 1280×720 sem overflow | smoke visual | abrir `#/27`; F12 console clean; sem scroll horizontal | ✅ apresentacao/index.html |
| TOOL-03 | section #/28 com 3 painéis lado a lado legíveis | smoke visual | abrir `#/28`; verificar altura uniforme dos 3 painéis | ✅ |
| MARKER-04 | section #/29 com 3 pills done + pill 4 planned (sem animação) | smoke visual | abrir `#/29`; observar pill 4 estática; comparar com `#/26` (running spin) | ✅ |
| END-01 | section #/30 com "Obrigado." centralizado | smoke visual | abrir `#/30`; verificar centralização vertical+horizontal | ✅ |
| AGENDA-01 | section #/2 com cabeçalho `> agenda` + 4 fases EDM | smoke visual | abrir `#/2`; verificar caret blink no item 4; comparar com agenda antiga (não deve ter) | ✅ |
| PENDING-01 | conteúdo do slide Agenda decidido (resolvido por D-93a) | n/a | resolvido por documentação | n/a |

### Sampling Rate
- **Per slide commit:** abrir o slide específico no browser e validar visualmente.
- **Per wave:** se waves forem usadas, validar todos os slides da wave antes de avançar.
- **Phase gate (D-104):** navegação completa `#/0` → `#/30` sem erro de console; ritmo de defesa subjetivo ≤ 10 min.

### Wave 0 Gaps
- **Nenhum gap real** — não há infraestrutura de teste automatizado a criar. Toda validação é browser + grep manual no commit.
- Comandos de verificação úteis no fechamento de cada plan:
  - `grep -c "<section " apresentacao/index.html` (esperado 31 ao fim da fase)
  - `grep -c "marker--phase" apresentacao/index.html` (esperado 4 ao fim)
  - `grep -c "deck-topic" apresentacao/index.html` (esperado +1 vs HEAD pela AGENDA-01)
  - `grep -n "marker-pill--planned" apresentacao/index.html` (esperado 1 ocorrência, MARKER-04)
  - `grep -n "agenda-side\|agenda-main\|agenda-list" apresentacao/` (esperado 0 ocorrências após cleanup)

## Security Domain

Não aplica. Apresentação estática HTML/CSS sem inputs, autenticação, sessão, criptografia, ou dados sensíveis. ASVS V2/V3/V4/V5/V6 todas marcadas "no" para este escopo.

## STYLE.md updates — cross-cutting

Lista concreta do que o plan 05-02 (AGENDA-01) e/ou plan 05-06 (fechamento) precisam atualizar em `apresentacao/STYLE.md`:

### Update 1 — §"Cabeçalho de todo slide após a AGENDA" (linhas 37-60) — plan 05-02 (AGENDA-01)

**Mudanças mínimas:**
- Linha 37: `## Cabeçalho de todo slide após a AGENDA` → `## Cabeçalho de TODO slide (incluindo AGENDA)`
- Linha 39: "Padrão obrigatório: **uma única linha de cabeçalho** com o nome da seção..." (sem mudança)
- Linha 46-47: "Classe única: `.deck-topic`. Aplica a TODOS os slides de conteúdo (após a AGENDA), incluindo os que antes usavam o template `.slide-related` com par `.rel-kicker.kicker` + `.rel-title` + `.rel-sub`." → "Classe única: `.deck-topic`. Aplica a TODOS os slides de conteúdo, **incluindo a AGENDA** (refator em fase 5)."
- Linha 50-54 (exemplos travados): adicionar `> agenda` à lista.

### Update 2 — §Inventário de slides (linhas 108-138) — plan 05-06 (fechamento)

Reescrever a tabela para 31 sections finais. Adicionar as 4 novas linhas após linha 138 (MARKER-03) e refatorar a linha 114 (slide-agenda) para refletir o novo padrão:

```
| 2 | slide-related | `> agenda` | Agenda (4 fases EDM como sumário) |
...
| 27 | slide-related slide-bridge | `> proposta da aplicação` | TOOL-01: pipeline 6 etapas |
| 28 | slide-related slide-bridge (ou dash-card-row) | `> dashboard da aplicação` | TOOL-03: wireframe 3 painéis |
| 29 | slide-marker--phase4 | (sem temático) | MARKER-04: Implantação planned (TCC 2) |
| 30 | slide-end | (sem cabeçalho) | END-01: Obrigado |
```

Atualizar também o totalizador na linha 140: "27 slides após a fase 4" → "31 slides após a fase 5".

### Update 3 — §Gaps reservados (linhas 142-146) — plan 05-06 (fechamento)

**Remover o §Gaps inteiro.** Não há mais fases.

### Update 4 — §Classes reutilizáveis (linhas 148-157) — plan 05-06 (fechamento)

Adicionar bullets para classes novas desta fase:
- `.agenda-edm-list`: lista numerada vertical para Agenda (uso único, mas registrado)
- `.marker-pill--planned`: modificador aditivo do `.slide-marker` (estado "futuro previsto", sem animação)
- `.slide-end`, `.end-thanks`, `.end-credits`: trio do slide de encerramento
- (condicional) `.dash-card-row`, `.dash-card`: grid 3 painéis estilo Word/ABNT (se TOOL-03 usar fallback)

### Update 5 — §"Linhagem de KT" (linha 146) — não precisa update

Já está completa após fase 4.

## PROJECT.md updates — fechamento

Lista para o plan 05-06:

### Active → Validated

Mover TODOS os 6 REQ-IDs da fase 5:
- AGENDA-01 → Validated (resolvido junto com PENDING-01)
- TOOL-01 → Validated
- TOOL-03 → Validated
- MARKER-04 → Validated
- END-01 → Validated
- PENDING-01 → Validated (resolvido por D-93a)

### Key Decisions — novas linhas

Adicionar 2 linhas em PROJECT.md § Key Decisions (atual linha 169-186):

```
| Vocabulário "aplicação" no lugar de "ferramenta" nos slides; REQ-IDs TOOL-01/TOOL-03 não renomeados | D-92 fase 5; a entrega é uma aplicação que contém ferramentas internas (extração KCs, modelo ML); REQ-IDs são identificadores estáveis | ✓ Confirmado |
| AGENDA-01 incorporada ao padrão `> [seção]` (override STYLE.md linha 39-42) | D-93b fase 5; consistência visual com o deck inteiro pós-AGENDA; AGENDA atual destoa com `<h2>Agenda</h2>` + agenda-side | ✓ Confirmado |
```

### Validated Updates (linhas 16-37)

Adicionar referência aos 4 slides novos + AGENDA refatorada ao final da seção Validated (após linha 37). Manter formato existente.

### "What This Is" (linhas 4-7)

Sem mudança; descrição genérica da apresentação inteira já cobre.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|---|---|---|---|
| `<h2>` interno + tópico kicker separado por slide | `.deck-topic` único com caret blink | Fase 1 (D-04..D-11) | Toda a fase 5 herda |
| Modificadores `.marker-pill--done`/`--running`/`--pending` (3 estados) | + `.marker-pill--planned` (4 estados) | Fase 5 (D-96c) | Aditivo; MARKER-01/02/03 inalterados |
| `.slide-agenda` com agenda-side azul + logo grande + agenda-main + agenda-list | `.slide-related` reformulado com cabeçalho `.deck-topic` + lista vertical | Fase 5 (D-93) | Cleanup de 4 classes órfãs |

## Sources

### Primary (HIGH confidence)
- `apresentacao/index.html` (HEAD em 2026-05-29) — markup canônico das 27 sections existentes
- `apresentacao/assets/theme-unifacens.css` (HEAD) — 517 linhas; todas as classes reusáveis localizadas
- `apresentacao/STYLE.md` (HEAD) — regras travadas; inventário 27 sections; §Gaps reservados linha 142-146 enumera os 5 slides desta fase
- `.planning/phases/05-implanta-o-agenda-e-encerramento-fase-4-edm/05-CONTEXT.md` — 13 decisões D-92..D-104 locked
- `.planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-05-SUMMARY.md` — referência do padrão "1 plan por slide + plan de fechamento"
- `.planning/PROJECT.md` Key Decisions linha 183 — gate "ProgSnap2 só em INTRO-01" / "entrada de submissões dos estudantes" para a aplicação
- `.planning/STATE.md` — confirmação de 27 sections HEAD; plans concluídos
- `.planning/REQUIREMENTS.md` linha 168-172 — tabela Traceability mostrando TOOL-01/03, MARKER-04, END-01, AGENDA-01, PENDING-01 todos mapeados a Phase 5

### Documented (HIGH confidence)
- `docs/tcc2_prototipo.html` (parcial: linhas 40-134) — confirmadas 6 páginas na sidebar (Upload, KC, EDA, KT, Recomendações, Chat) + tags `tag-intended`/`tag-emerged`. Pano de fundo conceitual de TOOL-01 e TOOL-03; não é templated para layout.

### Inferido / não verificado (LOW)
- Comportamento de `.bridge-seq` com 6 etapas em 1280×720 — derivado de cálculo de largura disponível e tamanho do `.step` no MODEL-05. Requer validação visual no browser (Pitfall 1).
- Distinção visual entre `--planned` e `--pending` — requer teste a 3m no browser (Pitfall 2). 3 alternativas propostas; recomendação Alt A (borda tracejada) baseada em precedente CSS comum, não em teste do reviewer ainda.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|---|---|---|
| A1 | `.bridge-seq` com 6 etapas comporta visualmente em 1280px se microcópia for ≤ 2 palavras + 1 linha de descrição | Pitfall 1, Code Example 5 | TOOL-01 pode precisar de ajustes inline (fonte 17px, padding 12/10, etc.) ou de `.bridge-seq--6step` CSS dedicado. Detectável no checkpoint TOOL-01. |
| A2 | `border-style: dashed` em `.marker-pill--planned` é visualmente distinguível de `--pending` (sólido) e `--running` (sólido + animado) | Pitfall 2, Code Example 1 (Alt A) | Reviewer pode pedir outra alternativa no checkpoint MARKER-04; testar Alt B ou C em iteração. |
| A3 | `.agenda-side`, `.agenda-main`, `.agenda-list`, `.slide-agenda` ficam órfãs após refator AGENDA-01 | Pitfall 3 | Verificável no plan AGENDA-01 com `grep`; risco baixo dado grep retornou apenas 4 linhas no CSS + 4 no HTML que serão substituídas. |
| A4 | Reveal.js 5.1.0 renderiza HTML entity `&#x25CB;` (círculo vazio) corretamente em todos browsers modernos | Code Example 1, 4 | Já validado em MARKER-01/02 (commits `d37304d`, `3d47be4`) — risco MUITO baixo. |
| A5 | Nenhum outro slide do deck depende de `data-background-gradient` (o gradient atual do slide-agenda) — pode ser trocado para `data-background-color` sem regressão | Code Example 2 | grep `data-background-gradient` em index.html confirma uso só na agenda. |
| A6 | O modificador `--planned` é necessário APENAS para MARKER-04; não há plano de uso futuro | Don't Hand-Roll, Code Example 1 | Memória `feedback_marker_design` deve ser atualizada após a fase 5 para registrar o 4º modificador. Sem impacto técnico imediato. |
| A7 | "Obrigado." em Arial 96px bold preto centralizado é o default mais sóbrio para defesa acadêmica | Code Example 3 | Reviewer pode preferir Cascadia, tamanho diferente, cor `--uni-blue`. Decisão de checkpoint. |
| A8 | END-01 sem marca d'água é mais minimal e bracket-narrativo com slide-cover-brand (#/0 também sem `.wm`) | D-97d default, Code Example 3 | Reviewer pode pedir marca d'água para coesão com slides de conteúdo. Decisão de checkpoint. |
| A9 | Plan de fechamento (05-06) não precisa do checkpoint humano para meta-arquivos (STYLE.md/PROJECT.md) | Plan-Level Execution Order | Padrão da fase 1 (commit `907a4b5`) e fase 4 (commit `3ea83d3`) — atualizações de doc sem checkpoint. Risco zero. |

**Se este Assumptions Log é vazio (A1..A9 todos verificados):** dispensa confirmação humana. Recomendo verificar A1, A2, A7, A8 explicitamente em checkpoint dos respectivos plans.

## Open Questions (RESOLVED via checkpoint routing)

1. **Cabeçalho exato de TOOL-03: `> dashboard da aplicação` ou `> o dashboard`?**
   - What we know: D-95a marca `> dashboard da aplicação` como proposta principal, `> o dashboard` como alternativa.
   - What's unclear: qual soa melhor para a defesa.
   - Recomendação: ir com `> dashboard da aplicação` (proposta principal) no markup inicial e confirmar no checkpoint.
   - RESOLVED → plan 05-04 checkpoint task 2

2. **TOOL-01 — manter ou cortar a frase de fechamento "O dashboard fecha o ciclo..."?**
   - D-94f explicitamente marca como opcional, corta se apertado.
   - Recomendação: incluir no markup inicial e validar visualmente se cabe; remover no checkpoint se gerar pressão de espaço.
   - RESOLVED → plan 05-05 checkpoint task 2

3. **END-01 — incluir créditos (`Léo Kuntz · TCC 1 · UniFacens · 2026`) ou puro?**
   - D-97c marca como discretion.
   - Recomendação: incluir versão com créditos (mais informativa para banca) e oferecer toggle visual ao reviewer no checkpoint.
   - RESOLVED → plan 05-03 checkpoint task 2

4. **`--planned` estética — escolher Alt A no plan ou apresentar 3 no checkpoint?**
   - D-96c marca discretion.
   - Recomendação: implementar Alt A (borda tracejada) como default por ser a mais aditiva e baixo risco. No checkpoint MARKER-04, mostrar Alt A funcionando E oferecer mudança para Alt B/C se reviewer pedir.
   - RESOLVED → plan 05-01 checkpoint task 2

5. **Plan 05-04 TOOL-03 — começar com `.bridge-seq` adaptado ou já anexar `.dash-card`?**
   - D-95d defere ao executor.
   - Recomendação: começar com `.bridge-seq` adaptado (zero CSS novo); se altura/largura dos 3 painéis não casarem visualmente após 1 iteração, migrar para `.dash-card`. Padrão "menos é mais" aplica aqui.
   - RESOLVED → plan 05-04 checkpoint task 2

## Environment / Tooling Notes

- Servidor local: porta 8000 padrão em STYLE.md linha 162. Se conflito (porta em uso), STYLE.md sugere subir em outra porta para evitar cache. Recomendação: usar `python3 -m http.server 8001` se houver conflito; URL: `http://127.0.0.1:8001/#/N`.
- Forçar reload de CSS: `Ctrl+Shift+R` (Linux/Windows) ou `Cmd+Shift+R` (Mac).
- Rotas de slides após inserção (assumindo ordem D-92.1):
  - `#/0` slide-cover-brand
  - `#/1` slide-title-tcc
  - **`#/2` AGENDA-01 refatorado**
  - `#/3..#/26` slides existentes (Martins, EDM, Yağcí, Shi, MARKER-01, INTRO-01, EDA-01..03, EDA-02, MARKER-02, INTRO-KC, MODEL-01a, MODEL-01b, slide-code, MODEL-04, MODEL-05, Martins p2, Martins p3, slide-kcfig, slide-fig, MARKER-03)
  - **`#/27` TOOL-01**
  - **`#/28` TOOL-03**
  - **`#/29` MARKER-04**
  - **`#/30` END-01**

## Validation Checklist (gate D-104)

Listado aqui para o planner copiar para o último plan (05-06 fechamento):

```
[ ] grep -c "<section " apresentacao/index.html → 31
[ ] grep -c "marker--phase" apresentacao/index.html → 4 (phase1, phase2, phase3, phase4)
[ ] grep -c "marker-pill--planned" apresentacao/index.html → 1
[ ] grep -c "marker-pill--running" apresentacao/index.html → 1 (apenas MARKER-03 herda)
[ ] grep -n "agenda-side\|agenda-main\|agenda-list" apresentacao/index.html → 0 ocorrências
[ ] grep -n "\.slide-agenda\|\.agenda-side\|\.agenda-main\|\.agenda-list" apresentacao/assets/theme-unifacens.css → 0 ocorrências (cleanup pós-AGENDA-01)
[ ] grep -c "deck-topic" apresentacao/index.html → N+1 vs HEAD (AGENDA-01 ganhou o padrão)
[ ] Servir local: cd apresentacao && python3 -m http.server 8000
[ ] #/0 → #/30 navegação contínua sem erro de console (F12)
[ ] #/2 AGENDA-01: cabeçalho `> agenda` + 4 itens; caret blink no item 4
[ ] #/26 MARKER-03: pill 4 ainda "Implantação --running" girando
[ ] #/27 TOOL-01: pipeline 6 etapas sem overflow horizontal
[ ] #/28 TOOL-03: 3 painéis lado a lado com mesma altura
[ ] #/29 MARKER-04: 3 pills done check ✓ + pill 4 planned (sem animação, distinguível)
[ ] #/30 END-01: "Obrigado." centralizado vertical+horizontal
[ ] Tempo natural de defesa estimado pelo apresentador ≤ 10 min
[ ] STYLE.md §Cabeçalho atualizado (incluindo AGENDA)
[ ] STYLE.md §Inventário com 31 sections
[ ] STYLE.md §Gaps reservados removido
[ ] PROJECT.md REQ-IDs Active → Validated (TOOL-01, TOOL-03, MARKER-04, END-01, AGENDA-01, PENDING-01)
[ ] PROJECT.md Key Decisions: D-92, D-93b adicionados
```

## Metadata

**Confidence breakdown:**
- Standard stack (classes existentes): HIGH — todo CSS canônico localizado por grep, MARKER-03 inspecionado linha a linha
- Architecture / componentes a reusar: HIGH — padrões estabelecidos em fases 1-4 com decisões D-04..D-91 herdadas
- Pitfalls 1-2 (bridge-seq 6 etapas, planned vs pending): MEDIUM — calculados, não testados no browser; requer checkpoint
- Pitfalls 3-7: HIGH — verificados por grep
- Ordem de execução: MEDIUM — recomendação fundamentada em risco, alternativa válida (TOOL-01 primeiro) também defensável
- STYLE.md / PROJECT.md updates: HIGH — linhas exatas mapeadas

**Research date:** 2026-05-29
**Valid until:** 2026-06-07 (defesa) ou até a próxima edição em theme-unifacens.css/STYLE.md

---

*Phase: 5-Implantação, Agenda e Encerramento (Fase 4 EDM)*
*Research gathered: 2026-05-29*
