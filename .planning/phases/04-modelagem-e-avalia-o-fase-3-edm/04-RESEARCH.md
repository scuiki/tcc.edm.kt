# Phase 4: Modelagem e Avaliação (Fase 3 EDM) — Research

**Researched:** 2026-05-28
**Domain:** Apresentação reveal.js — 4 slides novos (MODEL-01, MODEL-04, MODEL-05, MARKER-03) + 4 reaproveitamentos (MODEL-03, slide-kcfig, CLOSE-01/02/03) sobre Code-DKT (Shi et al., 2022) e KCGen-KT (Duan et al., 2025), fechando o bloco da Fase 3 da EDM no deck.
**Confidence:** HIGH (Code-DKT, MARKER, MODEL-04 números, componentes CSS); MEDIUM-HIGH (Duan pipeline phrasing, AST SVG escala); MEDIUM (5 caixas em `.bridge-seq` em 1280px — não testado em browser ainda).

## Summary

A pesquisa confirmou todas as fontes primárias e numéricas para os 4 slides novos, identificou divergências críticas entre o CONTEXT e a fonte primária (3 vs 5 etapas em Duan; 28 vs 17 KCs no slide-kcfig; identificação errada do paper short-83) e mapeou os componentes CSS reusáveis sem necessidade de criar novas classes. Os 4 PNGs candidatos do CLOSE-03 existem no `results/`, com MD5 do `curves_by_martins` idêntico ao asset atual no slide. O SVG da AST (560×620) renderiza dentro de `~450×500` com `transform: scale(0.8)`. Toda a tabela ABNT do MODEL-04 já tem números canônicos travados em `results/comparison_table_first_auc.md` (Code-DKT A439=73,27%, dentro do gate ±3pp do paper Shi A439=75,74%).

**Primary recommendation:** Implementar na ordem MARKER-03 → MODEL-04 → MODEL-01 → MODEL-05 (do mais determinístico ao mais experimental visualmente), reusando 100% dos componentes existentes (`.slide-marker`, `.eda-grid`, `.bridge-seq`, `.deck-topic`). CLOSE-03 vira um plan separado com 4 sections temporários para escolha visual no checkpoint, e correção do comentário HTML linha 541 que aponta ao filename errado.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**D-75 — Posição no DOM:** Os 4 slides novos entram após MARKER-02 (`#/15`) e antes do trio Martins+fig + MARKER-03 no fim. Ordem dentro do bloco: MODEL-01 → slide-code (MODEL-03) → MODEL-04 → MODEL-05 → slide-kcfig → Martins p2 (CLOSE-01) → Martins p3 (CLOSE-02) → slide-fig (CLOSE-03) → MARKER-03. Slide-code atualmente em `#/16` desloca para `#/17`.

**D-76 — Justificativa narrativa:** MARKER-02 fecha "Preparação dos Dados ✓"; MODEL-01 abre dizendo como o Code-DKT funciona; slide-code (MODEL-03) mostra atenção sobre código real; MODEL-04 mostra resultados quantitativos; MODEL-05 introduz extração automática de KCs; slide-kcfig mostra a saída; CLOSE-01/02/03 fecham com retomada Martins (eixo prioritário); MARKER-03 fecha "Modelagem e Avaliação ✓".

**D-77 — MODEL-01:**
- Cabeçalho: `> como o code-dkt funciona`
- Layout: cronologia 3 chips horizontais (BKT 1995 / Bayes / habilidades por KC) → (DKT 2015 / RNN / histórico sequencial) → (Code-DKT 2022 / RNN + paths AST / code2vec); body 2 colunas (texto + AST inset).
- Texto: 1 frase contexto + 4 bullets (`javalang → AST`; `code2vec → caminhos folha-a-folha`; `atenção pondera os caminhos`; `LSTM combina com (ProblemID, acerto/erro)`).
- Inset SVG: `docs/figures/ast_codedkt_ptbr.svg` (560×620) escalado para ~450×500.
- Rodapé: `Fonte: adaptado de Shi <i>et al.</i> (2022).`
- NÃO usar `codedkt_model_structure_ptbr.svg` (1180×640) — reservado para TCC.

**D-78 — MODEL-04:**
- Cabeçalho: `> code-dkt no csedm`
- Escopo: 3 modelos (BKT, DKT, Code-DKT) × 5 assignments + linha "Shi (2022)" só com A439.
- Métrica: first-attempt AUC apenas (all-attempts e Wilcoxon ficam para fala/QA).
- Caption: "first-attempt AUC: métrica primária; mede transferência entre problemas e evita autocorrelação intra-problema (Shi <i>et al.</i>, 2022, §5)."
- Forma: tabela ABNT em `.eda-grid`. NÃO embutir PNG.
- Números: Code-DKT A439 first = 73,27% (multirun 10 seeds); paper Shi A439 first = 75,74%; delta = -2,47pp.
- Rodapé: `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.`

**D-79 — MODEL-05:**
- Cabeçalho: `> extração automática de kcs`
- Estrutura: abertura 1 frase + pipeline horizontal 5 etapas + frase de fechamento + rodapé.
- Abertura: "Construímos um pipeline de cinco etapas para extrair Knowledge Components do CSEDM."
- 5 etapas (em `.bridge-seq` estendido): Sampling estratificado (n=5/problema) → LLM gera KCs brutos (código bruto) → Clustering Sentence-BERT + HAC → Rotulagem dos clusters (LLM) → Q-matrix (28 KCs / 50 problemas).
- Fechamento: "A decisão-chave foi alimentar o LLM com código bruto, não AST (Duan <i>et al.</i>, 2025, Tab. 4)."
- D-79f: override PROJECT.md (3 etapas → 5 etapas) por fidelidade ao notebook 03b.
- Voz: 1ª pessoa do plural; Duan parentético `<i>et al.</i>` ABNT.
- Rodapé: `Fonte: adaptado de Duan <i>et al.</i> (2025).`
- NÃO duplicar slide-kcfig.

**D-80 — MODEL-03 (slide-code reaproveitado):** Nenhuma alteração; já reformatado na fase 1.

**D-81 — Justificativa first-attempt AUC:** métrica primária cross-projeto; all-attempts infla por autocorrelação intra-problema; first-attempt mede transferência pura.

**D-82 — CLOSE-01/02 (Martins p2/p3):** NÃO TOCAR nesta fase. Já reformatados na fase 1 (commits `590ae34`, `2a86049`); citação direta mantida como exceção D-28.

**D-83 — CLOSE-03:**
- D-83a: PENDING-04 resolvido. `codedkt_kc_retrained.pkl` existe (2026-05-25 01:42); asset MD5 idêntico a `results/fig_codedkt_curves_by_martins.png`.
- D-83b: 4 PNGs candidatos em `results/`: `fig_codedkt_curves_by_martins.png` (atual), `fig_codedkt_difficulty_martins.png`, `fig_codedkt_kc_curves.png`, `fig_codedkt_level_vs_slope.png`.
- D-83c: plan cria 4 sections temporários para comparação visual no checkpoint; user escolhe 1; 3 removidos; comentário HTML linha 541 corrigido.
- D-83d: `fig-read` text defere para checkpoint visual após escolha.

**D-84 — MARKER-03:**
- Implementação mecânica do componente `.slide-marker` (zero CSS novo).
- Pills 1, 2, 3: `--done` com check + badge `[done]`.
- Pill 4: `--running` com ícone reload girando + badge `[running]`.
- Título `> AS QUATRO FASES DA EDM`; rodapé `Fonte: adaptado de Zorić (2020).`

**D-85 a D-90 — Convenções herdadas:**
- Cabeçalho `> [seção]` único (D-85).
- Paráfrase indireta como padrão; citação direta literal proibida nos 3 MODEL novos (D-86).
- Sem em-dash (D-87); memória `feedback_no_em_dashes` vinculante.
- `<i>et al.</i>` ABNT em todas as citações parentéticas múltiplas (D-88).
- "Estudantes", nunca "alunos" em prosa nova (D-89).
- Cada slide novo tem `Fonte:` no rodapé (D-90).

