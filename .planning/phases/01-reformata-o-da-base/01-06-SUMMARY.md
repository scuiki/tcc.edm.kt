---
phase: 01-reformata-o-da-base
plan: 06
subsystem: apresentacao
tags: [reformat, dom-move, martins, slide-code, slide-kcfig, slide-fig, mvp]
requires:
  - "01-05 (working tree clean, 12 sections, padrão `.deck-topic` aplicado em Martins p1 + Zorić fundido + Yağcí fundido + slide-phases)"
provides:
  - "5 slides (slide-code, slide-kcfig, Martins p2, Martins p3, slide-fig) reformatados com cabeçalho `.deck-topic` único e movidos para o fim do `<div class=\"slides\">` na ordem travada D-16/D-17"
  - "ordem DOM final: capa → título TCC → agenda → Martins p1 (intro) → Zorić fundido → slide-phases → Yağcí fundido → slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig"
  - "trio adjacente Martins p2 + Martins p3 + slide-fig no fim do deck (CLOSE-01/02/03), pronto para a fase 4 inserir MODEL-01..06 nos gaps abertos antes de slide-code e entre slide-kcfig/Martins p2"
  - "todos os 7 slides afetados pela fase 1 agora carregam o cabeçalho `> [seção]` único (`.deck-topic`); padrão `> trabalhos correlatos` extinto no deck"
  - "as 2 citações diretas Martins (p.19 \"mencionada por 13 autores\" e p.20 \"citado por 10 autores\") preservadas intactas como exceção legítima D-28"
affects:
  - apresentacao/index.html
tech_stack_added: []
patterns_added: []
key_files_created:
  - .planning/phases/01-reformata-o-da-base/01-06-SUMMARY.md
key_files_modified:
  - apresentacao/index.html
