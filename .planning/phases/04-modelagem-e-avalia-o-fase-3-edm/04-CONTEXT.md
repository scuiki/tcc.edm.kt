# Phase 4: Modelagem e Avaliação (Fase 3 EDM) - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Inserir **4 slides novos** em `apresentacao/index.html` (MODEL-01, MODEL-04, MODEL-05, MARKER-03) e **reaproveitar 4 slides existentes** (slide-code = MODEL-03, slide-kcfig = saída MODEL-05, Martins p2 = CLOSE-01, Martins p3 = CLOSE-02, slide-fig = CLOSE-03) para entregar o bloco da Fase 3 da EDM (Modelagem e Avaliação) no deck reveal.js. Eixo prioritário da defesa: **CLOSE-01/02/03** (retomada Martins → evidência Code-DKT/KCs).

A sequência narrativa final entre MARKER-02 (atual `#/15`) e MARKER-03 (novo, fim deste bloco):

```
#/15 MARKER-02      Fase 2 EDM concluída                   (existente)
#/16 MODEL-01       Como o Code-DKT funciona               (NOVO)
#/17 MODEL-03       O que o Code-DKT olha                  (slide-code, reaproveitado)
#/18 MODEL-04       Code-DKT no CSEDM (resultados vs Shi)  (NOVO)
#/19 MODEL-05       Extração automática de KCs (Duan+pipe) (NOVO)
#/20 slide-kcfig    KCs semânticos extraídos               (reaproveitado, saída de MODEL-05)
#/21 CLOSE-01       Retomando o problema (Martins p2)      (reaproveitado)
#/22 CLOSE-02       Retomando o problema (Martins p3)      (reaproveitado)
#/23 CLOSE-03       Evolução por dificuldade (gráfico)     (reaproveitado, PENDING-04 → defere)
#/24 MARKER-03      Fase 3 EDM concluída                   (NOVO)
```

CLOSE-01/02 **não são tocados nesta fase** (já reformatados na fase 1 com cabeçalho `> retomando o problema` e citação direta literal dos 13/10 autores Martins; D-28 mantém citação direta como exceção por argumento quantitativo). CLOSE-03 tem implementação especial: 4 PNGs candidatos inseridos como slides temporários para escolha visual no checkpoint, depois 3 removidos.

Total esperado de sections no `<div class="slides">` ao fim da fase: 21 (pós-fase 3) + 4 novos (MODEL-01, MODEL-04, MODEL-05, MARKER-03) = **25 sections** (transitoriamente 25 + 3 PNG candidatos = 28 durante o checkpoint do CLOSE-03, voltando a 25 após escolha).

</domain>

<decisions>
## Implementation Decisions

### Posição no DOM (D-75)

- **D-75:** Os 4 slides novos entram após MARKER-02 (`#/15`) e antes do trio Martins+fig + MARKER-03 no fim. Ordem dentro do bloco: MODEL-01 → slide-code (reaproveitado como MODEL-03) → MODEL-04 → MODEL-05 → slide-kcfig (reaproveitado) → Martins p2 (CLOSE-01) → Martins p3 (CLOSE-02) → slide-fig (CLOSE-03) → MARKER-03. Slide-code atualmente em `#/16` desloca para `#/17`; demais slides existentes deslocam +4 (slide-fig `#/20` → `#/23`).
- **D-76:** Justificativa narrativa: MARKER-02 fecha "Preparação dos Dados ✓"; MODEL-01 abre dizendo como o Code-DKT funciona; slide-code (MODEL-03) mostra atenção sobre código real; MODEL-04 mostra os resultados quantitativos; MODEL-05 introduz a extração automática de KCs (Duan+pipeline 5 etapas); slide-kcfig mostra a saída desse pipeline; CLOSE-01/02/03 fazem a retomada Martins (eixo prioritário, 30-40s cada); MARKER-03 fecha "Modelagem e Avaliação ✓" com pill 4 `--running` (TCC 2 segue).

### MODEL-01 — Como o Code-DKT funciona (D-77)

- **D-77a (cabeçalho):** `> como o code-dkt funciona`
- **D-77b (layout):** Topo: cabeçalho `> [seção]`. Logo abaixo: **cronologia em 3 chips horizontais** (BKT 1995 / Bayes / habilidades por KC) → (DKT 2015 / RNN / histórico sequencial) → (Code-DKT 2022 / RNN + paths AST / code2vec). Componente sugerido: `.bridge-seq` estendido ou novo `.chrono-step` (executor decide). Body em 2 colunas: esquerda = texto, direita = AST inset SVG.
- **D-77c (texto coluna esquerda):**
  - Contexto (1 frase): "O Code-DKT incorpora o conteúdo do código que o DKT ignorava, mantendo o tracing sequencial."
  - 4 bullets:
    1. `javalang → AST`
    2. `code2vec → caminhos folha-a-folha`
    3. `atenção pondera os caminhos`
    4. `LSTM combina com (ProblemID, acerto/erro)`
