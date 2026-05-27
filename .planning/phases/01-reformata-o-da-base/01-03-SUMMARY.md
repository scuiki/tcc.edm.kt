---
phase: 01-reformata-o-da-base
plan: 03
subsystem: apresentacao
tags: [reformat, yagci, parafrase, voz-propria, deck-topic, bridge-seq, mvp]
requires:
  - "01-02 (working tree clean, 13 sections, slide Zorić fundido com paráfrase D-26)"
provides:
  - "slide Yağcı fundido único com cabeçalho `> da edm ao knowledge tracing` e `.bridge-seq` preservada"
  - "segundo slide da fase 1 a aplicar o novo padrão `.deck-topic` substituindo `.rel-kicker` + `.rel-title` + `.rel-sub`"
  - "aplicação da política D-25/D-27 (paráfrase indireta + autor parentético no lugar de citação direta literal Yağcı 2022 p.2)"
  - "ponte argumentativa explícita EDM → predição → knowledge tracing em voz própria (nós seguimos o passo seguinte)"
affects:
  - apresentacao/index.html
tech_stack_added: []
patterns_added:
  - "paráfrase D-27 em `<p class=\"rel-lead\">` com autor parentético (Yağcı, 2022) + `<b>` em 'acompanhamos o conhecimento ao longo do tempo' + `<i>` em `knowledge tracing`; sem `<blockquote class=\"rel-quote\">`; sem 'tradução nossa'"
  - "preservação literal de `.bridge-seq` (3 spans `.step` + 2 `.arr`) no slide-bridge fundido"
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-03-SUMMARY.md
key_files_modified:
  - apresentacao/index.html
decisions:
  - "D-01 aplicado: `.deck-topic` único substitui `.rel-kicker` + `.rel-title` + `.rel-sub` em ambos os slides de origem; subtítulo 'Predição do desempenho acadêmico com mineração de dados educacionais' descartado (D-03)."
  - "D-02 aplicado: autor 'Yağcı' não aparece no corpo, kicker ou h2; só no rodapé `Fonte: Yağcı (2022).` e como autor parentético na paráfrase."
  - "D-06 aplicado: cabeçalho travado `> da edm ao knowledge tracing` (1 ocorrência verificada)."
  - "D-12 aplicado: os 2 slides Yağcı viraram 1 `<section>` único com classes `slide-related slide-bridge` (preserva CSS de `.slide-bridge .bridge-seq`)."
  - "D-13 aplicado: corpo do slide fundido na ordem (paráfrase `.rel-lead` → `.bridge-seq` → `.rel-cite`); citação direta da p.2 substituída por paráfrase D-27."
  - "D-14 aplicado: descartados do p1 a citação inicial p.1, o `.rel-sub` 'Predição do desempenho acadêmico [...]' e os 3 bullets `.rel-points` (algoritmos, acurácia 70-75%, 1854 alunos)."
  - "D-23 aplicado: rodapé `Fonte: Yağcı (2022).` preservado intacto."
  - "D-25 e D-27 aplicados: citação direta Yağcı p.2 ('Outra dimensão da análise de aprendizagem é prever...') substituída por paráfrase D-27 em voz própria com autor parentético; sem `<blockquote class=\"rel-quote\">`; sem 'tradução nossa' no slide fundido."
  - "Task 1 (leitura de docs/edm_prediction.pdf) cumprida: páginas 1-3 lidas (abstract, introduction, primeira página de literature); confirmei que (a) Yağcı posiciona predição de desempenho acadêmico como 'another dimension of learning analytics' (p.2 do PDF, 1º parágrafo da subsection após 'Learning analytics has gained a new dimension'), o que sustenta a paráfrase D-27; (b) Yağcı NÃO menciona knowledge tracing em nenhum momento das páginas iniciais, portanto a transição 'Nós seguimos o passo seguinte' é corretamente marcada como autoria própria; (c) a grafia 'Yağcı' (com `ğ` e `ı`) está confirmada no cabeçalho do artigo (Mustafa Yağcı)."
  - "Bridge-text descartado: a `<p class=\"bridge-text\">` da section #13 antiga ('Yağcı (2022) posiciona a predição [...] dá o passo seguinte: em vez de uma única previsão ao fim do curso, acompanha o conhecimento [...]') foi DESCARTADA porque seu conteúdo está absorvido na paráfrase nova D-27 (voz 'nós' + gancho explícito ao knowledge tracing)."
  - "Comentário HTML do slide fundido: `<!-- ============ SLIDE · Da EDM ao knowledge tracing (Yağcı, 2022) — fusão p1+p2 ============ -->` (mantém em-dash no comentário, que não viola 'sem em-dash em prosa' por não ser texto renderizado; a prosa do `.rel-lead` está limpa de em-dash)."
