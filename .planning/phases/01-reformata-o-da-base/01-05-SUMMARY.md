---
phase: 01-reformata-o-da-base
plan: 05
subsystem: apresentacao
tags: [reformat, zoric, deck-topic, slide-phases, quatro-fases, mvp]
requires:
  - "01-04 (working tree clean, 12 sections, slide Martins p1 com cabeçalho `> introdução`)"
provides:
  - "slide-phases (Zorić p3) com cabeçalho único `> as quatro fases da edm` no `.deck-topic` interno"
  - "remoção do `<h2 class=\"phases-title\">As quatro fases do processo de EDM</h2>` redundante (D-03)"
  - "comentário HTML do slide atualizado: `SLIDE 5 · As 4 fases do EDM (fluxo horizontal formal · Zorić, 2020)` → `SLIDE · As 4 fases da EDM (Zorić, 2020)` (remove número fixo impreciso após DOM moves dos plans 02/06)"
  - "quarto slide da fase 1 a aplicar o novo padrão `> [seção]` (após plans 01-02 Zorić fundido, 01-03 Yağcí fundido, 01-04 Martins p1)"
affects:
  - apresentacao/index.html
tech_stack_added: []
patterns_added: []
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-05-SUMMARY.md
key_files_modified:
  - apresentacao/index.html
decisions:
  - "D-01 aplicado: cabeçalho `<p class=\"deck-topic\"><span class=\"ps1\">&gt;</span>as quatro fases da edm<span class=\"caret blink\"></span></p>` único; substitui o par `.deck-topic` (texto antigo `> trabalhos correlatos`) + `<h2 class=\"phases-title\">` que coexistiam dentro de `.phases-head`."
  - "D-02 aplicado: autor (Zorić) não aparece no corpo nem no cabeçalho; sobrevive exclusivamente no rodapé `<p class=\"phases-fonte\">Fonte: Zorić (2020).</p>` e na atribuição parentética `(Zorić, 2020)` dentro de `.phases-note`."
  - "D-03 aplicado: `<h2 class=\"phases-title\">As quatro fases do processo de EDM</h2>` removido por inteiro; classe `slide-phases` preservada no `<div class=\"deck-slide slide-phases\">`; wrapper `<div class=\"phases-head\">...</div>` mantido em torno do `.deck-topic` (controla margem/posicionamento contra `.phases-list`)."
  - "D-05 aplicado: cabeçalho travado `> as quatro fases da edm` (minúsculo, edm minúsculo conforme convenção `> [seção]` Cascadia `#5b6472`, STYLE.md 'Tipografia'). 1 ocorrência confirmada."
  - "D-23 aplicado: `<p class=\"phases-fonte\">Fonte: Zorić (2020).</p>` preservado intacto (linha 311)."
  - "D-29 aplicado: slide já em paráfrase no HEAD; nenhuma reescrita textual da `.phases-list` (4 itens: Definição do problema / Preparação e coleta dos dados / Modelagem e avaliação / Implantação) nem da `.phases-note` (`O processo é iterativo: a saída pode iniciar um novo ciclo (Zorić, 2020).`). Apenas o cabeçalho mudou."
  - "Wrapper `<div class=\"phases-head\">` MANTIDO (não removido): decisão tomada porque o `.phases-head` continua a função de agrupar/posicionar o cabeçalho contra a `.phases-list`. O `<h2>` interno saiu, sobrou só o `.deck-topic` dentro do wrapper. Per PATTERNS.md § 'Variante do slide-phases': a remoção do wrapper era opcional e seria decisão do planner com base em efeito visual; em texto-only não é possível avaliar visualmente, então a opção conservadora (manter) foi escolhida. Browser smoke test pode reverter essa decisão em sessão futura se o gap colapsar."
  - "Comentário HTML acima do `<section>` atualizado: `<!-- ============ SLIDE 5 · As 4 fases do EDM (fluxo horizontal formal · Zorić, 2020) ============ -->` → `<!-- ============ SLIDE · As 4 fases da EDM (Zorić, 2020) ============ -->`. Motivo: 'SLIDE 5' virou impreciso após os DOM moves planejados para os plans 02/06 (numeração posicional muda; nome do autor é descritor estável). Per PATTERNS.md § 'Template comment': 'atualizar a descrição do comentário se ela ficar enganadora após o cabeçalho mudar'. Comentário descritor 'fluxo horizontal formal' também removido (era detalhe interno do design original, sem valor de leitura para o futuro)."
  - "Sem em-dash no comentário HTML novo (diferentemente de plans 01-02/03/04 que mantiveram em-dash em separadores de descrição de slide). Justificativa: o comentário atual já é curto o suficiente para usar parênteses como agrupador (`As 4 fases da EDM (Zorić, 2020)`); um em-dash seria gratuito. Plans 01-02/03/04 mantiveram em-dashes em comentários porque o texto descritor era mais longo e o em-dash separava partes funcionalmente diferentes; aqui não há essa motivação."
  - "Mensagem do commit `apresentacao: reformatar slide-phases com > as quatro fases da edm (REFORMAT-02, D-05)` segue convenção `.planning/codebase/CONVENTIONS.md` L261-285 (minúsculo, prefixo de área `apresentacao:`, sem `feat:`/`fix:`). Referência ao requirement (REFORMAT-02) e decisão (D-05) ao fim do subject reforça rastreabilidade. Padrão idêntico ao do plan 01-04."
