# Quick Task 260531-wkw: Aumentar e centralizar figuras + Fonte ABNT - Context

**Gathered:** 2026-06-01
**Status:** Ready for planning

<domain>
## Task Boundary

Ajustar as figuras do deck `apresentacao/index.html`:
1. Aumentar o tamanho e garantir centralização das figuras.
2. Recolocar a linha `Fonte:` (ABNT, conforme manual de textos técnicos) abaixo
   de cada Figura e Tabela.

Contexto: nesta mesma sessão (commit `d40a4c4`) removemos TODOS os rodapés
`Fonte:` do deck. Essa remoção foi agressiva demais para figuras e tabelas, que
por ABNT exigem fonte. Esta tarefa restaura a fonte apenas em Figuras e Tabelas
(slides de texto permanecem sem rodapé) e aproveita para aumentar/centralizar as
figuras.

NÃO está no escopo: reintroduzir `Fonte:` em slides de texto (Martins intro,
Yağcí, Shi, Price, Zorić phases, INTRO-KC, etc.). A citação direta de Martins
(slide-problem) mantém apenas a atribuição inline `(Martins, Marin e Alves, 2024,
p. X)` dentro da blockquote, como já está.
</domain>

<decisions>
## Implementation Decisions

### Escopo "aumentar + centralizar" — Imagens + diagramas CSS
Redimensionar/centralizar:
- **4 figuras de imagem:** Figura 1 (`eda-curvas-aprendizado.png`), Figura 2
  (`eda-xgrade-completados.png`), AST (`ast_codedkt_ptbr.svg`, slide MODEL-01b),
  curvas Martins (`fig-martins-curves-predita.png`, `.slide-fig`).
- **3 diagramas CSS:** Pipeline de extração de KCs (`.bridge-seq`, MODEL-05), mapa
  de KCs (`.kcfig-map`, `.slide-kcfig`), fluxo da aplicação (`.bridge-seq` grid,
  TOOL-01).
- **Tabelas NÃO** entram no redimensionamento (Tabela 1 e Tabela 2 ficam como
  estão de tamanho).

### Escopo "Fonte:" — Figuras E Tabelas
Recolocar `Fonte:` abaixo de toda Figura e Tabela ABNT (as 4 imagens + 3 diagramas
+ Tabela 1 + Tabela 2). Slides de texto seguem sem rodapé.

### Texto da Fonte — reaproveitar os antigos (recuperados de `d40a4c4^`)
Mapa exato (restaurar literalmente, preservando `<i>et al.</i>` ABNT):

| Elemento | Slide | Texto da Fonte (restaurar) |
|---|---|---|
| Tabela 1 — Taxa de acerto | EDA | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` |
| Figura 1 — Curvas de aprendizado | EDA | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` |
| Figura 2 — X-Grade | EDA | `Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).` |
| AST (`ast_codedkt_ptbr.svg`) | MODEL-01b | `Fonte: adaptado de Shi <i>et al.</i> (2022).` |
| Tabela 2 — First-attempt AUC | MODEL-04 | `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.` |
| Pipeline extração de KCs | MODEL-05 | `Fonte: elaborado pelo autor; adaptado de Duan <i>et al.</i> (2025).` |
| Mapa de KCs (`.kcfig-map`) | slide-kcfig | `Fonte: elaborado pelos autores, com base em Duan <i>et al.</i> (2025) e Martins, Marin e Alves (2024).` |
| Curvas Martins (`fig-martins-curves-predita.png`) | slide-fig | `Fonte: elaborado pelos autores (estimativa do Code-DKT, Shi <i>et al.</i>, 2022; conceitos via KCGen-KT, Duan <i>et al.</i>, 2025; dificuldades de Martins, Marin e Alves, 2024).` |
| Fluxo da aplicação | TOOL-01 | `Fonte: elaborado pelo autor; baseado em <i>docs/tcc2_prototipo.html</i>.` |

Recuperar do git se precisar de contexto: `git show d40a4c4^:apresentacao/index.html`.

### Claude's Discretion
- Magnitude exata do aumento de cada figura (max-width/max-height): decisão visual
  do executor; o usuário valida no browser. Garantir que NÃO estoure o slide
  1280×720 nem sobreponha título/fonte.
- Classe/estilo do parágrafo de fonte: reusar as classes existentes que sobraram
  no CSS (`.eda-source` para figuras/tabelas EDA e tabelas; o padrão centralizado
  14-18px cinza `#5b6472` do manual). Conferir que a regra CSS ainda existe; se a
  classe foi removida como órfã, recriar uma regra mínima conforme o manual.
</decisions>

<specifics>
## Specific Ideas / Pontos de atenção

- **`.slide-fig` (curvas Martins):** o título tem um hack `margin-bottom: -100px`
  (introduzido para puxar a imagem grande para cima quando a fonte saiu). Ao
  re-adicionar a Fonte e redimensionar/centralizar corretamente, REMOVER esse
  `-100px` e normalizar o espaçamento. O `.fig-wrap` já centraliza via flex.
- **`.eda-fig`** já centraliza (flex justify-center). Figura 2 está `--compact`
  (max-width 72%, max-height 340px) — é a menor; aumentar. Figura 1 é `--wide`.
- **CSS órfão:** na remoção dos rodapés algumas regras podem ter ficado sem uso
  (`.code-fonte`, `.rel-cite`, `.phases-fonte`). Para figuras/tabelas as classes
  relevantes são `.eda-source` (figuras/tabelas EDA) e o `.eda-fig`/`.slide-fig`.
  Verificar que `.eda-source` ainda existe no CSS antes de reusar.
- **STYLE.md:** atualizar a seção de citação. A decisão agora é mais matizada:
  slides de TEXTO não levam rodapé `Fonte:`, mas FIGURAS e TABELAS levam `Fonte:`
  abaixo (exigência ABNT / manual). Corrigir o texto que hoje diz "rodapés Fonte
  removidos de todos os slides".
- **Sem em-dash** na prosa (constraint do projeto).
</specifics>

<canonical_refs>
## Canonical References

- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — manual de
  textos técnicos Facens. LER a seção de Figuras/Tabelas para o formato ABNT de
  título (acima) e fonte (abaixo): alinhamento, fonte menor, "elaborado pelo
  autor" para produção própria. Vinculante (trabalho científico).
- `apresentacao/STYLE.md` — guia de estilo; seção "Convenções de citação" e
  "Diagramas (estilo Word/ABNT)". Atualizar conforme nota acima.
- `git show d40a4c4^:apresentacao/index.html` — estado com as fontes originais.
- Commit `d40a4c4` — removeu os rodapés Fonte (base desta tarefa).
</canonical_refs>
