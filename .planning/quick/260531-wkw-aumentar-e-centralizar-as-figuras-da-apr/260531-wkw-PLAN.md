---
phase: quick-260531-wkw
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - apresentacao/index.html
  - apresentacao/assets/theme-unifacens.css
  - apresentacao/STYLE.md
autonomous: false
requirements: [QUICK-260531-wkw]
must_haves:
  truths:
    - "Toda Figura (4 imagens + 3 diagramas CSS) tem um rodapé Fonte: ABNT abaixo dela"
    - "Toda Tabela (Tabela 1 e Tabela 2) tem um rodapé Fonte: ABNT abaixo dela"
    - "As 4 figuras de imagem aparecem maiores e centralizadas, sem estourar o slide 1280x720"
    - "Slides de texto (Martins, Yagci, Shi, Zoric, INTRO-KC) continuam SEM rodapé Fonte:"
    - "O hack margin-bottom: -100px do titulo do slide-fig foi removido"
    - "STYLE.md descreve a regra matizada: texto sem Fonte, figuras e tabelas com Fonte"
  artifacts:
    - path: "apresentacao/index.html"
      provides: "9 paragrafos de Fonte: re-adicionados (Tabela 1, Fig 1, Fig 2, AST, Tabela 2, Pipeline KCs, Mapa KCs, Curvas Martins, Fluxo aplicacao)"
      contains: "eda-source"
    - path: "apresentacao/STYLE.md"
      provides: "Convencoes de citacao atualizadas"
      contains: "Fonte"
  key_links:
    - from: "apresentacao/index.html"
      to: "apresentacao/assets/theme-unifacens.css"
      via: "classe .eda-source aplicada aos paragrafos de Fonte"
      pattern: "eda-source"
---

<objective>
Restaurar a linha `Fonte:` (ABNT, manual MSGQ-21.01) abaixo de cada Figura e Tabela do deck `apresentacao/index.html`, e aumentar/centralizar as 4 figuras de imagem.

Contexto: o commit `d40a4c4` removeu TODOS os rodapés `Fonte:` do deck. Para slides de texto isso fica como está, mas Figuras e Tabelas exigem fonte por ABNT. Esta tarefa restaura a fonte apenas nesses elementos e ajusta o tamanho das figuras.

Purpose: conformidade ABNT das figuras/tabelas + legibilidade visual.
Output: index.html com 9 rodapés Fonte: re-adicionados; CSS de figuras ajustado; STYLE.md corrigido.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/quick/260531-wkw-aumentar-e-centralizar-as-figuras-da-apr/260531-wkw-CONTEXT.md
@apresentacao/STYLE.md

<interfaces>
<!-- Estado atual confirmado no codigo (nao explorar de novo). -->

Regra CSS `.eda-source` EXISTE em theme-unifacens.css (linhas 482-487):
  width: 92%; margin: 4px auto 0; Arial 14px; color: #5b6472; text-align: center.
  -> Reusar essa classe para os rodapes Fonte de figuras/tabelas. NAO recriar.

Mapa exato elemento -> localizacao -> texto da Fonte (restaurar literalmente, com `<i>et al.</i>` preservado):

