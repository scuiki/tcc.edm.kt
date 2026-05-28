# Phase 4: Modelagem e Avaliação (Fase 3 EDM) — Pattern Map

**Mapped:** 2026-05-28
**Files analyzed:** 1 modificado (`apresentacao/index.html`) + 4 slides novos + 4 reaproveitados + 4 PNGs temporários CLOSE-03
**Analogs found:** 4 / 4 slides novos (todos com âncora exata localizada no `index.html` atual; todos os componentes CSS pré-existentes)

## File Classification

Todos os artefatos desta fase são `<section>` inseridas no mesmo arquivo. Não há "files" no sentido tradicional; o vetor de mudança é sempre `apresentacao/index.html`.

| Slide novo / modificado | Role | Data Flow | Análogo `<section>` no `index.html` | Match Quality |
|-------------------------|------|-----------|-------------------------------------|---------------|
| MODEL-01 `> como o code-dkt funciona` | slide-related (prosa + cronologia + 2 colunas + SVG inset) | static markup (composição visual; sem dados externos no DOM) | Yağcı (`#/6`, L135-147, `.slide-related.slide-bridge` com `.bridge-seq` 3 chips) + INTRO-03a (`#/7`, L150-164, 2 cols texto/figura) | role-match (compõe 2 análogos) |
| MODEL-04 `> code-dkt no csedm` | slide-related (tabela ABNT `.eda-grid`) | static markup (transcrição numérica) | EDA-01 (`#/11`, L246-271, `.eda-grid` 5 linhas × 5 colunas) | exact |
| MODEL-05 `> extração automática de kcs` | slide-related (prosa curta + pipeline horizontal 5 caixas + fechamento) | static markup (composição visual) | Yağcí (`#/6`, L135-147, `.bridge-seq` 3 caixas — extensão para 5) | role-match (pipeline horizontal, mas precisa estender) |
| MARKER-03 (sem temático) | slide-marker--phase3 (puro reuso) | static markup (4 deltas mecânicos) | MARKER-02 (`#/15`, L332-375, `.slide-marker.slide-marker--phase2`) | exact (copy-paste com 4 deltas) |
| MODEL-03 (slide-code reaproveitado, `#/16`→`#/17`) | slide-code | nenhuma alteração | (próprio slide-code, L377-426) | reaproveitamento puro |
| slide-kcfig (saída de MODEL-05, `#/17`→`#/20`) | slide-kcfig | nenhuma alteração | (próprio slide-kcfig, L428-494) | reaproveitamento puro |
| CLOSE-01 Martins p2 (`#/18`→`#/21`) | slide-problem | nenhuma alteração | (próprio slide, L496-517) | reaproveitamento puro |
| CLOSE-02 Martins p3 (`#/19`→`#/22`) | slide-problem | nenhuma alteração | (próprio slide, L519-538) | reaproveitamento puro |
| CLOSE-03 slide-fig (`#/20`→`#/23`) | slide-fig | swap de `<img src>` + comentário | (próprio slide, L540-551) | reaproveitamento + 4 candidatos transitórios |

## Pattern Assignments

### Plan 1 — MARKER-03 (slide marker, sem temático)