- **D-77d (inset visual):** `docs/figures/ast_codedkt_ptbr.svg` (560×620) — código pseudo-Java + AST + caminho folha-a-folha em vermelho (representa um path code2vec). Escalar para caber em ~450×500. **NÃO** incluir `codedkt_model_structure_ptbr.svg` (arquitetura completa fica para o documento TCC; cabe Figura 3 lá, dimensão 1180×640 com fórmulas é denso demais para defesa de 10 min).
- **D-77e (rodapé):** `Fonte: adaptado de Shi <i>et al.</i> (2022).`
- **D-77f (caveat SVG AST):** o snippet no quadro usa sintaxe pseudo-Python (`def metodo(entrada):`) e não Java. Conceito de AST é language-agnostic; a versão atual é mais didática. Manter como está; não redesenhar.

### MODEL-04 — Code-DKT no CSEDM (resultados vs Shi) (D-78)

- **D-78a (cabeçalho):** `> code-dkt no csedm`
- **D-78b (escopo):** **3 modelos × 5 assignments + linha Shi paper**. BKT/DKT/Code-DKT em A439-A502 (números de `results/comparison_table_first_auc.md`, média sobre 10 seeds). Linha extra "Shi (2022)" só com A439 (paper só publica A1, equivalente a A439). srcML-DKT **fora** (alinhado com Out of Scope do PROJECT.md linha 101).
- **D-78c (métrica):** apenas first-attempt AUC. All-attempts AUC e Wilcoxon (Code-DKT > DKT significativo, Holm-Bonferroni N=50) ficam para fala/QA, não no slide.
- **D-78d (caption discreto):** abaixo da tabela, frase curta justificando a métrica primária: "first-attempt AUC: métrica primária; mede transferência entre problemas e evita autocorrelação intra-problema (Shi <i>et al.</i>, 2022, §5)."
- **D-78e (forma):** tabela ABNT renderizada em `.eda-grid` (componente da fase 3 — 3 bordas horizontais, fundo transparente, ABNT/IBGE 1993). Consistente com EDA-01 e EDA-02. NÃO embutir PNG; render HTML.
- **D-78f (rodapé):** `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.`
- **D-78g (números a usar):** Code-DKT A439 first = **73,27%** (multirun, 10 seeds); paper Shi A439 first = **75,74%**; delta = **-2,47pp**, dentro do gate ±3pp do CLAUDE.md Critério 1.

### MODEL-05 — Extração automática de KCs (Duan + pipeline) (D-79)

- **D-79a (cabeçalho):** `> extração automática de kcs`
- **D-79b (estrutura):** abertura textual (1 frase) + pipeline horizontal de **5 etapas** + frase de fechamento + rodapé.
- **D-79c (abertura, 1 frase):** "Construímos um pipeline de cinco etapas para extrair Knowledge Components do CSEDM."
- **D-79d (5 etapas, componente `.bridge-seq` estendido):**
  1. Sampling estratificado (n=5 por problema; Duan Tab. 5)
  2. LLM gera KCs brutos do código bruto
  3. Clustering Sentence-BERT + HAC
  4. Rotulagem dos clusters via LLM
  5. Q-matrix por assignment (28 KCs / 50 problemas)
- **D-79e (fechamento, 1 frase pós-pipeline):** "A decisão-chave foi alimentar o LLM com código bruto, não AST (Duan <i>et al.</i>, 2025, Tab. 4)."
- **D-79f (override PROJECT.md):** PROJECT.md NEW-09/D-66 fixava "pipeline em 3 etapas". User overrideu para 5 etapas por fidelidade ao 03b_kc_generation.ipynb. Registrar como decisão ad-hoc D-79f.
- **D-79g (voz):** primeira pessoa do plural ("Construímos", "alimentar"); Duan parentético com `<i>et al.</i>` ABNT (D-54 herdado); sem citação direta literal (D-69 herdado).
- **D-79h (rodapé):** `Fonte: adaptado de Duan <i>et al.</i> (2025).`
- **D-79i (não duplicar):** slide-kcfig (next, reaproveitado) já mostra os 28 KCs canônicos mapeados às dificuldades Martins. MODEL-05 NÃO repete os KCs nem o mapeamento.

### MODEL-03 — slide-code reaproveitado (D-80)

- **D-80:** Nenhuma alteração nesta fase. Já reformatado na fase 1 (cabeçalho `> o que o code-dkt olha`, D-10) e movido para o fim do deck (D-16/D-17). Esta fase apenas confirma a posição (`#/17` após inserir MODEL-01).

### MODEL-04 caption métrica primária — first-attempt AUC (D-81)

- **D-81 (justificativa cross-projeto):** first-attempt AUC é métrica primária em todo o projeto (CLAUDE.md linha 116; 07_comparison.ipynb seção 1; Critério 1 CLAUDE.md). Mecanismo técnico: all-attempts AUC infla por autocorrelação intra-problema (o modelo "vê" tentativas 1..k-1 do mesmo problema quando prevê a tentativa k); first-attempt mede transferência pura entre problemas. Shi et al. (2022) §5: "first attempts are important... ITS interventions". Caption discreto em D-78d traz o mecanismo.

### CLOSE-01/02 — Martins return (D-82)

