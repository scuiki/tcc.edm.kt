---
phase: 01-reformata-o-da-base
plan: 02
subsystem: apresentacao
tags: [merge, zoric, parafrase, voz-propria, deck-topic, mvp]
requires:
  - "01-01 (working tree clean, 14 sections, sem Corbett)"
provides:
  - "slide Zorić fundido único com cabeçalho `> mineração de dados educacionais`"
  - "primeiro slide da fase 1 a aplicar o novo padrão `.deck-topic` substituindo `.rel-kicker` + `.rel-title` + `.rel-sub`"
  - "primeiro slide a aplicar a política D-25/D-26 (paráfrase indireta + autor parentético no lugar de citação direta literal)"
affects:
  - apresentacao/index.html
tech_stack_added: []
patterns_added:
  - "paráfrase D-26 com voz própria + autor parentético (Zorić, 2020) em `<p class=\"rel-lead\">` substituindo `<blockquote class=\"rel-quote\">`"
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-02-SUMMARY.md
key_files_modified:
  - apresentacao/index.html
decisions:
  - "D-01 aplicado: `.deck-topic` único substitui `.rel-kicker` + `.rel-title` + `.rel-sub`; subtítulo 'Mineração de Dados Educacionais (EDM)' descartado conforme D-03."
  - "D-02 aplicado: autor 'Zorić' não aparece no corpo, kicker ou h2; só no rodapé `Fonte: Zorić (2020).` e como autor parentético na paráfrase."
  - "D-11 aplicado: cabeçalho travado `> mineração de dados educacionais` (1 ocorrência verificada)."
  - "D-23 aplicado: rodapé `Fonte: Zorić (2020).` preservado intacto."
  - "D-25 e D-26 aplicados: 2 citações diretas (Zorić, 2020, p. 12, tradução nossa) substituídas por 1 paráfrase única em voz própria com autor parentético; sem `<blockquote class=\"rel-quote\">`; sem 'tradução nossa' no novo slide."
  - "Classe CSS `slide-methods` removida do `<div>` do slide fundido conforme plan (slide deixa de ser apresentado como 'métodos'); regras CSS de `.slide-methods` ficam inertes no tema mas não são deletadas nesta fase."
  - "Conteúdo descartado: `.rel-intro` + 3 bullets `.rel-points` da section #9 antiga, `.rel-src` 'Com base em Zorić (2020, p. 12-14).' e 2 `.meth-text` da section #10 antiga; toda essa carga foi resumida na paráfrase única (tarefas como classificação, agrupamento, predição e associação)."
  - "Bridge para 'processo de quatro fases' (linha `.bridge-text` da section #10 antiga) descartada porque o slide-phases (Zorić p3) vem imediatamente em seguida e já carrega o gancho."
  - "Task 1 (leitura de docs/edm_review.pdf) cumprida: PDF é Kalita et al. (2025), 'Educational data mining: a 10-year review' (o symlink `docs/edm_review.pdf` aponta para esse arquivo). Confirmei que a paráfrase D-26 é fiel ao argumento do paper: introdução afirma que EDM é 'interdisciplinary field' que 'employs data mining tools and techniques, statistics, and machine learning algorithms' e que o processo é iterativo com 4 fases (Problem definition / Data preparation / Modelling / Deployment). A citação `(Zorić, 2020)` mantida no slide é convenção pré-existente do projeto (rodapé original), não introduzida nesta fase; preservada conforme D-23/D-26."
requirements_completed:
  - MERGE-01
metrics:
  duration_seconds: 480
  duration_human: "~8 min (leitura PDF + edição + verificação)"
  completed_at: "2026-05-27T18:57:48Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 1
  files_created: 1
---

# Phase 1 Plan 02: MERGE-01 Zorić p1+p2 fundido — Summary

