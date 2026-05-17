# Plano — `notebooks/07_comparison.ipynb`

Notebook de fechamento do TCC 1: consolida BKT, DKT, Code-DKT e srcML-DKT em uma comparação única, com tabelas, gráficos e teste de significância. Atende aos **Critérios 2 e 3** de conclusão definidos em `CLAUDE.md` (a Tabela comparativa por assignment e o Wilcoxon signed-rank), incorpora o resultado negativo do srcML-DKT como discussão metodológica honesta, e fornece a base do capítulo de Resultados do TCC escrito.

Baseado em: Shi et al. (2022) *Code-DKT* (EDM 2022) — protocolo de avaliação e gráficos de referência; Pankiewicz, Shi & Baker (2025) *srcML-DKT* (EDM 2025) — esquema de comparação multi-modelo e heatmap de predição por aluno; Piech et al. (2015) *Deep Knowledge Tracing* (NeurIPS 2015) — formulação original do DKT. Documentos internos consultados: [`docs/srcml_dkt_implementation.md`](srcml_dkt_implementation.md) Seções 7-8 (resultados srcML e análise do resultado negativo), [`docs/code_dkt_implementation.md`](code_dkt_implementation.md) Seções 9-10 (protocolo de avaliação e schema dos pickles), [`docs/dkt_implementation.md`](dkt_implementation.md) (protocolo DKT).

---

## 1. Contexto e objetivo

### 1.1 Por que este notebook existe

Os notebooks `04_bkt`, `05_dkt`, `06_code_dkt` e `09_srcml_dkt` rodaram cada modelo isoladamente — cada um produziu seu próprio pickle de resultados, cada um tem um sumário interno. Mas a leitura do TCC exige uma comparação consolidada: precisamos de uma única tabela, de gráficos lado-a-lado, e de uma resposta clara à pergunta "qual modelo é o melhor para o nosso dataset e por quê?". É essa síntese que `07_comparison.ipynb` produz.

Concretamente, o notebook fecha:

- **Critério 2 do CLAUDE.md:** Tabela comparativa BKT vs DKT vs Code-DKT por assignment, com first-attempt AUC e all-attempts AUC. Adaptado para incluir srcML-DKT como 4ª coluna.
- **Critério 3 do CLAUDE.md:** Teste de significância Wilcoxon signed-rank entre modelos.
- **Material para o capítulo de Discussão do TCC:** gráficos publicáveis, análise honesta do resultado negativo do srcML-DKT, comparação numérica com Shi et al. (2022) Table 1/2 e Pankiewicz et al. (2025) Table 3.

### 1.2 Escopo: o que este notebook NÃO faz

- **Não re-treina nenhum modelo.** Todos os 4 pickles já existem em `results/` (Seção 2). O notebook é puramente analítico.
- **Não substitui as análises qualitativas internas** de cada notebook (atenção do Code-DKT em `06_code_dkt.ipynb` Seção 12, métricas de transparência srcML em `09_srcml_dkt.ipynb` Seção 3). Ele faz referência cruzada quando útil mas não duplica.
- **Não faz ablation** (srcML sem Compile.Error, hiperparâmetros alternativos): essas investigações ficam para o TCC 2, registradas no Capítulo de Limitações.

---

## 2. Inputs — pickles, schema e como carregar uniformemente

Os 4 modelos têm pickles no diretório `results/`. Verificamos os schemas reais (cf. inspeção em 2026-05-17) e a tabela abaixo reflete o estado de fato — não a documentação prévia:

| Modelo | Arquivo | Tipo | Tamanho do `runs` | `pred_df` presente? |
|---|---|---|---|---|
| BKT | `bkt_results_multirun.pkl` | `dict[aid → dict]` | `len(runs) == 1` (BKT determinístico) | **Não** (`pred_df = None` em todos) |
| DKT | `dkt_results_multirun.pkl` | `dict[aid → dict]` | `len(runs) == 10` (seeds 42-51) | Sim, `(2264, 5)` em A439 |
| Code-DKT | `code_dkt_results_multirun.pkl` | `dict[aid → dict]` | `len(runs) == 10` | Sim |
| srcML-DKT | `srcml_dkt_results_multirun.pkl` | `dict[aid → dict]` | `len(runs) == 10` | Sim |

Assignments: `[439, 487, 492, 494, 502]` em todos os 4 pickles (chaves int).

### 2.1 Schema canônico (chaves de nível 1 sob cada `aid`)

Todos os 4 pickles compartilham as chaves agregadas:

```
all_auc_mean,   all_auc_std,
first_auc_mean, first_auc_std,
runs: list[dict],   # ver 2.2
```

BKT difere dos demais nas chaves laterais: tem `n_train`, `n_test`, `params` (DataFrame pyBKT). Os 3 modelos profundos têm `n_train_events`, `n_test_events`, `config`. Code-DKT e srcML-DKT têm ainda `vocab`, `problem_to_idx`, `model_state_dict_seed42`.

