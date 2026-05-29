# Phase 5: Implantação, Agenda e Encerramento (Fase 4 EDM) - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-29
**Phase:** 5-implanta-o-agenda-e-encerramento-fase-4-edm
**Areas discussed:** AGENDA-01 estrutura, TOOL-01 forma do pipeline, TOOL-03 dashboard, MARKER-04 + END-01

---

## AGENDA-01 estrutura

### Q1: Qual estrutura a Agenda deve refletir?

| Option | Description | Selected |
|---|---|---|
| 4 fases EDM (espelha marcadores) | Definição do Problema · Preparação dos Dados · Modelagem e Avaliação · Implantação | ✓ |
| 5 blocos narrativos | Introdução · Dataset · EDA · Modelagem · Ferramenta TCC 2 | |
| 6 marcos cronológicos | Problema · EDM · KT · Dataset · Code-DKT+KCs · Ferramenta | |

**User's choice:** 4 fases EDM.
**Notes:** Espelha exatamente as 4 pills dos MARKERs e refaz a Agenda como sumário canônico-EDM.

### Q2: Cabeçalho do slide-agenda segue o padrão `> [seção]`?

| Option | Description | Selected |
|---|---|---|
| Sim, `> agenda` com caret | Aplica D-04..D-11 (override STYLE.md linha 39-42) | ✓ |
| Não, mantém `<h2>Agenda</h2>` atual | Preserva exclusão explícita da AGENDA do padrão | |

**User's choice:** Sim, `> agenda`.
**Notes:** Override do STYLE.md fica registrado em D-93b; STYLE.md §"Cabeçalho de todo slide após a AGENDA" precisa ser reescrito dentro desta fase.

---

## TOOL-01 forma do pipeline

### Q1: Como o pipeline da ferramenta TCC 2 aparece no slide?

| Option | Description | Selected |
|---|---|---|
| `.bridge-seq` 6 etapas | Reusa componente de MODEL-05/Yağcı; zero CSS novo; consistência | ✓ |
| Screenshot do protótipo | Captura de `docs/tcc2_prototipo.html` como Figura ABNT | |
| `.bridge-seq` + thumbnail | Híbrido; pipeline + dashboard inset | |

**User's choice:** `.bridge-seq` 6 etapas (recommended).

### Q2: Qual a abertura textual do TOOL-01?

| Option | Description | Selected |
|---|---|---|
| 1 frase em 1ª pessoa do plural | Curta, direta; padrão MODEL-05 | |
| 2 frases (motivação + escopo) | Mais narrativa | ✓ |
| Sem frase de abertura | Apenas cabeçalho + pipeline + fechamento | |

**User's choice:** 2 frases. **+ free-text override:** "ao invés de chamarmos de ferramenta, vamos chamar de aplicação (é uma aplicação que contém ferramentas de extração de KCs, modelo de aprendizado de máquina)".
**Notes:** Vocabulário "aplicação" no lugar de "ferramenta" registrado como D-92 (decisão vocabular nova). Aplica em TOOL-01, TOOL-03, MARKER-04 conteúdos e fala. REQ-IDs TOOL-01/TOOL-03 não são renomeados (identificadores estáveis).

### Q3: Vocação do slide — a etapa 'Code-DKT' do pipeline destaca algo?

| Option | Description | Selected |
|---|---|---|
| Sem destaque (todas iguais) | 6 caixas neutras como MODEL-05 | ✓ |
| Code-DKT em azul UniFacens | 5 neutras + 1 destacada (modelo escolhido) | |
| Dashboard em azul (ponte para TOOL-03) | 5 neutras + última destacada | |

**User's choice:** Sem destaque.
**Notes:** Pipeline como processo contínuo; destaque criaria hierarquia que confunde a narrativa "a aplicação espelha o que já mostramos".

---

## TOOL-03 dashboard

### Q1: Como o dashboard é apresentado?

| Option | Description | Selected |
|---|---|---|
| Screenshot do protótipo | Captura de `docs/tcc2_prototipo.html` como Figura ABNT | |
| Wireframe 3 painéis | Estilo Word/ABNT (borda 1.5px, cantos retos) | ✓ |
| Screenshot + 3 rótulos overlay | Híbrido | |