- **D-82:** **Não tocados nesta fase.** CLOSE-01 (Martins p2, 13 autores) e CLOSE-02 (Martins p3, 10 autores) já reformatados na fase 1 (commits `590ae34` e `2a86049`) com cabeçalho `> retomando o problema` e citação direta literal preservada (D-28 herdado: argumento quantitativo "13/10 autores" justifica exceção a D-69). ROADMAP Success Criteria 5 explicita "MANTÊM citação direta atual".

### CLOSE-03 — Gráfico Code-DKT por dificuldade (D-83)

- **D-83a (status PENDING-04):** **resolvido**. `codedkt_kc_retrained.pkl` existe (2026-05-25 01:42); `assets/fig-codedkt-martins-curves.png` no slide tem MD5 idêntico a `results/fig_codedkt_curves_by_martins.png` (mesmo timestamp 2026-05-25 02:02, ~20min após re-treino). Re-treino e alinhamento foram feitos. Memória `project_codedkt_kc_difficulty` ("desalinhamento") é histórica.
- **D-83b (pick visual diferido):** 4 PNGs candidatos em `results/` (todos gerados pelo mesmo script `scripts/analyze_kc_difficulty_codedkt.py`, re-treino alinhado):
  1. `fig_codedkt_curves_by_martins.png` (atual no slide)
  2. `fig_codedkt_difficulty_martins.png`
  3. `fig_codedkt_kc_curves.png` (28 curvas, uma por KC)
  4. `fig_codedkt_level_vs_slope.png` (scatter nível × inclinação)
- **D-83c (implementação no plan):** o plan de CLOSE-03 cria **4 slides temporários** (1 por PNG) no deck para comparação visual; user escolhe 1 no checkpoint; 3 slides temporários são removidos; slide-fig final fica com o PNG escolhido; comentário HTML linha 541 corrigido para apontar ao filename certo.
- **D-83d (insight `fig-read`):** texto da frase de leitura abaixo da figura **defere para o checkpoint visual** — depende de qual PNG vence. Insight atual ("Estruturas de controle aprende rápido; Vetores e Funções ficam planos") é específico de `curves_by_martins`; se trocar, refrasear.
- **D-83e (cabeçalho):** `> evolução por dificuldade` já estabelecido na fase 1 (D-09). Manter.
- **D-83f (rodapé):** `Fonte: elaborado pelo autor (Code-DKT, Shi <i>et al.</i>, 2022; dificuldades de Martins, Marin e Alves, 2024).` (já no slide; só ajustar `et al.` ABNT se ainda não estiver).

### MARKER-03 — Fase 3 EDM concluída (D-84)

- **D-84a:** Implementação mecânica do componente `.slide-marker` (commit `5d44606`, pipeline CI/CD ABNT), padrão herdado de MARKER-01/02. Zero CSS novo. Só `index.html` edita.
- **D-84b (modificadores das pills):**
  - Pill 1 (Definição do Problema): `--done` com check + badge `[done]`
  - Pill 2 (Preparação dos Dados): `--done` com check + badge `[done]`
  - Pill 3 (Modelagem e Avaliação): `--done` com check + badge `[done]` (fechando esta fase)
  - Pill 4 (Implantação): **`--running`** com símbolo de reload girando + badge `[running]` (TCC 2 segue na sequência narrativa; slides TOOL-01/03 da fase 5 mostram a proposta de implantação)
- **D-84c (título e rodapé):** título `> AS QUATRO FASES DA EDM` em Arial bold 24px (`.marker-title`); rodapé `Fonte: adaptado de Zorić (2020).` (idênticos ao MARKER-01/02).
- **D-84d (validar visualmente):** animação spin do `--running` aplica apenas na pill 4 nesta fase (na fase 5, MARKER-04 deve fechar tudo em `--done`).

### Convenções herdadas das fases 1-3 (re-locked)

- **D-85 (cabeçalho):** padrão `> [seção]` único conforme D-01..D-03 fase 1; aplica-se a MODEL-01, MODEL-04, MODEL-05. MARKER-03 sem temático (D-67/D-34d herdado).
- **D-86 (voz):** paráfrase indireta com autor parentético (D-69 herdado, D-43 fase 2). Citação direta literal **proibida** nos 3 slides MODEL novos. CLOSE-01/02 mantêm citação direta como exceção declarada (D-82).
- **D-87 (sem em-dash):** D-70 herdado; memória `feedback-no-em-dashes` vinculante. Usar vírgula, dois-pontos ou parênteses.
- **D-88 (itálico ABNT):** `<i>et al.</i>` em todas as citações parentéticas múltiplas (D-54 herdado, 8 ocorrências normalizadas na fase 2); termos estrangeiros em itálico minúsculas (`<i>code2vec</i>`, `<i>knowledge tracing</i>`, `<i>pipeline</i>`, `<i>tracing</i>`, `<i>cluster</i>`, `<i>gap</i>`); nomes de modelos preservados (BKT, DKT, Code-DKT, srcML-DKT); CSEDM e ProgSnap2 como nomes próprios (não itálico).
- **D-89 (estudantes, nunca alunos):** D-67e herdado (feedback `feedback_estudantes_nao_alunos`). Em prosa nova: "estudantes" ou "discentes". Exceção apenas em citação direta literal.
- **D-90 (Fonte):** cada slide novo tem `Fonte:` no rodapé (Arial 17-18px cor `#5b6472`).

