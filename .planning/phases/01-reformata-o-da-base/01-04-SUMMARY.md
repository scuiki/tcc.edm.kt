---
phase: 01-reformata-o-da-base
plan: 04
subsystem: apresentacao
tags: [reformat, martins, deck-topic, introducao, mvp]
requires:
  - "01-03 (working tree clean, 12 sections, slide Yağcí fundido com cabeçalho `> da edm ao knowledge tracing`)"
provides:
  - "slide Martins p1 reformatado com cabeçalho único `> introdução` substituindo `.rel-kicker` + `.rel-title`"
  - "terceiro slide da fase 1 a aplicar o novo padrão `.deck-topic` (após plan 01-02 e 01-03)"
  - "remoção do último `.rel-kicker` do `apresentacao/index.html` (todos os 3 slides correlato puros já reformatados ou fundidos)"
  - "remoção da linha de comentário obsoleta `<!-- regra do deck: todo autor novo é introduzido como trabalho correlato antes de ser usado -->` (regra revogada por D-01/D-02)"
affects:
  - apresentacao/index.html
tech_stack_added: []
patterns_added: []
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-04-SUMMARY.md
key_files_modified:
  - apresentacao/index.html
decisions:
  - "D-01 aplicado: par `.rel-kicker.kicker` + `<h2 class=\"rel-title\">` substituído por uma única linha `<p class=\"deck-topic\">` com `> introdução` + caret blink."
  - "D-02 aplicado: nome 'Martins, Marin e Alves (2024)' removido do `<h2>` do slide. Sobrevive apenas em (a) rodapé `Fonte: Martins, Marin e Alves (2024).` (D-23) e (b) prosa do `.rel-lead` parágrafo 2 como autor parentético (`Martins <i>et al</i>. (2024) trazem uma revisão sistemática...`), que é parte da paráfrase já existente, não do cabeçalho."
  - "D-03 aplicado: `<h2 class=\"rel-title\">` deletado por inteiro; classe CSS `.slide-related` preservada para o layout."
  - "D-04 aplicado: cabeçalho travado `> introdução` (minúsculo, sem caracteres especiais, conforme STYLE.md 'Tipografia' Cascadia `#5b6472`). 1 ocorrência confirmada."
  - "D-23 aplicado: rodapé `<p class=\"rel-cite\">Fonte: Martins, Marin e Alves (2024).</p>` preservado intacto, sobrenome e ano corretos."
  - "D-29 aplicado: os 3 `<p class=\"rel-lead\">` (programação beneficia / revisão sistemática / estratégias de ensino) preservados literal, sem reescrita textual. O slide já estava em paráfrase no HEAD; apenas o cabeçalho mudou."
  - "Task 1 (leitura de docs/Artigo+2+Desafios+na+aprendizagem+de+lógica+de+programação.pdf, p. 12-14) cumprida: confirmei que os 3 `.rel-lead` atuais refletem fielmente Resumo + Introdução do artigo: (a) p.12 'Programar é uma atividade que beneficia qualquer indivíduo ao estimular o pensamento lógico' → parágrafo 1; (b) p.13 'O objetivo deste trabalho é identificar as dificuldades enfrentadas pelos alunos... revisão bibliográfica de artigos científicos publicados entre 2008 e 2023' → parágrafo 2; (c) p.12 'Este trabalho pode auxiliar na elaboração de estratégias e métodos de ensino que melhoram o processo de ensino e aprendizagem de programação, ao promover melhores resultados acadêmicos e reduzindo a taxa de desistência e reprovação' → parágrafo 3 (quase verbatim). Nenhuma divergência fatual."
  - "Comentário HTML do slide atualizado: linha `<!-- regra do deck: todo autor novo é introduzido como trabalho correlato antes de ser usado -->` REMOVIDA (a regra foi revogada por D-01/D-02, política nova é 'autor introduzido no momento da relevância via cabeçalho temático'); comentário principal trocado de `<!-- ============ SLIDE · Trabalho correlato: Martins, Marin e Alves (2024) ============ -->` para `<!-- ============ SLIDE · Introdução · Martins, Marin e Alves (2024) — recorte do problema ============ -->` (per PATTERNS.md § 'Template comment')."
  - "Em-dash no comentário HTML mantido (mesma convenção do plan 01-03): a regra 'sem em-dash em prosa' aplica a texto renderizado, não a comentários do markup invisíveis ao público. A prosa do `.rel-lead` segue limpa de em-dash."
  - "Mensagem do commit `apresentacao: reformatar Martins p1 com > introdução (REFORMAT-01, D-04)` segue convenção .planning/codebase/CONVENTIONS.md L261-285 (minúsculo, prefixo de área `apresentacao:`, sem `feat:`/`fix:`); referência ao requirement (REFORMAT-01) e decisão (D-04) ao fim do subject reforça rastreabilidade."
