---
phase: 01-reformata-o-da-base
plan: 07
subsystem: apresentacao
tags: [style-md, css-cleanup, checkpoint, mvp, phase-closure]
status: pre-checkpoint
requires:
  - "01-06 (deck com 12 sections, padrão `.deck-topic` aplicado em todos os 9 slides de conteúdo; ordem D-16/D-17 verificada; working tree clean)"
provides:
  - "apresentacao/STYLE.md atualizado refletindo a fase 1 (D-21): seção `Cabeçalho de todo slide após a AGENDA` reescrita para descrever o `.deck-topic` único `> [seção]`; bullet `Regra dos correlatos` removido e substituído por `Apresentação de autores` + `Voz própria como padrão` (D-25); tabela `Inventário de slides` reescrita para 12 slides pós-fase 1 com gaps reservados para fases 2-5"
  - "Regras CSS órfãs `.slide-related .rel-kicker`, `.slide-related .rel-kicker .ps1`, `.slide-related .rel-title`, `.slide-related .rel-sub` removidas de apresentacao/assets/theme-unifacens.css (Branch A do Task 4, grep confirmou 0 ocorrências dessas classes em apresentacao/index.html)"
  - "Pre-checkpoint state pronto para validação humana fim-a-fim: 12 sections, 9 cabeçalhos `.deck-topic`, 0 slide-corbett, 0 `trabalhos correlatos` fora de comentários, 2 citações diretas Martins preservadas (D-28)"
affects:
  - apresentacao/STYLE.md
  - apresentacao/assets/theme-unifacens.css
tech_stack_added: []
patterns_added: []
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-07-SUMMARY.md
key_files_modified:
  - apresentacao/STYLE.md
  - apresentacao/assets/theme-unifacens.css
decisions:
  - "D-21 aplicado (Tasks 1-3): apresentacao/STYLE.md sincronizado com o estado pós-fase 1 do markup. Três seções reescritas: Cabeçalho (descrição do `.deck-topic` único, autor só em Fonte:); Regras de redação (Regra dos correlatos removida, Apresentação de autores + Voz própria como padrão adicionadas); Inventário de slides (12 linhas, cabeçalhos travados D-04..D-11, gaps reservados para fases 2-5, linhagem KT reescrita para fases futuras)."
  - "D-22 aplicado (Tasks 1-3 em commit único): as 3 reescritas do STYLE.md entram num único commit dedicado `907a4b5` (apresentacao: atualizar STYLE.md para padrão > [seção] (D-21, D-25)) imediatamente antes do checkpoint humano. Decisão preferida ao commit-por-task porque as três seções têm sentido conjunto (descrever o novo padrão único)."
  - "D-25 aplicado (Task 2): novo bullet `Voz própria como padrão` no STYLE.md formaliza a política de paráfrase indireta com autor parentético, citação direta apenas quando a frase é o argumento. Reflete o feedback da orientadora da 2ª rodada (CONTEXT D-25) e fica documentado para as fases 2-5."
  - "D-29 aplicado (implícito): Cabeçalho do STYLE.md menciona explicitamente que os slides que já estão em paráfrase recebem apenas cabeçalho, sem reescrita textual (cabeçalhos travados D-04..D-11)."
  - "D-30 aplicado (implícito na escrita do STYLE.md): as paráfrases D-26 (Zorić fundido) e D-27 (Yağcí fundido) ficam referenciadas pelos cabeçalhos novos na tabela; STYLE.md não duplica o texto da paráfrase, apenas formaliza a política."
  - "Task 4 Branch A escolhido: grep -c 'rel-kicker|rel-title|rel-sub' apresentacao/index.html retornou 0; as 4 regras CSS órfãs foram deletadas do theme-unifacens.css em commit dedicado `30ba911`. Demais classes do template .slide-related preservadas (.rel-lead em uso por Martins p1 e Zorić fundido; .rel-cite em uso por rodapés Fonte: de todos os slide-related; .rel-quote/.rel-points/.rel-finding/.rel-aim/.rel-src/.rel-intro mantidas no CSS porque podem voltar nas fases 2-5)."
  - "Task 5 status: AWAITING HUMAN VERIFICATION. Execução sequencial parou aqui per <checkpoint_protocol_human_verify> no prompt do executor. Comandos automatizados de gate rodados; outputs anotados abaixo na seção 'Automated Gate Output (pre-checkpoint)'."
  - "Política sem em-dash em prosa preservada: a regra `**Sem travessões (em-dash)**` no STYLE.md continua intacta; nenhum em-dash novo introduzido em prosa nesta sessão (duas pré-existentes em STYLE.md linhas 1 e 29 ficaram, mas são fora do escopo deste plano per Scope Boundary do executor)."