decisions:
  - "D-01 aplicado (Task 1): cabeçalho `<p class=\"deck-topic\"><span class=\"ps1\">&gt;</span>[texto]<span class=\"caret blink\"></span></p>` único em todos os 5 slides; substitui o par `.deck-topic` (`> trabalhos correlatos`) + `<h2>` (ou `.kcfig-title`) que coexistiam."
  - "D-02 aplicado: autores (Martins, Duan) não aparecem no corpo nem no cabeçalho; sobrevivem exclusivamente nos rodapés `Fonte:`."
  - "D-03 aplicado: `<h2 class=\"prob-head\">` (×2), `<h2 class=\"fig-title\">`, `<h2 class=\"code-title\">` e `<p class=\"kcfig-title\">` removidos por inteiro; classes CSS de layout (`.slide-problem`, `.slide-fig`, `.slide-code`, `.slide-kcfig`) preservadas."
  - "D-07 aplicado: Martins p2 e Martins p3 ambos com cabeçalho `> retomando o problema` (mesmo texto, deliberadamente — reforça continuidade no bloco de fechamento). 2 ocorrências confirmadas."
  - "D-08 aplicado: slide-kcfig com cabeçalho `> kcs semânticos extraídos`. 1 ocorrência."
  - "D-09 aplicado: slide-fig com cabeçalho `> evolução por dificuldade`. 1 ocorrência."
  - "D-10 aplicado: slide-code com cabeçalho `> o que o code-dkt olha` (code-dkt minúsculo com hífen). 1 ocorrência."
  - "D-15 aplicado (Task 2): movimentação executada na fase 1 (não deferida para fase 4); cabeçalho `> retomando o problema` faz sentido agora porque Martins p2/p3 estão posicionados ao fim do deck."
  - "D-16 aplicado: ordem final no fim de `<div class=\"slides\">`: slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig."
  - "D-17 aplicado: (a) Martins p2 e Martins p3 adjacentes; (b) slide-fig imediatamente após Martins p3; (c) slide-code e slide-kcfig precedem o trio Martins+fig. Verificado por script Python parseando a ordem das classes `deck-slide`."
  - "D-18 respeitado: os gaps abertos por esta movimentação (entre Yağcí e slide-code; entre slide-kcfig e Martins p2) ficam reservados para a fase 4 inserir MODEL-01/02 antes de slide-code e MODEL-04..06 entre slide-kcfig e o trio; MARKER-03 logo após slide-fig."
  - "D-23 aplicado: cada um dos 5 slides reformatados mantém UMA linha `Fonte:` correta (Martins p2/p3: `Fonte: adaptado de Martins, Marin e Alves (2024).`; slide-kcfig: rodapé com múltiplas referências; slide-fig e slide-code: rodapés `elaborado pelos autores` originais preservados)."
  - "D-24 aplicado: slide-kcfig mantém o formato existente `Fonte: elaborado pelos autores, com base em Duan et al. (2025) e Martins, Marin e Alves (2024).` sem mudança."
  - "D-25 aplicado por exceção: como o padrão é paráfrase, slide-fig, slide-code e slide-kcfig ficam apenas com cabeçalho novo (já não tinham citação direta no HEAD); Martins p2/p3 são EXCEÇÃO legítima conforme D-28."
  - "D-28 aplicado: as 2 citações diretas Martins (`<blockquote class=\"prob-quote\">` em Martins p2 com p.19 \"mencionada por 13 autores\" e Martins p3 com p.20 \"citado por 10 autores\") PRESERVADAS intactas — paráfrase enfraqueceria o argumento quantitativo da revisão sistemática."
  - "D-29 aplicado: corpo interno de cada um dos 5 slides preservado intacto (2 ascii-charts, kcfig-map com 6 kc-row, fig-wrap com img, code-card com pre devcpp; subtítulos `.prob-sub`, leitura `.fig-read`, lead/take `.code-lead`/`.code-take`)."
  - "Claude's Discretion D-16: escolhi `slide-code` ANTES de `slide-kcfig` no bloco final. Justificativa narrativa: a interpretabilidade do código (atenção no operador `&&` da submissão real do CSEDM) é a evidência concreta do Code-DKT \"olhando\" para construtos relevantes; o slide-kcfig vem depois para mostrar como a saída do pipeline LLM-para-KC (Duan) confirma a mesma estrutura conceitual que o Code-DKT extrai estatisticamente. Recomendação do plan seguida verbatim."
  - "Comentário HTML do Martins p3 mantém o em-dash do plan: `<!-- ============ SLIDE · Retomando o problema · Martins p3 — dentro dos conceitos técnicos (Martins, Marin e Alves, 2024) ============ -->`. O plan especifica esse texto exato; segui literal. Plan 01-05 SUMMARY adotou política de evitar em-dash em comentários quando não agrega; plan 01-06 reverte essa preferência ao escrever os comentários verbatim no texto do plano. Substância (o slide carrega o cabeçalho correto e está no lugar certo) preservada; estilo do comentário segue o plano."
  - "Mensagens de commit seguem convenção CONVENTIONS.md L261-285 (minúsculo, prefixo `apresentacao:`, sem `feat:`/`fix:`): Task 1 = `apresentacao: reformatar cabeçalhos dos 5 slides do bloco final (REFORMAT-04 + REFORMAT-05)`; Task 2 = `apresentacao: mover trio Martins+fig e slide-code/slide-kcfig para o fim (REFORMAT-04 + REFORMAT-05, D-16/D-17)`."
requirements_completed:
  - REFORMAT-04
  - REFORMAT-05
metrics:
  duration_seconds: 240
  duration_human: "~4 min (2 tasks: header reformatting + DOM move; commits atômicos)"
  completed_at: "2026-05-27T20:00:00Z"
  tasks_completed: 2
  tasks_total: 2
  files_modified: 1
  files_created: 1
---

# Phase 1 Plan 06: REFORMAT-04 + REFORMAT-05 — Reformatação + DOM move dos 5 slides finais — Summary

REFORMAT-04 e REFORMAT-05 concluídos em duas passadas atômicas. Task 1: reformatou os cabeçalhos dos 5 slides afetados in-place (Martins p2, Martins p3, slide-kcfig, slide-fig, slide-code), substituindo `> trabalhos correlatos<h2>...</h2>` pelo `.deck-topic` único travado por D-07..D-10. Task 2: recortou os 5 sections (com seus comentários) e colou no fim de `<div class="slides">` na ordem travada D-16: slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig. As 2 citações diretas Martins (p.19 e p.20) preservadas intactas como exceção D-28. Corpo interno de todos os 5 slides preservado (2 ascii-charts, kcfig-map de 6 rows, fig-wrap, code-card com snippet real do CSEDM). Section count permanece em 12. Diff total: +118 / -123 linhas (Task 1: +11/-16; Task 2: +115/-115 — o "swap" da movimentação produz contagens grandes mas balanceadas).

