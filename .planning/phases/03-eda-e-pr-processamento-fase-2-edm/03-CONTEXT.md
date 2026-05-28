# Phase 3: EDA e Pré-processamento (Fase 2 EDM) - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Inserir 4 slides novos em `apresentacao/index.html`, todos posicionados após o slide MARKER-01 (atual `#/10`) e antes do `slide-code` (atual `#/11`, futuro MODEL-03 da fase 4). Os 4 slides fecham a Fase 2 da EDM (Preparação dos Dados) na narrativa da defesa:

1. **EDA-01** ("como navegamos o CSEDM"): hub narrativo + tabela/cards A1..A5 com distribuição interna do dataset (n alunos, n problemas, taxa de acerto por assignment); NÃO repete os totais globais já apresentados em INTRO-01.
2. **EDA-02** ("pré-processamento"): justifica aproximação ao protocolo de Shi como parâmetro de comparação e lista 2 etapas concretas (filtro `min_attempts ≥ 3` resultando em 410 alunos; truncagem nas últimas 50 tentativas). Comunica a ponte explícita 413 (CSEDM bruto) → 410 (filtro Shi) → 328 treino / 82 teste.
3. **EDA-03** ("perfis dos alunos"): scatter PCA 2D com 3 clusters K-Means (Alto desempenho / Médio / Em risco). Insight central: cluster "Em risco" é maioritário (~55%) e tem alta taxa de acerto eventual MAS pouco engajamento (2-4,6 tentativas/assignment) — em risco não é quem erra, é quem desiste cedo.
4. **MARKER-02** ("Preparação dos Dados ✓"): reusa o componente `.slide-marker` redesenhado em 2026-05-28 (pipeline CI/CD ABNT). Modificadores: pill 1 (Definição) `--done`, pill 2 (Preparação) `--done`, pill 3 (Modelagem) `--running`, pill 4 (Implantação) `--pending`.

Resultado da fase: deck navega do primeiro ao MARKER-02 sem quebra; padrão `> [seção]` aplicado nos 3 slides EDA com cabeçalho temático; voz própria (paráfrase com autor parentético) preservada; nenhum slide existente é alterado exceto pela inserção dos 4 sections na posição correta. Nada de Code-DKT, modelagem ou KCs aqui (fase 4).

Total esperado de sections no `<div class="slides">` ao fim da fase: 16 (pós-fase 2) + 4 (novos) = **20 sections**.

</domain>

<decisions>
## Implementation Decisions

### Posição no DOM (D-60)

- **D-60:** Os 4 slides entram **após o slide 10 (MARKER-01)** e **antes do atual slide 11 (`slide-code`, futuro MODEL-03)**. Ordem dentro do bloco: EDA-01 → EDA-02 → EDA-03 → MARKER-02.
- **D-61:** Esta posição já está consistente com `apresentacao/STYLE.md` §Gaps reservados linha 130 ("Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02"); nenhuma correção do STYLE.md é necessária nesta fase. Após inserção, slide-code passa de `#/11` para `#/15`; demais slides existentes deslocam +4.
- **D-62:** Justificativa narrativa: MARKER-01 fecha a Fase 1 EDM com "Definição do Problema ✓"; EDA-01 abre dizendo "agora navegamos o dataset que descrevemos no INTRO-01"; EDA-02 mostra as decisões de pré-processamento; EDA-03 entrega o insight; MARKER-02 fecha a Fase 2 EDM. Sequência metodológica encadeada.

### Cabeçalhos temáticos (D-63)

- **D-63a (EDA-01):** cabeçalho em aberto; gsd-planner propõe (sugestão neutra: `> como navegamos o csedm` ou `> o curso por dentro`). Decisão de phrasing final fica no plan/checkpoint visual.
- **D-63b (EDA-02):** cabeçalho em aberto; gsd-planner propõe (sugestão neutra: `> pré-processamento` ou `> aproximação ao protocolo`). Decisão no plan/checkpoint visual.
- **D-63c (EDA-03):** cabeçalho em aberto; gsd-planner propõe (sugestão neutra: `> perfis dos alunos` ou `> três jeitos de aprender`). Decisão no plan/checkpoint visual.
- **D-63d (MARKER-02):** sem `.deck-topic` no padrão `> [seção]`; herda exatamente o layout do MARKER-01 redesenhado (D-34d da fase 2 mantido); o título dentro do slide continua sendo `> AS QUATRO FASES DA EDM` em Arial bold 24px via classe `.marker-title`.

