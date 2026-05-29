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

Padrão obrigatório: **uma única linha de cabeçalho** com o nome da seção, em
formato `> [nome da seção]`, sem subtítulo e sem `<h2>` com nome do autor.

```html
<p class="deck-topic"><span class="ps1">&gt;</span>nome da seção<span class="caret blink"></span></p>
```

- Classe única: `.deck-topic`. Aplica a TODOS os slides de conteúdo (após a AGENDA),
  com exceção da capa (`slide-cover-brand`), do título do TCC (`slide-title-tcc`),
  da AGENDA (`slide-agenda`, padrão UniFacens com faixa azul e `<h2>Agenda</h2>`),
  dos marcadores (`slide-marker`, que usam `.marker-title`) e do slide de
  encerramento (replica de `slide-cover-brand`).
- Texto do cabeçalho: minúsculo, em Cascadia (`--mono`) 24px, cor `#5b6472`, com
  o `>` em azul UniFacens (`--uni-blue`). Exemplos travados nas fases 1 e 5:
  `> introdução`, `> mineração de dados educacionais`,
  `> as quatro fases da edm`, `> da edm ao knowledge tracing`,
  `> retomando o problema`, `> kcs semânticos extraídos`,
  `> evolução por dificuldade`, `> o que o code-dkt olha`,
  `> proposta da aplicação`.
- Nome do autor **não aparece** no corpo, nem em `<h2>`, nem em `.rel-sub`. Migra
  para a linha "Fonte:" no rodapé do slide (ver `Convenções de citação`).
- Caret piscante (`<span class="caret blink">`) como último filho de
  `<p class="deck-topic">`.
- Cabeçalhos travados por seção/fase ficam documentados nos PLAN.md de cada fase
  (D-04..D-11 da fase 1).

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
- **Apresentação de autores:** autores são introduzidos no momento da relevância
  via cabeçalho temático `> [nome da seção]`, nunca em slide dedicado de
  "trabalhos correlatos". O nome do autor não aparece no corpo nem no cabeçalho,
  apenas em `Fonte:` no rodapé do slide.