### Validação visual (D-91)

- **D-91:** Ao fim da fase, validar no browser (`cd apresentacao && python3 -m http.server 8000`) percorrendo do slide `#/0` ao `#/24`. Sucesso: navegação completa sem erro de console; cronologia de MODEL-01 legível com 3 chips; AST inset SVG renderiza no MODEL-01 sem distorção; tabela ABNT do MODEL-04 com Code-DKT A439=73,27% e linha Shi visível; pipeline 5 etapas do MODEL-05 cabe em 1280×720 sem sobreposição; slide-kcfig segue MODEL-05 sem quebra de fluxo; CLOSE-01/02/03 inalterados em conteúdo; MARKER-03 com pill 4 `--running` animado.

### Claude's Discretion

- **Ordem de implementação dos 4 slides novos:** sugestão neutra MARKER-03 primeiro (mecânico, puro reuso de CSS, valida ambiente), depois MODEL-04 (tabela ABNT determinística, números travados em D-78), depois MODEL-01 (AST SVG + cronologia, densidade visual a calibrar), depois MODEL-05 (pipeline 5 etapas, maior risco de layout). Alternativa: MODEL-05 primeiro porque a extensão de `.bridge-seq` para 5 caixas é o maior risco visual.
- **Granularidade dos commits:** 1 plan por slide (4 plans) com 1 commit funcional por plan; alinhado com fases 2 e 3.
- **Componente exato da cronologia em MODEL-01:** `.bridge-seq` estendido (reusa do slide Yağcı) vs novo `.chrono-step`. Default: tentar `.bridge-seq` primeiro; se não casar, anexar `.chrono-step` em theme-unifacens.css.
- **Componente exato do pipeline em MODEL-05:** `.bridge-seq` estendido para 5 caixas + 4 setas. Tipografia das caixas: ícone pequeno + verbo + 1 linha. Se 5 caixas ficar apertado em 1280px, calibrar tipografia.
- **Microcópia exata do fechamento de MODEL-05:** "A decisão-chave foi alimentar o LLM com código bruto, não AST" é o phrasing-alvo; pequenos ajustes textuais aceitáveis no checkpoint.
- **`fig-read` do CLOSE-03:** defere para o checkpoint visual após escolha do PNG (D-83d).
- **Atualização do STYLE.md §Inventário de slides:** ao fim da fase 4, atualizar a tabela (linhas 108-132) com os 4 novos sections (MODEL-01, MODEL-04, MODEL-05, MARKER-03) e os reposicionamentos; ajustar `§Gaps reservados` (linha 136-138) movendo o gap para "Após CLOSE-03 / MARKER-03 e antes da fase 5: TOOL-01, TOOL-03, MARKER-04, END-01, AGENDA-01".

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning ou implementar.**

### Decisões de projeto e contexto desta fase