### EDA-01 — conteúdo e formato (D-64)

- **D-64 (combo narrativo + distribuição A1..A5):** EDA-01 combina um parágrafo curto ("hub narrativo": encontramos a base via Shi, primeira inspeção mostrou heterogeneidade entre os 5 assignments) com uma tabela/cards horizontais por assignment. Colunas mínimas: assignment (A1..A5 / 439/487/492/494/502), n alunos, n problemas, taxa de acerto. Insight observável sem repetir contagens globais de INTRO-01.
- **D-64a (números a usar):** valores do `docs/eda_insights.md` Seção 1.1 (Release/Train, 246 alunos): A1 233/27,3%, A2 224/20,3%, A3 234/19,1%, A4 221/25,2%, A5 222/30,4%. **Atenção:** estes valores são Release/Train, não MainTable+protocolo Shi. **gsd-planner valida** se os mesmos números se sustentam no split que EDA-02 vai comunicar (MainTable + filtro Shi, 410 alunos); se divergirem >5%, regenerar com pandas direto do MainTable Spring 2019. A escolha do split em EDA-02 (D-65) afeta este slide.
- **D-64b (calibração de densidade):** combo pode ficar com elementos demais; gsd-planner começa com versão enxuta (parágrafo de 2-3 linhas + 5 cards horizontais ou tabela compacta) e o reviewer humano ajusta no checkpoint visual. Padrão herdado da fase 2: iterações textuais pós-checkpoint são esperadas (média 2 por slide).
- **D-64c (sem repetir INTRO-01):** os números globais já mostrados em INTRO-01 (413 estudantes, 5 assignments × 10 problemas, 201 mil eventos, 6 colunas-chave) **NÃO** voltam em EDA-01. O slide entra direto na granularidade por assignment.

### EDA-02 — split e etapas (D-65)

- **D-65 (split a comunicar):** protocolo Shi (D-38b da fase 2 mandata): **413 (CSEDM bruto) → 410 (filtro `min_attempts ≥ 3`) → 328 treino / 82 teste (split 80/20, random_state=1)**. Liga direto com MODEL-04 da fase 4 (A439 first_auc=72,55%, dentro de ±3% do paper). Coerente com CLAUDE.md (dataset primário = MainTable + protocolo Shi). NÃO mencionar Release/Train (decisão histórica abandonada; comentário fica para banca se perguntar).
- **D-65a (etapas listadas):** 2 etapas concretas após o split:
  1. **Filtro `min_attempts ≥ 3`** — descarta alunos com menos de 3 tentativas Run.Program globais; resulta em 410 alunos (de 413). Justificativa: sequência KT útil exige histórico mínimo.
  2. **Truncagem em 50 últimas tentativas** — limite computacional do LSTM e foco no estado mais recente. Insight: mediana é 32, mas P95=109 e máximo=272; 28% dos pares (aluno, assignment) excedem 50.
- **D-65b (etapas que NÃO entram em EDA-02):**
  - Threshold binário `correct = (Score == 1.0)` — decisão metodológica que pode ser mencionada na voz da seção 4 do BKT (fase 4) ou implícita em "tratam respostas como corretas/incorretas". gsd-planner decide se cabe 1 linha aqui.
  - Separação Run.Program vs Compile.Error — pertence à fase 4 (Code-DKT). EDA-02 não toca; reservar para MODEL-01.
