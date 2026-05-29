# Phase 5: Implantação, Agenda e Encerramento (Fase 4 EDM) - Context

**Gathered:** 2026-05-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Inserir **4 slides novos** em `apresentacao/index.html` (TOOL-01, TOOL-03, MARKER-04, END-01) e **refatorar 1 slide existente** (slide-agenda na posição `#/2`, hoje com 8 bullets genéricos do template UniFacens). Resolver PENDING-01 (conteúdo da Agenda) em conjunto com a refatoração.

A sequência final entre MARKER-03 (atual `#/26`) e o fim do deck:

```
#/26 MARKER-03      Fase 3 EDM concluída                    (existente, fechado fase 4)
#/27 TOOL-01        Proposta da aplicação + pipeline 6 etapas (NOVO)
#/28 TOOL-03        Dashboard (wireframe 3 painéis)          (NOVO)
#/29 MARKER-04      Fase 4 EDM (Implantação --planned)        (NOVO)
#/30 END-01         Obrigado.                                (NOVO)
```

Slide `#/2` (slide-agenda) é refatorado in-place: nova estrutura interna (4 fases EDM como sumário) + cabeçalho `> agenda` no padrão `.deck-topic` (override de STYLE.md linha 39-42 que hoje exclui a Agenda do padrão; o STYLE.md precisa ser atualizado dentro desta fase).

Total esperado de sections ao fim da fase: 27 (pós-fase 4) + 4 novos (TOOL-01, TOOL-03, MARKER-04, END-01) = **31 sections**. Slide-agenda permanece `#/2` (refatoração não muda posição).

Vocabulário-chave: **"aplicação"** substitui **"ferramenta"** nesta fase (ver D-92). ROADMAP, REQUIREMENTS e PROJECT.md ainda referem como "ferramenta TCC 2"; nos slides e na fala diz-se "aplicação" porque a entrega contém ferramentas internas (extração de KCs, modelo de ML). Mantemos os REQ-IDs TOOL-01/TOOL-03 sem renomear (custo > benefício).

</domain>

<decisions>
## Implementation Decisions

### Posição no DOM (D-92.1)

- **D-92.1:** Ordem dos novos slides no fim do deck: TOOL-01 → TOOL-03 → MARKER-04 → END-01. Marcador fecha as 4 fases EDM ANTES do agradecimento (simetria com MARKER-01/02/03 que sempre fecham um bloco). END-01 é o último slide.
- **D-92.2:** Slide-agenda permanece em `#/2`; refatoração interna não desloca nada.
- **D-92.3:** Justificativa narrativa: MARKER-03 fechou "Modelagem ✓" com Implantação `--running`; TOOL-01 abre a proposta da aplicação; TOOL-03 mostra o dashboard (output final do pipeline); MARKER-04 fecha as 4 fases conceitualmente (Implantação como proposta, pill 4 em `--planned`); END-01 encerra. Defesa ≈ 10 min cabe com este desenho.

### Vocabulário "aplicação" vs "ferramenta" (D-92)

- **D-92:** Nos slides e na fala da fase 5, usa-se **"aplicação"** no lugar de "ferramenta". Razão (user, 2026-05-29): "é uma aplicação que contém ferramentas de extração de KCs, modelo de aprendizado de máquina". Implica: cabeçalho do TOOL-01 = `> proposta da aplicação`; TOOL-03 contextualiza como "dashboard da aplicação"; AGENDA-01 menciona "Implantação" no rótulo (canônico EDM) e "proposta da aplicação" na descrição se houver subtítulo. **REQ-IDs TOOL-01/TOOL-03 não são renomeados** (são identificadores estáveis); ROADMAP/REQUIREMENTS/PROJECT.md mantêm a redação "ferramenta TCC 2" como vocabulário-projeto histórico. Apenas o conteúdo dos slides usa "aplicação".

### AGENDA-01 — Refatoração do slide-agenda (D-93)

- **D-93a (estrutura):** **4 fases EDM como sumário**, espelhando exatamente os 4 marcadores (e as 4 pills do `.slide-marker`):
  1. Definição do Problema
  2. Preparação dos Dados
  3. Modelagem e Avaliação
  4. Implantação
