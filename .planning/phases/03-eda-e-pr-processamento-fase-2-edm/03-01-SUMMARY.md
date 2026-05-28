---
phase: 03-eda-e-pr-processamento-fase-2-edm
plan: 01
status: complete
requirements:
  - MARKER-02
key-files:
  modified:
    - apresentacao/index.html
  created: []
commits:
  - 0ed1382
---

## What Was Built

Section MARKER-02 ("Preparação dos Dados ✓") inserido em `apresentacao/index.html`
entre o `</section>` do MARKER-01 (linha 243 pré-task) e o comentário do slide-code
(linha 245 pré-task). 45 linhas adicionadas; zero CSS novo (D-67d).

O slide reusa integralmente o componente `.slide-marker` redesenhado em
commit `5d44606`, aplicando 4 deltas mecânicos vs MARKER-01 HEAD (conforme
03-RESEARCH §5.2):

| # | De (MARKER-01) | Para (MARKER-02) |
|---|---|---|
| 1 | `slide-marker--phase1` (linha 202) | `slide-marker--phase2` (linha 244 pós-task) |
| 2 | Pill 2 (Preparação): `--running` + `&#x21BB;` + `[running]` | `--done` + `&check;` + `[done]` |
| 3 | Pill 3 (Modelagem): `--pending` + `&#x25CB;` + `[]` | `--running` + `&#x21BB;` + `[running]` |
| 4 | Comentário "fase 1 concluida" | "fase 2 concluida" |

Pill 1 (Definição) e Pill 4 (Implantação) ficaram idênticas. Marca d'água Facens
e rodapé `Fonte: adaptado de Zorić (2020).` inalterados.

## Posição no deck

- **Atual** (com este plan único executado): MARKER-02 em #/11, vindo logo após
  MARKER-01 (#/10).
- **Final** (após plans 03-02/03/04 inserirem EDA-01/EDA-02/EDA-03 no gap):
  MARKER-02 em #/14, fechando o bloco `MARKER-01 → EDA-01 → EDA-02 → EDA-03 → MARKER-02`
  conforme ordem narrativa D-60/D-62.

## Acceptance Criteria — todos passaram

| # | Critério | Esperado | Observado |
|---|---|---|---|
| 1 | `grep -c 'slide-marker--phase2'` | 1 | 1 |
| 2 | `grep -c 'slide-marker--phase1'` (MARKER-01 inalterado) | 1 | 1 |
| 3 | `grep -c 'marker-pill marker-pill--done'` | 3 | 3 |
| 4 | `grep -c 'marker-pill marker-pill--running'` | 2 | 2 |
| 5 | `grep -c 'marker-pill marker-pill--pending'` | 3 | 3 |
| 6 | `grep -c 'Fonte: adaptado de Zorić (2020)'` | 2 | 2 |
| 7 | `grep -c 'fase 2 concluida'` | 1 | 1 |
| 8 | `git diff --stat apresentacao/assets/theme-unifacens.css` | vazio | vazio (D-67d) |
| 9 | `grep -c '<section'` | +1 vs HEAD pré-task (16 → 17) | 17 |

## Checkpoint visual — APPROVED

Testado em http://127.0.0.1:8000/#/11 pelo reviewer humano. Pills 1+2 done,
pill 3 running com spin, pill 4 pending. MARKER-01 (#/10) confirmado inalterado.
Console sem erros.

## Deviations

Nenhuma. Implementação literal vs 03-RESEARCH §5.3.

## Observação metodológica

A ordem de implementação dos 4 plans da fase 3 foi reordenada após este plan:
o RESEARCH §1 sugeria `MARKER-02 → EDA-02 → EDA-01 → EDA-03` (do mais
determinístico ao mais arriscado), mas após este plan, o reviewer indicou
que a ordem narrativa é mais apropriada para sessões de slide do TCC.
Próxima sequência: `EDA-02 (Plan 03-02) → EDA-01 (Plan 03-03) → EDA-03 (Plan 03-04)`,
respeitando o DAG declarado `depends_on` (que coincide com a ordem narrativa
para os 3 slides EDA).

## Self-Check: PASSED