requirements_completed:
  - REFORMAT-02
metrics:
  duration_seconds: 60
  duration_human: "~1 min (slide já tinha `.deck-topic` na forma; só trocou texto + deletou `<h2>` + atualizou comentário)"
  completed_at: "2026-05-27T19:40:00Z"
  tasks_completed: 1
  tasks_total: 1
  files_modified: 1
  files_created: 1
---

# Phase 1 Plan 05: REFORMAT-02 Zorić p3 / slide-phases — Summary

REFORMAT-02 concluído: o slide `slide-phases` (Zorić p3, "As quatro fases do processo de EDM") teve o `<p class="deck-topic">` interno reescrito de `> trabalhos correlatos` para `> as quatro fases da edm` (D-05), e o `<h2 class="phases-title">As quatro fases do processo de EDM</h2>` que coexistia dentro do `<div class="phases-head">` foi removido (D-03). O wrapper `.phases-head` foi mantido (decisão conservadora; ver Decisions Made). Todo o conteúdo abaixo do cabeçalho (`.phases-list` com 4 itens, `.phases-note` "O processo é iterativo...", `.phases-fonte` "Fonte: Zorić (2020).") foi preservado intacto (D-29, D-23). Section count permanece em 12. Diff: 1 arquivo, +2 / -3 linhas.

Com esta REQ encerrada, 4 dos 7 plans da fase 1 estão concluídos. Padrão `.deck-topic` único agora aplicado em: Zorić fundido (01-02), Yağcí fundido (01-03), Martins p1 (01-04), slide-phases (01-05). Slides ainda no padrão antigo (a reformatar nos plans 01-06 e 01-07): slide-problem ×2 (Martins p2/p3 — REFORMAT-04), slide-kcfig (REFORMAT-05a), slide-fig (REFORMAT-05b), slide-code (REFORMAT-05c). Sequenciamento: plan 01-06 fará os 5 DOM moves + reformatações de cabeçalho dos slides ainda pendentes; plan 01-07 atualiza STYLE.md (D-21) e opcionalmente faz cleanup CSS órfão.

## What Was Built

- **Task 1 (REFORMAT-02, único task do plan):** bloco entre linhas 294-302 do `apresentacao/index.html` (estado pré-edição) editado por substituição direta. Estado pós-edição (linhas 294-301 atuais):
  - Comentário principal (linha 294): `<!-- ============ SLIDE · As 4 fases da EDM (Zorić, 2020) ============ -->`. Atualização do anterior `<!-- ============ SLIDE 5 · As 4 fases do EDM (fluxo horizontal formal · Zorić, 2020) ============ -->`: remove o número fixo "SLIDE 5" (vai virar impreciso após DOM moves nos plans 02/06) e o descritor de design "fluxo horizontal formal" (detalhe interno do design original sem valor de leitura).
  - `<section data-background-color="#F1F6FB">` (linha 295) — preservada.
  - `<div class="deck-slide slide-phases">` (linha 296) — classe `slide-phases` preservada (D-03).
  - `<svg class="wm">` (linha 297) — preservada.
  - `<div class="phases-head">` (linha 299) — wrapper preservado.
  - `<p class="deck-topic"><span class="ps1">&gt;</span>as quatro fases da edm<span class="caret blink"></span></p>` (linha 300) — **NOVO**, substitui `> trabalhos correlatos` e absorve o papel de cabeçalho único (D-01/D-05). Caret blink como último filho do `<p>`. Texto exato `as quatro fases da edm` (minúsculo, sem caracteres especiais).
  - `</div>` (linha 301) — fechamento do `.phases-head` preservado.
  - `<ol class="phases-list">` + 4 `<li>` (linhas 303-308) — preservados intactos (D-29).
  - `<p class="phases-note">O processo é iterativo: a saída pode iniciar um novo ciclo (Zorić, 2020).</p>` (linha 310) — preservado intacto (D-29).
  - `<p class="phases-fonte">Fonte: Zorić (2020).</p>` (linha 311) — preservado intacto (D-23).
  - `</div></section>` (linhas 312-313) — preservadas.