- `.planning/PROJECT.md` — escopo, constraints (estilo, ABNT, 10 min, sem em-dash), Key Decisions (eixo prioritário CLOSE-01/02/03; Duan vem depois do Code-DKT; ProgSnap2 só em INTRO-01; Shi como problema antes do modelo; voz própria como padrão).
- `.planning/REQUIREMENTS.md` §MODEL-01, §MODEL-03, §MODEL-04, §MODEL-05, §CLOSE-01, §CLOSE-02, §CLOSE-03, §MARKER-03, §PENDING-04; tabela de Traceability.
- `.planning/ROADMAP.md` §"Phase 4: Modelagem e Avaliação (Fase 3 EDM)" — Goal, Mode, Requirements, Success Criteria 1-8.
- `.planning/phases/01-reformata-o-da-base/01-CONTEXT.md` — decisões D-01..D-30 da fase 1 (especialmente padrão `> [seção]`, voz, STYLE.md, mapa de slides e reposicionamento dos slides finais Martins+fig).
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-CONTEXT.md` — decisões D-31..D-47 da fase 2 (D-54 `<i>et al.</i>` ABNT, D-44 sem em-dash, D-46 itálico).
- `.planning/phases/03-eda-e-pr-processamento-fase-2-edm/03-CONTEXT.md` — decisões D-60..D-74 da fase 3 (componentes ABNT `.eda-grid`/`.eda-fig`/`.eda-source` estabelecidos; D-67 reuso mecânico do `.slide-marker`).
- `.planning/phases/03-eda-e-pr-processamento-fase-2-edm/PHASE-SUMMARY.md` — vocabulário herdado, padrões de execução (iterações pós-checkpoint esperadas; média 1-3 por slide).

### Estilo visual e citação (vinculante)

- `apresentacao/STYLE.md` — Identidade visual, paleta UniFacens, tipografia, regras de citação ABNT, inventário de slides pós-fase 3 (21 sections), `§Gaps reservados` (linhas 136-138 marcam o gap correto para esta fase: "Antes do trio Martins+fig: MODEL-01, MODEL-03, MODEL-04, MODEL-05"; "Após slide-fig: MARKER-03").
- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — Manual UniFacens de citação ABNT.

### Markup-alvo

- `apresentacao/index.html` — único arquivo HTML a editar; 21 `<section>` no estado pós-fase 3; 4 novos serão inseridos conforme D-75. **NÃO** alterar slide-code, slide-kcfig, Martins p2, Martins p3, slide-fig em conteúdo (apenas reposicionar se necessário, já reposicionados na fase 1).
- `apresentacao/assets/theme-unifacens.css` — tema; componentes já prontos para reuso: `.slide-marker` (linhas 358-408 + redesign `5d44606`) para MARKER-03; `.bridge-seq` (slide Yağcı) candidato para cronologia MODEL-01 e pipeline MODEL-05; `.eda-grid` para tabela MODEL-04. Eventuais classes novas para MODEL-01 (`.chrono-step` se `.bridge-seq` não casar) podem ser anexadas.
- `apresentacao/assets/fig-codedkt-martins-curves.png` — figura atual do slide-fig (CLOSE-03); MD5 idêntico a `results/fig_codedkt_curves_by_martins.png`.

### Fontes primárias e dados

- `docs/Code-DKT.pdf` (Shi, Mao, Akram, Lytinen e Heffernan, 2022) — base de MODEL-01, MODEL-03, MODEL-04. **LER §4 (Methodology)** para travar phrasing do funcionamento Code-DKT, §5 para justificativa first-attempt AUC, Table 1 (resultados A1=A439).
- `docs/AutomatedKC.pdf` E/OU `docs/2025.EDM.short-papers.83.pdf` (Duan, Fernandez, Hassany, Sampaio de Alencar, Brusilovsky, Akram e Lan, 2025) — base de MODEL-05. **LER §3 (KCGen-KT pipeline), Tab. 4 (código bruto vs AST), Tab. 5 (n=5 sampling), Tab. 9 (rotulagem de clusters)** para travar phrasing do pipeline.
- `docs/figures/ast_codedkt_ptbr.svg` (560×620) — inset visual MODEL-01.
- `docs/figures/codedkt_model_structure_ptbr.svg` (1180×640) — **NÃO usar no slide**; reservar para documento TCC.
- `docs/Artigo+2+Desafios+na+aprendizagem...pdf` (Martins, Marin e Alves, 2024) — base de CLOSE-01/02 (já no deck, não alterar). 13 e 10 autores são argumento quantitativo das duas páginas.
- `docs/deepKnowledgeTracing.pdf` (Piech et al., 2015) — cronologia MODEL-01 (DKT, RNN, histórico sequencial).
- `docs/893CorbettAnderson1995.pdf` (Corbett e Anderson, 1995) — cronologia MODEL-01 (BKT, Bayes, habilidades por KC). **Citado parentético**, sem slide próprio (REMOVE-01 da fase 1 já consolidou isso).

### Notebooks executados (fonte dos números)

- `notebooks/06_code_dkt.ipynb` — implementação Code-DKT vanilla. Seção 14 tem tabela single-seed; comparação seção 10. **NÃO usar números single-seed nos slides**; usar multirun.
- `notebooks/07_comparison.ipynb` — comparação final 4 modelos × 5 ass × 10 seeds. **Fonte canônica dos números de MODEL-04** (cell 11 = literatura, cell 27 = sumário executivo). Code-DKT A439 first=73,27%, Shi paper A439=75,74%, delta=-2,47pp.
- `notebooks/08_multirun_regeneration.ipynb` — regeneração com 10 seeds (42-51) para DKT, Code-DKT, srcML-DKT.
- `notebooks/09_srcml_dkt.ipynb` — srcML-DKT (out of scope nesta apresentação; mas pickles informam a tabela do 07_comparison).
- `notebooks/03b_kc_generation.ipynb` — pipeline KCGen-KT 7 etapas. **Fonte canônica do pipeline de MODEL-05**. Etapas 1-5 e 7 completas para 5/5 assignments; Etapa 6 parcial. 28 KCs canônicos / 50 problemas.
- `notebooks/03c_eda_kc_crossover.ipynb` — cruzamento EDA × KCs. **Fonte canônica do conteúdo CLOSE-01/02 (texto Martins) e CLOSE-03 (figura)**: top KCs com atrito empírico, A2 vs A3 desagregados, ρ Spearman KCs × X-Grade.

### Resultados gerados (PNGs e tabelas)

- `results/comparison_table_first_auc.md` E `results/comparison_table_first_auc.png` — tabela 4 modelos × 5 assignments first-attempt AUC. **Não usar PNG no slide**; render HTML em `.eda-grid` (D-78e).
- `results/comparison_table_all_auc.md` / `.png` — secundário (não no slide; fala/QA).
- `results/comparison_table_pooled.md` / `.png` — secundário.
- `results/comparison_summary.json` — JSON sumário (input para outros artefatos).
- `results/codedkt_kc_retrained.pkl` — re-treino Code-DKT alinhado aos dados atuais; **PENDING-04 resolvido** (D-83a).
- `results/codedkt_kc_difficulty.json` — dificuldade por KC (números brutos).
- `results/fig_codedkt_curves_by_martins.png` — **candidato 1 para CLOSE-03** (atual no slide; MD5 igual ao asset).
- `results/fig_codedkt_difficulty_martins.png` — candidato 2.
- `results/fig_codedkt_kc_curves.png` — candidato 3 (28 curvas).
- `results/fig_codedkt_level_vs_slope.png` — candidato 4 (scatter).
- `results/qmatrix_A{439,487,492,494,502}.csv` — Q-matrix por assignment (5 arquivos).
- `results/kc_descriptions_A{...}.json` — KCs canônicos com descrições (insumo de slide-kcfig).
- `scripts/analyze_kc_difficulty_codedkt.py` — script que gera as figuras CLOSE-03 (D-83b candidatos).

### Memórias (auto-context, vinculantes)

- `~/.claude/.../memory/feedback-marker-design.md` — MARKER-XX componente CI/CD ABNT; modificadores `--done`/`--running`/`--pending` + badges (vinculante para D-84).
- `~/.claude/.../memory/project_codedkt_results.md` — A439 first=72,55% **single-seed**; **não usar** este número em MODEL-04 (multirun é 73,27%, D-78g).
- `~/.claude/.../memory/project_multirun_results.md` — Code-DKT Δ=+2,10pp first_auc média; std 3-5× menor que DKT. Vocabulário disponível para fala/QA.
- `~/.claude/.../memory/project_comparison_results.md` — Wilcoxon Code-DKT > DKT p=0,002; srcML < Code-DKT significativo; pred_df só em seed=42.
- `~/.claude/.../memory/project_codedkt_kc_difficulty.md` — curva por KC ligada a Martins; re-treino por desalinhamento do pred_df salvo (**resolvido em 2026-05-25 conforme D-83a**).
- `~/.claude/.../memory/feedback_no_em_dashes.md` — vinculante para D-87.
- `~/.claude/.../memory/feedback_tcc_writing_style.md` — ABNT + prosa acessível.
- `~/.claude/.../memory/feedback_estudantes_nao_alunos.md` — "estudantes" em prosa nova (D-89).
- `~/.claude/.../memory/feedback_abnt_tabela_slides.md` — padrão ABNT para tabelas em slides (`.eda-grid` reutilizável; D-78e).
- `~/.claude/.../memory/reference_manual_citacoes.md` — manual Facens; "tradução nossa" só em direta literal estrangeira; voz padrão é paráfrase indireta.

### Codebase context já gerado

- `.planning/codebase/STRUCTURE.md` — onde inserir slides em `apresentacao/index.html`.
- `.planning/codebase/CONVENTIONS.md` — convenções de redação e commit message style (lowercase português, prefixo `apresentacao:`).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets (sem CSS novo, exceto onde indicado)

- `.deck-topic` + `.caret.blink` (em `theme-unifacens.css`): padrão de cabeçalho `> [seção]`. Aplica em MODEL-01, MODEL-04, MODEL-05.
- `.slide-marker` + `.marker-track` + `.marker-step` + modificadores `--done`/`--running`/`--pending` + `.marker-step__mark` + `.marker-arr` + `.marker-title` + `.rel-cite`: **componente completamente pronto** para MARKER-03 reusar (commit `5d44606`, redesign CI/CD ABNT). Sem CSS novo (D-84a, D-67d herdado).
- `.bridge-seq` + `.step` + `.arr` (slide Yağcí, fundido fase 1): candidato para cronologia MODEL-01 (3 chips) E pipeline MODEL-05 (5 caixas). Verificar visualmente se 5 caixas em 1280px cabem; pode requerer ajustes de padding/tipografia.
- `.eda-grid` + `.eda-title` + `.eda-source` (anexados em commit `aa69eb1` fase 3): tabela ABNT/IBGE 1993 — 3 bordas horizontais, fundo transparente, fonte centralizada abaixo, última coluna em azul UniFacens. **Aplica em MODEL-04**.
- `.eda-fig` (`apresentacao/assets/theme-unifacens.css`): wrapper de figura. Disponível se CLOSE-03 escolher caminho de figura grande.
- `.fig-wrap` + `.fig-read` + `.fig-fonte` (slide-fig existente, CLOSE-03): já estabelecidos. Mantém estrutura atual.
- `.rel-lead` + `.rel-cite` (template `slide-related`): pode ser reusado para introdução textual de MODEL-01 e MODEL-05 sem inventar classes novas.
- Marca d'água Facens `<svg class="wm">`: replicar nos 4 novos.

### Established Patterns

- Estrutura de slide: `<section data-background-color="#F1F6FB"><div class="deck-slide slide-XYZ">...</div></section>`. **NUNCA mudar.**
- Comentário acima de cada `<section>`: `<!-- ============ SLIDE · descrição ============ -->`.
- Tipografia: títulos/corpo em Arial; tópico `>` em Cascadia 24px; "Fonte:" em Arial 17-18px.
- Cores: paleta UniFacens (`--uni-blue #2667FF`, `--uni-ink #111317`, fundo `#F1F6FB`, cinza secundário `#5b6472`).
- Citação parentética: `(Autor, ano)` sem `p. X` em paráfrase indireta; `<i>et al.</i>` ABNT (D-88).
- Iterações textuais pós-checkpoint: padrão herdado das fases 2 e 3 (média 1-3 por slide); reviewer humano ajusta no browser.