- **D-65c (voz):** "Nosso pré-processamento segue o protocolo de Shi et al. (2022) como parâmetro de comparação..." — voz em primeira pessoa do plural; citação parentética `(Shi et al., 2022)`; `<i>et al.</i>` em itálico ABNT (D-54 herdado). Rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`

### EDA-03 — gráfico de insight (D-66)

- **D-66 (gráfico escolhido):** **scatter PCA 2D com 3 clusters K-Means coloridos** (PENDING-02 resolvido). 1 ponto = 1 aluno; eixos PC1/PC2 das features de cluster (taxa de acerto eventual + tentativas médias + X-Grade). 3 grupos em cores distintas com legenda inline; preferir cores acessíveis e coerentes com paleta UniFacens.
- **D-66a (insight central — texto do slide):** "O grupo majoritário (~55%) NÃO é quem erra muito; é quem tenta pouco. Em risco no CSEDM tem alta taxa de acerto eventual e poucas tentativas por assignment." Frase única, em destaque (e.g. `.eda-insight` em Arial 21-23px), abaixo ou ao lado do scatter.
- **D-66b (geração da figura):** PNG não existe pronto em `results/`; código PCA existe em `notebooks/01_eda.ipynb` linha 2330. gsd-planner adiciona task de gerar PNG (e.g. `results/sec2_perfis_pca.png`) reaproveitando código existente; rodar célula isolada via `jupyter nbconvert --execute` ou snippet Python standalone. Validar SEED=42 reproduzível antes do commit.
- **D-66c (números base):** valores do `docs/eda_insights.md` Seção 3.1 com 453 estudantes, k=3, SEED=42: Alto 139 (30,7%) X-Grade 73,8 / Médio 66 (14,6%) X-Grade 64,9 / Em risco 248 (54,7%) X-Grade 55,9; tentativas médias 4,4-10,9 / 5,1-9,7 / 2,0-4,6 respectivamente. **Atenção:** notebook output atual mostra outras contagens (saída k=3 com 96 Alto visível em sed); gsd-planner re-executa a célula, valida e usa os números atuais.
- **D-66d (fonte):** `Fonte: análise sobre CSEDM (Spring 2019); K-Means k=3 com SEED=42.` Sem citação Shi aqui (o cluster é nosso, não do paper).
- **D-66e (silhouette + caveat):** silhouette score 0,237 para k=3 (k=2 é máximo com 0,285); escolhemos k=3 pela interpretabilidade do perfil intermediário. **Não** colocar esse caveat no slide; mantém-se como nota privada caso a banca pergunte.

### MARKER-02 — reuso mecânico do componente (D-67)

- **D-67:** MARKER-02 é **implementação mecânica**, sem decisões de design. Reusa o componente `.slide-marker` redesenhado em commit `5d44606` (pipeline CI/CD ABNT-friendly). Diferença em relação ao MARKER-01: apenas os modificadores das pills.
- **D-67a (modificadores conforme memória `feedback-marker-design`):**
  - Pill 1 (Definição do Problema): `--done` com check
  - Pill 2 (Preparação dos Dados): `--done` com check
  - Pill 3 (Modelagem e Avaliação): `--running` com símbolo de reload girando
  - Pill 4 (Implantação): `--pending` com círculo cinza em ring cinza
- **D-67b (badges):** badge `[done]` abaixo das pills 1 e 2; badge `[running]` abaixo da pill 3; sem badge na pill 4 (pending).
- **D-67c (título e rodapé):** título `> AS QUATRO FASES DA EDM` em Arial bold 24px (classe `.marker-title`); rodapé `Fonte: adaptado de Zorić (2020).` via `.rel-cite` (idênticos ao MARKER-01).
- **D-67d (sem CSS novo):** zero linhas adicionadas em `theme-unifacens.css`; só `index.html` edita. Validar visualmente que a animação spin do `--running` aplica somente na pill 3.

### Convenções herdadas das fases 1-2 (re-locked)

- **D-68 (cabeçalho):** padrão `> [seção]` único conforme D-01..D-03 fase 1; aplica-se aos 3 slides EDA. MARKER-02 fica sem temático (D-34d herdado).
- **D-69 (voz):** paráfrase indireta com autor parentético (D-25 fase 1, D-43 fase 2). Citação direta literal **proibida** nos 4 slides desta fase (nenhum argumento quantitativo justifica exceção; CLOSE-01/02 da fase 4 mantêm o privilégio).
- **D-70 (sem em-dash):** sem em-dash em prosa; usar vírgula, dois-pontos ou parênteses (D-44 herdado; memória `feedback-no-em-dashes` vinculante).
- **D-71 (fonte):** cada slide novo tem `Fonte:` no rodapé (Arial 17-18px cor `#5b6472`).
- **D-72 (itálico):** termos estrangeiros em itálico minúsculas: `<i>knowledge tracing</i>`, `<i>pipeline</i>`, `<i>cluster</i>`, `<i>scatter</i>` se aparecer, `<i>baseline</i>`. Nomes de modelos preservados (BKT, DKT, Code-DKT). CSEDM e ProgSnap2 como nomes próprios (não itálico). `<i>et al.</i>` ABNT em qualquer citação parentética múltipla (D-54 herdado).
- **D-73 (vocabulário herdado fase 2):**
  - "5 assignments com 10 problemas cada" / 6 colunas-chave do ProgSnap2 (D-50, D-51) — não redefinir; usar como referência implícita
  - Ponte KT → trabalho → CSEDM (D-53) — não precisa repetir; já estabelecido
  - "tratam respostas como corretas/incorretas, ignorando seu conteúdo" (D-52, vocabulário Shi 2022 Abstract) — disponível se útil

