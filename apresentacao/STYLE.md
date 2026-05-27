# STYLE.md — Apresentação do TCC (reveal.js)

Guia de estilo dos slides. Mantém consistência visual e de citação. Os arquivos
são `apresentacao/index.html` (marcação dos slides) e
`apresentacao/assets/theme-unifacens.css` (tema). Base: template oficial
`Layout PPTs UniFacens_TCC.pptx` + acentos de programação (terminal/código).

## Identidade visual

- Slides 1280×720 (`reveal.js`, `width:1280 height:720`).
- Cada slide vive em `<section><div class="deck-slide slide-XYZ">…</div></section>`
  (o reveal força `display:block` na `<section>`, por isso o layout fica no `div` interno).
- Paleta (CSS vars em `:root`):
  - `--uni-blue #2667FF` (acento), `--uni-blue-d #1a4fd6` (negrito azul)
  - `--uni-dark #202124` (capa), `--uni-light #F1F6FB` (fundo de conteúdo)
  - `--uni-gray #DDE2EC` (marca d'água), `--uni-ink #111317` (texto)
- Marca d'água do símbolo Facens no canto superior direito dos slides de conteúdo
  (`<svg class="wm"><use href="#sym"/></svg>`).

## Tipografia (padronizada)

| Elemento | Fonte | Tamanho | Observações |
|---|---|---|---|
| Tópico `> ...` | Cascadia (`--mono`) | **24px** | cor `#5b6472`, `>` azul, caret piscando |
| Título do slide | **Arial** | **30px** | negrito 700, cor `--uni-ink` |
| Subtítulo (`.rel-sub`) | Arial | 22px | cor `#5b6472` |
| Corpo / prosa | Arial | ~21-23px | justificado quando parágrafo |
| Legenda "Fonte:" | Arial | 17-18px | cor `#5b6472` |
| Bloco de código exemplo | monospace (Courier) | — | NÃO mudar para Arial |

- `--uni-font` (Segoe UI) é a base do reveal, mas **títulos e corpo usam Arial**
  (alinhado ao manual). Cuidado: `.reveal h1,h2,h3` força `--uni-font`; em títulos
  `<h2>` é preciso declarar `font-family: Arial` explicitamente.
- O acento de terminal (`>` e caret) permanece em **mono** (Cascadia). Só os
  títulos/corpo são Arial.

## Cabeçalho de todo slide após a AGENDA

Padrão obrigatório: **linha de tópico + título**, com **16px** de espaço entre eles.

```html
<p class="deck-topic"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
<h2 class="prob-head">Título do slide</h2>
```

- Tópico genérico: classe `.deck-topic`. Nos slides de correlato (template
  `.slide-related`) o equivalente é `.rel-kicker.kicker` + `.rel-title`.
- Hoje todos os slides de conteúdo usam o tópico **`> trabalhos correlatos`**.
- O caret piscante (`<span class="caret blink">`) fica no fim do tópico, ou no fim
  do último item de uma lista (padrão da Agenda e do correlato do Zorić).
- Gap tópico→título = 16px: garantido por `margin:0 0 16px` no tópico e
  `margin-top:0` no título (zerar a margem padrão de `<p>` quando o título for `<p>`).

## Caret / blink

```css
.caret { display:inline-block; width:.55em; height:1.02em; background: var(--caret-color, var(--uni-blue)); }
.caret.blink { animation: caretBlink 1.05s steps(1) infinite; }
```

## Convenções de citação (manual MSGQ-21.01, em `apresentacao/`)

- **Citação direta curta (até 3 linhas):** entre aspas duplas, no texto, com
  `(Sobrenome, ano, p. X)`. Estilo no deck: `.rel-quote` / `.prob-quote` (barra
  azul à esquerda) + `<span class="src">` para a fonte.
- **Citação direta longa (mais de 3 linhas):** parágrafo independente, sem aspas,
  fonte menor.
- **Tradução de artigo estrangeiro (feita por nós):** acrescentar `tradução nossa`
  ao final → `(Zorić, 2020, p. 12, tradução nossa)`. Só para citação DIRETA literal.
- **Paráfrase = citação indireta:** `Com base em Sobrenome (ano, p. X)` ou
  citação autor-prominente; **sem** "tradução nossa".
- **Legenda de fonte** no rodapé do slide: `Fonte: ...` em Arial.
- Sobrenome dentro de parênteses: só a inicial maiúscula. Dois autores: `(Corbett; Anderson, 1995)`.

## Regras de redação

- **Termos estrangeiros em itálico e minúsculas** (ex.: *knowledge tracing*),
  inclusive em títulos/subtítulos. Nomes de modelos (BKT, Code-DKT) ficam como estão.
- **Sem travessões (em-dash)** na prosa; usar vírgula, dois-pontos ou parênteses.
- **Regra dos correlatos:** todo autor novo é introduzido em um slide
  `> trabalhos correlatos` ANTES do slide que usa seus resultados.

## Diagramas (estilo Word/ABNT)

Caixas de diagrama (mapas, sequências) seguem aparência de figura ABNT monocromática:

```css
background:#fff; border:1.5px solid #1f1f1f; border-radius:0;  /* cantos retos */
```

Setas pretas (`#1f1f1f`). Exemplos: `.kc-box`/`.kc-diff` (slide de KCs) e
`.bridge-seq .step` (slide-ponte). Cada figura/diagrama leva `Fonte:` abaixo.

## Inventário de slides (ordem atual)

| # | classe | conteúdo |
|---|---|---|
| 0 | slide-cover-brand | Abertura (logo + tagline) |
| 1 | slide-title-tcc | Capa do TCC (grafite, formal) |
| 2 | slide-agenda | Agenda (faixa azul + lista `>`) |
| 3 | slide-related | Correlato: Martins, Marin e Alves (2024) |
| 4 | slide-problem | O problema (dificuldades, Quadro 3) |
| 5 | slide-problem | Dentro dos conceitos técnicos |
| 6 | slide-kcfig | KCs (KCGen-KT) × dificuldades |
| 7 | slide-fig | Curva de aprendizado do Code-DKT |
| 8 | slide-code | O que o Code-DKT "olha" ao prever erro |
| 9 | slide-related | Correlato: Zorić (2020) — EDM |
| 10 | slide-related slide-methods | Ferramentas e metodologias da EDM |
| 11 | slide-phases | As quatro fases do processo de EDM |
| 12 | slide-related | Correlato: Yağcı (2022) — predição |
| 13 | slide-related slide-bridge | Ponte: da predição ao *knowledge tracing* |
| 14 | slide-related slide-corbett | Corbett e Anderson (1995) — origem do KT (motivação: mastery learning, model tracing × knowledge tracing) |
| 15 | slide-related slide-corbett | Corbett e Anderson (1995) — modelo de dois estados e os 4 parâmetros (base do BKT) |

Linhagem de KT no deck: **Corbett & Anderson (1995): KT + BKT → Piech (2015): DKT
→ Shi (2022): Code-DKT** (Code-DKT é o que fundamenta o TCC). Corbett e Anderson
ocupam dois slides (#14 motivação, #15 modelo/parâmetros). Em aberto: ordem
cronológica (os slides de resultado do Code-DKT, #7-#8, estão antes da
fundamentação de KT) e os próximos correlatos (Piech, Shi).

## Classes reutilizáveis

- `.slide-related`: template de correlato (`.rel-kicker`, `.rel-title`, `.rel-sub`,
  `.rel-quote` + `.src`, `.rel-points` com `>`, `.rel-cite`).
- `.deck-topic`: tópico `>` para slides fora do template de correlato.
- `.bridge-seq` (`.step`, `.arr`): sequência horizontal estilo Word.
- `.bkt-groups` (`.bkt-group` > `.bkt-group__head`/`.bkt-group__cap` + `.param` >
  `.sym` + `.lbl`): dois pares de parâmetros do BKT (aprendizado × desempenho);
  `.bkt-close` é o parágrafo de fecho sobre a inferência do estado.

## Pré-visualizar

```bash
cd apresentacao && python3 -m http.server 8000   # abrir http://127.0.0.1:8000
```

Navegação por hash: `#/N` (N = índice do slide, 0-based, ver inventário acima).
Atenção: o `http.server` não envia cabeçalhos de cache; ao editar o CSS, o navegador
pode servir a versão antiga. Para forçar recarregar, **suba em outra porta**.

## Fontes externas (para edição de conteúdo)

- Artigos: `docs/` (Code-DKT, Corbett1995 [escaneado, ler como imagem], Zorić,
  Yağcı, Martins, etc.).
- Manual de citações: `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf`.
- Report 4 (base dos correlatos): `~/Documents/Facens/TCC/Reports/Report 4/Report 4 - Documento de Projeto - EDM e KT.pdf`.