### Integration Points

- Único arquivo HTML a editar: `apresentacao/index.html`.
- CSS recebe acréscimo possível de `.chrono-step` (MODEL-01) **se** `.bridge-seq` não casar; caso contrário zero CSS novo.
- Browser: `cd apresentacao && python3 -m http.server 8000` → http://127.0.0.1:8000/#/N. Após inserção em D-75, MODEL-01 = `#/16`, slide-code → `#/17`, MODEL-04 = `#/18`, MODEL-05 = `#/19`, slide-kcfig → `#/20`, Martins p2 → `#/21`, Martins p3 → `#/22`, slide-fig → `#/23`, MARKER-03 = `#/24`.
- Sem build system; recarregar página direto.
- Para CLOSE-03 (D-83c): durante o plan, inserir 4 sections temporários (com classes mínimas e PNGs distintos); usuário visualiza; depois de escolher 1, remover os outros 3 e atualizar slide-fig com o filename escolhido. Corrigir comentário HTML linha 541.

### Slides existentes pós-fase 3 (estado HEAD; índice 0-based)

| # | classe | cabeçalho | papel na fase 4 |
|---|---|---|---|
| 0 | slide-cover-brand | (sem) | inalterado |
| 1 | slide-title-tcc | (sem) | inalterado |
| 2 | slide-agenda | (sem temático) | inalterado (revisada na fase 5) |
| 3 | slide-related | `> introdução` | inalterado |
| 4 | slide-related | `> mineração de dados educacionais` | inalterado |
| 5 | slide-phases | `> as quatro fases da edm` | inalterado |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | inalterado |
| 7 | slide-related | `> o problema do kt binário` (INTRO-03a) | inalterado |
| 8 | slide-related | `> sinal pedagógico perdido` (INTRO-03b) | inalterado |
| 9 | slide-marker--phase1 | (sem temático) | inalterado |
| 10 | slide-related | `> o dataset csedm` (INTRO-01) | inalterado |
| 11 | slide-related | `> como navegamos o csedm` (EDA-01) | inalterado |
| 12 | slide-related | `> como o aprendizado se manifesta` (EDA-03) | inalterado |
| 13 | slide-related | `> engajamento e desempenho` (EDA-04) | inalterado |
| 14 | slide-related | `> aproximação ao protocolo` (EDA-02) | inalterado |
| 15 | slide-marker--phase2 | (sem temático) | **ÂNCORA SUPERIOR** — MODEL-01 entra após este |
| 16 | slide-code | `> o que o code-dkt olha` | reaproveitado como **MODEL-03**; vira `#/17` |
| 17 | slide-kcfig | `> kcs semânticos extraídos` | reaproveitado como saída de **MODEL-05**; vira `#/20` |
| 18 | slide-problem | `> retomando o problema` (Martins p2) | reaproveitado como **CLOSE-01**; vira `#/21`. **NÃO TOCAR** |
| 19 | slide-problem | `> retomando o problema` (Martins p3) | reaproveitado como **CLOSE-02**; vira `#/22`. **NÃO TOCAR** |
| 20 | slide-fig | `> evolução por dificuldade` | reaproveitado como **CLOSE-03**; vira `#/23`. PENDING-04 picks (D-83c) |