### 2.2 Schema de cada `runs[i]`

```
seed: int
all_auc: float
first_auc: float
pred_df: pd.DataFrame | None
```

Quando `pred_df` é não-nulo, as colunas são fixas: `['user_id' (str), 'skill_name' (str = ProblemID), 'correct' (int 0/1), 'is_first_attempt' (bool), 'correct_predictions' (float ∈ [0,1])]`. O `(2264, 5)` em A439 corresponde a 2.264 predições no test set fixo (consistente entre runs).

### 2.3 Achado importante: BKT `pred_df` é `None`

A inspeção empírica confirmou que `bkt_results_multirun.pkl[aid]['runs'][0]['pred_df'] = None` para **todos** os 5 assignments. O wrapper multirun envelopa o BKT no schema padrão, mas o notebook `04_bkt.ipynb` não persistiu as predições per-evento — só os escalares `all_auc` e `first_auc` por assignment.

**Consequência para este notebook:**

1. Não podemos fazer bootstrap sobre o `pred_df` do BKT para gerar pseudo-variância (o caminho mais limpo seria refitar pyBKT a partir de `params` e rodar `.predict()` no test set, mas isso reintroduz complexidade que não é gate do TCC).
2. **Decisão:** tratar BKT como ponto-referência escalar (1 valor por assignment, sem desvio padrão), e restringir o Wilcoxon signed-rank aos 3 modelos profundos (DKT, Code-DKT, srcML-DKT), onde temos 10 seeds × 5 assignments = 50 pares por par de modelos. Para BKT vs deep models, reportamos apenas a diferença média por assignment e descrevemos qualitativamente (não há poder estatístico em N=5 sem variância intra-assignment).
3. Documentamos no notebook que regerar `pred_df` do BKT é viável (~30 segundos com pyBKT) e fica como TODO se for necessário um teste estatístico formal envolvendo BKT — não é, para os Critérios 2 e 3.

### 2.4 Função `load_all_results()` (no notebook, Seção 2)

Função única que carrega os 4 pickles e devolve um dict aninhado uniforme:

```python
all_results = {
    'BKT':       {aid: {'first_auc_mean': ..., 'first_auc_std': 0.0, 'all_auc_mean': ..., 'all_auc_std': 0.0, 'runs': [...]}},
    'DKT':       {aid: ...},  # std real, 10 runs
    'Code-DKT':  {aid: ...},
    'srcML-DKT': {aid: ...},
}
```

A ordem fixa `['BKT', 'DKT', 'Code-DKT', 'srcML-DKT']` reflete a evolução cronológica/conceitual e é reusada em todos os gráficos para coerência visual.

---

## 3. Métricas a reportar

### 3.1 Primárias

| Métrica | O que mede | Fonte do paper |
|---|---|---|
| **First-attempt AUC** | Capacidade de prever o resultado da primeira tentativa de cada (aluno, problema) — métrica menos inflada por autocorrelação temporal | Shi et al. (2022), Table 2; Pankiewicz et al. (2025), Table 3 |
| **All-attempts AUC** | AUC sobre todas as tentativas (≤ 50 por aluno) — métrica mais clássica do DKT | Piech et al. (2015); Shi et al. (2022), Table 1 |

Ambas em `mean ± std` sobre 10 runs (DKT/Code-DKT/srcML-DKT) ou valor pontual (BKT). Métrica primária do TCC é **first-attempt AUC**, consistente com o critério 1 do CLAUDE.md ("Code-DKT A439 ≈ 74% ±3% em first-attempt AUC").

### 3.2 Decisão: pooled (per-assignment) vs pooled (global)

- **Per-assignment** (5 valores separados, um por A439-A502): formato do Shi et al. (2022) Table 1. Usado na nossa **Tabela principal** (Seção 4) e na maior parte dos gráficos.
- **Pooled global** (1 valor agregando todos os assignments): formato do Pankiewicz et al. (2025) Table 3. Reportado como **sumário executivo** na Seção 4.2 (1 linha por modelo).

Justificativa para reportar os dois: Critério 2 do CLAUDE.md pede per-assignment; mas o leitor que olhar a Table 3 do Pankiewicz et al. e quiser comparar precisa de um número pooled. Os dois formatos são complementares, não conflitantes.

### 3.3 Comparação com os valores de referência da literatura

Tabela que sobrepõe nossos valores aos da literatura, com a coluna `Δ vs paper` em pontos percentuais. Essa tabela é o material direto da seção "Comparação com a literatura" do TCC.