### Validação visual (D-74)

- **D-74:** Ao fim da fase, validar no browser (`cd apresentacao && python3 -m http.server 8000`) percorrendo do slide `#/0` ao slide `#/19`. Sucesso: navegação completa sem erro de console; transição visual nos 4 novos sem layout quebrado; números, tabela e scatter legíveis; rodapé `Fonte:` em cada slide; MARKER-02 com pills 1+2 em `--done`, pill 3 em `--running` (ícone girando suavemente), pill 4 em `--pending`. Validar também que slide-code antes era `#/11` e agora é `#/15`.

### Claude's Discretion (executor decide no plan)

- **Ordem de implementação dos 4 slides:** sugestão neutra MARKER-02 primeiro (puro reuso de CSS, valida ambiente), depois EDA-02 (números travados em D-65a, mais determinístico), depois EDA-01 (densidade visual a calibrar), depois EDA-03 (precisa gerar PNG novo, maior risco). Alternativa: EDA-03 primeiro porque depende de figura nova e bloquear cedo é melhor.
- **Granularidade dos commits:** 1 plan por slide (4 plans) com 1 commit funcional por plan; alinhado com fase 2.
- **Microcópia exata dos cabeçalhos `> [seção]`:** D-63 deixa em aberto; gsd-planner propõe phrasing e reviewer ajusta no checkpoint visual.
- **Formato visual exato do scatter PCA (D-66):** matplotlib + savefig PNG ou SVG; cores específicas; presença/ausência de eixos numerados; legenda inline vs separada. Default: PNG com cores do paleta UniFacens, eixos rotulados "PC1" / "PC2", legenda no canto.
- **Tabela A1..A5 do EDA-01 (D-64):** HTML `<table>` puro com classe própria (e.g. `.eda-grid`) ou layout flex com 5 cards (`.eda-card` × 5). Executor decide pelo que casa melhor com STYLE.md.
- **Atualização do STYLE.md §Inventário de slides (linha 108-125):** ao fim da fase 3, atualizar a tabela com os 4 novos sections e ajustar `§Gaps reservados` linha 131 (mover gap para "Após MARKER-02 e antes do trio Martins+fig: MODEL-01, MODEL-03, MODEL-04, MODEL-05 (fase 4)"). Plan ou commit separado fica a critério do gsd-planner.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning ou implementar.**

### Decisões de projeto e contexto desta fase

- `.planning/PROJECT.md` — escopo, constraints (estilo, ABNT, 10 min, sem em-dash), Key Decisions (ProgSnap2 nominalmente único em INTRO-01; Shi como problema antes do modelo; voz própria como padrão).
- `.planning/REQUIREMENTS.md` §EDA-01, §EDA-02, §EDA-03, §MARKER-02, §PENDING-02; tabela de Traceability.
- `.planning/ROADMAP.md` §"Phase 3: EDA e Pré-processamento (Fase 2 EDM)" — Goal, Mode, Requirements, Success Criteria 1-5.
- `.planning/phases/01-reformata-o-da-base/01-CONTEXT.md` — decisões D-01..D-30 da fase 1 (especialmente padrão `> [seção]`, voz, STYLE.md, mapa de slides).
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-CONTEXT.md` — decisões D-31..D-47 da fase 2 (especialmente D-38b que mandata a ponte 413 → 410 → 328/82 nesta fase, D-44 sem em-dash, D-46 itálico).
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/PHASE-SUMMARY.md` — vocabulário herdado (D-50..D-59), padrões de execução (iterações textuais pós-checkpoint esperadas).

### Estilo visual e citação (vinculante)