requirements_completed:
  - REFORMAT-01
metrics:
  duration_seconds: 90
  duration_human: "~1.5 min (leitura de 3 páginas do PDF Martins + edição de 1 bloco HTML + verificação + commit)"
  completed_at: "2026-05-27T19:30:00Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 1
  files_created: 1
---

# Phase 1 Plan 04: REFORMAT-01 Martins p1 — Summary

REFORMAT-01 concluído: o slide Martins p1 (`slide-related`, 1º slide de conteúdo após a Agenda) teve o par `.rel-kicker.kicker` ("> trabalhos correlatos") + `<h2 class="rel-title">Martins, Marin e Alves (2024)</h2>` substituído por uma única linha `<p class="deck-topic"><span class="ps1">&gt;</span>introdução<span class="caret blink"></span></p>`. O nome do autor desapareceu do cabeçalho do slide; sobrevive apenas no rodapé `Fonte: Martins, Marin e Alves (2024).` (D-23) e como autor parentético dentro do `.rel-lead` parágrafo 2 (que é parte da paráfrase existente, não do cabeçalho). Os 3 parágrafos `.rel-lead` foram preservados intactos (D-29). Section count em `apresentacao/index.html` permanece em 12 (sem fusão nem remoção nesta REQ). Com esta REQ encerrada, o `.rel-kicker` deixa de existir no arquivo (último uso eliminado): todos os 3 slides `slide-related` puros (Martins p1, Zorić p1, Yağcí p1+p2) já foram reformatados ou fundidos.

## What Was Built

- **Task 1 (leitura da referência Martins, Marin e Alves 2024):** `docs/Artigo+2+Desafios+na+aprendizagem+de+lógica+de+programação.pdf` páginas 1-3 (revista p. 12-14) lidas (Resumo, Abstract, Introdução, Referencial Teórico e início da Metodologia). Confirmações de fidelidade dos 3 `.rel-lead` atuais à fonte primária:
  - **Parágrafo 1 do slide** ("Programar beneficia qualquer pessoa. Porém, o ensino de programação tem se mostrado complexo, com altos índices de reprovação e desistência nas disciplinas introdutórias de cursos de tecnologia.") — corresponde ao Resumo (p. 12): "Programar é uma atividade que beneficia qualquer indivíduo ao estimular o pensamento lógico e a resolução de problemas... A aprendizagem de programação nesses cursos tem se mostrado complexa, o que resulta em dificuldades significativas para os alunos na compreensão de lógica de programação, leva a altos índices de reprovação e desistência em disciplinas introdutórias." E à Introdução (p. 13): "essa disciplina é um obstáculo significativo para os alunos, resultando em altos índices de reprovação e desistência devido à complexidade do conteúdo."
  - **Parágrafo 2 do slide** ("Martins et al. (2024) trazem uma revisão sistemática da literatura, cujo objetivo é identificar os principais desafios enfrentados por alunos durante a aprendizagem de programação de computadores.") — corresponde ao Resumo (p. 12): "Este trabalho visa identificar os principais desafios enfrentados por alunos durante a aprendizagem de programação de computadores... Para isso, foi realizada uma revisão sistemática abrangente em bases de dados como Google Acadêmico, IEEE, Periódicos da Capes, ScienceDirect e Scielo." E à Introdução (p. 13): "O objetivo deste trabalho é identificar as dificuldades enfrentadas pelos alunos nos cursos de tecnologia ao aprenderem programação. Este estudo pode contribuir para o desenvolvimento de metodologias de ensino mais eficazes... A pesquisa foi realizada por meio de uma revisão bibliográfica de artigos científicos publicados entre 2008 e 2023."
  - **Parágrafo 3 do slide** ("Este trabalho pode auxiliar na elaboração de estratégias e métodos de ensino que melhoram o processo de ensino e aprendizagem de programação, ao promover melhores resultados acadêmicos e reduzindo a taxa de desistência e reprovação") — corresponde quase verbatim ao Resumo (p. 12): "Este trabalho pode auxiliar na elaboração de estratégias e métodos de ensino que melhoram o processo de ensino e aprendizagem de programação, ao promover melhores resultados acadêmicos e reduzindo a taxa de desistência e reprovação."
  - **Conclusão da Task 1:** nenhum ajuste textual necessário no corpo do slide. Nenhuma divergência fatual com a fonte primária. Pronto para Task 2.

