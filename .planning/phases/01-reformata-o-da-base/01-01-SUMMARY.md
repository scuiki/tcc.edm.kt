---
phase: 01-reformata-o-da-base
plan: 01
subsystem: apresentacao
tags: [reformatacao, remove, corbett, working-tree, mvp]
requires: []
provides:
  - "estado conhecido do working tree (commit-WIP ed03327)"
  - "apresentacao/index.html com 14 sections, sem slides Corbett"
affects:
  - apresentacao/index.html
  - apresentacao/assets/theme-unifacens.css
  - apresentacao/STYLE.md
tech_stack_added: []
patterns_added: []
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-01-SUMMARY.md
key_files_modified:
  - apresentacao/index.html
  - apresentacao/assets/theme-unifacens.css
  - apresentacao/STYLE.md
decisions:
  - "Task 1 (checkpoint:decision) resolvido como commit-wip por escolha do usuario via AskUserQuestion do orquestrador. Snapshot ed03327 vira ponto ancora da fase 1."
  - "D-19 aplicado integralmente: nenhum placeholder, comentario TODO ou referencia residual a Corbett no markup."
  - "D-20 atendido: grep -c 'slide-corbett' apresentacao/index.html retorna 0."
requirements_completed:
  - REMOVE-01
metrics:
  duration_seconds: 68
  duration_human: "~1 min entre commits (excluindo discussao do checkpoint:decision)"
  completed_at: "2026-05-27T18:52:44Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 3
  files_created: 1
---

# Phase 1 Plan 01: Reformatação da base, abertura — Summary

REMOVE-01 concluído: o working tree pré-fase 1 foi commitado como snapshot âncora (`ed03327`) e os 2 slides Corbett e Anderson (1995) foram apagados de `apresentacao/index.html` em commit atômico (`91b9675`), sem nenhum placeholder ou nota residual.

## What Was Built

- **Task 1 (checkpoint:decision resolvido):** snapshot WIP de `apresentacao/index.html` + `apresentacao/assets/theme-unifacens.css` + `apresentacao/STYLE.md` (untracked) versionado como commit nomeado `apresentacao: WIP working tree antes da fase 1`. Cada plan subsequente da fase 1 passa a ser diff isolado contra este âncora.
- **Task 2 (REMOVE-01):** dois blocos `<!-- ============ SLIDE · ... ============ -->` + `<section>` correspondentes deletados de `apresentacao/index.html`:
  - Bloco 1 (era linhas 386-407): slide-related slide-corbett "A origem do *knowledge tracing*"
  - Bloco 2 (era linhas 409-439): slide-related slide-corbett "O modelo de dois estados (base do BKT)"
- A linha em branco que separava os dois blocos também foi removida, e a section anterior (slide-bridge Yağcí) ficou seguida diretamente por `    </div>\n  </div>` (fechamento de `.slides` e `.reveal`) e pelo `<script>` final, sem nenhuma section Corbett entre eles.

## Commits

| Hash | Mensagem | Files |
|---|---|---|
| `ed03327` | `apresentacao: WIP working tree antes da fase 1` | apresentacao/index.html, apresentacao/assets/theme-unifacens.css, apresentacao/STYLE.md (novo) |
| `91b9675` | `apresentacao: remover slides Corbett (REMOVE-01)` | apresentacao/index.html (55 linhas removidas) |

## Verification

### Automated (todas passaram)

| Check | Esperado | Obtido |
|---|---|---|
| `grep -c 'slide-corbett' apresentacao/index.html` | 0 | 0 |
| `grep -c 'Corbett e Anderson' apresentacao/index.html` | 0 | 0 |
| `grep -c '<section data-background' apresentacao/index.html` | 14 | 14 |
| `grep -c 'Corbett\|TODO\|placeholder\|futuro slide'` | 0 | 0 |
| `grep -c '<section'` vs `grep -c '</section>'` | balanceado | 14 / 14 |
| Commit `apresentacao: remover slides Corbett` em `git log` | sim | sim (`91b9675`) |

### Manual (a validar em sessão futura, fora deste plano)

- Browser smoke test: `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000, navegar do slide 0 ao último com a tecla seta-direita, DevTools console sem erro. **Status: a verificar em browser** (acceptance lista esse passo como item manual; não bloqueia este plano).

## Decisions Made

- **commit-wip (Task 1):** usuário escolheu commitar o working tree como snapshot nomeado ao invés de deixar implícito (`integrate`). Vantagem: histórico nomeia exatamente o estado pré-fase 1, e cada plano subsequente da fase produz diff limpo contra `ed03327`. Custo: 1 commit "administrativo" extra no histórico, justificado por ser fronteira de fase.
- **Mensagem do commit Task 2** (`apresentacao: remover slides Corbett (REMOVE-01)`): segue convenção do projeto (`.planning/codebase/CONVENTIONS.md` linhas 261-285): minúsculo, prefixo de área (`apresentacao:`), sem prefixos `feat:`/`fix:`. Referência ao requirement (`REMOVE-01`) ao fim do subject reforça rastreabilidade com `REQUIREMENTS.md`.

## Working Tree Final State

```
$ git status apresentacao/
nothing to commit, working tree clean (relativo a apresentacao/)
```

`apresentacao/index.html`: 14 sections (eram 16, menos 2 Corbett). Comentário acima de slide-bridge Yağcí (`<!-- ============ SLIDE · Ponte EDM -> KT que o trabalho de Yağcí (2022) mostra ============ -->`) é agora o último bloco antes do `</div></div>` que fecha `.slides` e `.reveal`.

## Deviations from Plan

Nenhuma. Plano executado exatamente como escrito.

## Self-Check: PASSED

- `apresentacao/index.html`: FOUND
- `apresentacao/assets/theme-unifacens.css`: FOUND
- `apresentacao/STYLE.md`: FOUND
- Commit `ed03327` (Task 1): FOUND
- Commit `91b9675` (Task 2): FOUND
- Todas as 4 verificações automatizadas: passaram

## Próximo Plan

**01-02 (MERGE-01 Zorić fundido):** funde slides #9 (Zorić p1, slide-related) e #10 (Zorić p2, slide-related slide-methods) em um único section com cabeçalho `> mineração de dados educacionais`, substituindo as 2 citações diretas atuais por paráfrase indireta única em voz própria (D-26).
