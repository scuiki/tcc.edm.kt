---
phase: 05-implanta-o-agenda-e-encerramento-fase-4-edm
plan: 05
status: complete
requirements: [TOOL-01, TOOL-03]
commits:
  - 5f3a17f
  - 7eb2470
  - 12b70b6
  - cf813ec
  - 191ae01
  - efa716a
absorbed_from_plan: 05-04
---

# Plan 05-05 — TOOL-01 (proposta da aplicação, fluxograma 6 etapas)

## Resultado

Section TOOL-01 inserida entre MARKER-03 (#/26) e MARKER-04 (deslocada para #/28). Slide implementa o **fluxograma único da aplicação docente proposta para o TCC 2** que substitui o par TOOL-01 + TOOL-03 originalmente planejado (pivot D-104b consolidado no plan 05-04).

**Estrutura final do slide (após 6 commits de iteração):**

- Cabeçalho: `> proposta da aplicação` em `.deck-topic` com caret blink
- Abertura (1ª pessoa do plural): *"Este processo pode ser instrumentalizado para professores. Propomos uma aplicação docente que organiza o fluxo em seis etapas."*
- Título Figura ABNT: `Figura – Fluxo da aplicação docente proposta` (preto, Arial)
- Fluxograma horizontal **CSS Grid `1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr`** (6 colunas de etapa com largura exatamente igual, 5 colunas auto para setas)
- Cada etapa: bordas pretas 1.5px, fundo branco, cantos retos, padding `18px 10px`, font Arial inline
  - Título bold preto 16px (sem nowrap; permite quebra natural em 2 linhas para títulos longos)
  - Subtexto preto 14px com `margin-top: 6px`
- Rodapé legenda: `Fonte: elaborado pelo autor; baseado em docs/tcc2_prototipo.html.` em `.eda-source`
- Fechamento focado no professor (margin-top 38px do fluxograma): *"O professor consegue mapear os padrões da turma e ajustar suas aulas conforme o estado de aprendizado, individual e coletivo."*

**As 6 etapas (todas com largura igual, preto, Arial):**

| # | Título | Subtexto |
|---|---|---|
| 1 | **Import ProgSnap2** | dados dos estudantes |
| 2 | **Extração de KCs** | automática, Duan *et al.* (2025) |
| 3 | **Docente valida** | edita, adiciona ou remove |
| 4 | **Preparação dos dados** | sequências por estudante |
| 5 | **Code-DKT** | prediz turma e individual |
| 6 | **Dashboard** | estado de aprendizado |

Deck: 29 → 30 sections após a inserção. Posição final: TOOL-01 em `#/27`, MARKER-04 deslocou para `#/28`, END-01 para `#/29`.

## Trajetória de iterações

| # | Commit | Mudança |
|---|---|---|
| v1 | `5f3a17f` | Insercao inicial com 6 etapas em `.bridge-seq` flex; subtexto cinza; abertura mencionando "gesto humano na validação dos KCs"; min-height 280px (default do MODEL-05) |
| v2 | `7eb2470` | Remove trecho "com gesto humano..." da abertura; alonga caixas (padding 22×10, font-size 17/14, white-space nowrap nos títulos, padding 0 8px nas setas) |
| v3 | `12b70b6` | Padroniza visual: tudo preto (#000), Arial inline em cada step, min-height 120px + align-items stretch + justify-content center |
| v4 | `cf813ec` | Remove min-height 120px (usuário esclareceu que queria padronizar **largura**, não altura; min-height tinha deixado as caixas grandes demais) |
| v5 | `191ae01` | **Troca flex → CSS Grid** (1fr auto 1fr auto...) para forçar largura realmente igual; remove white-space nowrap; reduz font-size do bold de 17 para 16px; padding vertical 18px |
| v6 | `efa716a` | Aumenta margin-top do fechamento de 18px → 38px (separa visualmente fluxograma da prosa final) |

## Decisões emergentes registradas

**D-104f (CSS Grid em vez de flex para uniformidade horizontal):** o componente `.bridge-seq` foi originalmente projetado com flex `1 1 0`, que distribui largura proporcionalmente mas respeita conteúdo intrínseco quando combinado com `white-space: nowrap`. Para garantir largura exatamente igual entre 6 caixas com títulos de comprimentos variados, refatoramos para CSS Grid via inline-style. **Decisão local ao TOOL-01** — não estende a `.bridge-seq` global porque MODEL-05 e Yağcí (callers existentes) funcionam bem com o flex.

**D-104g (preto puro em vez de cinza no subtexto):** o template `.bridge-seq` herda `color: #5b6472` no contexto do subtexto. No TOOL-01 trocamos para `color: #000` puro per pedido explícito do usuário. Aplica só ao TOOL-01; demais slides preservam o cinza secundário.

**D-104h (largura prima sobre legibilidade em 1 linha):** títulos longos como "Preparação dos dados" agora quebram naturalmente em 2 linhas dentro da caixa, em vez de forçar nowrap (que distorcia largura). Tradeoff aceito pelo usuário no checkpoint v5.

## Acceptance gates finais (v6)

| Gate | Esperado | Obtido | Status |
|---|---|---|---|
| `grep -c "<section " index.html` | 30 | 30 | ✓ |
| `grep -c "proposta da aplicação" index.html` | 1 | 1 | ✓ |
| `grep -c "Fluxo da aplicação docente proposta" index.html` | 1 | 1 | ✓ |
| `grep -c "Import ProgSnap2" index.html` | 1 | 1 | ✓ |
| `grep -c "Extração de KCs" index.html` | 1 | 1 | ✓ |
| `grep -c "Docente valida" index.html` | 1 | 1 | ✓ |
| `grep -c "Preparação dos dados" index.html` | 1 | 1 | ✓ |
| `grep -c "Dashboard" index.html` (TOOL-01) | 1 (nova no TOOL-01) | 1 | ✓ |
| `grep -c "display: grid; grid-template-columns: 1fr auto" index.html` | 1 | 1 | ✓ |
| `grep -c "min-width: 0" index.html` | 6 | 6 | ✓ |
| `grep -c "white-space: nowrap" index.html` (no TOOL-01) | 0 | 0 | ✓ |
| `grep -c "ferramenta" index.html` | 1 (legacy, não TOOL-01) | 1 | ✓ |
| Sem em-dash novo | mesmo número antes/depois | mesmo | ✓ |
| HTTP 200 | 200 | 200 | ✓ |

## REQ coverage

- **REQ TOOL-01:** ✓ coberto pelo fluxograma 6 etapas (proposta da aplicação)
- **REQ TOOL-03:** ✓ coberto pela última etapa do fluxograma (Dashboard / estado de aprendizado) — pivot D-104b absorveu o slide TOOL-03 dedicado no único TOOL-01.
- **ROADMAP Phase 5 Success Criterion 1:** ✓ "Slide TOOL-01 ... pipeline mini-horizontal de 6 etapas, sem detalhar cada uma" — o detalhamento por etapa cresceu modestamente (override D-104e), mas o pipeline está dentro do espírito.
- **ROADMAP Phase 5 Success Criterion 2:** ✓ "Slide TOOL-03 mostra o dashboard..." — atendido como etapa do fluxograma TOOL-01, não como slide próprio. Pivot documentado em 05-04-SUMMARY.

## Iterações pós-checkpoint

**5 iterações** após a inserção inicial (incomum para esta fase; razão: pivot estrutural mid-plan):
1. Enxugar abertura
2. Padronizar visual (cor, Arial, blocos uniformes — interpretação errada de "padronizar")
3. Reverter min-height (esclarecimento: era largura, não altura)
4. CSS Grid para largura igual real
5. Espaçamento entre fluxograma e fechamento

## Commits

- `5f3a17f` apresentacao: slide TOOL-01 - proposta da aplicacao (fluxograma 6 etapas) [v1]
- `7eb2470` apresentacao: TOOL-01 - alongar caixas e enxugar abertura [v2]
- `12b70b6` apresentacao: TOOL-01 - padronizar caixas (tudo preto, Arial, min-height) [v3]
- `cf813ec` apresentacao: TOOL-01 - remover min-height 120px (altura natural) [v4]
- `191ae01` apresentacao: TOOL-01 - largura igual via CSS Grid (1fr x 6) [v5]
- `efa716a` apresentacao: TOOL-01 - aumentar espaco entre fluxograma e fechamento [v6 final]