**User's choice:** Wireframe 3 painéis (recommended).
**Notes:** 3 painéis nomeados: respostas de código da turma · predição de conhecimento por estudante · dificuldade da turma por KC. Componente: `.bridge-seq` adaptado preferido; `.dash-card` novo se não casar (Claude's Discretion).

### Q2: Qual a microcópia de fechamento de TOOL-03 (1 frase)?

| Option | Description | Selected |
|---|---|---|
| Foco no professor | "O dashboard auxilia o professor a direcionar intervenções..." | ✓ |
| Foco no fechamento do ciclo | "O dashboard fecha o ciclo: dos dados à decisão pedagógica" | |
| Sem frase de fechamento | Apenas wireframe + Fonte | |

**User's choice:** Foco no professor.

---

## MARKER-04 + END-01

### Q1: Estado das pills no MARKER-04?

| Option | Description | Selected |
|---|---|---|
| Todas 4 em --done | Default da Deferred Idea da fase 4 | |
| Pill 4 em --planned (proposta apresentada, sem código) | 3 done + pill 4 com novo modificador `--planned`; honesto sobre TCC 2 não implementado | ✓ |
| Pill 4 em --done com badge alternativo | Visualmente done com badge `[proposed]` | |

**User's choice:** Pill 4 em `--planned`.
**Notes:** Override da Deferred Idea da fase 4 (linha 349). Requer adicionar modificador `--planned` ao `.marker-pill` em `theme-unifacens.css` (D-96c). Compatibilidade preservada com MARKER-01/02/03.

### Q2: Posição relativa de MARKER-04 e END-01 no fim do deck?

| Option | Description | Selected |
|---|---|---|
| TOOL-01 → TOOL-03 → MARKER-04 → END-01 | Simetria com outros 3 marcadores | ✓ |
| TOOL-01 → TOOL-03 → END-01 → MARKER-04 | Marcador como pós-créditos | |
| TOOL-01 → MARKER-04 → TOOL-03 → END-01 | Marcador no meio | |

**User's choice:** TOOL-01 → TOOL-03 → MARKER-04 → END-01.

### Q3: Forma do slide END-01 (agradecimento)?

| Option | Description | Selected |
|---|---|---|
| Slide minimal com 'Obrigado.' | Fundo `#F1F6FB`, palavra centralizada grande | ✓ |
| Reuso do slide-cover-brand modificado | Bracket narrativo com a capa | |
| Slide-title-tcc modificado com recap | Layout do título + recap + obrigado | |

**User's choice:** Slide minimal.
**Notes:** Sem cabeçalho `> [seção]`. Rodapé com créditos discretos (nome + email/GitHub) defere ao checkpoint visual.

---

## Claude's Discretion

- Ordem de implementação dos 5 plans (sugestão: MARKER-04 → AGENDA-01 → END-01 → TOOL-03 → TOOL-01).
- Estética exata do modificador `--planned` (cor, ícone, borda).
- Componente exato do wireframe TOOL-03 (`.bridge-seq` adaptado vs `.dash-card` novo).
- Ilustração interna dos 3 painéis do TOOL-03 (barras stub vs scatter stub vs caixa-texto).
- Frase de fechamento opcional de TOOL-01 (corta se apertar).
- Cabeçalho exato do TOOL-03 (`> dashboard da aplicação` vs `> o dashboard`).
- END-01 rodapé (minimal puro vs com créditos discretos).
- Atualização do STYLE.md ao fim da fase (§Cabeçalho, §Inventário, §Gaps reservados, §Classes reutilizáveis).
- Update PROJECT.md ao fim da fase (Active → Validated, Key Decisions).

## Deferred Ideas

- Renomear "ferramenta" → "aplicação" em ROADMAP/REQUIREMENTS/PROJECT.md: **NÃO renomear** (REQ-IDs estáveis; vocabulário-projeto histórico).
- Cleanup CSS pós-refatoração AGENDA-01: remover classes órfãs `.slide-agenda`, `.agenda-side`, `.agenda-main`, `.agenda-list` se aplicável.
- Bracket narrativo END-01 ↔ slide-cover-brand: opcional, defere ao checkpoint.
- Modificador `--planned` documentado na memória `feedback_marker_design`: estender após travar a estética.
- Speaker notes / cronometragem: Out of Scope (PROJECT.md linha 103-104).