- `apresentacao/STYLE.md` — Identidade visual, paleta UniFacens, tipografia, regras de citação ABNT, inventário de slides pós-fase 2 (12 + 4 = 16 sections), `§Gaps reservados` (linha 130 marca o gap correto para esta fase). **Não tem frase obsoleta a corrigir nesta fase.**
- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — Manual UniFacens de citação ABNT.

### Markup-alvo

- `apresentacao/index.html` — único arquivo HTML a editar; 16 `<section>` no estado pós-fase 2; 4 novos serão inseridos após MARKER-01 (`#/10`) e antes de `slide-code` (`#/11`).
- `apresentacao/assets/theme-unifacens.css` — tema; componente `.slide-marker` (linhas 358-408 + redesign de `5d44606`) **já pronto e reusável** para MARKER-02. Eventuais classes novas para EDA-01 (`.eda-grid`/`.eda-card`) ou EDA-03 (`.eda-insight`) podem ser anexadas.

### Fontes primárias e dados

- `docs/Code-DKT.pdf` (Shi, Mao, Akram, Lytinen e Heffernan, 2022) — base de EDA-02 (protocolo de pré-processamento). **LER §3 (Methodology)** para travar o phrasing exato do filtro `min_attempts ≥ 3`, do split 80/20 e da truncagem em 50.
- `docs/eda_insights.md` — síntese pós-EDA dos notebooks 01 e 02. Seção 1.1 (taxa de acerto por assignment), Seção 2.1 (distribuição seq_len), Seção 3.1 (clusters K-Means). **Fonte primária dos números** que vão nos slides; gsd-planner valida cada número contra MainTable+protocolo Shi (não só Release/Train).
- `notebooks/01_eda.ipynb` — Seção 2.3 (linha ~1832) tem o K-Means; linha ~2330 tem o PCA scatter. Re-executar a célula para gerar PNG novo (`results/sec2_perfis_pca.png` sugerido).
- `data/CSEDM/MainTable.csv` — fonte primária do dataset Spring 2019 (413 alunos brutos). Validar contagens por assignment com `pd.read_csv` se `eda_insights.md` divergir.

### Memórias (auto-context, vinculantes)

- `~/.claude/.../memory/feedback-marker-design.md` — MARKER-XX redesenhado 2026-05-28 (commit `5d44606`); MARKER-02 é mecânico, só altera modificadores das pills (tabela na própria memória).
- `~/.claude/.../memory/project_split_discovery.md` — paper usa 80/20 de 410; nós usamos Release/ (329) historicamente; nenhum código errado, só 3/5 assignments avaliáveis em Release/. Migramos para MainTable+Shi protocol no pipeline final. M=10 confirmado, AUC pooled idem.
- `~/.claude/.../memory/project_codedkt_results.md` — A439 first_auc=72,55% (dentro ±3% Shi); resultado final do pipeline com 410 alunos.
- `~/.claude/.../memory/feedback_no_em_dashes.md` — vinculante para D-70.
- `~/.claude/.../memory/feedback_tcc_writing_style.md` — ABNT + prosa acessível.
- `~/.claude/.../memory/reference_manual_citacoes.md` — manual Facens.

### Codebase context já gerado

- `.planning/codebase/STRUCTURE.md` — onde inserir slides em `apresentacao/index.html`.
- `.planning/codebase/CONVENTIONS.md` — convenções de redação e commit message style (lowercase português, prefixo `apresentacao:`).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `.deck-topic` + `.caret.blink` (em `theme-unifacens.css`): padrão de cabeçalho `> [seção]`. Aplica em EDA-01, EDA-02, EDA-03.
- `.slide-marker` + `.marker-track` + `.marker-step` + modificadores `--done`/`--running`/`--pending` + `.marker-step__mark` + `.marker-arr` + `.marker-title` + `.rel-cite`: componente **completamente pronto** para MARKER-02 reusar sem alterar CSS (commit `5d44606`, redesign CI/CD ABNT).
- `.rel-lead` (3 parágrafos do template `slide-related`): pode ser reusado para EDA-01 (hub narrativo) e EDA-02 (justificativa + etapas) em vez de inventar classes novas.
- `.rel-cite` / `.prob-cite` / `.fig-fonte`: rodapé `Fonte:` existente. EDA-* pode reusar `.rel-cite`.
- `.bridge-seq` (slide Yağcí fundido): sequência horizontal com `.step` + `.arr`. Modelo de inspiração para a tabela A1..A5 se gsd-planner optar por cards (`.eda-step`-like).
- Marca d'água Facens `<svg class="wm">`: replicar nos 4 novos.

