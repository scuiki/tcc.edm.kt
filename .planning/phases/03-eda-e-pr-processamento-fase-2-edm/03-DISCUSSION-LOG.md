# Phase 3 — Discussion Log

**Date:** 2026-05-28
**Mode:** discuss-phase (interactive, sem flags)
**Outcome:** CONTEXT.md gravado; pronto para `/gsd-plan-phase 3`

---

## Gray Areas Apresentadas

Após análise da fase com base em PROJECT.md / REQUIREMENTS.md / STATE.md / 02-CONTEXT.md / 02-PHASE-SUMMARY.md / docs/eda_insights.md / memórias, identifiquei 4 candidatos:

1. **EDA-03 — qual gráfico de insight (PENDING-02)**
2. **EDA-01 — foco do slide sem repetir INTRO-01**
3. **EDA-02 — splits (410 Shi vs 246 Release/Train) e etapas concretas**
4. **Microcópia textual dos 3 EDAs**

Decisões já travadas (não apresentadas como gray area):
- Posição no DOM (após MARKER-01 `#/10`, antes do slide-code `#/11`): travada pelo STYLE.md §Gaps reservados (atualizado pelo plan 02-04 da fase 2).
- Padrão de cabeçalho `> [seção]`, voz própria, sem em-dash, `<i>et al.</i>` ABNT, citações ABNT: herdados das fases 1-2.
- MARKER-02 visual: mecânico, sem decisões de design (memória `feedback-marker-design` trava modificadores).
- D-38b da fase 2 mandata ponte 413 → 410 → 328/82 em EDA-02.
- Componente `.slide-marker` redesenhado em `5d44606` (pipeline CI/CD ABNT).

**Seleção do usuário (multiSelect):** áreas 1, 2 e 3. Microcópia descartada (decisão derivada: gsd-planner propõe phrasing e reviewer ajusta no checkpoint visual, conforme padrão herdado da fase 2).

---

## Área 1 — EDA-03 (gráfico do insight)

### Pergunta 1: qual gráfico vai no EDA-03?

**Opções apresentadas:**
- Perfis K-Means (3 clusters) — insight "em risco = pouco engajamento, não muito erro"
- Desbalanceamento 3,22:1 (sec5_imbalance.png) — motiva escolha de AUC
- Distribuição de tentativas (sec4_sequence_distribution.png) — motiva truncagem
- Correlação Compile.Error × Label (ρ=-0,569)

**Seleção:** Perfis K-Means (3 clusters).

**Decisão capturada:** D-66 — scatter PCA 2D com 3 clusters. PNG não existe pronto; gsd-planner gera reusando código de `notebooks/01_eda.ipynb` linha 2330 (Seção 2.3).

### Pergunta 2: como o gráfico dos 3 perfis aparece?

**Opções apresentadas:**
- Scatter PCA (2 dim) com 3 clusters coloridos + legenda
- Tabela síntese (3 linhas × 4 colunas)
- Bar chart duplo: tentativas médias × perfil
- Combo: tabela compacta + microvisual

**Seleção:** Scatter PCA (2 dim) com 3 clusters coloridos + legenda. Selected preview confirmado.

**Decisão capturada:** D-66 (forma visual) — scatter PCA com cores acessíveis da paleta UniFacens; eixos rotulados PC1/PC2; legenda inline. Insight central (D-66a) acompanha em destaque textual abaixo ou ao lado.

---

## Área 2 — EDA-01 (foco sem repetir INTRO-01)

### Pergunta 1: qual o foco do EDA-01?

**Opções apresentadas:**
- Distribuição por assignment (A1..A5)
- Composição dos eventos (Run.Program × Compile.Error)
- Hub narrativo "como navegamos a base via Shi"
- Combo: distribuição por assignment + nota sobre Compile.Error

**Seleção:** (no option selected) com nota textual: "hub narrativo + distribuição por assignment talvez fique interessante, talvez fique com elementos demais, mas podemos tentar".

**Decisão capturada:** D-64 — combo das opções 3+1 (hub narrativo + tabela A1..A5). Calibração de densidade reservada ao plan/checkpoint visual (D-64b). Composição dos eventos (Run.Program vs Compile.Error) explicitamente reservada para fase 4 / MODEL-01 (não entra em EDA-01 nem EDA-02).

---

## Área 3 — EDA-02 (splits e etapas)

### Pergunta 1: quais números e splits o EDA-02 comunica?

**Opções apresentadas:**
- Protocolo Shi (D-38b): 413 → 410 → 328/82
- Release/Train pré-existente (246 alunos, 3 assignments avaliáveis)
- Ambos: "começamos com Release/, migramos para protocolo Shi"

**Seleção:** Protocolo Shi (D-38b).

**Decisão capturada:** D-65 — comunicar apenas o protocolo Shi (coerente com CLAUDE.md e com os resultados que serão reportados em MODEL-04 da fase 4). Release/Train fica disponível como resposta a pergunta da banca (deferred).

### Pergunta 2: quais etapas de pré-processamento o EDA-02 lista?

**Opções apresentadas (multiSelect):**
- Filtro min_attempts ≥ 3
- Truncagem em 50 últimas tentativas
- Threshold binário correct = (Score == 1.0)
- Separação Run.Program vs Compile.Error

**Seleção:** Filtro min_attempts ≥ 3 + Truncagem em 50.

**Decisão capturada:** D-65a — apenas 2 etapas concretas. Threshold binário fica como discretion do gsd-planner (1 linha extra se houver espaço); separação Run.Program/Compile.Error fica explicitamente para a fase 4 (MODEL-01).

---

## Checkpoint Final

### Pergunta: mais algo a travar antes de gerar o CONTEXT.md?

**Opções apresentadas:**
- Pode fechar e gravar CONTEXT.md
- Discutir cabeçalhos temáticos dos 3 EDAs
- Discutir ordem de implementação e granularidade de commits

**Seleção:** Pode fechar e gravar CONTEXT.md.

**Decisão capturada:** cabeçalhos `> [seção]` ficam em aberto (D-63a/b/c); gsd-planner propõe e reviewer ajusta. Ordem de implementação e granularidade de commits seguem padrão herdado da fase 2 (1 plan por slide, 1 commit funcional por plan).

---

## Deferred Ideas (capturadas no CONTEXT.md §Deferred)

- Microcópia textual antes da execução
- Threshold Score==1.0 como 1 linha extra
- Separação Run.Program / Compile.Error (reservado fase 4)
- Caveat técnico silhouette k=3 vs k=2 (nota privada)
- Release/Train vs MainTable+Shi como narrativa de evolução (resposta a banca)
- Bar chart / tabela síntese pura no EDA-03 (backup do scatter PCA)

---

*Discussion log written: 2026-05-28*