| Elemento | Linha aprox. (apos qual fechar) | Texto da Fonte |
|---|---|---|
| Tabela 1 (EDA, `.eda-grid`) | apos `</table>` linha 259 | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` |
| Figura 1 (`eda-curvas-aprendizado.png`, `.eda-fig--wide`) | apos `</figure>` linha 277 | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` |
| Figura 2 (`eda-xgrade-completados.png`, `.eda-fig--compact`) | apos `</figure>` linha 294 | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` |
| AST (`ast_codedkt_ptbr.svg`, slide MODEL-01b) | apos `</div>` que fecha o wrapper centralizado, linha 421 | `Fonte: adaptado de Shi <i>et al.</i> (2022).` |
| Tabela 2 (`.eda-grid`, MODEL-04) | apos `</table>` linha 445 | `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.` |
| Pipeline KCs (`.bridge-seq`, MODEL-05) | apos o ultimo `.rel-lead` linha 476, antes de `</div>` | `Fonte: elaborado pelo autor; adaptado de Duan <i>et al.</i> (2025).` |
| Mapa KCs (`.kcfig-map`) | apos `</div>` que fecha `.kcfig-map` linha 545 | `Fonte: elaborado pelos autores, com base em Duan <i>et al.</i> (2025) e Martins, Marin e Alves (2024).` |
| Curvas Martins (`fig-martins-curves-predita.png`, `.slide-fig`) | apos `</div>` que fecha `.fig-wrap` linha 601 | `Fonte: elaborado pelos autores (estimativa do Code-DKT, Shi <i>et al.</i>, 2022; conceitos via KCGen-KT, Duan <i>et al.</i>, 2025; dificuldades de Martins, Marin e Alves, 2024).` |
| Fluxo aplicacao (`.bridge-seq` grid, TOOL-01) | apos o ultimo `.rel-lead` linha 673, antes de `</div>` | `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.` |

Markup do rodape (figuras EDA, tabelas, pipeline, mapa KCs):
  `<p class="eda-source">Fonte: ...</p>`

Markup do rodape para o slide-fig (curvas Martins): a classe propria `.fig-fonte` ja
existe (CSS linha 318: Arial 18px centralizado cinza). Usar `<p class="fig-fonte">Fonte: ...</p>`.
A AST (slide MODEL-01b) usa markup inline atual; aplicar `<p class="eda-source">` tambem.

Pontos de atencao (de CONTEXT.md, vinculantes):
- `.slide-fig` (linha 600): o `.eda-title` tem `style="...margin-bottom: -100px;"` (hack para
  puxar a imagem quando a fonte saiu). REMOVER esse `-100px` ao re-adicionar a fonte; usar
  espacamento normal (ex.: margin-bottom pequeno ou 0). `.fig-wrap` ja centraliza via flex.
- `.eda-fig` ja centraliza (flex justify-center). Figura 2 esta `--compact` (max-width 72%,
  img max-height 340px) = a menor; aumentar. Figura 1 e `--wide` (max-width 150%, max-height 1000px).
- CSS orfao possivel (`.code-fonte`, `.rel-cite`, `.phases-fonte`): NAO sao usados por figuras/tabelas;
  nao mexer nesta tarefa (fora de escopo).
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Re-adicionar Fonte ABNT em todas as Figuras e Tabelas</name>
  <files>apresentacao/index.html</files>
  <action>
Inserir 9 paragrafos de Fonte: no index.html, um abaixo de cada Figura e Tabela, usando o mapa exato em <interfaces>. Restaurar os textos literalmente, preservando `<i>et al.</i>` e demais formatos ABNT.

Para Tabela 1, Figura 1, Figura 2, AST, Tabela 2, Pipeline KCs e Mapa KCs: usar `<p class="eda-source">Fonte: ...</p>` (a classe `.eda-source` ja existe no CSS, nao criar regra nova).

Para Curvas Martins (`.slide-fig`): usar `<p class="fig-fonte">Fonte: ...</p>` (classe `.fig-fonte` ja existe, linha 318 do CSS). Inserir apos o `</div>` que fecha `.fig-wrap` (linha 601).

Para o Fluxo da aplicacao (TOOL-01): inserir o `<p class="eda-source">` apos o ultimo `.rel-lead` (linha 673), ainda dentro de `.deck-slide`.

NAO adicionar Fonte: a nenhum slide de texto (Martins intro, Yagci, Shi INTRO-03a/03b, Zoric phases, INTRO-KC, slide-code). NAO reverter a remocao geral de `d40a4c4` nesses slides.

Se precisar conferir o texto original de algum rodape: `git show d40a4c4^:apresentacao/index.html`.

Sem em-dash na prosa (constraint do projeto).
  </action>
  <verify>
    <automated>cd apresentacao && grep -c 'eda-source\|fig-fonte' index.html | grep -qx 9 && echo "9 rodapes OK" || (echo "esperado 9 rodapes Fonte"; exit 1)</automated>
  </verify>
  <done>
9 paragrafos de Fonte: presentes (8 `.eda-source` + 1 `.fig-fonte`), cada um abaixo da sua Figura/Tabela, com `<i>et al.</i>` preservado nos 5 que o usam (AST, Tabela 2, Pipeline, Mapa, Curvas Martins). Nenhum slide de texto recebeu Fonte:.
  </done>
</task>

<task type="auto">
  <name>Task 2: Aumentar e centralizar as 4 figuras de imagem + remover hack do slide-fig</name>
  <files>apresentacao/index.html, apresentacao/assets/theme-unifacens.css</files>
  <action>
Aumentar o tamanho das 4 figuras de imagem garantindo centralizacao, sem estourar o slide 1280x720 nem sobrepor titulo/Fonte. As tabelas NAO sao redimensionadas (ficam como estao).

Figuras a aumentar:
1. Figura 1 (`eda-curvas-aprendizado.png`, `.eda-fig--wide`) — ja larga; ajustar se necessario para preencher melhor sem cortar.
2. Figura 2 (`eda-xgrade-completados.png`, `.eda-fig--compact`) — a MENOR (max-width 72%, img max-height 340px). Aumentar (ex.: subir max-width e/ou max-height da regra `.eda-fig--compact` / `.eda-fig--compact img` no CSS, linhas 504-505).
3. AST (`ast_codedkt_ptbr.svg`, slide MODEL-01b, linha 420) — aumentar o `max-width` inline (atual 620px) respeitando a Fonte adicionada na Task 1.
4. Curvas Martins (`fig-martins-curves-predita.png`, `.slide-fig`) — REMOVER o `margin-bottom: -100px` do `.eda-title` inline (linha 600), normalizando o espacamento; a imagem usa `.slide-fig .fig-wrap img` (max-width 92%, max-height 488px no CSS linha 314), aumentar se couber acima da Fonte.

Magnitude exata de cada aumento e discricao visual do executor: o usuario valida no browser. Cada figura deve caber inteira no slide 1280x720, centralizada, sem sobrepor titulo nem rodape Fonte:.

Editar as regras de tamanho no CSS (`.eda-fig--compact`, `.eda-fig--wide`, `.slide-fig .fig-wrap img`) e/ou os styles inline da AST conforme necessario. Manter a centralizacao existente (flex justify-center ja presente em `.eda-fig` e `.fig-wrap`).
  </action>
  <verify>
    <automated>cd apresentacao && grep -c 'margin-bottom: -100px\|margin-bottom:-100px' index.html | grep -qx 0 && echo "hack -100px removido" || (echo "hack -100px ainda presente"; exit 1)</automated>
  </verify>
  <done>
Hack `margin-bottom: -100px` removido do `.slide-fig`. As 4 figuras (Fig 1, Fig 2, AST, Curvas Martins) aparecem maiores e centralizadas. Tabela 1 e Tabela 2 inalteradas de tamanho. Validacao final no checkpoint visual.
  </done>
</task>

<task type="auto">
  <name>Task 3: Atualizar STYLE.md para a regra matizada de Fonte</name>
  <files>apresentacao/STYLE.md</files>
  <action>
Corrigir STYLE.md, que hoje afirma (linhas 61-63 e 87-92, e nota em "Regras de redacao" linha 104) que "Os rodapes Fonte: foram removidos de todos os slides".

A regra correta agora e matizada:
- Slides de TEXTO continuam SEM rodape `Fonte:` (a atribuicao fica no cabecalho tematico `> [secao]` e, em citacao direta literal, na fonte inline da blockquote).
- FIGURAS e TABELAS levam `Fonte:` abaixo (exigencia ABNT / manual MSGQ-21.01), usando `.eda-source` (Arial 14-18px cinza `#5b6472`, centralizado) ou `.fig-fonte` no `.slide-fig`.

