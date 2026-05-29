---
phase: 05-implanta-o-agenda-e-encerramento-fase-4-edm
plan: 04
status: complete-as-pivot
requirements: [TOOL-03]
commits:
  - 3801d58
  - 5b975cc
pivot_to_plan: 05-05
---

# Plan 05-04 — TOOL-03 (PIVOT: wireframe removido, conteúdo migra para fluxograma TOOL-01)

## Resultado

Plan 05-04 executado, **resultado pós-checkpoint foi pivot**: a section TOOL-03 (wireframe dashboard 3 painéis) foi inserida (commit `3801d58`) e em seguida **removida integralmente** (commit `5b975cc`) por rejeição do reviewer no checkpoint visual.

Razão do pivot: o usuário avaliou que mostrar um mockup do dashboard era prematuro e narrativamente fraco para a defesa. A alternativa proposta foi **trocar o slide inteiro por um fluxograma único da aplicação** (input → extração KCs → edição docente → Code-DKT → dashboard), o que conflita diretamente com o conteúdo planejado para o TOOL-01 (plan 05-05). A solução escolhida: **fundir os dois slots num único TOOL-01 fluxograma** e deixar TOOL-03 ausente.

Deck mantém **29 sections** ao final do plan (estado idêntico ao pós-05-03).

## Trajetória do plan

1. **Task 1 executada** (commit `3801d58`): section TOOL-03 inserida entre MARKER-03 e MARKER-04 com `.bridge-seq` adaptado (3 painéis paralelos `min-height 280px`, bordas pretas, cantos retos, fundo branco). Deck: 29 → 30 sections.
2. **Task 2 checkpoint visual**: reviewer abriu `http://127.0.0.1:8003/#/27`, **rejeitou** a abordagem. Citou duas razões:
   - "Não acho que precisamos mostrar como seria o dashboard" (mockup prematuro)
   - "Eu estava pensando em um fluxograma de aplicação" (proposta alternativa)
3. **Pivot decidido em conversa** (checkpoint pós-rejeição):
   - Fundir TOOL-01 + TOOL-03 num único slide fluxograma (deletar TOOL-03)
   - Aceitar override D-94h (ProgSnap2 nominal no fluxograma)
   - Aceitar override D-94e (detalhar mais cada etapa)
4. **Task 1 revertida** (commit `5b975cc`): section TOOL-03 deletada integralmente. Deck: 30 → 29 sections.

## Decisões emergentes registradas

**D-104b (pivot TOOL-03 → fluxograma único):** O slide TOOL-03 com wireframe de dashboard é eliminado da fase 5. O conteúdo conceitual de "dashboard final entregue ao professor" passa a ser a **última etapa do fluxograma** no TOOL-01 (plan 05-05). Razão: evitar duplicação narrativa entre "pipeline conceitual" (TOOL-01) e "mockup visual" (TOOL-03); o fluxograma único cobre input → output em um só slide.

**D-104c (Code-DKT prediz turma + individual):** Confirmado em consulta ao usuário: a saída nativa do Code-DKT é `P(correct | student, problem, history)` (individual por estudante × problema); vistas agregadas de turma (curvas de aprendizado por KC, AUC por assignment, distribuições) são derivadas por agregação trivial. O fluxograma do TOOL-01 pode legitimamente mostrar a etapa "Code-DKT prediz turma e individual".

**D-104d (override D-94h aceito):** O fluxograma TOOL-01 vai dizer "Import ProgSnap2" na etapa 1, **revertendo** o gate D-94h (que dizia "Submissões dos estudantes, não ProgSnap2") e a Key Decision do PROJECT.md linha 183 ("ProgSnap2 só em INTRO-01"). Razão do usuário: ProgSnap2 já foi apresentado em INTRO-01; recapitular reforça a continuidade técnica e ancora a aplicação num formato concreto.

**D-104e (override D-94e aceito):** O fluxograma terá mais detalhamento por etapa que MODEL-05 (que só dizia verbo + 1 linha curta). Cada etapa do TOOL-01 ganha contexto narrativo: ex. etapa 3 explicita "docente edita/adiciona/remove KCs", etapa 5 explicita "prediz turma e individual".

## Impacto cruzado nos demais artefatos

- **Plan 05-05 (TOOL-01)** redesenhado para acomodar o fluxograma proposto pelo usuário; o PLAN.md original do 05-05 fica como referência mas será **executado com adaptações** (etapas detalhadas, ProgSnap2 nominal, encerramento focado no professor + dashboard).
- **REQ TOOL-03** do REQUIREMENTS.md é atendido pela última etapa do fluxograma do TOOL-01 (não por um slide dedicado). Plan 05-06 (fechamento) precisa marcar TOOL-03 como Validated **através** do TOOL-01.
- **ROADMAP Phase 5 Success Criterion 2** ("Slide TOOL-03 mostra o dashboard...") fica parcialmente coberto: o dashboard aparece como ETAPA, não como slide próprio. Pode ser registrado como pivot aceito ou ajustado.
- **STYLE.md §Inventário** (a ser atualizado em 05-06) deve refletir 30 sections finais (não 31): cover + título + AGENDA + 23 slides existentes pós-fase 4 + TOOL-01 fluxograma + MARKER-04 + END-01.
- **Memory `feedback_no_em_dashes` e `feedback_estudantes_nao_alunos`** continuam vinculantes.

## Acceptance gates finais (estado pós-pivot)

| Gate | Esperado | Obtido | Status |
|---|---|---|---|
| `grep -c "<section " index.html` | 29 (pré-TOOL-03) | 29 | ✓ |
| `grep -c "Painéis principais do dashboard" index.html` | 0 (TOOL-03 removido) | 0 | ✓ |
| `grep -c "deck-slide slide-related slide-bridge" index.html` | 2 (Yağcı + MODEL-05, sem TOOL-03) | 2 | ✓ |
| Posição entre MARKER-03 e MARKER-04 vazia | sim (sem section intermediária) | sim | ✓ |
| Working tree limpo após revert | sim | sim | ✓ |

## Commits

- `3801d58` apresentacao: slide TOOL-03 - dashboard wireframe 3 paineis (estilo ABNT Word) [**revertido**]
- `5b975cc` apresentacao: remover slide TOOL-03 wireframe (pivot para fluxograma TOOL-01) [pivot final]