### Established Patterns

- Estrutura de slide: `<section data-background-color="#F1F6FB"><div class="deck-slide slide-XYZ">...</div></section>`. NUNCA mudar.
- Comentário acima de cada `<section>`: `<!-- ============ SLIDE · descrição ============ -->`.
- Tipografia: títulos/corpo em Arial; tópico `>` em Cascadia 24px; "Fonte:" em Arial 17-18px.
- Cores: paleta UniFacens (`--uni-blue #2667FF`, `--uni-ink #111317`, fundo `#F1F6FB`, cinza secundário `#5b6472`).
- Citação parentética: `(Autor, ano)` sem `p. X` em paráfrase indireta; `<i>et al.</i>` ABNT (D-54 herdado).

### Integration Points

- Único arquivo HTML a editar: `apresentacao/index.html`.
- CSS provavelmente recebe pequeno acréscimo de classes específicas para EDA (`.eda-grid`/`.eda-card`/`.eda-insight`); MARKER-02 não exige CSS novo.
- Browser: `cd apresentacao && python3 -m http.server 8000` → http://127.0.0.1:8000/#/N. Após inserção em D-60, os novos slides ficam em `#/11` a `#/14`; slide-code desloca de `#/11` para `#/15`; restante do deck desloca +4.
- Sem build system; recarregar página direto.
- Geração de PNG para EDA-03: rodar célula do `notebooks/01_eda.ipynb` (Seção 2.3, ~linha 2330) isoladamente; salvar em `results/sec2_perfis_pca.png`; commit do PNG junto com o slide.

### Slides existentes pós-fase 2 (estado HEAD; índice 0-based)

| # | classe | cabeçalho | papel na fase 3 |
|---|---|---|---|
| 0 | slide-cover-brand | (sem) | inalterado |
| 1 | slide-title-tcc | (sem) | inalterado |
| 2 | slide-agenda | (sem temático) | inalterado |
| 3 | slide-related | `> introdução` | inalterado |
| 4 | slide-related | `> mineração de dados educacionais` | inalterado |
| 5 | slide-phases | `> as quatro fases da edm` | inalterado |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | inalterado |
| 7 | slide-related | `> o dataset csedm` (INTRO-01) | inalterado |
| 8 | slide-related | `> o problema do kt binário` (INTRO-03a) | inalterado |
| 9 | slide-related | `> sinal pedagógico perdido` (INTRO-03b) | inalterado |
| 10 | slide-marker slide-marker--phase1 | (sem temático; MARKER-01 redesenhado) | **ÂNCORA SUPERIOR** — EDA-01 entra após este |
| 11 | slide-code | `> o que o code-dkt olha` | **ÂNCORA INFERIOR** — MARKER-02 entra antes deste; vira `#/15` após inserção |
| 12 | slide-kcfig | `> kcs semânticos extraídos` | inalterado; vira `#/16` |
| 13 | slide-problem | `> retomando o problema` (Martins p2) | inalterado; vira `#/17` |
| 14 | slide-problem | `> retomando o problema` (Martins p3) | inalterado; vira `#/18` |
| 15 | slide-fig | `> evolução por dificuldade` | inalterado; vira `#/19` |

### Slides a criar (4 novos)

| # após inserção | classe sugerida | cabeçalho | requirement |
|---|---|---|---|
| 11 | `slide-related` ou `slide-eda` adaptado | `> [a definir D-63a]` | EDA-01 |
| 12 | `slide-related` ou `slide-eda` adaptado | `> [a definir D-63b]` | EDA-02 |
| 13 | `slide-related slide-eda-insight` (ou similar) | `> [a definir D-63c]` | EDA-03 |
| 14 | `slide-marker slide-marker--phase2` | (sem temático; reusa CSS de MARKER-01) | MARKER-02 |

Nomenclatura de classes ficou em sugestão; executor pode usar `.slide-related` reutilizado (template existente) ou padronizar `.slide-eda` único. **Decisão fica no plan-phase.**

</code_context>

<specifics>
## Specific Ideas

