---
phase: 03-eda-e-pr-processamento-fase-2-edm
plan: 04
status: complete
requirements:
  - EDA-03
  - PENDING-02
key-files:
  modified:
    - apresentacao/index.html
    - apresentacao/assets/theme-unifacens.css
    - apresentacao/STYLE.md
  created:
    - scripts/build_eda_learning_curves.py
    - scripts/build_eda_xgrade_by_completed.py
    - results/sec4_learning_curves_clean.png
    - results/sec2_xgrade_by_completed.png
    - apresentacao/assets/eda-curvas-aprendizado.png
    - apresentacao/assets/eda-xgrade-completados.png
commits:
  - a51edcf
  - 8d4e37c
  - cffc4c8
---

## What Was Built

O Plan 03-04 original previa **um único slide EDA-03 com scatter PCA dos
3 perfis K-Means** (script `build_eda_pca_scatter.py`, dataset early+late+
Subject). Durante o checkpoint visual o reviewer identificou inconsistência
narrativa grave: o scatter usava 239 estudantes (subset com participação
nos 5 assignments + X-Grade), número nunca apresentado nos slides
anteriores que ancoraram a Fase 2 EDM em 413/410 (MainTable Spring 2019).

A discussão produziu uma reformulação do plan em **2 slides com figuras
reproduzíveis sobre MainTable Spring 2019**, mantendo coerência total com
EDA-01/02 e com INTRO-01 (movido no Plan 03-03).

### EDA-03 — `> como o aprendizado se manifesta` (Figura 1)

- **Texto antes da figura:** define "tentativa ordinal" e escopo (413
  estudantes Spring 2019).
- **Figura 1 — Curvas de aprendizado por assignment (Spring 2019):** 5
  subplots (`.eda-fig--wide`) sobre as 30 primeiras tentativas ordinais
  por assignment, mínimo 10 estudantes por ponto. Globais batem com
  Tabela 1: 26.15 / 20.06 / 20.34 / 24.72 / 30.62.
- **Insight:** "No A1, os estudantes precisam de várias tentativas para
  acertar; no A5, já acertam logo nas primeiras."
- Cabeçalho final escolhido: `> como o aprendizado se manifesta`
  (variante c expandida do 03-RESEARCH §7.3; mais didática que
  `> três jeitos de aprender` original).

### EDA-04 — `> engajamento e desempenho` (Figura 2)

Slide adicionado em consenso com o reviewer (não previsto no plan
original). Mantém o mesmo padrão ABNT da Tabela 1 do EDA-01.

- **Texto antes da figura:** introduz X-Grade (nota final normalizada
  0 a 1).
- **Figura 2 — X-Grade por número de assignments completados (Spring 2019):**
  boxplot (`.eda-fig--compact`) com 5 bins de 1 a 5 assignments
  (n=14, 19, 26, 73, 241). Mediana sobe de 0.16 para 0.70, std cai
  de 0.32 para 0.18.
- **Insight:** "Quanto mais assignments o estudante completa, maior a
  mediana e menor a variância da nota final."

### Reorganização cross-plan

- **EDA-02 movido** de `#/13` para `#/15`, ficando imediatamente antes
  do MARKER-02 (fecha o bloco da Fase 2 EDM com o pré-processamento).
- **EDA-02 reescrito** para incluir a confirmação `23,68% de tentativas
  corretas, mesma proporção reportada no paper, mais um sinal de que
  estamos trabalhando sob os mesmos dados, viabilizando a comparação
  direta dos resultados dos nossos modelos aos resultados dos modelos
  treinados por Shi et al. (2022)`.
- **10 substituições "aluno/alunos" → "estudante/estudantes/discentes"**
  em 6 slides do deck (slide Introdução, INTRO-01, INTRO-03b, EDA-01/03/04,
  EDA-02 e Martins p2). Citação direta literal de Martins, Marin e Alves
  (2024, p. 20) preservada — regra ABNT.

## CSS adicionado

`.eda-fig`, `.eda-fig--wide`, `.eda-fig--compact`, `.eda-insight`,
`.eda-source` em `apresentacao/assets/theme-unifacens.css`. Componentes
reutilizáveis para slides MODEL-* e CLOSE-* futuros que precisem de
figura + insight + fonte ABNT.

## Scripts reprodutíveis

- `scripts/build_eda_learning_curves.py` — lê `MainTable.csv` (Run.Program,
  413 estudantes Spring 2019), gera curvas de aprendizado por assignment.
- `scripts/build_eda_xgrade_by_completed.py` — lê `Subject.csv` (X-Grade)
  e `MainTable.csv` (count distinct assignments por estudante), gera
  boxplot.

Ambos com `matplotlib.use("Agg")`, fundo transparente, tipografia em
preto puro `#000000`, paleta UniFacens (azul `#2667FF` no boxplot;
cores distintas por assignment nas curvas).

## Acceptance Criteria

O plan original tinha critérios para o scatter PCA (`SEED=42`,
3 cores K-Means etc.) — não se aplicam à versão entregue. Critérios
substitutos validados:

| Critério | Esperado | Observado |
|---|---|---|
| Scripts existem e são Python válido | 2 scripts | 2 (`ast.parse` OK) |
| PNGs em `results/` + assets do deck | 4 PNGs | 4 (curvas + boxplot × 2) |
| Globais por assignment batem com Tabela 1 do EDA-01 | A1=26.15% etc. | match perfeito |
| Mediana X-Grade cresce monotonicamente com n_assignments | True | 0.16 → 0.44 → 0.62 → 0.61 → 0.70 |
| Slides EDA-03 e EDA-04 referenciam `assets/`, não `results/` | True | confirmado por grep |
| Sem em-dash em EDA-03/04 | 0 | 0 |
| Sem Shi/Code-DKT em EDA-03/04 | 0 | 0 (clusters são nossos) |
| Total sections em `<div class="slides">` | 21 | 21 |

## Checkpoint visual — APPROVED (após 4 iterações)

Iterações registradas:
1. Scatter PCA original com 239 estudantes — rejeitado por incoerência narrativa.
2. Curvas + boxplot com tipografia cinza e fontes pequenas — pedido reduzir e aumentar legibilidade.
3. Tipografia em preto puro, fontes ampliadas, gráfico das curvas aumentado, insight em negrito centralizado — pedido tirar negrito, alinhar à esquerda, mais respiro.
4. Insight em peso normal, alinhado em `max-width: 1060px` igual `.rel-lead`, microcópia ajustada ("logo nas primeiras"), boxplot do EDA-04 reduzido para liberar espaço ao insight — **APROVADO**.

## Deviations (vs Plan 03-04 original)

- **D-66h:** Scatter PCA descartado por incoerência narrativa (239 ≠ 413/410).
  Substituído por curvas de aprendizado + boxplot X-Grade × engajamento.
- **D-66i:** Acréscimo de 1 slide na Fase 2 EDM (EDA-04 não previsto no
  ROADMAP); aceitável porque cada insight é distinto e a mensagem
  pedagógica (engajamento correlaciona com nota) é diretamente útil ao
  argumento do TCC.
- **D-66j:** EDA-02 reposicionado de meio para fim do bloco EDA (antes
  do MARKER-02). Ordem narrativa: descrever dataset → navegá-lo →
  observar aprendizado → mostrar relação engajamento/desempenho →
  apresentar pré-processamento → fechar Fase 2.
- **D-67e (memória de feedback):** "estudantes" / "discentes" substituem
  "alunos" em prosa acadêmica do TCC. Citação direta literal preserva
  termo original do autor. Salvo como `feedback_estudantes_nao_alunos.md`.

## Self-Check: PASSED
