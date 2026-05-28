---
phase: 03-eda-e-pr-processamento-fase-2-edm
plan: 02
status: complete
requirements:
  - EDA-02
key-files:
  modified:
    - apresentacao/index.html
  created: []
commits:
  - 2944567
---

## What Was Built

Section EDA-02 ("aproximação ao protocolo") inserido em `apresentacao/index.html`
entre o INTRO-01 movido (#/11) e o MARKER-02 (#/14), na posição final #/13. Reusa
o template `.slide-related` sem CSS novo.

Estrutura:
- Cabeçalho `> aproximação ao protocolo` (variante (b) do 03-RESEARCH §7.2, recomendada)
- 3 parágrafos `.rel-lead` em voz primeira pessoa do plural, paráfrase indireta de
  Shi et al. (2022) §4.1/§4.2:
  1. Justificativa baseline: "Nosso pré-processamento segue o protocolo de Shi
     *et al.* (2022) como *baseline* de comparação, com ênfase em análise."
  2. Ponte 413 → 410 → 328/82: "Dos **413** alunos brutos do CSEDM, mantivemos
     **410** com pelo menos 3 tentativas de execução, mesma seleção do paper.
     Em seguida, dividimos em **328 estudantes para treino e 82 para teste**,
     na proporção 80/20 com semente fixa."
  3. Truncagem 50 últimas: "Limitamos cada sequência às **50 últimas tentativas**.
     A mediana é 32 tentativas por aluno e *assignment*; 28% dos pares ultrapassam
     50, com cauda longa até 272."
- Rodapé: `Fonte: adaptado de Shi <i>et al.</i> (2022).`

## Cabeçalho final escolhido

Variante (b) `> aproximação ao protocolo` — recomendada pelo 03-RESEARCH §7.2 por
comunicar "seguimos Shi por design" e dialogar com a 1ª frase do corpo. Variantes
(a) `> pré-processamento` e (c) `> do bruto ao split` ficaram disponíveis como
fallback, mas não foram solicitadas no checkpoint.

## Acceptance Criteria — todos passaram

| # | Critério | Esperado | Observado |
|---|---|---|---|
| 1 | `grep -c 'SLIDE · EDA-02'` | 1 | 1 |
| 2 | Cabeçalho visível único | 1 | 1 (deck-topic único; comentário HTML conta extra mas é invisível) |
| 3 | `'413 alunos brutos do CSEDM'` | 1 | 1 |
| 4 | `'<b>410</b>'` | 1 | 1 |
| 5 | `'328 estudantes para treino e 82 para teste'` | 1 | 1 |
| 6 | `'50 últimas tentativas'` | 1 | 1 |
| 7 | `'28% dos pares'` | 1 | 1 |
| 8 | `'Fonte: adaptado de Shi <i>et al.</i> (2022)'` | 2 (INTRO-03b + EDA-02) | 2 |
| 9 | `'<i>baseline</i>'` | ≥1 | 1 |
| 10 | Code-DKT dentro do EDA-02 | 0 | 0 |
| 11 | Release/Train / Compile.Error / Score==1.0 dentro do EDA-02 | 0 | 0 |
| 12 | em-dash dentro do EDA-02 | 0 | 0 |
| 13 | `<blockquote>` ou `<h2>` dentro do EDA-02 | 0 | 0 |
| 14 | `git diff --stat theme-unifacens.css` | vazio (template existente) | vazio |

## Checkpoint visual — APPROVED (tacitamente)

O reviewer humano viu o slide no browser e questionou apenas a ordem de
implementação (não a microcópia). Após a reordenação para inserir o EDA-01
antes do EDA-02, o reviewer revisou novamente a sequência contígua
MARKER-01 → INTRO-01 (movido) → EDA-01 → EDA-02 → MARKER-02 e aprovou.

## Deviations

Nenhuma na microcópia. Ordem de implementação dos slides foi reordenada
após este plan para respeitar a sequência narrativa (ver SUMMARY do 03-03).

## Self-Check: PASSED