**D-91 — Validação visual:** `cd apresentacao && python3 -m http.server 8000` percorrendo `#/0` ao `#/24`.

### Claude's Discretion

- **Ordem de implementação dos 4 slides novos:** sugestão neutra MARKER-03 → MODEL-04 → MODEL-01 → MODEL-05 (mais determinístico ao mais experimental). Alternativa: MODEL-05 primeiro porque a extensão de `.bridge-seq` para 5 caixas é o maior risco.
- **Granularidade dos commits:** 1 plan por slide (4 plans); 1 commit funcional por plan.
- **Componente da cronologia em MODEL-01:** `.bridge-seq` estendido vs novo `.chrono-step`. Default: tentar `.bridge-seq` primeiro.
- **Componente do pipeline em MODEL-05:** `.bridge-seq` estendido para 5 caixas + 4 setas; tipografia das caixas a calibrar se ficar apertado.
- **Microcópia exata do fechamento MODEL-05:** phrasing-alvo travado; pequenos ajustes aceitos no checkpoint.
- **`fig-read` do CLOSE-03:** defere para checkpoint visual.
- **Atualização do STYLE.md §Inventário de slides:** ao fim da fase, atualizar tabela (linhas 108-132) com 4 novos sections + reposicionamentos; mover gap §Gaps reservados.

### Deferred Ideas (OUT OF SCOPE)

- `fig-read` insight de CLOSE-03 (defere para checkpoint).
- All-attempts AUC e Wilcoxon visíveis no MODEL-04 (fora do slide).
- Arquitetura completa Code-DKT (`codedkt_model_structure_ptbr.svg`) — reservada para documento TCC.
- Redesenho visual do `.slide-marker` — já resolvido em commit `5d44606`.
- Transição narrativa explícita slide-kcfig → CLOSE-01 — depende da fala.
- Caveat snippet pseudo-Python da AST SVG — não redesenhar.
- Visualizações alternativas MODEL-04 (`fig_comparison_bars_*.png`, `fig_seed_variance_boxplot.png`, etc.).
- Reduzir MODEL-05 para 3 etapas (override D-79f confirmado).
- MARKER-04 modificadores (fase 5).
- CLOSE-01/02 ajustes textuais (fora desta fase).

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (REQUIREMENTS.md) | Research Support |
|----|------------------------------|------------------|
| MODEL-01 | Code-DKT funcionamento + AST como inset visual; cronologia BKT (1995) → DKT (2015) → Code-DKT (2022); code2vec; vetorização via javalang | Shi et al. (2022) §3.2 (Code Representation, Model Input, Model Structure) confirma code2vec + AST + leaf-to-leaf paths + LSTM. `docs/figures/ast_codedkt_ptbr.svg` (560×620) exists, escalável a ~450×500. Cronologia BKT/DKT confirmada via Piech et al. (2015) §2.1 que cita Corbett & Anderson como HMM com binário. [VERIFIED: docs/Code-DKT.pdf, docs/deepKnowledgeTracing.pdf] |
| MODEL-03 | Reaproveita `slide-code` ("o que o code-dkt olha") já reformatado na fase 1; apenas confirma posição `#/17` após inserir MODEL-01 | Conferido no `index.html` linhas 379-428; nenhuma alteração de conteúdo. [VERIFIED: apresentacao/index.html] |
| MODEL-04 | Resultados Code-DKT lado a lado com Shi; A439 first=73,27% vs paper 75,74%; tabela ABNT em `.eda-grid` | Números confirmados em `results/comparison_table_first_auc.md`; Shi paper Table 2 confirma First Attempts A1 = 75.74% ± 0.69%. [VERIFIED: results/comparison_table_first_auc.md, docs/Code-DKT.pdf p.6 Table 2] |
| MODEL-05 | Introdução Duan (2025) + pipeline de 5 etapas; código bruto não AST; saída em slide-kcfig | Pipeline confirmado em `notebooks/03b_kc_generation.ipynb` cell 0 (5 etapas listadas literalmente); paper Duan §3.1 confirma 3 sub-etapas (KC gen + clustering Sentence-BERT/HAC + labeling). Override D-79f registra que nosso slide mostra 5 (envolvendo Sampling Etapa 1 e Q-matrix Etapa 5 ao redor das 3 do paper). [VERIFIED: notebooks/03b_kc_generation.ipynb, docs/AutomatedKC.pdf §3.1, Fig.1] |
| CLOSE-01 | Martins p2 (13 autores) reposicionado e reformatado na fase 1; citação direta literal mantida | Já no deck linhas 497-517; cabeçalho `> retomando o problema`; citação `(Martins; Marin; Alves, 2024, p. 19)` intacta. NÃO TOCAR. [VERIFIED: apresentacao/index.html] |
| CLOSE-02 | Martins p3 (10 autores) reposicionado e reformatado na fase 1; citação direta literal mantida | Já no deck linhas 520-538; cabeçalho `> retomando o problema`; citação `(Martins; Marin; Alves, 2024, p. 20)` intacta. NÃO TOCAR. [VERIFIED: apresentacao/index.html] |
| CLOSE-03 | Gráfico Code-DKT por dificuldade; reaproveita slide-fig; PENDING-04 picks 4 PNGs candidatos | 4 PNGs confirmados em `results/` (existem, gerados 2026-05-25 01:42-02:02); asset atual MD5=`89827663` = `fig_codedkt_curves_by_martins.png`. Comentário HTML linha 541 aponta a `fig_codedkt_difficulty_martins.png` (inconsistente com img real). [VERIFIED: results/fig_codedkt_*.png, apresentacao/assets/fig-codedkt-martins-curves.png, apresentacao/index.html L541/L547] |
| MARKER-03 | Slide marcador "Modelagem e Avaliação ✓"; reusa `.slide-marker` redesenhado | Componente CSS pronto em `theme-unifacens.css` L358-452 (commit `5d44606`); MARKER-02 markup é a base de cópia (linhas 333-374 do index.html). [VERIFIED: apresentacao/index.html, apresentacao/assets/theme-unifacens.css] |
| PENDING-04 | Validar gráfico Code-DKT antes de incluir; re-treino + pred_df alinhamento | Resolvido (D-83a): `results/codedkt_kc_retrained.pkl` (76MB, 2026-05-25 01:42) presente. Re-treino concluído antes do CONTEXT desta fase. [VERIFIED: results/codedkt_kc_retrained.pkl] |

</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Markup dos 4 slides novos | apresentacao/index.html (browser HTML) | — | reveal.js 5.1.0 renderiza direto; sem build system |
| Estilos reaproveitados (`.deck-topic`, `.slide-marker`, `.eda-grid`, `.bridge-seq`, `.wm`) | apresentacao/assets/theme-unifacens.css | — | tema único; todos os componentes já existem |
| Inset visual SVG (MODEL-01) | docs/figures/ast_codedkt_ptbr.svg | apresentacao/index.html (inline via `<img>` ou `<object>`) | SVG fica em `docs/figures/`; slide consome via `<img src="...">` relativo |
| PNGs CLOSE-03 candidatos | results/fig_codedkt_*.png | apresentacao/assets/ (asset escolhido copiado) | resultados em `results/`; slide consome via cópia para `assets/` |
| Fonte numérica MODEL-04 | results/comparison_table_first_auc.md | — | tabela canônica multirun 10 seeds; sem cálculo no slide |
| Fonte do pipeline MODEL-05 | notebooks/03b_kc_generation.ipynb | docs/AutomatedKC.pdf | notebook implementa as 5 etapas; paper Duan §3.1 fundamenta o phrasing |
| Validação visual | browser via `python3 -m http.server 8000` | — | sem build; recarregar página |