| Modelo | Referência | Métrica reportada | Valor no paper | Nosso valor (mean±std) |
|---|---|---|---|---|
| Code-DKT | Shi (2022) T1/T2 | A439 first / overall | 75.74% / 74.31% | ~73.27% / ~70.35% |
| DKT | Shi (2022) T1 | A439 overall | 71.24% | preencher |
| srcML-DKT | Pankiewicz (2025) T3 | first / all (pooled) | 83.55% / 84.67% | preencher (pooled) |

Importante: o paper Pankiewicz et al. usa dataset diferente (C#, 6 tasks, 610 alunos), então a coluna `Δ vs paper` para srcML-DKT é **descritiva** — não é validação de implementação. Documentar isso explicitamente.

---

## 4. Tabela comparativa principal (Critério 2 do CLAUDE.md)

### 4.1 Layout

Tabela 4x5x2 — 4 modelos (linhas) × 5 assignments (colunas) × 2 métricas (sub-células). Renderizada via `pandas.DataFrame.to_markdown()` para inclusão direta no TCC, e também como imagem `results/comparison_table.png` via `matplotlib` para slides.

Formato exemplificado (números são placeholders):

```
First-attempt AUC (mean ± std sobre 10 runs)
┌────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Modelo     │ A439         │ A487         │ A492         │ A494         │ A502         │
├────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ BKT        │ 63.21%       │ ...          │ ...          │ ...          │ ...          │
│ DKT        │ 75.56 ± 3.40 │ 76.70 ± 1.92 │ 82.05 ± 2.31 │ 80.17 ± 2.18 │ 80.78 ± 1.85 │
│ Code-DKT   │ 73.27 ± 1.34 │ 79.56 ± 0.91 │ 86.12 ± 0.65 │ 81.85 ± 0.94 │ 84.98 ± 0.81 │
│ srcML-DKT  │ 70.41 ± 1.01 │ 76.56 ± 0.87 │ 81.93 ± 0.71 │ 78.30 ± 0.90 │ 81.17 ± 0.99 │
└────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

Tabela análoga para `all-attempts AUC` logo abaixo. Em ambas, **célula em negrito = melhor modelo no assignment**.

### 4.2 Resumo pooled (1 linha por modelo)

Versão compacta no estilo Pankiewicz et al. (2025) Table 3 — útil para o resumo executivo do TCC:

```
┌────────────┬─────────────────────────┬─────────────────────────┐
│ Modelo     │ First-attempt AUC       │ All-attempts AUC        │
│            │ (pooled 5 assignments)  │ (pooled 5 assignments)  │
├────────────┼─────────────────────────┼─────────────────────────┤
│ BKT        │ ~xx.x%                  │ ~xx.x%                  │
│ DKT        │ xx.x ± y.y              │ xx.x ± y.y              │
│ Code-DKT   │ xx.x ± y.y              │ xx.x ± y.y              │
│ srcML-DKT  │ xx.x ± y.y              │ xx.x ± y.y              │
└────────────┴─────────────────────────┴─────────────────────────┘
```

Decisão sobre "pooled": agregamos por média simples das 5 médias por assignment (não AUC sobre as predições concatenadas dos 5). Razão: cada assignment tem um modelo separado treinado independentemente; AUC concatenado seria conceitualmente confuso e dependente do balanço de tamanhos entre test sets. Média de médias é o agregador mais conservador e mais legível.

### 4.3 Ressalvas a explicitar na tabela

Em nota de rodapé direto na tabela:

1. **BKT sem std** porque o modelo é determinístico e o pickle não persistiu predições para bootstrap (Seção 2.3).
2. **DKT/Code-DKT/srcML-DKT std** vem de 10 runs com seeds 42-51 (mesma faixa em todos — comparabilidade entre modelos).
3. **srcML-DKT treinou com `Compile.Error` events**; os outros 3 não. Avaliação no mesmo test set (cf. `docs/srcml_dkt_implementation.md` Seção 2 para justificativa).
4. **Code-DKT em A439 = 73.27%** (esperado ≈ 74.31% no paper, dentro de ±3% do alvo do CLAUDE.md critério 1 — o critério está satisfeito por margem).

---

## 5. Teste estatístico (Critério 3 do CLAUDE.md)

### 5.1 Decisão: Wilcoxon signed-rank apenas entre modelos profundos

Justificativa empírica (Seção 2.3): BKT não tem `pred_df` no pickle, portanto não temos variância intra-assignment para BKT — não é possível parear runs BKT vs runs DKT no nível seed-a-seed. Reportamos BKT vs deep models apenas como diferença média descritiva.

Três comparações pareadas:

| Par | Hipótese alternativa | N de pares (assignment × seed) |
|---|---|---|
| Code-DKT vs DKT | Code-DKT > DKT (esperado, replicação de Shi 2022) | 5 × 10 = 50 |
| srcML-DKT vs Code-DKT | srcML-DKT < Code-DKT (achado nosso, divergente do paper Pankiewicz 2025) | 50 |
| srcML-DKT vs DKT | bilateral (não temos hipótese forte a priori) | 50 |

### 5.2 Algoritmo concreto

Para cada par (M_A, M_B):

```python
diffs = []  # 50 valores
for aid in [439, 487, 492, 494, 502]:
    for seed in range(42, 52):
        a = get_run(results[M_A], aid, seed)['first_auc']
        b = get_run(results[M_B], aid, seed)['first_auc']
        diffs.append(a - b)

stat, p = scipy.stats.wilcoxon(diffs, alternative=<direção da hipótese>)
effect_r = stat_z / sqrt(N)   # tamanho de efeito
```

Repetir para `all_auc`. Reportar: estatística W, p-valor (com e sem correção Holm-Bonferroni para 3 comparações), tamanho de efeito r, mean(diff) ± std(diff), e bootstrap CI 95% sobre os 50 pares (1000 resamples).

### 5.3 Correção para múltiplas comparações

3 testes simultâneos sobre os mesmos dados. Aplicar **Holm-Bonferroni** (mais poderoso que Bonferroni puro, igualmente conservador no controle de FWER). Reportar p-valores ajustados em coluna separada na tabela final.

### 5.4 Expectativas vs literatura

| Comparação | Esperado | Por quê |
|---|---|---|
| Code-DKT > DKT | p < 0.05 esperado | Replica Shi (2022) Table 1: +3-4pp consistente em todos 5 assignments |
| srcML-DKT < Code-DKT | p < 0.05 esperado, com sinal **invertido vs Pankiewicz 2025** | srcML ficou -2.9 a -4.2pp em todos 5 assignments (cf. `srcml_dkt_implementation.md` Seção 7.1) |
| srcML-DKT vs DKT | possivelmente não-significativo | Os deltas são pequenos e inconsistentes em sinal (A439 srcML < DKT, A492 srcML ≈ DKT) — verificar empiricamente |

A divergência esperada com Pankiewicz et al. é **a contribuição** deste notebook do ponto de vista do TCC. A Seção 7 (Discussão) trata como reportar isso sem rebaixar nem o paper nem o nosso trabalho.

### 5.5 BKT vs deep models: tratamento descritivo

Para cada deep model M, reportar tabela 5×1 com `diff_aid = mean(M_aid) - BKT_aid`. Sem teste estatístico, com nota explícita: "BKT é determinístico; diferença reportada sem inferência estatística por ausência de variância intra-assignment no pickle persistido. Direção da diferença é consistente em todos 5 assignments (deep models > BKT), o que é descritivo da magnitude do salto."

---

## 6. Gráficos a produzir

Cada gráfico documentado abaixo: tipo, eixos, o que comunica, **origem** (paper + figura quando for replicação ou adaptação), arquivo de saída.

### 6.1 Visão geral — barras agrupadas por assignment × modelo

- **Tipo:** grouped bar chart, 4 barras por assignment (uma por modelo), 5 grupos (assignments)
- **Eixos:** x = assignment (A439...A502); y = first-attempt AUC; cor = modelo
- **Anotações:** barra de erro = ±1 std (apenas para DKT/Code-DKT/srcML-DKT); linha pontilhada horizontal em 0.5 (chance)
- **O que comunica:** visão de helicóptero da Tabela 4.1 — "o leitor entende o resultado principal em 5 segundos"
- **Origem:** inspirado em Shi et al. (2022) Table 1 (apresentação tabular) e Pankiewicz et al. (2025) Table 3 (formato compacto), mas como gráfico em vez de tabela. Não há figura equivalente direta nos papers — é nossa síntese visual.
- **Arquivo:** `results/fig_comparison_bars_first_auc.png` (+ `_all_auc.png`)

### 6.2 Distribuição sobre seeds — boxplot por modelo dentro de cada assignment

- **Tipo:** boxplot/violin, 4 caixas por painel (uma por modelo profundo + BKT como linha horizontal), 5 painéis (um por assignment)
- **Eixos:** x = modelo; y = first-attempt AUC; cada caixa agrega os 10 valores (seeds 42-51)
- **O que comunica:** **a estabilidade dos runs**, que é o argumento metodológico mais forte do Code-DKT/srcML-DKT em relação ao DKT (std ~5x menor — registrado em [[project_multirun_results]]). DKT tem caixa larga; Code-DKT/srcML-DKT têm caixas bem mais estreitas.
- **Origem:** original. Os papers não publicam essa visualização (reportam apenas mean±std em tabela). É um diferencial do nosso trabalho — multirun completo permite mostrar a forma da distribuição, não só seus dois primeiros momentos.
- **Arquivo:** `results/fig_seed_variance_boxplot.png`

### 6.3 Δ vs DKT — barras divergentes

- **Tipo:** barras divergentes (positivas para cima, negativas para baixo), 3 barras por assignment (Code-DKT − DKT, srcML-DKT − DKT, srcML-DKT − Code-DKT), 5 grupos
- **Eixos:** x = assignment; y = Δ first-attempt AUC (pp); linha zero destacada
- **O que comunica:** **direção e magnitude consistentes**. Esperamos ver: barras Code-DKT−DKT positivas em 4-5 dos 5 assignments (replicando Shi 2022); barras srcML−Code-DKT consistentemente negativas em todos 5 (achado nosso).
- **Origem:** original. Análoga ao formato "improvement over baseline" usado em diversos papers de KT (Shi 2022 discussão pp.6 reporta "+3-4% AUC across all assignments"), mas como gráfico.
- **Arquivo:** `results/fig_delta_vs_dkt.png`

### 6.4 Heatmap per-problem within assignment

- **Tipo:** heatmap, 4 linhas (modelos) × 10 colunas (ProblemIDs do assignment), uma figura por assignment ou painel facetado
- **Eixos:** linhas = modelo; colunas = ProblemID; cor = first-attempt AUC daquele problema, com média sobre 10 seeds (DKT/Code/srcML)
- **Cálculo:** para cada (modelo, aid, problema), filtrar `pred_df` por `skill_name == problema` e `is_first_attempt == True`, computar AUC; média sobre os 10 seeds dos deep models. Para BKT, regerar `pred_df` no notebook (Seção 2.3) **OU** marcar células como N/A — decisão a tomar empiricamente: se gerar BKT é trivial (<30s), incluir; caso contrário, deixar linha BKT em cinza com nota "predições per-evento não persistidas, ver Seção 2.3".
- **O que comunica:** granularidade — quais problemas dentro de cada assignment beneficiam mais dos code features. Replica conceitualmente a Table 3 de Shi et al. (2022), que decompõe o AUC do A1 por problema entre DKT e Code-DKT.
- **Origem:** Shi et al. (2022) **Table 3** — decomposição por problema na assignment A1. Nós generalizamos para 4 modelos × 5 assignments.
- **Arquivo:** `results/fig_per_problem_heatmap.png`

### 6.5 Heatmap de predições por aluno (case study)

- **Tipo:** heatmap, 3 linhas (DKT, Code-DKT, srcML-DKT) × N colunas (tentativas em ordem cronológica), cor = `correct_predictions`, anotação na célula = ground truth (0/1)
- **Seleção de aluno:** 1-2 alunos selecionados com critério explícito: (a) ao menos 5 tentativas no test set; (b) mistura de acerto/erro nas tentativas; (c) ao menos uma tentativa em que os 3 modelos divergem em mais de 0.2 na probabilidade prevista. Critério (c) garante que o heatmap mostra algo interessante.
- **O que comunica:** **comportamento qualitativo dos modelos** — onde acertam, onde divergem, onde se enganam juntos. É o tipo de figura que sustenta a narrativa "o srcML está abaixo do Code-DKT porque...".
- **Origem:** **Pankiewicz et al. (2025) Figure 2** (heatmap comparativo DKT/Code-DKT/srcML-DKT em 4 tentativas de 1 aluno em T4) e **Shi et al. (2022) Figures 4 e 5** (heatmap separado de Code-DKT e DKT em todas as predições de 1 aluno em A1). Nosso layout é mais próximo do Pankiewicz (3 modelos numa única figura) mas pode incluir BKT como 4ª linha se regenerarmos seu `pred_df`.
- **Arquivo:** `results/fig_student_heatmap_{user_id}.png` (1-2 figuras)

### 6.6 Mean ± std como forest plot (opcional, se sobrar tempo)

- **Tipo:** forest plot — 4 modelos × 5 assignments = 20 pontos com barras de IC 95%, sobre o eixo first-attempt AUC
- **O que comunica:** alternativa à Tabela 4.1 com IC explícito; útil para slides
- **Origem:** original (formato comum em meta-análises e clinical trials)
- **Decisão:** incluir só se as 5 figuras anteriores ficarem prontas no tempo planejado da Seção 8.

### 6.7 Resumo de gráficos vs origem

| # | Figura | Origem | Adaptação |
|---|---|---|---|
| 6.1 | Barras agrupadas | Inspirado em Shi 2022 T1 + Pankiewicz 2025 T3 | Tabela → gráfico; 4 modelos |
| 6.2 | Boxplot por seed | **Original** | — |
| 6.3 | Δ vs DKT | Inspirado em narrativa "+3-4%" de Shi 2022 | — |
| 6.4 | Heatmap per-problem | Shi 2022 **Table 3** | Generalizado para 4 modelos × 5 assignments |
| 6.5 | Heatmap por aluno | Pankiewicz 2025 **Figure 2** + Shi 2022 **Figures 4-5** | Layout Pankiewicz; possível 4ª linha BKT |
| 6.6 | Forest plot (opc.) | Convenção meta-analítica | — |

Não replicamos figuras de arquitetura (Shi 2022 Fig 1/3, Pankiewicz 2025 Fig 1) — essas pertencem aos capítulos de Metodologia (`docs/code_dkt_implementation.md` e `docs/srcml_dkt_implementation.md`), não ao capítulo de Resultados.

---

## 7. Discussão — como contar essa história no TCC

### 7.1 Estrutura da seção 13 do notebook

A célula de Discussão (penúltima do notebook, antes do sumário executivo) tem 4 sub-seções em texto Markdown:

1. **Hierarquia esperada confirmada:** Deep models > BKT em todos os assignments. Magnitude do salto: ~5-15 pp em first-attempt AUC. Comentar a relação com Shi 2022 Section 6 RQ1.
2. **Code-DKT > DKT confirmado, com significância estatística:** Wilcoxon p < 0.05 esperado. Magnitude consistente com Shi (2022) Table 1 (+3-4pp). Discutir a redução de variância sobre seeds como contribuição adicional do Code-DKT (não documentada no paper original, achado nosso registrado em [[project_multirun_results]]).
3. **srcML-DKT abaixo do Code-DKT — divergência do paper Pankiewicz et al.** Subsessão dedicada (Seção 7.2 abaixo).
4. **Implicações para o TCC 2:** qual é o modelo-base recomendado e por quê.

### 7.2 Sub-seção sobre o srcML-DKT — postura explícita

Esta é a sub-seção mais delicada do notebook. Postura a adotar (alinhada com `docs/srcml_dkt_implementation.md` Seção 8 e [[feedback_protocol_fidelity]]):

- **Não esconder.** O srcML-DKT é um peer dos outros 3 na tabela, não nota de rodapé.
- **Não rebaixar o paper.** Pankiewicz et al. publicou em short paper (8 páginas, EDM 2025) sem código aberto. A regra de tokenização do XML não é especificada. É inteiramente plausível que a implementação deles seja diferente da nossa, e que essa diferença explique o gap entre +1.65pp (paper) e -2.9 a -4.2pp (nosso).
- **Não rebaixar o nosso trabalho.** A cobertura de parsing de 100% (43.661/43.661, incluindo 109k Compile.Error) confirma o ganho metodológico central da abordagem. O resultado em AUC é negativo, mas isso é um **achado científico legítimo** que motiva trabalho futuro.
- **Enquadrar como contribuição metodológica.** A frase-âncora a usar no TCC (também presente em `srcml_dkt_implementation.md` Seção 10.3):

> "Apesar de o parser ter alcançado 100% de cobertura, o modelo final ficou 2.9 a 4.2 pontos percentuais abaixo do Code-DKT em first-attempt AUC, em todos os 5 assignments. Nossa hipótese para a divergência é que a regra de tokenização do XML srcML, não publicada no paper de referência, é determinante para o resultado. O vocabulário de paths que conseguimos extrair tem aproximadamente um terço do tamanho do gerado pelo javalang, o que reduz a discriminação efetiva da atenção code2vec. Esse achado é uma contribuição metodológica útil: aponta para um detalhe de implementação que merece publicação em trabalhos futuros sobre o método."

- **Wilcoxon com sinal invertido.** Esperamos p < 0.05 favorecendo Code-DKT sobre srcML-DKT — direção oposta à do paper. Reportar literalmente: "diferença estatisticamente significativa com sinal invertido em relação ao reportado por Pankiewicz et al. (2025) Table 3". Isso é fato, não opinião.

### 7.3 Conclusão — qual modelo para o TCC 2

Recomendação clara e justificada: **Code-DKT é o modelo-base do TCC 2**. Razões:

1. Maior first-attempt AUC pooled.
2. Estabilidade sobre seeds (std 3-5× menor que DKT).
3. Resultado replicável ao paper de referência (Critério 1 do CLAUDE.md confirmado para A439).
4. srcML-DKT, apesar do potencial (cobertura de Compile.Error), exige investigação adicional de tokenização e tuning antes de ser usado em produção — fica como Linha 1 de trabalho futuro.

---

## 8. Estrutura do notebook em células

Espelhando o estilo dos planos anteriores (`docs/srcml_dkt_plan.md` Seção "Estrutura do notebook 09", `docs/code_dkt_implementation.md` Seção 13). Estimativas conservadoras de tempo de execução.

| # | Seção | Conteúdo | Tempo |
|---|---|---|---|
| 1 | Setup | Imports (pandas, numpy, scipy.stats, matplotlib, seaborn, sklearn.metrics), `set_global_seed(42)`, paths, configuração de estilo dos plots | <5s |
| 2 | Carregamento uniforme | `load_all_results()` carrega os 4 pickles e monta o dict `all_results` (Seção 2.4). Verificações: 5 assignments em cada, 10 runs em DKT/Code/srcML, 1 run em BKT, schema das chaves coerente | ~10s |
| 3 | Tabela comparativa principal | Construir DataFrame 4×5×2; renderizar com `pandas.style` (negrito no melhor por assignment); salvar `.md` e `.png` (Seção 4) | ~5s |
| 4 | Tabela pooled (1 linha por modelo) | Agregar média de médias; comparar com valores do Shi 2022 e Pankiewicz 2025 (Seção 4.2) | ~2s |
| 5 | Comparação com a literatura | Tabela paralela: nossos valores vs paper de referência; coluna Δ; nota de rodapé sobre datasets diferentes para srcML-DKT (Seção 3.3) | ~2s |
| 6 | Wilcoxon signed-rank | 3 comparações sobre `first_auc` e 3 sobre `all_auc` = 6 testes; aplicar Holm-Bonferroni; reportar W, p, p_adj, effect_r, mean_diff, CI 95% bootstrap (Seção 5) | ~10s (bootstrap 1000 resamples) |
| 7 | BKT vs deep models — descritivo | Tabela 3×5 de diferenças médias (sem teste estatístico); nota explícita sobre BKT pred_df=None (Seção 5.5) | ~2s |
| 8 | Gráfico 6.1 — barras agrupadas | first_auc + all_auc (2 figuras); salvar em `results/` | ~5s |
| 9 | Gráfico 6.2 — boxplot por seed | 5 painéis (um por assignment); salvar | ~5s |
| 10 | Gráfico 6.3 — Δ vs DKT | barras divergentes; salvar | ~3s |
| 11 | Gráfico 6.4 — heatmap per-problem | Computar AUC por (modelo, aid, problema) a partir dos `pred_df`; render heatmap; para BKT decidir empiricamente se regerar `pred_df` ou marcar N/A (Seção 6.4) | ~30s |
| 12 | Gráfico 6.5 — heatmap de aluno | Selecionar 1-2 alunos por critérios da Seção 6.5; render heatmap com `correct_predictions` colorido e ground truth como annotation | ~10s |
| 13 | Discussão | Markdown com 4 sub-seções (Seção 7.1); ~400-600 palavras | — |
| 14 | Sumário executivo | Recomendação para o TCC 2; resposta direta aos Critérios 1, 2, 3 do CLAUDE.md (Seção 7.3) | — |
| 15 | Serialização (opcional) | Salvar tabelas em `results/comparison_summary.json` para consumo futuro (TCC 2) | ~1s |

Tempo total de execução estimado: **~1.5 minuto** (notebook puramente analítico, sem treino). Tamanho final esperado: ~40-60 cells, ~80-120 KB de notebook.

---

## 9. Critérios de sucesso

Vinculados aos Critérios de Conclusão do TCC 1 (CLAUDE.md "Critérios de Conclusão do TCC 1"):

1. **Critério 1 (Code-DKT A439 ≈ 74% ±3%)** — já satisfeito pelo `06_code_dkt.ipynb` (73.27% pooled sobre 10 runs, dentro da banda). `07_comparison.ipynb` apenas reporta esse fato na Seção 5.
2. **Critério 2 (Tabela comparativa)** — Seções 3 e 4 do notebook produzem a tabela 4×5×2 (Seção 4.1 deste plano) + a tabela pooled (Seção 4.2 deste plano). **Marcado como atendido** quando ambas estão renderizadas em Markdown e PNG no `results/`.
3. **Critério 3 (Wilcoxon signed-rank)** — Seção 6 do notebook produz 6 testes (3 pares × 2 métricas) com correção Holm-Bonferroni. **Marcado como atendido** quando a tabela de p-valores está renderizada e os p_adj < 0.05 estão destacados.
4. **Critério 4 (notebooks executáveis do zero com seed fixo)** — `07_comparison.ipynb` carrega 4 pickles pré-existentes; o `set_global_seed(42)` na Seção 1 garante reprodutibilidade dos passos estocásticos (bootstrap CI). Não há treino, portanto não há risco de divergência por não-determinismo CUDA.

Critérios técnicos adicionais (não em CLAUDE.md mas necessários para a coerência do notebook):

5. Todos os 5 gráficos da Seção 6 (excluindo o forest plot opcional 6.6) renderizados sem erros.
6. Nenhuma referência a `pred_df` do BKT sem o guard `is not None` (evitar `AttributeError`).
7. Notebook executa end-to-end em menos de 2 minutos (sem treino).
8. Seção 13 (Discussão) tem ≥400 palavras e cobre as 4 sub-seções da Seção 7.1 deste plano.

---

## 10. Pontos em aberto

Decisões a confirmar com o autor antes da implementação. Cada item tem uma recomendação default que vamos usar se não houver resposta explícita.

1. **Regerar `pred_df` do BKT?** Default: **não**. Justificativa: BKT vs deep model não precisa de Wilcoxon (Seção 5.5), e o heatmap per-problem (6.4) funciona com linha BKT marcada como "N/A". Se o autor quiser BKT com per-problem AUC e/ou Wilcoxon BKT vs DKT, fazemos a regeneração (~30 segundos via pyBKT) no notebook como Seção 2b. **A confirmar.**

2. **Quantos alunos no heatmap de case study (6.5)?** Default: **2 alunos**, um onde Code-DKT vence srcML claramente e outro onde os modelos convergem. Se o autor preferir 1 só (mais espaço para a anotação), reduzir.

3. **Forest plot opcional (6.6)?** Default: **não incluir** na primeira versão (tempo apertado). Pode-se adicionar em revisão se a banca pedir.

4. **Pooled = média de médias ou média de runs?** Default: **média de médias** (mais robusto a desbalanço de tamanhos de assignment). Alternativa: média de todos os 50 valores (10 seeds × 5 assignments). As duas dão números muito próximos na prática; média de médias é mais conservadora.

5. **Linguagem do notebook (markdown cells)** — default: **Português BR**, consistente com os outros notebooks e com `CLAUDE.md`. Comentários no código em inglês curto (variável names, docstrings) seguindo o padrão dos `src/` modules.

6. **Salvar `results/comparison_summary.json`** (Seção 15)? Default: **sim** — útil para o TCC 2 consumir sem precisar reprocessar os pickles. Schema: `{"per_assignment": {modelo: {aid: {first_mean, first_std, all_mean, all_std}}}, "pooled": {modelo: {first, all}}, "wilcoxon": {par: {p, p_adj, effect_r}}}`.

7. **Incluir tempo de inferência por modelo na Seção 5?** Default: **não** — não é Critério do CLAUDE.md e adiciona ruído à narrativa principal. Pode-se reportar separadamente no `docs/comparison_plan.md` follow-up se relevante.

---

## 11. Caminhos dos artefatos

| Artefato | Caminho | Status no início | Status ao final |
|---|---|---|---|
| `bkt_results_multirun.pkl` | `results/` | Existe (4.4 KB) | Inalterado |
| `dkt_results_multirun.pkl` | `results/` | Existe (266 KB) | Inalterado |
| `code_dkt_results_multirun.pkl` | `results/` | Existe (~76 MB) | Inalterado |
| `srcml_dkt_results_multirun.pkl` | `results/` | Existe (~69 MB) | Inalterado |
| Notebook | `notebooks/07_comparison.ipynb` | Não existe | **Criado** (~50 cells) |
| Tabela 4.1 | `results/comparison_table_first_auc.md`, `.png` | — | **Criado** |
| Tabela 4.2 (pooled) | `results/comparison_table_pooled.md`, `.png` | — | **Criado** |
| Fig 6.1 (barras) | `results/fig_comparison_bars_{first,all}_auc.png` | — | **Criado** |
| Fig 6.2 (boxplot) | `results/fig_seed_variance_boxplot.png` | — | **Criado** |
| Fig 6.3 (Δ vs DKT) | `results/fig_delta_vs_dkt.png` | — | **Criado** |
| Fig 6.4 (heatmap per-problema) | `results/fig_per_problem_heatmap.png` | — | **Criado** |
| Fig 6.5 (heatmap aluno) | `results/fig_student_heatmap_{user_id}.png` | — | **Criado** (1-2 arquivos) |
| Sumário JSON | `results/comparison_summary.json` | — | **Criado** (default sim — Seção 10 ponto 6) |

Tamanho total dos artefatos novos: ~500 KB-2 MB (apenas notebook + PNGs + JSON), todos versionáveis e leves o suficiente para commit direto.

---

## 12. Resumo executivo do plano

- `notebooks/07_comparison.ipynb` é um notebook **puramente analítico**: carrega 4 pickles, não treina nada, executa em <2 min.
- Atende **Critério 2** (tabela comparativa BKT vs DKT vs Code-DKT vs srcML-DKT por assignment) e **Critério 3** (Wilcoxon signed-rank) do CLAUDE.md.
- **BKT tem `pred_df = None`** — restringimos Wilcoxon aos 3 modelos profundos (50 pares por par); BKT vs deep models é descritivo.
- **5 gráficos principais** (+ 1 opcional): visão geral em barras, variância por seed em boxplot, Δ vs DKT, heatmap per-problem (inspirado em Shi 2022 Table 3) e heatmap por aluno (inspirado em Pankiewicz 2025 Figure 2 + Shi 2022 Figs 4-5).
- **Discussão honesta** do resultado negativo do srcML-DKT (−2.9 a −4.2pp em first-attempt AUC, divergente do paper de referência) enquadrada como contribuição metodológica — não como erro ou nota de rodapé.
- **Recomendação final** para o TCC 2: Code-DKT como modelo-base, com srcML-DKT como Linha 1 de trabalho futuro (ablation + retuning de tokenização).