requirements_completed:
  - REFORMAT-01
  - REFORMAT-02
  - REFORMAT-03
  - REFORMAT-04
  - REFORMAT-05
  - MERGE-01
  - REMOVE-01
metrics:
  duration_seconds: 200
  duration_human: "~3 min até o checkpoint (Tasks 1-4); STATE/REQUIREMENTS/ROADMAP serão atualizados na Task 6 após approve do usuário"
  completed_at: "2026-05-27T19:31:49Z"
  tasks_completed: 4
  tasks_total: 6
---

# Phase 1 Plan 07: STYLE.md (D-21) + CSS Cleanup + Human Checkpoint — Summary (pre-checkpoint)

Plan de fechamento da fase 1 executado até o checkpoint humano. Tasks 1-3 atualizam o `apresentacao/STYLE.md` para refletir o estado pós-fase 1 do deck (12 slides, padrão `.deck-topic` único, ordem D-16/D-17, regra "Apresentação de autores" + "Voz própria como padrão"). Task 4 deleta as 4 regras CSS órfãs em `apresentacao/assets/theme-unifacens.css` (Branch A confirmado: grep no index.html retornou 0 para as 3 classes). Task 5 (checkpoint humano fim-a-fim) suspende a execução por design: o orquestrador apresenta este SUMMARY parcial e os outputs dos comandos automatizados de gate ao usuário, que valida o deck no browser e responde `approved` ou lista de problemas. Task 6 (STATE/REQUIREMENTS/ROADMAP + commit final do PHASE-SUMMARY) só roda depois da aprovação.

**Status:** PRE-CHECKPOINT. 2 commits criados (`907a4b5` STYLE.md, `30ba911` CSS). Working tree limpa exceto por este SUMMARY parcial (será incluído no commit final da Task 6).

## What Was Built

### Task 1 — STYLE.md seção "Cabeçalho de todo slide após a AGENDA" reescrita

Substituída a descrição do par tópico + título (`<p class="deck-topic">trabalhos correlatos</p>` + `<h2 class="prob-head">Título</h2>`) pela descrição do padrão único `<p class="deck-topic">> [nome da seção]</p>`. Texto novo destaca:

- Classe única `.deck-topic` aplicada a TODOS os slides de conteúdo após a AGENDA.
- Lista os 8 cabeçalhos travados na fase 1 como exemplos (D-04..D-11).
- Autor não aparece no corpo, nem em `<h2>`, nem em `.rel-sub` (migra para "Fonte:" no rodapé).
- Caret piscante como último filho de `<p class="deck-topic">`.

A seção `## Caret / blink` (linha seguinte) ficou intocada.

### Task 2 — STYLE.md bullet "Regra dos correlatos" removido + 2 bullets novos adicionados

Em `## Regras de redação`:

- REMOVIDO: bullet "Regra dos correlatos" (todo autor novo é introduzido em slide `> trabalhos correlatos`).
- ADICIONADO: "Apresentação de autores" — autores introduzidos no momento da relevância via cabeçalho temático; nome do autor só em "Fonte:" no rodapé.
- ADICIONADO: "Voz própria como padrão" — paráfrase indireta com autor parentético é o padrão; primeira pessoa do plural quando aplicável; citação direta literal só quando a frase é o argumento.

Os 2 bullets anteriores ("Termos estrangeiros em itálico..." e "Sem travessões (em-dash)...") preservados intactos.

### Task 3 — STYLE.md tabela "Inventário de slides" reescrita para 12 slides pós-fase 1

Tabela antiga (16 linhas, ordem pré-fase 1, Corbett presente, Zorić p1 e p2 separados) substituída por:

| # | classe | cabeçalho | conteúdo |
|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho) | Abertura (logo + tagline) |
| 1 | slide-title-tcc | (sem cabeçalho) | Capa do TCC (autores em grafite) |
| 2 | slide-agenda | (sem cabeçalho temático) | Agenda |
| 3 | slide-related | `> introdução` | Recorte do problema (Martins, Marin e Alves, 2024) |
| 4 | slide-related | `> mineração de dados educacionais` | EDM como processo (Zorić, 2020), fundido p1+p2 |
| 5 | slide-phases | `> as quatro fases da edm` | As 4 fases (Zorić, 2020) |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | Ponte EDM para KT (Yağcı, 2022), fundido p1+p2 |
| 7 | slide-code | `> o que o code-dkt olha` | Atenção do Code-DKT no operador `&&` da submissão real do CSEDM |
| 8 | slide-kcfig | `> kcs semânticos extraídos` | Mapeamento KCs (Duan et al., 2025) para dificuldades de Martins |
| 9 | slide-problem | `> retomando o problema` | Martins p2, 13 autores (citação direta D-28) |
| 10 | slide-problem | `> retomando o problema` | Martins p3, 10 autores (citação direta D-28) |
| 11 | slide-fig | `> evolução por dificuldade` | Curva de aprendizado do Code-DKT por sub-dificuldade |