- O `.deck-topic` novo aparece na **linha 300** do `apresentacao/index.html`.

- **Deleção**: `<h2 class="phases-title">As quatro fases do processo de EDM</h2>` (linha 301 do estado pré-edição) removida por inteiro (D-03). Sem placeholder ou comentário.

## Commits

| Hash | Mensagem | Files | Diff |
|---|---|---|---|
| `23eed8b` | `apresentacao: reformatar slide-phases com > as quatro fases da edm (REFORMAT-02, D-05)` | apresentacao/index.html | +2 / -3 |

## Verification

### Automated (todas as gates substantivas passaram)

| Check (markup-aware, equivalente substantivo do plan) | Esperado | Obtido |
|---|---|---|
| `grep -c 'as quatro fases da edm<span class="caret blink"' apresentacao/index.html` (cabeçalho D-05 presente como `.deck-topic` literal) | 1 | 1 |
| `grep -c '<h2 class="phases-title">' apresentacao/index.html` (h2 antigo removido, D-03) | 0 | 0 |
| `grep -c '<ol class="phases-list">' apresentacao/index.html` (lista preservada, D-29) | 1 | 1 |
| `grep -c '<div class="phases-head">' apresentacao/index.html` (wrapper preservado, D-03) | 1 | 1 |
| `grep -c 'phases-note' apresentacao/index.html` (nota "processo é iterativo" preservada, D-29) | 1 | 1 |
| `grep -c 'class="phases-fonte">Fonte: Zorić' apresentacao/index.html` (rodapé preservado, D-23) | 1 | 1 |
| `grep -c '<section data-background' apresentacao/index.html` (section count inalterado) | 12 | 12 |
| `grep -c 'SLIDE 5 · As 4 fases' apresentacao/index.html` (comentário antigo "SLIDE 5" removido) | 0 | 0 |
| Commit `apresentacao: reformatar slide-phases com > as quatro fases da edm` em `git log --oneline -1` | sim | sim (`23eed8b`) |

**Sobre o desalinhamento entre as gates literais do plan e a estrutura do markup:**

O plan listou duas gates expressas em forma renderizada que não correspondem ao markup raw:

1. **Gate plan #1** (`grep -c '> as quatro fases da edm' apresentacao/index.html` retorna `1`): inviável estruturalmente, porque o markup gerado é `<span class="ps1">&gt;</span>as quatro fases da edm` (entidade HTML `&gt;` em vez do literal `>`, e sem espaço entre tags). Nenhum dos 9 `.deck-topic` no arquivo carrega a sequência literal `> `; todos usam `&gt;</span>` seguido sem espaço pelo texto. Equivalente substantivo verificado por `grep -c 'as quatro fases da edm<span class="caret blink"'` retornando 1.

2. **Gate plan #4** (`grep -c 'phases-head' apresentacao/index.html` retorna `2`): superpartitiva, porque o tag de fechamento em HTML é `</div>` sem o nome da classe; só o tag de abertura carrega `class="phases-head"`. O grep só consegue contar 1, mesmo com o wrapper preservado. Equivalente substantivo verificado por `grep -c '<div class="phases-head">' apresentacao/index.html` retornando 1 (wrapper preservado).

