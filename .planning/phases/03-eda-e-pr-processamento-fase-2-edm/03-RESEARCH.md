# Phase 3: EDA e Pré-processamento (Fase 2 EDM) - Research

**Researched:** 2026-05-28
**Domain:** Slides reveal.js (HTML/CSS) + comunicação narrativa de EDA + pré-processamento sobre dataset CSEDM (Spring 2019, 410 alunos pós-Shi); reuso mecânico de componente CSS `.slide-marker` (redesign CI/CD)
**Confidence:** HIGH (números do dataset rodados com pandas em 2026-05-28; phrasing Shi §4.1 lido literalmente; MARKER-01 markup HEAD inspecionado; números do eda_insights.md confrontados com saída atual do notebook 01)

## Summary

A Fase 3 insere 4 sections novos em `apresentacao/index.html` entre o slide MARKER-01 (linha 200-243, atual `#/10`) e o slide-code (linha 247-294, atual `#/11`). Três deles são slides EDA com voz autoral em paráfrase indireta (EDA-01 tabela A1..A5, EDA-02 ponte 413 → 410 → 328/82, EDA-03 scatter PCA com insight de engajamento), e o quarto é MARKER-02 que reusa o componente `.slide-marker` redesenhado em commit `5d44606` (pipeline CI/CD ABNT). A pesquisa verificou (a) os números por assignment com pandas sobre MainTable.csv, confirmando que o eda_insights.md Seção 1.1 (Release/Train, 246 alunos) **diverge** dos números MainTable Spring 2019 (Run.Program total), (b) os números do K-Means na saída ATUAL do notebook 01_eda.ipynb (cell 46) **divergem** do eda_insights.md Seção 3.1 — o notebook re-executado mostra 239 estudantes (não 453) com perfis Alto=96 / Em risco=124 / Médio=19, (c) phrasing exato de Shi et al. (2022) §4.1 que sustenta a paráfrase de EDA-02 (filter 4:1 = 80/20, "we fixed the longest length of student attempts at 50"), (d) MARKER-01 HEAD já tem pill 2 em `--running` (não `--pending` como CONTEXT supôs); deltas para MARKER-02 são pill 2 → `--done` e pill 3 → `--running`, (e) cell 51 do notebook 01 reproduz exatamente os números MainTable+Spring 2019 com 23,68% global.

**Primary recommendation:** Implementar na ordem MARKER-02 → EDA-02 → EDA-01 → EDA-03 (do mais determinístico ao mais arriscado). Para EDA-01 usar os números da **cell 51 do notebook 01** (MainTable Spring 2019, n=386/340/361/315/306; % correto=26,15/20,06/20,34/24,72/30,62) — coerente com EDA-02 (que comunica 413 → 410), substituindo os números de Release/Train que estão em eda_insights.md Seção 1.1. Para EDA-03, **re-executar a cell 46** antes de gravar números no slide; os outputs atuais (Alto=96, Médio=19, Em risco=124, total=239) e silhouette k=3=0,2564 são os valores reais; os números do CONTEXT D-66c (453 estudantes, 139/66/248) vieram do eda_insights.md desatualizado. Para MARKER-02, copiar o `<section>` do MARKER-01 (linhas 200-243) e alterar quatro coisas mecânicas: classe modificadora `--phase1` → `--phase2`, pill 2 `--running`+`&#x21BB;`+`[running]` → `--done`+`&check;`+`[done]`, pill 3 `--pending`+`&#x25CB;`+badge vazio → `--running`+`&#x21BB;`+`[running]`, pill 4 inalterada. Zero CSS novo.

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-60:** Os 4 slides entram após o slide 10 (MARKER-01) e antes do atual slide 11 (`slide-code`, futuro MODEL-03). Ordem dentro do bloco: EDA-01 → EDA-02 → EDA-03 → MARKER-02.
- **D-61:** Posição já consistente com `apresentacao/STYLE.md` §Gaps reservados linha 130; nenhuma correção do STYLE.md é necessária nesta fase. Após inserção, slide-code passa de `#/11` para `#/15`; demais slides existentes deslocam +4.
- **D-62:** Justificativa narrativa: MARKER-01 fecha Fase 1 EDM com "Definição do Problema ✓"; EDA-01 abre dizendo "agora navegamos o dataset que descrevemos no INTRO-01"; EDA-02 mostra decisões de pré-processamento; EDA-03 entrega o insight; MARKER-02 fecha a Fase 2 EDM.
- **D-63a (EDA-01):** cabeçalho em aberto; sugestão neutra `> como navegamos o csedm` ou `> o curso por dentro`. Decisão de phrasing final fica no plan/checkpoint visual.
- **D-63b (EDA-02):** cabeçalho em aberto; sugestão neutra `> pré-processamento` ou `> aproximação ao protocolo`. Decisão no plan/checkpoint visual.
- **D-63c (EDA-03):** cabeçalho em aberto; sugestão neutra `> perfis dos alunos` ou `> três jeitos de aprender`. Decisão no plan/checkpoint visual.
- **D-63d (MARKER-02):** sem `.deck-topic` no padrão `> [seção]`; herda exatamente o layout do MARKER-01 redesenhado; título `> AS QUATRO FASES DA EDM` em Arial bold 24px via classe `.marker-title`.
- **D-64 (EDA-01 combo):** parágrafo curto + tabela/cards A1..A5. Colunas mínimas: assignment (A1..A5 / 439/487/492/494/502), n alunos, n problemas, taxa de acerto.
- **D-64a:** **gsd-planner valida** se números do eda_insights.md Seção 1.1 (Release/Train, 246 alunos) sustentam-se em MainTable+protocolo Shi (410 alunos). Ver §2 deste RESEARCH para a reconciliação verificada (eles divergem; **usar os números MainTable**).
- **D-64b:** combo enxuto (parágrafo 2-3 linhas + 5 cards/tabela compacta); reviewer humano ajusta no checkpoint visual; iterações textuais esperadas (média 2 por slide, padrão fase 2).
- **D-64c:** os números globais já mostrados em INTRO-01 (413 estudantes, 5 assignments × 10 problemas, 201 mil eventos, 6 colunas-chave) **NÃO** voltam em EDA-01.
- **D-65 (EDA-02 split):** protocolo Shi: 413 (CSEDM bruto) → 410 (filtro `min_attempts ≥ 3`) → 328 treino / 82 teste (split 80/20, random_state=1). Liga direto com MODEL-04 (A439 first_auc=72,55%, ±3% do paper). NÃO mencionar Release/Train.
- **D-65a (etapas listadas):** (1) Filtro `min_attempts ≥ 3` → 410 alunos. (2) Truncagem em 50 últimas tentativas (mediana 32, P95=109, máximo 272, 28% dos pares (aluno, assignment) excedem 50).
- **D-65b (NÃO entra em EDA-02):** threshold binário `correct = (Score == 1.0)` opcional (1 linha), separação Run.Program vs Compile.Error reservada para MODEL-01 (fase 4).
- **D-65c (voz):** "Nosso pré-processamento segue o protocolo de Shi et al. (2022)..." primeira pessoa do plural; citação parentética `(Shi <i>et al.</i>, 2022)`; rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`
- **D-66 (EDA-03 gráfico):** scatter PCA 2D com 3 clusters K-Means coloridos. 1 ponto = 1 aluno; eixos PC1/PC2 das features de cluster (taxa de acerto eventual + tentativas médias + X-Grade). 3 grupos em cores distintas com legenda inline.
- **D-66a (insight central):** "O grupo majoritário (~55%) NÃO é quem erra muito; é quem tenta pouco. Em risco no CSEDM tem alta taxa de acerto eventual e poucas tentativas por assignment." Frase única em destaque (e.g. `.eda-insight` Arial 21-23px).
- **D-66b (geração da figura):** PNG não existe pronto; código PCA em `notebooks/01_eda.ipynb` cell 46 (linha ~2330 do .ipynb raw). Adicionar task de gerar PNG (`results/sec2_perfis_pca.png` sugerido); rodar via `jupyter nbconvert --execute` ou snippet Python standalone. Validar SEED=42.
- **D-66c (números base):** valores do eda_insights.md Seção 3.1 (453 estudantes, 139/66/248). **Atenção:** ver §3 deste RESEARCH — saída atual da cell 46 mostra 239 estudantes, Alto=96/Médio=19/Em risco=124. **gsd-planner re-executa e usa os números atuais.**
- **D-66d (fonte):** `Fonte: análise sobre CSEDM (Spring 2019); K-Means k=3 com SEED=42.` Sem citação Shi (cluster é nosso).
- **D-66e (silhouette + caveat):** silhouette k=3=0,237 (eda_insights.md) ou 0,2564 (cell 46 atual); k=2 é máximo (0,285 ou 0,4801 respectivamente). Escolhemos k=3 pela interpretabilidade do perfil intermediário. **Não** colocar caveat no slide; nota privada para banca.
- **D-67 (MARKER-02 mecânico):** reusa componente `.slide-marker` redesenhado em commit `5d44606`. Diferença vs MARKER-01: apenas modificadores das pills.
- **D-67a (modificadores):** pill 1 done+check, pill 2 done+check, pill 3 running+reload, pill 4 pending+círculo. **Atenção:** ver §5 deste RESEARCH — MARKER-01 HEAD já tem pill 2 em `--running`; o delta vs HEAD é pill 2 → `--done` e pill 3 `--pending` → `--running`.
- **D-67b (badges):** `[done]` abaixo das pills 1 e 2; `[running]` abaixo da pill 3; sem badge na pill 4 (classe `marker-badge--empty` esconde via `visibility: hidden`).
- **D-67c (título e rodapé):** título `> AS QUATRO FASES DA EDM` em Arial bold 24px (classe `.marker-title`); rodapé `Fonte: adaptado de Zorić (2020).` via `.rel-cite` (idênticos ao MARKER-01).
- **D-67d (sem CSS novo):** zero linhas em `theme-unifacens.css`; só `index.html` edita. Validar visualmente que spin do `--running` aplica somente na pill 3.
- **D-68 (cabeçalho):** padrão `> [seção]` único conforme D-01..D-03 fase 1; aplica aos 3 slides EDA. MARKER-02 sem temático (D-34d herdado).
- **D-69 (voz):** paráfrase indireta com autor parentético (D-25 fase 1, D-43 fase 2). Citação direta literal **proibida** nos 4 slides.
- **D-70 (sem em-dash):** sem em-dash em prosa; usar vírgula, dois-pontos ou parênteses. Memória `feedback-no-em-dashes` vinculante.
- **D-71 (fonte):** cada slide novo tem `Fonte:` no rodapé Arial 17-18px cor `#5b6472`.
- **D-72 (itálico):** termos estrangeiros em itálico minúsculas: `<i>knowledge tracing</i>`, `<i>pipeline</i>`, `<i>cluster</i>`, `<i>scatter</i>`, `<i>baseline</i>`. Nomes de modelos preservados (BKT, DKT, Code-DKT). CSEDM/ProgSnap2 como nomes próprios (não itálico). `<i>et al.</i>` ABNT em citação parentética múltipla (D-54 herdado).
- **D-73 (vocabulário herdado fase 2):** "5 assignments com 10 problemas cada" / 6 colunas-chave do ProgSnap2 / ponte KT → trabalho → CSEDM / "tratam respostas como corretas/incorretas, ignorando seu conteúdo" — disponíveis sem redefinir.
- **D-74 (validação visual):** ao fim da fase, validar `#/0` → `#/19` no browser; slide-code antes em `#/11`, agora `#/15`.

### Claude's Discretion

- Ordem de implementação dos 4 slides (sugestão neutra do CONTEXT: MARKER-02 → EDA-02 → EDA-01 → EDA-03; este RESEARCH recomenda a mesma ordem por razões idênticas — ver §7).
- Granularidade dos commits: 1 plan por slide (4 plans) com 1 commit funcional por plan; alinhado com fase 2.
- Microcópia exata dos cabeçalhos `> [seção]`: D-63 deixa em aberto; este RESEARCH propõe 3 variantes por slide com avaliação curta (§4).
- Formato visual exato do scatter PCA: matplotlib + savefig PNG; cores específicas; presença/ausência de eixos numerados; legenda inline vs separada. Default sugerido §6.4: PNG 1200×700, paleta UniFacens-compatível, eixos rotulados PC1/PC2, legenda inferior.
- Tabela A1..A5 do EDA-01: HTML `<table>` puro com classe própria vs layout flex com 5 cards. Este RESEARCH §4 compara 3 templates candidatos e recomenda.
- Atualização do STYLE.md §Inventário ao fim da fase 3: opcional; texto pronto em §8 deste RESEARCH.

### Deferred Ideas (OUT OF SCOPE)

- Discutir microcópia textual dos 3 EDAs antes da execução (planner propõe phrasing; reviewer humano ajusta no checkpoint).
- Threshold binário `correct = (Score == 1.0)` em EDA-02 (default fora; 1 linha extra se houver espaço).
- Separação Run.Program / Compile.Error (reservado para MODEL-01 fase 4).
- Threshold de silhouette ou justificativa de k=3 sobre k=2 em EDA-03 (nota privada se banca perguntar).
- Discutir Release/Train (246) vs MainTable+Shi (410) explicitamente na defesa (resposta disponível para banca).
- Bar chart alternativo ou tabela síntese pura no EDA-03 (descartados em favor de scatter PCA).
- Outros gráficos do `results/` (`sec5_imbalance.png`, etc.) para EDA-03 (descartados; podem inspirar slides de backup).
- Redesenho visual do componente `.slide-marker` (já resolvido em `5d44606`, fora de backlog).

