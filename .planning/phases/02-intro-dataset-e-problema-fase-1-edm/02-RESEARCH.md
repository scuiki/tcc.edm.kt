# Phase 2: Intro, Dataset e Problema (Fase 1 EDM) - Research

**Researched:** 2026-05-27
**Domain:** Slides reveal.js (HTML/CSS) + fidelidade de citação a papers de referência (Code-DKT, ProgSnap2)
**Confidence:** HIGH (todas as fontes primárias lidas; números do dataset rodados; markup-alvo inspecionado)

## Summary

A Fase 2 insere 4 sections novos em `apresentacao/index.html` no único intervalo disponível entre os slides 6 (Yağcı, `> da edm ao knowledge tracing`) e 7 (slide-code, `> o que o code-dkt olha`). Três dos slides (INTRO-01, INTRO-03a, INTRO-03b) reutilizam o template `.slide-related` e a classe `.deck-topic` já consolidados na fase 1; o quarto (MARKER-01) introduz um componente novo `.slide-marker` que será template para MARKER-02/03/04 nas fases seguintes. A pesquisa confirmou (a) phrasing exato de Shi et al. (2022) que sustenta a paráfrase indireta de INTRO-03a/b, (b) phrasing exato de Price (2020) que sustenta a citação parentética de INTRO-01, (c) números do MainTable.csv onde o evento difere do estimado em CONTEXT, (d) ponto de inserção exato no DOM (entre linhas 147 e 149), (e) sentença obsoleta no STYLE.md (linha 129), e (f) inventário de classes Fonte: existentes para decidir reuso vs novas classes.