Ambas as imprecisões são análogas à do plan 01-04 (acceptance criterion #5: contagem total de `.rel-lead` no arquivo em vez de no slide específico), que foi tratada da mesma forma: registrar o gate inviável, executar e verificar o equivalente substantivo. Esta abordagem mantém o entregável fiel ao espírito do plan sem reescrever os criterios do planner.

### Manual (a validar em sessão futura, fora deste plano)

- Browser smoke test: `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000, navegar até o slide-phases (índice atualmente ~#9 do deck pós-fusões dos plans 02/03), validar:
  - Cabeçalho `> as quatro fases da edm` em Cascadia `#5b6472` com `>` em azul e caret piscando
  - 4 itens `<li>` da `.phases-list` em Arial intactos (Definição do problema / Preparação e coleta dos dados / Modelagem e avaliação / Implantação)
  - Nota `.phases-note` ("O processo é iterativo: a saída pode iniciar um novo ciclo (Zorić, 2020).") em Arial menor
  - Rodapé `.phases-fonte` ("Fonte: Zorić (2020).") no canto inferior
  - Marca d'água Facens (`<svg class="wm">`) no canto superior direito
  - DevTools console sem erro
  - Navegação ponta a ponta do deck (0..11) sem quebra
  - **Gap visual tópico → lista**: antes da reformatação, o cabeçalho tinha 2 elementos (`.deck-topic` + `<h2>`) dentro de `.phases-head`. Agora só o `.deck-topic` sobrou. Validar se o gap até `<ol class="phases-list">` continua legível; se houver colapso visual, ajuste de `margin-top` em `.phases-list` ou `margin-bottom` em `.phases-head` pode entrar no plan 01-07 (CSS cleanup).
  - **Status: a verificar em browser** (mesma situação dos plans 01-01/02/03/04; não bloqueia este plano).

## Decisions Made

- **Wrapper `<div class="phases-head">` mantido (não removido):** o PATTERNS.md § "Variante do slide-phases" deixou a remoção do wrapper como opcional, decisão do planner com base no efeito visual sobre o gap até `.phases-list`. Como esta sessão é text-only (sem acesso a browser headless integrado a este turn), a avaliação visual não foi possível. Decisão conservadora: manter o wrapper para preservar margem/posicionamento original do cabeçalho. Se o browser smoke test futuro identificar gap excessivo (espaço vazio no lugar do `<h2>` removido), o plan 01-07 pode (a) remover o wrapper completamente, ou (b) ajustar `margin-bottom` em `.phases-head` no CSS.
- **Comentário HTML atualizado, em-dash não usado:** o comentário novo (`<!-- ============ SLIDE · As 4 fases da EDM (Zorić, 2020) ============ -->`) usa parênteses para agrupar o autor + ano, não em-dash, diferentemente dos comentários novos dos plans 01-02/03/04 (que carregavam em-dash em separadores tipo `· Trabalhos correlatos: Martins, Marin e Alves (2024) — recorte do problema`). Justificativa: o texto descritor aqui é curto e estruturalmente simples (tópico + atribuição); um em-dash seria gratuito. A regra "sem em-dash em prosa" aplica ao texto renderizado; comentários HTML não são prosa renderizada, mas optar por dispensar o em-dash quando não agrega valor mantém a higiene textual do projeto.
- **Remoção do detalhe "SLIDE 5" e "fluxo horizontal formal" do comentário:** o número "5" virou impreciso após os DOM moves dos plans 02 (Zorić fundido reduziu 14→13 sections) e 03 (Yağcí fundido reduziu 13→12 sections), e os plans 06/07 vão re-ordenar mais slides ainda. Manter "SLIDE 5" no comentário criaria divergência permanente entre o número estático e a posição real do slide. O descritor "fluxo horizontal formal" descrevia uma característica do design original que não é mais relevante para leitura futura do markup (o estilo visual está em `theme-unifacens.css`, não no comentário). Comentário final é descritivo do conteúdo e atribuição (`As 4 fases da EDM (Zorić, 2020)`), padronizado com os outros comentários do arquivo.
- **Nenhuma releitura do PDF de Zorić feita:** o slide cita Zorić (2020) e a CRITICAL note do prompt avisou que o symlink `docs/edm_review.pdf` aponta para Kalita et al. (2025), não Zorić. Como este plan NÃO alterou texto citacional do slide (D-29: só cabeçalho mudou; `.phases-list`, `.phases-note`, `.phases-fonte` ficaram intactos), e como o conteúdo do slide já foi validado em sessões anteriores (PROJECT.md "Validated"), a releitura da fonte não era requirement. Se um plan futuro alterar o texto das 4 fases, esse plan deverá localizar a fonte Zorić correta (provavelmente fora de `docs/`) antes de redigir.
- **Mensagem do commit:** `apresentacao: reformatar slide-phases com > as quatro fases da edm (REFORMAT-02, D-05)` segue convenção `.planning/codebase/CONVENTIONS.md` L261-285 (minúsculo, prefixo de área `apresentacao:`, sem `feat:`/`fix:`). Referência ao requirement (REFORMAT-02) e decisão (D-05) ao fim do subject reforça rastreabilidade. Padrão idêntico ao dos plans 01-02/03/04.

## Deferred Issues

Nenhum específico deste plan. Itens já deferidos da fase 1 que continuam pendentes:

- Cleanup CSS órfão `.slide-related .rel-kicker` / `.rel-title` / `.rel-sub` em `theme-unifacens.css` linhas 164-167 (confirmado órfão desde o plan 01-04). Deferido ao plan 01-07.
- Avaliação visual em browser (smoke test fim-a-fim) para validar o gap entre `.deck-topic` e `.phases-list` após remoção do `<h2>` interno. Se o gap colapsar visualmente, ajuste de CSS ou remoção do wrapper `.phases-head` entra no plan 01-07.
- STYLE.md update (D-21) com a nova convenção de cabeçalho `> [seção]`, atualização do inventário, remoção do bullet "Regra dos correlatos". Deferido ao plan 01-07.

## Working Tree Final State

```
$ git status apresentacao/
nothing to commit, working tree clean
```

`apresentacao/index.html`: 12 sections (inalterado desde plan 01-03). slide-phases vive entre as linhas 295-313 com cabeçalho novo `> as quatro fases da edm` na linha 300 e `<h2 class="phases-title">` removido.

## Deviations from Plan

Nenhuma deviation que altere o entregável. Observações de execução:

- **Acceptance criterion #1 do plan (`grep -c '> as quatro fases da edm' apresentacao/index.html` = `1`):** literal não encontrável no markup raw porque o `>` é entidade HTML `&gt;` (sem espaço para o texto seguinte). Equivalente substantivo verificado por `grep -c 'as quatro fases da edm<span class="caret blink"'` = 1. Imprecisão estilística do plan; substância entregue.
- **Acceptance criterion #4 do plan (`grep -c 'phases-head' apresentacao/index.html` = `2`):** superpartitivo porque tag de fechamento HTML `</div>` não carrega o nome da classe. Equivalente substantivo verificado por `grep -c '<div class="phases-head">' apresentacao/index.html` = 1 (wrapper aberto e fechado dentro do slide; visualmente preservado). Imprecisão estilística do plan; substância entregue.

Tratamento análogo ao do plan 01-04 (acceptance criterion #5: contagem total de `.rel-lead` no arquivo em vez de no slide). Política aplicada: registrar a imprecisão, executar o equivalente substantivo, e documentar a divergência no SUMMARY para auditoria futura sem reescrever o plan.

## Self-Check: PASSED

- `apresentacao/index.html`: FOUND
- `.planning/phases/01-reformata-o-da-base/01-05-SUMMARY.md`: FOUND (este arquivo, criado neste plan)
- Commit `23eed8b` (Task 1): FOUND em `git log --oneline -1`
- Todas as 9 verificações automatizadas (markup-aware): passaram
- Section count preservado em 12 (sem fusão nem remoção nesta REQ)
- Cabeçalho `> as quatro fases da edm` literal aplicado (1 ocorrência)
- `<h2 class="phases-title">`: 0 ocorrências (D-03)
- `.phases-list` (4 itens), `.phases-note`, `.phases-fonte` preservados intactos (D-29, D-23)
- Wrapper `.phases-head` preservado (decisão conservadora documentada)
- Comentário HTML acima do `<section>` atualizado (removido "SLIDE 5", removido "fluxo horizontal formal", autor + ano agrupados em parênteses)

## Próximo Plan

**01-06 (REFORMAT-04 + REFORMAT-05a/b/c):** DOM move + reformatação de cabeçalho dos 5 slides finais ainda no padrão antigo:

- Martins p2 (`slide-problem`) → cabeçalho `> retomando o problema` (D-07) + mover para fim do `<section>` raiz
- Martins p3 (`slide-problem`) → cabeçalho `> retomando o problema` (D-07) + adjacente a Martins p2
- slide-kcfig → cabeçalho `> kcs semânticos extraídos` (D-08) + mover para fim, antes do trio Martins+fig
- slide-fig → cabeçalho `> evolução por dificuldade` (D-09) + mover para fim, imediatamente após Martins p3
- slide-code → cabeçalho `> o que o code-dkt olha` (D-10) + mover para fim, antes do trio Martins+fig

Ordem final no fim do `<section>` raiz (D-16/D-17): slide-code OU slide-kcfig (ordem livre) → outro → trio Martins p2 → Martins p3 → slide-fig (NESTA ordem, sem nada entre eles). REFORMAT-04 (Martins p2/p3) é EXCEÇÃO à regra de paráfrase (D-28): citações diretas literais mantidas porque os números "13 autores" / "10 autores" são o argumento quantitativo.

Plans 01-07 fica para o final: STYLE.md update (D-21), cleanup CSS órfão `.rel-kicker`/`.rel-title`/`.rel-sub`, e validação visual fim-a-fim.