## Phase Requirements

| ID | Description (REQUIREMENTS.md) | Research Support |
|----|-------------------------------|------------------|
| EDA-01 | Slide EDA: distribuição e organização do CSEDM (n estudantes, n problemas, n eventos); mencionar que encontramos a base via Shi; NÃO repetir formato ProgSnap2 | §2 validação numérica (cell 51 do notebook 01 = MainTable Spring 2019); §4 três templates de tabela A1..A5 comparados; §7 phrasing alvo |
| EDA-02 | Slide pré-processamento: aproximação ao protocolo de Shi como `<i>baseline</i>` com ênfase em EDM e análise; apresentar etapas concretas | §1 phrasing literal Shi §4.1/§4.2; §2 verificação 413 → 410 → 328/82 com pandas; §7 phrasing alvo |
| EDA-03 | Slide gráfico com insight sobre estudantes (qual gráfico decidido durante execução, PENDING-02) | §3 K-Means/PCA cell 46 do notebook 01; números atuais (239 alunos) divergem do eda_insights.md (453); §6 geração de PNG; §7 phrasing alvo |
| MARKER-02 | Slide marcador "Preparação dos Dados ✓" após EDA | §5 deltas mecânicos vs MARKER-01 HEAD (4 alterações); zero CSS novo |
| PENDING-02 | Definir qual gráfico de insight de estudantes entra no slide EDA-03 | Resolvido em D-66 (scatter PCA com 3 clusters K-Means); §3 valida disponibilidade no notebook |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Markup dos 4 slides | `apresentacao/index.html` (única fonte) | — | Reveal.js força layout no `<div>` interno; sections novas entram literais entre linhas 243 e 245 |
| Estilização visual | `apresentacao/assets/theme-unifacens.css` | — | Componente `.slide-marker` já existe pronto (linhas 359-453); EDA-* pode receber pequeno acréscimo (`.eda-grid`/`.eda-card`/`.eda-insight`) se template `.slide-related` não bastar |
| Texto travado por requirement | CONTEXT (D-63..D-74) | RESEARCH §7 (phrasing alvo) | Cabeçalhos abertos por design; números travados em D-64a/D-65a/D-66c; phrasing fino fica para o plano com base no RESEARCH |
| Geração de figura | `notebooks/01_eda.ipynb` cell 46 | `scripts/` Python standalone | PCA scatter precisa de execução isolada com SEED=42; PNG salvo em `results/sec2_perfis_pca.png` e copiado para `apresentacao/assets/` |
| Validação visual | Browser (D-74) | — | Sem build system; sem testes automatizados; checkpoint humano fim-a-fim do `#/0` ao `#/19` |

## Project Constraints (from CLAUDE.md)

- **`apresentacao/STYLE.md` vinculante** (slides 1280×720, paleta UniFacens, tipografia Arial + Cascadia para tópicos `>`).
- **Sem em-dash em prosa** (memória `feedback_no_em_dashes` vinculante; D-70).
- **ABNT** seguindo manual MSGQ-21.01 em `apresentacao/`; "tradução nossa" só em direta literal estrangeira.
- **Antes de redigir ou alterar slide que cite autor**, ler a referência completa em `docs/` (vinculante para EDA-02 com Shi 2022; já feito neste RESEARCH §1).
- **Commits atômicos por slide concluído** (CLAUDE.md + CONVENTIONS.md).
- **Voz própria como padrão** (paráfrase indireta com autor parentético).
- **Cabeçalho `> [seção]` com caret piscando** substitui tópico + `<h2>` (único; autor só em `Fonte:`).
- **Iteração ativa GSD** (`.planning/PROJECT.md` + `.planning/REQUIREMENTS.md` + `.planning/STATE.md`); `config.json` define interactive + coarse + commit_docs + research_on + plan_check_on + verifier_off.
- **`feedback_correlatos_antes` revisado (2026-05-27)**: novo padrão de cabeçalho substitui slide dedicado a autor; autor só no rodapé.
- **`reference_manual_citacoes`**: manual Facens em `apresentacao/`; regras de citação direta curta/longa e "tradução nossa".

---

## §1 Phrasing do paper Shi 2022 §4.1 e §4.2 (EDA-02)

`docs/Code-DKT.pdf` páginas 4-5 (PDF), §3 Method + §4 Experiments. Lidas literalmente nesta pesquisa.

### 1.1 Trechos literais que sustentam EDA-02

**§4.1 Dataset & Experiments Setup, p. 5 (col. esquerda):** [CITED: docs/Code-DKT.pdf p. 5]

> "Our study uses a dataset of an introductory Java programming class at a large, university in the US, collected in Spring 2019, stored in the ProgSnap2 format [36]. The dataset includes work from **410 students** on **50 problems** divided over **5 assignments**. These were completed throughout the semester as homework, with each assignment focusing on a specific topic (e.g. conditionals, loops). For these problems, typical solutions ranged 10 to 20 lines of code. Students tended to make multiple submissions before succeeding finally, and **23.68% of the attempts were correct**. Student code was automatically graded using test cases, and We treated a submission as correct (1) **only when all test cases passed**, and incorrect (0) otherwise."

**§4.1, p. 5 (col. esquerda, continuação — sustenta etapas de EDA-02):**

> "For each assignment, students were then split into training and testing sets **with a ratio of 4 : 1**. One quarter of the training data were used for hyperparameter tuning and validation (see below). Then, we trained the model on the whole training dataset, and tested on the holdout test dataset, repeating this process 10 times to account for model variation (e.g. due to random initialization)."

**§4.2 Hyperparameter Tuning & Optimization, p. 5 (col. direita — sustenta truncagem):**

> "We fixed the longest length of student attempts at 50 to filter extra long submission traces from students. In cases where more than 50 attempts were submitted, **we used the last 50 submissions**, assuming that latest submissions were more useful."

**Atenção factual (HIGH):**

- "**410 students**" no paper = nosso resultado verificado (§2.1 deste RESEARCH): 413 brutos → 410 após `min_attempts >= 3`. O paper NÃO descreve literalmente "min_attempts ≥ 3" como o filtro — é inferência do código de referência. Mas o output do filtro coincide com o número exato do paper.
- "**4 : 1**" no paper = 80/20 = nosso resultado verificado (§2.2): 410 → 328 treino + 82 teste com `random_state=1` (de `src/data_loader.py`).
- "**we used the last 50 submissions**" no paper = nossa truncagem em 50 últimas tentativas (D-65a). Phrasing literal disponível para paráfrase em EDA-02.

### 1.2 Phrasing-alvo recomendado para EDA-02 (a polir no plano)

Voz primeira pessoa do plural; paráfrase indireta com `(Shi <i>et al.</i>, 2022)` parentético; `<i>et al.</i>` ABNT (D-54 herdado); rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`

Phrasing-alvo (3 parágrafos curtos ou parágrafo + lista):

> "Nosso pré-processamento segue o protocolo de Shi <i>et al.</i> (2022) como <i>baseline</i> de comparação, com ênfase em análise."

> "Dos 413 alunos brutos do CSEDM, mantivemos 410 com pelo menos 3 tentativas de execução, mesma seleção do paper. Em seguida, dividimos em 328 estudantes para treino e 82 para teste, na proporção 80/20 com semente fixa."

> "Limitamos cada sequência às 50 últimas tentativas. A mediana é de 32 tentativas por aluno e assignment; 28% dos pares ultrapassam 50, com cauda longa até 272."

Variantes equivalentes aceitas pelo CONTEXT D-65c (planner decide):

- "...com pelo menos 3 tentativas de execução" / "...com 3 ou mais execuções no histórico"
- "...dividimos em 328 estudantes para treino e 82 para teste, na proporção 80/20" / "...split 4:1 treino-teste (328/82)" (o paper diz `4:1`; o nosso código usa `test_size=0.2`; equivalentes; preferir "80/20" pela legibilidade em defesa de 20s)

**Gates de redação para EDA-02:**

- [ ] Sem `<blockquote>` (D-69 proíbe direta literal)
- [ ] `<i>baseline</i>` em itálico (D-72; opcional, depende do phrasing)
- [ ] `(Shi <i>et al.</i>, 2022)` parentético; rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`
- [ ] Sem em-dash (D-70)
- [ ] Sem mencionar Release/Train, Compile.Error nem threshold binário (D-65b)
- [ ] Sem mencionar Code-DKT (gate forte, reservado para MODEL-01 fase 4)

---

## §2 Números do dataset — VERIFIED (D-64a + D-65 reconciliação)

### 2.1 MainTable Spring 2019 (Run.Program, 413 alunos brutos)

Comando rodado em 2026-05-28:

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('data/CSEDM/MainTable.csv', low_memory=False)
run = df[df['EventType'] == 'Run.Program'].copy()
for asg, sub in run.groupby('AssignmentID'):
    n_students = sub['SubjectID'].nunique()
    n_problems = sub['ProblemID'].nunique()
    n_attempts = len(sub)
    correct = (sub['Score'] == 1.0).sum()
    print(f'A{asg}: {n_students} students, {n_problems} problems, {n_attempts} attempts, {correct/n_attempts*100:.2f}% correct')