**Por que este mapa importa:** Nenhuma capability nesta fase atravessa runtime/backend — é puro front-end estático. O risco de mis-alocação é zero. O risco real é confundir **fonte do dado** (results/, docs/, notebooks/) com **destino visual** (apresentacao/), o que levaria a slides com dados não-reproduzíveis.

## Standard Stack

Stack 100% existente, zero dependências novas.

### Core

| Componente | Versão | Purpose | Why Standard |
|------------|--------|---------|--------------|
| reveal.js | 5.1.0 (CDN jsDelivr) | renderização do deck | já em uso desde a fase 1; sem motivo para mudar [VERIFIED: apresentacao/index.html L556] |
| theme-unifacens.css | local (project-specific) | tema visual UniFacens + paleta + componentes | construído ao longo das fases 1-3; todos os componentes necessários existem [VERIFIED: apresentacao/assets/theme-unifacens.css] |

### Supporting (apenas reusos, sem instalação)

| Asset | Path | Purpose | When to Use |
|-------|------|---------|-------------|
| AST inset SVG | `docs/figures/ast_codedkt_ptbr.svg` | inset visual MODEL-01 (coluna direita) | MODEL-01 only — escalar a ~450×500 via CSS |
| comparison_table_first_auc.md | `results/comparison_table_first_auc.md` | números canônicos MODEL-04 | MODEL-04 — copiar 3 linhas BKT/DKT/Code-DKT × 5 colunas |
| fig_codedkt_curves_by_martins.png | `results/` (= `assets/fig-codedkt-martins-curves.png`) | CLOSE-03 candidato 1 (atual) | default; 145.673 bytes, 2026-05-25 02:02 |
| fig_codedkt_difficulty_martins.png | `results/` | CLOSE-03 candidato 2 | 95.266 bytes, 2026-05-25 01:48 |
| fig_codedkt_kc_curves.png | `results/` | CLOSE-03 candidato 3 (28 curvas, 1 por KC) | 186.582 bytes, 2026-05-25 01:42 |
| fig_codedkt_level_vs_slope.png | `results/` | CLOSE-03 candidato 4 (scatter nível × inclinação) | 132.890 bytes, 2026-05-25 01:42 |

### Alternativas Consideradas

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `.bridge-seq` para 5 caixas (MODEL-05) | nova classe `.chrono-step` em theme-unifacens.css | `.bridge-seq` testado em 3 caixas (Yağcí slide); 5 caixas em 1280px exige `font-size: 17px` ou shrink. Recomendo tentar `.bridge-seq` antes; se quebrar, criar `.chrono-step` específico. |
| `.eda-grid` para tabela MODEL-04 | layout flex com 5 cards | `.eda-grid` é o padrão ABNT do projeto (D-66g herdado fase 3); cards quebrariam consistência visual com EDA-01. **Não considerar alternativa.** |
| PNG embutido no MODEL-04 | tabela HTML `.eda-grid` | PNG perde acessibilidade e exige regenerar a cada mudança numérica; HTML é mais robusto e consistente com EDA-01/02. **Não considerar.** |
| `codedkt_model_structure_ptbr.svg` no MODEL-01 | `ast_codedkt_ptbr.svg` (escolhido) | SVG completo (1180×640) tem fórmulas matemáticas, denso demais para defesa de 10 min. AST simples (560×620) é didático. **Locked por D-77d.** |

**Sem instalação:** todos os componentes são reuso. Nenhum `npm install`, `pip install`, dependência sistema, ou nova ferramenta exigida.

## Architecture Patterns

### System Architecture Diagram

```
[notebooks/06_code_dkt.ipynb] ──► [results/comparison_table_first_auc.md]
[notebooks/07_comparison.ipynb] ─┘                                       │
                                                                          ▼
                                                            [MODEL-04 .eda-grid HTML]
                                                                          │
[notebooks/03b_kc_generation.ipynb] ─► [results/qmatrix_A*.csv]          │
                                       [results/kc_descriptions_*.json]  │
                                                                          ▼
                                                            [MODEL-05 .bridge-seq HTML]
                                                                          │
[docs/figures/ast_codedkt_ptbr.svg] ─────────────────────────────────────┘
                                                                          │
                                                                          ▼
                                                            [MODEL-01 .deck-slide HTML]
                                                                          │
[results/fig_codedkt_*.png] ────► [apresentacao/assets/*.png] ───────────┤
                                                                          ▼
                                                            [CLOSE-03 .slide-fig HTML]
                                                                          │
                                                                          ▼
                                  [apresentacao/index.html (25 sections)]
                                                                          │
                                                                          ▼
                              [reveal.js 5.1.0 + theme-unifacens.css]
                                                                          │
                                                                          ▼
                                                   browser (http://127.0.0.1:8000)
                                                                          │
                                                                          ▼
                                                       checkpoint visual humano
```

**Componentes por papel:**

| Component | Role | File |
|-----------|------|------|
| 4 slides novos | sections HTML | `apresentacao/index.html` (insert) |
| Componentes CSS | classes reuso | `apresentacao/assets/theme-unifacens.css` (read-only) |
| AST inset | SVG estático | `docs/figures/ast_codedkt_ptbr.svg` (read-only) |
| PNG escolhido CLOSE-03 | imagem estática | `apresentacao/assets/fig-codedkt-martins-curves.png` (overwrite se trocar) |
| Validação | manual | browser local porta 8000 |

### Recommended Project Structure

```
apresentacao/
├── index.html          # ÚNICO arquivo HTML a editar
├── assets/
│   ├── theme-unifacens.css     # tema; ler para conferir componentes; NÃO editar (D-84a, D-67d herdado)
│   ├── fig-codedkt-martins-curves.png   # asset CLOSE-03 (substituir conforme escolha)
│   └── (outros assets EDA-03/04 inalterados)
└── STYLE.md            # atualizar ao fim da fase (D-91 / Claude's Discretion)

docs/figures/
└── ast_codedkt_ptbr.svg    # inset MODEL-01 (referência relativa do <img>)

results/
├── comparison_table_first_auc.md    # números canônicos MODEL-04 (read-only)
├── fig_codedkt_curves_by_martins.png    # candidato 1 CLOSE-03
├── fig_codedkt_difficulty_martins.png   # candidato 2
├── fig_codedkt_kc_curves.png            # candidato 3
└── fig_codedkt_level_vs_slope.png       # candidato 4
```

### Pattern 1: Reuso do componente `.slide-marker` (MARKER-03)

**What:** copy-paste o `<section>` do MARKER-02 (linhas 332-375 do index.html) e alterar 4 deltas mecânicos.

**When to use:** MARKER-03 — implementação 100% mecânica, zero CSS novo (D-84a).

**Deltas para MARKER-02 → MARKER-03:**

| Delta | MARKER-02 (linha) | MARKER-03 (novo) |
|-------|------------------|-------------------|
| 1. classe modificadora da section | `slide-marker--phase2` (L334) | `slide-marker--phase3` |
| 2. pill 3 (Modelagem) modificador | `marker-pill--running` + ícone `&#x21BB;` (L357-358) | `marker-pill--done` + ícone `&check;` |
| 3. pill 4 (Implantação) modificador | `marker-pill--pending` + ícone `&#x25CB;` (L365-366) | `marker-pill--running` + ícone `&#x21BB;` |
| 4. badges pill 3 + pill 4 | pill 3 `[running]` (L361), pill 4 `[]` empty (L369) | pill 3 `[done]`, pill 4 `[running]` (remover classe `marker-badge--empty`) |