- **Voz própria como padrão:** paráfrase indireta com autor parentético é o
  padrão. Voz em primeira pessoa do plural quando aplicável ("nosso trabalho
  aplica", "nós seguimos", "implementamos"). Citação direta literal só quando a
  frase específica é o argumento (ex.: dados quantitativos em Martins p2/p3).

## Diagramas (estilo Word/ABNT)

Caixas de diagrama (mapas, sequências) seguem aparência de figura ABNT monocromática:

```css
background:#fff; border:1.5px solid #1f1f1f; border-radius:0;  /* cantos retos */
```

Setas pretas (`#1f1f1f`). Exemplos: `.kc-box`/`.kc-diff` (slide de KCs) e
`.bridge-seq .step` (slide-ponte). Cada figura/diagrama leva `Fonte:` abaixo.

## Inventário de slides (ordem final, pós-fase 5)

| # | classe | cabeçalho | conteúdo |
|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho temático) | Abertura (logo + tagline `> educational data mining e knowledge tracing`) |
| 1 | slide-title-tcc | (sem cabeçalho) | Capa do TCC (autores em grafite) |
| 2 | slide-agenda | (sem cabeçalho temático, `<h2>Agenda</h2>` na faixa azul) | AGENDA-01: 9 seções narrativas do deck (Introdução, Definição do problema, Dataset CSEDM, Preparação dos dados, Modelagem, Extração de KCs, Resultados, Proposta da aplicação, Encerramento); padrão UniFacens com faixa azul restaurado pós-fase 5; bullets em Arial sentence case |
| 3 | slide-related | `> introdução` | Recorte do problema (Martins, Marin e Alves, 2024) |
| 4 | slide-phases | `> mineração de dados educacionais` | EDM como processo + 4 fases (Zorić, 2020); fusão pós-fase 5 dos antigos #/4 (descrição) + #/5 (4 fases detalhadas); parágrafo `.phases-intro` genérico ("uma das metodologias possíveis para esse processo é a divisão em quatro fases") + lista numerada |
| 5 | slide-related slide-bridge | `> da edm ao knowledge tracing` | Ponte EDM para KT (Yağcı, 2022), fundido p1+p2 |
| 6 | slide-related | `> o problema do kt binário` | INTRO-03a (Shi et al., 2022) |
| 7 | slide-related | `> sinal pedagógico perdido` | INTRO-03b (adaptado de Shi et al., 2022) |
| 8 | slide-marker--phase1 | (sem temático) | MARKER-01 — Fase 1 EDM concluída |
| 9 | slide-related | `> o dataset csedm` | INTRO-01 (movido para abrir a Fase 2 EDM): CSEDM em ProgSnap2 (Price, 2020) |
| 10 | slide-related | `> como navegamos o csedm` | EDA-01: Tabela 1 com A1..A5 (alunos, participação, problemas, taxa de acerto) |
| 11 | slide-related | `> como o aprendizado se manifesta` | EDA-03: Figura 1 com curvas de aprendizado por assignment (Spring 2019) |
| 12 | slide-related | `> engajamento e desempenho` | EDA-04: Figura 2 com X-Grade por número de assignments completados |
| 13 | slide-related | `> aproximação ao protocolo` | EDA-02: pré-processamento e ponte 413 → 410 → 328/82; 23,68% confirma o match com Shi et al. (2022) |
| 14 | slide-marker--phase2 | (sem temático) | MARKER-02 — Fase 2 EDM concluída |
| 15 | slide-related | `> conhecimento como componentes` | INTRO-KC: definição de KCs (Corbett e Anderson, 1995) + nossa escolha (KC = ProblemID, protocolo Shi et al., 2022) |
| 16 | slide-related | `> o modelo escolhido` | MODEL-01a: escolha do Code-DKT + linha do tempo horizontal BKT (1995) → DKT (2015) → Code-DKT (2022) |
| 17 | slide-related | `> dentro do code-dkt` | MODEL-01b: pipeline interno (javalang → AST → code2vec → atenção → LSTM) + AST como Figura ABNT |
| 18 | slide-code | `> o que o code-dkt olha` | MODEL-03: atenção do Code-DKT no operador `&&` da submissão real do CSEDM (Code-DKT, Shi et al., 2022) |
| 19 | slide-related | `> code-dkt no csedm` | MODEL-04: Tabela 2 ABNT 4 modelos × 5 assignments (vírgula decimal pt-BR; linha Shi com en-dash) |
| 20 | slide-related slide-bridge | `> extração automática de kcs` | MODEL-05: pipeline 5 etapas Sampling → LLM → Clustering → Rotulagem → Q-matrix (Duan et al., 2025) |
| 21 | slide-problem | `> retomando o problema` | CLOSE-01: Martins p2 (13 autores; quote sem destaque, src preto, Arial; citação direta mantida porque o número é o argumento) |
| 22 | slide-problem | `> retomando o problema` | CLOSE-02: Martins p3 (10 autores; idem) |
| 23 | slide-kcfig | `> kcs semânticos extraídos` | Mapeamento KCs (saída do pipeline MODEL-05) para dificuldades de Martins, Marin e Alves (2024); brief text + Figura ABNT + blocos estilo bridge-seq |
| 24 | slide-fig | `> evolução por dificuldade` | CLOSE-03: Curva de aprendizado do Code-DKT por sub-dificuldade (curves_by_martins, PENDING-04 resolved); brief text + Figura ABNT, sem fig-read |
| 25 | slide-marker--phase3 | (sem temático) | MARKER-03 — Fase 3 EDM concluída (Implantação running) |
| 26 | slide-related slide-bridge | `> proposta da aplicação` | TOOL-01: fluxograma 6 etapas via CSS Grid (Import ProgSnap2 → Extração de KCs → Docente valida → Preparação dos dados → Code-DKT → Dashboard); absorve REQ TOOL-03 como última etapa (pivot D-104b da fase 5) |
| 27 | slide-marker--phase4 | (sem temático) | MARKER-04 — Fase 4 EDM (Implantação `--planned`, tracejado cinza, sem animação; sinaliza honestamente que o TCC 2 implementará) |
| 28 | slide-cover-brand | (sem cabeçalho temático) | END-01: réplica da abertura, tagline `> obrigado` (bracket narrativo com #/0) |

**Estado do deck:** 29 slides (era 30 ao fim da fase 5; refatoração pós-fase 5 fundiu os antigos #/4 e #/5 num único `slide-phases` que combina descrição de EDM + 4 fases de Zorić; demais slides após o #/4 deslocaram -1 posição). AGENDA-01 restaurada ao padrão UniFacens com 9 seções narrativas em uppercase bold.

**Linhagem de KT (consolidada nas fases 1-4):** Corbett e Anderson (1995) volta na cronologia do MODEL-01 (fase 4), seguida por Piech (2015) DKT e Shi (2022) Code-DKT. Yağcı (2022) ocupa o slide-bridge (slide 6) e Duan (2025) é introduzido no MODEL-05 (fase 4).

## Classes reutilizáveis

- `.slide-related`: template de correlato (`.rel-kicker`, `.rel-title`, `.rel-sub`,
  `.rel-quote` + `.src`, `.rel-points` com `>`, `.rel-cite`).
- `.deck-topic`: tópico `>` para slides fora do template de correlato.
- `.bridge-seq` (`.step`, `.arr`): sequência horizontal estilo Word. Default flex; o
  TOOL-01 (slide #/27) aplica inline `display: grid; grid-template-columns: 1fr auto ...`
  para forçar 6 caixas com largura exatamente igual.
- `.bkt-groups` (`.bkt-group` > `.bkt-group__head`/`.bkt-group__cap` + `.param` >
  `.sym` + `.lbl`): dois pares de parâmetros do BKT (aprendizado × desempenho);
  `.bkt-close` é o parágrafo de fecho sobre a inferência do estado.
- `.slide-agenda` (`.agenda-side`, `.agenda-main`, `.agenda-list`): template UniFacens
  com faixa azul à esquerda + logo Facens grande + `<h2>Agenda</h2>` + bullets em
  Cascadia mono com `>` azul. Restaurado pós-fase 5 para abrigar as 9 seções
  narrativas do deck (override do refator AGENDA da fase 5 plan 05-02).
- `.marker-pill--planned`: modificador aditivo do `.slide-marker` (estado "futuro
  previsto"; borda tracejada cinza azulado `#5b6472`, sem animação; distinguível de
  `--pending` sólido e `--running` que anima). Adicionado na fase 5.

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