Atualizar a secao "Convencoes de citacao" e a nota em "Cabecalho de todo slide" e "Diagramas (estilo Word/ABNT)" (linha 119 ja diz "Cada figura/diagrama leva Fonte: abaixo." — manter coerente). Substituir as frases que dizem "removidos de todos os slides" pela regra matizada.

Sem em-dash na prosa.
  </action>
  <verify>
    <automated>cd apresentacao && grep -qi 'figuras e tabelas levam' STYLE.md && grep -qvi 'removidos de todos os slides' <(grep -i 'removidos de todos os slides' STYLE.md) && echo "STYLE.md atualizado" || echo "revisar STYLE.md manualmente"</automated>
  </verify>
  <done>
STYLE.md descreve a regra matizada: slides de texto sem `Fonte:`, figuras e tabelas com `Fonte:` abaixo. Frases obsoletas "removidos de todos os slides" corrigidas. Sem em-dash.
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
9 rodapes `Fonte:` ABNT re-adicionados abaixo das 4 figuras + 3 diagramas + Tabela 1 + Tabela 2. As 4 figuras de imagem aumentadas e centralizadas. Hack `margin-bottom: -100px` removido. STYLE.md atualizado.
  </what-built>
  <how-to-verify>
1. Subir o preview numa porta nova (evita cache de CSS):
   `cd apresentacao && python3 -m http.server 8011`