- **Task 2 (REFORMAT-01):** bloco entre linhas 82-100 do `apresentacao/index.html` (estado pré-edição) editado por substituição direta. Estado pós-edição (linhas 82-98 atuais):
  - Comentário principal: `<!-- ============ SLIDE · Introdução · Martins, Marin e Alves (2024) — recorte do problema ============ -->` (linha 82).
  - Comentário obsoleto removido: `<!-- regra do deck: todo autor novo é introduzido como trabalho correlato antes de ser usado -->` deletado (a regra foi revogada por D-01/D-02; ver D-21 do CONTEXT, plan 07).
  - `<section data-background-color="#F1F6FB">` (linha 83) — preservada.
  - `<div class="deck-slide slide-related">` (linha 84) — classe `slide-related` preservada para o layout (D-03).
  - `<svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>` (linha 85) — preservada.
  - `<p class="deck-topic"><span class="ps1">&gt;</span>introdução<span class="caret blink"></span></p>` (linha 87) — **NOVO**, substitui o par `.rel-kicker.kicker` + `<h2 class="rel-title">`. Caret blink como último filho do `<p>`. Texto exato `introdução` (minúsculo, sem caracteres especiais, conforme STYLE.md "Tipografia"). 1 ocorrência confirmada.
  - 3 `<p class="rel-lead">` (linhas 89, 91, 93-94) — preservados intactos (D-29).
  - `<p class="rel-cite">Fonte: Martins, Marin e Alves (2024).</p>` (linha 96) — preservado intacto (D-23).
  - `</div></section>` (linhas 97-98) — preservadas.
- O `.deck-topic` novo aparece na **linha 87** do `apresentacao/index.html`.

## Commits

| Hash | Mensagem | Files | Diff |
|---|---|---|---|
| `c31658c` | `apresentacao: reformatar Martins p1 com > introdução (REFORMAT-01, D-04)` | apresentacao/index.html | +2 / -4 |

## Verification

### Automated (todas passaram)

| Check | Esperado | Obtido |
|---|---|---|
| `grep -c 'introdução<span class="caret blink"' apresentacao/index.html` (cabeçalho D-04 presente) | 1 | 1 |
| `grep -c 'rel-title">Martins, Marin e Alves' apresentacao/index.html` (h2 antigo removido) | 0 | 0 |
| `grep -c 'rel-kicker' apresentacao/index.html` (último `.rel-kicker` eliminado) | 0 | 0 |
| `grep -c 'Fonte: Martins, Marin e Alves (2024)' apresentacao/index.html` (rodapé D-23 preservado) | ≥1 | 1 |
| `grep -c '<p class="rel-lead">' apresentacao/index.html` (rel-lead total no arquivo) | ≥3 | 5 |
| `grep -c '<section data-background' apresentacao/index.html` (section count inalterado) | 12 | 12 |
| Commit `apresentacao: reformatar Martins p1 com > introdução` em `git log --oneline -1` | sim | sim (`c31658c`) |