- **D-93b (cabeçalho):** `> agenda` com caret piscando, no padrão `.deck-topic` (D-04..D-11 herdado). **OVERRIDE explícito do STYLE.md linha 39-42** que hoje exclui a AGENDA do padrão. Justificativa: consistência visual com todo o deck pós-AGENDA; AGENDA atual destoa (`<h2>Agenda</h2>` + agenda-side com logo grande). Atualizar STYLE.md §"Cabeçalho de todo slide após a AGENDA" no mesmo plan que refatora o slide.
- **D-93c (layout):** Refatorar para o template `.slide-related` (mesmo padrão dos demais slides de conteúdo) com cabeçalho + 4 itens listados. Remover `agenda-side` (logo grande) e `agenda-main`. Marca d'água Facens `<svg class="wm">` aplicada como nos slides de conteúdo. Lista vertical com numeração + nome de cada fase; um item por linha, tipografia Arial 21-23px.
- **D-93d (caret blink):** caret só no último item (Implantação), padrão herdado da agenda atual.
- **D-93e (rodapé):** sem "Fonte:" (Agenda é estrutural, não derivada de fonte externa). Compatível com slide-cover-brand e slide-title-tcc que também não têm "Fonte:".
- **D-93f (CSS órfão):** classes `.slide-agenda`, `.agenda-side`, `.agenda-main`, `.agenda-list` do `.slide-agenda` original podem ficar órfãs após refatoração. Decisão: **deletar do `theme-unifacens.css`** se não houver outro caller (análise no plan, paralelo ao cleanup de `.rel-kicker/.rel-title/.rel-sub` da fase 1, commit `30ba911`).

### TOOL-01 — Proposta da aplicação + pipeline 6 etapas (D-94)

- **D-94a (cabeçalho):** `> proposta da aplicação`
- **D-94b (abertura, 2 frases):** motivação + escopo, em 1ª pessoa do plural. Phrasing-alvo (ajuste fino no checkpoint):
  > "O processo apresentado pode ser instrumentalizado para professores. Propomos uma aplicação docente que organiza esse fluxo em seis etapas."

  Observação: "aplicação" no lugar de "ferramenta" (D-92).
- **D-94c (pipeline `.bridge-seq` 6 etapas):**
  1. **Submissões dos estudantes** (entrada; "submissões" no lugar de "ProgSnap2" porque ProgSnap2 só é nomeado em INTRO-01, gate herdado do PROJECT.md Key Decision linha 183)
  2. **Extração de KCs** (espelha o pipeline MODEL-05 do deck)
  3. **Professor valida** (gesto humano in-the-loop)
  4. **Preparação dos dados** (espelha o slide EDA-02 do deck)
  5. **Code-DKT** (espelha MODEL-01a/01b/03/04)
  6. **Dashboard** (saída; ponte natural para TOOL-03)

  Componente `.bridge-seq` reusado (zero CSS novo). Caixas neutras, sem destaque em nenhuma etapa (D-94d). Estilo idêntico ao pipeline 5 etapas do MODEL-05.

- **D-94d (sem destaque):** todas as 6 caixas neutras (sem azul UniFacens em nenhuma). Razão: o pipeline é um processo contínuo; destacar Code-DKT ou Dashboard cria hierarquia que confunde a narrativa "a aplicação espelha o que já mostramos".
- **D-94e (não detalhar):** **não** explicar cada etapa. ROADMAP Success Criterion 1 explicita "sem detalhar cada uma; pipeline espelha o que já foi mostrado nas fases 2-4, não repete conteúdo". Microcópia das caixas: verbo + 1 linha curta (como MODEL-05).
- **D-94f (fechamento textual):** opcional, 1 frase de ponte para TOOL-03. Phrasing-alvo (defere ao checkpoint):
  > "O dashboard fecha o ciclo e é o que detalhamos no próximo slide."

  Pode ser cortado se o slide ficar visualmente apertado em 1280×720.
- **D-94g (rodapé):** `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.` (adapted; manter consistência com Fonte das fases anteriores)
- **D-94h (sem ProgSnap2 nominal):** etapa 1 do pipeline diz "Submissões dos estudantes", não "ProgSnap2". Gate herdado do PROJECT.md Key Decision linha 183.

### TOOL-03 — Dashboard (wireframe 3 painéis) (D-95)