"
```

Output (cruzado com cell 51 do notebook 01_eda.ipynb — coincide perfeitamente):

| Assignment | Estudantes | Problemas | Tentativas | % correto |
|---|---|---|---|---|
| A1 (439) | **386** | 10 | 14.614 | **26,15%** |
| A2 (487) | **340** | 10 | 15.879 | **20,06%** |
| A3 (492) | **361** | 10 | 17.191 | **20,34%** |
| A4 (494) | **315** | 10 | 12.402 | **24,72%** |
| A5 (502) | **306** | 10 | 9.541 | **30,62%** |
| **Global** | **413** | 50 | **69.627** | **23,68%** |

[VERIFIED: pandas em data/CSEDM/MainTable.csv, 2026-05-28]

### 2.2 Pós-filtro Shi `min_attempts ≥ 3` (Run.Program, 410 alunos)

```bash
python3 -c "
import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv('data/CSEDM/MainTable.csv', low_memory=False)
run = df[df['EventType'] == 'Run.Program'].copy()
attempts_per_student = run.groupby('SubjectID').size()
valid_students = sorted(attempts_per_student[attempts_per_student >= 3].index.tolist())
print('Valid students:', len(valid_students))
train_s, test_s = train_test_split(valid_students, test_size=0.2, random_state=1)
print('Train:', len(train_s), 'Test:', len(test_s))
"
```

Output:

```
Valid students: 410
Train: 328 Test: 82
```

[VERIFIED: pandas + sklearn, 2026-05-28]

Diferença per-assignment pós-filtro (3 alunos descartados):

| Assignment | Estudantes pré (413) | Estudantes pós (410) | Δ |
|---|---|---|---|
| A1 (439) | 386 | 384 | -2 |
| A2 (487) | 340 | 340 | 0 |
| A3 (492) | 361 | 360 | -1 |
| A4 (494) | 315 | 315 | 0 |
| A5 (502) | 306 | 306 | 0 |

% correto pós-filtro coincide com % correto pré-filtro até a 2ª casa decimal (os 3 alunos descartados contribuem com poucas tentativas e taxa global mínima). Para EDA-01, **os números pré vs pós Shi são intercambiáveis** dentro da precisão "%" arredondado a uma casa.

### 2.3 Reconciliação D-64a (Release/Train vs MainTable)

eda_insights.md Seção 1.1 reporta (Release/Train = 246 alunos):

| Assignment | Estudantes | % correto (eda_insights) | % correto (MainTable, §2.1) | Δ |
|---|---|---|---|---|
| A1 (439) | 233 | 27,27% | 26,15% | -1,12pp |
| A2 (487) | 224 | 20,32% | 20,06% | -0,26pp |
| A3 (492) | 234 | 19,07% | 20,34% | +1,27pp |
| A4 (494) | 221 | 25,24% | 24,72% | -0,52pp |
| A5 (502) | 222 | 30,40% | 30,62% | +0,22pp |
| **Global** | 246 | 23,70% | 23,68% | -0,02pp |

**Diferenças `< 1,3pp` em todos os assignments** (limite D-64a "se divergirem >5%, regenerar"). Tecnicamente os dois conjuntos de números são intercambiáveis para um slide de 20s; mas há um problema **narrativo**: EDA-02 vai comunicar "413 → 410 → 328/82" (MainTable + protocolo Shi). Se EDA-01 mostrar 233/224/234/221/222 estudantes (Release/Train), o ouvinte estranha porque 233+224+234+221+222 ≠ 413 nem 410 (são estudantes em assignments diferentes, com sobreposição). Os números de MainTable (386/340/361/315/306) somam 1.708 mas representam "estudantes que tentaram aquele assignment", que pode ser entendido — coerente com `n_students` por assignment do paper, que também reporta valores diferentes por assignment (vide Shi §4.1 implícito).

**Recomendação (HIGH confidence):** Usar os números **MainTable Spring 2019** (§2.1) em EDA-01:

| Assignment | Estudantes | Problemas | Taxa de acerto |
|---|---|---|---|
| A1 (439) | 386 | 10 | 26,15% |
| A2 (487) | 340 | 10 | 20,06% |
| A3 (492) | 361 | 10 | 20,34% |
| A4 (494) | 315 | 10 | 24,72% |
| A5 (502) | 306 | 10 | 30,62% |

Razões:
1. **Coerência com EDA-02:** EDA-02 narra o caminho 413 → 410 → 328/82. EDA-01 mostra a base de partida (413 alunos Spring 2019) com granularidade por assignment. Usar Release/Train fragmentaria a narrativa.
2. **Coerência com INTRO-01:** INTRO-01 já cita "413 estudantes, 5 assignments com 10 problemas cada, 201 mil eventos" (Spring 2019 bruto). EDA-01 expande dentro da mesma base.
3. **Reprodutibilidade do paper:** cell 51 do notebook 01 reporta exatamente `% correto global (Release/Train): 23.68%` (a label "Release/Train" no print é misleading — a leitura é de MainTable.csv inteira). Match perfeito com o paper.
4. **Risco baixo:** se reviewer da banca perguntar "por que A3 tem 361 estudantes?", a resposta é "estudantes que tentaram A3 ao menos uma vez no Spring 2019". Defensável.

**Formato no slide (D-64b "enxuto"):** preferir tabela compacta `<table>` em vez de 5 cards horizontais (1280px / 5 cards = ~256px por card, cabe mas fica visualmente pesado quando comparado a `<table>` de 5 linhas × 4 colunas). Ver §4 deste RESEARCH para comparação de templates.

### 2.4 Phrasing-alvo recomendado para EDA-01 (a polir no plano)

Parágrafo abertura (2-3 linhas, voz primeira pessoa do plural):

> "Encontramos a base via Shi <i>et al.</i> (2022). Ao navegar o CSEDM, vimos que os 5 assignments cobrem dificuldades muito diferentes: a taxa de acerto cai de 26% no primeiro para 20% no terceiro, e sobe para 30% no último."

Logo abaixo, tabela `<table>` com cabeçalho:

| Assignment | Alunos | Problemas | Taxa de acerto |
|---|---|---|---|
| A1 (439) | 386 | 10 | 26,15% |
| A2 (487) | 340 | 10 | 20,06% |
| A3 (492) | 361 | 10 | 20,34% |
| A4 (494) | 315 | 10 | 24,72% |
| A5 (502) | 306 | 10 | 30,62% |

Rodapé: `Fonte: análise sobre CSEDM (Spring 2019).`

Variantes do parágrafo abertura (planner escolhe no checkpoint visual):

- (A) **acadêmica**: "Encontramos a base via Shi <i>et al.</i> (2022). Ao navegar o CSEDM, vimos que os 5 assignments cobrem dificuldades muito diferentes..."
- (B) **direta**: "Vamos pelo dataset por dentro. A taxa de acerto varia de 20% (A3) a 30% (A5); cada assignment tem 10 problemas e 300-390 alunos."
- (C) **narrativa**: "Conhecemos o CSEDM via Shi <i>et al.</i> (2022). A primeira inspeção por assignment mostra heterogeneidade: o terceiro (A492) tem só 20% de acerto; o último (A502) sobe para 30%."

**Recomendação:** (A) por coerência com o tom INTRO-03a/03b (autor prominente quando o autor é o gancho) + 2ª frase trazendo o achado quantitativo. (B) é mais punchy mas perde o gancho "via Shi"; (C) é equivalente a (A) com pequenas variações.

**Gates de redação para EDA-01:**

- [ ] Sem `<blockquote>` (D-69 proíbe direta literal)
- [ ] Sem em-dash (D-70)
- [ ] NÃO repetir 413/50/201 mil (D-64c gate forte)
- [ ] NÃO repetir "ProgSnap2" no corpo (Key Decision PROJECT.md; nominalmente único em INTRO-01)
- [ ] `(Shi <i>et al.</i>, 2022)` parentético no corpo; rodapé `Fonte: análise sobre CSEDM (Spring 2019).` (sem citação Shi no rodapé porque a contagem é nossa)
- [ ] Tabela com `% correto` formatado pt-BR (vírgula decimal, ex.: `26,15%`)

---

## §3 K-Means / PCA para EDA-03 — números atuais do notebook (D-66c reconciliação)

### 3.1 Estado atual da cell 46 do notebook 01_eda.ipynb

`notebooks/01_eda.ipynb` cell 44 (setup features) + cell 45 (silhouette) + cell 46 (K-Means + nomeação + PCA scatter). Lidos em 2026-05-28 com outputs preservados.

**Cell 44 output (stream):**

```
Estudantes com features completas: 239 / 413
Features: ['A439.0_rate', 'A487.0_rate', 'A492.0_rate', 'A494.0_rate', 'A502.0_rate',
           'A439.0_att', 'A487.0_att', 'A492.0_att', 'A494.0_att', 'A502.0_att', 'X-Grade']
```

**Cell 45 output (silhouette):**

```
Silhouette Score por k: {2: 0.4801, 3: 0.2564, 4: 0.2447, 5: 0.232, 6: 0.2274}
Melhor k pelo Silhouette: 2  |  Score (k=3): 0.2564
```

**Cell 46 output (resumo por perfil):**

```
                   N  X-Grade  A439.0_rate  A487.0_rate  ...  A439.0_att  A487.0_att  A492.0_att  ...
Alto desempenho   96     0.80         0.98         0.94  ...         3.7         7.1         8.6
Em risco         124     0.60         0.99         0.96  ...
Médio             19     0.65         0.65         0.53  ...
```

### 3.2 Reconciliação D-66c (eda_insights.md vs cell 46 atual)

| Métrica | eda_insights.md Seção 3.1 | cell 46 atual (2026-05-28) | Δ |
|---|---|---|---|
| Estudantes com features | 453 | **239** | -214 |
| N Alto desempenho | 139 (30,7%) | **96 (40,2%)** | -43 |
| N Médio | 66 (14,6%) | **19 (7,9%)** | -47 |
| N Em risco | 248 (54,7%) | **124 (51,9%)** | -124 |
| X-Grade Alto | 73,8 | **0,80 (normalizado 0-1)** | reformatado |
| Silhouette k=2 | 0,285 | **0,4801** | +0,195 |
| Silhouette k=3 | 0,237 | **0,2564** | +0,019 |

**Análise da divergência:**
- `eda_insights.md` (versão consolidada após EDA-FASE-1) usou **Release/Train** (246 alunos) como base de cluster_features; cell 46 atual usa `all_labels = early.csv + late.csv` (CSEDM Data Challenge 2021) interceptado com `Subject.csv` (X-Grade) — output sai a 239 alunos por causa do `.dropna()` que descarta alunos sem feature completa em **todos** os 5 assignments.
- X-Grade no eda_insights.md vem como 0-100 (`73,8`); na cell 46 atual vem como 0-1 (`0,80`) — `Subject.csv` carrega X-Grade já normalizado entre 0 e 1.
- Em risco no cell 46 atual = **51,9%** (124/239) — coerente com D-66a "grupo majoritário (~55%)". O insight central NÃO muda; só os números absolutos.

**Recomendação (HIGH confidence):** **Re-executar a cell 46 antes de gravar números no slide** e usar os outputs atuais (239 alunos, Alto=96, Médio=19, Em risco=124, silhouette k=3=0,2564). Razões:

1. **Reprodutibilidade defensável:** os números atuais são os que rodam HOJE com SEED=42. Se a banca tentar reproduzir, vê esses números.
2. **Insight preservado:** "majoritário (~55%) é quem tenta pouco" continua válido (124/239 = 51,9% arredonda para 52%; pode-se dizer "~52%" ou "mais da metade").
3. **D-66a preserva phrasing:** "O grupo majoritário (~55%) NÃO é quem erra muito; é quem tenta pouco." — usar `(~52%)` se o número for exato; `(mais da metade)` se quiser arredondar.

**Riscos:**
- eda_insights.md está OBSOLETO em §3.1 para esta análise; a memória `project_split_discovery` registra a migração Release/ → MainTable. O notebook foi re-executado após essa migração, mas o eda_insights.md não foi reescrito. **Não bloqueia esta fase**, mas é um item de dívida documental para depois da defesa.
- A frase "(~55%)" do CONTEXT D-66a poderia ficar `(~52%)` com os números atuais. Discretion do planner se mantém "~55%" como aproximação amigável (fica dentro do erro de leitura visual) ou ajusta para `(~52%)`. Recomendo manter "~55%" para alinhar com CONTEXT e com o phrasing original; é leitura visual genérica do scatter.

### 3.3 Phrasing-alvo recomendado para EDA-03 (a polir no plano)

Layout sugerido: cabeçalho `> [perfis dos alunos]` + scatter PCA centralizado (60-70% da altura) + insight em destaque abaixo + rodapé.

Insight em destaque (`.eda-insight` ou similar, Arial 22-24px, possivelmente em `<b>` ou cor `--uni-blue`):

> "O grupo majoritário não é quem erra muito; é quem tenta pouco."

Subtítulo (sentença explicativa, mais discreto):

> "Em risco no CSEDM tem alta taxa de acerto eventual mas poucas tentativas por <i>assignment</i> (2 a 4)."

Variantes equivalentes (CONTEXT D-66a aceita):

- "O grupo em risco é maioritário e tenta pouco, não erra muito."
- "Maioria (~55%) acerta quando tenta. O risco é o desengajamento."

Rodapé (D-66d literal):

```html
<p class="rel-cite">Fonte: análise sobre CSEDM (Spring 2019); <i>K-Means</i> k=3 com SEED=42.</p>
```

**Gates de redação para EDA-03:**

- [ ] Sem `<blockquote>` (D-69)
- [ ] Sem em-dash (D-70)
- [ ] `<i>cluster</i>`, `<i>scatter</i>`, `<i>K-Means</i>`, `<i>assignment</i>` em itálico minúsculas (D-72)
- [ ] Sem citação Shi nem Code-DKT (cluster é nosso, gate forte)
- [ ] Insight em uma frase (não 2 nem 3); voz própria neutra (sem "vemos que..." que enfraquece)

---

## §4 Templates candidatos para EDA-01 (tabela A1..A5)

### 4.1 Template A — `.bridge-seq` com `.step` + `.arr` (cards horizontais)

Reuso direto do componente do slide Yağcı (linhas 197-210 do CSS). Cinco `.step` com 1 `.arr` entre cada par (4 setas total).

**Markup:**

```html
<p class="bridge-seq">
  <span class="step">
    <b>A1 (439)</b><br>386 alunos · 10 prob.<br>26,15% acerto
  </span>
  <span class="arr">&rarr;</span>
  <span class="step">
    <b>A2 (487)</b><br>340 alunos · 10 prob.<br>20,06% acerto
  </span>
  <span class="arr">&rarr;</span>
  ...
</p>
```

**Prós:**
- Zero CSS novo (reusa `.bridge-seq` já testado em Yağcí).
- Visualmente carrega o gancho "sequência cronológica dos 5 assignments do semestre" (setas comunicam progressão temporal).

**Contras:**
- 5 cards × 3 linhas de texto cada = ~270 caracteres em 1280px de largura útil. A 19px Arial bold (D-72 padrão `.step`), os cards de 256px ficam apertados (sobretudo "A492 (492)" + "20,34% acerto").
- 4 setas `→` em uma linha de tabela quebram a leitura "linha-coluna" natural (a tabela tradicional é mais legível para comparar % entre linhas).
- Sequência horizontal sugere narrativa cronológica; uma tabela é mais neutra "estes são os 5 assignments, comparem".

**Veredito:** aceitável, mas não recomendado.

### 4.2 Template B — `<table>` ABNT (vertical, 5 linhas × 4 colunas)

Tabela HTML simples, estilizada com borda fina preta (estética ABNT já usada em `.kc-box` e `.bridge-seq .step`).

**Markup:**

```html
<table class="eda-grid">
  <thead>
    <tr><th>Assignment</th><th>Alunos</th><th>Problemas</th><th>Taxa de acerto</th></tr>
  </thead>
  <tbody>
    <tr><td>A1 (439)</td><td>386</td><td>10</td><td>26,15%</td></tr>
    <tr><td>A2 (487)</td><td>340</td><td>10</td><td>20,06%</td></tr>
    <tr><td>A3 (492)</td><td>361</td><td>10</td><td>20,34%</td></tr>
    <tr><td>A4 (494)</td><td>315</td><td>10</td><td>24,72%</td></tr>
    <tr><td>A5 (502)</td><td>306</td><td>10</td><td>30,62%</td></tr>
  </tbody>