**Sobre o gate 5 (`rel-lead` total = 5):** este é o total no arquivo inteiro, não só no slide Martins p1. Decomposição: 3 `.rel-lead` no slide Martins p1 + 1 `.rel-lead` no slide Zorić fundido (plan 01-02) + 1 `.rel-lead` no slide Yağcí fundido (plan 01-03) = 5. O critério do plan ("mantém pelo menos 3 ocorrências dentro do slide Martins p1") foi confirmado por inspeção visual das linhas 89, 91, 93-94 (3 `<p class="rel-lead">` consecutivos no slide).

### Manual (a validar em sessão futura, fora deste plano)

- Browser smoke test: `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000, navegar até o slide Martins p1 (#3), validar:
  - Cabeçalho `> introdução` em Cascadia `#5b6472` com `>` em azul e caret piscando
  - 3 parágrafos `.rel-lead` em Arial intactos (programação beneficia / revisão sistemática / estratégias de ensino)
  - Rodapé `Fonte: Martins, Marin e Alves (2024).` presente no canto inferior
  - Marca d'água Facens (`<svg class="wm">`) no canto superior direito
  - DevTools console sem erro
  - Navegação ponta a ponta do deck (0..11) sem quebra
  - **Status: a verificar em browser** (mesma situação dos plans 01-01/02/03; não bloqueia este plano).

## Decisions Made

- **Comentário HTML obsoleto removido:** a linha `<!-- regra do deck: todo autor novo é introduzido como trabalho correlato antes de ser usado -->` foi deletada porque essa regra é revogada pela política nova (D-01/D-02): autor agora é introduzido no momento da relevância via cabeçalho temático `> [seção]`, nunca em slide dedicado. Mantê-lo geraria confusão de leitura para quem encontrar o markup no futuro. Decisão alinhada com PATTERNS.md § "Template comment" (em REFORMAT-01: "atualizar a descrição do comentário se ela ficar enganadora").
- **Comentário principal com em-dash mantido:** o comentário novo `<!-- ============ SLIDE · Introdução · Martins, Marin e Alves (2024) — recorte do problema ============ -->` carrega um em-dash (`—`). Mantido seguindo a mesma convenção aplicada pelo plan 01-03: a regra "sem em-dash em prosa" do CLAUDE.md/STYLE.md aplica ao texto renderizado ao público (prosa de slide), não a comentários do markup invisíveis. Alternativas com dois-pontos ou parênteses ("Introdução · Martins, Marin e Alves (2024): recorte do problema") foram consideradas e descartadas para preservar consistência com os comentários dos plans 01-02 e 01-03, que também usaram em-dash em separadores de descrição de slide.
- **`<h2>` deletado por inteiro, sem substituição:** D-03 dita que `<h2 class="rel-title">Martins, Marin e Alves (2024)</h2>` desaparece sem ser substituído por outro título. O nome do autor segue presente APENAS em (a) rodapé `Fonte:` (D-23, D-02) e (b) prosa interna `Martins <i>et al</i>. (2024) trazem uma revisão sistemática...` no `.rel-lead` parágrafo 2, que é texto da paráfrase já existente no HEAD (D-29) e não conta como cabeçalho. A política D-02 ("autor passa a aparecer apenas no rodapé Fonte:") foi respeitada na intenção (nenhum kicker/h2 com nome do autor) e o nome só aparece como atribuição parentética dentro de prosa acadêmica padrão.
- **Subtítulo `.rel-sub` inexistente:** o slide Martins p1 não tinha `.rel-sub` no HEAD (diferente do Zorić p1 e do Yağcí p1, que tinham). Não houve `.rel-sub` para descartar.
- **CSS órfão `.rel-kicker` agora confirmado:** com este commit, `grep -c 'rel-kicker' apresentacao/index.html` retorna 0. As regras CSS `.slide-related .rel-kicker` e `.slide-related .rel-kicker .ps1` em `theme-unifacens.css` linhas 164-165 agora são oficialmente órfãs. Cleanup CSS é deferido ao plan 01-07 (CSS cleanup opcional + STYLE.md D-21) conforme já planejado no ROADMAP. Não tocar agora porque o plan 01-04 tem escopo restrito a `apresentacao/index.html` (frontmatter `files_modified`).
- **Mensagem do commit:** `apresentacao: reformatar Martins p1 com > introdução (REFORMAT-01, D-04)` segue convenção `.planning/codebase/CONVENTIONS.md` L261-285 (minúsculo, prefixo de área `apresentacao:`, sem `feat:`/`fix:`). Referência ao requirement (REFORMAT-01) e decisão (D-04) ao fim do subject reforça rastreabilidade.