### Slides a criar (4 novos)

| # após inserção | classe sugerida | cabeçalho | requirement |
|---|---|---|---|
| 16 | `slide-related` ou `slide-model` adaptado | `> como o code-dkt funciona` | MODEL-01 |
| 18 | `slide-related slide-eda-grid` adaptado (ABNT) | `> code-dkt no csedm` | MODEL-04 |
| 19 | `slide-related slide-pipeline` adaptado | `> extração automática de kcs` | MODEL-05 |
| 24 | `slide-marker slide-marker--phase3` | (sem temático; reusa CSS) | MARKER-03 |

Nomenclatura de classes ficou em sugestão; executor decide pelo que casa melhor com STYLE.md.

</code_context>

<specifics>
## Specific Ideas

- **MODEL-01 phrasing alvo (rascunho):**
  - Cronologia chips: `[BKT 1995 · Bayes · habilidades por KC] → [DKT 2015 · RNN · histórico sequencial] → [Code-DKT 2022 · RNN + paths AST · code2vec]`
  - Contexto: "O Code-DKT incorpora o conteúdo do código que o DKT ignorava, mantendo o tracing sequencial."
  - Bullets: `javalang → AST`; `code2vec → caminhos folha-a-folha`; `atenção pondera os caminhos`; `LSTM combina com (ProblemID, acerto/erro)`
  - Inset: `docs/figures/ast_codedkt_ptbr.svg` à direita.
  - Rodapé: `Fonte: adaptado de Shi <i>et al.</i> (2022).`

