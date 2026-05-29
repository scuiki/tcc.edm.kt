---
phase: 05-implanta-o-agenda-e-encerramento-fase-4-edm
plan: 02
status: complete
requirements: [AGENDA-01, PENDING-01]
commits:
  - 01bead5
  - 68c638e
  - 35a0b34
---

# Plan 05-02 — AGENDA refatorada + STYLE.md override + cleanup CSS

## Resultado

- **Slide `#/2` refatorado in-place** em `apresentacao/index.html`: o markup antigo (`<h2>Agenda</h2>` + `agenda-side` faixa azul + `agenda-main` com 8 bullets genéricos do template UniFacens) foi substituído pelo template `.slide-related` com cabeçalho `.deck-topic` `> agenda` + `<ol class="agenda-edm-list">` com as 4 fases EDM (Definição do Problema, Preparação dos Dados, Modelagem e Avaliação, Implantação). Caret blink apenas no último item per D-93d. Sem rodapé `Fonte:` per D-93e.
- **Nova classe `.agenda-edm-list`** anexada em `apresentacao/assets/theme-unifacens.css` (logo após o bloco `.slide-related`, ~22 linhas novas): contadores azuis UniFacens via `::before`, Arial 23px line-height 1.4, max-width 900px.
- **Cleanup CSS:** removidas 8 declarações órfãs (`.slide-agenda`, `.slide-agenda .agenda-side`, `.slide-agenda .agenda-side h2`, `.slide-agenda .agenda-side .logo`, `.slide-agenda .agenda-main`, `.agenda-list`, `.agenda-list li`, `.agenda-list li .ps1`) — total 19 linhas removidas. Paralelo ao precedente da fase 1 (commit `30ba911`).
- **STYLE.md §Cabeçalho reescrito** (override D-93b): título trocado para "Cabeçalho de TODO slide (incluindo AGENDA)"; bullet de escopo agora explicita "incluindo a AGENDA (refator em fase 5)" e enumera as exceções (`slide-cover-brand`, `slide-title-tcc`, `slide-marker` com `.marker-title`, `slide-end`); `> agenda` adicionado à lista de exemplos travados.

Deck mantém **28 sections** (refatoração não desloca contagem). AGENDA permanece em `#/2` per D-92.2.

## Markup final da AGENDA-01 (index.html linhas 59-73)

```html
<!-- ============ SLIDE · Agenda · 4 fases da EDM ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>agenda<span class="caret blink"></span></p>

    <ol class="agenda-edm-list">
      <li>Definição do Problema</li>
      <li>Preparação dos Dados</li>
      <li>Modelagem e Avaliação</li>
      <li>Implantação<span class="caret blink"></span></li>
    </ol>
  </div>
</section>
```

## CSS adicionado em theme-unifacens.css (após linha 182, bloco `.slide-related`)

```css
/* ---------------------------------------------------------------------------
   AGENDA (refator fase 5): lista numerada das 4 fases EDM dentro do template
   .slide-related; cabeçalho `> agenda` (.deck-topic) + .agenda-edm-list com
   contadores azuis UniFacens. Override D-93b do STYLE.md.
   --------------------------------------------------------------------------- */
.agenda-edm-list {
  list-style: none; counter-reset: agenda;
  margin: 32px 0 0; padding: 0; max-width: 900px;
  --caret-color: var(--uni-blue);
}
.agenda-edm-list li {
  counter-increment: agenda; position: relative;
  padding: 10px 0 10px 50px;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 23px; line-height: 1.4; color: var(--uni-ink);
}
.agenda-edm-list li::before {
  content: counter(agenda) ".";
  position: absolute; left: 12px; top: 10px;
  color: var(--uni-blue); font-weight: 700;
}
```

## Acceptance gates

| Gate | Esperado | Obtido | Status |
|---|---|---|---|
| `grep -c "<section " index.html` | 28 | 28 | ✓ |
| `grep -c "agenda-edm-list" index.html` | 1 | 1 | ✓ |
| `grep -c "agenda-edm-list" theme-unifacens.css` | ≥ 3 | 4 | ✓ |
| `grep -c "agenda-side\|agenda-main" index.html` | 0 | 0 | ✓ |
| `grep -c "<h2>Agenda</h2>" index.html` | 0 | 0 | ✓ |
| `grep -c '>agenda<span class="caret blink"></span>' index.html` | 1 | 1 | ✓ |
| `grep -c "data-background-gradient" index.html` | 0 | 0 | ✓ |
| `grep -nE "\.slide-agenda\|\.agenda-side\|\.agenda-main\|\.agenda-list" theme-unifacens.css` | 0 hits | 0 | ✓ |
| `grep -c "## Cabeçalho de TODO slide" STYLE.md` | 1 | 1 | ✓ |
| `grep -c "## Cabeçalho de todo slide após a AGENDA" STYLE.md` | 0 | 0 | ✓ |
| `grep -c "incluindo a AGENDA" STYLE.md` | ≥ 1 | 1 | ✓ |
| `grep -c "> agenda" STYLE.md` | ≥ 1 | 1 | ✓ |
| HTTP 200 em `/index.html` | 200 | 200 | ✓ |
| Sem em-dash novo introduzido (diff STYLE.md) | 0 | 0 | ✓ |

## Decisões ad-hoc registradas

Nenhuma. Plan executado autônomo (`autonomous: true`); todas as decisões D-93a..D-93f foram aplicadas literalmente do plano original. Nenhuma divergência.

**Observação:** o único remanescente da string "slide-agenda" em todo o repositório `apresentacao/` está em `STYLE.md` linha 114 (tabela §Inventário), referência histórica que será reescrita pelo plan 05-06 de fechamento da fase. Não é regressão.

## Commits

- `01bead5` apresentacao: refatorar slide-agenda para padrao .deck-topic + 4 fases EDM
- `68c638e` apresentacao: limpar regras CSS orfas do slide-agenda original
- `35a0b34` docs(style): override D-93b - .deck-topic agora cobre AGENDA tambem
