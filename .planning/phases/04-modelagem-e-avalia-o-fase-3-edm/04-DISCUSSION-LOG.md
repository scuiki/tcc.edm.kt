# Phase 4: Modelagem e Avaliação (Fase 3 EDM) - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-28
**Phase:** 4-modelagem-e-avalia-o-fase-3-edm
**Areas discussed:** MODEL-04 formato comparação Shi, MODEL-05 Duan + pipeline em 1 slide, MODEL-01 cronologia + AST inset, PENDING-04 CLOSE-03 + MARKER-03

**Nota intermediária:** Após a primeira pergunta de MODEL-04 ser rejeitada para esclarecimento, o usuário pediu re-análise dos notebooks que foram atualizados recentemente (alinhamento Spring 2019 split). Foram lidos `06_code_dkt`, `07_comparison`, `03b_kc_generation`, `03c_eda_kc_crossover`, `09_srcml_dkt`. Descobertas registradas: Code-DKT A439 first=73,27% (multirun) vs 75,74% paper (delta -2,47pp dentro do gate ±3pp); Wilcoxon agora N=50 com Holm-Bonferroni; 7 etapas reais do KCGen-KT; 28 KCs canônicos; PNGs CLOSE-03 alinhados ao re-treino. PENDING-04 essencialmente resolvido.

---

## MODEL-04 — formato comparação com Shi

### Pergunta 1: escopo + granularidade

| Option | Description | Selected |
|--------|-------------|----------|
| 3 modelos × 5 ass + linha Shi paper (ABNT) | Tabela ABNT `.eda-grid`, BKT/DKT/Code-DKT em A439-A502 + linha Shi paper só A439. srcML fora. | ✓ |
| 4 modelos × 5 ass + linha Shi (inclui srcML) | Mantém srcML-DKT como 4ª linha. | |
| Foco A439 vs Shi + tabela compacta dos demais | Bloco central destacado + tabela menor. | |
| PNG existente reaproveitado + caption | Embute `comparison_table_first_auc.png`. | |

**User's choice:** 3 modelos × 5 ass + linha Shi paper (ABNT)
**Notes:** primeira tentativa da pergunta foi rejeitada para o usuário verificar a justificativa de first-attempt AUC como métrica primária; após verificação (Shi §5, CLAUDE.md, 07_comparison) confirmada a consistência cross-projeto; mecanismo técnico = autocorrelação intra-problema.

### Pergunta 1.5 (subordinada): onde justificar first-attempt AUC?

| Option | Description | Selected |
|--------|-------------|----------|
| Em EDA-02 (pré-processamento) | Acrescentar linha no slide já fechado. | |
| Caption discreto dentro do MODEL-04 | Acima/abaixo da tabela. | ✓ |
| Sem justificar no deck, fica para fala/QA | | |
| Slide novo dedicado (métricas) | +1 slide na fase. | |

**User's choice:** Caption discreto dentro do MODEL-04

### Pergunta 2: profundidade estatística

| Option | Description | Selected |
|--------|-------------|----------|
| Só first-attempt + nota Wilcoxon | Wilcoxon em nota discreta. | |
| First-attempt destacado + botão all-attempts | Linha resumo all-attempts no rodapé. | |
| 2 tabelas (first + all) lado a lado | Atende critério 2 com forma simétrica. | |
| Só first-attempt, sem Wilcoxon visual | Slide mais compacto. | ✓ |

**User's choice:** Só first-attempt, sem Wilcoxon visual
**Notes:** Wilcoxon e all-attempts ficam para fala/QA e documento TCC.

### Pergunta 3: cabeçalho `> [seção]`

| Option | Description | Selected |
|--------|-------------|----------|
| > replicando shi | Foca a narrativa de replicação. | |
| > resultados | Mínimo, deixa tabela falar. | |
| > code-dkt no csedm | Foco no nosso experimento. | ✓ |
| > first-attempt auc | Técnico, sobre a métrica. | |

**User's choice:** `> code-dkt no csedm`

---

## MODEL-05 — Duan + pipeline em 1 slide

### Pergunta 1: quantas etapas mostrar (condensação 7→N)

| Option | Description | Selected |
|--------|-------------|----------|
| Input → Processo LLM → Output | 3 caixas agregando o miolo. | |
| Gerar → Agrupar → Mapear | 3 verbos com "código bruto" destacado. | |
| Sampling → LLM gera → Cluster+Q-matrix | 3 caixas fiéis. | |
| Mostrar as 5 etapas em pipeline compacto | Sampling → LLM bruto → Clustering → Rotulagem → Q-matrix. | ✓ |