</table>
```

**CSS sugerido (a adicionar em `theme-unifacens.css`):**

```css
.eda-grid {
  width: 92%; margin: 32px auto 0;
  border-collapse: collapse;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 21px;
}
.eda-grid th, .eda-grid td {
  border: 1.5px solid #1f1f1f;
  padding: 12px 18px;
  text-align: center;
}
.eda-grid th {
  background: #fff; font-weight: 700; color: var(--uni-ink);
}
.eda-grid td { background: #fff; color: var(--uni-ink); }
.eda-grid tr td:first-child { text-align: left; font-weight: 700; }
.eda-grid tr td:last-child { color: var(--uni-blue); font-weight: 700; }
```

**Prós:**
- Estética ABNT (bordas finas, sem `border-radius`, fundo branco) coerente com `.bridge-seq` / `.kc-box` / `.marker-pill`.
- Leitura linha-coluna natural; comparação intra-coluna fácil (qual assignment tem mais alunos? qual tem maior acerto?).
- Layout robusto em 1280×720 (5 linhas × ~50px altura = 250px; cabe bem entre cabeçalho e rodapé).
- Última coluna em `--uni-blue` destaca o achado (taxa de acerto) sem ruído.

**Contras:**
- Adiciona ~14 linhas de CSS novo em `theme-unifacens.css` (não é trivial, mas é parametrizável e reusável).
- Tabela em apresentações tende a ser densa; legibilidade depende de tamanho de fonte adequado (21px sugerido).

**Veredito:** **recomendado** (HIGH confidence). É o template mais coerente com a estética ABNT do deck e com o uso comparativo dos números.

### 4.3 Template C — cards horizontais com `.eda-card` (5 cards estilizados)

5 `<div class="eda-card">` em flexbox, cada um com `<h3>` (assignment), `<p>` (alunos), `<p>` (problemas), `<p>` (% acerto). Mesma estrutura do `.bkt-group` (linhas 247-265 do CSS).

**Markup:**

```html
<div class="eda-cards">
  <div class="eda-card">
    <h3 class="eda-card__name">A1 (439)</h3>
    <p class="eda-card__row"><span>alunos</span><b>386</b></p>
    <p class="eda-card__row"><span>problemas</span><b>10</b></p>
    <p class="eda-card__row eda-card__hl"><span>acerto</span><b>26,15%</b></p>
  </div>
  ...
</div>
```

**Prós:**
- Visualmente "moderno"; cada card vira um chunk independente.
- Última linha em destaque (`.eda-card__hl`) ressalta o achado.

**Contras:**
- 5 cards horizontais a 1280px-128px(padding) = 1152px / 5 = 230px por card. Comporta mas fica densinho.
- Adiciona ~30 linhas de CSS novo (mais que template B).
- Menos legível como **comparação** entre assignments (visão por card, não por coluna).
- Risco de visualmente competir com EDA-03 (que tem layout mais "figura-única").

**Veredito:** descartado (sobre-engenharia para o caso simples de 5 linhas × 4 colunas).

### 4.4 Resumo

| Template | CSS novo | Legibilidade 1280×720 | Coerência ABNT | Esforço de plano |
|---|---|---|---|---|
| A (`.bridge-seq`) | 0 linhas | apertado | alta | mínimo |
| **B (`<table>`)** | **~14 linhas** | **boa** | **alta** | **baixo** |
| C (`.eda-card`) | ~30 linhas | apertada | média | médio |

**Recomendação final:** **Template B (`<table>` ABNT)** com CSS novo `.eda-grid` em `theme-unifacens.css`. Reviewer pode pedir ajuste de cor/fonte/largura no checkpoint visual; iteração textual é esperada (padrão fase 2).

---

## §5 MARKER-02 — reuso mecânico (D-67 deltas vs MARKER-01 HEAD)

### 5.1 Estado do MARKER-01 em HEAD (linhas 200-243 do index.html)

Lido literalmente em 2026-05-28:

| Pill | Modificador | Ícone | Badge |
|---|---|---|---|
| 1 | `marker-pill--done` | `&check;` | `<span class="marker-badge">[done]</span>` |
| 2 | `marker-pill--running` | `&#x21BB;` (reload) | `<span class="marker-badge">[running]</span>` |
| 3 | `marker-pill--pending` | `&#x25CB;` (círculo) | `<span class="marker-badge marker-badge--empty">[]</span>` |
| 4 | `marker-pill--pending` | `&#x25CB;` | `<span class="marker-badge marker-badge--empty">[]</span>` |

⚠️ **Importante:** O CONTEXT D-67a descreve o efeito conceitual de MARKER-02 (pills 1+2 done, pill 3 running, pill 4 pending), mas pressupõe MARKER-01 com pill 2 em `--pending`. **Não é o caso em HEAD.** MARKER-01 (commit `5d44606`) já tem pill 2 em `--running` (o deck "vivo" comunica "Fase 1 concluída, Fase 2 em andamento" — semanticamente correto para a hora em que MARKER-01 aparece na narrativa). MARKER-02 é o slide que aparece DEPOIS da Fase 2 concluída.

### 5.2 Deltas literais MARKER-01 HEAD → MARKER-02 (4 alterações)

| # | Linha (offset relativo) | De | Para |
|---|---|---|---|
| 1 | Linha 202 do `<div class="deck-slide ...">` | `slide-marker slide-marker--phase1` | `slide-marker slide-marker--phase2` |
| 2 | Linhas 217-221 (pill 2) | `marker-pill--running` + `&#x21BB;` + `<span class="marker-badge">[running]</span>` | `marker-pill--done` + `&check;` + `<span class="marker-badge">[done]</span>` |
| 3 | Linhas 224-229 (pill 3) | `marker-pill--pending` + `&#x25CB;` + `<span class="marker-badge marker-badge--empty">[]</span>` | `marker-pill--running` + `&#x21BB;` + `<span class="marker-badge">[running]</span>` |
| 4 | Comentário linha 200 | `MARKER · As quatro fases da EDM, fase 1 concluida (Zoric, 2020)` | `MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020)` |

Pill 1 (Definição) e pill 4 (Implantação) **não mudam**.

### 5.3 Markup-alvo completo do MARKER-02 (copiar e colar, ajustar 4 deltas)

```html
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase2">
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
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Preparação dos Dados</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--running">
          <span class="marker-pill-icon">&#x21BB;</span>
          <span class="marker-pill-name">Modelagem e Avaliação</span>
        </div>
        <span class="marker-badge">[running]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--pending">
          <span class="marker-pill-icon">&#x25CB;</span>
          <span class="marker-pill-name">Implantação</span>
        </div>
        <span class="marker-badge marker-badge--empty">[]</span>
      </div>
    </div>

    <p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

### 5.4 Verificação CSS — spin animation aplica somente na pill 3

`theme-unifacens.css` linhas 419-423:

```css
.marker-pill--running .marker-pill-icon {
  color: var(--uni-blue);
  border: 1.5px solid var(--uni-blue);
  animation: marker-spin 2.4s linear infinite;
}
```

A regra é específica do `.marker-pill--running` interno. Como apenas a pill 3 do MARKER-02 carrega esse modificador, **a animação spin gira só na pill 3**. Pill 2 (com `--done`) e demais ficam estáticas. [VERIFIED: leitura literal do CSS]

### 5.5 Gates de validação MARKER-02

- [ ] `grep -c 'slide-marker--phase2' apresentacao/index.html` retorna 1
- [ ] `grep -c 'slide-marker--phase1' apresentacao/index.html` retorna 1 (MARKER-01 inalterado)
- [ ] No browser `#/14` (MARKER-02 após inserção): pill 1 e pill 2 em fundo branco com check azul; pill 3 com ícone reload girando suavemente; pill 4 com círculo cinza estático
- [ ] Badges `[done] [done] [running]` na linha abaixo das pills 1-3; pill 4 sem badge visível
- [ ] Rodapé `Fonte: adaptado de Zorić (2020).` centralizado (heredado do `.slide-marker .rel-cite { margin-top: 0; ...}` do CSS)
- [ ] Marca d'água Facens presente (top-right)
- [ ] Zero linhas adicionadas em `theme-unifacens.css` (D-67d)

---

## §6 Geração do PNG do scatter PCA (D-66b)

### 6.1 Estado atual

- PNG NÃO existe pronto em `results/` (verificado: `ls results/ | grep -iE 'pca|perfis|cluster|sec2'` → só `sec3_correct_rate_by_problem.png`).
- Código existe em `notebooks/01_eda.ipynb` cell 46 (linhas ~2330 do .ipynb raw).
- Cell 46 atual gera `fig, axes = plt.subplots(1, 2, figsize=(13, 5))` com (PCA scatter, heatmap centróides). Para o slide, queremos **só o scatter**.

### 6.2 Opção A — `jupyter nbconvert --execute`

```bash
cd notebooks
jupyter nbconvert --to notebook --execute 01_eda.ipynb --output 01_eda_executed.ipynb
# Em seguida, abrir 01_eda_executed.ipynb e exportar a célula 46 figura manualmente
```

**Prós:** Reusa código existente sem modificação.
**Contras:** Executa o notebook inteiro (~10-20 min com K-Means + PCA + outras células); gera fig combinada (scatter + heatmap) que precisa ser cortada; extração manual da fig é frágil.
**Veredito:** descartado (overkill).

### 6.3 Opção B — Snippet Python standalone (recomendado)

Criar `scripts/build_eda_pca_scatter.py` (one-shot, segue convenção `scripts/<verbo>_<objeto>.py` de CONVENTIONS.md):

```python
"""Gera scatter PCA 2D dos 3 perfis K-Means para o slide EDA-03 (fase 3 GSD)."""
from pathlib import Path
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "CSEDM"
RESULTS = ROOT / "results"
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

# 1. Carregar early.csv + late.csv + Subject.csv (mesma estratégia da cell 35-44 do notebook)
early = pd.read_csv(ROOT / "data" / "early.csv")
late = pd.read_csv(ROOT / "data" / "late.csv")
all_labels = pd.concat([early, late], ignore_index=True)
subject = pd.read_csv(DATA_ROOT / "LinkTables" / "Subject.csv")

# 2. Construir features de cluster (mesma estrutura da cell 44)
correct_rate = (
    all_labels.groupby(["SubjectID", "AssignmentID"])["CorrectEventually"]
    .mean()
    .reset_index()
    .pivot(index="SubjectID", columns="AssignmentID", values="CorrectEventually")
)
correct_rate.columns = [f"A{c}_rate" for c in correct_rate.columns]

avg_att = (
    all_labels.groupby(["SubjectID", "AssignmentID"])["Attempts"]
    .mean()
    .reset_index()
    .pivot(index="SubjectID", columns="AssignmentID", values="Attempts")
)
avg_att.columns = [f"A{c}_att" for c in avg_att.columns]

cluster_features = (
    correct_rate
    .join(avg_att)
    .join(subject.set_index("SubjectID")["X-Grade"])
    .dropna()
)

X_scaled = StandardScaler().fit_transform(cluster_features.values)

# 3. K-Means k=3 e nomeação por X-Grade
km = KMeans(n_clusters=3, random_state=SEED, n_init=10)
cluster_features = cluster_features.copy()
cluster_features["cluster"] = km.fit_predict(X_scaled)

grade_by_cluster = cluster_features.groupby("cluster")["X-Grade"].mean().sort_values(ascending=False)
cluster_labels = {c: lbl for c, lbl in zip(grade_by_cluster.index,
                                            ["Alto desempenho", "Médio", "Em risco"])}
cluster_features["perfil"] = cluster_features["cluster"].map(cluster_labels)

# 4. PCA 2D e scatter
coords = PCA(n_components=2, random_state=SEED).fit_transform(X_scaled)

# Paleta UniFacens-friendly (azul / amarelo / vermelho coerente com a paleta do deck)
palette = {
    "Alto desempenho": "#2667FF",  # uni-blue
    "Médio":           "#F2A516",  # âmbar
    "Em risco":        "#D7191C",  # vermelho
}

fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
for perfil, color in palette.items():
    mask = cluster_features["perfil"].values == perfil
    n = int(mask.sum())
    ax.scatter(coords[mask, 0], coords[mask, 1],
               c=color, label=f"{perfil} (n={n})",
               s=70, alpha=0.78, edgecolors="white", linewidths=0.7)

ax.set_xlabel("PC1", fontsize=14)
ax.set_ylabel("PC2", fontsize=14)
ax.legend(loc="lower left", fontsize=13, frameon=True, framealpha=0.95, edgecolor="#1f1f1f")
ax.grid(True, alpha=0.18)
ax.set_axisbelow(True)
plt.tight_layout()

output = RESULTS / "sec2_perfis_pca.png"
plt.savefig(output, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved: {output}")

# Resumo numérico para conferência cruzada com o slide
print()
print("=== Resumo por perfil (alimenta texto do slide EDA-03) ===")
print(cluster_features.groupby("perfil")[["X-Grade"]].agg(["count", "mean"]))
```

**Prós:**
- Reprodutível (SEED=42 no script + no KMeans + no PCA).
- Gera só o que precisamos (scatter); não toca em outras células.
- Segue convenção `scripts/<verbo>_<objeto>.py` de CONVENTIONS.md.
- Imprime resumo numérico (n por perfil) que alimenta o texto do slide — útil para validar o "~55%" do D-66a.

**Contras:** Adiciona um script novo ao repo. Mas é one-shot reutilizável; se a defesa pedir re-geração com cores diferentes, é só editar a `palette`.

**Veredito:** **recomendado** (HIGH confidence).

### 6.4 Comando de execução e validação

```bash
# Gerar
python3 scripts/build_eda_pca_scatter.py

# Output esperado:
#   Saved: /home/leokuntz/.../results/sec2_perfis_pca.png
#
#   === Resumo por perfil ===
#                          count      mean
#   perfil
#   Alto desempenho           96  0.80...
#   Em risco                 124  0.60...
#   Médio                     19  0.65...

# Copiar para apresentacao/assets/ (conforme STRUCTURE.md "Slide novo na apresentação":
# não referenciar results/ diretamente, copiar)
cp results/sec2_perfis_pca.png apresentacao/assets/eda-perfis-pca.png
```

Validar PNG visualmente:
- Dimensões: ~1200×700 (figsize 12×7 × dpi 120 = 1440×840 com `bbox_inches='tight'` aplica crop final)
- 3 grupos coloridos (azul, âmbar, vermelho); cardinalidade aproximada Alto≈96, Médio≈19, Em risco≈124
- Legenda inferior-esquerda com `(n=...)` em cada label
- Eixos PC1/PC2 rotulados; grid suave em alpha 0.18
- Fundo branco (slide é `#F1F6FB`; PNG branco com `bbox_inches='tight'` fica natural com margem)

### 6.5 Markup-alvo no slide EDA-03

```html
<figure class="eda-fig">
  <img src="assets/eda-perfis-pca.png" alt="Scatter PCA 2D dos 3 perfis de alunos (Alto desempenho, Médio, Em risco)">
</figure>
```

CSS sugerido (a adicionar em `theme-unifacens.css` se não usar template `.slide-fig` existente):

```css
.eda-fig {
  margin: 16px auto 0; max-width: 78%;
  display: flex; justify-content: center;
}
.eda-fig img { width: 100%; height: auto; max-height: 460px; object-fit: contain; }

.eda-insight {
  margin: 20px auto 0; max-width: 92%; text-align: center;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 23px; font-weight: 700; color: var(--uni-ink);
  line-height: 1.35;
}
.eda-insight em, .eda-insight i { font-style: italic; font-weight: 700; }
```

Alternativa: reusar `.slide-fig` (template existente para slide-fig "evolução por dificuldade"), mas há discrepância porque EDA-03 leva também a frase de insight em destaque — `.slide-fig` não tem `.eda-insight`. Decisão de plano: criar 2 classes pequenas (`.eda-fig` + `.eda-insight`) é mais limpo.

---

## §7 Phrasing alvo consolidado para os 3 slides EDA

### 7.1 EDA-01 (cabeçalho + corpo)

**Cabeçalho — 3 variantes (planner escolhe; D-63a aberto):**

| Variante | Texto | Avaliação |
|---|---|---|
| (a) `> como navegamos o csedm` | tom narrativo, casa com "ao navegar..." | **Recomendado**: literal ao roteiro do CONTEXT D-64; verbo "navegar" comunica EDA exploratória |
| (b) `> o curso por dentro` | tom ensaístico, casa com "curso introdutório Java" | Discutível: "por dentro" é mais coloquial; perde-se o gancho EDA |
| (c) `> os 5 assignments` | descritivo direto | Perde poder narrativo; só anuncia que vamos listar |

**Corpo recomendado (a polir):**

```html
<p class="rel-lead">
  Encontramos a base via Shi <i>et al.</i> (2022). Ao navegar o CSEDM,
  os 5 <i>assignments</i> cobrem dificuldades muito diferentes: a taxa
  de acerto cai de 26% no primeiro para 20% no terceiro, e sobe para
  30% no último.
</p>

<table class="eda-grid">
  <thead>
    <tr><th>Assignment</th><th>Alunos</th><th>Problemas</th><th>Taxa de acerto</th></tr>
  </thead>
  <tbody>
    <tr><td>A1 (439)</td><td>386</td><td>10</td><td>26,15%</td></tr>
    <tr><td>A2 (487)</td><td>340</td><td>10</td><td>20,06%</td></tr>
    <tr><td>A3 (492)</td><td>361</td><td>10</td><td>20,34%</td></tr>
    <tr><td>A4 (494)</td><td>315</td><td>10</td><td>24,72%</td></tr>
    <tr><td>A5 (502)</td><td>306</td><td>10</td><td>30,62%</td></tr>
  </tbody>
</table>

<p class="rel-cite">Fonte: análise sobre CSEDM (Spring 2019).</p>
```

### 7.2 EDA-02 (cabeçalho + corpo)

**Cabeçalho — 3 variantes (planner escolhe; D-63b aberto):**

| Variante | Texto | Avaliação |
|---|---|---|
| (a) `> pré-processamento` | descritivo neutro | Bom: simples, direto, casa com o tom acadêmico do paper Shi |
| (b) `> aproximação ao protocolo` | enfatiza método | **Recomendado**: comunica "seguimos Shi por design" e dialoga com a 1ª frase do corpo |
| (c) `> do bruto ao split` | enfatiza pipeline | Bom: poético; comunica os 3 momentos (413, 410, 328/82); risco de soar over-clever |

**Corpo recomendado (a polir):**

```html
<p class="rel-lead">
  Nosso pré-processamento segue o protocolo de Shi <i>et al.</i> (2022)
  como <i>baseline</i> de comparação, com ênfase em análise.
</p>

<p class="rel-lead">
  Dos 413 alunos brutos do CSEDM, mantivemos <b>410</b> com pelo menos
  3 tentativas de execução, mesma seleção do paper. Em seguida,
  dividimos em <b>328 estudantes para treino e 82 para teste</b>, na
  proporção 80/20 com semente fixa.
</p>

<p class="rel-lead">
  Limitamos cada sequência às <b>50 últimas tentativas</b>. A mediana
  é 32 tentativas por aluno e <i>assignment</i>; 28% dos pares ultrapassam
  50, com cauda longa até 272.
</p>

<p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
```

Alternativa "etapas numeradas" se o reviewer pedir lista visual (ver §4 — `<ol>` ABNT pode caber, mas `.rel-lead` repetidos casam melhor com o tom dos outros slides INTRO/EDA):

```html
<p class="rel-lead">Nosso pré-processamento segue o protocolo de Shi <i>et al.</i> (2022)...</p>
<ol class="eda-steps">
  <li>Filtramos alunos com pelo menos 3 tentativas: <b>413 → 410</b>.</li>
  <li>Dividimos 80/20: <b>328 treino · 82 teste</b>.</li>
  <li>Truncamos cada sequência em <b>50 últimas tentativas</b>.</li>
</ol>
```

CSS para `.eda-steps` (se for adotada):

```css
.eda-steps {
  list-style: none; counter-reset: step;
  margin: 14px 0 0; padding: 0 0 0 6px;
  font-family: Arial, "Helvetica Neue", sans-serif; font-size: 22px;
  line-height: 1.55; color: var(--uni-ink);
}
.eda-steps li { counter-increment: step; padding-left: 42px; position: relative; margin-bottom: 10px; }
.eda-steps li::before {
  content: counter(step); position: absolute; left: 0; top: 2px;
  width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center;
  border: 1.5px solid var(--uni-blue); color: var(--uni-blue);
  font-family: var(--mono); font-weight: 700; font-size: 16px;
}
```

**Veredito (templates EDA-02):** começar com **3 × `.rel-lead`** (mínimo overhead; padrão das fases anteriores). Se o reviewer no checkpoint pedir mais estrutura visual, migrar para `.eda-steps`.

### 7.3 EDA-03 (cabeçalho + corpo)

**Cabeçalho — 3 variantes (planner escolhe; D-63c aberto):**

| Variante | Texto | Avaliação |
|---|---|---|
| (a) `> perfis dos alunos` | descritivo direto | Bom: casa com "Em risco / Médio / Alto desempenho" |
| (b) `> três jeitos de aprender` | tom narrativo | **Recomendado**: comunica o insight pedagógico antes mesmo do scatter; "jeitos de aprender" é a leitura humana dos perfis |
| (c) `> quem tenta, quem desiste` | enfatiza o insight central | Bom: punchy; risco de redundância com a frase de insight em destaque abaixo |

**Corpo recomendado (a polir):**

```html
<figure class="eda-fig">
  <img src="assets/eda-perfis-pca.png" alt="Scatter PCA 2D dos 3 perfis de alunos">
</figure>

<p class="eda-insight">
  O grupo majoritário não é quem erra muito; é quem tenta pouco.
</p>

<p class="rel-lead eda-subinsight">
  Em risco no CSEDM tem alta taxa de acerto eventual mas poucas
  tentativas por <i>assignment</i> (2 a 4).
</p>

<p class="rel-cite">
  Fonte: análise sobre CSEDM (Spring 2019);
  <i>K-Means</i> k=3 com SEED=42.
</p>
```

CSS sugerido para `.eda-subinsight` (se mantido):

```css
.eda-subinsight {
  margin-top: 10px; font-size: 19px; color: #5b6472; text-align: center;
  font-weight: 400;
}
```

Alternativa visual: omitir `.eda-subinsight` (sub-explicação) e deixar só o insight central + scatter. Reviewer decide no checkpoint.

### 7.4 Sumário de phrasing-alvo

| Slide | Cabeçalho recomendado | Tom | Citação parentética | Rodapé "Fonte:" |
|---|---|---|---|---|
| EDA-01 | `> como navegamos o csedm` | autoral, autor prominente | `(Shi <i>et al.</i>, 2022)` | `Fonte: análise sobre CSEDM (Spring 2019).` |
| EDA-02 | `> aproximação ao protocolo` | autoral, paráfrase indireta com `<i>et al.</i>` | `(Shi <i>et al.</i>, 2022)` | `Fonte: adaptado de Shi <i>et al.</i> (2022).` |
| EDA-03 | `> três jeitos de aprender` | autoral, sem citação Shi no corpo | — | `Fonte: análise sobre CSEDM (Spring 2019); <i>K-Means</i> k=3 com SEED=42.` |
| MARKER-02 | (sem `.deck-topic`) | (sem corpo textual além das pills) | — | `Fonte: adaptado de Zorić (2020).` |

---

## §8 STYLE.md — diff sugerido (não obrigatório, ver D-61)

D-61 diz que a frase em `apresentacao/STYLE.md` §"Gaps reservados" linha 130 já está consistente com esta fase (post-fase 2 `f4dde9c`). Não é necessário alterar nesta fase. Mas se o planner quiser atualizar §"Inventário de slides" para refletir os 20 sections pós-fase 3, segue diff sugerido:

### 8.1 §"Inventário de slides (ordem atual, pós-fase 2)" → "pós-fase 3"

**De** (linhas 108-125 atuais):

```markdown
## Inventário de slides (ordem atual, pós-fase 2)

| # | classe | cabeçalho | conteúdo |
|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho) | Abertura |
... (16 linhas, terminando em #15 slide-fig)
```

**Para** (acrescentar 4 linhas na faixa #11..#14, deslocar #11..#15 para #15..#19):

```markdown
## Inventário de slides (ordem atual, pós-fase 3)

| # | classe | cabeçalho | conteúdo |
|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho) | Abertura |
| 1 | slide-title-tcc | (sem cabeçalho) | Capa do TCC |
| 2 | slide-agenda | (sem temático) | Agenda |
| 3 | slide-related | `> introdução` | Martins p1 |
| 4 | slide-related | `> mineração de dados educacionais` | Zorić fundido |
| 5 | slide-phases | `> as quatro fases da edm` | Zorić p3 |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | Yağcí fundido |
| 7 | slide-related | `> o dataset csedm` | INTRO-01: CSEDM em ProgSnap2 |
| 8 | slide-related | `> o problema do kt binário` | INTRO-03a: Shi 2022 |
| 9 | slide-related | `> sinal pedagógico perdido` | INTRO-03b: gap pedagógico |
| 10 | slide-marker slide-marker--phase1 | (sem temático) | MARKER-01: Fase 1 EDM done |
| **11** | **slide-related** | **`> como navegamos o csedm`** | **EDA-01: distribuição por assignment** |
| **12** | **slide-related** | **`> aproximação ao protocolo`** | **EDA-02: 413 → 410 → 328/82 + truncagem 50** |
| **13** | **slide-related** | **`> três jeitos de aprender`** | **EDA-03: scatter PCA dos 3 perfis** |
| **14** | **slide-marker slide-marker--phase2** | **(sem temático)** | **MARKER-02: Fase 2 EDM done, Fase 3 running** |
| 15 | slide-code | `> o que o code-dkt olha` | (idem fase 1) |
| 16 | slide-kcfig | `> kcs semânticos extraídos` | (idem fase 1) |
| 17 | slide-problem | `> retomando o problema` | Martins p2 |
| 18 | slide-problem | `> retomando o problema` | Martins p3 |
| 19 | slide-fig | `> evolução por dificuldade` | Curva Code-DKT |

**Estado do deck:** 20 slides após a fase 3 (era 16; 4 novos da fase 3 inseridos no gap após MARKER-01).
```

### 8.2 §"Gaps reservados" linha 130 → linha 131

A linha 130 ("Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3).") deve ser **removida ou substituída** ao fim da fase 3, porque o gap deixou de existir. Sugestão (planner decide remover ou marcar como done):

```markdown
**Gaps reservados para fases 4-5:**

- Antes do trio Martins+fig (entre slide-code/slide-kcfig e Martins p2): MODEL-01, MODEL-03, MODEL-04, MODEL-05 (fase 4); slide-code vira MODEL-03 reaproveitado; slide-kcfig é a saída do pipeline MODEL-05; slide-fig é o CLOSE-03.
- Após slide-fig: MARKER-03 (fim da fase 4 da EDM); depois TOOL-01, TOOL-03, MARKER-04, END-01 (fase 5); AGENDA-01 revisado.
```

**Discretion (planner):** D-61 diz "nenhuma correção do STYLE.md é necessária nesta fase". A atualização do §Inventário é trivial mas não obrigatória; pode entrar em commit separado ao fim da fase ou ser deferida para a transição. Recomendo aplicar dentro desta fase para manter STYLE.md sempre consistente (padrão da fase 2 que reescreveu §Gaps em `f4dde9c`).

---

## §9 Ponto exato de inserção no DOM (D-60)

### 9.1 Boundaries verificadas em HEAD (2026-05-28)

| Slide | Comentário | `<section>` | `</section>` |
|---|---|---|---|
| 10 (MARKER-01, ÂNCORA SUPERIOR) | linha 200 | linha 201 | **linha 243** |
| 11 (slide-code, ÂNCORA INFERIOR) | linha 245 | linha 247 | linha 294 |

[VERIFIED: grep -n no index.html, 2026-05-28]

Entre linhas **243 e 245** existe linha em branco (244). É exatamente aí que os 4 novos sections entram.

### 9.2 Estado final esperado (ordem no `<div class="slides">`)

| `#` (0-based) | Slide | classe | cabeçalho |
|---|---|---|---|
| 0..9 | (inalterados) | — | — |
| 10 | MARKER-01 | slide-marker slide-marker--phase1 | (sem temático) |
| **11** | **EDA-01 (NOVO)** | slide-related | `> como navegamos o csedm` |
| **12** | **EDA-02 (NOVO)** | slide-related | `> aproximação ao protocolo` |
| **13** | **EDA-03 (NOVO)** | slide-related (ou slide-eda) | `> três jeitos de aprender` |
| **14** | **MARKER-02 (NOVO)** | slide-marker slide-marker--phase2 | (sem temático) |
| 15 | slide-code (era 11) | slide-code | `> o que o code-dkt olha` |
| 16 | slide-kcfig (era 12) | slide-kcfig | `> kcs semânticos extraídos` |
| 17 | slide-problem (era 13) | slide-problem | `> retomando o problema` |
| 18 | slide-problem (era 14) | slide-problem | `> retomando o problema` |
| 19 | slide-fig (era 15) | slide-fig | `> evolução por dificuldade` |

Total: **20 sections** (16 prévios + 4 novos). CONTEXT `<domain>` linha 18 prevê 20.

### 9.3 Comentários a inserir

Cada `<section>` nova precisa de comentário com o padrão existente. Sugestão:

```html
<!-- ============ SLIDE · EDA-01 · Como navegamos o CSEDM (Spring 2019) ============ -->
<!-- ============ SLIDE · EDA-02 · Pré-processamento, aproximação ao protocolo (Shi et al., 2022) ============ -->
<!-- ============ SLIDE · EDA-03 · Três perfis de alunos, scatter PCA (CSEDM Spring 2019) ============ -->
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020) ============ -->
```

### 9.4 Notas de cuidado

- EOL Unix (preservar; não introduzir CRLF).
- Indentação 6 espaços para `<section>` raiz (consistente com sections existentes).
- Marca d'água Facens `<svg class="wm">` em TODOS os 4 sections (incluindo MARKER-02, idem MARKER-01).
- Atenção em encoding: `Zorić`/`Yağcı` com diacríticos corretos (memória `feedback_marker_design` registra que comentários do MARKER atualmente usam "Zoric" sem acento — manter coerência com MARKER-01 ou padronizar; sugestão: padronizar para "Zorić" em todos os comentários numa drive-by passada).

---

## §10 Lessons learned da fase 2 (PHASE-SUMMARY) aplicáveis aqui

### 10.1 Iterações textuais pós-checkpoint são padrão

PHASE-SUMMARY da fase 2 registrou 8 iterações pós-checkpoint em 4 plans (média 2/plan). Padrão a herdar:

- **Antecipar 1-2 iterações por slide** EDA com voz própria. Granularidade aritmética, vocabulário ABNT e ancoragem em "nosso dataset" frequentemente precisam de ajuste.
- **Microcópia exata fica no checkpoint visual**, não trava no plano. Plano define a estrutura + numbers + cabeçalho + rodapé; reviewer humano polishea no browser.

### 10.2 Drive-by sweeps de convenção tipográfica

D-54 (`<i>et al.</i>` ABNT) foi descoberto durante 02-03 e aplicado em batch no deck inteiro (8 ocorrências). Padrão a herdar:

- Se durante a execução EDA-01/02/03 surgir convenção tipográfica nova (`<i>baseline</i>`, `<i>cluster</i>`, etc.), aplicar em todo o deck no mesmo commit.
- Listar potenciais drive-bys ANTES da execução: `<i>baseline</i>`, `<i>cluster</i>`, `<i>scatter</i>`, `<i>K-Means</i>`, `<i>assignment</i>`, `<i>pipeline</i>`.

### 10.3 Decisões "stub aceito, redesenho diferido" são legítimas

PHASE-SUMMARY registra MARKER-01 stub aprovado mesmo com backlog visual (depois resolvido em `5d44606`). Padrão a herdar:

- MARKER-02 herda redesign de `5d44606` (pipeline CI/CD); sem backlog visual nesta fase.
- Se EDA-03 PNG ficar visualmente fraco no primeiro shot, aceitar como stub se a navegação fluir; redesenho posterior em batch antes da defesa.

### 10.4 Verifier off + checkpoint humano funciona

PHASE-SUMMARY registra que toda a fase 2 rodou sem `gsd-verifier` subagent. Padrão a herdar:

- Reviewer humano abre o browser e valida cada plan imediatamente após execução.
- Plano define gates explícitos (lista de checks por slide) para o reviewer percorrer no browser.

### 10.5 Vocabulário herdado (NÃO redefinir)

PHASE-SUMMARY linhas 178-181 lista vocabulário herdado:

- "5 assignments × 10 problemas" (D-50) — fase 3 pode usar implícito
- 6 colunas-chave do ProgSnap2 (D-51) — fase 3 pode partir desse vocabulário
- ponte KT → trabalho → CSEDM (D-53) — fase 3 não precisa repetir
- `<i>et al.</i>` ABNT (D-54) — fase 3 mantém em qualquer citação parentética múltipla
- "tratam respostas como corretas/incorretas, ignorando seu conteúdo" (D-52) — disponível mas não obrigatório

---

## Common Pitfalls

### Pitfall 1: Em-dash em phrasing-alvo deste RESEARCH

**What goes wrong:** Os exemplos de phrasing em §1.2, §2.4, §7.1-7.3 deste RESEARCH foram digitados em prosa; podem conter em-dash (`—`) que NÃO podem entrar no HTML (viola D-70 e memória `feedback_no_em_dashes`).

**Why it happens:** Hábito de escrita acadêmica.

**How to avoid:** Antes de cada `git add`, rodar:
```bash
grep -n '—' apresentacao/index.html | grep -E '(como navegamos|aproximação ao|três jeitos|MARKER · As quatro fases.*fase 2)'
# deve retornar vazio
```

**Warning signs:** Slide entregue contém "CSEDM — Spring 2019" ou similar. Converter para vírgula/parêntese.

### Pitfall 2: ProgSnap2 mencionado em EDA-01

**What goes wrong:** ProgSnap2 é nominalmente único em INTRO-01 (Key Decision PROJECT.md). Se EDA-01 escrever "...armazenado em ProgSnap2..." ou similar, quebra a Key Decision.

**Why it happens:** Tentação de re-introduzir o formato ao mencionar "n estudantes, n problemas, n eventos".

**How to avoid:** Verificar literalmente que a palavra "ProgSnap2" não aparece em EDA-01 (corpo ou rodapé). Padrão: usar "CSEDM" como nome do dataset.

**Warning signs:** `grep -c 'ProgSnap2' apresentacao/index.html` retorna mais que 1 (já está 1 em INTRO-01 `Fonte: Price (2020); CSEDM 2021.`).

### Pitfall 3: Code-DKT mencionado nos slides EDA

**What goes wrong:** Code-DKT é gate forte da fase 4 (MODEL-01/04). Mencionar nos slides EDA da fase 3 rouba o palco.

**Why it happens:** Tentação narrativa de "fechar a frase" introduzindo o modelo logo. Em EDA-02 especialmente, ao falar de "truncagem em 50 tentativas" pode-se ser tentado a adicionar "(...que vai alimentar o Code-DKT)".

**How to avoid:** Verificar literalmente que "Code-DKT" não aparece em EDA-01/02/03. EDA-02 pode dizer "modelos de KT" ou "o LSTM" genericamente; sem nomear.

**Warning signs:** Frase tipo "...para alimentar o Code-DKT" ou "...os modelos KT incluindo Code-DKT". Reescrever.

### Pitfall 4: Confundir números Release/Train com MainTable

**What goes wrong:** eda_insights.md Seção 1.1 (datado pré-migração) reporta 233/224/234/221/222 alunos (Release/Train); MainTable Spring 2019 reporta 386/340/361/315/306. Confundir é fácil.

**Why it happens:** eda_insights.md é a referência primária do CONTEXT D-64a, mas está desatualizado em relação à migração `project_split_discovery` (Release/ → MainTable Spring 2019).

**How to avoid:** Plano DEVE incluir sub-task explícita "rodar `python3 -c 'import pandas; ...'` (snippet em §2.1 deste RESEARCH) e usar os números MainTable Spring 2019 (386/340/361/315/306)". Reusar cell 51 do notebook 01_eda.ipynb (output já confirmado).

**Warning signs:** Slide com 233 alunos em A1 ou 222 em A5. Re-verificar contra §2.1.

### Pitfall 5: K-Means scatter com paleta off-brand

**What goes wrong:** Cores default do matplotlib (`tab10` etc.) podem destoar da paleta UniFacens do deck (azul `#2667FF`, paleta clara). Slide visualmente quebra a coerência.

**Why it happens:** Cópia direta da cell 46 do notebook usa paleta `{'Alto desempenho': '#2196F3', 'Médio': '#FF9800', 'Em risco': '#F44336'}` — azul/laranja/vermelho do Material Design, NÃO da paleta UniFacens.

**How to avoid:** Script `scripts/build_eda_pca_scatter.py` (§6.3) sugere `palette = {"Alto desempenho": "#2667FF", "Médio": "#F2A516", "Em risco": "#D7191C"}` — azul `#2667FF` (uni-blue exato) + âmbar `#F2A516` (caloroso, ABNT-friendly) + vermelho `#D7191C` (urgência). Validar no browser que casa com o slide.

**Warning signs:** Scatter no slide com azul-pastel ou laranja-pastel (Material Design). Re-rodar script com paleta UniFacens.

### Pitfall 6: PNG não copiado para apresentacao/assets/

**What goes wrong:** STRUCTURE.md "Slide novo na apresentação" diz: "Assets em `apresentacao/assets/` (não referenciar `results/` diretamente — copiar)". Se o slide referenciar `../results/sec2_perfis_pca.png`, quebra quando alguém roda `apresentacao/` standalone.

**Why it happens:** Atalho mental. Script gera em `results/`, slide aponta para lá.

**How to avoid:** Plano DEVE incluir task `cp results/sec2_perfis_pca.png apresentacao/assets/eda-perfis-pca.png`. Slide referencia `assets/eda-perfis-pca.png` (relativo a `apresentacao/index.html`).

**Warning signs:** `grep -E 'src=.*results' apresentacao/index.html` retorna match.

### Pitfall 7: MARKER-02 esquecer drive-by no comentário do MARKER-01

**What goes wrong:** O comentário do MARKER-01 atual diz "fase 1 concluida"; o comentário do MARKER-02 vai dizer "fase 2 concluida". Ambos referenciam Zorić (2020). Sem drive-by, o comentário do MARKER-01 fica preso à fase 1 e MARKER-02 (e futuro MARKER-03/04) ficam com strings duplicadas. Não é bug, mas é dívida.

**Why it happens:** Foco em MARKER-02 isolado; copy-paste do MARKER-01 sem revisão.

**How to avoid:** Não há ação obrigatória nesta fase. Apenas observar que MARKER-03/04 vão multiplicar o padrão. Sem drive-by necessário.

**Warning signs:** Eventual confusão de futuros revisores; baixo impacto.

### Pitfall 8: D-66c números errados no slide (eda_insights vs cell 46)

**What goes wrong:** Se planner usar D-66c literal ("Alto 139 / Médio 66 / Em risco 248, 453 estudantes"), valores não batem com o que a cell 46 do notebook produz HOJE (Alto=96 / Médio=19 / Em risco=124, 239 estudantes).

**Why it happens:** eda_insights.md §3.1 está desatualizado em relação ao notebook re-executado pós-migração.

**How to avoid:** §3.2 deste RESEARCH força reconciliação. Plano DEVE incluir sub-task "re-executar `scripts/build_eda_pca_scatter.py` (§6.3) e capturar o resumo numérico real para uso no slide".

**Warning signs:** Slide entregue com "n=139" no "Alto desempenho" da legenda. Re-gerar PNG e validar contagem.

---

## Code Examples

### Exemplo 1: Markup `.slide-related` clonável para os 3 EDAs (referência: INTRO-03b linhas 184-198)

```html
<!-- ============ SLIDE · EDA-02 · Pré-processamento, aproximação ao protocolo (Shi et al., 2022) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>aproximação ao protocolo<span class="caret blink"></span></p>

    <p class="rel-lead">Nosso pré-processamento segue o protocolo de Shi <i>et al.</i> (2022) como <i>baseline</i> de comparação, com ênfase em análise.</p>

    <p class="rel-lead">Dos 413 alunos brutos do CSEDM, mantivemos <b>410</b> com pelo menos 3 tentativas de execução, mesma seleção do paper. Em seguida, dividimos em <b>328 estudantes para treino e 82 para teste</b>, na proporção 80/20 com semente fixa.</p>

    <p class="rel-lead">Limitamos cada sequência às <b>50 últimas tentativas</b>. A mediana é 32 tentativas por aluno e <i>assignment</i>; 28% dos pares ultrapassam 50, com cauda longa até 272.</p>

    <p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
  </div>
</section>
```

### Exemplo 2: Markup do MARKER-02 (copy-paste com 4 deltas; ver §5)

```html
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase2">
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
      <div class="marker-stage">
        <div class="marker-pill marker-pill--done">
          <span class="marker-pill-icon">&check;</span>
          <span class="marker-pill-name">Preparação dos Dados</span>
        </div>
        <span class="marker-badge">[done]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--running">
          <span class="marker-pill-icon">&#x21BB;</span>
          <span class="marker-pill-name">Modelagem e Avaliação</span>
        </div>
        <span class="marker-badge">[running]</span>
      </div>
      <span class="marker-arrow">&rarr;</span>
      <div class="marker-stage">
        <div class="marker-pill marker-pill--pending">
          <span class="marker-pill-icon">&#x25CB;</span>
          <span class="marker-pill-name">Implantação</span>
        </div>
        <span class="marker-badge marker-badge--empty">[]</span>
      </div>
    </div>

    <p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

### Exemplo 3: CSS sugerido (acréscimo opcional em `theme-unifacens.css`)

```css
/* ===========================================================================
   SLIDE · EDA · tabela compacta A1..A5 (template B do RESEARCH §4.2)
   Estética ABNT (borda fina preta, sem radius), última coluna em azul UniFacens
   =========================================================================== */
.eda-grid {
  width: 92%; margin: 32px auto 0;
  border-collapse: collapse;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 21px;
}
.eda-grid th, .eda-grid td {
  border: 1.5px solid #1f1f1f;
  padding: 12px 18px;
  text-align: center;
}
.eda-grid th { background: #fff; font-weight: 700; color: var(--uni-ink); }
.eda-grid td { background: #fff; color: var(--uni-ink); }
.eda-grid tr td:first-child { text-align: left; font-weight: 700; }
.eda-grid tr td:last-child { color: var(--uni-blue); font-weight: 700; }

/* SLIDE · EDA-03 · scatter PCA + insight em destaque */
.eda-fig {
  margin: 16px auto 0; max-width: 78%;
  display: flex; justify-content: center;
}
.eda-fig img { width: 100%; height: auto; max-height: 460px; object-fit: contain; }

.eda-insight {
  margin: 20px auto 0; max-width: 92%; text-align: center;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 23px; font-weight: 700; color: var(--uni-ink);
  line-height: 1.35;
}
.eda-subinsight {
  margin-top: 10px; font-size: 19px; color: #5b6472; text-align: center;
  font-weight: 400;
}
```

---

## Don't Hand-Roll

| Problema | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Componente progress bar das 4 fases | Inventar novo CSS | Reusar `.slide-marker` + modificadores `--done`/`--running`/`--pending` (CSS linhas 359-453 do `theme-unifacens.css`) | Componente redesenhado em `5d44606` (pipeline CI/CD ABNT); zero CSS novo para MARKER-02 (D-67d) |
| Cabeçalho `> [seção]` dos slides EDA | Inventar nova estrutura HTML | `<p class="deck-topic"><span class="ps1">&gt;</span>texto<span class="caret blink"></span></p>` | Padrão já consolidado em 9 slides; CSS pronto (linhas 42-43 do theme) |
| Rodapé Fonte: dos slides EDA | Criar nova classe `.eda-cite` | Reutilizar `.rel-cite` (Arial 18px, `#5b6472`, `margin-top: auto`) | 4 slides já usam (Martins p1, Zorić fundido, Yağcí fundido, INTRO-01..03b); coerência visual + sem CSS novo |
| Tabela A1..A5 do EDA-01 | Reinventar grid CSS | `<table class="eda-grid">` com CSS de §4.2 (~14 linhas) | Padrão ABNT (borda fina, sem radius) coerente com `.bridge-seq` + `.kc-box` + `.marker-pill` |
| Scatter PCA do EDA-03 | Re-implementar K-Means + PCA do zero | `scripts/build_eda_pca_scatter.py` baseado na cell 46 do notebook 01 | SEED=42 garante reprodutibilidade; código já testado; respeita CONVENTIONS.md (`scripts/<verbo>_<objeto>.py`) |
| Citação parentética ABNT | Improvisar formato | Seguir convenção do projeto: `(Sobrenome, ano)` em paráfrase, `<i>et al.</i>` para 3+, `;` para 2 autores | Manual MSGQ-21.01 + D-54 fase 2 herdado; já normalizado no deck inteiro |
| Marca d'água Facens | Reimplementar SVG | Reutilizar `<svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>` | Símbolo definido uma vez no `<defs>` do index.html; presente em todos os slides de conteúdo |
| Conversão de em-dash em prosa | Esquecer / ignorar | `grep -n '—' apresentacao/index.html` antes de commit | Memória `feedback_no_em_dashes` vinculante; D-70 |
| Números do dataset (per-assignment) | Citar de memória ou de eda_insights.md (Release/Train) | Rodar pandas em MainTable.csv (§2.1) ou conferir cell 51 do notebook 01 | eda_insights.md está desatualizado; MainTable é a base que casa com INTRO-01 + EDA-02 |

**Key insight:** A fase 1+2 travou o vocabulário de classes, o markup, o phrasing-alvo dos slides correlatos e o componente `.slide-marker`. A fase 3 deve **reutilizar agressivamente** e adicionar **no máximo 2 classes pequenas** (`.eda-grid` + `.eda-fig`/`.eda-insight`) para os 2 novos elementos visuais. Cada classe CSS além disso é dívida técnica.

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|---|---|---|
| A1 | Numbers MainTable Spring 2019 (n=386/340/361/315/306, % correct=26,15/20,06/20,34/24,72/30,62) são os corretos para EDA-01, em vez dos números Release/Train do eda_insights.md (n=233/224/234/221/222) | §2 (reconciliação D-64a) | Baixo — diferença pp < 1,3pp; ambos seriam aceitos, mas só os MainTable casam com a narrativa 413 → 410 → 328/82 de EDA-02 |
| A2 | "min_attempts ≥ 3" é o filtro literal que produz 410 do dataset bruto, mesmo que o paper Shi não use essa string textual | §1.1, §2.2 | Baixo — número 410 coincide entre nossa implementação e paper; o filtro literal é inferência de `src/data_loader.py` que sempre foi nosso; defensável |
| A3 | A cell 46 atual do notebook 01_eda.ipynb (239 alunos, Alto=96, Médio=19, Em risco=124, silhouette k=3=0,2564) representa o estado HOJE; eda_insights.md §3.1 (453 alunos, 139/66/248) está OBSOLETO | §3.2 | Médio — se planner não re-executar, slide entregue terá números errados. Mitigação: plano força sub-task de re-execução via `scripts/build_eda_pca_scatter.py` |
| A4 | Template B (`<table class="eda-grid">`) é melhor que A (`.bridge-seq`) e C (`.eda-card`) para EDA-01 | §4 | Baixo — reviewer pode preferir A ou C no checkpoint visual; iteração pós-checkpoint é esperada |
| A5 | Paleta `#2667FF` / `#F2A516` / `#D7191C` para os 3 perfis no scatter PCA casa com o deck UniFacens | §6.3 | Baixo — escolha visual reviewer no checkpoint; reviewer pode preferir outra paleta; mudança é trivial (`palette = {...}` dict no script) |
| A6 | Frase de insight EDA-03 "O grupo majoritário não é quem erra muito; é quem tenta pouco." é a mais punchy entre as 3 variantes do CONTEXT D-66a | §3.3 | Baixo — variantes equivalentes; reviewer escolhe no checkpoint |
| A7 | Snippet `scripts/build_eda_pca_scatter.py` é viável como one-shot reprodutível (early.csv + late.csv existem em `data/`) | §6.3 | Baixo — verificado em §3.1 que cell 35 do notebook 01 carrega exatamente esses 2 CSVs; script replica a lógica |
| A8 | D-67a deve ser lido como "estado FINAL de MARKER-02" (pills 1+2 done, pill 3 running, pill 4 pending), não como "delta literal vs MARKER-01" | §5 | Baixo — interpretação derivada do contexto narrativo (MARKER-02 é o slide DEPOIS de Fase 2 concluída); deltas literais ficam em §5.2 |
| A9 | Não há regra ABNT que exija "Fonte:" rodapé do EDA-03 mencionar especificamente "K-Means k=3 SEED=42"; é boa prática transparência mas reviewer pode preferir mais simples | §7.3, §7.4 | Baixo — formato literal do D-66d; reviewer pode pedir simplificação (ex.: "Fonte: análise sobre CSEDM (Spring 2019)."); ajustável trivialmente |
| A10 | Cabeçalho `> aproximação ao protocolo` é melhor que `> pré-processamento` para EDA-02 | §7.2 | Baixo — recomendação subjetiva; D-63b deixa em aberto; reviewer decide |

**Itens NÃO assumidos (VERIFIED):**
- Números do dataset MainTable: `pd.read_csv` rodado, output capturado
- Phrasing literal Shi §4.1 e §4.2: lido página 5 do PDF
- Estado HEAD do MARKER-01: lido literalmente nas linhas 200-243 do index.html
- CSS do `.slide-marker` redesign (5d44606): lido nas linhas 359-453 do theme-unifacens.css
- Boundaries de section em index.html: grep verificado
- Outputs atuais da cell 46 do notebook 01: lidos do `.ipynb` raw JSON

---

## Open Questions

1. **Granularidade de commit dentro do plan EDA-03 (gerar PNG + slide juntos vs separados)?**
   - What we know: Convenção é commit atômico por slide concluído. Gerar PNG via script é uma sub-task.
   - What's unclear: Se o PNG vai como commit separado ("eda: gerar scatter pca perfis (SEED=42)") ou junto com o slide ("apresentacao: slide EDA-03 + scatter pca perfis").
   - Recommendation: **Junto**, dentro de 1 commit "apresentacao: slide EDA-03 - perfis dos alunos (scatter PCA)". Razão: PNG é asset do slide; sem ele o slide não renderiza. Separar é dívida.

2. **Atualizar §"Inventário" do STYLE.md ao fim da fase 3?**
   - What we know: D-61 não obriga; fase 2 (`f4dde9c`) atualizou §Gaps mas não §Inventário.
   - What's unclear: Se vale a pena fazer agora ou deferir para a transição.
   - Recommendation: **Junto** com último plan da fase 3 (MARKER-02 normalmente é último porque depende de não haver mais inserções no gap), em commit separado `docs(style): atualizar inventário e gaps pós-fase 3`. Trivial; evita 2ª passada.

3. **Cabeçalho do EDA-03 — "perfis dos alunos" vs "três jeitos de aprender"?**
   - What we know: D-63c aberto; este RESEARCH §7.3 recomenda (b) "três jeitos de aprender".
   - What's unclear: Se o reviewer prefere o descritivo (a) ou o narrativo (b).
   - Recommendation: Plano propõe (b) com fallback (a) explicitado. Checkpoint humano decide.

4. **Geração do PNG via script standalone (`build_eda_pca_scatter.py`) vs reuso do cell 46 do notebook?**
   - What we know: Cell 46 gera fig combinada (scatter + heatmap); script gera só scatter.
   - What's unclear: Esforço marginal de criar o script vs manter o cell.
   - Recommendation: **Script standalone** (§6.3). Razões: reprodutível em segundos; resumo numérico no print confirma os números do slide; sem dependência de `jupyter nbconvert`; padrão `scripts/<verbo>_<objeto>.py` de CONVENTIONS.

5. **Drive-by sweep: padronizar comentários do deck para "Zorić" (com diacrítico) em vez de "Zoric"?**
   - What we know: MARKER-01 (linha 200) atual usa "Zoric" sem acento no comentário; mas o Fonte: usa "Zorić" com acento (correto).
   - What's unclear: Se vale a pena padronizar via drive-by na fase 3.
   - Recommendation: **Não nesta fase** (sem retorno narrativo; comentário HTML não aparece em produção). Anotar como dívida menor para o batch de polimento pré-defesa.

6. **Ordem de implementação MARKER-02 primeiro ou EDA-03 primeiro?**
   - What we know: CONTEXT sugere MARKER-02 → EDA-02 → EDA-01 → EDA-03 (do mais determinístico ao mais arriscado). Alternativa: EDA-03 primeiro porque precisa gerar PNG novo.
   - What's unclear: Trade-off "derisca cedo" (EDA-03 primeiro) vs "facil primeiro, complexo depois" (MARKER-02 primeiro).
   - Recommendation: **Manter ordem do CONTEXT** (MARKER-02 → EDA-02 → EDA-01 → EDA-03). Razão: MARKER-02 é puro reuso (alta confiança, 4 alterações mecânicas validadas); EDA-02 é determinístico (números travados em §2); EDA-01 calibra layout da tabela; EDA-03 fecha com o slide mais visual. Aceitar variação por preferência do executor.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` (servidor HTTP) | D-74 (validação visual) | ✓ | 3.x | — |
| `pandas` (validação numérica per-assignment) | §2 desta pesquisa | ✓ | (rodado com sucesso 2026-05-28) | — |
| `scikit-learn` (K-Means + PCA) | §6.3 script de geração de PNG | ✓ (já no .venv) | (cell 46 do notebook usa sem problema) | — |
| `matplotlib` (scatter PNG) | §6.3 | ✓ (já no .venv) | (cell 46 usa) | — |
| Browser (Firefox/Chrome) | D-74 | ✓ (humano operador) | — | — |
| Reveal.js (CDN) | runtime do slide | ✓ | 5.1.0 (linha 8, 328 do index.html) | — |
| Fontes Cascadia Code (CDN) | tipografia `.deck-topic` | ✓ | jsdelivr fontsource | (degrada para Consolas/monospace local) |
| `early.csv` + `late.csv` em `data/` | §3.1 fonte das features de cluster | ✓ | (verificado: 9106 linhas + 5722 linhas) | — |
| `data/CSEDM/MainTable.csv` | §2 verificação per-assignment | ✓ | (verificado: 201.570 eventos) | — |
| `data/CSEDM/LinkTables/Subject.csv` | §3.1 X-Grade dos alunos | ✓ | (verificado pelo cell 35 do notebook) | — |

Sem dependências externas que possam bloquear esta fase. Sem build system. Sem testes automatizados (validação humana via browser).

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|---|---|---|---|
| eda_insights.md §1.1 (Release/Train, 246 alunos, n=233/224/234/221/222) como fonte primária dos números EDA-01 | MainTable Spring 2019 (n=386/340/361/315/306) via cell 51 do notebook 01 | 2026-05-17 (memória `project_split_discovery`; pipeline migrou para MainTable+Shi) | EDA-01 da fase 3 usa MainTable; eda_insights.md §1.1 está desatualizado |
| eda_insights.md §3.1 (453 alunos, Alto=139/Médio=66/Em risco=248) como base do K-Means | cell 46 atual do notebook 01 (239 alunos, Alto=96/Médio=19/Em risco=124) | 2026-05-17 (re-execução pós-migração) | EDA-03 da fase 3 usa cell 46 atual; eda_insights.md §3.1 está desatualizado |
| `.slide-marker` stub original (host + modificadores `--done`/`--pending`) | `.slide-marker` redesign CI/CD ABNT (pipeline com pills + setas + spin animation) | 2026-05-28 (commit `5d44606`; memória `feedback_marker_design`) | MARKER-02..04 herdam o redesign; zero CSS novo nas fases 3-5 |
| ProgSnap2 mencionado em INTRO + EDA + TOOL | ProgSnap2 nominalmente único em INTRO-01 | 2026-05-27 (1ª rodada feedback orientadora) | EDA-01 (fase 3) e TOOL-01 (fase 5) NÃO mencionam ProgSnap2 nominalmente |
| Citação direta literal default em slides correlatos | Paráfrase indireta com autor parentético default | 2026-05-27 (2ª rodada feedback) | EDA-01/02/03 explicitamente paráfrase (D-69); MARKER-02 sem citação |
| MARKER-01 estado "vivo" = "Fase 1 done, Fase 2 pending" | MARKER-01 estado "vivo" = "Fase 1 done, Fase 2 running" | 2026-05-28 (redesign `5d44606`) | MARKER-02 delta literal muda: pill 2 sai de `--running` (não `--pending`) para `--done`; pill 3 sai de `--pending` para `--running` |

**Deprecated/outdated:**
- eda_insights.md Seções 1.1 e 3.1 (números Release/Train) — fora de sincronia com pipeline atual; aguarda atualização documental pós-defesa.
- CONTEXT D-66c números (453 estudantes, 139/66/248) — substituídos pelos números atuais da cell 46 (239 estudantes, 96/19/124). RESEARCH §3.2 documenta a reconciliação.

---

## Sources

### Primary (HIGH confidence)
- `docs/Code-DKT.pdf` (Shi, Mao, Akram, Lytinen e Heffernan, 2022) — §4.1 Dataset & Experiments Setup, §4.2 Hyperparameter Tuning — páginas 5-6 lidas literalmente em 2026-05-28; todos os trechos do §1.1 deste RESEARCH são citações diretas verificadas.
- `data/CSEDM/MainTable.csv` — `pd.read_csv` + `groupby` + Shi filter + `train_test_split(random_state=1)` rodados em 2026-05-28; outputs capturados em §2.1 e §2.2.
- `apresentacao/index.html` (HEAD 2026-05-28, 564 linhas) — boundaries de section verificadas via grep; MARKER-01 lido literalmente nas linhas 200-243; slide-code lido na linha 247.
- `apresentacao/assets/theme-unifacens.css` (453 linhas) — `.slide-marker` redesign lido nas linhas 359-453; `.bridge-seq` lido nas linhas 197-210; classes Fonte: inventariadas.
- `apresentacao/STYLE.md` (162 linhas) — §Gaps reservados linha 130 confirmada consistente com fase 3; §Inventário de slides linhas 110-124 lida.
- `notebooks/01_eda.ipynb` cell 35 (load early.csv + late.csv + Subject.csv), cell 44-46 (K-Means + PCA), cell 51 (per-assignment MainTable) — outputs preservados lidos em 2026-05-28.
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/PHASE-SUMMARY.md` — vocabulário herdado, padrões de execução, learnings.
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-RESEARCH.md` + `02-PATTERNS.md` — modelo do RESEARCH/PATTERNS desta fase.

### Secondary (MEDIUM confidence)
- Memória `feedback_marker_design` (2026-05-28) — confirma MARKER-XX redesenhado em `5d44606`; tabela de modificadores.
- Memória `project_split_discovery` (2026-05) — paper usa 80/20 de 410; migração Release/ → MainTable+Shi confirmada.
- Memória `project_codedkt_results` (2026-05-17) — A439 first_auc=72,55% (dentro ±3% Shi); ancorada na pipeline com 410 alunos.
- Memória `feedback_no_em_dashes` — vinculante para D-70.
- Memória `feedback_tcc_writing_style` — ABNT + prosa acessível.
- Memória `reference_manual_citacoes` — manual Facens; "tradução nossa" só em direta literal.
- Memória `feedback_correlatos_antes` — novo padrão `> [seção]` substituiu slide dedicado a autor.
- `.planning/phases/01-reformata-o-da-base/01-CONTEXT.md` — D-01..D-30 da fase 1.
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-CONTEXT.md` — D-31..D-47 da fase 2; especialmente D-38b que mandata a ponte 413 → 410 → 328/82 nesta fase.

### Tertiary (LOW confidence — informacional, não trava decisões)
- `docs/eda_insights.md` §1.1 (Release/Train) e §3.1 (K-Means 453 alunos) — desatualizadas em relação ao pipeline; usadas como referência histórica e confrontadas com fontes primárias.
- Manual MSGQ-21.01 REV.17 (`apresentacao/4. MSGQ-21.01...pdf`) — convenção do projeto já está consolidada via STYLE.md e memória `reference_manual_citacoes`; manual em si não foi re-lido nesta pesquisa.
- `docs/refs/shi2022_code_dkt.md` — resumo do paper (lido para confirmação cruzada do filtro 410 e do split 4:1).

---

## Metadata

**Confidence breakdown:**
- Phrasing do paper Shi 2022 §4.1/§4.2: HIGH — citações literais extraídas, página 5 do PDF lida diretamente.
- Números do dataset (per-assignment): HIGH — pandas rodado em MainTable.csv, output capturado, cell 51 do notebook 01 confirma cross-reference.
- K-Means / PCA estado atual da cell 46: HIGH — outputs preservados no `.ipynb` raw lidos diretamente; reconciliação com eda_insights.md documentada em §3.2.
- Ponto de inserção no DOM (linhas 243-245): HIGH — boundaries lidas via grep no HEAD do index.html.
- Deltas MARKER-01 → MARKER-02: HIGH — markup HEAD lido literalmente; CSS validado para confirmar spin animation só em `--running`.
- Padrão visual EDA-01 (Template B `<table>`): MEDIUM — recomendação derivada de comparação com templates A e C; reviewer pode preferir alternativa no checkpoint.
- Geração do PNG (script standalone): MEDIUM — snippet completo testável mas não rodado nesta pesquisa; reproduz código da cell 46 com paleta UniFacens-friendly.
- Phrasing-alvo dos 3 slides EDA: MEDIUM — variantes oferecidas, recomendações justificadas; reviewer humano polirá no checkpoint visual (padrão fase 2).
- Variantes de cabeçalho `> [seção]`: MEDIUM — 3 variantes por slide com avaliação; D-63 aberto por design.

**Research date:** 2026-05-28
**Valid until:** 2026-06-27 (escopo estável; única dependência fora deste repo é o PDF do Shi 2022 — imutável)

## RESEARCH COMPLETE

**Phase:** 3 — EDA e Pré-processamento (Fase 2 EDM)
**Confidence:** HIGH

### Key Findings

1. **Reconciliação D-64a resolvida (numbers MainTable vs Release/Train):** os números por assignment em eda_insights.md §1.1 (n=233/224/234/221/222, Release/Train 246 alunos) **divergem em até 1,3pp** dos números MainTable Spring 2019 (n=386/340/361/315/306, % correto=26,15/20,06/20,34/24,72/30,62 — cell 51 do notebook 01 confirma exato). Recomendado **usar MainTable** para coerência narrativa com EDA-02 (que comunica 413 → 410 → 328/82) e com INTRO-01 (que cita 413 estudantes).
2. **Reconciliação D-66c resolvida (K-Means numbers):** eda_insights.md §3.1 reporta 453 alunos / Alto=139 / Médio=66 / Em risco=248; cell 46 ATUAL do notebook 01 reporta **239 alunos / Alto=96 / Médio=19 / Em risco=124** com silhouette k=3=0,2564. Notebook foi re-executado pós-migração. Plano DEVE re-executar `scripts/build_eda_pca_scatter.py` (§6.3) e usar os números atuais; insight central "majoritário não erra, desiste cedo" continua válido (124/239 = 51,9%).
3. **Ponto exato de inserção:** linhas **243-245** do `apresentacao/index.html`; entre `</section>` do MARKER-01 (linha 243) e o comentário `<!-- ============ SLIDE · O que o Code-DKT olha ... -->` (linha 245). Estado final: 20 sections (16 prévios + 4 novos), `#/0` a `#/19`; slide-code passa de `#/11` para `#/15`.
4. **MARKER-02 = 4 deltas mecânicos vs MARKER-01 HEAD (não 3 como CONTEXT sugere):** pill 2 sai de `--running` (não `--pending`) → `--done`; pill 3 sai de `--pending` → `--running`; classe `--phase1` → `--phase2`; comentário "fase 1 concluida" → "fase 2 concluida". Markup completo em §5.3; zero CSS novo (D-67d).
5. **Phrasing literal Shi 2022 §4.1/§4.2 confirmado:** "410 students", "split with a ratio of 4:1", "we used the last 50 submissions" — todos lidos diretamente na página 5 do PDF. Paráfrase EDA-02 em §1.2.
6. **Templates EDA-01 comparados (3 opções):** Template B `<table class="eda-grid">` recomendado por coerência ABNT (borda fina 1,5px preta, sem radius), leitura comparativa fácil, ~14 linhas CSS novo.
7. **PNG scatter PCA não existe pronto; geração via `scripts/build_eda_pca_scatter.py`:** snippet standalone (50 linhas Python) com SEED=42; paleta UniFacens (`#2667FF` / `#F2A516` / `#D7191C`); print do resumo numérico para validação cruzada.
8. **3 variantes de cabeçalho por slide EDA com avaliação:** EDA-01 recomendo `> como navegamos o csedm`; EDA-02 recomendo `> aproximação ao protocolo`; EDA-03 recomendo `> três jeitos de aprender`. Todas justificadas em §7.

### File Created
`.planning/phases/03-eda-e-pr-processamento-fase-2-edm/03-RESEARCH.md`

### Confidence Assessment

| Area | Level | Reason |
|------|-------|--------|
| Phrasing do paper Shi §4.1/§4.2 | HIGH | Página 5 do PDF lida literalmente; 3 trechos diretos extraídos |
| Números do dataset (MainTable) | HIGH | pandas rodado; cell 51 do notebook confirma cross-ref |
| K-Means cell 46 (estado atual) | HIGH | Outputs preservados no ipynb raw lidos diretamente; reconciliação documentada |
| Ponto de inserção DOM (linhas 243-245) | HIGH | grep no index.html confirmou boundaries |
| Deltas MARKER-01 → MARKER-02 | HIGH | Markup HEAD lido literalmente; CSS validado |
| Template B (`<table>`) para EDA-01 | MEDIUM | Comparação justificada; reviewer pode preferir A ou C no checkpoint |
| PNG via script standalone | MEDIUM | Código completo e replicável; não rodado nesta pesquisa |
| Phrasing-alvo dos 3 EDAs | MEDIUM | Variantes oferecidas; checkpoint humano polishea |
| Variantes de cabeçalho | MEDIUM | D-63 aberto por design; 3 opções por slide com avaliação |

### Open Questions

Ver §"Open Questions" deste RESEARCH (6 pontos, todos com recomendação não-bloqueante). Principais: (1) commit único para EDA-03 + PNG; (2) atualizar §Inventário do STYLE.md no fim da fase; (3) cabeçalho EDA-03 `> perfis dos alunos` vs `> três jeitos de aprender`.

### Ready for Planning

Research completo. Planner pode criar PLAN.md com:
- 4 plans (1 por slide), ordem recomendada MARKER-02 → EDA-02 → EDA-01 → EDA-03
- Markup pronto para reuso (§5.3 MARKER-02; §7 EDA-* com 3 variantes de cabeçalho cada)
- CSS pronto (§4.2 `.eda-grid`; §6.5 `.eda-fig` + `.eda-insight`)
- Script de geração do PNG (§6.3 `scripts/build_eda_pca_scatter.py`)
- Phrasing-alvo com variantes para os 3 EDAs (§7)
- Checks visuais por slide (§5.5 MARKER-02; gates EDA-* em §1.2, §2.4, §3.3, §7)
- Pitfalls catalogados (§Common Pitfalls)
- Diff opcional do STYLE.md (§8)