Restante idêntico (título `> AS QUATRO FASES DA EDM`, marca d'água `<svg class="wm">`, rodapé `Fonte: adaptado de Zorić (2020).`). [VERIFIED: apresentacao/index.html L332-375]

```html
<!-- Source: apresentacao/index.html L332-375 (MARKER-02), com 4 deltas D-84b -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase3">
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
      <!-- pill 2 idêntica (done) -->
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done"><!-- DELTA 2 -->
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Modelagem e Avaliação</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--running"><!-- DELTA 3 -->
          <span class="marker-pill-icon">&#x21BB;</span>
          <span class="marker-pill-name">Implantação</span>
        </div>
        <span class="marker-badge">[running]</span>
      </div>
    </div>
    <p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

### Pattern 2: Tabela ABNT em `.eda-grid` (MODEL-04)

**What:** mesma estrutura HTML da tabela A1..A5 do EDA-01, com header diferente.

**When to use:** MODEL-04 — D-78e mandata `.eda-grid`; consistente com EDA-01 e EDA-02 (D-66g herdado fase 3).

**Considerações de layout (4 linhas × 6 colunas):**

- Header: `Modelo | A439 | A487 | A492 | A494 | A502`
- Linhas: BKT, DKT, Code-DKT, Shi (2022)*
- Última coluna em azul UniFacens (CSS já define `tr td:last-child` em L484); **MODEL-04 não destaca "melhor modelo por assignment"** porque o `.eda-grid` destaca apenas a última coluna (A502) por padrão. Isso é OK — D-78b não pede destaque per-célula.
- Asterisco em `Shi (2022)*` + nota explicativa em `.eda-source` ou caption próprio.

```html
<!-- Source: padrão derivado de apresentacao/index.html L246-271 (EDA-01) -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>code-dkt no csedm<span class="caret blink"></span></p>

    <p class="rel-lead">Comparamos os três modelos por <i>assignment</i> no <i>test set</i> do CSEDM Spring 2019; números são médias sobre 10 seeds.</p>

    <p class="eda-title">Tabela 2 &ndash; <i>First-attempt</i> AUC por modelo e <i>assignment</i> (%)</p>

    <table class="eda-grid">
      <thead>
        <tr><th>Modelo</th><th>A439</th><th>A487</th><th>A492</th><th>A494</th><th>A502</th></tr>
      </thead>
      <tbody>
        <tr><td>BKT</td><td>63,21</td><td>68,40</td><td>54,20</td><td>57,81</td><td>56,92</td></tr>
        <tr><td>DKT</td><td>75,56</td><td>76,70</td><td>82,05</td><td>80,17</td><td>80,78</td></tr>
        <tr><td>Code-DKT</td><td>73,27</td><td>79,56</td><td>86,12</td><td>81,85</td><td>84,98</td></tr>
        <tr><td>Shi (2022)*</td><td>75,74</td><td>&ndash;</td><td>&ndash;</td><td>&ndash;</td><td>&ndash;</td></tr>
      </tbody>
    </table>

    <p class="rel-lead" style="font-size: 18px; margin-top: 12px;">
      <i>* Paper Shi reporta apenas A1, equivalente a A439.</i>
      <i>First-attempt</i> AUC é a métrica primária: mede transferência entre problemas e evita autocorrelação intra-problema (Shi <i>et al.</i>, 2022, §5).
    </p>

    <p class="eda-source">Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.</p>
  </div>
</section>
```

**Decimal pt-BR:** vírgula como separador decimal (`75,74` não `75.74`). CSV/MD originais usam ponto — converter na transcrição.

### Pattern 3: Cronologia 3 chips + AST inset em 2 colunas (MODEL-01)

**What:** combinar `.bridge-seq` (3 chips horizontais) no topo + 2 colunas (texto/AST SVG) abaixo dentro do mesmo `.deck-slide`.

**When to use:** MODEL-01 — D-77b.

**Risco visual:** `.bridge-seq` foi testado com 3 chips em Yağcí slide e renderizou bem em 1280px. Manter 3 chips MODEL-01 fica dentro do limite testado.

**Microcópia das 3 caixas (alvo):**

| Chip 1 | Chip 2 | Chip 3 |
|--------|--------|--------|
| `BKT (1995)` | `DKT (2015)` | `Code-DKT (2022)` |
| Bayes / habilidades por KC | RNN / histórico sequencial | RNN + paths AST / code2vec |

Recomendação: 2 linhas dentro de cada `.step` (`<br>` entre nome+ano e descrição), font-size ≤ 18px para caber.

**Estrutura sugerida:**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <p class="deck-topic"><span class="ps1">&gt;</span>como o code-dkt funciona<span class="caret blink"></span></p>

    <!-- cronologia 3 chips: usar .bridge-seq do Yağcí (linhas 197-206 do CSS) -->
    <p class="bridge-seq" style="margin-top: 24px;">
      <span class="step"><b>BKT</b> (1995)<br><span style="font-size: 16px;">Bayes &middot; habilidades por KC</span></span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>DKT</b> (2015)<br><span style="font-size: 16px;">RNN &middot; histórico sequencial</span></span>
      <span class="arr">&rarr;</span>
      <span class="step"><b>Code-DKT</b> (2022)<br><span style="font-size: 16px;">RNN + paths AST &middot; <i>code2vec</i></span></span>
    </p>

    <!-- body 2 colunas: texto à esquerda, AST inset à direita -->
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
        <img src="../docs/figures/ast_codedkt_ptbr.svg" alt="AST com um caminho folha-a-folha entre input e &quot;valor&quot;" style="width: 100%; max-width: 420px; height: auto;">
      </div>
    </div>

    <p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
  </div>
</section>
```

**Path do SVG:** `../docs/figures/ast_codedkt_ptbr.svg` (relativo a `apresentacao/index.html`). Validar que reveal.js não bloqueia o path para fora de `apresentacao/` (deve ser ok porque é file://); se bloquear, **copiar** o SVG para `apresentacao/assets/ast_codedkt_ptbr.svg` e referenciar como `assets/ast_codedkt_ptbr.svg`. Recomendação: já copiar para `assets/` para portabilidade — não custa nada e evita pegadinha.

**AST SVG dimensões reais:** `viewBox="0 0 560 620"` (560 width × 620 height nativo). Escala para 420×465 mantendo proporção em `width: 420px; height: auto`. [VERIFIED: docs/figures/ast_codedkt_ptbr.svg L2]

### Pattern 4: Pipeline 5 etapas em `.bridge-seq` estendido (MODEL-05)

**What:** 5 caixas + 4 setas horizontais em `.bridge-seq` reusado.

**When to use:** MODEL-05 — D-79d.

**Risco visual:** o CSS de `.bridge-seq .step` define `flex: 1 1 0` (L202) — cada caixa ocupa 1/5 do total. Em 1280px com padding 64px, sobram ~1152px úteis. 5 caixas + 4 setas (16px × 4 = 64px) → ~1088px / 5 = ~218px por caixa. Apertado mas possível.

**Mitigação tipográfica:**
- `.step font-size` atual = 19px (L202); para 5 caixas pode precisar baixar para 16-17px
- Reduzir conteúdo de cada caixa: 1 verbo + 1 linha curta
- Setas `font-size: 22px` (vs 26px atual) para apertar mais

**Microcópia das 5 caixas (alvo D-79d, com encurtamento sugerido para caber):**

| # | Caixa | Forma compacta |
|---|-------|----------------|
| 1 | Sampling estratificado (n=5 por problema; Duan Tab. 5) | `Sampling`<br>`n=5/problema` |
| 2 | LLM gera KCs brutos do código bruto | `LLM`<br>`KCs brutos` |
| 3 | Clustering Sentence-BERT + HAC | `Clustering`<br>`Sentence-BERT + HAC` |
| 4 | Rotulagem dos clusters via LLM | `Rotulagem`<br>`LLM nos clusters` |
| 5 | Q-matrix por assignment (28 KCs / 50 problemas) | `Q-matrix`<br>`72 KCs / 50 problemas` |

**Atenção em "28 KCs":** D-79d diz "28 KCs / 50 problemas". Investigação:
- `results/qmatrix_A*.csv` tem 15+15+15+15+12 = **72 KCs por-assignment** (com possíveis nomes repetidos).
- Distintos por string-match: **70** (verificado via `kc_descriptions_A*.json`).
- Slide-kcfig (linhas 436-490 do index.html) mostra apenas **17 KCs** agrupados por 6 dificuldades Martins (3+3+3+3+3+2).
- "28 KCs" não corresponde a nenhuma contagem direta no projeto.

**Recomendação:** mudar a caixa 5 para `Q-matrix`<br>`KCs canônicos por assignment` (sem número), ou usar `~15 KCs/ass.` (faixa real é 12-15). O número exato é melhor não fixar no slide, porque o número canônico cross-assignment não foi consolidado no projeto. Se quiser número, usar **17 KCs canônicos** (= o que o slide-kcfig mostra), que é o número que o público vai ver imediatamente depois. Anotar no plano: **a caixa 5 precisa ser revista junto com microcópia do MODEL-05 no checkpoint**.

```html
<!-- Source: padrão derivado de apresentacao/index.html L143 (Yağcí .bridge-seq) -->
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

### Anti-Patterns to Avoid

- **Embutir PNG na MODEL-04 em vez de tabela HTML:** quebra consistência ABNT, dificulta atualização. (D-78e)
- **Criar classe nova `.chrono-step` antes de testar `.bridge-seq`:** viola "zero CSS novo se possível" herdado de D-67/D-84. Tentar reuso primeiro.
- **Citação direta literal nos 3 slides MODEL novos:** explicitamente proibido (D-86); só paráfrase com autor parentético.
- **Em-dash em qualquer prosa nova:** D-87 vinculante; converter para vírgula/dois-pontos/parênteses.
- **"Alunos" em prosa nova:** D-89 herdado; usar "estudantes" ou "discentes". Exceção apenas em citação direta literal (Martins p2/p3).
- **Mexer em CLOSE-01/02:** D-82 explícito; já fechados na fase 1.
- **Usar single-seed A439=72,55% em MODEL-04:** memória `project_codedkt_results` registra esse número; MODEL-04 usa multirun A439=73,27% (D-78g).
- **Citar Shi como `Shi (2022)` em texto sem `et al.`:** Shi tem 5 autores (Mao, Akram, Lytinen, Heffernan); usar `Shi <i>et al.</i> (2022)` ABNT.
- **Citar Duan como `Duan (2025)` em texto sem `et al.`:** Duan tem 7 autores (Fernandez, Hassany, Sampaio de Alencar, Brusilovsky, Akram, Lan); usar `Duan <i>et al.</i> (2025)`.

## Don't Hand-Roll

| Problema | Don't Build | Use Instead | Why |
|----------|-------------|-------------|-----|
| Componente de fases concluídas/em-execução/pendentes | Novo CSS `.fase-status` | `.slide-marker` + modificadores `--done` / `--running` / `--pending` | já existe e foi redesenhado em commit `5d44606` (CI/CD ABNT) |
| Tabela ABNT | `<table>` cru com `border-collapse` inline | `.eda-grid` + `.eda-title` + `.eda-source` | padrão ABNT/IBGE 1993 fixado em commit `aa69eb1` (fase 3) |
| Sequência horizontal de caixas | Novo `.chrono-step` ou `.pipeline-step` | `.bridge-seq` + `.step` + `.arr` (Yağcí slide) | testado em 3 caixas; 5 caixas pode caber com calibração tipográfica |
| Cabeçalho `> [seção]` | Novo `<h1>` ou `<h2>` | `.deck-topic` + `.ps1` + `.caret.blink` | padrão único do deck desde a fase 1; uso consistente em 21 slides |
| Marca d'água | Logo PNG | `<svg class="wm"><use href="#sym"/></svg>` | símbolo Facens já registrado no `<defs>` do HTML |
| Citação `(Autor, ano)` ABNT | Escrever `Shi (2022)` literal | `Shi <i>et al.</i> (2022)` ABNT D-88 | D-54 (fase 2) normalizou 8 ocorrências; precedente vinculante |
| Geração de PNGs CLOSE-03 | Script novo | `scripts/analyze_kc_difficulty_codedkt.py` (existe; gera os 4 candidatos) | já alinhado ao `codedkt_kc_retrained.pkl`; nada a regerar |
| Tabela first-attempt AUC | Recalcular notebook 07 | `results/comparison_table_first_auc.md` | tabela canônica multirun 10 seeds; pronta para transcrição |

**Key insight:** A fase 4 é **puramente de composição visual**. Toda a substância (números, figuras, vocabulário) está fixada em arquivos existentes. O risco está em (a) digitar números errados, (b) inventar componentes CSS, ou (c) violar uma das D-85..D-90 herdadas. Nenhum problema técnico novo aparece.

## Runtime State Inventory

| Categoria | Itens encontrados | Ação |
|-----------|------------------|------|
| Stored data | nenhum stored data muda nesta fase | none — fase 4 só escreve em `apresentacao/index.html` e talvez copia 1 PNG para `apresentacao/assets/` |
| Live service config | nenhum | none |
| OS-registered state | nenhum | none |
| Secrets/env vars | nenhum | none |
| Build artifacts | reveal.js carregado via CDN (jsDelivr); cache do browser pode servir CSS antigo | mitigação documentada no STYLE.md L160: "para forçar recarregar, suba em outra porta" |

**Conclusão:** rename/refactor inventory effectively empty — esta é fase de composição visual sobre arquivo único (`apresentacao/index.html`). Nada de runtime state externo é tocado.

## Common Pitfalls

### Pitfall 1: Confundir Shi paper A1=A439 com qualquer outro assignment

**What goes wrong:** colocar números de A2-A5 atribuídos ao paper Shi.
**Why it happens:** o paper Shi reporta detalhadamente apenas A1 (Table 2) e mostra A1-A5 overall AUC em Table 1, sem first-attempt para A2-A5.
**How to avoid:** linha "Shi (2022)*" da tabela MODEL-04 deve ter `&ndash;` (en-dash HTML, traço médio) nas colunas A487-A502, e o asterisco/caption deve explicitar "Paper Shi reporta apenas A1, equivalente a A439."
**Warning signs:** qualquer número >0 nessas 4 células sem citação clara.
[VERIFIED: docs/Code-DKT.pdf p.6 Tables 1+2]

### Pitfall 2: Misturar números single-seed e multirun

**What goes wrong:** usar 72,55% para Code-DKT A439 (single-seed, memória `project_codedkt_results`) em vez de 73,27% (multirun, `comparison_table_first_auc.md`).
**Why it happens:** memória inicial salvou single-seed; multirun veio depois.
**How to avoid:** consultar SEMPRE `results/comparison_table_first_auc.md` como fonte canônica. D-78g trava 73,27%.
**Warning signs:** número diferente de 73,27% para Code-DKT A439.
[VERIFIED: results/comparison_table_first_auc.md]

### Pitfall 3: Identificar errado o paper Duan vs srcML-DKT

**What goes wrong:** o CONTEXT L172 cita `docs/2025.EDM.short-papers.83.pdf` como Duan paper alternativo. NÃO É. Esse paper é **srcML-DKT (Pankiewicz, Shi, Baker, 2025)**, o paper alvo da Fase 2 de srcML do nosso projeto (out of scope da apresentação).
**Why it happens:** ambos são papers EDM 2025; confusão de filename.
**How to avoid:** Duan está em `docs/AutomatedKC.pdf` SOMENTE. Confirmar título "Automated Knowledge Component Generation for Interpretable Knowledge Tracing in Coding Problems" antes de citar.
**Warning signs:** qualquer phrasing que misture "Pankiewicz", "Baker" ou "srcML" no contexto do MODEL-05.
[VERIFIED: docs/AutomatedKC.pdf p.1 title; docs/2025.EDM.short-papers.83.pdf p.541 title]

### Pitfall 4: Citar "pipeline em 3 etapas" no MODEL-05 (alinhado ao paper)

**What goes wrong:** Duan paper §3.1 explicitamente descreve **3 etapas** (Figura 1 caption: "three-step automated KC generation"). Nosso slide diz **5 etapas**. Se a banca conferir o paper, há divergência.
**Why it happens:** nosso notebook 03b expande o pipeline com Sampling (Etapa 1) e Q-matrix (Etapa 5) ao redor das 3 do paper.
**How to avoid:** o phrasing-alvo D-79c "Construímos um pipeline de cinco etapas para extrair KCs do CSEDM" deixa claro que **nós construímos** (paráfrase autoral, não citação literal de Duan). Tab. 4 e Tab. 5 do paper são citadas como justificativas pontuais (código bruto, n=5), não como esquema geral. Isso é consistente com D-86 (voz autoral).
**Warning signs:** qualquer phrasing tipo "Duan propõe 5 etapas" — isso é factualmente errado. "Duan propõe um pipeline LLM para extrair KCs" é OK; "nós implementamos em 5 etapas" é OK.
[VERIFIED: docs/AutomatedKC.pdf Fig.1 caption "three-step"]

### Pitfall 5: "28 KCs / 50 problemas" no MODEL-05

**What goes wrong:** D-79d sugere "Q-matrix · 28 KCs / 50 problemas" na 5ª caixa do pipeline. O número 28 não corresponde a nenhuma contagem real:
- 5 assignments × 12-15 KCs canônicos = **72 KCs com possíveis duplicatas**
- Distintos por string match: **70**
- Slide-kcfig mostra **17 KCs** (3+3+3+3+3+2 agrupados por 6 dificuldades Martins)

**Why it happens:** "28 KCs" pode ter origem em algum cálculo intermediário ou estimativa antiga; investigação não localizou fonte canônica.

**How to avoid:** opções recomendadas para a 5ª caixa, em ordem de preferência:
1. **Sem número:** `Q-matrix` / `por assignment` — neutro, alinha-se a "extração automática" sem se comprometer com contagem
2. **Faixa real:** `Q-matrix` / `12-15 KCs/ass.`
3. **Match com slide-kcfig:** `Q-matrix` / `17 KCs canônicos` (mas isso é cross-assignment agregado por dificuldade, não o número técnico)

**Warning signs:** "28 KCs" no slide final. Pedir confirmação do usuário no checkpoint.
[VERIFIED: results/qmatrix_A*.csv, results/kc_descriptions_A*.json, apresentacao/index.html L436-490]

### Pitfall 6: Caminho relativo do SVG AST quebra no reveal.js

**What goes wrong:** `<img src="../docs/figures/ast_codedkt_ptbr.svg">` em `apresentacao/index.html` pode não resolver em alguns servers ou se `apresentacao/` for servido como root.
**Why it happens:** `python3 -m http.server 8000` rodado em `apresentacao/` serve `apresentacao/` como root; `..` sai para `repositories/studies/tcc.edm.kt/` o que não é servido.
**How to avoid:** copiar o SVG para `apresentacao/assets/ast_codedkt_ptbr.svg` e usar `<img src="assets/ast_codedkt_ptbr.svg">`. Mantém o arquivo dentro do escopo servido.
**Warning signs:** SVG não aparece no browser; console DevTools mostra 404.
[VERIFIED: pattern aplicado em fig-codedkt-martins-curves.png que está em `apresentacao/assets/` por essa razão]

### Pitfall 7: 5 chips em `.bridge-seq` 1280px quebra layout

**What goes wrong:** CSS atual do `.bridge-seq` foi calibrado para 3 caixas (Yağcí). Com 5 caixas, cada uma fica com ~218px (1280 - 128 padding - 64 setas / 5), texto pode estourar ou caixas ficarem visualmente desbalanceadas.
**Why it happens:** `flex: 1 1 0` distribui igualmente, mas o conteúdo pode ser maior que a caixa.
**How to avoid:**
1. Reduzir `font-size` da `.step` no MODEL-05 para 16-17px (CSS atual: 19px, L202)
2. Usar `<br>` para 2 linhas por caixa (verbo na 1ª, descrição na 2ª)
3. Encurtar texto por caixa para ≤ 18 caracteres por linha
4. Se mesmo assim quebrar: criar `.chrono-step` específico em `theme-unifacens.css` com padding/font menores (último recurso)

**Warning signs:** texto cortado, caixas com alturas diferentes, setas desalinhadas.
[NOT YET VERIFIED no browser — risco MÉDIO]

### Pitfall 8: Vírgula vs ponto decimal em pt-BR

**What goes wrong:** `results/comparison_table_first_auc.md` usa ponto decimal (formato Python pandas). Slide ABNT pt-BR usa vírgula.
**Why it happens:** transcrição direta sem conversão.
**How to avoid:** converter explicitamente cada número na transcrição. EDA-01 e EDA-02 já usam vírgula (`23,68%`, `93,46%`) — manter consistência.
**Warning signs:** `73.27%` ou `75.74%` no slide.
[VERIFIED: apresentacao/index.html L261-265 usa vírgula]

### Pitfall 9: Comentário HTML linha 541 aponta a filename errado

**What goes wrong:** linha 541 diz `<!-- figura: results/fig_codedkt_difficulty_martins.png -->` mas a `<img>` real (L547) carrega `assets/fig-codedkt-martins-curves.png` (= `results/fig_codedkt_curves_by_martins.png` por MD5). Comentário e código divergem.
**Why it happens:** edição anterior trocou a figura mas não o comentário.
**How to avoid:** plan de CLOSE-03 (D-83c) deve incluir explicitamente a correção do comentário linha 541 ao apontar para o filename escolhido no checkpoint.
**Warning signs:** comentário ainda dizendo `fig_codedkt_difficulty_martins.png` ao fim da fase.
[VERIFIED: apresentacao/index.html L541, L547]

## Code Examples

Verified patterns from existing slides:

### Exemplo 1: deck-topic com caret blink (cabeçalho `> [seção]`)

```html
<!-- Source: apresentacao/index.html L233 (INTRO-01) -->
<p class="deck-topic"><span class="ps1">&gt;</span>o dataset csedm<span class="caret blink"></span></p>
```

### Exemplo 2: tabela ABNT `.eda-grid` completa

```html
<!-- Source: apresentacao/index.html L254-269 (EDA-01) -->
<p class="eda-title">Tabela 1 &ndash; Taxa de acerto por <i>assignment</i> (Spring 2019)</p>

<table class="eda-grid">
  <thead>
    <tr><th>Assignment</th><th>Alunos</th><th>Participação</th><th>Problemas</th><th>Taxa de acerto</th></tr>
  </thead>
  <tbody>
    <tr><td>A1 (439)</td><td>386</td><td>93,46%</td><td>10</td><td>26,15%</td></tr>
    <!-- ... -->
  </tbody>
</table>

<p class="eda-source">Fonte: elaborado pelo autor sobre CSEDM (Spring 2019).</p>
```

### Exemplo 3: `.bridge-seq` com 3 caixas (Yağcí)

```html
<!-- Source: apresentacao/index.html L143 (Yağcí .bridge-seq) -->
<p class="bridge-seq">
  <span class="step">mineração de dados educacionais</span>
  <span class="arr">&rarr;</span>
  <span class="step">predição de desempenho</span>
  <span class="arr">&rarr;</span>
  <span class="step"><i>knowledge tracing</i></span>
</p>
```

### Exemplo 4: marca d'água Facens (presente em todos os slides de conteúdo)

```html
<!-- Source: apresentacao/index.html L186 (qualquer slide) -->
<svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
```

### Exemplo 5: rodapé Fonte: padrão

```html
<!-- Source: apresentacao/index.html L241 (INTRO-01) -->
<p class="rel-cite">Fonte: Price (2020); CSEDM 2021.</p>

<!-- Source: apresentacao/index.html L328 (EDA-02) com adaptado de -->
<p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
```

### Exemplo 6: section completa MARKER-02 (base de cópia para MARKER-03)

Já mostrado em `Pattern 1`. Linhas 332-375 de `apresentacao/index.html`.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Tópico + título h2 + subtítulo `.rel-sub` em cada slide | Cabeçalho `> [seção]` único via `.deck-topic` | Fase 1 (commits `c31658c`, `23eed8b`, `b60439e`, ...) | obrigatório em todos os slides de conteúdo (STYLE.md L37-60) |
| Tabela com bordas verticais ou PNG embutido | `.eda-grid` ABNT/IBGE 1993 (3 bordas horizontais, fundo transparente) | Fase 3 (commit `aa69eb1`) | padrão para todas as tabelas em slides |
| `.slide-marker` versão antiga (caixas arredondadas) | Pipeline CI/CD ABNT (4 retângulos + ícones + badges) | Fase 3 (commit `5d44606`) | MARKER-01/02/03/04 todos usam o mesmo componente |
| `Shi (2022)` no texto | `Shi <i>et al.</i> (2022)` ABNT | Fase 2 (D-54, commit `4a9af6e`) | 8 ocorrências normalizadas; precedente vinculante |
| "Alunos" em prosa | "Estudantes" | Fase 3 (D-67e, feedback) | 10 substituições; D-89 herdado |
| Em-dash (—) em prosa | Vírgula/dois-pontos/parênteses | Fase 1 (D-44, feedback) | memória `feedback_no_em_dashes` vinculante |

**Deprecated/outdated:**

- **Single-seed A439=72,55%** (memória `project_codedkt_results`): substituído por multirun A439=73,27% (D-78g). NÃO usar no slide.
- **PROJECT.md "pipeline em 3 etapas"** (NEW-09/D-66): overrideu para 5 etapas (D-79f) por fidelidade ao notebook 03b. Documentado.
- **`docs/2025.EDM.short-papers.83.pdf` como paper Duan alternativo** (CONTEXT L172): identificação errada. É srcML-DKT (Pankiewicz et al., 2025), out of scope. **Não usar para Duan refs.**

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `.bridge-seq` com 5 caixas em 1280px cabe com `font-size: 17px` e quebra `<br>` | Pattern 4, Pitfall 7 | Médio: pode exigir criar `.chrono-step` em CSS (não bloqueante; só atrasa MODEL-05) |
| A2 | Path `../docs/figures/ast_codedkt_ptbr.svg` quebra; copiar para `apresentacao/assets/` é a solução robusta | Pattern 3, Pitfall 6 | Baixo: cópia trivial; se path relativo funcionar, é overhead mínimo |
| A3 | Número "28 KCs" do D-79d não tem origem documentada; recomendo "12-15 por assignment" ou remover número | Pitfall 5 | Médio: requer confirmação do usuário no checkpoint; afeta phrasing da 5ª caixa do pipeline |
| A4 | Pill 4 `--running` no MARKER-03 sinaliza "Implantação em curso" pedagogicamente; assume que TCC 2 segue na narrativa | D-84b confirmado em CONTEXT | Baixo: D-84b já trava isso |
| A5 | Linha "Shi (2022)*" deve usar `&ndash;` (en-dash) nas colunas A487-A502 — encaixa visualmente em tabela ABNT | Pattern 2 | Baixo: padrão visual standard; outras opções (`-`, `n/a`, vazio) também funcionam |
| A6 | Footnote/asterisco explicando "Shi reporta apenas A1=A439" deve aparecer próximo da tabela MODEL-04 | Pattern 2 | Baixo: D-78b explicita o caption; D-78d já cobre |

**Confirmação necessária no checkpoint:** A3 (número de KCs no MODEL-05 caixa 5).

## Open Questions

1. **Número exato de KCs na 5ª caixa do pipeline MODEL-05**
   - What we know: Q-matrices têm 12-15 KCs por assignment (5 assignments × 12-15); slide-kcfig mostra 17 KCs agrupados.
   - What's unclear: origem do "28" mencionado em D-79d.
   - Recommendation: usar "Q-matrix / por assignment" sem número OU "12-15 KCs/ass." OU "17 KCs canônicos". Confirmar com usuário no checkpoint visual.

2. **5 caixas em `.bridge-seq` cabem em 1280×720?**
   - What we know: 3 caixas cabem (Yağcí); cálculo de espaço sugere ~218px/caixa em 5; calibração tipográfica ajuda.
   - What's unclear: visualmente confortável ou apertado demais.
   - Recommendation: implementar primeiro com `font-size: 17px` + `<br>`; validar no browser durante checkpoint; criar `.chrono-step` apenas se quebrar.

3. **Path do SVG: relativo `../docs/figures/` ou cópia para `apresentacao/assets/`?**
   - What we know: PNG do CLOSE-03 já está em `assets/` (copiado de `results/`).
   - What's unclear: se reveal.js + http.server toleram `..`.
   - Recommendation: copiar SVG para `apresentacao/assets/ast_codedkt_ptbr.svg` por consistência e robustez. Custo zero.

4. **Ponte narrativa slide-kcfig → CLOSE-01 (D-deferred)**
   - What we know: D-deferred indicou que o salto pode soar abrupto; CLOSE-01 abre com "retomando o problema" sem ponte explícita do slide anterior.
   - What's unclear: se durante o checkpoint humano isso vai pedir microcópia.
   - Recommendation: NÃO criar requirement; deixar para a fala do orador. Se o checkpoint sinalizar, ajustar microcópia de slide-kcfig (fechar com 1 frase tipo "Mas o problema reportado na literatura...") ou abertura do CLOSE-01.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` | servir o deck localmente | ✓ | (default sistema) | `npx http-server` |
| `python3 -m http.server` | servir HTML estático | ✓ | stdlib | qualquer HTTP server local |
| browser (Chrome/Firefox) | renderizar reveal.js | ✓ | qualquer recente | — |
| `git` | commits dos slides | ✓ | qualquer 2.x | — |
| reveal.js 5.1.0 | runtime | ✓ via CDN | jsDelivr | local copy se offline (não esperado) |
| `docs/figures/ast_codedkt_ptbr.svg` | inset MODEL-01 | ✓ | 4302 bytes | usar `fig4_ast_javalang.png` (300KB, similar conceito) — última alternativa |
| `results/comparison_table_first_auc.md` | números MODEL-04 | ✓ | 9 linhas | regerar via `notebooks/07_comparison.ipynb` se ausente |
| `results/codedkt_kc_retrained.pkl` | PENDING-04 base | ✓ | 76MB | — |
| 4 PNGs candidatos CLOSE-03 | escolha visual | ✓ todos | 95-186KB | — |

**Missing dependencies with no fallback:** nenhum.
**Missing dependencies with fallback:** nenhum.

## Security Domain

Não aplicável. Esta fase produz **apenas HTML estático** (`apresentacao/index.html`) e copia 1 PNG de `results/` para `apresentacao/assets/`. Nenhum input do usuário, nenhuma autenticação, nenhum dado sensível, nenhuma comunicação de rede. ASVS não se aplica.

## Project Constraints (from CLAUDE.md)

Diretivas vinculantes extraídas de `./CLAUDE.md`:

1. **Iteração ativa = apresentação de defesa GSD em `apresentacao/`** — único alvo desta fase é o HTML do deck.
2. **Cabeçalho novo dos slides: `> [nome da seção]` com caret piscando** substitui tópico ("trabalhos correlatos") e título h2 (nome do autor); única menção ao autor é o rodapé "Fonte:".
3. **Toda alteração em `apresentacao/` deve respeitar `apresentacao/STYLE.md`** (tipografia Arial, paleta UniFacens, slide 1280×720).
4. **Citações ABNT seguindo manual MSGQ-21.01 em `apresentacao/`**; "tradução nossa" só em direta literal estrangeira; **sem em-dash em prosa**.
5. **Antes de redigir ou alterar slide que cite um autor, ler a referência completa em `docs/`** (este é um trabalho científico, vinculante).
6. **Commits atômicos por slide concluído**; cada fase termina com `apresentacao/index.html` navegável no browser.
7. **Knowledge Component (KC) = `ProblemID`** no protocolo Shi; um modelo por assignment.
8. **First-attempt AUC primária + all-attempts AUC secundária** — MODEL-04 mostra apenas first-attempt (D-78c).
9. **Sequências truncadas em 50 tentativas, SEED=42 fixo** — não tocado nesta fase (só apresentação).
10. **Critério 1: Code-DKT A1 ~74% ±3%** — MODEL-04 mostra 73,27% (delta -2,47pp), dentro do gate.

Compliance check: planner deve verificar que (a) os 4 slides novos seguem `.deck-topic` (item 2); (b) tipografia Arial/Cascadia respeita STYLE.md (item 3); (c) ABNT com `<i>et al.</i>` e sem em-dash (item 4); (d) Code-DKT (Shi), Duan, Corbett, Piech foram lidos via PDF antes do phrasing (item 5 — feito por este RESEARCH); (e) commit por plan (item 6); (f) número 73,27% para A439 (item 10).

## Sources

### Primary (HIGH confidence)

- **`docs/Code-DKT.pdf`** (Shi, Mao, Akram, Lytinen, Heffernan, 2022) — §3 DKT formalism, §3.2 Code-DKT model (code2vec + AST paths + attention + LSTM), §4.1 dataset (410 students, 23.68% correct, 4:1 train:test), §5.1.3 first-attempt rationale (perfeito para D-78d caption), Table 1 (A1-A5 overall AUC), Table 2 (A1 First Attempts = 75.74% ± 0.69%). [VERIFIED via Read pages 4-7]
- **`docs/AutomatedKC.pdf`** (Duan, Fernandez, Hassany, Sampaio de Alencar, Brusilovsky, Akram, Lan, 2025) — §3.1 KCGen-KT pipeline (3 etapas: KC Generation, Clustering Sentence-BERT+HAC, Labeling), §3.1.2 HAC com cosine similarity, §3.1.3 Labeling chain-of-thought GPT-4o, Figure 1 caption "three-step automated KC generation pipeline", §5.1 (Tab. 5 ablação n=5 sampling), §5.1.3 (Tab. 4 ablação Student Code→AST hurts performance). [VERIFIED via Read pages 3-7]
- **`docs/deepKnowledgeTracing.pdf`** (Piech, Bassen, Huang, Ganguli, Sahami, Guibas, Sohl-Dickstein, 2015) — §2.1 BKT como HMM com binário (Corbett & Anderson reference), §Introduction define DKT como aplicação de RNN ao tracing. [VERIFIED via Read pages 1-2]
- **`results/comparison_table_first_auc.md`** — números canônicos multirun 10 seeds; Code-DKT A439=73.27%, A487=79.56%, A492=86.12%, A494=81.85%, A502=84.98%. [VERIFIED via Read]
- **`apresentacao/index.html`** — markup atual (696 linhas, 21 sections); âncoras de inserção; conteúdo CLOSE-01/02/03 e slide-code/slide-kcfig confirmados. [VERIFIED via Read + grep]
- **`apresentacao/assets/theme-unifacens.css`** — componentes `.slide-marker` (L358-452), `.bridge-seq` (L197-210), `.eda-grid` (L466-490), `.deck-topic` confirmados. [VERIFIED via Read]
- **`apresentacao/STYLE.md`** — inventário pós-fase 3 (21 slides), gaps reservados, tipografia, paleta. [VERIFIED via Read]
- **`docs/figures/ast_codedkt_ptbr.svg`** — viewBox 560×620, conteúdo (pseudo-Python intencional, caveat em D-77f). [VERIFIED via Read]
- **`notebooks/03b_kc_generation.ipynb`** cell 0 — pipeline de 5 etapas explicitamente listado; cell 20 confirma "12-15 KCs canônicos por assignment". [VERIFIED via Bash grep + json parsing]

### Secondary (MEDIUM confidence)

- **`results/qmatrix_A*.csv`** + **`results/kc_descriptions_A*.json`** — contagem real de KCs canônicos por assignment (15/15/15/15/12 = 72 com possíveis duplicatas; 70 distintos por string-match). [VERIFIED via Bash count]
- **`results/fig_codedkt_*.png`** — 4 PNGs candidatos CLOSE-03 existem com timestamps 2026-05-25 01:42-02:02; MD5 do candidato 1 = asset atual. [VERIFIED via ls + md5sum]
- **`.planning/phases/03-eda-e-pr-processamento-fase-2-edm/PHASE-SUMMARY.md`** — componentes `.eda-grid`, `.eda-fig`, `.eda-source`, `.eda-insight` consolidados; reuso recomendado. [VERIFIED via Read]
- **`.planning/phases/01-reformata-o-da-base/01-CONTEXT.md`** — D-16/D-17 fixam ordem dos slides no fim do deck; D-25 voz padrão. [VERIFIED via Read]

### Tertiary (LOW confidence, flagged)

- **`docs/2025.EDM.short-papers.83.pdf`** — CONTEXT L172 cita como paper Duan alternativo. **Identificação errada**: é srcML-DKT (Pankiewicz, Shi, Baker, 2025). Out of scope para MODEL-05. Documentado como Pitfall 3. [VERIFIED via Read p.541 title]
- **"28 KCs / 50 problemas" em D-79d (MODEL-05 caixa 5)** — origem não localizada; investigação inconclusiva. Documentado como Pitfall 5 e Assumption A3. [NOT VERIFIED — recomendar checkpoint]
- **Layout `.bridge-seq` com 5 caixas em 1280px** — não testado em browser nesta fase; cálculo de espaço sugere viável com calibração tipográfica. Documentado como Pitfall 7 e Assumption A1. [NOT VERIFIED — risco médio]

## Metadata

**Confidence breakdown:**

- **Stack & componentes CSS:** HIGH — todos os componentes existem e foram verificados via Read do CSS + comparação com slides existentes.
- **Números MODEL-04:** HIGH — `comparison_table_first_auc.md` é a fonte canônica do projeto (multirun 10 seeds), confirmado via paper Shi Table 2 (75.74% A1 First Attempts).
- **Phrasing Code-DKT (MODEL-01, MODEL-03):** HIGH — paper Shi §3.2 e §5 lidos integralmente; bullets do D-77c (`javalang → AST`, `code2vec → paths`, `atenção`, `LSTM`) são paráfrase fiel sem citação literal.
- **Phrasing Duan (MODEL-05):** MEDIUM-HIGH — paper §3.1 e §5.1 lidos; nuance "3 etapas no paper vs 5 no slide" documentada como Pitfall 4; phrasing-alvo "Construímos um pipeline de cinco etapas" é autoral, juridicamente correto.
- **MARKER-03 implementação:** HIGH — componente CSS 100% pronto, 4 deltas mecânicos sobre MARKER-02; padrão idêntico a fase 3.
- **CLOSE-03 picks:** HIGH para existência dos 4 PNGs (verificados); MEDIUM para qual será escolhido (decisão visual do usuário).
- **`.bridge-seq` 5 caixas:** MEDIUM — risco visual não testado.
- **Cronologia BKT/DKT/Code-DKT em 3 chips:** HIGH — fontes Piech §2.1 + Corbett (referência em Piech) + Shi §3.2 confirmam datas/métodos.

**Research date:** 2026-05-28
**Valid until:** 2026-06-15 (apresentação é trabalho temporal de defesa; sem dependências externas voláteis; datas de validade longas não fazem sentido aqui)

---

*Phase: 4-Modelagem e Avaliação (Fase 3 EDM)*
*Researched: 2026-05-28*