**User's choice:** Mostrar as 5 etapas em pipeline compacto
**Notes:** override da diretriz "3 etapas" do PROJECT.md / D-66 por fidelidade ao pipeline real do 03b_kc_generation.

### Pergunta 2: layout/componente

| Option | Description | Selected |
|--------|-------------|----------|
| .bridge-seq estendido (5 .step + 4 .arr) | Reusa componente Yağcí. | ✓ |
| .marker-track adaptado (pipeline CI/CD) | Pode confundir com .slide-marker EDM. | |
| Tabela ABNT 5 colunas (.eda-grid de 1 linha) | Sem setas, perde flow. | |
| Pipeline horizontal novo (.kc-pipeline) | +1 componente. | |

**User's choice:** `.bridge-seq` estendido

### Pergunta 3: abertura + onde colocar "código bruto, não AST"

| Option | Description | Selected |
|--------|-------------|----------|
| Intro 2 frases + 'código bruto' na caixa 2 | Decisão destacada na intro. | |
| Intro 1 frase + 'código bruto' só no pipeline | Detalhe sutil. | |
| Intro 1 frase neutra + insight no rodapé | "Construímos um pipeline..." + fechamento "A decisão-chave foi...". | ✓ |
| Intro com pergunta + pipeline + resposta | Mais retórico. | |

**User's choice:** Intro 1 frase neutra + insight no rodapé

### Pergunta 4: cabeçalho `> [seção]`

| Option | Description | Selected |
|--------|-------------|----------|
| > nosso pipeline de kcs | Primeira pessoa. | |
| > extração automática de kcs | Técnico, neutro. | ✓ |
| > da submissão ao kc | Orientado por fluxo. | |
| > kcgen-kt adaptado | Sinaliza fidelidade ao paper Duan. | |

**User's choice:** `> extração automática de kcs`

---

## MODEL-01 — cronologia + AST inset

### Pergunta 1: como apresentar a cronologia BKT → DKT → Code-DKT

| Option | Description | Selected |
|--------|-------------|----------|
| 3 chips horizontais com ano e ideia-chave | Componente .bridge-seq ou .chrono-step. | ✓ |
| Linha do tempo horizontal (timeline visual) | Eixo proporcional aos anos. | |
| Texto inline curto (1 frase contextual) | Sem caixas. | |
| Cronologia em rodapé como 'linhagem' | Subaproveita. | |

**User's choice:** 3 chips horizontais com ano e ideia-chave

### Pergunta 2: qual SVG entra como inset

| Option | Description | Selected |
|--------|-------------|----------|
| ast_codedkt_ptbr.svg (AST com caminho destacado) | Canonical per ROADMAP. | ✓ (após esclarecimento) |
| codedkt_model_structure_ptbr.svg (arquitetura) | 1180×640, denso demais para defesa. | |
| Sem inset visual, foco em texto + cronologia | Viola Success Criteria 1. | |
| AST inset + chip arquitetura referenciado | Pointer pro documento TCC. | |

**User's choice:** ast_codedkt_ptbr.svg (após esclarecimento sobre arquitetura SVG)
**Notes:** primeira tentativa rejeitada para o usuário pedir análise se a arquitetura SVG encaixaria. Resposta: arquitetura SVG é grande (1180×640) e denso (fórmulas e_s/e_q/e_o, x_t, α, z, dimensões M=10/R=50); cabe melhor no documento TCC como Figura 3. AST inset é o veículo que conecta "código → paths code2vec" com 1 olhada; ROADMAP Success Criteria 1 menciona AST inset; o snippet pseudo-Python da SVG é didático intencionalmente (concept language-agnostic).

### Pergunta 3: nível de detalhe da descrição

| Option | Description | Selected |
|--------|-------------|----------|
| 1-2 frases com code2vec e javalang nomeados | Voz científica. | |
| 1 frase, sem termos específicos | Viola Success Criteria 1. | |
| 2 colunas: extração vs predição | Apertado com cronologia em cima. | |
| Lista de 3-4 bullets técnicos | Lista quebra padrão de prosa. | |

**User's choice:** Híbrido pedido pelo usuário (não nas opções)
**Notes:** primeira tentativa rejeitada; usuário pediu "bullets técnicos + 1 ou 2 frases contextualizando". Reformulada com 4 variantes de contexto.

### Pergunta 3 (reformulada): contexto + bullets