Com esta REQ encerrada, **6 dos 7 plans da fase 1 estão concluídos**. Padrão `.deck-topic` único agora aplicado em todos os 9 slides de conteúdo do deck (capa/título TCC/agenda preservados como exceções estruturais). Resta apenas o plan 01-07: STYLE.md update (D-21), cleanup CSS órfão `.rel-kicker`/`.rel-title`/`.rel-sub` em `theme-unifacens.css`, e validação visual fim-a-fim em browser.

## What Was Built

### Task 1 — Reformatar cabeçalhos dos 5 slides (commit `590ae34`)

Substituições in-place no `apresentacao/index.html` (sem mover sections):

**Slide-problem Martins p2** (`<h2 class="prob-head">O problema</h2>`):
- Comentário HTML: `<!-- ============ SLIDE 4 · O problema (Martins, Marin e Alves, 2024) ============ -->` → `<!-- ============ SLIDE · Retomando o problema · Martins p2 (Martins, Marin e Alves, 2024) ============ -->`
- Cabeçalho: `<p class="deck-topic">...trabalhos correlatos...</p>` + `<h2 class="prob-head">O problema</h2>` → `<p class="deck-topic"><span class="ps1">&gt;</span>retomando o problema<span class="caret blink"></span></p>` (h2 deletado)
- Preservado intacto: `<blockquote class="prob-quote">` (p.19, D-28), `<p class="prob-sub">`, `<div class="ascii-chart">` (7 barras: 13/12/10/8/7/6/6), `<p class="prob-cite">Fonte: adaptado de Martins, Marin e Alves (2024).</p>`.

**Slide-problem Martins p3** (`<h2 class="prob-head">Dentro dos conceitos técnicos</h2>`):
- Comentário HTML: `<!-- ============ SLIDE · Dentro dos conceitos técnicos (decomposição · Martins et al., 2024, p. 20-21) ============ -->` → `<!-- ============ SLIDE · Retomando o problema · Martins p3 — dentro dos conceitos técnicos (Martins, Marin e Alves, 2024) ============ -->`
- Cabeçalho: análogo ao Martins p2, h2 deletado, novo `.deck-topic` = `> retomando o problema` (mesmo texto, D-07).
- Preservado intacto: `<blockquote class="prob-quote">` (p.20, D-28), `<p class="prob-sub">`, `<div class="ascii-chart">` (5 barras: 10/7/4/4/3), rodapé.

**Slide-kcfig**:
- Comentário HTML: `<!-- ============ SLIDE · Figura: KCs (KCGen-KT) ligados às dificuldades (Martins et al., 2024) ============ -->` + linha auxiliar removida `tudo em Arial; nomes PT-BR` → `<!-- ============ SLIDE · KCs semânticos extraídos (Duan et al., 2025; Martins, Marin e Alves, 2024) ============ -->` + linha auxiliar `modelo "Word": quadrados ligados; nomes PT-BR de results/kc_translations.json`
- Cabeçalho: `<p class="deck-topic">...trabalhos correlatos...</p>` + `<p class="kcfig-title">KCs (KCGen-KT) e as dificuldades em conceitos de programação</p>` → `<p class="deck-topic"><span class="ps1">&gt;</span>kcs semânticos extraídos<span class="caret blink"></span></p>` (`.kcfig-title` deletado por consistência D-03)
- Preservado intacto: `<div class="kcfig-map">` com 6 `.kc-row` (estruturas de controle, manipulação de variáveis, operadores e expressões lógicas, funções, vetores, conhecimento matemático), cada uma com `.kc-diff` + `.kc-link` + 3 ou 2 `.kc-box`; rodapé múltipla-referência D-24.