- **D-95a (cabeçalho):** `> dashboard da aplicação` (proposta; alternativa `> o dashboard` se ficar mais leve)
- **D-95b (forma):** **Wireframe estático com 3 painéis lado a lado**, estilo Word/ABNT monocromático (borda 1.5px preta, cantos retos, fundo branco; padrão STYLE.md §Diagramas linha 100-106). Sem screenshot do `docs/tcc2_prototipo.html` (eleva risco de ilegibilidade em 1280×720). Sem cards 2x2.
- **D-95c (3 painéis nomeados):**
  1. **Respostas de código da turma** (painel esquerdo)
  2. **Predição de conhecimento por estudante** (painel central)
  3. **Dificuldade da turma por KC** (painel direito)

  Cada painel: título em Arial bold preto + ilustração esquemática mínima (ex.: barras stub, scatter stub, ou só caixa-texto). Decisão da ilustração interna defere ao checkpoint visual (ver Claude's Discretion).
- **D-95d (componente CSS):** preferência por **reusar `.bridge-seq` adaptado** (mesma estética Word/ABNT já estabelecida). Se 3 caixas grandes verticais não couberem visualmente, anexar nova classe `.dash-card` em `theme-unifacens.css` (paralelo ao precedente `.eda-grid` da fase 3). Executor decide no plan; default = tentar `.bridge-seq` primeiro.
- **D-95e (fechamento textual, 1 frase):** foco no professor. Phrasing-alvo:
  > "O dashboard auxilia o professor a direcionar intervenções por estudante e por dificuldade."
- **D-95f (rodapé):** `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.`

### MARKER-04 — Fase 4 EDM concluída (Implantação --planned) (D-96)

- **D-96a (decisão central):** **Pill 4 (Implantação) em `--planned`**, NÃO `--done`. Razão (user, 2026-05-29): defesa apresenta a proposta da aplicação mas o TCC 2 (implementação) não foi feito. `--planned` reconhece honestamente que a Fase 4 EDM está prevista, não executada. Pills 1, 2, 3 todas em `--done` com `&check;`.
- **D-96b (override de Deferred Idea da fase 4):** O CONTEXT.md da fase 4 (linha 349) tinha como default "todas as 4 pills `--done`". Esta fase **override** essa default por honestidade epistemológica.
- **D-96c (CSS novo necessário):** O componente `.slide-marker` hoje suporta apenas `--done`, `--running`, `--pending` (commit `5d44606`). Precisa adicionar modificador **`--planned`** ao `theme-unifacens.css`. Sugestão de estética (defere ao plan/checkpoint):
  - Estilo intermediário entre `--pending` (cinza neutro) e `--running` (animado): sem animação, cor cinza azulada `#5b6472` ou borda tracejada
  - Ícone: pode ser `⋯` (etc) ou `◯` (círculo vazio) ou ícone de calendário/relógio sem girar
  - Badge: `[planned]`
- **D-96d (compatibilidade com MARKER-01/02/03):** adicionar `--planned` é aditivo; callers existentes (MARKER-01/02/03) não quebram. Mesma garantia do redesign CI/CD ABNT (commit `5d44606`).
- **D-96e (título e rodapé):** título `> AS QUATRO FASES DA EDM` em Arial bold 24px; rodapé `Fonte: adaptado de Zorić (2020).` (idênticos a MARKER-01/02/03).
- **D-96f (sem animação):** Pill 4 `--planned` NÃO gira (≠ `--running` da pill 4 no MARKER-03). Validar visualmente que a diferença `--running` (em MARKER-03) vs `--planned` (em MARKER-04) é clara.

### END-01 — Obrigado. (D-97)

- **D-97a (forma):** **Slide minimal**. Fundo `#F1F6FB` (consistente com slides de conteúdo). Palavra "Obrigado." centralizada vertical+horizontalmente, grande, Arial bold ou Cascadia (defere ao checkpoint).
- **D-97b (sem cabeçalho):** sem `.deck-topic` (END não é seção; é encerramento). Sem `> [seção]`.
- **D-97c (rodapé):** discreto, sem "Fonte:". Conteúdo padrão sugerido (defere ao checkpoint):
  - Nome do autor (Léo Kuntz ou nome formal do TCC)
  - Email institucional (se disponível) ou GitHub
  - Logo Facens pequeno (opcional)

  Estilo: Arial 16-18px cor `#5b6472`, alinhado à direita ou centralizado.
- **D-97d (sem marca d'água?):** decisão visual no checkpoint. Default: **sem `<svg class="wm">`** para reforçar minimalismo do encerramento. Verificar harmonia com slide-cover-brand (`#/0`) para criar bracket narrativo opcional.
- **D-97e (paleta):** texto principal em `--uni-ink` (#111317) ou `--uni-blue` (#2667FF) destaque sutil. Defere ao checkpoint.

### Convenções herdadas das fases 1-4 (re-locked)

- **D-98 (cabeçalho):** padrão `> [seção]` único (D-04..D-11 fase 1) aplica-se a TOOL-01 e TOOL-03. Slide-agenda **incorporado ao padrão** nesta fase (D-93b). MARKER-04 sem `> [seção]` temático (usa `.marker-title`). END-01 sem cabeçalho (D-97b).
- **D-99 (voz):** paráfrase indireta com autor parentético (D-69, D-79g herdado). 1ª pessoa do plural em TOOL-01 (D-94b). Sem citação direta literal nesta fase.
- **D-100 (sem em-dash):** D-44/D-87 herdado; memória `feedback_no_em_dashes` vinculante.
- **D-101 (itálico ABNT):** `<i>et al.</i>` em citações parentéticas múltiplas (D-54); termos estrangeiros em itálico minúsculas (`<i>pipeline</i>`, `<i>dashboard</i>` se aparecer no corpo, `<i>knowledge tracing</i>`, `<i>knowledge components</i>`); nomes próprios preservados (BKT, DKT, Code-DKT, CSEDM, ProgSnap2). **Importante:** "dashboard" pode ficar em redondo no cabeçalho `> dashboard da aplicação` (vocabulário cotidiano em PT-BR técnico); checar no checkpoint.
- **D-102 (estudantes, nunca alunos):** D-89 herdado. Em TOOL-01 etapa 1 ("Submissões dos estudantes"), em TOOL-03 painel 1 ("Respostas de código da turma"), em qualquer microcópia: usar "estudantes" ou "discentes".
- **D-103 (Fonte):** cada slide de conteúdo (TOOL-01, TOOL-03) tem `Fonte:` no rodapé Arial 17-18px cor `#5b6472`. MARKER-04 tem `Fonte: adaptado de Zorić (2020).` (herdado). END-01 sem Fonte. AGENDA-01 sem Fonte.

### Validação visual (D-104)

- **D-104:** Ao fim da fase, validar no browser (`cd apresentacao && python3 -m http.server 8000`) percorrendo do slide `#/0` ao `#/30`. Sucesso:
  - Navegação completa sem erro de console
  - AGENDA-01 (`#/2`) com cabeçalho `> agenda` e 4 fases EDM legíveis
  - TOOL-01 (`#/27`) com pipeline 6 etapas neutras cabendo em 1280×720
  - TOOL-03 (`#/28`) com wireframe 3 painéis legível
  - MARKER-04 (`#/29`) com 3 pills `--done` e pill 4 `--planned` (sem animação)
  - END-01 (`#/30`) com "Obrigado." centralizado
  - Tempo natural de defesa dentro de 10 min (validação subjetiva pelo apresentador)

### Claude's Discretion

- **Ordem de implementação:** sugestão neutra **MARKER-04 primeiro** (mecânico, só pequeno CSS novo `--planned`, valida ambiente), depois **AGENDA-01** (refatoração in-place com cleanup CSS, baixo risco), depois **END-01** (minimal), depois **TOOL-03** (wireframe 3 painéis com possível `.dash-card` novo), e por último **TOOL-01** (pipeline 6 etapas é a calibragem visual mais densa). Alternativa: TOOL-01 primeiro porque é o slide mais "pesado" do bloco e calibra o ritmo.
- **Granularidade dos commits:** 1 plan por slide (5 plans: AGENDA-01, TOOL-01, TOOL-03, MARKER-04, END-01); alinhado com fases 2-4.
- **Componente exato do wireframe TOOL-03:** `.bridge-seq` adaptado vs `.dash-card` novo. Default: tentar `.bridge-seq` primeiro; se 3 caixas grandes verticais não casarem, anexar `.dash-card`.
- **Modificador `--planned` do `.slide-marker`:** estética exata (cor, ícone, borda tracejada vs sólida) defere ao checkpoint visual do MARKER-04. Restrições: zero animação; visualmente distinguível de `--running` e de `--pending`; aditivo (não quebra callers existentes).
- **Ilustração interna dos 3 painéis do TOOL-03:** barras stub, scatter stub, ou só caixa-texto. Defere ao checkpoint; default = caixa-texto minimalista para evitar prometer pixel-perfect.
- **Frase de fechamento de TOOL-01 (D-94f):** opcional; corta se o slide ficar apertado.
- **Cabeçalho exato do TOOL-03:** `> dashboard da aplicação` vs `> o dashboard`. Defere ao checkpoint.
- **END-01 rodapé:** decidir no checkpoint entre minimal puro (só "Obrigado.") vs com nome+contato discreto.
- **Atualização do STYLE.md ao fim da fase:**
  - §"Cabeçalho de todo slide após a AGENDA" precisa ser **reescrito** porque a AGENDA agora também segue o padrão `.deck-topic` (D-93b). Reescrever o §título para "Cabeçalho de TODO slide (incluindo AGENDA)" e atualizar o exemplo.
  - §Inventário de slides (linhas 108-138) atualizado para 31 sections.
  - §Gaps reservados removido (não há mais fases).
  - §Classes reutilizáveis atualizado se `.dash-card` ou `--planned` forem adicionados.
- **PROJECT.md ao fim da fase:** mover todos os REQ-IDs validados de Active para Validated; atualizar Key Decisions com D-92 ("aplicação" vocabulário) e D-93b (override STYLE.md). Decisão sobre se "Apresentação TCC 1" milestone fica completa após a defesa ou se aguarda confirmação humana posterior fica para o git_commit step.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning ou implementar.**

### Decisões de projeto e contexto desta fase

- `.planning/PROJECT.md` — escopo, constraints (estilo, ABNT, 10 min, sem em-dash), Key Decisions linha 183 (eixo prioritário CLOSE-01/02/03 já entregue; ProgSnap2 só em INTRO-01; "entrada de submissões dos estudantes" no lugar de "entrada ProgSnap2" para a aplicação), Out of Scope linha 97-107 (implementação da ferramenta TCC 2 fora; só proposta visual).
- `.planning/REQUIREMENTS.md` §TOOL-01, §TOOL-03, §MARKER-04, §END-01, §AGENDA-01, §PENDING-01; tabela de Traceability linha 167-172.
- `.planning/ROADMAP.md` §"Phase 5: Implantação, Agenda e Encerramento (Fase 4 EDM)" linha 99-110 — Goal, Mode, Requirements, Success Criteria 1-6.
- `.planning/phases/01-reformata-o-da-base/01-CONTEXT.md` — decisões D-01..D-30 da fase 1 (padrão `> [seção]`, voz, STYLE.md, mapa de slides; herança crítica para o override D-93b).
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-CONTEXT.md` — decisões D-31..D-59 da fase 2 (D-54 `<i>et al.</i>` ABNT, D-44 sem em-dash, D-46 itálico).
- `.planning/phases/03-eda-e-pr-processamento-fase-2-edm/03-CONTEXT.md` — decisões D-60..D-74 da fase 3 (componentes ABNT `.eda-grid`/`.eda-fig`/`.eda-source`; D-67 reuso mecânico do `.slide-marker`).
- `.planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-CONTEXT.md` — decisões D-75..D-91 da fase 4 (D-84 modificadores `--done`/`--running`/`--pending` do `.slide-marker`; D-89 "estudantes" não "alunos"; Deferred Idea linha 349 "MARKER-04 todas 4 pills `--done`" — **OVERRIDE nesta fase por D-96a**).
- `.planning/phases/04-modelagem-e-avalia-o-fase-3-edm/04-05-SUMMARY.md` — resumo agregado da fase 4 (deck 21 → 27 sections).

### Estilo visual e citação (vinculante)

- `apresentacao/STYLE.md` — Identidade visual, paleta UniFacens, tipografia, regras de citação ABNT, inventário de slides pós-fase 4 (27 sections, linhas 108-138). **§Cabeçalho de todo slide após a AGENDA (linhas 39-42) será sobrescrito nesta fase (D-93b)**. §Gaps reservados (linhas 142-146) lista exatamente os slides desta fase (TOOL-01, TOOL-03, MARKER-04, END-01, AGENDA-01 revisado).
- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — Manual UniFacens de citação ABNT.

### Markup-alvo

- `apresentacao/index.html` — único arquivo HTML a editar; 27 `<section>` no estado pós-fase 4; 4 novos serão inseridos após MARKER-03 (linha 688+); slide-agenda (linhas 62-80) será refatorado in-place.
- `apresentacao/assets/theme-unifacens.css` — tema; componentes prontos para reuso: `.slide-marker` (suporte para `--planned` precisa ser **adicionado**, D-96c); `.bridge-seq` (slide Yağcí + MODEL-05) candidato para TOOL-01 (6 etapas) e potencialmente TOOL-03 (3 painéis); `.deck-topic` aplicado também ao slide-agenda (D-93b). Eventuais classes novas: `.dash-card` (TOOL-03 se `.bridge-seq` não casar) e modificador `--planned` em `.marker-pill`.

### Protótipo e dados de fonte

- `docs/tcc2_prototipo.html` (60 KB, 952 linhas) — **base canônica do TOOL-01 e TOOL-03**. Estrutura: sidebar com 6 páginas (id="page-upload", "page-kc", "page-eda", "page-kt", "page-rec", "page-chat"). Tags ABNT relevantes: `tag-intended` / `tag-emerged` (validação humana de KCs). Para TOOL-01: a sequência das páginas (Upload → KC → EDA → KT → Rec/Chat) inspira o pipeline 6 etapas, mas o pipeline do slide é **redesenhado conceitualmente** (Submissões → Extração KCs → Professor valida → Preparação → Code-DKT → Dashboard), não copiado da estrutura HTML.
- Para TOOL-03 wireframe: usar `page-eda` (linha 416-) e `page-kt` (linha 494-) como referência conceitual dos 3 painéis (respostas, predição, dificuldade). **Não copiar layout do protótipo**; rascunhar wireframe Word/ABNT.

### Memórias (auto-context, vinculantes)

- `~/.claude/.../memory/feedback_marker_design.md` — MARKER-XX componente CI/CD ABNT; modificadores `--done`/`--running`/`--pending` + badges (precisa **estender** com `--planned`, D-96c).
- `~/.claude/.../memory/feedback_no_em_dashes.md` — vinculante para D-100.
- `~/.claude/.../memory/feedback_tcc_writing_style.md` — ABNT + prosa acessível.
- `~/.claude/.../memory/feedback_estudantes_nao_alunos.md` — "estudantes" em prosa nova (D-102).
- `~/.claude/.../memory/feedback_abnt_tabela_slides.md` — padrão ABNT para tabelas (não aplica direto a esta fase; precedente para diagrama Word/ABNT em TOOL-03).
- `~/.claude/.../memory/feedback_correlatos_antes.md` — cabeçalho `> [seção]` substitui "trabalhos correlatos" e nome de autor (precedente para a refatoração AGENDA-01).
- `~/.claude/.../memory/reference_manual_citacoes.md` — manual Facens; "tradução nossa" só em direta literal estrangeira; voz padrão é paráfrase indireta.

### Codebase context já gerado

- `.planning/codebase/STRUCTURE.md` — onde inserir slides em `apresentacao/index.html`.
- `.planning/codebase/CONVENTIONS.md` — convenções de redação e commit message style (lowercase português, prefixo `apresentacao:`).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets (sem CSS novo, exceto onde indicado)

- `.deck-topic` + `.caret.blink` (em `theme-unifacens.css`): padrão de cabeçalho `> [seção]`. Aplica em AGENDA-01 (refatorado, D-93b), TOOL-01 e TOOL-03.
- `.slide-marker` + `.marker-track` + `.marker-stage` + `.marker-pill` + modificadores `--done`/`--running`/`--pending` + `.marker-pill-icon` + `.marker-pill-name` + `.marker-arrow` + `.marker-badge` + `.marker-title` + `.rel-cite`: **componente quase pronto** para MARKER-04 reusar. **Falta adicionar modificador `--planned`** (D-96c). Demais classes intactas.
- `.bridge-seq` + `.step` + `.arr` (slide Yağcí + MODEL-05): candidato principal para pipeline TOOL-01 (6 etapas) E potencialmente para wireframe TOOL-03 (3 painéis). MODEL-05 já valida 5 etapas; precisamos validar visualmente que 6 cabem em 1280px.
- `.slide-related` template: pode ser reusado para wrapper de AGENDA-01 refatorado e para TOOL-01/TOOL-03 (mesmo padrão dos demais slides de conteúdo).
- `.rel-lead` + `.rel-cite` (template `slide-related`): para introdução textual de TOOL-01 e TOOL-03 (D-94b, D-95e) e rodapé "Fonte:".
- Marca d'água Facens `<svg class="wm">`: replicar nos 3 novos slides de conteúdo (AGENDA-01 refatorado, TOOL-01, TOOL-03). MARKER-04 herda padrão MARKER-01/02/03. END-01 sem marca d'água (D-97d default).

### Established Patterns

- Estrutura de slide: `<section data-background-color="#F1F6FB"><div class="deck-slide slide-XYZ">...</div></section>`. **NUNCA mudar.**
- Comentário acima de cada `<section>`: `<!-- ============ SLIDE · descrição ============ -->`.
- Tipografia: títulos/corpo em Arial; tópico `>` em Cascadia 24px; "Fonte:" em Arial 17-18px.
- Cores: paleta UniFacens (`--uni-blue #2667FF`, `--uni-ink #111317`, fundo `#F1F6FB`, cinza secundário `#5b6472`).
- Citação parentética: `(Autor, ano)` sem `p. X` em paráfrase indireta; `<i>et al.</i>` ABNT (D-101).
- Iterações textuais pós-checkpoint: padrão herdado das fases 2-4 (média 1-3 por slide); reviewer humano ajusta no browser.

### Integration Points

- Único arquivo HTML a editar: `apresentacao/index.html`.
- CSS recebe acréscimos definidos:
  - **Modificador `--planned`** em `.marker-pill` (D-96c, mandatory)
  - **Classe `.dash-card`** se `.bridge-seq` não casar para TOOL-03 (D-95d, opcional)
- CSS recebe limpeza opcional: classes `.slide-agenda`, `.agenda-side`, `.agenda-main`, `.agenda-list` órfãs após refatoração (D-93f).
- Browser: `cd apresentacao && python3 -m http.server 8000` → http://127.0.0.1:8000/#/N. Após inserção: AGENDA-01 refatorado fica em `#/2`; TOOL-01 = `#/27`, TOOL-03 = `#/28`, MARKER-04 = `#/29`, END-01 = `#/30`.
- Sem build system; recarregar página direto.

### Slides existentes pós-fase 4 (estado HEAD; índice 0-based)

| # | classe | cabeçalho | papel na fase 5 |
|---|---|---|---|
| 0 | slide-cover-brand | (sem) | inalterado |
| 1 | slide-title-tcc | (sem) | inalterado |
| 2 | slide-agenda | `<h2>Agenda</h2>` interno | **REFATORADO** in-place: 4 fases EDM + `> agenda` (D-93) |
| 3-9 | (intro + fase 1 EDM) | — | inalterados |
| 10-15 | (dataset + fase 2 EDM + MARKER-02) | — | inalterados |
| 16-26 | (fase 3 EDM modelagem + MARKER-03) | — | inalterados |

### Slides a criar (4 novos)

| # após inserção | classe sugerida | cabeçalho | requirement |
|---|---|---|---|
| 27 | `slide-related` | `> proposta da aplicação` | TOOL-01 |
| 28 | `slide-related` | `> dashboard da aplicação` (ou `> o dashboard`) | TOOL-03 |
| 29 | `slide-marker slide-marker--phase4` | (sem temático; usa `.marker-title`) | MARKER-04 |
| 30 | `slide-end` (nova ou minimal) | (sem cabeçalho) | END-01 |

Nomenclatura de classes em sugestão; executor decide pelo que casa melhor com STYLE.md.

### Slide-agenda refatorado (proposta de markup)

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

Classe `.agenda-edm-list` candidata (nova, mínima); ou reaproveitar `.rel-lead` em sequência. Defere ao plan.

</code_context>

<specifics>
## Specific Ideas

- **AGENDA-01 phrasing alvo:**
  - Cabeçalho: `> agenda`
  - Lista numerada (4 itens, espelha pills do MARKER):
    1. Definição do Problema
    2. Preparação dos Dados
    3. Modelagem e Avaliação
    4. Implantação
  - Caret blink no último item (Implantação)

- **TOOL-01 phrasing alvo (rascunho):**
  - Cabeçalho: `> proposta da aplicação`
  - Abertura (2 frases): "O processo apresentado pode ser instrumentalizado para professores. Propomos uma aplicação docente que organiza esse fluxo em seis etapas."
  - Pipeline `.bridge-seq` 6 etapas (todas neutras, sem destaque):
    `[1. Submissões dos estudantes] → [2. Extração de KCs] → [3. Professor valida] → [4. Preparação dos dados] → [5. Code-DKT] → [6. Dashboard]`
  - Fechamento opcional (1 frase): "O dashboard fecha o ciclo e é o que detalhamos no próximo slide."
  - Rodapé: `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.`

- **TOOL-03 phrasing alvo (rascunho):**
  - Cabeçalho: `> dashboard da aplicação` (ou `> o dashboard`)
  - Wireframe 3 painéis (estilo Word/ABNT, borda 1.5px preta, fundo branco, cantos retos):
    `[Respostas de código da turma]   [Predição de conhecimento por estudante]   [Dificuldade da turma por KC]`
  - Cada painel: título Arial bold preto + ilustração esquemática mínima (defere ao checkpoint)
  - Fechamento: "O dashboard auxilia o professor a direcionar intervenções por estudante e por dificuldade."
  - Rodapé: `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.`

- **MARKER-04 markup-alvo:** copiar a section do MARKER-03 (`#/26`); alterar:
  - classe modificadora da `<section>` de `slide-marker--phase3` para `slide-marker--phase4`
  - pill 3 (Modelagem) mantém `--done` + `&check;` + `[done]` (já fechado na fase 4)
  - pill 4 (Implantação) muda de `--running` (girando) para **`--planned`** (novo modificador; ícone sem animação; badge `[planned]`)
  - badges: pills 1, 2, 3 = `[done]`; pill 4 = `[planned]`
  - tudo o resto idêntico (título, rodapé, classes)

- **END-01 markup-alvo (rascunho):**
  ```html
  <!-- ============ SLIDE · Obrigado ============ -->
  <section data-background-color="#F1F6FB">
    <div class="deck-slide slide-end">
      <p class="end-thanks">Obrigado.</p>
      <p class="end-credits">Léo Kuntz · TCC 1 · UniFacens · 2026</p>
    </div>
  </section>
  ```
  Layout: flex column centralizado vertical+horizontal. Classes novas mínimas (`.slide-end`, `.end-thanks`, `.end-credits`). Conteúdo dos credits defere ao checkpoint.

</specifics>

<deferred>
## Deferred Ideas

- **Estética exata do modificador `--planned`:** cor (cinza azulado vs cinza neutro), ícone (`⋯` etc, `◯` círculo vazio, ou ícone de calendário), borda (sólida vs tracejada). Defere ao checkpoint visual do MARKER-04. Restrições já travadas: zero animação; distinguível de `--running` e `--pending`; aditivo (não quebra MARKER-01/02/03).
- **Ilustração interna dos 3 painéis do TOOL-03:** barras stub, scatter stub, ou só caixa-texto. Defere ao checkpoint. Default sugerido: caixa-texto minimalista (não promete pixel-perfect).
- **Frase de fechamento opcional de TOOL-01 (D-94f):** corta se o slide ficar apertado em 1280×720.
- **Cabeçalho exato do TOOL-03:** `> dashboard da aplicação` vs `> o dashboard` vs outra variação. Defere ao checkpoint.
- **END-01 rodapé com nome+contato:** decidir minimal puro vs com créditos discretos. Conteúdo dos créditos (email vs GitHub vs só nome) defere ao checkpoint.
- **Renomear "ferramenta" → "aplicação" em ROADMAP/REQUIREMENTS/PROJECT.md:** **NÃO renomear** (REQ-IDs TOOL-01/TOOL-03 são identificadores estáveis; vocabulário "ferramenta" é histórico-projeto). Apenas slides e fala usam "aplicação" (D-92).
- **Cleanup CSS pós-refatoração AGENDA-01:** verificar se `.slide-agenda`, `.agenda-side`, `.agenda-main`, `.agenda-list` ficam órfãs e remover (D-93f), paralelo ao precedente de `.rel-kicker/.rel-title/.rel-sub` da fase 1.
- **Update STYLE.md §"Cabeçalho de todo slide após a AGENDA":** **fazer dentro desta fase**, no plan de AGENDA-01 ou no fechamento. Reescrever o §título para "Cabeçalho de todo slide (incluindo AGENDA)" e atualizar exemplo. Atualizar inventário linhas 108-138 para 31 sections. Remover §Gaps reservados.
- **Update PROJECT.md ao fim da fase:** mover REQ-IDs TOOL-01, TOOL-03, MARKER-04, END-01, AGENDA-01 de Active para Validated; adicionar D-92 e D-93b em Key Decisions. Defere ao fechamento da fase.
- **Modificador `--planned` documentado na memória `feedback_marker_design`:** estender a memória existente com o novo modificador depois que a estética estiver travada no checkpoint. Defere ao fim da fase 5.
- **Speaker notes / cronometragem:** Out of Scope do PROJECT.md (linha 103-104). Validação visual no browser é a única gate; cronometragem é responsabilidade do apresentador, não do roadmap.
- **Bracket narrativo END-01 ↔ slide-cover-brand (`#/0`):** opcional. Se durante checkpoint o END-01 minimal soar desconectado do tom da capa, considerar reusar identidade visual da capa. Não criar requirement por enquanto.

### Reviewed Todos (not folded)

Nenhum todo cruzado para esta fase (`gsd-sdk query todo.match-phase 5` não consultado; padrão das fases 1-4 com 0 matches).

</deferred>

---

*Phase: 5-Implantação, Agenda e Encerramento (Fase 4 EDM)*
*Context gathered: 2026-05-29*