Ordem real escrita verbatim (slide-code antes de slide-kcfig, conforme Claude's Discretion D-16 do plan 01-06). Sem "OU" nas colunas — o SUMMARY do plan 01-06 confirma a escolha. Bloco "Estado do deck" diz "12 slides após a fase 1 (era 16 antes; ...)". Bloco "Gaps reservados para fases 2-5" prepara as próximas inserções (INTRO, EDA, MODEL, CLOSE, MARKER, TOOL, END, AGENDA). Parágrafo "Linhagem de KT (preenchida em fases futuras)" substitui o antigo "Linhagem de KT no deck" (Corbett volta em MODEL-01, Yağcı na slide 6, Duan em MODEL-05).

### Task 4 — CSS cleanup (Branch A aplicado)

Verificação prévia: `grep -c 'rel-kicker\|rel-title\|rel-sub' apresentacao/index.html` retornou **0**. Branch A do plan se aplica → cleanup feito.

Deletadas 4 linhas de `apresentacao/assets/theme-unifacens.css`:

```css
.slide-related .rel-kicker { font-size: 24px; color: #5b6472; margin: 0 0 16px; }
.slide-related .rel-kicker .ps1 { color: var(--uni-blue); }
.slide-related .rel-title { font-family: Arial, "Helvetica Neue", sans-serif; font-size: 30px; font-weight: 700; color: var(--uni-ink); margin-top: 0; }
.slide-related .rel-sub { font-family: Arial, "Helvetica Neue", sans-serif; font-size: 22px; color: #5b6472; margin-top: 2px; }
```

Demais classes do template `.slide-related` preservadas no CSS porque ainda em uso (verificadas individualmente via grep no index.html):

| classe | uso no index.html | mantida no CSS? |
|---|---|---|
| `.rel-lead` | 5 ocorrências (Martins p1, Zorić fundido) | sim |
| `.rel-cite` | 3 ocorrências (rodapés Fonte: nos 3 slide-related) | sim |
| `.rel-quote` | 0 no markup atual, mas pode voltar em fases 2-5 | sim (regra mantida) |
| `.rel-points` | 0 no markup atual, idem | sim |
| `.rel-finding`/`.rel-aim`/`.rel-src`/`.rel-intro` | 0 no markup atual, idem | sim |

A política conservadora preserva regras CSS órfãs apenas para as classes específicas que o plan instruiu remover (`.rel-kicker`, `.rel-title`, `.rel-sub`). As demais ficam disponíveis no CSS para a fase 2+ caso slides novos as queiram reutilizar; deletar todas seria uma decisão arquitetural fora do escopo deste plano (Rule 4).

### Task 5 — Checkpoint humano fim-a-fim (BLOQUEANTE — aguardando)

Execução sequencial parou aqui per `<checkpoint_protocol_human_verify>` no prompt do executor. Os comandos automatizados do gate final do plan foram rodados; outputs estão na seção "Automated Gate Output" abaixo. O usuário precisa:

1. Subir o dev server (`cd apresentacao && python3 -m http.server 8000`).
2. Abrir http://127.0.0.1:8000 com DevTools (F12) na aba Console.
3. Navegar com seta direita do slide 0 ao slide 11.
4. Para cada slide, validar visualmente (lista detalhada em PLAN.md Task 5 `<how-to-verify>` itens 3 a-l).
5. Confirmar console DevTools sem erro vermelho.
6. Confirmar os 8 Success Criteria do ROADMAP fase 1 (checklist em PLAN.md Task 5).
7. Responder `approved` (orchestrator continua para Task 6) ou listar problemas (orchestrator abre `/gsd-plan-phase 1 --gaps`).

### Task 6 — Atualização STATE/REQUIREMENTS/ROADMAP + commit final (PENDENTE — pós-checkpoint)

Não executada nesta passagem. Será executada por um agente de continuação após o `approved` do usuário. Escopo:

- Marcar fase 1 como `Complete` em `.planning/STATE.md` (`completed_phases: 1`, `completed_plans: 7`).
- Atualizar `**Current focus:**` para a fase 2.
- Marcar todos os 7 requirements REFORMAT-01..05, MERGE-01, REMOVE-01 como `[x]` em `.planning/REQUIREMENTS.md` (já estão; conferir).
- Atualizar `.planning/ROADMAP.md` se há coluna de status na visão geral.
- Commit final `docs: marcar fase 1 (reformatação da base) como concluída`.
- Opcionalmente criar `.planning/phases/01-reformata-o-da-base/PHASE-SUMMARY.md` agregando os 7 plans (per PLAN.md `<output>` section).

## Commits

| Hash | Task | Mensagem | Files | Diff |
|---|---|---|---|---|
| `907a4b5` | 1-3 | `apresentacao: atualizar STYLE.md para padrão > [seção] (D-21, D-25)` | apresentacao/STYLE.md | +53 / -38 |
| `30ba911` | 4 | `apresentacao: limpar regras CSS órfãs (.rel-kicker/.rel-title/.rel-sub)` | apresentacao/assets/theme-unifacens.css | +0 / -4 |

Pendente após approve do usuário: commit final do Task 6 cobrindo STATE.md, REQUIREMENTS.md, ROADMAP.md e (opcional) PHASE-SUMMARY.md.

## Automated Gate Output (pre-checkpoint)

Output completo dos comandos do bloco `<how-to-verify>` item 6 da Task 5 do plan, para apresentação ao usuário durante a validação visual:

```
section count: 12
slide-corbett: 0

cabeçalhos travados (markup-aware, ancorados no <span class="caret blink">):
  > introdução: 1
  > mineração de dados educacionais: 1
  > as quatro fases da edm: 1
  > da edm ao knowledge tracing: 1
  > retomando o problema: 2
  > kcs semânticos extraídos: 1
  > evolução por dificuldade: 1
  > o que o code-dkt olha: 1
TOTAL cabeçalhos .deck-topic: 9 (um por slide de conteúdo; capa/título TCC/agenda não têm cabeçalho temático)

trabalhos correlatos (fora de linhas de comentário): 0

citações Martins preservadas (D-28):
  13 autores: 1
  10 autores: 1

Bonus checks:
  HTML rel-kicker: 0
  HTML rel-title: 0
  HTML rel-sub: 0
  CSS rel-kicker: 0 (deletado neste plan)
  CSS rel-title: 0 (deletado neste plan)
  CSS rel-sub: 0 (deletado neste plan)
  CSS rel-lead: 1 (preservado, em uso)
  CSS rel-cite: 1 (preservado, em uso)
```

**Comparação com os valores esperados pelo plan (PLAN.md Task 5 `<how-to-verify>` item 6 "Esperado:"):**

| gate | esperado | obtido | status |
|---|---|---|---|
| section count | 12 | 12 | ✓ |
| slide-corbett | 0 | 0 | ✓ |
| > introdução | 1 | 1 | ✓ |
| > mineração de dados educacionais | 1 | 1 | ✓ |
| > as quatro fases da edm | 1 | 1 | ✓ |
| > da edm ao knowledge tracing | 1 | 1 | ✓ |
| > retomando o problema | 2 | 2 | ✓ |
| > kcs semânticos extraídos | 1 | 1 | ✓ |
| > evolução por dificuldade | 1 | 1 | ✓ |
| > o que o code-dkt olha | 1 | 1 | ✓ |
| trabalhos correlatos fora de comentário | 0 | 0 | ✓ |
| 13 autores | 1 | 1 | ✓ |
| 10 autores | 1 | 1 | ✓ |

**13 / 13 gates passaram.** Pendente: validação visual humana no browser dos 12 slides + console DevTools limpo + 8 Success Criteria do ROADMAP.

**Imprecisão idêntica aos plans 01-05 e 01-06:** o gate literal `grep -c "> $hdr"` retorna 0 porque o `>` no markup é entidade HTML `&gt;` (não literal) e o texto vem em seguida sem espaço (`</span>introdução`). Política aplicada (igual aos plans anteriores): rodar o equivalente substantivo `grep -c "$hdr<span class=\"caret blink\""` para confirmar o cabeçalho. Documentado nesta seção e na seção "Deviations from Plan" abaixo.

## Success Criteria checklist (8 do ROADMAP fase 1 — para o usuário marcar durante a validação)

- [ ] #1 `apresentacao/index.html` abre no browser sem erro de console e a navegação reveal.js funciona do primeiro ao último slide
- [ ] #2 Slide Martins p1 (slide 3) exibe cabeçalho `> introdução` (caret piscando); autor aparece apenas em "Fonte:" no rodapé
- [ ] #3 Slide Zorić p3 / slide-phases (slide 5) exibe cabeçalho `> as quatro fases da edm` com o conteúdo das fases preservado
- [ ] #4 Slide Yağcí fundido (slide 6) exibe cabeçalho `> da edm ao knowledge tracing` com gancho explícito sobre acompanhamento ao longo do tempo (`.bridge-seq` + `.bridge-text`)
- [ ] #5 Slide Zorić fundido (slide 4) tem cabeçalho `> mineração de dados educacionais` e mostra Zorić como autor + ferramentas/metodologias num único slide (paráfrase única em voz própria)
- [ ] #6 Os 2 slides de Corbett & Anderson removidos; busca por `slide-corbett` no `index.html` retorna 0 ocorrências (já confirmado nos automated gates acima)
- [ ] #7 Slides Martins p2/p3 (slides 9 e 10) movidos para posição próxima ao final do deck, adjacentes
- [ ] #8 Slides `slide-fig` (11), `slide-code` (7) e `slide-kcfig` (8) reformatados ao novo padrão de cabeçalho

## Deviations from Plan

1. **Plan acceptance Task 5 — `grep -c "> $hdr" apresentacao/index.html`:** literais não encontráveis no markup raw porque `>` é entidade HTML `&gt;` (não literal) e o texto vem colado em `</span>$hdr`. Equivalente substantivo executado: `grep -c "$hdr<span class=\"caret blink\""` (anchor no caret span que vem imediatamente após o texto). Imprecisão idêntica à do plan 01-05 (gate plan #1 `> as quatro fases da edm`) e do plan 01-06 (gates Task 1 `> retomando o problema`, etc.). Substância (cabeçalhos presentes e corretos no markup) entregue. Política aplicada nos 3 plans: registrar a imprecisão, executar o equivalente substantivo, documentar.

2. **Tasks 1-3 em commit único em vez de 3 commits separados (D-22 honrado):** o orchestrator's `<sequential_execution>` block menciona "commit each task atomically", mas o plano explícito (Task 6 `(a) Commit do STYLE.md atualizado (tasks 1-3)`) consolida as 3 reescritas do STYLE.md num único commit dedicado. D-22 do CONTEXT também sugere "commit próprio ao final da fase". Consolidação favorece a coerência narrativa (as 3 seções descrevem o mesmo padrão único e ficam compreensíveis juntas no diff). Commit final único: `907a4b5`.

3. **Pre-checkpoint SUMMARY criado antes da Task 5 completar:** o orchestrator's `<sequential_execution>` block diz "Write SUMMARY.md → commit → only then any narration", e o `<success_criteria>` do prompt pede "Pre-SUMMARY parcial criado para o orchestrator capturar o estado pré-checkpoint". Este SUMMARY documenta o estado pós-Task 4 / pré-Task 5, com placeholders para Tasks 5 e 6. Após o `approved` do usuário, o agente de continuação atualiza este mesmo arquivo (ou cria uma seção `## Post-Checkpoint Resolution`) com o registro da aprovação e o resultado final de STATE/REQUIREMENTS/ROADMAP/PHASE-SUMMARY.

## Self-Check: PASSED (parcial)

- `apresentacao/STYLE.md`: FOUND (modificado, +53 / -38 vs HEAD~2)
- `apresentacao/assets/theme-unifacens.css`: FOUND (modificado, -4 vs HEAD~1)
- `.planning/phases/01-reformata-o-da-base/01-07-SUMMARY.md`: FOUND (este arquivo, será incluído no commit final da Task 6)
- Commit `907a4b5` (STYLE.md, Tasks 1-3): FOUND em `git log --oneline -3`
- Commit `30ba911` (CSS cleanup, Task 4): FOUND em `git log --oneline -3`
- Automated gates Task 5: 13 / 13 PASSADOS
- Tasks 5 e 6: AGUARDANDO checkpoint humano e agente de continuação (documentado em Deviations item 3)

## Próximo Passo

Aguardar resposta do usuário ao checkpoint Task 5 (vide PLAN.md `<resume-signal>`):

- **Se `approved`:** agente de continuação executa Task 6 (STATE.md, REQUIREMENTS.md, ROADMAP.md updates + opcional PHASE-SUMMARY.md + commit final `docs: marcar fase 1 (reformatação da base) como concluída`). Depois: `/gsd-discuss-phase 2`.
- **Se lista de problemas:** abrir `/gsd-plan-phase 1 --gaps` com os items reportados; NÃO marcar a fase como completa.