| Option | Description | Selected |
|--------|-------------|----------|
| Contexto liga à cronologia + 4 bullets | "O Code-DKT incorpora o conteúdo do código que o DKT ignorava, mantendo o tracing sequencial." + 4 bullets. | ✓ |
| Contexto técnico em 2 frases + 4 bullets | Mais robusto para banca técnica. | |
| Contexto curto 'o que faz' + 4 bullets | Mais neutro. | |
| Contexto 'o porquê' + 3 bullets condensados | Mais prosa em cada bullet. | |

**User's choice:** Contexto liga à cronologia + 4 bullets

### Pergunta 4: cabeçalho `> [seção]`

| Option | Description | Selected |
|--------|-------------|----------|
| > da árvore ao tracing | Narrativo, conecta AST com KT. | |
| > como o code-dkt funciona | Direto, descritivo. | ✓ |
| > entra o code-dkt | Narrativo de transição. | |
| > caminhos da ast | Foca a representação nova. | |

**User's choice:** `> como o code-dkt funciona`

---

## PENDING-04 CLOSE-03 + MARKER-03

### Pergunta 1: qual figura para CLOSE-03

| Option | Description | Selected |
|--------|-------------|----------|
| Manter `curves_by_martins.png` (atual) | Curvas das 6 sub-dificuldades Martins. | |
| Trocar para `difficulty_martins.png` | MD5 distinto, conteúdo diferente. | |
| Trocar para `level_vs_slope.png` (scatter) | Tira noção de tempo. | |
| Decidir só após ver as 4 alternativas no browser | Defere para o plan-phase. | ✓ (com adendo) |

**User's choice:** "Pode seguir com a decisão 4, mas adicione os 4 pngs diretamente nos slides, ai escolho um e removemos os demais"
**Notes:** plan vai criar 4 slides temporários (1 por PNG); user escolhe no checkpoint visual; 3 removidos; slide-fig fica com o PNG vencedor; comentário HTML linha 541 corrigido.

### Pergunta 2: MARKER-03 pill 4 (Implantação)

| Option | Description | Selected |
|--------|-------------|----------|
| --running (TCC 2 segue, slides TOOL próximos) | Continuidade narrativa. | ✓ |
| --pending (defesa TCC 1 fecha aqui) | Implantação realmente acontece no TCC 2. | |
| Decidir conforme o que MARKER-04 vai mostrar | Adiar para fase 5. | |

**User's choice:** `--running`

### Pergunta 3: detalhes restantes

| Option | Description | Selected |
|--------|-------------|----------|
| Atualizar insight (`fig-read`) após escolha do PNG | Defere para checkpoint visual. | ✓ |
| Tudo decidido, fechar discussion | | |
| Discutir ordem de implementação dos slides novos | | |
| Discutir transição slide-kcfig → CLOSE-01 | | |

**User's choice:** Atualizar insight após escolha do PNG (deferido)

---

## Claude's Discretion

- Ordem de implementação dos 4 slides novos (sugestão: MARKER-03 → MODEL-04 → MODEL-01 → MODEL-05)
- Granularidade de commits (1 plan por slide, 1 commit funcional por plan)
- Componente exato da cronologia em MODEL-01 (`.bridge-seq` estendido vs novo `.chrono-step`)
- Tipografia exata das 5 caixas do pipeline MODEL-05 se ficar apertado em 1280px
- Microcópia ajustável pós-checkpoint nos 3 slides MODEL (padrão fase 2/3: média 1-3 iterações textuais)
- Atualização do STYLE.md §Inventário e §Gaps reservados ao fim da fase
- Markup exato da tabela ABNT MODEL-04 dentro do `.eda-grid` (estilo herdado da fase 3)

## Deferred Ideas

- `fig-read` insight de CLOSE-03 (defere para checkpoint visual após escolha do PNG)
- All-attempts AUC e Wilcoxon visíveis no MODEL-04 (ficam para fala/QA e documento TCC)
- Arquitetura completa Code-DKT (`codedkt_model_structure_ptbr.svg`) — reservada para documento TCC
- Transição narrativa explícita slide-kcfig → CLOSE-01 (depende da fala; ajustar só se soar abrupto)
- Caveat do snippet AST ser pseudo-Python (não redesenhar; nota de pé documento TCC se banca perguntar)
- MODEL-04 visualizações alternativas (bars, boxplot, delta, heatmap por problema) — descartadas; disponíveis para backup
- MODEL-05 reduzir para 3 etapas (override registrado; só reverter se layout quebrar)
- MARKER-04 modificadores (decidir na fase 5)
- CLOSE-01/02 ajustes textuais (fora desta fase; já fechados na fase 1)