MERGE-01 concluído: os 2 slides `slide-related` Zorić (#9 conceito de EDM + #10 ferramentas/metodologias) foram fundidos em um único `<section>` com cabeçalho `> mineração de dados educacionais`, e as 2 citações diretas atuais (Zorić, 2020, p. 12, tradução nossa) foram substituídas por 1 paráfrase única em voz própria com autor parentético, conforme D-25/D-26. Rodapé `Fonte: Zorić (2020).` preservado intacto. Section count em `apresentacao/index.html` cai de 14 (após plan 01-01) para 13.

## What Was Built

- **Task 1 (leitura da referência):** `docs/edm_review.pdf` (Kalita et al., 2025, "Educational data mining: a 10-year review", páginas 1-5 da introdução) lido para validar que a paráfrase D-26 reflete fielmente o argumento da fonte sobre EDM como área interdisciplinar (mineração de dados + estatística + ML) com tarefas de classificação, agrupamento, predição e associação. Conclusão: paráfrase fiel, sem necessidade de ajuste. A citação `(Zorić, 2020)` no slide é convenção pré-existente do projeto (rodapé herdado); a referência primária lida foi Kalita et al. (2025), que apoia o mesmo argumento.
- **Task 2 (MERGE-01 + paráfrase D-26):** seções #9 e #10 (linhas 283-323 do `apresentacao/index.html` pré-merge) substituídas por 1 `<section>` único com:
  - Comentário `<!-- ============ SLIDE · Mineração de Dados Educacionais (Zorić, 2020) — fusão p1+p2 ============ -->`
  - `<div class="deck-slide slide-related">` (sem `slide-methods`)
  - `<svg class="wm">` (marca d'água Facens) preservado
  - `<p class="deck-topic"><span class="ps1">&gt;</span>mineração de dados educacionais<span class="caret blink"></span></p>` (único cabeçalho)
  - `<p class="rel-lead">Nosso trabalho aplica o processo de <b>Mineração de Dados Educacionais</b>, área interdisciplinar que combina mineração de dados, estatística e aprendizado de máquina para apoiar decisões pedagógicas (Zorić, 2020). Tarefas típicas incluem classificação, agrupamento, <b>predição</b> e associação.</p>` (texto literal D-26, "Mineração de Dados Educacionais" e "predição" em negrito conforme plan)
  - `<p class="rel-cite">Fonte: Zorić (2020).</p>` (D-23 preservado)
- O slide fundido vive a partir da linha 283 do `apresentacao/index.html` (comentário) / linha 285 (`<section>`) / linha 288 (`.deck-topic`).

## Commits

| Hash | Mensagem | Files |
|---|---|---|
| `f9907b8` | `apresentacao: fundir slides Zorić p1+p2 com paráfrase (MERGE-01, D-26)` | apresentacao/index.html (3 inserções, 32 deleções) |

## Verification

### Automated (todas passaram)

| Check | Esperado | Obtido |
|---|---|---|
| `grep -F -c '&gt;</span>mineração de dados educacionais' apresentacao/index.html` (cabeçalho D-11) | 1 | 1 |
| `grep -F -c 'Nosso trabalho aplica o processo de' apresentacao/index.html` (paráfrase D-26) | 1 | 1 |
| `grep -F -c 'A Mineração de Dados Educacionais (EDM) é uma área de pesquisa interdisciplinar' apresentacao/index.html` (citação direta Zorić p1 removida) | 0 | 0 |
| `grep -F -c 'Utiliza diferentes métodos e técnicas de aprendizado de máquina' apresentacao/index.html` (citação direta Zorić p2 removida) | 0 | 0 |
| `grep -F -c 'slide-methods' apresentacao/index.html` (classe deixou de ser usada) | 0 | 0 |
| `grep -c '<section data-background' apresentacao/index.html` (section count) | 13 | 13 |
| `grep -F -c 'Fonte: Zorić (2020).' apresentacao/index.html` (D-23 preservado; aparece também no slide-phases) | >=1 | 2 |
| `grep -F -c 'tradução nossa' apresentacao/index.html` (diminuiu em ≥2; só Yağcı p1+p2 sobram) | 2 | 2 |
| em-dash na prosa `<p class="rel-lead">` do slide fundido | 0 | 0 |
| Balance `<section` vs `</section>` | 13 / 13 | 13 / 13 |
| Commit `apresentacao: fundir slides Zorić p1+p2 com paráfrase (MERGE-01, D-26)` em `git log` | sim | sim (`f9907b8`) |

### Manual (a validar em sessão futura, fora deste plano)

- Browser smoke test: `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000, navegar até o slide Zorić fundido, validar:
  - Cabeçalho em Cascadia `#5b6472` com `>` em azul e caret piscando
  - "Mineração de Dados Educacionais" em negrito Arial no parágrafo `.rel-lead`
  - "predição" em negrito Arial no mesmo parágrafo
  - Rodapé `Fonte: Zorić (2020).` presente no canto inferior
  - DevTools console sem erro
  - **Status: a verificar em browser** (mesma situação do plan 01-01; não bloqueia este plano).

## Decisions Made

- **Comentário HTML do slide fundido (`<!-- ============ SLIDE · Mineração de Dados Educacionais (Zorić, 2020) — fusão p1+p2 ============ -->`):** mantém em-dash dentro do comentário HTML, o que NÃO viola a regra "sem em-dash em prosa" (a regra aplica a texto exibido, não a comentários do markup). A prosa do `.rel-lead` está limpa.
- **Identidade da referência `docs/edm_review.pdf`:** o symlink aponta para "Educational Data Mining: a 10 year review" de Kalita et al. (2025), e não a Zorić (2020) como CONTEXT.md L109 assume. A citação `(Zorić, 2020)` no slide é convenção pré-existente do projeto (presente nos rodapés desde antes da fase 1); a paráfrase é fiel ao argumento da fonte primária lida (Kalita et al. 2025), que apoia tese idêntica sobre EDM. **Implicação para próximas fases:** vale registrar como deferred (ver "Deferred Issues" abaixo) para conferir se a citação `Zorić, 2020` deveria ser substituída por `Kalita et al., 2025` ou se há um PDF Zorić 2020 separado em outro caminho; decisão fora do escopo deste plan.
- **Mensagem do commit Task 2:** `apresentacao: fundir slides Zorić p1+p2 com paráfrase (MERGE-01, D-26)` segue convenção do projeto (`.planning/codebase/CONVENTIONS.md` L261-285): minúsculo, prefixo de área (`apresentacao:`), sem `feat:`/`fix:`. Referência ao requirement (`MERGE-01`) e decisão (`D-26`) ao fim do subject reforça rastreabilidade.

## Deferred Issues

- **Verificar identidade da citação Zorić (2020):** o symlink `docs/edm_review.pdf` aponta para Kalita et al. (2025), não Zorić (2020). Se `Zorić (2020)` for citação herdada de algum outro paper / PDF não disponível em `docs/`, vale: (a) localizar o PDF Zorić 2020 verdadeiro e adicioná-lo a `docs/`, OU (b) substituir a citação por `Kalita et al. (2025)` em todos os slides afetados (este, slide-phases #11 que vem em seguida, e qualquer outro). Deferred para uma próxima fase porque: (1) o slide-phases ainda não foi reformatado (plan 01-05); (2) a paráfrase deste plan é fiel ao argumento da fonte que foi lida; (3) corrigir a citação isoladamente neste slide criaria inconsistência com o slide-phases que ainda cita "Zorić (2020)". Sugestão: tratar no plan 01-05 (REFORMAT-02 slide-phases) ou em commit de revisão de citações.

## Working Tree Final State

```
$ git status apresentacao/
nothing to commit, working tree clean
```

`apresentacao/index.html`: 13 sections (era 14 após plan 01-01, menos 1 do merge). Slide fundido na linha 285-294. Próxima section depois do slide fundido é o `slide-phases` Zorić p3 (linha 296, comentário `SLIDE 5 · As 4 fases do EDM`).

## Deviations from Plan

Nenhuma deviation que altere o entregável. Uma observação contextual foi adicionada como Deferred Issue:
- **[Deferred]** Identidade do PDF `docs/edm_review.pdf` (Kalita et al. 2025) versus a citação `Zorić (2020)` no slide. Não foi tratado neste plan porque está fora do escopo (acceptance criteria do plan exigem preservar `Fonte: Zorić (2020).` literal — D-23). Documento em "Deferred Issues" para tratativa em plan futuro.

## Self-Check: PASSED

- `apresentacao/index.html`: FOUND
- `.planning/phases/01-reformata-o-da-base/01-02-SUMMARY.md`: FOUND
- Commit `f9907b8` (Task 2): FOUND em `git log --oneline -3`
- Todas as 11 verificações automatizadas: passaram
- Section count caiu de 14 para 13 (esperado: -1)
- Paráfrase D-26 literal aplicada (1 ocorrência)
- 0 citações diretas Zorić restantes
- `slide-methods` removido (0 ocorrências)

## Próximo Plan

**01-03 (REFORMAT-03 Yağcí fundido):** funde slides #12 (Yağcí p1, slide-related) e #13 (Yağcí p2, slide-related slide-bridge) em um único section com cabeçalho `> da edm ao knowledge tracing`, substituindo a citação direta atual (Yağcı, 2022, p. 2, tradução nossa) por paráfrase indireta em voz própria com autor parentético (D-27), e preservando a sequência horizontal `.bridge-seq` (3 passos) intacta.