## Deferred Issues

Nenhum específico deste plan. O cleanup das regras CSS órfãs `.slide-related .rel-kicker` / `.slide-related .rel-title` / `.slide-related .rel-sub` em `theme-unifacens.css` (agora confirmadas como sem uso após esta fase eliminar o último `.rel-kicker`) fica para o plan 01-07, conforme CONTEXT.md "Claude's Discretion" e ROADMAP § "Phase 1 Plans".

## Working Tree Final State

```
$ git status apresentacao/
nothing to commit, working tree clean
```

`apresentacao/index.html`: 12 sections (inalterado do plan 01-03). Slide Martins p1 vive entre as linhas 82-98 com cabeçalho novo `> introdução` na linha 87.

## Deviations from Plan

Nenhuma deviation que altere o entregável. Observações de execução:

- **Acceptance criterion #3 do plan ("`grep -c 'rel-kicker' apresentacao/index.html` diminui em 1 vs estado pré-task"):** confirmado. Estado pré-task: 1 ocorrência (linha 88 do HEAD); estado pós-task: 0 ocorrências. Diminuição de 1 → 0 = -1 (exatamente como o critério pedia). Adicionalmente, este foi o último `.rel-kicker` do arquivo, então a contagem agora atinge zero pela primeira vez na fase 1.
- **Acceptance criterion #5 do plan ("`grep -c '<p class="rel-lead">' apresentacao/index.html` mantém pelo menos 3 ocorrências dentro do slide Martins p1"):** o `grep -c` retorna 5 (total no arquivo), não 3 (no slide). Inspeção visual confirma 3 `<p class="rel-lead">` consecutivos no slide Martins p1 (linhas 89, 91, 93-94 do estado pós-edição). Os outros 2 `.rel-lead` no arquivo são do slide Zorić fundido (plan 01-02) e do slide Yağcí fundido (plan 01-03), portanto o critério é satisfeito pela contagem total ≥ 3 e pela inspeção dirigida.

## Self-Check: PASSED

- `apresentacao/index.html`: FOUND
- `.planning/phases/01-reformata-o-da-base/01-04-SUMMARY.md`: FOUND (este arquivo)
- Commit `c31658c` (Task 2): FOUND em `git log --oneline -1`
- Todas as 7 verificações automatizadas: passaram
- Section count preservado em 12 (sem fusão nem remoção nesta REQ)
- Cabeçalho `> introdução` literal aplicado (1 ocorrência)
- `<h2 class="rel-title">` com nome do autor: 0 ocorrências
- `.rel-kicker`: 0 ocorrências no arquivo (último uso eliminado)
- 3 `.rel-lead` do slide Martins p1 preservados intactos (D-29)
- Rodapé `Fonte: Martins, Marin e Alves (2024).` preservado (D-23)

## Próximo Plan

**01-05 (REFORMAT-02 Zorić p3 / slide-phases):** reformatar o slide `slide-phases` (Zorić p3, "As quatro fases do processo de EDM") trocando o `<p class="deck-topic">` interno + `<h2 class="phases-title">` por `<p class="deck-topic">` único com cabeçalho `> as quatro fases da edm` (D-05). A wrapper `<div class="phases-head">` pode ser mantida ou removida conforme efeito visual sobre o gap até `.phases-list` (decisão do planner do 01-05). Conteúdo `.phases-list` preservado intacto. Rodapé `Fonte: Zorić (2020).` preservado. Cleanup CSS órfão `.rel-kicker`/`.rel-title`/`.rel-sub` segue deferido ao plan 01-07.