- **EDA-01 phrasing alvo (rascunho):** parágrafo abertura "Encontramos a base via Shi et al. (2022). Ao navegar o CSEDM, vimos que os 5 assignments cobrem diferentes níveis de dificuldade." + tabela 5 linhas (A1..A5, alunos, problemas, acerto). Cabeçalho candidato: `> como navegamos o csedm` (3 outras opções no plan).
- **EDA-02 phrasing alvo (rascunho):** "Nosso pré-processamento segue o protocolo de Shi et al. (2022) como parâmetro de comparação. Dos 413 alunos brutos do CSEDM, mantivemos 410 com `min_attempts ≥ 3` (filtro Shi) e dividimos 328 treino / 82 teste (split 80/20). Limitamos cada sequência às últimas 50 tentativas, conforme o paper original." Cabeçalho candidato: `> pré-processamento`. Rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`
- **EDA-03 phrasing alvo (rascunho):** insight em destaque: "O grupo majoritário (~55%) não é quem erra muito; é quem tenta pouco." Subtítulo abaixo (opcional): "Em risco no CSEDM tem alta taxa de acerto eventual mas poucas tentativas por assignment." Cabeçalho candidato: `> perfis dos alunos` ou `> três jeitos de aprender`.
- **MARKER-02 markup-alvo:** copiar exatamente o `<section>` do MARKER-01 (linhas a verificar em `apresentacao/index.html`); alterar:
  - classe modificadora da `<section>` de `slide-marker--phase1` para `slide-marker--phase2`
  - segundo modificador de pill 2 de `--pending` para `--done` + check
  - terceiro modificador de pill 3 de `--pending` para `--running` + ícone reload
  - badge: adicionar `[done]` abaixo da pill 2; mover `[running]` da pill 2 (do MARKER-01) para pill 3
  - tudo o resto idêntico (título, rodapé, classes)
- **PNG do scatter PCA:** salvar como `results/sec2_perfis_pca.png`; dimensão sugerida 1200×700 ou 1000×600 (encaixa em 1280×720 com margens); DPI 100-120; transparent background opcional. SEED=42 obrigatório (memória `feedback_protocol_fidelity`).

</specifics>

<deferred>
## Deferred Ideas

- **Discutir microcópia textual dos 3 EDAs antes da execução:** usuário optou por não travar agora; gsd-planner propõe phrasing e reviewer humano ajusta no checkpoint visual. Padrão herdado da fase 2 (média 2 iterações textuais pós-checkpoint por slide).
- **Threshold binário `correct = (Score == 1.0)` em EDA-02:** decisão metodológica que pode aparecer como 1 linha extra se houver espaço; default fora. Memória `project_split_discovery` registra "37% dos eventos têm Score parcial"; argumento existe se quiser aprofundar.
- **Separação Run.Program / Compile.Error:** explicitamente reservado para MODEL-01 da fase 4 (Code-DKT). EDA-02 não toca.
- **Threshold de silhouette ou justificativa de k=3 sobre k=2 em EDA-03:** caveat técnico que fica como nota privada caso a banca pergunte; NÃO entra no slide (D-66e).
- **Discutir Release/Train (246) vs MainTable+Shi (410) explicitamente na defesa:** usuário escolheu protocolo Shi sem mencionar Release/Train. A história "começamos com Release/, migramos para Shi" fica disponível como resposta a pergunta da banca.
- **Bar chart alternativo (tentativas médias × perfil) ou tabela síntese pura no EDA-03:** opções consideradas mas descartadas em favor do scatter PCA (D-66). Disponíveis se durante execução o scatter PCA ficar visualmente ruim.
- **Outros gráficos do `results/` (sec5_imbalance.png, sec4_sequence_distribution.png, correlação Compile.Error × Label):** opções consideradas para EDA-03 mas descartadas. Podem inspirar slides de backup ou Q&A.
- **Redesenho visual do componente `.slide-marker`:** resolvido em commit `5d44606` (pipeline CI/CD ABNT); não está mais em backlog. MARKER-02/03/04 herdam o redesign.

### Reviewed Todos (not folded)

Nenhum todo cruzado para esta fase (`gsd-sdk query todo.match-phase 3` não consultado; assumindo 0 matches conforme padrão das fases 1 e 2).

</deferred>

---

*Phase: 3-EDA e Pré-processamento (Fase 2 EDM)*
*Context gathered: 2026-05-28*