2. Abrir `http://127.0.0.1:8011` (HTTP 200 esperado).
3. Verificar slide a slide pelos hashes (indices 0-based do inventario do STYLE.md):
   - `#/10` (EDA-01 Tabela 1) — Fonte abaixo da tabela.
   - `#/11` (EDA-03 Figura 1) — figura maior, centralizada, Fonte abaixo.
   - `#/12` (EDA-04 Figura 2) — figura maior que antes, centralizada, Fonte abaixo.
   - `#/17` (MODEL-01b AST) — AST maior, Fonte "adaptado de Shi et al. (2022)" abaixo.
   - `#/19` (MODEL-04 Tabela 2) — Fonte abaixo da tabela.
   - `#/20` (MODEL-05 Pipeline KCs) — Fonte abaixo do pipeline.
   - `#/23` (slide-kcfig Mapa KCs) — Fonte abaixo do mapa.
   - `#/24` (slide-fig Curvas Martins) — imagem bem posicionada (sem o hack -100px), Fonte abaixo.
   - `#/26` (TOOL-01 Fluxo) — Fonte abaixo do fluxograma.
4. Confirmar que NENHUMA figura/tabela estoura o slide 1280x720 nem sobrepoe titulo ou Fonte.
5. Confirmar que slides de TEXTO (ex.: `#/3` Martins, `#/5` Yagci, `#/6`/`#/7` Shi, `#/15` INTRO-KC) continuam SEM rodape Fonte:.
  </how-to-verify>
  <resume-signal>Digite "approved" ou descreva ajustes de tamanho/posicao por slide.</resume-signal>
</task>

</tasks>

<verification>
- `grep -c 'eda-source\|fig-fonte' apresentacao/index.html` retorna 9.
- `grep -c 'margin-bottom: -100px' apresentacao/index.html` retorna 0.
- `python3 -m http.server` numa porta nova serve `index.html` com HTTP 200.
- Checkpoint visual APPROVED nos 9 slides de figura/tabela + amostragem de slides de texto sem Fonte.
</verification>

<success_criteria>
- Toda Figura (4 imagens + 3 diagramas) e Tabela (2) tem rodape `Fonte:` ABNT abaixo, com texto literal do mapa e `<i>et al.</i>` preservado.
- As 4 figuras de imagem aparecem maiores e centralizadas, cabendo no slide 1280x720.
- Hack `margin-bottom: -100px` do `.slide-fig` removido.
- Slides de texto permanecem sem rodape Fonte:.
- STYLE.md descreve a regra matizada.
- Sem em-dash na prosa adicionada.
</success_criteria>

<output>
After completion, create `.planning/quick/260531-wkw-aumentar-e-centralizar-as-figuras-da-apr/260531-wkw-SUMMARY.md`
</output>