- **MODEL-04 phrasing alvo (rascunho):**
  - Cabeçalho: `> code-dkt no csedm`
  - Tabela ABNT `.eda-grid`:
    ```
    Modelo       A439   A487   A492   A494   A502
    BKT          63,21  68,40  54,20  57,81  56,92
    DKT          75,56  76,70  82,05  80,17  80,78
    Code-DKT     73,27  79,56  86,12  81,85  84,98
    Shi (2022)*  75,74    -      -      -      -
    ```
  - * Paper Shi só publica A1 (equivalente a A439).
  - Caption discreto: "first-attempt AUC: métrica primária; mede transferência entre problemas e evita autocorrelação intra-problema (Shi <i>et al.</i>, 2022, §5)."
  - Rodapé: `Fonte: elaborado pelo autor (10 seeds); Shi <i>et al.</i> (2022) Table 2.`

- **MODEL-05 phrasing alvo (rascunho):**
  - Cabeçalho: `> extração automática de kcs`
  - Abertura: "Construímos um pipeline de cinco etapas para extrair Knowledge Components do CSEDM."
  - Pipeline `.bridge-seq` 5 etapas:
    `[1. Sampling estratificado · n=5/problema] → [2. LLM gera KCs brutos · código bruto] → [3. Clustering Sentence-BERT + HAC] → [4. Rotulagem dos clusters · LLM] → [5. Q-matrix · 28 KCs / 50 problemas]`
  - Fechamento: "A decisão-chave foi alimentar o LLM com código bruto, não AST (Duan <i>et al.</i>, 2025, Tab. 4)."
  - Rodapé: `Fonte: adaptado de Duan <i>et al.</i> (2025).`

- **MARKER-03 markup-alvo:** copiar a section do MARKER-02 (`#/15`); alterar:
  - classe modificadora da `<section>` de `slide-marker--phase2` para `slide-marker--phase3`
  - pill 3 (Modelagem) modificador de `--running` para `--done` + check
  - pill 4 (Implantação) modificador de `--pending` para `--running` + ícone reload
  - badges: trocar `[running]` da pill 3 para `[done]`; adicionar `[running]` na pill 4; manter `[done]` em pills 1 e 2
  - tudo o resto idêntico (título, rodapé, classes)

- **CLOSE-03 PENDING-04 (impl):** o plan cria 4 sections temporários com a classe `slide-fig-temp-N`. Cada uma com cabeçalho temporário (e.g. `> pick: curves_by_martins`, `> pick: difficulty_martins`, etc.) e `<img>` apontando para um dos 4 PNGs em `results/`. User escolhe no browser; plan remove os 3 não-escolhidos e atualiza o slide-fig oficial. Corrige comentário HTML linha 541 do `index.html`.

</specifics>

<deferred>
## Deferred Ideas

- **`fig-read` insight de CLOSE-03:** texto da frase de leitura abaixo da figura defere para checkpoint visual após escolha do PNG (D-83d). Insight atual ("Estruturas de controle aprende rápido; Vetores e Funções ficam planos") é específico de `curves_by_martins`; refrasear se trocar.
- **All-attempts AUC e Wilcoxon visíveis no MODEL-04:** fora do slide nesta fase. Disponíveis para fala/QA e documento TCC. Critério 2 do CLAUDE.md ("reportando first-attempt AUC e all-attempts AUC") atendido pelo documento, não pelo slide.
- **Arquitetura completa Code-DKT (`codedkt_model_structure_ptbr.svg`):** reservada para documento TCC (Figura 3). Não entra em slide algum desta apresentação.
- **Redesenho visual do `.slide-marker`:** já resolvido em commit `5d44606` (pipeline CI/CD ABNT). MARKER-03 herda.
- **Transição narrativa explícita slide-kcfig → CLOSE-01:** não há ponte textual; depende da fala. Se durante checkpoint o salto soar abrupto, considerar microcópia menor em slide-kcfig ou CLOSE-01. Nesta fase, não criar requirement.
- **Caveat snippet da AST SVG ser pseudo-Python:** não redesenhar; conceito de AST é language-agnostic e a versão atual é mais didática. Reservada para nota de pé do documento TCC caso a banca pergunte.
- **MODEL-04 visualizações alternativas (`fig_comparison_bars_*.png`, `fig_seed_variance_boxplot.png`, `fig_delta_vs_dkt.png`, `fig_per_problem_heatmap.png`):** todas existem em `results/`; foram descartadas em favor de tabela ABNT por consistência com EDA-01/02. Disponíveis para slides de backup ou Q&A.
- **MODEL-05 reduzir para 3 etapas conforme PROJECT.md original:** override registrado (D-79f); 5 etapas é a versão escolhida. Reverter para 3 só se o slide ficar visualmente quebrado em 1280px durante execução.
- **MARKER-04 (fase 5) modificadores:** decisão fica para o CONTEXT da fase 5. Default: todas as 4 pills `--done` (proposta apresentada, defesa encerrada). Aqui apenas anotamos que MARKER-03 deixa pill 4 em `--running` esperando MARKER-04 fechar tudo.
- **CLOSE-01/02 ajustes textuais:** fora desta fase (já fechados na fase 1, ROADMAP Success Criteria 5 explicita "MANTÊM citação direta atual").

### Reviewed Todos (not folded)

Nenhum todo cruzado para esta fase (`gsd-sdk query todo.match-phase 4` não consultado; padrão das fases 1-3 com 0 matches).

</deferred>

---

*Phase: 4-Modelagem e Avaliação (Fase 3 EDM)*
*Context gathered: 2026-05-28*