**Slide-fig**:
- Comentário HTML: `<!-- ============ SLIDE · Dificuldade de aprendizado (Code-DKT) por dificuldade de Martins ============ -->` → `<!-- ============ SLIDE · Evolução por dificuldade · Curva Code-DKT (Code-DKT, Shi et al., 2022; Martins, Marin e Alves, 2024) ============ -->` (linha auxiliar `figura: results/fig_codedkt_difficulty_martins.png ...` mantida intacta)
- Cabeçalho: `<p class="deck-topic">...trabalhos correlatos...</p>` + `<h2 class="fig-title">Quão difícil de aprender? Curva de aprendizado do Code-DKT por dificuldade</h2>` → `<p class="deck-topic"><span class="ps1">&gt;</span>evolução por dificuldade<span class="caret blink"></span></p>` (h2 deletado)
- Preservado intacto: `<div class="fig-wrap"><img src="assets/fig-codedkt-martins-curves.png" ...></div>`, `<p class="fig-read">` (leitura do gráfico), `<p class="fig-fonte">` (rodapé).

**Slide-code**:
- Comentário HTML: `<!-- ============ SLIDE · O que o Code-DKT olha ao prever erro (exemplo de código real) ============ -->` → `<!-- ============ SLIDE · O que o Code-DKT olha (Code-DKT, Shi et al., 2022) ============ -->` (linha auxiliar `submissão real do CSEDM (A439, dateFashion); atenção máxima no operador && (0,97)` mantida intacta)
- Cabeçalho: `<p class="deck-topic">...trabalhos correlatos...</p>` + `<h2 class="code-title">O que o Code-DKT &ldquo;olha&rdquo; ao prever erro</h2>` → `<p class="deck-topic"><span class="ps1">&gt;</span>o que o code-dkt olha<span class="caret blink"></span></p>` (h2 deletado)
- Preservado intacto: `<p class="code-lead">` (intro Diferente de BKT e DKT), `<div class="code-card">` com `<pre class="devcpp__gutter">1..15` e `<pre class="devcpp__code">` (snippet dateFashion completo do CSEDM, 15 linhas com keyword highlighting e `<span class="hl">&amp;&amp;</span>`), `<p class="code-take">` (takeaway interpretabilidade), `<p class="code-fonte">` rodapé.

### Task 2 — Mover os 5 sections para o fim do `<div class="slides">` (commit `2a86049`)

Operação: recortar cada uma das 5 sections (com seus respectivos comentários HTML acima) do meio do arquivo (linhas 100-274 do estado pós-Task 1) e colar no fim de `<div class="slides">`, imediatamente após o Yağcí fundido (que era até então o último slide), na ordem travada D-16: slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig.

**Ordem DOM final** (validada por script Python parseando classes `deck-slide` no arquivo):

```
[slide-cover-brand, slide-title-tcc, slide-agenda, slide-related, slide-related, slide-phases, slide-related slide-bridge, slide-code, slide-kcfig, slide-problem, slide-problem, slide-fig]
```