requirements_completed:
  - REFORMAT-03
metrics:
  duration_seconds: 112
  duration_human: "~2 min (leitura de 3 páginas do PDF + edição + verificação + commit)"
  completed_at: "2026-05-27T19:03:13Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 1
  files_created: 1
---

# Phase 1 Plan 03: REFORMAT-03 Yağcı p1+p2 fundido — Summary

REFORMAT-03 concluído: os 2 slides `slide-related` Yağcı (#12 introdução do autor + #13 slide-bridge ponte EDM→KT) foram fundidos em um único `<section>` com cabeçalho `> da edm ao knowledge tracing`. A citação direta (Yağcı, 2022, p. 2, tradução nossa) sobre "alunos em risco de reprovação" foi substituída por paráfrase D-27 em voz própria centrada em "acompanhamos o conhecimento ao longo do tempo, a cada nova tentativa, via knowledge tracing". A sequência horizontal `.bridge-seq` (3 passos: mineração de dados educacionais → predição de desempenho → knowledge tracing) foi preservada literalmente do slide #13 original. Rodapé `Fonte: Yağcı (2022).` mantido intacto. Section count em `apresentacao/index.html` cai de 13 (após plan 01-02) para 12.

## What Was Built

- **Task 1 (leitura da referência Yağcı 2022):** `docs/edm_prediction.pdf` páginas 1-3 lidas (abstract, introduction, primeira página da seção Literature). Confirmações:
  - **p. 1 (introduction):** Yağcı define EDM como aplicação de DM em educação, com foco em descobrir padrões ocultos em dados educacionais.
  - **p. 2 (passagem-chave que é substituída):** "Another dimension of learning analytics is predicting student academic performance, uncovering patterns of system access and navigational actions, and determining students who are potentially at risk of failing (Waheed et al., 2020)." Confirmou-se que Yağcı argumenta predição como uma DIMENSÃO da análise de aprendizagem dentro do EDM, o que sustenta a paráfrase D-27 ("Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar alunos em risco").
  - **knowledge tracing não aparece em Yağcı:** o termo `knowledge tracing` não é mencionado nas páginas iniciais do artigo. A transição "Nós seguimos o passo seguinte" é corretamente marcada como autoria própria dos defendentes, não como citação a Yağcı.
  - **Grafia confirmada:** "Mustafa Yağcı" no cabeçalho do artigo (Smart Learning Environments, 2022, 9:11), com `ğ` (g com breve) e `ı` (i sem ponto).

- **Task 2 (REFORMAT-03 + paráfrase D-27):** sections #12 (linhas 318-337 pré-merge) e #13 (linhas 339-355 pré-merge) substituídas por 1 `<section>` único:
  - Comentário `<!-- ============ SLIDE · Da EDM ao knowledge tracing (Yağcı, 2022) — fusão p1+p2 ============ -->`
  - `<div class="deck-slide slide-related slide-bridge">` (preserva `slide-bridge` para o CSS `.slide-bridge .bridge-seq` em `theme-unifacens.css`)
  - `<svg class="wm">` (marca d'água Facens) preservado
  - `<p class="deck-topic"><span class="ps1">&gt;</span>da edm ao knowledge tracing<span class="caret blink"></span></p>` (único cabeçalho, padrão D-01)
  - `<p class="rel-lead">Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar alunos em risco. Nós seguimos o passo seguinte: em vez de uma previsão única ao fim do curso, <b>acompanhamos o conhecimento ao longo do tempo</b>, a cada nova tentativa, via <i>knowledge tracing</i>.</p>` (texto literal D-27)
  - `<p class="bridge-seq"><span class="step">mineração de dados educacionais</span><span class="arr">&rarr;</span><span class="step">predição de desempenho</span><span class="arr">&rarr;</span><span class="step"><i>knowledge tracing</i></span></p>` (preservada literalmente da section #13 original)
  - `<p class="rel-cite">Fonte: Yağcı (2022).</p>` (D-23 preservado)
- O slide fundido vive a partir da linha 318 (comentário) / linha 319 (`<section>`) / linha 323 (`.deck-topic`) em `apresentacao/index.html`.

## Commits

| Hash | Mensagem | Files |
|---|---|---|
| `b60439e` | `apresentacao: fundir slides Yağcı p1+p2 com paráfrase (REFORMAT-03, D-27)` | apresentacao/index.html (3 inserções, 27 deleções) |

## Verification

### Automated (todas passaram)

| Check | Esperado | Obtido |
|---|---|---|
| `grep -F -c '&gt;</span>da edm ao knowledge tracing' apresentacao/index.html` (cabeçalho D-06) | 1 | 1 |
| `grep -c 'Nós seguimos o passo seguinte' apresentacao/index.html` (paráfrase D-27) | 1 | 1 |
| `grep -c 'acompanhamos o conhecimento ao longo do tempo' apresentacao/index.html` (gancho D-27) | 1 | 1 |
| `grep -c 'Outra dimensão da análise de aprendizagem é prever' apresentacao/index.html` (citação direta p.2 removida) | 0 | 0 |
| `grep -c 'A mineração de dados educacionais tornou-se uma ferramenta eficaz' apresentacao/index.html` (citação direta p.1 removida; D-14) | 0 | 0 |
| `grep -c 'class="bridge-seq"' apresentacao/index.html` (sequência horizontal preservada) | 1 | 1 |
| `grep -o 'class="step"' apresentacao/index.html \| wc -l` (3 spans `.step` intactos) | 3 | 3 |
| `grep -c 'Yağcı' apresentacao/index.html` (grafia correta) | ≥2 | 3 |
| `grep -c 'Yagci' apresentacao/index.html` (grafia errada bloqueada) | 0 | 0 |
| `grep -c '<section data-background' apresentacao/index.html` (section count) | 12 | 12 |
| Balance `<section ` vs `</section>` | 12 / 12 | 12 / 12 |
| `grep -c 'rel-title.*Yağcı\|Yağcı.*rel-title' apresentacao/index.html` (h2 com nome do autor removido) | 0 | 0 |
| em-dash na nova `<p class="rel-lead">` | 0 | 0 |
| `grep -c 'Fonte: Yağcı (2022).' apresentacao/index.html` (D-23 preservado) | 1 | 1 |
| Commit `apresentacao: fundir slides Yağcı p1+p2 com paráfrase (REFORMAT-03, D-27)` em `git log` | sim | sim (`b60439e`) |

### Manual (a validar em sessão futura, fora deste plano)

- Browser smoke test: `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000, navegar até o slide Yağcı fundido, validar:
  - Cabeçalho em Cascadia `#5b6472` com `>` em azul e caret piscando
  - Paráfrase em Arial com "acompanhamos o conhecimento ao longo do tempo" em negrito Arial
  - "knowledge tracing" em itálico Arial (termo estrangeiro, STYLE.md linha 77)
  - `.bridge-seq` horizontal com 3 caixas estilo Word/ABNT (mineração de dados educacionais → predição de desempenho → knowledge tracing)
  - Rodapé `Fonte: Yağcı (2022).` presente no canto inferior
  - DevTools console sem erro
  - **Status: a verificar em browser** (mesma situação do plan 01-02; não bloqueia este plano).

## Decisions Made

- **`<p class="bridge-text">` da section #13 antiga descartado:** o conteúdo do `.bridge-text` original ("Yağcı (2022) posiciona a predição do desempenho como uma dimensão da análise de aprendizagem dentro do EDM. O knowledge tracing dá o passo seguinte: em vez de uma única previsão ao fim do curso, acompanha o conhecimento do estudante ao longo do tempo, a cada nova tentativa.") foi absorvido e evoluído na paráfrase D-27, que agora usa voz "nós" e explicita o gancho ao knowledge tracing. Mantê-lo como segundo parágrafo geraria redundância. Decisão alinhada com D-12 (slide fundido único) e D-13 (corpo na ordem paráfrase → `.bridge-seq` → rodapé).
- **Mensagem do commit:** `apresentacao: fundir slides Yağcı p1+p2 com paráfrase (REFORMAT-03, D-27)` segue convenção `.planning/codebase/CONVENTIONS.md` L261-285 (minúsculo, prefixo de área `apresentacao:`, sem `feat:`/`fix:`). Referência ao requirement (REFORMAT-03) e decisão (D-27) ao fim do subject reforça rastreabilidade.
- **Comentário HTML do slide fundido:** mantém em-dash dentro do comentário `<!-- ... — fusão p1+p2 ============ -->`. A regra "sem em-dash em prosa" aplica a texto exibido ao público, não a comentários do markup. A prosa do `.rel-lead` está limpa de em-dash (Gate 12 confirmou).
- **Classe `slide-bridge` preservada:** mantida porque `theme-unifacens.css` linhas ~201-210 estilizam `.slide-bridge .bridge-seq` (apresentação horizontal estilo Word/ABNT). Remover `slide-bridge` quebraria visualmente a sequência. O slide segue sendo "slide-related slide-bridge" mesmo após fusão.

## Deferred Issues

Nenhum específico deste plan. O Deferred Issue do plan 01-02 (identidade do PDF `docs/edm_review.pdf` versus citação `Zorić (2020)`) segue em aberto para tratativa futura — fora do escopo deste plan.

## Working Tree Final State

```
$ git status apresentacao/
nothing to commit, working tree clean
```

`apresentacao/index.html`: 12 sections (era 13 após plan 01-02, menos 1 do merge Yağcı). Slide fundido na linha 319-329. Próxima section depois do slide Yağcı fundido é o slide #14/#15 antigos (Corbett) — espera, esses já foram removidos em 01-01. A próxima seção após o slide Yağcí fundido agora é o fim do `<div class="slides">` raiz.

## Deviations from Plan

Nenhuma deviation que altere o entregável. Observações de execução:

- **Gate 1 do `<automated>` do plan:** a string literal `'> da edm ao knowledge tracing'` no grep do plan não casa diretamente com o markup porque o `>` é codificado como `&gt;` na HTML. A semântica do gate ("o cabeçalho aparece exatamente uma vez") foi validada com `grep -F -c '&gt;</span>da edm ao knowledge tracing' apresentacao/index.html` retornando 1, idêntico ao padrão aplicado no plan 01-02. Sem mudança de entregável.

## Self-Check: PASSED

- `apresentacao/index.html`: FOUND
- `.planning/phases/01-reformata-o-da-base/01-03-SUMMARY.md`: FOUND (este arquivo)
- Commit `b60439e` (Task 2): FOUND em `git log --oneline -3`
- Todas as 14 verificações automatizadas: passaram
- Section count caiu de 13 para 12 (esperado: -1)
- Paráfrase D-27 literal aplicada (1 ocorrência)
- 0 citações diretas Yağcı restantes
- `.bridge-seq` preservada literalmente (3 spans `.step`, 2 `.arr`)
- Grafia "Yağcı" presente (3 ocorrências: paráfrase, rodapé, comentário HTML); "Yagci" zerada

## Próximo Plan

**01-04 (REFORMAT-01 Martins p1):** reformatar slide #3 (Martins, Marin e Alves 2024 — introdução) trocando o par `.rel-kicker` + `.rel-title` + `.rel-sub` por `<p class="deck-topic">` único com cabeçalho `> introdução` (D-04). Slide já está em paráfrase (D-29: sem reescrita textual), apenas mudança de cabeçalho. Rodapé `Fonte: Martins, Marin e Alves (2024).` preservado.