**Primary recommendation:** Reutilizar `.slide-related` + `.rel-lead` + `.rel-cite` para INTRO-01/03a/03b (mesmo template dos slides Martins p1, Zorić fundido, Yağcı fundido); criar componente novo `.slide-marker` reaproveitando a estética de `.bridge-seq` (caixas com borda preta 1.5px, fundo branco, setas pretas) e adicionando modificadores `--done`/`--pending` para o checkmark e cor azul UniFacens. Implementar CSS no `theme-unifacens.css` agora (D-41) para que MARKER-02/03/04 das fases 3-5 só troquem qual caixa fica preenchida.

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-31:** Os 4 slides entram após o slide 6 (Yağcí, `> da edm ao knowledge tracing`) e antes do atual slide 7 (`slide-code`, futuro MODEL-03). Ordem dentro do bloco: INTRO-01 → INTRO-03a → INTRO-03b → MARKER-01.
- **D-32:** Frase obsoleta em `apresentacao/STYLE.md` §"Gaps reservados" ("Após `> introdução` (slide 3): INTRO-01...") deve ser corrigida nesta fase. A posição correta é após Yağcı (slide 6).
- **D-33:** Justificativa narrativa: Yağcı lança "acompanhar o conhecimento ao longo do tempo, a cada nova tentativa"; INTRO-01 entra dizendo "o dataset que usamos preserva exatamente isso"; INTRO-03a/b: "mas o KT clássico ainda ignora a estrutura do código"; MARKER-01 fecha a Fase 1 EDM.
- **D-34a (INTRO-01):** cabeçalho travado `> o dataset csedm`.
- **D-34b (INTRO-03a, diagnóstico):** cabeçalho travado `> o problema do kt binário`.
- **D-34c (INTRO-03b, consequência):** cabeçalho travado `> sinal pedagógico perdido`.
- **D-34d (MARKER-01):** sem `.deck-topic` no padrão `> [seção]`; o próprio progress bar é o cabeçalho visual.
- **D-35 (INTRO-01):** voz primeira pessoa do plural; propriedade-chave (preservar todas as tentativas) aparece como justificativa; rodapé `Fonte: Price (2020); CSEDM 2021.`
- **D-36 (INTRO-03a):** paráfrase indireta de Shi et al. (2022), centrada em "BKT e DKT usam apenas acerto/erro e ignoram a estrutura do código"; voz própria; **proibida** citação direta literal. Rodapé `Fonte: Shi et al. (2022).`
- **D-37 (INTRO-03b):** paráfrase autoral; sem citação direta. Rodapé `Fonte: adaptado de Shi et al. (2022).`
- **D-38:** números brutos do MainTable Spring 2019 (sem filtro Shi). Validar com `pd.read_csv`. ⚠️ **Ver §2 deste RESEARCH para os números reais confirmados — a estimativa "~360k eventos" do CONTEXT está incorreta.**
- **D-38b:** Phase 3 (EDA-02) deve fazer ponte explícita "do CSEDM bruto (413) seguimos o protocolo de Shi et al. (2022) com filtro `min_attempts >= 3` → 410 estudantes". Não citar no INTRO-01.
- **D-38c:** Não citar filtro/protocolo Shi no INTRO-01; é função da EDA-02 (fase 3).
- **D-39 (estética MARKER-01):** progress bar horizontal com 4 etapas em linha, primeira preenchida em `--uni-blue` (#2667FF) com `✓`, demais em outline cinza/`#5b6472`. Caixas conectadas por seta `→`, mesma estética do `.bridge-seq` do slide Yağcı.
- **D-40 (terminologia):** texto literal das 4 caixas, na ordem: `Definição do Problema` (✓), `Preparação dos Dados`, `Modelagem e Avaliação`, `Implantação`. Espelha ROADMAP e STYLE.md.
- **D-41 (reuso):** MARKER-02/03/04 (fases 3-5) DEVEM usar o mesmo componente `.slide-marker`. Classe `.marker-step--done` para preenchida, `.marker-step--pending` para demais. CSS no `theme-unifacens.css` agora.
- **D-42 (cabeçalho):** padrão `<p class="deck-topic"><span class="ps1">&gt;</span>[seção]<span class="caret blink"></span></p>` para INTRO-01/03a/03b; MARKER-01 sem (D-34d).
- **D-43 (voz):** paráfrase indireta com autor parentético padrão; citação direta literal **proibida** nos 3 slides INTRO.
- **D-44 (sem em-dash):** previews em CONTEXT contêm em-dash (ex.: "CSEDM — curso..."); executor DEVE converter antes de gravar HTML. Vinculante.
- **D-45 (Fonte:):** Arial 17-18px, cor `#5b6472`, no rodapé de cada slide; formato STYLE.md.
- **D-46 (estrangeirismos):** `*knowledge tracing*` em itálico minúsculas; nomes de modelos (BKT, DKT, Code-DKT) preservados; ProgSnap2 e CSEDM como nomes próprios (não itálico).
- **D-47 (validação visual):** ao fim da fase, validar do `#/0` ao `#/15` no browser (`cd apresentacao && python3 -m http.server 8000`).

### Claude's Discretion

- Ordem de implementação dos 4 slides (sugestão neutra: MARKER-01 primeiro para travar `.slide-marker`, depois INTRO-01, INTRO-03a, INTRO-03b).
- Granularidade de commits: 4 commits (1/slide) vs 3 commits (INTRO-01 / INTRO-03 / MARKER-01). Convenção do projeto sugere atômico por slide → 4 commits.
- Microcópia exata de INTRO-03b ("quase certo / completamente errado" ou variantes equivalentes; manter o argumento).
- Inset visual / diagrama em INTRO-03a: default sem; executor pode inserir se ficar visualmente vazio.
- Largura/tipografia exata do progress bar dentro do que D-39/D-40 travam.
- Atualização do STYLE.md (D-32): plano decide se faz junto com último slide ou commit separado.
- Nomenclatura das classes CSS dos slides INTRO: padronizar como `.slide-intro` único com modificadores OU reutilizar `.slide-related` como-é (decisão de plan-phase).

### Deferred Ideas (OUT OF SCOPE)

- **Inset visual ou diagrama** dentro de INTRO-03a/b (ex.: 3 caixas `código → score 0/1 → KT clássico`): default **fora**; pode entrar oportunista durante execução, sem virar requirement próprio.
- **Snippet de código real do CSEDM no INTRO-03**: defer; argumento numérico já está em CLOSE-01/02, exemplos de código no slide-code (MODEL-03 da fase 4).
- **Atualização do REQUIREMENTS.md** para INTRO-03 virar 2 sub-slides: decisão do plan-phase; "1 a 2 slides" do REQUIREMENTS.md já previu.
- **Uso do `.slide-marker` em MARKER-02/03/04**: implementação do componente aqui (D-41); uso fica para fases 3-5.
- **Bridge textual 413 (bruto) → 410 (Shi)**: defer para EDA-02 (fase 3).
- **Cronologia BKT→DKT→Code-DKT** com Corbett & Anderson parentético: fase 4 (MODEL-01).
- **Reordenação do slide-code antes de slide-kcfig**: fase 4 (MODEL-01/04). Esta fase 2 não toca.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INTRO-01 | Slide "nosso dataset": CSEDM (CS1 Java, coleta 2019, competição CSEDM 2021) armazenado em ProgSnap2 (Price, 2020); preserva múltiplas tentativas; voz primeira pessoa do plural | §1 phrasing Price (2020) confirmado; §2 números do dataset validados via pandas; §6 reuso de `.rel-cite` recomendado; §4 ponto de inserção definido |
| INTRO-03 | Slide(s) Shi e o problema: BKT/DKT usam acerto/erro e ignoram a estrutura do código; paráfrase indireta; sem Code-DKT | §1 phrasing Shi et al. (2022) confirmado com 5 trechos literais (Abstract + §2.1) que sustentam o argumento; phrasing-alvo de INTRO-03a/b em §1.3 |
| MARKER-01 | Progress bar 4 fases EDM com primeira marcada como "Definição do Problema ✓" | §3 CSS rascunho com estética `.bridge-seq` estendida; §4 ponto de inserção define `#/10` após inserção; §7 checks visuais |

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Markup dos 4 slides | `apresentacao/index.html` (única fonte) | — | Reveal.js força layout no `<div>` interno; sections novas entram literais |
| Estilização visual reutilizável | `apresentacao/assets/theme-unifacens.css` | — | Componente `.slide-marker` precisa estar disponível para fases 3-5 (D-41) |
| Texto travado por requirement | CONTEXT (D-34a-d, D-38, D-40) | RESEARCH §1 (phrasing alvo) | Cabeçalhos e texto-âncora fixados; phrasing fino fica para o plano com base no RESEARCH |
| Validação visual | Browser (D-47) | — | Sem build system; sem testes automatizados; checkpoint humano fim-a-fim |

---

## §1 Phrasing dos papers (Shi 2022, Price 2020)

### 1.1 Code-DKT — Shi, Mao, Akram, Lytinen e Heffernan (2022)

`docs/Code-DKT.pdf`, EDM 2022, pp. 50-61. Lidas: §Abstract, §1 Introduction, §2 Related Work, §2.1 Knowledge Tracing.

**Citação completa para "Fonte:" em INTRO-03a/b:**
`Fonte: Shi et al. (2022).` (D-36)
`Fonte: adaptado de Shi et al. (2022).` (D-37)

**Trechos literais que sustentam a paráfrase autoral (CITED: docs/Code-DKT.pdf):**

1. **Abstract, p. 50 (conceito central):**
   > "Knowledge tracing (KT) models are a popular approach for predicting students' future performance at practice problems using their prior attempts. Though many innovations have been made in KT, most models including the state-of-the-art Deep Knowledge Tracing (DKT) mainly leverage each student's response either as correct or incorrect, **ignoring its content**."

2. **Abstract, p. 50 (motivação pedagógica — esta é a base direta de INTRO-03b):**
   > "In these domains, correctness may not provide enough information about student modeling, varying significantly in the reasons both for incorrectness and correctness. **In programming, for example, one incorrect attempt may have a minor syntax error while another includes a clear misconception. Similarly, two different correct answers could reveal dramatically different levels of concept mastery depending on their conciseness and the concepts used. Most KT models would treat all correct and all incorrect attempts identically.**"

3. **§1 Introduction, p. 50 (col. dir., 2º parágrafo — argumento de "ignora conteúdo"):**
   > "The simplest version of the KT problem uses only the sequence of: 1) which problems the student has attempted, and 2) whether or not each attempt was correct. While this makes KT models widely applicable across domains, this also omits a potential wealth of information about how the student attempted each problem."

4. **§2.1 Related Work — Knowledge Tracing, p. 51 (col. esq.):**
   > "the datasets used generally only indicate whether a student's attempt was correct, but not the content of a student's answer or their process for achieving it, **and the models therefore do not use this information**."

5. **§2.1 Related Work, p. 51 (col. dir.):**
   > "However, these models only use problem information, but **no information about the students' answer beyond binary correctness information**. This suggests an opportunity to create improved, domain-specific KT models in areas such as programming."

**Atenção factual (HIGH):**
- Os autores nomeiam BKT e DKT explicitamente como o "estado-da-arte" do KT clássico (Abstract: "Bayesian Knowledge Tracing (BKT) and Deep Knowledge Tracing (DKT)"). Logo, a paráfrase do INTRO-03a — "modelos clássicos de *knowledge tracing*, como BKT e DKT, usam apenas acerto/erro e ignoram a estrutura do código produzido pelo estudante" — é **fiel** ao paper e pode ser travada como-é no slide.
- O paper usa "content" (conteúdo) e "structural information" (informação estrutural). Em PT-BR, "estrutura do código" cobre as duas. Mantido.
- O paper NÃO usa a frase "quase certo / completamente errado" literalmente. O equivalente é "varying significantly in the reasons both for incorrectness and correctness" + "one incorrect attempt may have a minor syntax error while another includes a clear misconception". A paráfrase de INTRO-03b é leitura autoral — por isso D-37 usa `Fonte: adaptado de Shi et al. (2022).` Coerente.
- INTRO-03b NÃO deve transbordar para "Code-DKT resolve isso"; isso é fase 4 (MODEL-01/04). O slide fecha no diagnóstico do problema, deixando a transição narrativa para o MARKER-01.

**Phrasing-alvo recomendado para o plano (a polir):**

- **INTRO-03a (corpo):**
  > "Shi et al. (2022) apontam que modelos clássicos de *knowledge tracing*, como BKT e DKT, usam apenas a informação de **acerto ou erro** e ignoram a estrutura do código produzido pelo estudante."

  Reforço opcional (segunda sentença, mantém voz autoral): "Toda a riqueza do código submetido fica fora do modelo."

- **INTRO-03b (corpo):**
  > "Como consequência, esses modelos tratam de forma idêntica uma submissão **quase correta** e uma **completamente errada**; o sinal pedagógico estrutural se perde no processo."

  Variantes equivalentes aceitas pelo CONTEXT: "acerto parcial vs erro total", "sinal de progresso vs sinal de erro". Manter o argumento.

### 1.2 ProgSnap2 — Price et al. (2020)

`docs/ProgSnap2.pdf`, ITiCSE '20 (junho 2020), pp. 356-362. Lidas: §Abstract, §1 Introduction, §2 The ProgSnap2 Specification, §2.1 Main Event Table.

**Citação completa para "Fonte:" em INTRO-01 (D-35):**
`Fonte: Price (2020); CSEDM 2021.`

⚠️ **Ano confirmado: 2020** (publicado em 15 de junho de 2020 no ITiCSE '20 Proceedings, página de copyright e DOI registram `2020`). HIGH confidence. Não é 2019 (formato antecessor "ProgSnap original" estava em uso desde antes) nem 2021 (CSEDM 2021 é a competição que usou o formato, não a publicação do formato).

**Autoria parentética no slide:**
- O paper tem 12 autores; em ABNT brasileira para 3+ autores em parênteses usa-se `(Sobrenome do primeiro, ano)` ou `(Sobrenome do primeiro et al., ano)`. Convenção do projeto (já aplicada em Shi et al., 2022 e Martins et al., 2024): usar `(Price, 2020)` na primeira menção parentética e `(Price et al., 2020)` se quiser ser mais formal. CONTEXT trava `(Price, 2020)` (D-35); mantido.
- Primeiro autor: **Thomas W. Price** (NC State University). "Price" sozinho é o sobrenome correto.

**Trechos literais que sustentam INTRO-01 (CITED: docs/ProgSnap2.pdf):**

1. **Abstract, p. 356:**
   > "ProgSnap2, a standardized format for logging programming process data. ProgSnap2 is a tool for computing education researchers, with the goal of enabling collaboration by helping them to collect and share data, analysis code, and data-driven tools to support students."

2. **§1 Introduction, p. 356:**
   > "In this paper, we present ProgSnap2, a standardized format for logging programming process data. Researchers can use ProgSnap2 as a tool to assist in conducting computing education research, as it is specifically designed to support researchers in collecting, sharing and analyzing programming process data."

3. **§2 The ProgSnap2 Specification, p. 357:**
   > "A ProgSnap2 dataset consists of logs and relevant data that capture how users interacted with a programming environment. A dataset includes a **main event table**, a metadata table and optional link tables to reference outside resources, all represented as CSV files. A dataset also contains a **code repository** containing sequential snapshots of students' code and optional auxiliary resources."

4. **§2.1 Main Event Table, p. 358 (a propriedade "múltiplas tentativas" sai diretamente daqui):**
   > "The main event table represents a collection of all events that took place in the programming environment. These events can represent both fine-grained interactions, such as individual keystrokes, and high-level actions, such as **entire problem attempts**, depending on the granularity of the logging system. Each row in the table represents one event, and each column represents an event property. All events have an EventType column, and ProgSnap2 provides over 20 predefined EventTypes, listed in Figure 1 (e.g. File.Edit, Compile.Error, Run.Program)."

5. **§2.1, p. 358 (colunas obrigatórias confirmam SubjectID + CodeStateID):**
   > "ProgSnap2 defines a small set of mandatory columns: 1) EventType: a value indicating the type of event; 2) EventID: the unique ID of the event; 3) **SubjectID**: the ID of the human subject (or group) associated with the event; 4) ToolInstances: the names and versions of tools (e.g. IDE, compiler) associated with the event; and 5) **CodeStateID**: an ID for a snapshot of the source code when the event occurred."

**Atenção factual (HIGH):**
- O paper **NÃO menciona CSEDM nominalmente**. O paper apresenta cinco datasets ProgSnap2 como case study (de Java, Python, Snap), nenhum é CSEDM. **Quem batiza o CSEDM como dataset ProgSnap2 é a documentação do dataset CSEDM em si** e o uso por Shi et al. (2022). A frase "CSEDM armazenado em ProgSnap2 (Price, 2020)" é factualmente correta porque (a) o formato dos arquivos do CSEDM (`MainTable.csv` com colunas `EventType`, `SubjectID`, `CodeStateID`, etc.) **é** ProgSnap2; (b) a competição CSEDM 2021 publicou o dataset explicitamente nesse formato. Não há overclaim.
- O paper NÃO usa literalmente a frase "preserva múltiplas tentativas". A propriedade que CSEDM herda (manter cada `Run.Program` de cada estudante como linha distinta) sai da arquitetura do `main event table` + `SubjectID` + `EventType=Run.Program` + sequência temporal. Phrasing autoral seguro para INTRO-01: "formato que registra cada evento de programação como uma linha (edição, compilação, execução), preservando o histórico completo de tentativas de cada estudante". Conteúdo verdadeiro, paráfrase legítima.
- CSEDM 2021 = "CSEDM Data Challenge 2021" (memória `project_split_discovery` confirma; é uma competição em cima do mesmo dataset Spring 2019).

**Phrasing-alvo recomendado para o plano (a polir):**

- **INTRO-01 (corpo):**
  > "Nosso dataset é o **CSEDM** (curso introdutório CS1 em Java, coleta de 2019, divulgado na competição CSEDM 2021), armazenado em **ProgSnap2** (Price, 2020), formato que registra cada evento de programação do estudante (edição, compilação, execução), preservando o histórico completo das tentativas a cada problema."

  Logo abaixo do parágrafo introdutório, 3 números do dataset (ver §2). Sem em-dash em nenhum momento (D-44).

### 1.3 Resumo de phrasing para travar no plano

| Slide | Cabeçalho `> [seção]` | Voz | Citação parentética | Rodapé "Fonte:" |
|---|---|---|---|---|
| INTRO-01 | `> o dataset csedm` | 1ª pessoa do plural ("Nosso dataset é...") | `(Price, 2020)` parentético | `Fonte: Price (2020); CSEDM 2021.` |
| INTRO-03a | `> o problema do kt binário` | paráfrase indireta, autor prominente ("Shi et al. (2022) apontam que...") | — (autor prominente, sem parênteses no corpo) | `Fonte: Shi et al. (2022).` |
| INTRO-03b | `> sinal pedagógico perdido` | paráfrase autoral, consequência | — | `Fonte: adaptado de Shi et al. (2022).` |
| MARKER-01 | (sem `.deck-topic`) | nenhum corpo textual além do progress bar | — | `Fonte: adaptado de Zorić (2020).` (sugestão; ver §6) |

---

## §2 Números do dataset (D-38) — VERIFIED

Comando rodado (output literal capturado):

```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/CSEDM/MainTable.csv'); \
print('SubjectID:', df['SubjectID'].nunique()); \
print('ProblemID:', df['ProblemID'].nunique()); \
print('Events:', len(df))"
```

Output:
```
SubjectID: 413
ProblemID: 50
Events: 201570
```

[VERIFIED: pandas em data/CSEDM/MainTable.csv, 2026-05-27]

| Número | D-38 (CONTEXT estimou) | Real (VERIFICADO) | Diferença |
|---|---|---|---|
| Estudantes únicos | 413 | **413** | ✓ |
| Problemas únicos | 50 | **50** | ✓ |
| Total de eventos | ~360k | **201.570** | ⚠️ estimativa ~80% acima do real |

**⚠️ Erro corretivo em D-38:** O CONTEXT estima "~360k eventos"; a contagem real é **201.570**. Provável causa da estimativa errada: confusão com a contagem agregada de eventos `Run.Program` + `Compile` + `Compile.Error` em discussões anteriores (CLAUDE.md menciona "Compile.Error: 109.020 eventos (30.27% do total)" — 109020/0.3027 ≈ 360k seria uma soma diferente, talvez de outro arquivo ou contagem feita em outra timeline). O número canônico de `len(MainTable.csv)` é 201.570 e este é o que vale para o slide.

**Formato pt-BR recomendado (3 opções, recomendação destacada):**

| Opção | Texto no slide | Tradeoff |
|---|---|---|
| A (preciso, separador) | `413 estudantes · 50 problemas · 201.570 eventos` | Transparente, mas "201.570" tem 7 caracteres e pode parecer "muito numérico" para um slide de 20s |
| B (arredondado) | `413 estudantes · 50 problemas · ~200 mil eventos` | Mais legível; perde precisão; "mil" em pt-BR é ABNT-friendly |
| **C (recomendada)** | `413 estudantes · 50 problemas · 201 mil eventos` | Arredondamento natural pt-BR; mantém a ordem de grandeza correta; "201 mil" lê como "duzentos e um mil" |

**Recomendação:** opção **C** (`201 mil eventos`). Razões:
1. Apresentação de defesa: o número exato 201.570 não acrescenta nada na fala de 20s; o ouvinte memoriza "ordem de grandeza ~200 mil".
2. Convenção pt-BR: "201 mil" é mais natural que "201.570" em fala/legenda.
3. Coerência com fase 3 (EDA-01): EDA-01 vai mostrar histogramas e o número exato 201.570 aparecerá lá (ou em gráfico, ou em legenda); INTRO-01 não precisa antecipar.

Se preferir precisão absoluta (opção A), usar `201.570` com ponto como separador de milhar (não vírgula; ABNT pt-BR usa ponto para milhar e vírgula para decimal). NÃO usar `360k`, `360.000` ou `~360k`.

**Bloco visual sugerido no slide INTRO-01** (formato a polir no plano; D-38 não trava CSS):

```html
<ul class="intro-stats">
  <li><span class="stat-num">413</span> <span class="stat-lbl">estudantes</span></li>
  <li><span class="stat-num">50</span> <span class="stat-lbl">problemas</span></li>
  <li><span class="stat-num">201 mil</span> <span class="stat-lbl">eventos</span></li>
</ul>
```

ou inline em parágrafo (`.rel-lead`): "413 estudantes, 50 problemas, 201 mil eventos". Decisão de markup fica para o plano; ambos servem o requirement.

---

## §3 Padrão visual `.slide-marker` reutilizável (CSS rascunho)

D-39, D-40, D-41 travam: 4 caixas em linha, primeira preenchida em `--uni-blue` com `✓`, demais outline cinza `#5b6472`, conectadas por `→`, **mesma estética** do `.bridge-seq` do slide Yağcı.

### 3.1 Inventário do `.bridge-seq` existente (referência)

Localização: `theme-unifacens.css` linhas 197-210. CSS literal:

```css
.slide-bridge .bridge-seq {
  display: flex; align-items: stretch; justify-content: center; gap: 0;
  margin-top: 38px; font-family: Arial, "Helvetica Neue", sans-serif;
}
.slide-bridge .bridge-seq .step {
  flex: 1 1 0; text-align: center; font-size: 19px; font-weight: 700; color: #111;
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0; padding: 16px 14px;
  display: flex; align-items: center; justify-content: center;
}
.slide-bridge .bridge-seq .arr {
  flex: none; align-self: center; color: #1f1f1f; font-size: 26px; font-weight: 700; padding: 0 16px;
}
```

Markup atual (linha 143 do `index.html`, slide Yağcı):
```html
<p class="bridge-seq">
  <span class="step">mineração de dados educacionais</span>
  <span class="arr">&rarr;</span>
  <span class="step">predição de desempenho</span>
  <span class="arr">&rarr;</span>
  <span class="step"><i>knowledge tracing</i></span>
</p>
```

Características que `.slide-marker` deve herdar:
- Caixas `flex: 1 1 0` (largura igual entre todas)
- Borda `1.5px solid #1f1f1f`, sem border-radius (estilo ABNT Word)
- Fundo branco
- Setas `→` em preto `#1f1f1f`
- Fonte Arial bold

Diferença vs `.bridge-seq`: o `.slide-marker` precisa de **4 caixas** (vs 3) e o estado `--done` precisa de azul UniFacens + `✓`.

### 3.2 CSS rascunho proposto (a refinar no plano)

```css
/* ===========================================================================
   SLIDE · Marker · progress bar das 4 fases EDM
   Estende a estética do .bridge-seq (caixas pretas, fundo branco, setas pretas)
   acrescentando estados --done (azul UniFacens + checkmark) e --pending
   (outline cinza). Reusado por MARKER-01..04 (fases 2-5).
   =========================================================================== */
.slide-marker {
  display: flex; flex-direction: column; background: var(--uni-light);
  padding: 80px 64px 40px; --caret-color: var(--uni-blue);
  font-family: Arial, "Helvetica Neue", sans-serif;
  align-items: center; justify-content: center;
}
.slide-marker .wm { position: absolute; top: 26px; right: 34px; width: 58px; color: var(--uni-gray); opacity: .9; pointer-events: none; }

.marker-track {
  display: flex; align-items: stretch; justify-content: center; gap: 0;
  width: 100%; max-width: 1120px;
}
.marker-step {
  flex: 1 1 0; text-align: center; font-size: 19px; font-weight: 700;
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0;
  padding: 28px 12px; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 8px; min-height: 110px; line-height: 1.25;
}
.marker-step__mark {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 50%;
  font-family: var(--mono); font-size: 18px; line-height: 1; font-weight: 700;
}
.marker-step--done {
  background: var(--uni-blue); color: #fff; border-color: var(--uni-blue);
}
.marker-step--done .marker-step__mark {
  background: #fff; color: var(--uni-blue);
}
.marker-step--pending {
  background: #fff; color: #5b6472; border-color: #5b6472;
}
.marker-step--pending .marker-step__mark {
  border: 1.5px solid #5b6472; color: #5b6472;
}
.marker-arr {
  flex: none; align-self: center; color: #1f1f1f; font-size: 26px; font-weight: 700;
  padding: 0 14px;
}

/* rodapé Fonte: (centralizado, igual a .kcfig-fonte / .fig-fonte) */
.slide-marker .marker-fonte {
  margin-top: 36px; text-align: center;
  font-family: Arial, "Helvetica Neue", sans-serif; font-size: 18px; color: #5b6472;
}
```

### 3.3 Markup-alvo para o slide MARKER-01 (a refinar no plano)

```html
<!-- ============ SLIDE · MARKER · Definição do Problema concluída ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase1">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <div class="marker-track">
      <span class="marker-step marker-step--done">
        <span class="marker-step__mark">&check;</span>
        Definição do Problema
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">2</span>
        Preparação dos Dados
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">3</span>
        Modelagem e Avaliação
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">4</span>
        Implantação
      </span>
    </div>

    <p class="marker-fonte">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

### 3.4 Considerações de cabimento a 1280×720

Largura útil dentro de `.slide-marker` (padding 64px): ~1152px. Setas `→` (3 × 28px = 84px); restante para 4 caixas = ~1068px ÷ 4 = ~267px por caixa. Cada caixa precisa caber a string mais longa.

Strings literais por caixa (D-40):
- `Definição do Problema` — 20 caracteres
- `Preparação dos Dados` — 19 caracteres
- `Modelagem e Avaliação` — 21 caracteres
- `Implantação` — 11 caracteres

A 19px Arial bold, ~21 chars cabem confortavelmente em ~250-280px com padding lateral 12px. **Não deve precisar quebrar linha nem reduzir fonte.**

Riscos a verificar visualmente (D-47):
- Se "Modelagem e Avaliação" estourar uma única linha em alguma janela específica, usar quebra suave `<br>` ou reduzir font-size para 18px. Plano decide na hora.
- Se altura mínima 110px não acomodar o `marker-step__mark` (28px) + texto (2 linhas máx), ajustar `min-height` para 130-140px.

### 3.5 Reuso nas fases 3-5 (D-41)

Para MARKER-02 (fase 3, "Preparação dos Dados ✓"), basta:
- Caixa 1: trocar `marker-step--done` por `marker-step--done`, mas com `&check;` (sim, mantém)
- Caixa 2: `marker-step--done` (era pending)
- Caixas 3, 4: `marker-step--pending`
- Trocar classe modificadora do `<div>` raiz: `slide-marker--phase1` → `slide-marker--phase2`

Trivial. Componente cumpre D-41.

**Decisão de plano:** anotar nos CONTEXTs das fases 3-5 que `.slide-marker` já existe e como reutilizar.

---

## §4 Ponto exato de inserção no DOM (D-31)

### 4.1 Boundaries verificadas

Inspecionado `apresentacao/index.html` (468 linhas, HEAD em 2026-05-27).

| Slide | Comentário acima | `<section>` | `</section>` |
|---|---|---|---|
| 6 (Yağcı fundido, ÂNCORA SUPERIOR) | linha 134 | linha 135 | **linha 147** |
| 7 (slide-code, ÂNCORA INFERIOR) | linha 149 | linha 151 | linha 198 |

Entre linhas **147 e 149** existe linha em branco (148). É exatamente aí que os 4 novos sections entram.

### 4.2 Estado final esperado (ordem no `<div class="slides">`)

| `#` (0-based) | Slide | classe | cabeçalho |
|---|---|---|---|
| 0 | Capa | slide-cover-brand | (sem) |
| 1 | Título TCC | slide-title-tcc | (sem) |
| 2 | Agenda | slide-agenda | (sem temático) |
| 3 | Martins p1 | slide-related | `> introdução` |
| 4 | Zorić fundido | slide-related | `> mineração de dados educacionais` |
| 5 | Zorić p3 (4 fases) | slide-phases | `> as quatro fases da edm` |
| 6 | Yağcí fundido | slide-related slide-bridge | `> da edm ao knowledge tracing` |
| **7** | **INTRO-01 (NOVO)** | slide-related (ou .slide-intro) | `> o dataset csedm` |
| **8** | **INTRO-03a (NOVO)** | slide-related (ou .slide-intro) | `> o problema do kt binário` |
| **9** | **INTRO-03b (NOVO)** | slide-related (ou .slide-intro) | `> sinal pedagógico perdido` |
| **10** | **MARKER-01 (NOVO)** | slide-marker slide-marker--phase1 | (sem temático, progress bar é o visual) |
| 11 | slide-code (era 7) | slide-code | `> o que o code-dkt olha` |
| 12 | slide-kcfig (era 8) | slide-kcfig | `> kcs semânticos extraídos` |
| 13 | Martins p2 (era 9) | slide-problem | `> retomando o problema` |
| 14 | Martins p3 (era 10) | slide-problem | `> retomando o problema` |
| 15 | slide-fig (era 11) | slide-fig | `> evolução por dificuldade` |

Total: **16 sections** (12 prévios + 4 novos), conforme CONTEXT `<domain>`.

### 4.3 Comentários a inserir

Cada `<section>` nova precisa de comentário com o padrão existente `<!-- ============ SLIDE · descrição ============ -->`. Sugestão de redação (a refinar no plano):

```html
<!-- ============ SLIDE · INTRO-01 · O dataset CSEDM em ProgSnap2 (Price, 2020) ============ -->
<!-- ============ SLIDE · INTRO-03a · O problema do KT binário (Shi et al., 2022) ============ -->
<!-- ============ SLIDE · INTRO-03b · Sinal pedagógico perdido (adaptado de Shi et al., 2022) ============ -->
<!-- ============ SLIDE · MARKER · Definição do Problema concluída (Zorić, 2020) ============ -->
```

### 4.4 Notas de cuidado

- Linhas 147-149 são EOL Unix; preservar (não introduzir CRLF).
- Indentação: 6 espaços para o `<section>` raiz (consistente com sections existentes).
- Marca d'água Facens `<svg class="wm">` em TODOS os 4 sections novos (D-37 do CONTEXT da fase 1 confirma padrão; MARKER-01 também deve ter — não é "metaslide" puro, ainda é conteúdo).

---

## §5 Atualização do STYLE.md (D-32)

### 5.1 Localização da frase obsoleta

Arquivo: `apresentacao/STYLE.md`
Seção: §"Gaps reservados para fases 2-5"
**Linha 129** (exato):

```
- Após `> introdução` (slide 3): INTRO-01 "nosso dataset" + INTRO-03 "Shi e o problema" + MARKER-01 (fase 2).
```

### 5.2 Sentença substituta (per <specifics> do CONTEXT)

```
- Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).
```

A linha 130 abaixo (`Após \`> da edm ao knowledge tracing\` (slide 6): EDA-01...`) **também precisa ser ajustada**, porque a posição mudou: EDA-* da fase 3 não pode entrar mais no mesmo gap; precisará entrar **antes do slide MARKER-01** (que vai virar o "fechador" da fase 1 EDM) ou **depois do MARKER-01** (que vira o "abridor" da fase 2 EDM).

Análise narrativa: MARKER-01 fecha "Definição do Problema ✓"; o slide seguinte na narrativa é EDA-01 ("Preparação dos Dados"). Portanto MARKER-01 fica **antes** de EDA-01. Sequência canônica das fases 2-3:

```
... (#6 Yağcı) → #7 INTRO-01 → #8 INTRO-03a → #9 INTRO-03b → #10 MARKER-01
   (fase 2 termina aqui) → #11 EDA-01 → #12 EDA-02 → #13 EDA-03 → #14 MARKER-02
   (fase 3 termina aqui) → #15 (era #7, slide-code) → ...
```

Sugestão de reescrita completa do bloco "Gaps reservados" (linhas 127-132 do STYLE.md):

```markdown
**Gaps reservados para fases 2-5:**

- Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).
- Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3).
- Antes do trio Martins+fig (entre slide-code/slide-kcfig e Martins p2): MODEL-01, MODEL-03, MODEL-04, MODEL-05 (fase 4); slide-code vira MODEL-03 reaproveitado; slide-kcfig é a saída do pipeline MODEL-05; slide-fig é o CLOSE-03.
- Após slide-fig: MARKER-03 (fim da fase 4 da EDM); depois TOOL-01, TOOL-03, MARKER-04, END-01 (fase 5); AGENDA-01 revisado.
```

**Discretion (gsd-planner):**
- Aplicar apenas a linha 129 (escopo mínimo D-32) OU reescrever o bloco inteiro (linhas 127-132) para refletir a estrutura nova. Recomendação: reescrever o bloco inteiro, é trivial e evita uma 2ª passada na fase 3.
- Commit: junto com último slide da fase ou commit separado `docs(style): atualizar gaps reservados pós-fase 2`. CONTEXT deixa livre.

### 5.3 Inventário "Inventário de slides (ordem atual, pós-fase 1)"

Tabela atual no STYLE.md (linhas 110-124) lista 12 slides (pós-fase 1). **Fora do escopo D-32**, mas se o plano resolver atualizar agora para refletir os 16 slides pós-fase 2, listar:

```markdown
## Inventário de slides (ordem atual, pós-fase 2)

| # | classe | cabeçalho | conteúdo |
|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho) | Abertura (logo + tagline) |
| 1 | slide-title-tcc | (sem cabeçalho) | Capa do TCC (autores em grafite) |
| 2 | slide-agenda | (sem cabeçalho temático) | Agenda |
| 3 | slide-related | `> introdução` | Recorte do problema (Martins, Marin e Alves, 2024) |
| 4 | slide-related | `> mineração de dados educacionais` | EDM como processo (Zorić, 2020), fundido p1+p2 |
| 5 | slide-phases | `> as quatro fases da edm` | As 4 fases (Zorić, 2020) |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | Ponte EDM para KT (Yağcı, 2022), fundido p1+p2 |
| **7** | **slide-related (ou slide-intro)** | **`> o dataset csedm`** | **CSEDM em ProgSnap2 (Price, 2020); 413/50/201 mil; voz primeira pessoa do plural** |
| **8** | **slide-related (ou slide-intro)** | **`> o problema do kt binário`** | **Shi et al. (2022), paráfrase indireta; BKT e DKT ignoram código** |
| **9** | **slide-related (ou slide-intro)** | **`> sinal pedagógico perdido`** | **Consequência pedagógica; adaptado de Shi et al. (2022)** |
| **10** | **slide-marker slide-marker--phase1** | **(sem; progress bar é o visual)** | **Fase 1 EDM concluída (Zorić, 2020)** |
| 11 | slide-code | `> o que o code-dkt olha` | (idem fase 1) |
| 12 | slide-kcfig | `> kcs semânticos extraídos` | (idem fase 1) |
| 13 | slide-problem | `> retomando o problema` | (idem fase 1) |
| 14 | slide-problem | `> retomando o problema` | (idem fase 1) |
| 15 | slide-fig | `> evolução por dificuldade` | (idem fase 1) |

**Estado do deck:** 16 slides após a fase 2 (era 12; 4 novos da fase 2 inseridos no gap após o Yağcí).
```

Discretion: plano decide se atualiza a tabela junto ou deixa para a transição da fase. D-32 só obriga linha 129.

---

## §6 Classes `.*-cite` / `.*-fonte` — decisão de reuso

### 6.1 Inventário de classes existentes (verified via grep)

| Classe | Localização CSS | Template host | Estilo |
|---|---|---|---|
| `.rel-cite` | linha 182 | `.slide-related` | `margin-top: auto`, Arial 18px, `#5b6472`, esquerda |
| `.prob-cite` | linha 263 | `.slide-problem` | `margin-top: 26px`, Arial 18px, `#5b6472`, esquerda |
| `.phases-fonte` | linha 156 | `.slide-phases` | `margin-top: 10px`, Arial 18px, `#5b6472`, esquerda |
| `.kcfig-fonte` | linha 297-300 | `.slide-kcfig` | `margin-top: 6px; padding-top: 10px`, Arial 18px, `#5b6472`, **centralizada** |
| `.fig-fonte` | linha 319 | `.slide-fig` | `margin-top: 8px`, Arial 18px, `#5b6472`, **centralizada** |
| `.code-fonte` | linha 351 | `.slide-code` | `margin-top: auto; padding-top: 8px`, Arial 18px, `#5b6472`, **centralizada** |

**Padrão:** sempre Arial 18px cor `#5b6472`. Diferença é só (a) alinhamento (esquerda vs centralizada) e (b) `margin-top` (auto, 8px, 10px, 26px).

### 6.2 Decisão recomendada (com justificativa)

**INTRO-01, INTRO-03a, INTRO-03b: reutilizar `.rel-cite`** (Decisão recomendada HIGH).

Justificativa:
1. Os 3 slides INTRO usam o mesmo template visual dos slides pós-fase 1 que herdam `.slide-related` (Martins p1, Zorić fundido, Yağcí fundido). Mesma `.rel-lead` em parágrafos.
2. `.rel-cite` já tem `margin-top: auto` — empurra a citação para o rodapé do slide, comportamento desejado.
3. Não criar `.intro-cite` evita poluir o CSS com classe equivalente (só seria duplicação).
4. Coerência visual de toda a faixa do deck que apresenta literatura (slides 3-9 pós-fase 2 todos `.rel-cite`).

**MARKER-01: criar `.marker-fonte`** (Decisão recomendada HIGH).

Justificativa:
1. `.slide-marker` é template NOVO, não estende `.slide-related`.
2. O rodapé do MARKER-01 deve estar **centralizado** (alinha com o progress bar centralizado acima), consistente com `.kcfig-fonte`/`.fig-fonte`/`.code-fonte` (todos centrados, todos em slides cujo "centro de gravidade" é figura/diagrama).
3. Criar `.marker-fonte` (não reutilizar `.kcfig-fonte` ou `.fig-fonte`) mantém o template auto-contido (modular para MARKER-02/03/04).

**Aceitável (não preferido):** reutilizar `.fig-fonte` para o MARKER-01, considerando que ambos são "slides centrados em diagrama com rodapé centralizado". Reduz CSS em ~4 linhas. Trade-off: o `.slide-marker` fica acoplado ao `.slide-fig` na manutenção futura. **Não recomendo.**

### 6.3 Decisão deixada em aberto (Claude's Discretion)

Se o plan-phase decidir criar `.slide-intro` como classe própria (em vez de `.slide-related`), então deve criar também `.intro-cite` por coerência. Recomendação: ficar com `.slide-related` + `.rel-cite` (caminho mínimo, sem CSS novo) salvo se houver diferença visual real entre INTRO e os correlatos pós-fase 1. Como INTRO-01/03a/03b são essencialmente "slides correlatos com voz autoral", o template casa perfeitamente.

---

## §7 Validação visual (D-47)

### 7.1 URLs por slide após inserção

Comando para subir servidor:
```bash
cd apresentacao && python3 -m http.server 8000
```

URLs (0-based, conforme reveal.js `hash: true`):

| URL | Slide | Foco da inspeção |
|---|---|---|
| `http://127.0.0.1:8000/#/0` | Capa | inalterado |
| `http://127.0.0.1:8000/#/1` | Título TCC | inalterado |
| `http://127.0.0.1:8000/#/2` | Agenda | inalterado |
| `http://127.0.0.1:8000/#/3` | Martins p1 (`> introdução`) | inalterado |
| `http://127.0.0.1:8000/#/4` | Zorić fundido | inalterado |
| `http://127.0.0.1:8000/#/5` | 4 fases EDM | inalterado |
| `http://127.0.0.1:8000/#/6` | Yağcí fundido | inalterado |
| **`http://127.0.0.1:8000/#/7`** | **INTRO-01** | Cabeçalho `> o dataset csedm`; 3 números (413, 50, 201 mil); `(Price, 2020)` parentético; rodapé `Fonte: Price (2020); CSEDM 2021.`; voz "Nosso dataset é..." |
| **`http://127.0.0.1:8000/#/8`** | **INTRO-03a** | Cabeçalho `> o problema do kt binário`; paráfrase autor prominente "Shi et al. (2022) apontam..."; BKT + DKT mencionados; sem citação literal entre aspas; rodapé `Fonte: Shi et al. (2022).` |
| **`http://127.0.0.1:8000/#/9`** | **INTRO-03b** | Cabeçalho `> sinal pedagógico perdido`; paráfrase autoral consequencial; rodapé `Fonte: adaptado de Shi et al. (2022).` |
| **`http://127.0.0.1:8000/#/10`** | **MARKER-01** | Sem `.deck-topic`; progress bar com 4 caixas; caixa 1 em `--uni-blue` com `✓`; caixas 2-4 outline `#5b6472`; setas `→` pretas; rodapé `Fonte: adaptado de Zorić (2020).` |
| `http://127.0.0.1:8000/#/11` | slide-code (deslocado +4) | inalterado |
| `http://127.0.0.1:8000/#/12` | slide-kcfig | inalterado |
| `http://127.0.0.1:8000/#/13` | Martins p2 | inalterado |
| `http://127.0.0.1:8000/#/14` | Martins p3 | inalterado |
| `http://127.0.0.1:8000/#/15` | slide-fig | inalterado |

### 7.2 Checks visuais por slide

**Para os 3 slides INTRO (idênticos):**
- [ ] Cabeçalho `.deck-topic` presente, com `>` em azul UniFacens, caret piscando ao fim
- [ ] Sem em-dash (`—`) na prosa (D-44 vinculante)
- [ ] Sem citação direta literal entre aspas (D-43 vinculante)
- [ ] Termos estrangeiros em itálico minúsculas: `*knowledge tracing*` (D-46)
- [ ] Nomes próprios não-italizados: ProgSnap2, CSEDM, BKT, DKT, Code-DKT (D-46)
- [ ] Marca d'água Facens `<svg class="wm">` presente
- [ ] Rodapé `Fonte:` em Arial 17-18px cor `#5b6472`
- [ ] Layout 1280×720 sem overflow (texto não estoura para fora do slide)

**Para INTRO-01 (D-35, D-38):**
- [ ] Voz primeira pessoa do plural ("Nosso dataset...")
- [ ] 3 números visíveis: 413 estudantes, 50 problemas, 201 mil (ou 201.570) eventos
- [ ] Citação parentética `(Price, 2020)` no corpo (não autor prominente; é menção lateral)
- [ ] Rodapé com `CSEDM 2021` mencionado

**Para INTRO-03a (D-36):**
- [ ] Voz: paráfrase autor prominente ("Shi et al. (2022) apontam que...")
- [ ] BKT e DKT mencionados literalmente
- [ ] Frase central: "acerto ou erro" + "ignoram a estrutura do código"
- [ ] **Code-DKT NÃO mencionado** (gate forte: é fase 4)

**Para INTRO-03b (D-37):**
- [ ] Voz: paráfrase autoral consequencial ("Como consequência..." ou similar)
- [ ] Argumento "quase certo / completamente errado" ou equivalente do CONTEXT
- [ ] **Sem** citação parentética nova (Shi já foi citado no slide anterior)
- [ ] Rodapé "adaptado de" presente

**Para MARKER-01 (D-39, D-40, D-41):**
- [ ] Sem `.deck-topic` (D-34d)
- [ ] 4 caixas presentes, na ordem: "Definição do Problema" → "Preparação dos Dados" → "Modelagem e Avaliação" → "Implantação"
- [ ] Caixa 1 com fundo `--uni-blue` (#2667FF), texto branco, `✓`
- [ ] Caixas 2-4 com outline `#5b6472`, fundo branco, número 2/3/4 ou ícone neutro
- [ ] 3 setas `→` pretas entre as 4 caixas
- [ ] Marca d'água Facens presente
- [ ] Rodapé `Fonte:` presente e centralizado

### 7.3 Checks de navegação fim-a-fim (D-47)

- [ ] Navegação `#/0` → `#/15` sem erro de console (F12 do navegador)
- [ ] Transição visual em cada um dos 4 novos slides sem layout quebrado (sem texto cortado, caixas sem overflow)
- [ ] Caret piscando funciona nos 3 INTRO (`.caret.blink`)
- [ ] Marca d'água Facens visível nos 4 (top-right ~26px/34px)
- [ ] Hash atualizando na URL conforme navega
- [ ] Reveal.js `width: 1280, height: 720` respeitado (não houve override acidental)

### 7.4 Comando de servidor + atalhos

```bash
# Subir servidor (terminal 1)
cd /home/leokuntz/Documents/repositories/studies/tcc.edm.kt/apresentacao && python3 -m http.server 8000

# Abrir navegador no slide INTRO-01
firefox http://127.0.0.1:8000/#/7   # ou chrome / outro
```

**Atalho do reveal.js para validação rápida:**
- `Esc` ou `O`: visão geral em grade (todos os 16 slides visíveis ao mesmo tempo) — útil para checar overflow e layout
- `N` / `P` (ou setas): próximo / anterior
- `S`: notes view (sem speaker notes nesta apresentação; ignore)
- `B`: black-out (apaga tela; útil para ver letterbox)

⚠️ **Cache do http.server:** se o CSS for alterado, browser pode servir versão antiga. Conforme STYLE.md linha 154, **subir em outra porta** para forçar reload (`python3 -m http.server 8001`).

---

## Common Pitfalls

### Pitfall 1: Em-dash em previews do CONTEXT
**What goes wrong:** Os exemplos de phrasing dentro de CONTEXT.md contêm em-dash (`—`) que NÃO podem ser copiados literalmente para o HTML — viola D-44 e a memória `feedback_no_em_dashes` (vinculante).
**Why it happens:** Previews foram escritos para discussão humana, não para implementação. CONTEXT marca isso explicitamente em D-44 ("DEVEM ser convertidos pelo executor antes de gravar HTML").
**How to avoid:** Antes de cada `git add`, rodar `grep -n '—' apresentacao/index.html` e converter qualquer ocorrência nas 4 novas sections para vírgula, dois-pontos ou parênteses. Aplicar especificamente nos novos sections (não nos já existentes da fase 1, que estão limpos).
**Warning signs:** Se a preview do CONTEXT mostra `"CSEDM — curso introdutório..."`, o slide entregue deve ler `"CSEDM, curso introdutório..."` ou `"CSEDM (curso introdutório...)"`.

### Pitfall 2: Confundir 360k com 201.570 eventos
**What goes wrong:** D-38 do CONTEXT estima "~360k eventos". O número real do `len(MainTable.csv)` é **201.570** (verificado pela §2 deste research). Se o slide for gravado com "~360k", contradiz o dado.
**Why it happens:** Estimativas de discussão raramente são reverificadas; CLAUDE.md menciona "Compile.Error: 109.020 eventos (30.27% do total)" e 109020/0.3027 ≈ 360k pode ter sido confundido com a contagem agregada de outro arquivo ou recorte.
**How to avoid:** Plano deve incluir explicitamente uma sub-task "rodar `python3 -c \"import pandas...\"` e confirmar **201.570**". Recomendar formato pt-BR "201 mil eventos" (opção C do §2.2).
**Warning signs:** Slide entregue com "360k", "~360k" ou "360.000". Reabrir o RESEARCH §2.

### Pitfall 3: Code-DKT mencionado no INTRO-03
**What goes wrong:** O par INTRO-03a/b apresenta o **problema** que o KT clássico tem. Mencionar Code-DKT aqui rouba o palco do MODEL-01/04 da fase 4 (onde Code-DKT é apresentado como solução).
**Why it happens:** Tentação narrativa de "fechar a frase" introduzindo o modelo logo. Mas a estrutura da defesa exige problema → MARKER fase 1 ✓ → EDA (fase 2) → modelo (fase 3) → fechamento.
**How to avoid:** Verificar literalmente que a palavra "Code-DKT" não aparece nem em INTRO-03a nem em INTRO-03b. Os 2 slides terminam no DIAGNÓSTICO; a solução vem depois.
**Warning signs:** Frase tipo "Code-DKT resolve isso" ou "Shi propõe o Code-DKT para..." em qualquer um dos slides.

### Pitfall 4: ProgSnap2 introduzido outra vez nas fases 3-5
**What goes wrong:** ProgSnap2 é nominalmente único em INTRO-01 (Key Decision do PROJECT.md, 1ª rodada feedback). Se fases 3 (EDA-01) ou 5 (TOOL-01) repetirem "ProgSnap2", quebra a Key Decision.
**Why it happens:** Memória `feedback` não foi propagada para os 4 CONTEXTs das fases 3-5; cada planner pode esquecer.
**How to avoid:** Não é responsabilidade desta fase corrigir, mas o RESEARCH deve sinalizar para que os CONTEXTs das fases 3 e 5 sejam escritos com essa restrição em mente (já está no PROJECT.md, basta lembrar).
**Warning signs:** Em qualquer fase futura, slide com "ProgSnap2" no corpo (não no rodapé `Fonte:`) que não seja o INTRO-01.

### Pitfall 5: Citação direta literal escapar pela paráfrase
**What goes wrong:** D-43 proíbe citação direta literal nos 3 slides INTRO. Se o executor copiar uma frase entre aspas dos trechos literais do §1 deste RESEARCH (que são em inglês), viola D-43 e o ROADMAP.
**Why it happens:** Tentação de usar a frase mais "forte" do paper como gancho. Mas o tom de voz é autoral (D-25, D-43).
**How to avoid:** Os trechos no §1 deste RESEARCH são **referências de fidelidade**, não markup. O plano deve traduzir cada um em paráfrase pt-BR autoral. Especificamente: não usar `<blockquote class="rel-quote">` em nenhum dos 3 INTRO; texto corre em `<p class="rel-lead">`.
**Warning signs:** `grep -c 'rel-quote\|prob-quote' apresentacao/index.html` deveria retornar exatamente 2 (Martins p2 + Martins p3, que mantêm direta literal por D-28); se retornar 3+, alguém adicionou `<blockquote>` em um INTRO novo.

### Pitfall 6: Reveal.js display:block override
**What goes wrong:** Reveal.js força `display:block` na `<section>` ativa. Se o layout for posto direto na `<section>` (não no `<div class="deck-slide">` interno), flexbox quebra silenciosamente.
**Why it happens:** Padrão HTML ingênuo. Documentado em CONVENTIONS.md e theme-unifacens.css (linha 6-9): "Por isso TODO o layout fica num <div class=\"deck-slide\"> interno".
**How to avoid:** Markup dos 4 novos sections SEMPRE como `<section><div class="deck-slide slide-XYZ">...</div></section>`. Repetir o padrão dos 12 sections existentes.
**Warning signs:** Slide quebrando ao centralizar; flexbox sem efeito; texto sem espaçamento.

---

## Code Examples

### Exemplo 1: Markup `.slide-related` reutilizável (referência: slide 6 Yağcí, lines 134-147)

```html
<!-- ============ SLIDE · Da EDM ao knowledge tracing (Yağcı, 2022) — fusão p1+p2 ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>da edm ao knowledge tracing<span class="caret blink"></span></p>

    <p class="rel-lead">Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar alunos em risco. Nós seguimos o passo seguinte: em vez de uma previsão única ao fim do curso, <b>acompanhamos o conhecimento ao longo do tempo</b>, a cada nova tentativa, via <i>knowledge tracing</i>.</p>

    <p class="bridge-seq"><span class="step">mineração de dados educacionais</span><span class="arr">&rarr;</span><span class="step">predição de desempenho</span><span class="arr">&rarr;</span><span class="step"><i>knowledge tracing</i></span></p>

    <p class="rel-cite">Fonte: Yağcı (2022).</p>
  </div>
</section>
```

Comentários:
- `<svg class="wm">` é a marca d'água (sempre presente)
- `<p class="deck-topic">` é o cabeçalho `> [seção]` único (substituiu `.rel-kicker` + `<h2>` na fase 1)
- `<p class="rel-lead">` é o parágrafo de corpo (Arial 25px, justificado)
- `<p class="rel-cite">` é o rodapé `Fonte:` (Arial 18px, `#5b6472`)

Este markup é o template a ser **clonado e adaptado** para INTRO-01, INTRO-03a e INTRO-03b.

### Exemplo 2: Markup `.slide-marker` proposto (novo template; ver §3.3 para CSS)

```html
<!-- ============ SLIDE · MARKER · Definição do Problema concluída (Zorić, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase1">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <div class="marker-track">
      <span class="marker-step marker-step--done">
        <span class="marker-step__mark">&check;</span>
        Definição do Problema
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">2</span>
        Preparação dos Dados
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">3</span>
        Modelagem e Avaliação
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">4</span>
        Implantação
      </span>
    </div>

    <p class="marker-fonte">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

Notas:
- 4 `.marker-step` (não 3, diferente do `.bridge-seq` do Yağcí)
- 3 `.marker-arr` entre as caixas
- Modificadores: `--done` (caixa 1), `--pending` (caixas 2-4)
- Rodapé Fonte: usa `Zorić (2020)` porque foi quem definiu as 4 fases (slide #5 do deck). Se preferir, alternativa é "elaborado pelos autores, com base em Zorić (2020)" — plano decide.

---

## Don't Hand-Roll

| Problema | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Cabeçalho `> [seção]` | Inventar nova estrutura HTML | `<p class="deck-topic"><span class="ps1">&gt;</span>texto<span class="caret blink"></span></p>` | Padrão já consolidado em 6 slides pós-fase 1; consistência visual + CSS pronto (linha 42 do theme) |
| Rodapé Fonte: | Criar nova classe `.intro-fonte` | Reutilizar `.rel-cite` para INTRO-01/03a/03b | Mesma estilística (Arial 18px, `#5b6472`, `margin-top:auto`); evita poluir CSS |
| Citação parentética ABNT | Improvisar formato | Seguir convenção do projeto: `(Sobrenome, ano)` em paráfrase, `;` para 2 autores, `et al.` para 3+ | Manual MSGQ-21.01 + memória `reference_manual_citacoes`; já aplicado em 5 slides existentes |
| Sequência horizontal de caixas | Criar do zero | Estender `.bridge-seq` em `.slide-marker` | Estética ABNT (caixas borda 1.5px preta, sem radius, fundo branco, setas pretas) já validada visualmente |
| Marca d'água Facens | Reimplementar SVG | Reutilizar `<svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>` | Símbolo está definido uma vez (linhas 15-21 do index.html); `<use href="#sym"/>` referencia |
| Conversão de em-dash | Esquecer | `grep -n '—' apresentacao/index.html` antes de commit | Memória `feedback_no_em_dashes` vinculante |
| Verificação de números brutos do dataset | Citar de memória | Rodar `python3 -c "import pandas..."` (§2 deste RESEARCH) | Discutido em D-38; estimativa "~360k" estava errada |

**Key insight:** A fase 1 já travou o vocabulário de classes e o markup. A fase 2 deve **reutilizar agressivamente** e adicionar **um único novo template** (`.slide-marker`) que será reusado nas 3 fases seguintes. Cada nova classe CSS introduzida fora desse escopo é dívida técnica.

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|---|---|---|
| A1 | Convenção ABNT pt-BR: separador de milhar `.` (ponto), decimal `,` (vírgula); portanto "201.570" e não "201,570" | §2 (formato C) | Baixo — convenção é amplamente aceita; manual MSGQ-21.01 da Facens segue ABNT NBR pt-BR |
| A2 | Citação parentética para 3+ autores: `(Sobrenome, ano)` é aceito como simplificação de `(Sobrenome et al., ano)` quando o "et al." já apareceu no contexto; isto é a convenção do projeto, não verificada palavra-por-palavra no manual MSGQ-21.01 | §1.2 (Price 2020) | Baixo-médio — se o manual exigir `(Price et al., 2020)` em parênteses sempre, ajustar para `(Price et al., 2020)`. Verificar com manual abrindo §"Citação direta/indireta para 3+ autores". CONTEXT trava `(Price, 2020)`; mantido. |
| A3 | `Fonte: adaptado de Zorić (2020).` no rodapé do MARKER-01 é a citação correta para o progress bar das 4 fases EDM (porque Zorić é quem define as 4 fases no slide #5 do deck) | §3.3, §7.2 | Médio — alternativas válidas: "Fonte: elaborado pelos autores" (sem citação) OU "Fonte: elaborado pelos autores, com base em Zorić (2020)" (mais completo). Plano decide; sem impacto narrativo. |
| A4 | INTRO-03a e INTRO-03b devem reutilizar `.slide-related` (mesmo template dos slides Martins p1, Zorić fundido, Yağcí fundido) e não criar `.slide-intro` próprio | §6 | Baixo — `.slide-related` é exatamente o template para "slide de fundamentação teórica com voz autoral"; INTRO-03a/b se encaixam perfeitamente. Aceitável criar `.slide-intro` mas é dívida técnica sem ganho visual. |
| A5 | A primeira caixa do progress bar MARKER-01 deve ter o `✓` como ícone único (sem o número "1" também); a numeração nas caixas pending (2, 3, 4) substitui a ordenação visual | §3.3, §7.2 | Baixo — estética convencional de progress bar. Alternativa: "1 ✓" combinado. Plano decide. |
| A6 | O slide MARKER-01 deve ter marca d'água Facens `<svg class="wm">` (não é metaslide sem branding) | §3.3 | Baixo — todos os 12 slides de conteúdo da fase 1 têm a marca; consistência visual exige. CONTEXT D-34d diz "executor decide" no `code_context`. Recomendo SIM, manter. |
| A7 | `(Price, 2020)` no rodapé `Fonte:` é a referência canônica; "CSEDM 2021" depois do `;` é a competição que divulgou o dataset (não uma 2ª citação ABNT) | §1.2 | Baixo — CONTEXT D-35 trava esse formato literal. |

**Itens NÃO assumidos (todos verified):**
- Phrasing exato dos papers Code-DKT e ProgSnap2: lidos página por página, citados literalmente
- Números do dataset: rodados com pandas
- Ponto de inserção: lidos no HTML
- Linha 129 do STYLE.md: confirmada via grep
- Classes Fonte: inventariadas via grep no CSS

---

## Open Questions

1. **CSS de fallback para "Modelagem e Avaliação" estourar uma linha?**
   - What we know: 21 caracteres a 19px Arial bold dentro de caixa ~267px é confortável.
   - What's unclear: A 1280px (slide width), com padding 64px + 3 setas, o cálculo de largura por caixa pode ficar apertado se o navegador renderizar fonte ligeiramente diferente.
   - Recommendation: testar visualmente (D-47); se quebrar, reduzir font-size para 18px ou usar `<br>` entre "Modelagem e" / "Avaliação" — plano decide ao vivo.

2. **Atualizar inventário do STYLE.md (linhas 110-124) ou só linha 129?**
   - What we know: D-32 obriga apenas a linha 129 (sentença obsoleta).
   - What's unclear: Se vale a pena atualizar a tabela "Inventário de slides" no mesmo commit, antecipando o estado pós-fase 2.
   - Recommendation: §5.3 deste RESEARCH dá a tabela atualizada pronta; plano decide commit junto ou separado. **Recomendo junto** (trivial, evita 2ª passada).

3. **Nomenclatura `slide-intro` vs reutilizar `slide-related`?**
   - What we know: `.slide-related` é o template usado em todos os slides correlatos pós-fase 1; estilística casa com INTRO-01/03a/03b.
   - What's unclear: Se o autor preferir uma classe semântica nova (`slide-intro`) para sinalizar "esses 3 slides têm voz autoral, não são correlatos típicos".
   - Recommendation: ficar com `.slide-related` (caminho mínimo). Se plano insistir em `.slide-intro`, criar como alias CSS (`.slide-intro { /* extends */ }` herda) — não escrever CSS novo do zero.

4. **MARKER-01 deve ter um título textual além do progress bar?**
   - What we know: D-34d diz "sem `.deck-topic` no padrão `> [seção]`; o próprio progress bar é o cabeçalho visual".
   - What's unclear: Se algum texto auxiliar (ex.: "Fase 1 EDM concluída" como heading) deve aparecer entre a marca d'água e o progress bar.
   - Recommendation: NÃO. O progress bar com a caixa 1 em azul + `✓` + texto "Definição do Problema" já comunica visualmente que "esta fase está completa". Adicionar título textual seria redundante e roubaria proeminência do progress bar. Confirmar visualmente em D-47.

5. **Ordem de implementação dos 4 slides na fase de execução?**
   - What we know: CONTEXT discretion sugere MARKER-01 primeiro (para travar CSS reutilizável).
   - What's unclear: Trade-off entre "travar CSS primeiro" vs "começar pelo INTRO-01 que é o slide mais simples (texto autoral)".
   - Recommendation: MARKER-01 PRIMEIRO. Razões: (1) CSS novo é o único risco visual da fase; resolver primeiro derisca o resto. (2) Slides INTRO são paste-and-modify do template `.slide-related` (linha 100-110 do index.html), com risco baixíssimo. (3) Quando MARKER-01 estiver visualmente OK, os 3 INTRO ficam triviais.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` (servidor HTTP) | D-47 (validação visual) | ✓ | 3.x | — |
| `pandas` (números do dataset) | §2 desta pesquisa | ✓ | (rodado com sucesso) | — |
| Browser (Firefox/Chrome) | D-47 | ✓ (humano operador) | — | — |
| Reveal.js (CDN) | runtime do slide | ✓ | 5.1.0 (linha 8, 328 do index.html) | — |
| Fontes Cascadia Code (CDN) | tipografia `.deck-topic` | ✓ | jsdelivr fontsource | (degrada para Consolas/monospace local) |

Sem dependências externas que possam bloquear esta fase. Sem build system. Sem testes automatizados (validação humana via browser).

---

## State of the Art

| Old Approach (fase 1 pré-) | Current Approach (fase 2) | When Changed | Impact |
|---|---|---|---|
| `.rel-kicker` + `.rel-title` + `.rel-sub` no template `.slide-related` | `.deck-topic` único com caret blink | 2026-05-27 (fase 1) | Aplica-se aos 3 novos slides INTRO |
| Cada slide com seu próprio template | Componente `.slide-marker` reutilizável para 4 MARKERs (fases 2-5) | 2026-05-27 (esta fase) | Reduz duplicação CSS nas fases 3-5 |
| ProgSnap2 mencionado em múltiplos slides (INTRO + EDA-01 + TOOL-01) | ProgSnap2 nominalmente único em INTRO-01 | 2026-05-27 (1ª rodada feedback orientadora) | EDA-01 (fase 3) e TOOL-01 (fase 5) NÃO mencionam ProgSnap2 nominalmente |
| Citação direta literal default | Paráfrase indireta com autor parentético default | 2026-05-27 (2ª rodada feedback) | INTRO-03a/b explicitamente paráfrase (D-43); Martins p2/p3 exceção legítima (D-28) |

**Deprecated/outdated (para esta fase):**
- "INTRO-02" como slide separado: fundido em INTRO-01 (memória `requirements.md` §FUSED 2ª rodada).
- Cabeçalho "trabalhos correlatos": substituído por `> [seção]` específico (fase 1, D-21).

---

## Sources

### Primary (HIGH confidence)
- `docs/Code-DKT.pdf` (Shi, Mao, Akram, Lytinen e Heffernan, 2022) — §Abstract, §1 Introduction, §2.1 Knowledge Tracing — lidos página 1-3 (PDF), todos os 5 trechos literais do §1.1 deste RESEARCH são citações diretas verificadas.
- `docs/ProgSnap2.pdf` (Price et al., 2020, ITiCSE '20) — §Abstract, §1 Introduction, §2 The ProgSnap2 Specification, §2.1 Main Event Table — lidos página 1-4 (PDF), todos os 5 trechos literais do §1.2 deste RESEARCH são citações diretas verificadas. Ano publicação 2020 confirmado em cabeçalho ACM + DOI.
- `data/CSEDM/MainTable.csv` — `pd.read_csv` rodado em 2026-05-27, output: SubjectID=413, ProblemID=50, Events=201570.
- `apresentacao/index.html` (HEAD em 2026-05-27, 468 linhas) — boundaries de section verificadas via grep; padrão de markup do `<section><div class="deck-slide">` confirmado.
- `apresentacao/assets/theme-unifacens.css` (357 linhas) — inventário de classes Fonte: feito; CSS de `.bridge-seq`, `.deck-topic`, `.caret.blink` lidos literalmente.
- `apresentacao/STYLE.md` — frase obsoleta confirmada na linha 129; contexto das §"Gaps reservados" e §"Inventário" lido.

### Secondary (MEDIUM confidence)
- Memória `feedback_no_em_dashes` — restrição D-44 (sem em-dash) — vinculante.
- Memória `feedback_correlatos_antes` — padrão `> [seção]` vs slide dedicado a autor.
- Memória `project_split_discovery` — confirma 410 alunos pós-filtro Shi vs 413 brutos; CSEDM = Spring 2019.
- `.planning/PROJECT.md` — Key Decisions sobre ProgSnap2 único + voz própria.
- `.planning/REQUIREMENTS.md` — texto canônico de INTRO-01, INTRO-03, MARKER-01.
- `.planning/ROADMAP.md` (citado no CONTEXT) — Goal, Success Criteria 1-4.
- `.planning/phases/01-reformata-o-da-base/01-CONTEXT.md` — D-01..D-30 da fase 1, padrão `> [seção]`, voz autoral.
- `CLAUDE.md` — iteração ativa GSD, convenções da apresentação.

### Tertiary (LOW confidence)
- Manual MSGQ-21.01 REV.18 (apresentacao/4. MSGQ-21.01...pdf) — capa e folha de rosto lidas; regras detalhadas de citação direta vs indireta NÃO foram localizadas nas páginas 1-3 do PDF (manual tem várias dezenas de páginas; convenção do projeto já está consolidada via STYLE.md e memória `reference_manual_citacoes`). Não bloqueante.

---

## Metadata

**Confidence breakdown:**
- Phrasing dos papers: HIGH — citações literais extraídas, fontes primárias lidas
- Números do dataset: HIGH — pandas rodado, output capturado, contradição em D-38 detectada e documentada
- Ponto de inserção no DOM: HIGH — boundaries lidas via grep no HEAD do index.html
- Padrão CSS `.slide-marker`: MEDIUM — proposta derivada de `.bridge-seq` existente; precisa validação visual D-47 antes de travar; mas estética convencional (caixas ABNT) reduz risco
- Inventário de classes Fonte: HIGH — grep verificou todas as 6 classes
- Sentença substituta no STYLE.md (D-32): HIGH — texto literal do CONTEXT `<specifics>`

**Research date:** 2026-05-27
**Valid until:** 2026-06-27 (escopo estável; única dependência fora deste repo é o PDF dos papers — imutáveis)

## RESEARCH COMPLETE

**Phase:** 2 - Intro, Dataset e Problema (Fase 1 EDM)
**Confidence:** HIGH

### Key Findings

1. **Phrasing dos papers confirmado literalmente.** 5 trechos diretos extraídos de Code-DKT (Shi et al., 2022) sustentam a paráfrase autoral de INTRO-03a/b sem risco de overclaim; 5 trechos diretos de ProgSnap2 (Price, 2020) confirmam (a) ano 2020, (b) "registra eventos de programação" como descrição factualmente correta, (c) que o paper NÃO menciona CSEDM nominalmente (a vinculação CSEDM↔ProgSnap2 é factual via formato, não via citação literal).
2. **Números do dataset reais: 413 / 50 / 201.570 eventos.** D-38 do CONTEXT estima "~360k eventos" — está incorreto, a contagem real é ~80% menor. Recomendação de formato pt-BR para o slide: "201 mil eventos" (opção C do §2).
3. **Ponto de inserção no DOM: linhas 147-149 do `index.html`.** Os 4 novos sections entram exatamente entre o fim do slide 6 (Yağcı, `</section>` linha 147) e o comentário do slide 7 (slide-code, linha 149). Estado final: 16 sections, `#/0` a `#/15`.
4. **Componente `.slide-marker` reutilizável: CSS rascunho pronto** estendendo a estética do `.bridge-seq` (caixas borda preta 1.5px, fundo branco, setas `→` pretas) com modificadores `--done` (azul UniFacens + `✓`) e `--pending` (outline cinza). Markup completo proposto em §3.3. Reusado nas fases 3-5 sem alteração de CSS (só troca da caixa preenchida).
5. **Sentença obsoleta do STYLE.md localizada na linha 129; substituta pronta.** §5 deste RESEARCH entrega o texto-substituto literal + sugestão de atualização do bloco inteiro "Gaps reservados" (linhas 127-132). Plan-phase decide escopo do commit.
6. **Reuso de `.rel-cite` para INTRO-01/03a/03b; criar `.marker-fonte` para MARKER-01.** Inventário de 6 classes Fonte: existentes feito; padrão unificado (Arial 18px, `#5b6472`) facilita decisão.

### File Created

`.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-RESEARCH.md`

### Confidence Assessment

| Area | Level | Reason |
|------|-------|--------|
| Phrasing dos papers | HIGH | 5+5 trechos literais extraídos das fontes primárias; CSEDM/ProgSnap2 vinculação factual confirmada |
| Números do dataset | HIGH | pandas rodado; output capturado; D-38 erro detectado e corrigido em §2 |
| Ponto de inserção DOM | HIGH | grep no index.html confirma linhas 147-149 |
| CSS `.slide-marker` | MEDIUM | rascunho derivado de `.bridge-seq` já validado; validação visual (D-47) trava |
| Classes Fonte: reuso | HIGH | inventário completo via grep; padrão CSS uniforme |
| STYLE.md substituta | HIGH | texto literal do CONTEXT `<specifics>` |

### Open Questions

Ver §"Open Questions" deste RESEARCH (5 pontos, todos com recomendação não-bloqueante). Principal: ordem de implementação (sugiro MARKER-01 primeiro para travar CSS reutilizável).

### Ready for Planning

Research completo. Planner pode criar PLAN.md com:
- 4 slides + 1 update STYLE.md como tasks (4 a 5 atomicidade de commit)
- Markup pronto para reuso (§1, §3, §4, §6)
- CSS pronto para reuso (§3)
- Phrasing-alvo para 3 INTRO (§1.3)
- Checks visuais por slide (§7.2)
- Pitfalls catalogados (§Common Pitfalls)