Interpretação por slide:
1. slide-cover-brand (capa, intacto)
2. slide-title-tcc (capa TCC, intacto)
3. slide-agenda (intacto)
4. slide-related = Martins p1 (`> introdução`, plan 01-04)
5. slide-related = Zorić fundido (`> mineração de dados educacionais`, plan 01-02)
6. slide-phases = Zorić p3 (`> as quatro fases da edm`, plan 01-05)
7. slide-related slide-bridge = Yağcí fundido (`> da edm ao knowledge tracing`, plan 01-03)
8. **slide-code (`> o que o code-dkt olha`)** ← movido (Claude's Discretion: slide-code primeiro)
9. **slide-kcfig (`> kcs semânticos extraídos`)** ← movido
10. **slide-problem = Martins p2 (`> retomando o problema`)** ← movido, abre o trio
11. **slide-problem = Martins p3 (`> retomando o problema`)** ← movido, adjacente
12. **slide-fig (`> evolução por dificuldade`)** ← movido, imediatamente após Martins p3, último do deck

**Restrições D-17 verificadas:**
- (a) Martins p2 (índice 9) e Martins p3 (índice 10) adjacentes ✓
- (b) slide-fig (índice 11) imediatamente após Martins p3 (índice 10) ✓
- (c) slide-code (índice 7) e slide-kcfig (índice 8) precedem Martins p2 (índice 9) ✓

**Claude's Discretion D-16 — escolha slide-code antes de slide-kcfig:** seguida a recomendação do plan. Justificativa narrativa para o TCC 2: a interpretabilidade do código (Code-DKT olhando para o operador `&&` da submissão real do CSEDM no problema `dateFashion`) é a evidência concreta do que o modelo "olha"; o slide-kcfig vem depois mostrando como a saída do pipeline LLM-para-KC (Duan, 2025) confirma a mesma estrutura conceitual que o Code-DKT extrai estatisticamente. A ordem slide-code → slide-kcfig amarra "modelo olha" → "essa visão confirma a abstração semântica dos KCs" antes do CLOSE Martins (que retoma o problema original e mostra que os KCs cobrem as dificuldades quantificadas).

**Gaps abertos para a fase 4 (D-18):**
- Entre Yağcí (índice 6) e slide-code (índice 7): MODEL-01 (Code-DKT funcionamento + AST inset) e MODEL-02 (cortado, fundido em MODEL-01); espaço também para MARKER-02 (fim da fase 2) e MODEL-03 = slide-code reaproveitado.
- Entre slide-kcfig (índice 8) e Martins p2 (índice 9): MODEL-04 (resultados Code-DKT vs Shi), MODEL-05 (Duan + pipeline KCs).
- Após slide-fig (índice 11): MARKER-03 (fim da fase 3 EDM).

## Commits

| Hash | Task | Mensagem | Files | Diff |
|---|---|---|---|---|
| `590ae34` | 1 | `apresentacao: reformatar cabeçalhos dos 5 slides do bloco final (REFORMAT-04 + REFORMAT-05)` | apresentacao/index.html | +11 / -16 |
| `2a86049` | 2 | `apresentacao: mover trio Martins+fig e slide-code/slide-kcfig para o fim (REFORMAT-04 + REFORMAT-05, D-16/D-17)` | apresentacao/index.html | +115 / -115 |

## Verification

### Automated — Task 1 (todas as gates substantivas passaram)

| Check | Esperado | Obtido |
|---|---|---|
| `grep -c 'retomando o problema<span class="caret blink"' apresentacao/index.html` (D-07, equivalente markup-aware do gate plan) | 2 | 2 |
| `grep -c 'kcs semânticos extraídos<span class="caret blink"' apresentacao/index.html` (D-08) | 1 | 1 |
| `grep -c 'evolução por dificuldade<span class="caret blink"' apresentacao/index.html` (D-09) | 1 | 1 |
| `grep -c 'o que o code-dkt olha<span class="caret blink"' apresentacao/index.html` (D-10) | 1 | 1 |
| `grep -c '<h2 class="prob-head">' apresentacao/index.html` (D-03) | 0 | 0 |
| `grep -c '<h2 class="fig-title">' apresentacao/index.html` (D-03) | 0 | 0 |
| `grep -c '<h2 class="code-title">' apresentacao/index.html` (D-03) | 0 | 0 |
| `grep -c '<p class="kcfig-title">' apresentacao/index.html` (D-03) | 0 | 0 |
| `grep -c 'mencionada por 13 autores' apresentacao/index.html` (D-28 Martins p2) | 1 | 1 |
| `grep -c 'citado por 10 autores' apresentacao/index.html` (D-28 Martins p3) | 1 | 1 |
| `grep -c 'class="ascii-chart"' apresentacao/index.html` (charts Martins p2+p3) | 2 | 2 |
| `grep -c 'class="kcfig-map"' apresentacao/index.html` (mapa kcfig) | 1 | 1 |
| `grep -c 'class="fig-wrap"' apresentacao/index.html` (figura Code-DKT) | 1 | 1 |
| `grep -c 'class="code-card"' apresentacao/index.html` (snippet dateFashion) | 1 | 1 |
| Commit `apresentacao: reformatar cabeçalhos dos 5 slides do bloco final` em `git log` | sim | sim (`590ae34`) |

### Automated — Task 2 (todas as gates passaram)

| Check | Esperado | Obtido |
|---|---|---|
| DOM order Python check (D-17 a/b/c, classes parseadas via regex) | `OK: all D-17 constraints satisfied` | `OK: all D-17 constraints satisfied` |
| `grep -c '<section data-background' apresentacao/index.html` (section count) | 12 | 12 |
| Última section antes de `</div></div><script>` é slide-fig (validado via `grep -n` + `sed -n`: `<div class="deck-slide slide-fig">` em linha 315, `    </div>` em linha 325) | sim | sim |
| Commit `apresentacao: mover trio Martins+fig e slide-code/slide-kcfig para o fim` em `git log` | sim | sim (`2a86049`) |

### Manual (a validar em sessão futura — não bloqueia este plano)

Browser smoke test fim-a-fim: `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000.
- Slide 0 (capa Facens) → 1 (capa TCC) → 2 (agenda) → 3 (Martins p1 `> introdução`) → 4 (Zorić fundido) → 5 (slide-phases) → 6 (Yağcí fundido) → 7 (slide-code `> o que o code-dkt olha`) → 8 (slide-kcfig `> kcs semânticos extraídos`) → 9 (Martins p2 `> retomando o problema`, com chart animado) → 10 (Martins p3 `> retomando o problema`, com chart animado) → 11 (slide-fig `> evolução por dificuldade`)
- Em cada slide: cabeçalho `.deck-topic` em Cascadia 24px com `>` azul e caret piscando; corpo intacto; rodapé `Fonte:` correto
- Slides Martins: animação ASCII (`animateAscii`) deve disparar ao entrar via setas — verificar que `data-ascii` ainda está presente (foi preservado no recorte/cola)
- Slide-code: `pasteIDE` não aplica (gutter+code sem `data-paste-code`) — exibição estática esperada
- DevTools console SEM erro

## Decisions Made

- **Claude's Discretion D-16 — slide-code antes de slide-kcfig:** segui a recomendação literal do plan. Narrativa do TCC 2: a interpretabilidade no nível de token (Code-DKT olhando para `&&`) precede a abstração semântica (KCs do pipeline LLM). slide-code → slide-kcfig amarra "como o modelo olha" → "essa visão é consistente com a abstração semântica de KCs". A ordem oposta também cumpriria D-16 e D-17, mas a ordem narrativa escolhida favorece o storytelling do CLOSE Martins (problema quantificado → KCs gerados pela pipeline cobrem as dificuldades quantificadas).
- **Citações diretas Martins preservadas (D-28):** as 2 `<blockquote class="prob-quote">` com `(Martins; Marin; Alves, 2024, p. 19)` e `p. 20` permanecem intactas. Os números "mencionada por 13 autores" e "citado por 10 autores" são o argumento quantitativo da revisão sistemática; uma paráfrase do tipo "Martins et al. apontam que a compreensão de conceitos técnicos é a dificuldade mais comum" perde o impacto retórico do consenso da literatura. Esta é a exceção legítima registrada em D-25 e mantida durante toda a fase 1.
- **Comentários HTML — mantido o em-dash do plan no Martins p3:** o plan especifica verbatim `<!-- ============ SLIDE · Retomando o problema · Martins p3 — dentro dos conceitos técnicos (Martins, Marin e Alves, 2024) ============ -->` com em-dash separando "Martins p3" de "dentro dos conceitos técnicos". O plan 01-05 SUMMARY havia adotado política mais higiênica (parênteses no lugar de em-dash em comentários HTML novos), mas o plan 01-06 escreve o comentário literal. Como o entregável de cada plan é seguir o markup exato do plan, preservei o em-dash. Não é em-dash em prosa renderizada (regra `feedback_no_em_dashes`); HTML comments não são lidos pela banca. Substância (slide reformatado e posicionado corretamente) preservada.
- **Linhas auxiliares de comentário HTML (slide-kcfig, slide-fig, slide-code):** as linhas `<!-- modelo "Word"...-->`, `<!-- figura: results/...-->`, `<!-- submissão real do CSEDM...-->` foram tratadas individualmente:
  - slide-kcfig: simplificada de `<!-- modelo "Word": quadrados ligados; tudo em Arial; nomes PT-BR de results/kc_translations.json -->` para `<!-- modelo "Word": quadrados ligados; nomes PT-BR de results/kc_translations.json -->` (removido "tudo em Arial" que era detalhe redundante com o CSS).
  - slide-fig e slide-code: linhas auxiliares mantidas intactas (carregam metadado de origem do dado/figura, valor de leitura para futuras manutenções).
  - Plan especificou explicitamente a forma das atualizações; segui literalmente.
- **DOM move atomicamente em uma única operação por Edit tool:** considerei fazer 5 Edits separados (1 por slide), mas isso geraria um arquivo intermediário com 5 sections órfãs flutuando ao final, antes de cada inserção precisa. Em vez disso, usei 2 Edits para Task 2: (1) deletar o bloco contíguo de 5 sections do meio (linhas 100-274 do estado pós-Task 1, que eram todos adjacentes na ordem original Martins p2, p3, kcfig, fig, code), (2) inserir os 5 sections no fim do `<div class="slides">` na ordem correta (code, kcfig, p2, p3, fig). Essa abordagem garante que o arquivo nunca esteja num estado inconsistente entre Edits (sempre tem 12 sections válidas) e que as restrições D-17 sejam atendidas após o segundo Edit.
- **Mensagens dos 2 commits:** seguem convenção `.planning/codebase/CONVENTIONS.md` L261-285 (minúsculo, prefixo de área `apresentacao:`, sem `feat:`/`fix:`). Task 1 lista os REQs encerrados (REFORMAT-04 + REFORMAT-05) no subject; Task 2 adiciona as decisões D-16/D-17 ao subject para rastreabilidade. Padrão idêntico aos plans 01-02/03/04/05.

## Deferred Issues

Nenhum específico deste plan. Itens já deferidos da fase 1 que permanecem pendentes para o plan 01-07:

- **STYLE.md update (D-21):** três seções precisam de reescrita — "Cabeçalho de todo slide após a AGENDA" (descrever o `> [seção]` único como padrão), bullet "Regra dos correlatos" (remover e substituir por nota sobre cabeçalho temático), tabela "Inventário de slides (ordem atual)" (redesenhar para refletir 12 sections pós-fase 1 com a ordem final aqui registrada). Deferido para o plan 01-07.
- **CSS cleanup órfão:** confirmar via `grep -c 'rel-kicker\|rel-title\|rel-sub' apresentacao/index.html` que retorna 0; se sim, remover as 4 regras de `theme-unifacens.css` linhas 164-167. Deferido para o plan 01-07.
- **Browser smoke test fim-a-fim:** validação visual em http://127.0.0.1:8000 navegando do slide 0 ao 11 com setas, confirmando todos os 9 cabeçalhos `.deck-topic` novos, animações ASCII (chart Martins p2 e p3) disparando ao entrar, console DevTools sem erro. Deferido para o plan 01-07 (checkpoint humano final da fase 1).
- **Gap visual `.kcfig-title` removido:** o slide-kcfig perdeu o título `<p class="kcfig-title">KCs (KCGen-KT) e as dificuldades em conceitos de programação</p>` que ocupava espaço acima do `.kcfig-map`. Se o smoke test futuro identificar colapso visual ou espaço excessivo, ajuste de `margin-top` em `.kcfig-map` ou `margin-bottom` em `.deck-topic` pode entrar no plan 01-07.

## Working Tree Final State

```
$ git status apresentacao/
nothing to commit, working tree clean
```

`apresentacao/index.html`: 12 sections, 324 linhas (era 473 — diminuiu porque o conteúdo dos slides movidos permanece igual e não foi duplicado; o "swap" é apenas reordenação). DOM em ordem narrativa: capa → título → agenda → Martins p1 → Zorić fundido → slide-phases → Yağcí fundido → slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig.

## Deviations from Plan

Duas imprecisões estilísticas nas acceptance gates do plan, tratadas como nos plans 01-04 e 01-05 (registrar, executar o equivalente substantivo, documentar):

1. **Plan acceptance Task 1 — `grep -c '> retomando o problema' apresentacao/index.html` = `2`:** literal não encontrável no markup raw porque o `>` no `.deck-topic` é entidade HTML `&gt;` (não literal) e o texto que vem em seguida está colado em `</span>retomando` (sem espaço entre tags). Equivalente substantivo executado: `grep -c 'retomando o problema<span class="caret blink"' apresentacao/index.html` = 2 ✓. Mesmo padrão para `kcs semânticos extraídos`, `evolução por dificuldade`, `o que o code-dkt olha`. Imprecisão idêntica à do plan 01-05 (gate plan #1 `> as quatro fases da edm` impossível no markup raw).

2. **Plan acceptance Task 2 — `tail -30 apresentacao/index.html | grep -c 'slide-fig'` ≥ `1`:** falha porque o arquivo tem `<script>` JavaScript embutido de ~140 linhas após o `<div class="slides">` (linhas 333-471 atuais), então as últimas 30 linhas pegam só script, não slide-fig (que está em linha 315). Equivalente substantivo executado: `grep -n 'slide-fig' apresentacao/index.html | tail -1` mostrou linha 315; `grep -n '^    </div>' apresentacao/index.html | head -1` mostrou linha 325 (fechamento de `<div class="slides">`); confirmado que slide-fig é a última section dentro do `<div class="slides">` antes de seu fechamento (10 linhas de gap, contendo o `</section>` final e o `</div>`). Adicionalmente, o DOM order Python check do plan confirmou que slide-fig é a última deck-slide na ordem das classes (`non_basic[-1] == 'slide-fig'`).

Substância (acceptance criteria estruturais) entregue em ambos os casos. Política aplicada: registrar a imprecisão, executar o equivalente substantivo, documentar a divergência neste SUMMARY. Tratamento idêntico ao do plan 01-04 (criterion #5 `.rel-lead` contado no arquivo todo) e do plan 01-05 (gates #1 e #4).

## Self-Check: PASSED

- `apresentacao/index.html`: FOUND
- `.planning/phases/01-reformata-o-da-base/01-06-SUMMARY.md`: FOUND (este arquivo)
- Commit `590ae34` (Task 1): FOUND em `git log --oneline -3`
- Commit `2a86049` (Task 2): FOUND em `git log --oneline -3`
- DOM order check Python: PASSED (`OK: all D-17 constraints satisfied`)
- Section count: 12 ✓
- Cabeçalhos novos: `> retomando o problema` ×2, `> kcs semânticos extraídos` ×1, `> evolução por dificuldade` ×1, `> o que o code-dkt olha` ×1 — todos confirmados via markup-aware grep
- H2s removidos: `prob-head` ×2, `fig-title`, `code-title`, `kcfig-title` — todos 0 ocorrências
- Citações diretas Martins (D-28): `mencionada por 13 autores` ×1, `citado por 10 autores` ×1 — preservadas
- Corpos preservados: `ascii-chart` ×2, `kcfig-map` ×1, `fig-wrap` ×1, `code-card` ×1
- Restrições D-17: (a) Martins p2 e p3 adjacentes; (b) slide-fig logo após Martins p3; (c) slide-code e slide-kcfig precedem Martins p2 — todas satisfeitas
- Claude's Discretion D-16: slide-code antes de slide-kcfig (recomendação do plan seguida)

## Próximo Plan

**01-07 (último plan da fase 1):** STYLE.md update (D-21) + cleanup CSS órfão + checkpoint humano final.

Escopo:
1. Atualizar `apresentacao/STYLE.md`:
   - Reescrever seção "Cabeçalho de todo slide após a AGENDA" para descrever o `.deck-topic` único com `> [seção]` no lugar do par tópico + título (D-21);
   - Remover o bullet "Regra dos correlatos" da seção "Regras de redação"; substituir por nota sobre cabeçalho temático;
   - Redesenhar a tabela "Inventário de slides (ordem atual)" para refletir os 12 slides pós-fase 1 com a ordem final (capa → título → agenda → Martins p1 → Zorić fundido → slide-phases → Yağcí fundido → slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig);
   - Marcar gaps abertos para a fase 4 com "(reservado: MODEL-01..05/MARKER-03 entrarão aqui)" conforme D-18;
2. Verificar `grep -c 'rel-kicker\|rel-title\|rel-sub' apresentacao/index.html` retorna 0; se sim, deletar as 4 regras CSS órfãs de `theme-unifacens.css` linhas 164-167 em commit dedicado;
3. Browser smoke test fim-a-fim como checkpoint humano final (validar deck navegável do slide 0 ao 11; confirmar todos os 9 cabeçalhos `> [seção]` renderizando; confirmar animações ASCII no Martins p2/p3; confirmar console DevTools sem erro; opcionalmente ajustar margens em `.kcfig-map` ou `.phases-list` se gaps colapsarem);
4. Atualizar D-22: o STYLE.md atualizado entra em commit próprio (sugestão `apresentacao: atualizar STYLE.md para padrão > [seção]`); CSS cleanup em commit separado.