**Arquivo modificado:** `apresentacao/index.html`
**Ponto de inserção:** APÓS o fechamento `</section>` do slide-fig (CLOSE-03, hoje L551, pós-fase ficará L551+`); colocar IMEDIATAMENTE antes do `</div></div>` (linhas 553-554) que fecha `.slides` / `.reveal`. Cabeçalho de comentário recomendado:
```html
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 3 concluida (Zoric, 2020) ============ -->
```

**Análogo principal:** `apresentacao/index.html` L332-375 — slide MARKER-02 (`<section><div class="deck-slide slide-marker slide-marker--phase2">…</div></section>`).

**Snippet HTML completo do análogo (MARKER-02, base de cópia copy-paste):**

```html
<!-- Source: apresentacao/index.html L332-375 (MARKER-02) -->
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase2">                <!-- DELTA 1: phase2 -> phase3 -->
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="marker-title"><span class="ps1">&gt;</span>AS QUATRO FASES DA EDM<span class="caret blink"></span></p>

    <div class="marker-track">
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Definição do Problema</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Preparação dos Dados</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--running">                       <!-- DELTA 2: running -> done -->
          <span class="marker-pill-icon">&#x21BB;</span>                     <!-- DELTA 2: &#x21BB; -> &check; -->
          <span class="marker-pill-name">Modelagem e Avaliação</span>
        </div>
        <span class="marker-badge">[running]</span>                           <!-- DELTA 2: [running] -> [done] -->
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--pending">                        <!-- DELTA 3: pending -> running -->
          <span class="marker-pill-icon">&#x25CB;</span>                      <!-- DELTA 3: &#x25CB; -> &#x21BB; -->
          <span class="marker-pill-name">Implantação</span>
        </div>
        <span class="marker-badge marker-badge--empty">[]</span>              <!-- DELTA 4: --empty + [] -> remover --empty + [running] -->
      </div>
    </div>

    <p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

**O que MUDA no MARKER-03 (4 deltas mecânicos, D-84b):**

| # | Onde | MARKER-02 (atual) | MARKER-03 (alvo) |
|---|------|------------------|-------------------|
| 1 | classe da `.deck-slide` (L334) | `slide-marker slide-marker--phase2` | `slide-marker slide-marker--phase3` |
| 2a | classe pill 3 (Modelagem) (L357) | `marker-pill marker-pill--running` | `marker-pill marker-pill--done` |
| 2b | ícone pill 3 (L358) | `&#x21BB;` (reload) | `&check;` |
| 2c | badge pill 3 (L361) | `[running]` | `[done]` |
| 3a | classe pill 4 (Implantação) (L365) | `marker-pill marker-pill--pending` | `marker-pill marker-pill--running` |
| 3b | ícone pill 4 (L366) | `&#x25CB;` (círculo vazio) | `&#x21BB;` (reload) |
| 3c | classe da badge pill 4 (L369) | `marker-badge marker-badge--empty` | `marker-badge` (remover `--empty`) |
| 3d | texto da badge pill 4 (L369) | `[]` | `[running]` |
| 4 | comentário HTML acima da `<section>` | "fase 2 concluida" | "fase 3 concluida" |

**O que NÃO muda:**
- `<section data-background-color="#F1F6FB">` (idêntico em todos os markers)
- `<svg class="wm">` com `viewBox="0 0 136.7 139.78"` (marca d'água Facens; herdada de TODOS os slides de conteúdo)
- `.marker-title` `> AS QUATRO FASES DA EDM` em maiúsculas com caret (D-84c — `.marker-title` define `text-transform` na CSS L380; o texto literal é caixa alta)
- Pills 1 (Definição) e 2 (Preparação): ambas `--done` + `&check;` + `[done]` idênticas a MARKER-02
- 3 `<span class="marker-arrow">&rarr;</span>` entre as 4 stages
- `<p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>` (idêntico a MARKER-01/02)

**Componentes CSS envolvidos (`apresentacao/assets/theme-unifacens.css`, todos read-only):**
- L368-373 `.slide-marker` (container; flex column, padding 52px 64px 40px)
- L374 `.slide-marker .wm` (marca d'água absoluta)
- L376-382 `.marker-title` + `.marker-title .ps1` (cabeçalho em caixa alta letterspacing 0.02em)
- L384-387 `.marker-track` (flex row, gap 14px, max-width 1180px)
- L388-391 `.marker-stage` (flex column, gap 8px)
- L392-409 `.marker-pill` + `.marker-pill-icon` + `.marker-pill-name` (retângulo branco, borda 1.5px, fonte Arial 17px)
- **L411-416 `.marker-pill--done .marker-pill-icon`** (check branco em círculo azul preenchido) — **chave do DELTA 2**
- **L418-423 `.marker-pill--running .marker-pill-icon`** (reload azul girando, `animation: marker-spin 2.4s linear infinite`) — **chave do DELTA 3**
- L426-432 `.marker-pill--pending` + `.marker-pill--pending .marker-pill-icon` (cinza)
- L434-438 `.marker-arrow` (seta preta, font-size 26px, margin-top 32px)
- L440-444 `.marker-badge` (Cascadia mono 14px, cor `--uni-blue`)
- **L445 `.marker-badge--empty { visibility: hidden; }`** — chave do DELTA 4 (remover essa classe faz a badge `[running]` da pill 4 ficar visível)
- L447-450 `@keyframes marker-spin` (rotação 360° contínua)
- L452 `.slide-marker .rel-cite` (Fonte em Arial 18px cinza)

**Zero CSS novo.** Validação visual (D-91): pill 4 deve aparecer com reload girando e badge `[running]` azul Cascadia abaixo.

---

### Plan 2 — MODEL-04 (tabela ABNT `.eda-grid`)

**Arquivo modificado:** `apresentacao/index.html`
**Ponto de inserção:** APÓS o fechamento `</section>` do slide-code (atualmente L426, será `#/17` após inserir MODEL-01); ANTES da `<section>` do slide-kcfig (atualmente L428). Cabeçalho de comentário recomendado:
```html
<!-- ============ SLIDE · MODEL-04 · Code-DKT no CSEDM, resultados vs Shi (multirun 10 seeds; Shi et al., 2022 Tab. 2) ============ -->
```

**Análogo principal:** `apresentacao/index.html` L246-271 — slide EDA-01 (`<section><div class="deck-slide slide-related">…<table class="eda-grid">…`).

**Snippet HTML completo do análogo (EDA-01):**

```html
<!-- Source: apresentacao/index.html L246-271 (EDA-01) -->
<!-- ============ SLIDE · EDA-01 · Como navegamos o CSEDM (Spring 2019) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>como navegamos o csedm<span class="caret blink"></span></p>

    <p class="rel-lead">Ao navegar o CSEDM, observamos como a participação e a taxa de acerto se distribuem entre os 5 <i>assignments</i> do curso.</p>

    <p class="eda-title">Tabela 1 &ndash; Taxa de acerto por <i>assignment</i> (Spring 2019)</p>

    <table class="eda-grid">
      <thead>
        <tr><th>Assignment</th><th>Alunos</th><th>Participação</th><th>Problemas</th><th>Taxa de acerto</th></tr>
      </thead>
      <tbody>
        <tr><td>A1 (439)</td><td>386</td><td>93,46%</td><td>10</td><td>26,15%</td></tr>
        <tr><td>A2 (487)</td><td>340</td><td>82,32%</td><td>10</td><td>20,06%</td></tr>
        <tr><td>A3 (492)</td><td>361</td><td>87,41%</td><td>10</td><td>20,34%</td></tr>
        <tr><td>A4 (494)</td><td>315</td><td>76,27%</td><td>10</td><td>24,72%</td></tr>
        <tr><td>A5 (502)</td><td>306</td><td>74,09%</td><td>10</td><td>30,62%</td></tr>
      </tbody>
    </table>

    <p class="eda-source">Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).</p>
  </div>
</section>
```

**O que MUDA em MODEL-04:**

| Onde | EDA-01 (análogo) | MODEL-04 (alvo) |
|------|------------------|------------------|
| comentário | `EDA-01 · Como navegamos…` | `MODEL-04 · Code-DKT no CSEDM…` |
| `.deck-topic` texto | `como navegamos o csedm` | `code-dkt no csedm` (D-78a) |
| `.rel-lead` (intro) | Texto sobre participação/taxa | "Comparamos os três modelos por <i>assignment</i> no <i>test set</i> do CSEDM Spring 2019; números são médias sobre 10 seeds." (rascunho D-78b/g; ajustável no checkpoint) |
| `.eda-title` | `Tabela 1 &ndash; Taxa de acerto por <i>assignment</i> (Spring 2019)` | `Tabela 2 &ndash; <i>First-attempt</i> AUC por modelo e <i>assignment</i> (%)` |
| `<thead>` columns | `Assignment / Alunos / Participação / Problemas / Taxa de acerto` (5) | `Modelo / A439 / A487 / A492 / A494 / A502` (6) |
| `<tbody>` linhas | 5 linhas (A1-A5) | 4 linhas: BKT, DKT, Code-DKT, Shi (2022)* (D-78b/g) |
| números | acerto por assignment | first-attempt AUC × modelo × assignment; **vírgula decimal pt-BR** (D-78g, Pitfall 8) |
| linha Shi com en-dashes | n/a | `<tr><td>Shi (2022)*</td><td>75,74</td><td>&ndash;</td><td>&ndash;</td><td>&ndash;</td><td>&ndash;</td></tr>` (Pitfall 1) |
| caption extra (entre tabela e Fonte) | (não existe em EDA-01) | adicionar `<p class="rel-lead" style="font-size:18px;margin-top:12px;"><i>* Paper Shi reporta apenas A1, equivalente a A439.</i> <i>First-attempt</i> AUC é a métrica primária: mede transferência entre problemas e evita autocorrelação intra-problema (Shi <i>et al.</i>, 2022, §5).</p>` (D-78d) |
| `.eda-source` (Fonte:) | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` | `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.` (D-78f) |

**Números travados (D-78g, `results/comparison_table_first_auc.md`):**

| Modelo | A439 | A487 | A492 | A494 | A502 |
|--------|------|------|------|------|------|
| BKT | 63,21 | 68,40 | 54,20 | 57,81 | 56,92 |
| DKT | 75,56 | 76,70 | 82,05 | 80,17 | 80,78 |
| Code-DKT | **73,27** | 79,56 | 86,12 | 81,85 | 84,98 |
| Shi (2022)* | 75,74 | – | – | – | – |

**Investigação sobre células vazias na `.eda-grid`:** EDA-01 e EDA-02 NÃO têm células vazias hoje. CSS L483-484 não impõe nenhuma regra especial para células vazias; `&ndash;` (en-dash HTML) renderiza centrado como qualquer outro `<td>`. Conferir que `.eda-grid tr td:last-child { color: var(--uni-blue); font-weight: 700; }` (L484) destaca apenas a última coluna (A502). Para a linha Shi com 4 en-dashes nas colunas A487-A502, A502 ficará em azul. Visualmente aceitável (não conflita com mensagem; en-dash em azul ainda lê como "não publicado").

**O que NÃO muda:**
- `<section data-background-color="#F1F6FB">` + `<div class="deck-slide slide-related">` + `<svg class="wm">` (padrão de todos os slides de conteúdo)
- estrutura `.deck-topic > .ps1 + texto + .caret.blink`
- estrutura `.eda-title` (acima) + `.eda-grid` (corpo) + `.eda-source` (abaixo)
- nome `slide-related` como classe principal (EDA-02 também usa, é o padrão fase 3)

**Componentes CSS envolvidos:**
- L42-43 `.deck-topic` + `.deck-topic .ps1`
- L45-50 `.caret` + `.caret.blink`
- L460-465 `.eda-title` (Arial bold 18px centralizado)
- L466-473 `.eda-grid` (3 bordas horizontais: topo, bottom-header, base; sem verticais; Arial 20px)
- L474-478 `.eda-grid th, .eda-grid td` (padding 9px 18px, centralizado)
- L479-482 `.eda-grid th` (border-bottom 1.5px)
- L483 `.eda-grid td`
- **L484 `.eda-grid tr td:last-child` (última coluna em azul UniFacens, font-weight 700)** — destaca A502; aceitar por padrão (não há decisão D-78 pedindo destaque per-célula)
- L485-490 `.eda-source` (Arial 14px cinza centralizado)
- L156-... `.rel-lead` (Arial 22-23px justified; usado tanto para intro quanto para caption — inline style `font-size:18px` reduz para caption discreto)

---

### Plan 3 — MODEL-01 (cronologia 3 chips + 2 colunas com AST inset)

**Arquivo modificado:** `apresentacao/index.html`
**Asset adicional:** copiar `docs/figures/ast_codedkt_ptbr.svg` para `apresentacao/assets/ast_codedkt_ptbr.svg` (Pitfall 6: path relativo `../docs/figures/` quebra com `python3 -m http.server` rodado em `apresentacao/`).
**Ponto de inserção:** APÓS o fechamento `</section>` do MARKER-02 (atualmente L375); ANTES da `<section>` do slide-code (atualmente L379). Cabeçalho recomendado:
```html
<!-- ============ SLIDE · MODEL-01 · Como o Code-DKT funciona (cronologia BKT->DKT->Code-DKT; AST inset; Shi et al., 2022) ============ -->
```

**Análogo principal (cronologia 3 chips):** `apresentacao/index.html` L135-147 — slide Yağcí (`<section><div class="deck-slide slide-related slide-bridge">…<p class="bridge-seq">…`).

**Snippet HTML completo do análogo Yağcí:**

```html
<!-- Source: apresentacao/index.html L135-147 (Yağcí, slide-bridge) -->
<!-- ============ SLIDE · Da EDM ao knowledge tracing (Yağcı, 2022) — fusão p1+p2 ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>da edm ao knowledge tracing<span class="caret blink"></span></p>

    <p class="rel-lead">Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar estudantes em risco. Nos dispomos a trabalhar de forma similar, mas em vez de uma previsão única ao fim do curso, <b>acompanhamos o conhecimento ao longo do tempo</b>, levando em conta cada tentativa feita durante a resolução do problema, via <i>knowledge tracing</i>.</p>

    <p class="bridge-seq"><span class="step">mineração de dados educacionais</span><span class="arr">&rarr;</span><span class="step">predição de desempenho</span><span class="arr">&rarr;</span><span class="step"><i>knowledge tracing</i></span></p>

    <p class="rel-cite">Fonte: Yağcı (2022).</p>
  </div>
</section>
```

**Análogo secundário (slide com prosa 2 colunas, mesmo template `slide-related`):** L150-164 INTRO-03a — múltiplos `<p class="rel-lead">` empilhados; layout flex/grid de duas colunas com figura à direita ainda NÃO foi usado em fase anterior, então **MODEL-01 inaugura o padrão de 2 colunas inline-styled dentro do `slide-related`**.

**Snippet HTML completo de INTRO-03a (estrutura prosa-pura, sem grid):**

```html
<!-- Source: apresentacao/index.html L150-164 (INTRO-03a) -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>o problema do kt binário<span class="caret blink"></span></p>

    <p class="rel-lead">Modelos de <i>knowledge tracing</i> estimam, a partir do histórico de tentativas, a probabilidade de um estudante acertar o próximo problema. ...</p>

    <p class="rel-lead">Shi <i>et al.</i> (2022) apontam que a maioria desses modelos, incluindo <b>BKT</b> e <b>DKT</b>, ...</p>

    <p class="rel-lead">Daí a necessidade de modelos voltados a áreas com respostas estruturadas ...</p>

    <p class="rel-cite">Fonte: Shi <i>et al.</i> (2022).</p>
  </div>
</section>
```

**O que MUDA / é composto em MODEL-01:**

| Onde | Origem | MODEL-01 (alvo) |
|------|--------|------------------|
| comentário | n/a | `<!-- MODEL-01 · Como o Code-DKT funciona -->` |
| `.deck-topic` texto | Yağcí | `como o code-dkt funciona` (D-77a) |
| Cronologia 3 chips | Yağcí (`.bridge-seq` 3 steps) | mesmo `.bridge-seq` com `<b>nome do modelo</b> (ano)<br><span style="font-size:16px;">descrição</span>` em cada `.step` (D-77b) |
| Body 2 colunas | n/a (composição nova) | `<div style="display: grid; grid-template-columns: 1fr 0.85fr; gap: 32px; margin-top: 28px;">…texto…SVG inset…</div>` |
| Texto coluna esquerda | n/a | 1 `.rel-lead` (frase contexto) + `<ul>` com 4 bullets (D-77c) |
| Coluna direita | n/a | `<img src="assets/ast_codedkt_ptbr.svg" alt="..." style="width:100%;max-width:420px;height:auto;">` (D-77d; viewBox SVG = 560×620, escala automática) |
| Rodapé | Yağcí (`Fonte: Yağcı (2022).`) | `<p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>` (D-77e) |

**Estrutura sugerida (RESEARCH Pattern 3):**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>como o code-dkt funciona<span class="caret blink"></span></p>

    <p class="bridge-seq" style="margin-top: 24px;">
      <span class="step"><b>BKT</b> (1995)<br><span style="font-size: 16px;">Bayes &middot; habilidades por KC</span></span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>DKT</b> (2015)<br><span style="font-size: 16px;">RNN &middot; histórico sequencial</span></span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>Code-DKT</b> (2022)<br><span style="font-size: 16px;">RNN + paths AST &middot; <i>code2vec</i></span></span>
    </p>

    <div style="display: grid; grid-template-columns: 1fr 0.85fr; gap: 32px; margin-top: 28px;">
      <div>
        <p class="rel-lead" style="margin: 0;">O Code-DKT incorpora o conteúdo do código que o DKT ignorava, mantendo o <i>tracing</i> sequencial.</p>
        <ul style="font-family: Arial; font-size: 21px; margin-top: 18px; padding-left: 22px; line-height: 1.55;">
          <li><code>javalang</code> &rarr; AST</li>
          <li><i>code2vec</i> &rarr; caminhos folha-a-folha</li>
          <li>atenção pondera os caminhos</li>
          <li>LSTM combina com (<code>ProblemID</code>, acerto/erro)</li>
        </ul>
      </div>
      <div style="display: flex; align-items: center; justify-content: center;">
        <img src="assets/ast_codedkt_ptbr.svg" alt="AST com um caminho folha-a-folha entre input e &quot;valor&quot;" style="width: 100%; max-width: 420px; height: auto;">
      </div>
    </div>

    <p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
  </div>
</section>
```

**Risco-chave (Pitfall 6 + A2):** `<img src="../docs/figures/ast_codedkt_ptbr.svg">` quebra porque `python3 -m http.server` em `apresentacao/` não serve `..`. **Solução obrigatória no plan:** `cp docs/figures/ast_codedkt_ptbr.svg apresentacao/assets/ast_codedkt_ptbr.svg` antes/durante a inserção; usar `src="assets/ast_codedkt_ptbr.svg"`.

**O que NÃO muda:**
- `<section data-background-color="#F1F6FB">` + `.deck-slide slide-related` + `<svg class="wm">`
- estrutura `.deck-topic` (cabeçalho `> [seção]` com caret)
- componente `.bridge-seq` (Yağcí) reaproveitado com 3 chips (dentro do limite testado — sem risco visual)
- componente `.rel-lead` + `.rel-cite` (mesma família dos slides EDA da fase 3)

**Componentes CSS envolvidos:**
- L42-50 `.deck-topic` + `.caret.blink`
- L197-210 `.slide-bridge .bridge-seq` + `.step` + `.arr` (Yağcí; **MODEL-01 herda da mesma class `.slide-bridge` SE precisar acessar a regra `.slide-bridge .bridge-seq`** — risco: regra está aninhada em `.slide-bridge`; testar se `.bridge-seq` solta dentro de `.slide-related` ganha estilo. Verificação cruzada: Yağcí declara `<div class="deck-slide slide-related slide-bridge">`; INTRO-03a declara só `slide-related`. **Recomendação MODEL-01: usar `<div class="deck-slide slide-related slide-bridge">` para herdar a regra `.slide-bridge .bridge-seq`**, evitando que o flex layout caia em texto inline). Isto fecha o pattern.
- `.rel-lead` (Arial 22-23px) usado para o contexto à esquerda
- `.rel-cite` (Arial 18px cinza) usado para `Fonte:`
- Grid 2 colunas via inline-style (sem nova classe CSS; consistente com "zero CSS novo" exceto fallback)

**Decisão de class explícita para MODEL-01:** `<div class="deck-slide slide-related slide-bridge">` (para acessar regras `.slide-bridge .bridge-seq`).

---

### Plan 4 — MODEL-05 (pipeline 5 etapas + frases sandwich)

**Arquivo modificado:** `apresentacao/index.html`
**Ponto de inserção:** APÓS o fechamento `</section>` do slide-code (atualmente L426, será `#/17` após MODEL-01); APÓS MODEL-04 (Plan 2); ANTES da `<section>` do slide-kcfig (atualmente L428). Cabeçalho:
```html
<!-- ============ SLIDE · MODEL-05 · Extração automática de KCs (pipeline 5 etapas; Duan et al., 2025) ============ -->
```

**Análogo principal:** `apresentacao/index.html` L135-147 — slide Yağcí (mesma base do MODEL-01; pipeline horizontal `.bridge-seq` estendido de 3 para **5 caixas + 4 setas**).

**Snippet HTML completo de Yağcí** (já mostrado em Plan 3 acima).

**O que MUDA em MODEL-05:**

| Onde | Yağcí (análogo) | MODEL-05 (alvo) |
|------|------------------|------------------|
| comentário | Yağcí | `<!-- MODEL-05 · Extração automática de KCs -->` |
| `.deck-topic` texto | `da edm ao knowledge tracing` | `extração automática de kcs` (D-79a) |
| `.rel-lead` (abertura) | 1 parágrafo longo Yağcı | "Construímos um <i>pipeline</i> de cinco etapas para extrair <i>Knowledge Components</i> do CSEDM." (D-79c) |
| `.bridge-seq` chips | 3 caixas + 2 setas | **5 caixas + 4 setas** (D-79d) — estendido |
| Conteúdo de cada chip | 1 texto curto | `<b>verbo</b><br>descrição curta` (2 linhas, calibração tipográfica Pitfall 7) |
| `.rel-lead` (fechamento) | n/a | "A decisão-chave foi alimentar o LLM com código bruto, não AST (Duan <i>et al.</i>, 2025, Tab. 4)." (D-79e) |
| `.rel-cite` (Fonte) | `Fonte: Yağcı (2022).` | `Fonte: adaptado de Duan <i>et al.</i> (2025).` (D-79h) |

**Estrutura sugerida (RESEARCH Pattern 4):**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>extração automática de kcs<span class="caret blink"></span></p>

    <p class="rel-lead">Construímos um <i>pipeline</i> de cinco etapas para extrair <i>Knowledge Components</i> do CSEDM.</p>

    <p class="bridge-seq" style="margin-top: 28px; font-size: 17px;">
      <span class="step"><b>Sampling</b><br>n=5/problema</span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>LLM</b><br>KCs brutos</span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>Clustering</b><br>Sentence-BERT + HAC</span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>Rotulagem</b><br>LLM nos clusters</span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>Q-matrix</b><br>por <i>assignment</i></span>
    </p>

    <p class="rel-lead" style="margin-top: 28px;">A decisão-chave foi alimentar o LLM com código bruto, não AST (Duan <i>et al.</i>, 2025, Tab. 4).</p>

    <p class="rel-cite">Fonte: adaptado de Duan <i>et al.</i> (2025).</p>
  </div>
</section>
```

**Caixa 5 (revisão D-79d-rev confirmada 2026-05-28):** rótulo "Q-matrix / por assignment" SEM número. O número "28 KCs" do D-79d original NÃO tem origem documentada (Pitfall 5 + Open Question 1; Q-matrices reais têm 12-15 KCs/ass.; slide-kcfig mostra 17 agregados por dificuldade). Manter sem número evita inconsistência narrativa MODEL-05 → slide-kcfig.

**Risco-chave (Pitfall 7 + A1):** 5 caixas em 1280px com `.bridge-seq` testado para 3. Cálculo: ~218px/caixa após padding e setas. **Mitigação obrigatória no plan:**
1. inline-style `font-size: 17px` na `.bridge-seq` (vs 19px do CSS L202)
2. cada `.step` com 2 linhas (`<br>` entre verbo bold e descrição)
3. encurtar para ≤ 18 caracteres por linha
4. **Último recurso (não default):** criar classe `.chrono-step` ou modificadora `.bridge-seq--narrow` em `theme-unifacens.css`. Apenas se browser confirmar quebra de layout no checkpoint.

**Quantidade de caixas no Yağcí analog:** verificado L143 — `.bridge-seq` Yağcí tem **3 `.step` + 2 `.arr`** ("mineração de dados educacionais" → "predição de desempenho" → "knowledge tracing"). MODEL-05 estende para **5 `.step` + 4 `.arr`** (mais 2 chips e 2 setas).

**O que NÃO muda:**
- `<section data-background-color="#F1F6FB">` + `.deck-slide slide-related slide-bridge`
- `.deck-topic` + `.caret.blink`
- componente `.bridge-seq` (regra CSS L197-210, herdada de `.slide-bridge`)
- `.rel-lead` (abertura e fechamento) — mesma classe usada em Yağcí, INTRO-03a, EDA-02
- `.rel-cite` (Fonte)

**Componentes CSS envolvidos:**
- L42-50 `.deck-topic` + `.caret.blink`
- **L197-210 `.slide-bridge .bridge-seq` + `.step` + `.arr`** (Yağcí; usar `<div class="deck-slide slide-related slide-bridge">` para herdar)
- `.rel-lead` (Arial 22-23px justified)
- `.rel-cite` (Arial 18px cinza)

**Decisão de class explícita para MODEL-05:** `<div class="deck-slide slide-related slide-bridge">` (mesma chamada de MODEL-01, para herdar regra `.slide-bridge .bridge-seq`).

---

### Slides REAPROVEITADOS (Plans 0 / não-plans desta fase)

#### MODEL-03 = slide-code (`#/16` → `#/17`)

- **Cobertura:** D-80 (CONTEXT) + D-10 (fase 1) + D-16/D-17 (fase 1)
- **Mudança nesta fase:** nenhuma alteração de conteúdo. Posição física no `index.html` (linhas) muda automaticamente quando MODEL-01 é inserido acima; índice reveal `#/17` (era `#/16`).
- **Snippet existente:** L377-426 do `index.html` (intacto; classe `.slide-code`; cabeçalho `> o que o code-dkt olha`; código `dateFashion` com atenção no `&&`; rodapé "Fonte: elaborado pelos autores (Code-DKT, Shi <i>et al.</i>, 2022; ...)").
- **Ação no plan:** **nenhuma**. Não tocar.

#### slide-kcfig (saída visual de MODEL-05; `#/17` → `#/20`)

- **Cobertura:** D-79i (CONTEXT) — MODEL-05 NÃO duplica os 28/17 KCs. slide-kcfig já mostra os KCs.
- **Snippet existente:** L428-494 do `index.html` (intacto; classe `.slide-kcfig`; cabeçalho `> kcs semânticos extraídos`; 17 KCs agrupados em 6 dificuldades Martins; rodapé "Fonte: elaborado pelos autores, com base em Duan <i>et al.</i> (2025) e Martins, Marin e Alves (2024).").
- **Ação no plan:** **nenhuma**. Não tocar.

#### CLOSE-01 = Martins p2 (`#/18` → `#/21`)

- **Cobertura:** D-82 (CONTEXT) — reformatado na fase 1 (commits `590ae34` e `2a86049`); citação direta literal mantida como exceção D-28 (argumento quantitativo: "13 autores").
- **Snippet existente:** L496-517 do `index.html` (intacto; classe `.slide-problem`; cabeçalho `> retomando o problema`; quote "(Martins; Marin; Alves, 2024, p. 19)"; ascii-chart `data-ascii` com 7 barras).
- **Ação no plan:** **nenhuma**. Não tocar. ROADMAP Success Criteria 5 explicita "MANTÊM citação direta atual".

#### CLOSE-02 = Martins p3 (`#/19` → `#/22`)

- **Cobertura:** D-82 (CONTEXT) — idem CLOSE-01 (10 autores, exceção quantitativa).
- **Snippet existente:** L519-538 do `index.html` (intacto; classe `.slide-problem`; cabeçalho `> retomando o problema`; quote "(Martins; Marin; Alves, 2024, p. 20)"; ascii-chart com 5 barras).
- **Ação no plan:** **nenhuma**. Não tocar.

#### CLOSE-03 = slide-fig (`#/20` → `#/23`) — pick visual transitório

- **Cobertura:** D-83 (CONTEXT) — PENDING-04 resolvido em D-83a (`codedkt_kc_retrained.pkl` existe; asset MD5 igual ao `results/fig_codedkt_curves_by_martins.png`).
- **Snippet existente:** L540-551 do `index.html`:

```html
<!-- Source: apresentacao/index.html L540-551 (slide-fig atual) -->
<!-- ============ SLIDE · Evolução por dificuldade · Curva Code-DKT (Code-DKT, Shi et al., 2022; Martins, Marin e Alves, 2024) ============ -->
<!-- figura: results/fig_codedkt_difficulty_martins.png (curvas de mastery prevista; oportunidade = problema distinto) -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-fig">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>evolução por dificuldade<span class="caret blink"></span></p>
    <div class="fig-wrap"><img src="assets/fig-codedkt-martins-curves.png" alt="Curvas de aprendizado do Code-DKT por sub-dificuldade de Martins"></div>
    <p class="fig-read"><b>Estruturas de controle</b> parte do nível mais baixo mas tem a maior inclinação (aprende rápido); <b>Vetores</b> e <b>Funções</b> ficam planos (mais difíceis de <i>aprender</i>).</p>
    <p class="fig-fonte">Fonte: elaborado pelos autores (Code-DKT, Shi <i>et al.</i>, 2022; dificuldades de Martins, Marin e Alves, 2024).</p>
  </div>
</section>
```

**Procedimento de pick visual (D-83c — Plan 5 / CLOSE-03):**

**Etapa A — inserção de 3 sections temporários (pré-checkpoint, total 28 sections transitório):**

1. Copiar os 3 PNGs ausentes em `apresentacao/assets/` (o 1º já está como `fig-codedkt-martins-curves.png`):
   ```bash
   cp results/fig_codedkt_difficulty_martins.png apresentacao/assets/fig-codedkt-difficulty.png
   cp results/fig_codedkt_kc_curves.png         apresentacao/assets/fig-codedkt-kc-curves.png
   cp results/fig_codedkt_level_vs_slope.png    apresentacao/assets/fig-codedkt-level-vs-slope.png
   ```
2. Inserir 3 `<section>` temporários LOGO APÓS o slide-fig atual (entre L551 e antes de MARKER-03), cada um com classe `slide-fig` e ID temporário `slide-fig-pick-N`. Estrutura:

```html
<!-- ============ SLIDE TEMP · CLOSE-03 pick · candidato 2 (fig-codedkt-difficulty) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-fig" id="slide-fig-pick-2">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>pick: difficulty_martins<span class="caret blink"></span></p>
    <div class="fig-wrap"><img src="assets/fig-codedkt-difficulty.png" alt="Candidato 2: difficulty_martins"></div>
    <p class="fig-read">[temporário; defere para checkpoint]</p>
    <p class="fig-fonte">[temporário] candidato 2</p>
  </div>
</section>

<!-- ============ SLIDE TEMP · CLOSE-03 pick · candidato 3 (fig-codedkt-kc-curves) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-fig" id="slide-fig-pick-3">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>pick: kc_curves (28 curvas)<span class="caret blink"></span></p>
    <div class="fig-wrap"><img src="assets/fig-codedkt-kc-curves.png" alt="Candidato 3: 28 curvas, uma por KC"></div>
    <p class="fig-read">[temporário; defere para checkpoint]</p>
    <p class="fig-fonte">[temporário] candidato 3</p>
  </div>
</section>

<!-- ============ SLIDE TEMP · CLOSE-03 pick · candidato 4 (fig-codedkt-level-vs-slope) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-fig" id="slide-fig-pick-4">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>pick: level_vs_slope (scatter)<span class="caret blink"></span></p>
    <div class="fig-wrap"><img src="assets/fig-codedkt-level-vs-slope.png" alt="Candidato 4: scatter nível × inclinação"></div>
    <p class="fig-read">[temporário; defere para checkpoint]</p>
    <p class="fig-fonte">[temporário] candidato 4</p>
  </div>
</section>
```

**Etapa B — checkpoint visual humano (browser):** usuário vê 4 versões consecutivas (atual + 3 temporários) e escolhe 1.

**Etapa C — limpeza (pós-checkpoint, volta a 25 sections):**

1. Remover os 3 `<section>` temporários NÃO escolhidos.
2. Se escolha ≠ candidato 1 (atual `curves_by_martins`):
   - trocar `<img src="assets/fig-codedkt-martins-curves.png">` no slide-fig original (L547) para o novo asset escolhido.
   - opcionalmente renomear o asset para um filename estável (mas D-83a registra que `assets/fig-codedkt-martins-curves.png` é a referência canônica; preferir manter o filename e sobrescrever o conteúdo via `cp results/<novo>.png apresentacao/assets/fig-codedkt-martins-curves.png`).
   - refrasear `<p class="fig-read">` conforme o conteúdo do novo PNG (D-83d defere).
3. **Fix mecânico do comentário L541 (independente da escolha):** trocar `<!-- figura: results/fig_codedkt_difficulty_martins.png ... -->` para apontar ao filename real (Pitfall 9). Se escolha = candidato 1 (mantém atual), comentário deve dizer `<!-- figura: results/fig_codedkt_curves_by_martins.png (= assets/fig-codedkt-martins-curves.png) -->`.

**4 PNGs candidatos disponíveis (verified 2026-05-28):**

| # | Arquivo `results/` | Tamanho | Asset alvo (se escolhido) | Conteúdo |
|---|--------------------|---------|---------------------------|----------|
| 1 | `fig_codedkt_curves_by_martins.png` | 145.673 B | `fig-codedkt-martins-curves.png` (já existe; MD5 idêntico) | curvas por dificuldade (atual no slide) |
| 2 | `fig_codedkt_difficulty_martins.png` | 95.266 B | `fig-codedkt-difficulty.png` (novo) | dificuldade média/oportunidade por bloco Martins |
| 3 | `fig_codedkt_kc_curves.png` | 186.582 B | `fig-codedkt-kc-curves.png` (novo) | 28 curvas, uma por KC |
| 4 | `fig_codedkt_level_vs_slope.png` | 132.890 B | `fig-codedkt-level-vs-slope.png` (novo) | scatter nível × inclinação |

**Componentes CSS envolvidos (CLOSE-03, todos pré-existentes):**
- `.slide-fig` (não inspecionado em detalhe; pré-existente)
- `.fig-wrap` (container do `<img>`)
- `.fig-read` (frase de leitura abaixo da figura)
- `.fig-fonte` (rodapé Fonte:)
- `.deck-topic`, `.caret.blink`, marca d'água `<svg class="wm">` — herdados

**Decisões deferidas no CLOSE-03:**
- D-83d: texto exato de `<p class="fig-read">` depende do PNG escolhido. Insight atual ("Estruturas de controle aprende rápido; Vetores e Funções ficam planos") é específico de `curves_by_martins`. Se trocar, refrasear no checkpoint.

---

## Shared Patterns

Padrões cross-cutting aplicados a TODOS os 4 slides novos (MODEL-01, MODEL-04, MODEL-05, MARKER-03).

### 1. Envelope do slide (`<section>` + `.deck-slide`)

**Source:** padrão em todos os 21 slides existentes (e.g. INTRO-01 L228-242 ou MARKER-02 L333-374).
**Apply to:** TODOS os 4 slides novos.

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-XYZ">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <!-- conteúdo do slide -->
  </div>
</section>
```

**Nota:** o reveal.js força `display: block` no `<section>`, por isso o layout fica em `.deck-slide` interno (STYLE.md L13-14).

### 2. Cabeçalho `> [seção]` com caret piscando (`.deck-topic`)

**Source:** `apresentacao/index.html` L233 (INTRO-01) e em todos os 18 slides de conteúdo pós-AGENDA.
**Apply to:** MODEL-01, MODEL-04, MODEL-05 (slide markers usam `.marker-title` que é variante).

```html
<p class="deck-topic"><span class="ps1">&gt;</span>[seção em minúsculas]<span class="caret blink"></span></p>
```

**Cabeçalhos travados desta fase:**
- MODEL-01: `como o code-dkt funciona` (D-77a)
- MODEL-04: `code-dkt no csedm` (D-78a)
- MODEL-05: `extração automática de kcs` (D-79a)
- MARKER-03: `AS QUATRO FASES DA EDM` (caixa alta via CSS `text-transform: uppercase` na `.marker-title` L380; literal em maiúsculas no markup também é aceito; espelhar MARKER-02)

**CSS envolvido:** L42-43 `.deck-topic` + `.deck-topic .ps1`; L45-50 `.caret.blink`.

### 3. Marca d'água Facens (`<svg class="wm">`)

**Source:** todos os 18 slides de conteúdo (e.g. L85 INTRO; L186 MARKER-01; L335 MARKER-02).
**Apply to:** TODOS os 4 slides novos. Idêntico em todos:

```html
<svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
```

O `<symbol id="sym">` está definido uma vez em L16-21 do `index.html`.

### 4. Rodapé `Fonte:` (`.rel-cite` ou `.eda-source` ou `.fig-fonte`)

**Source:** L162 INTRO-03a (`<p class="rel-cite">Fonte: Shi <i>et al.</i> (2022).</p>`); L269 EDA-01 (`<p class="eda-source">Fonte: ...</p>`); L549 CLOSE-03 (`<p class="fig-fonte">Fonte: ...</p>`).
**Apply to:** TODOS os 4 slides novos. Variantes por contexto:

| Slide | Classe | Texto |
|-------|--------|-------|
| MODEL-01 | `.rel-cite` | `Fonte: adaptado de Shi <i>et al.</i> (2022).` (D-77e) |
| MODEL-04 | `.eda-source` | `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.` (D-78f) |
| MODEL-05 | `.rel-cite` | `Fonte: adaptado de Duan <i>et al.</i> (2025).` (D-79h) |
| MARKER-03 | `.rel-cite` | `Fonte: adaptado de Zorić (2020).` (D-84c) |

### 5. Citações ABNT — `<i>et al.</i>` para 3+ autores

**Source:** D-54 fase 2 (normalizada em 8 ocorrências, commit `4a9af6e`); padrão consolidado em L91 INTRO (Martins <i>et al.</i>), L158 INTRO-03a (Shi <i>et al.</i>), L322 EDA-02, etc.
**Apply to:** MODEL-01 (Shi <i>et al.</i>), MODEL-04 (Shi <i>et al.</i>), MODEL-05 (Duan <i>et al.</i>). MARKER-03 cita "Zorić (2020)" — apenas 1 autor, sem `et al.`.

**Anti-pattern:** "Shi (2022)" sem `et al.` (Shi tem 5 autores); "Duan (2025)" sem `et al.` (Duan tem 7 autores).

### 6. Sem em-dash em prosa

**Source:** D-44 fase 1 + memória `feedback_no_em_dashes` + D-87 herdado.
**Apply to:** TODA a prosa nova nos 4 slides. Substituir por vírgula, dois-pontos ou parênteses.

**Anti-pattern:** `—` (em-dash) em `.rel-lead`, `<li>`, `.fig-read`, caption.

### 7. "Estudantes", nunca "alunos" em prosa nova

**Source:** D-67e fase 3 + memória `feedback_estudantes_nao_alunos` + D-89 herdado.
**Apply to:** MODEL-01, MODEL-04, MODEL-05 (prosa nova). MARKER-03 não tem prosa.

**Exceção:** citações diretas literais (CLOSE-01/02 preservam o termo original); fora de escopo desta fase.

### 8. Vírgula decimal pt-BR (`.eda-grid`)

**Source:** L261-265 EDA-01 (`23,68%`, `93,46%`); L324 EDA-02 (`23,68%`).
**Apply to:** MODEL-04 (única tabela com números).

**Anti-pattern:** `73.27%` ou `75.74%` (ponto decimal) — `results/comparison_table_first_auc.md` usa ponto; converter explicitamente na transcrição.

### 9. Termos estrangeiros em itálico minúsculas

**Source:** STYLE.md L86; D-46 fase 2; D-88 herdado.
**Apply to:** TODOS os slides com prosa.

| Termo | Markup |
|-------|--------|
| code2vec | `<i>code2vec</i>` |
| knowledge tracing | `<i>knowledge tracing</i>` |
| Knowledge Components | `<i>Knowledge Components</i>` |
| pipeline | `<i>pipeline</i>` |
| tracing | `<i>tracing</i>` |
| assignment | `<i>assignment</i>` |
| test set | `<i>test set</i>` |
| baseline | `<i>baseline</i>` |
| first-attempt | `<i>first-attempt</i>` (usado como adjetivo composto em "First-attempt AUC") |

**Não-itálico (nomes próprios e nomes de modelos):** BKT, DKT, Code-DKT, srcML-DKT, CSEDM, ProgSnap2, LSTM, RNN, Bayes, Sentence-BERT, HAC, AST, LLM, GPT-4o.

---

## No Analog Found

Não há slides novos sem análogo no codebase. Todos os 4 slides novos têm pelo menos um análogo de role e/ou data flow:

| Slide novo | Por que houve análogo |
|------------|-----------------------|
| MARKER-03 | MARKER-02 é cópia mecânica idêntica (4 deltas) |
| MODEL-04 | EDA-01 estabeleceu `.eda-grid` ABNT na fase 3 |
| MODEL-01 | Yağcí estabeleceu `.bridge-seq` (cronologia) e INTRO-03a estabeleceu o template `slide-related` |
| MODEL-05 | Yağcí estabeleceu `.bridge-seq` (pipeline horizontal); extensão para 5 caixas é o único risco |

**Risco médio único:** layout `.bridge-seq` com 5 caixas em 1280px não foi testado em browser ainda (Pitfall 7 / Assumption A1). Mitigação documentada: `font-size: 17px` + `<br>` + ≤18 chars/linha; criar `.chrono-step` em CSS apenas se quebrar.

---

## Metadata

**Analog search scope:**
- `apresentacao/index.html` (696 linhas, 21 sections pós-fase 3) — Read integral
- `apresentacao/assets/theme-unifacens.css` (521 linhas) — Read parcial (`.deck-topic`, `.bridge-seq`, `.slide-marker`, `.eda-grid`, `.eda-fig` confirmados)
- `apresentacao/STYLE.md` — Read integral

**Files scanned:** 3 (HTML + CSS + STYLE.md)
**Analogs identified:** 4 / 4 slides novos
**Components reused (zero CSS new expected):**
- `.deck-topic` + `.caret.blink` + `.ps1` (4/4 slides novos)
- `<svg class="wm">` (4/4)
- `.rel-cite` (3/4: MODEL-01, MODEL-05, MARKER-03)
- `.eda-source` (1/4: MODEL-04)
- `.rel-lead` (3/4: MODEL-01, MODEL-04 intro+caption, MODEL-05 abertura+fechamento)
- `.bridge-seq` + `.step` + `.arr` (2/4: MODEL-01 com 3 chips, MODEL-05 com 5 chips estendidos)
- `.eda-title` + `.eda-grid` (1/4: MODEL-04)
- `.slide-marker` + `.marker-track` + `.marker-stage` + `.marker-pill` + `.marker-pill-icon` + `.marker-pill-name` + `.marker-pill--done/--running/--pending` + `.marker-arrow` + `.marker-badge` + `.marker-title` + `@keyframes marker-spin` (1/4: MARKER-03)

**CSS new (conditional, last resort only):**
- `.chrono-step` ou `.bridge-seq--narrow` em `theme-unifacens.css` — **APENAS** se MODEL-05 com 5 caixas quebrar visualmente em 1280px no checkpoint humano.

**Assets to copy (pre-execution):**
- `docs/figures/ast_codedkt_ptbr.svg` → `apresentacao/assets/ast_codedkt_ptbr.svg` (Plan 3 MODEL-01; obrigatório por Pitfall 6)
- `results/fig_codedkt_difficulty_martins.png` → `apresentacao/assets/fig-codedkt-difficulty.png` (Plan 5 CLOSE-03 etapa A; temporário)
- `results/fig_codedkt_kc_curves.png` → `apresentacao/assets/fig-codedkt-kc-curves.png` (idem; temporário)
- `results/fig_codedkt_level_vs_slope.png` → `apresentacao/assets/fig-codedkt-level-vs-slope.png` (idem; temporário)
- (pós-checkpoint, se candidato ≠ 1) `results/fig_codedkt_<escolhido>.png` → `apresentacao/assets/fig-codedkt-martins-curves.png` (overwrite preservando filename canônico)

**Pattern extraction date:** 2026-05-28

---

*Phase: 4-Modelagem e Avaliação (Fase 3 EDM)*
*Patterns mapped: 2026-05-28*
