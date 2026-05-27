# Phase 2: Intro, Dataset e Problema (Fase 1 EDM) - Context

**Gathered:** 2026-05-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Inserir 4 slides novos em `apresentacao/index.html`, todos posicionados após o slide `> da edm ao knowledge tracing` (Yağcí, atual slide 6) e antes do `slide-code` (atual slide 7, futuro MODEL-03 da fase 4). Os 4 slides fecham a Fase 1 da EDM (Definição do Problema) na narrativa da defesa:

1. **INTRO-01** ("nosso dataset"): apresenta o CSEDM em ProgSnap2 (Price, 2020), em voz própria, com 3 números de tamanho do dataset.
2. **INTRO-03a** (Shi e o problema, diagnóstico): paráfrase indireta de Shi et al. (2022) sobre KT clássico binário ignorar a estrutura do código.
3. **INTRO-03b** (consequência pedagógica): efeito do problema, modelos não distinguem "quase certo" de "completamente errado", perdem sinal pedagógico estrutural.
4. **MARKER-01** ("Definição do Problema ✓"): progress bar horizontal das 4 fases da EDM, primeira fase marcada.

Resultado da fase: deck navega do primeiro ao MARKER-01 sem quebra; padrão `> [seção]` aplicado nos 3 slides com cabeçalho temático; voz própria (paráfrase com autor parentético) preservada nos 2 INTRO-03; nenhum slide existente é alterado exceto pela inserção dos 4 sections na posição correta. Nada de Code-DKT, modelagem ou EDA aqui (fase 4 e 3 respectivamente).

Total esperado de sections no `<div class="slides">` ao fim da fase: 12 (pós-fase 1) + 4 (novos) = **16 sections**.

</domain>

<decisions>
## Implementation Decisions

### Posição no DOM (D-31)

- **D-31:** Os 4 slides entram **após o slide 6 (`> da edm ao knowledge tracing`, Yağcí)** e **antes do atual slide 7 (`slide-code`, futuro MODEL-03)**. Ordem dentro do bloco: INTRO-01 → INTRO-03a → INTRO-03b → MARKER-01.
- **D-32:** Esta posição contradiz a frase "Após `> introdução` (slide 3): INTRO-01..." que está em `apresentacao/STYLE.md` §"Gaps reservados". O **gsd-planner deve corrigir essa frase do STYLE.md** dentro desta fase ou, no mínimo, anotar no plano que ela está obsoleta. A posição correta é a deste CONTEXT.
- **D-33:** Justificativa narrativa: Yağcí lança "acompanhar o conhecimento ao longo do tempo, a cada nova tentativa"; INTRO-01 entra dizendo "o dataset que usamos preserva exatamente isso"; INTRO-03a/b entram dizendo "mas o KT clássico ainda ignora a estrutura do código"; MARKER-01 fecha a Fase 1 EDM. Sequência circular: problema (Martins) → ferramentas (Zorić/Yağcí) → dataset → problema técnico → fechamento da fase 1.

### Cabeçalhos temáticos travados (D-34)

- **D-34a (INTRO-01):** `> o dataset csedm`
- **D-34b (INTRO-03a, diagnóstico):** `> o problema do kt binário`
- **D-34c (INTRO-03b, consequência):** `> sinal pedagógico perdido`
- **D-34d (MARKER-01):** sem `.deck-topic` no padrão `> [seção]`; o próprio progress bar é o cabeçalho visual (similar ao que slide-cover e slide-title-tcc fazem, sem cabeçalho temático). Detalhe de markup fica a critério do executor.

### Tom e voz dos 4 slides (D-35..D-37)

- **D-35 (INTRO-01):** Eixo narrativo "**dataset + característica + números (sem gancho explícito ao Yağcí)**". Voz em primeira pessoa do plural ("Nosso dataset é o CSEDM..."). A propriedade-chave (preservar todas as tentativas) aparece como justificativa, conectando a Yağcí pela posição no deck (não pelo texto). Citação de Price (2020) parentética; rodapé `Fonte: Price (2020); CSEDM 2021.`
- **D-36 (INTRO-03a):** Paráfrase indireta de Shi et al. (2022), centrada no fato "modelos KT clássicos (BKT, DKT) usam apenas acerto/erro e ignoram a estrutura do código". Voz própria; **proibida** citação direta literal. Rodapé `Fonte: Shi et al. (2022).`
- **D-37 (INTRO-03b):** Continuação argumentativa: "modelos não distinguem 'quase certo' de 'completamente errado'; perde-se o sinal pedagógico estrutural". Paráfrase autoral; sem citação direta. Rodapé `Fonte: adaptado de Shi et al. (2022).` (porque a "consequência" é leitura nossa, não literal do paper).

### Números do dataset no INTRO-01 (D-38)

- **D-38:** Usar **números brutos do MainTable Spring 2019** (sem filtro Shi): **413 estudantes / 50 problemas / ~360k eventos**. Validar antes do commit: rodar `python3 -c "import pandas as pd; df = pd.read_csv('data/CSEDM/MainTable.csv'); print(df['SubjectID'].nunique(), df['ProblemID'].nunique(), len(df))"` ou abrir `notebooks/01_eda.ipynb` para conferir os 3 valores exatos. Se "~360k" for impreciso, usar o número exato com separador de milhar (ex.: 360.108).
- **D-38b (consequência downstream):** Phase 3 (EDA-02) **DEVE** fazer a ponte explícita "do CSEDM bruto (413) seguimos o protocolo de Shi et al. (2022) com filtro `min_attempts >= 3` → 410 estudantes, dos quais 328 treino / 82 teste no split 80/20". Sem essa ponte, MODEL-04 da fase 4 fica com number-shift inexplicado. Anotar isso no CONTEXT da fase 3.
- **D-38c:** Não citar o filtro/protocolo Shi no INTRO-01; é função da EDA-02 (fase 3). INTRO-01 mostra o dataset cru.

### MARKER-01 — progress bar das 4 fases (D-39..D-41)

- **D-39 (estética):** **Progress bar horizontal** com 4 etapas em linha, primeira etapa preenchida em `--uni-blue` (#2667FF) com checkmark `✓`, demais em outline cinza/`#5b6472` (não preenchidas). Caixas conectadas por seta `→` (mesma estética do `.bridge-seq` do slide Yağcí, classes a definir).
- **D-40 (terminologia das 4 etapas):** Texto literal dentro das caixas, na ordem:
  1. `Definição do Problema` (✓, marcada nesta fase)
  2. `Preparação dos Dados`
  3. `Modelagem e Avaliação`
  4. `Implantação`

  Espelha exatamente o ROADMAP.md e o STYLE.md. Pode demandar largura confortável; se ficar apertado a 1280px, **gsd-planner decide** entre (a) reduzir tipografia, (b) inserir quebra de linha dentro das caixas mais longas, ou (c) usar abreviações; sem quebrar D-40 trocando os nomes.
- **D-41 (reuso nos MARKERs futuros):** Os MARKER-02 (fase 3), MARKER-03 (fase 4) e MARKER-04 (fase 5) **DEVEM** usar o mesmo componente visual, mudando apenas qual caixa fica preenchida. Tratar como template `.slide-marker` reutilizável; classe `.marker-step--done` para a preenchida e `.marker-step--pending` para as demais. Implementar o CSS em `assets/theme-unifacens.css` agora; sem essa decisão downstream, cada fase reinventa o componente.

### Convenções herdadas da fase 1 (re-locked)

- **D-42:** Padrão de cabeçalho `> [seção]` único conforme D-01..D-03 da fase 1 (`<p class="deck-topic"><span class="ps1">&gt;</span>... <span class="caret blink"></span></p>`). Aplica-se aos slides com cabeçalho temático (INTRO-01, INTRO-03a, INTRO-03b). MARKER-01 fica sem por D-34d.
- **D-43:** Voz padrão = paráfrase indireta com autor parentético (D-25 fase 1). Citação direta literal **proibida** nos 3 slides com cabeçalho temático desta fase (não existe argumento quantitativo aqui).
- **D-44:** Sem em-dash (`—`) na prosa dos slides; usar vírgula, dois-pontos ou parênteses. Os previews mostrados durante a discussão deste CONTEXT contêm em-dash (ex.: "CSEDM — curso introdutório CS1 em Java") e **DEVEM** ser convertidos pelo executor antes de gravar HTML. Memória `feedback_no_em_dashes` é vinculante.
- **D-45:** Cada slide novo tem `Fonte:` no rodapé (Arial 17-18px, cor `#5b6472`). Formato conforme STYLE.md.
- **D-46:** Termos estrangeiros em itálico minúsculas: `*knowledge tracing*`, `*knowledge tracing binário*`, `*score*` quando aparecer. Nomes de modelos preservados (BKT, DKT, Code-DKT). ProgSnap2 e CSEDM como nomes próprios (não itálico).

### Validação visual (D-47)

- **D-47:** Ao fim da fase, validar no browser (`cd apresentacao && python3 -m http.server 8000`) percorrendo do slide 0 ao slide 15 (`#/0` até `#/15`). Sucesso: navegação completa sem erro de console; transição visual nos 4 novos sem layout quebrado; números e cabeçalhos legíveis; rodapé `Fonte:` em cada slide; progress bar do MARKER-01 com a primeira caixa preenchida e claramente marcada.

### Claude's Discretion (executor decide no plano)

- Ordem de implementação dos 4 slides (qual fica pronto primeiro). Sugestão neutra: MARKER-01 primeiro (para travar o CSS reutilizável do `.slide-marker`), depois INTRO-01, INTRO-03a, INTRO-03b.
- Granularidade dos commits: por slide (4 commits) vs por sub-bloco (INTRO-01 / INTRO-03 / MARKER-01 = 3 commits). Convenção do projeto sugere atômico por slide → 4 commits.
- Microcópia exata da paráfrase dentro do INTRO-03b: aceita-se "quase certo / completamente errado" ou variantes equivalentes ("acerto parcial vs erro total", "sinal de progresso vs sinal de erro"). Manter o argumento.
- Inset visual / diagrama dentro do INTRO-03a: a discussão não travou se entra. Default **sem diagrama** (par só de texto + paráfrase). Se durante a execução o slide ficar visualmente vazio, executor pode inserir um inset conceitual minimalista (ex.: 3 caixas `[ código Java ] → [ Score 0/1 ] → [ KT clássico ]` com seta cortando o `código Java`); sem comprometer os 10 min totais.
- Largura/tipografia exata do progress bar: D-40 trava os nomes, D-39 a estética; CSS fica livre dentro disso.
- Atualização do STYLE.md frase obsoleta (D-32): plano decide se faz junto com o último slide ou em commit separado.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning ou implementar.**

### Decisões de projeto e contexto desta fase

- `.planning/PROJECT.md` — escopo, constraints (estilo, ABNT, 10 min, sem em-dash), Key Decisions; especialmente os 4 requirements desta fase em "Active" e Key Decisions sobre ProgSnap2 nominalmente único e Shi como problema.
- `.planning/REQUIREMENTS.md` §INTRO-01, §INTRO-03, §MARKER-01 (categoria INTRO/MARKER); §Out of Scope; tabela de Traceability.
- `.planning/ROADMAP.md` §"Phase 2: Intro, Dataset e Problema (Fase 1 EDM)" — Goal, Mode, Requirements, Success Criteria 1-4.
- `.planning/phases/01-reformata-o-da-base/01-CONTEXT.md` — decisões D-01..D-30 da fase 1 (especialmente D-25 voz, D-01..D-03 padrão de cabeçalho, D-21..D-22 STYLE.md, mapa de slides em `<code_context>`).

### Estilo visual e citação (vinculante)

- `apresentacao/STYLE.md` — Identidade visual, paleta UniFacens, tipografia, regras de citação ABNT, inventário de slides pós-fase 1, "Gaps reservados". **Nota:** a frase "Após `> introdução` (slide 3): INTRO-01 + INTRO-03 + MARKER-01" desta seção está obsoleta e deve ser corrigida nesta fase (D-32). A posição real é após Yağcí (slide 6).
- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — Manual UniFacens de citação ABNT.

### Markup-alvo

- `apresentacao/index.html` — único arquivo HTML a editar; 12 `<section>` no estado pós-fase 1; 4 novos serão inseridos como descrito em D-31.
- `apresentacao/assets/theme-unifacens.css` — tema; precisa receber as classes `.slide-marker`, `.marker-step`, `.marker-step--done`, `.marker-step--pending` (ou nomenclatura equivalente) para D-39..D-41, mais ajuste para o layout dos 4 slides novos (espaçamento, tipografia dos números do dataset, caixas).

### Fontes primárias dos autores tocados nesta fase

- `docs/Code-DKT.pdf` (Shi, Mao, Akram, Lytinen e Heffernan, 2022) — base de INTRO-03a/b. **LER §Introduction e §Related Work** para travar o phrasing exato de "KT clássico binário ignora código". Ver também `docs/refs/shi2022_code_dkt.md` se existir resumo.
- `docs/ProgSnap2.pdf` (Price, 2020) — base do INTRO-01. **LER §1 Introduction e §2 Data Model** para confirmar (a) que o paper define ProgSnap2 como o formato que preserva múltiplas tentativas, (b) ano publicação correto (2020), (c) que CSEDM é uma instância. Citação será apenas `(Price, 2020)`.
- `data/CSEDM/MainTable.csv` — fonte dos números do dataset (D-38). Confirmar 413 estudantes únicos, 50 problemas únicos, contagem total de eventos com `pd.read_csv` ou via notebook 01_eda.
- `notebooks/01_eda.ipynb` — alternativa ao MainTable direto; pode já ter as 3 contagens na primeira célula de output. Não rodar o notebook inteiro, só consultar.

### Memórias (auto-context, vinculantes)

- `~/.claude/.../memory/project_split_discovery.md` — 410 alunos pós-filtro Shi vs 413 brutos; Spring 2019; split 80/20; 5 assignments × 10 problemas; AUC pooled como métrica do paper.
- `~/.claude/.../memory/feedback_no_em_dashes.md` — sem travessões em prosa (vinculante para D-44).
- `~/.claude/.../memory/feedback_tcc_writing_style.md` — citações ABNT + prosa técnica acessível.
- `~/.claude/.../memory/feedback_correlatos_antes.md` — padrão `> [seção]` substitui slide dedicado a autor; voz própria como default.
- `~/.claude/.../memory/reference_manual_citacoes.md` — manual Facens; "tradução nossa" só em direta literal estrangeira.

### Codebase context já gerado

- `.planning/codebase/STRUCTURE.md` — §"Slide novo na apresentação" descreve onde inserir e como.
- `.planning/codebase/CONVENTIONS.md` — convenções de redação e commit message style (lowercase português, prefixo `apresentacao:` ou `slide-XYZ:`).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `.deck-topic` + `.caret.blink` (em `theme-unifacens.css`): padrão de cabeçalho `> [seção]` já implementado e usado nos 12 slides da fase 1. Aplicar igual em INTRO-01, INTRO-03a, INTRO-03b.
- `.bridge-seq` (sequência horizontal com `.step` e `.arr`, no slide Yağcí): estética próxima da que MARKER-01 precisa. Pode ser estendida (não copiada) para `.slide-marker` com 4 passos e checkmark.
- `.rel-cite` / `.prob-cite` / `.fig-fonte` / `.code-fonte` / `.kcfig-fonte` / `.phases-fonte`: classes existentes para o rodapé `Fonte:`. Novos slides podem ter `.intro-cite` (INTRO-01/03) e `.marker-cite` (MARKER-01) — ou reutilizar `.rel-cite` se a estética casar; **executor decide**.
- Marca d'água Facens `<svg class="wm">`: presente em todos os slides de conteúdo; replicar nos 4 novos exceto se o MARKER-01 ficar conceitualmente "metaslide" (executor decide).

### Established Patterns

- Estrutura de slide: `<section data-background-color="#F1F6FB"><div class="deck-slide slide-XYZ">...</div></section>`. Reveal.js força `display:block` no `<section>`; layout no `<div>` interno. **NUNCA mudar isso.**
- Comentário acima de cada `<section>`: `<!-- ============ SLIDE · descrição ============ -->`. Manter formato.
- Tipografia: títulos/corpo em Arial; tópico `>` em Cascadia 24px; "Fonte:" em Arial 17-18px (alinhado às mudanças tipográficas do commit `9224d5f`).
- Cores: paleta UniFacens (`--uni-blue #2667FF`, `--uni-ink #111317`, fundo `#F1F6FB`, cinza secundário `#5b6472`).
- Citação parentética: `(Autor, ano)` sem `p. X` em paráfrase indireta; com `p. X` só em citação direta literal (proibida nesta fase). Dois autores: `;` em parênteses (`(Corbett; Anderson, 1995)`). Múltiplos autores: `Shi et al., 2022`.

### Integration Points

- Único arquivo HTML a editar: `apresentacao/index.html`.
- CSS recebe acréscimo de classes para `.slide-marker`/`.marker-step--done`/`.marker-step--pending` em `apresentacao/assets/theme-unifacens.css`.
- Browser: `cd apresentacao && python3 -m http.server 8000` → http://127.0.0.1:8000/#/N (N 0-based). Após inserção em D-31, os novos slides ficam em `#/7` a `#/10`; restante do deck desloca de +4.
- Sem build system; recarregar página direto.

### Slides existentes pós-fase 1 (estado HEAD; índice 0-based)

| # | classe | cabeçalho | papel na fase 2 |
|---|---|---|---|
| 0 | slide-cover-brand | (sem) | inalterado |
| 1 | slide-title-tcc | (sem) | inalterado |
| 2 | slide-agenda | (sem temático) | inalterado |
| 3 | slide-related | `> introdução` | inalterado |
| 4 | slide-related | `> mineração de dados educacionais` | inalterado |
| 5 | slide-phases | `> as quatro fases da edm` | inalterado |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | **ÂNCORA SUPERIOR** — INTRO-01 entra após este |
| 7 | slide-code | `> o que o code-dkt olha` | **ÂNCORA INFERIOR** — MARKER-01 entra antes deste; vira `#/11` após inserção |
| 8 | slide-kcfig | `> kcs semânticos extraídos` | inalterado; vira `#/12` |
| 9 | slide-problem | `> retomando o problema` (Martins p2) | inalterado; vira `#/13` |
| 10 | slide-problem | `> retomando o problema` (Martins p3) | inalterado; vira `#/14` |
| 11 | slide-fig | `> evolução por dificuldade` | inalterado; vira `#/15` |

### Slides a criar (4 novos)

| # após inserção | classe sugerida | cabeçalho | requirement |
|---|---|---|---|
| 7 | `slide-intro slide-dataset` ou `slide-related` adaptado | `> o dataset csedm` | INTRO-01 |
| 8 | `slide-intro slide-problem` ou `slide-related` adaptado | `> o problema do kt binário` | INTRO-03a |
| 9 | `slide-intro slide-problem` ou `slide-related` adaptado | `> sinal pedagógico perdido` | INTRO-03b |
| 10 | `slide-marker slide-marker--phase1` | (sem temático) | MARKER-01 |

Nomenclatura de classes ficou em sugestão; executor pode padronizar para `.slide-intro` único com modificadores ou usar `.slide-related` reutilizado (o template já existe). **Decisão fica no plan-phase.**

</code_context>

<specifics>
## Specific Ideas

- INTRO-01 voz: primeira pessoa do plural ("Nosso dataset é o CSEDM..."). Mencionar a propriedade-chave do ProgSnap2 (preservar todas as tentativas do mesmo estudante) como justificativa, **sem** citar nominalmente Yağcí no corpo (a posição no deck faz o gancho).
- INTRO-03a phrasing alvo (rascunho a polir no plano): "Shi et al. (2022) apontaram que modelos clássicos de *knowledge tracing*, como BKT e DKT, usam apenas acerto/erro e ignoram a estrutura do código produzido pelo estudante."
- INTRO-03b phrasing alvo: "Como consequência, esses modelos não distinguem uma submissão quase correta de uma completamente errada; o sinal pedagógico estrutural se perde no processo."
- MARKER-01: as 4 caixas espelham literalmente os títulos das fases da EDM no ROADMAP (D-40); primeira preenchida em `--uni-blue` com `✓`, as outras em outline cinza `#5b6472`; setas `→` pretas conforme estética ABNT já usada em `.bridge-seq`.
- Números do INTRO-01: 413 / 50 / 360k+ (D-38); o número exato de eventos deve ser conferido. Apresentar com separador de milhar pt-BR (ex.: `360.108`), não com vírgula.
- A frase do STYLE.md "Após `> introdução` (slide 3): INTRO-01..." em §"Gaps reservados" precisa virar "Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 'o dataset csedm' + INTRO-03a 'o problema do kt binário' + INTRO-03b 'sinal pedagógico perdido' + MARKER-01 (fase 2)".

</specifics>

<deferred>
## Deferred Ideas

- **Inset visual ou diagrama dentro do INTRO-03a/b** (ex.: 3 caixas `código → score 0/1 → KT clássico` com seta cortando o código): default **fora** desta fase. Pode entrar como ajuste oportunista se o slide ficar visualmente vazio durante execução, sem virar requirement próprio.
- **Snippet de código real do CSEDM no INTRO-03** (mostrar 2 submissões com Score parcial): defer; o argumento numérico já está em CLOSE-01/02 (Martins p2/p3 com 13/10 autores) e os exemplos de código real estão no slide-code (MODEL-03 da fase 4). Repetir aqui é redundante.
- **Atualização explícita do REQUIREMENTS.md** para refletir que INTRO-03 vira 2 sub-slides (INTRO-03a + INTRO-03b): pode entrar nesta fase ou só na transição. Decisão do plan-phase; já estava previsto pelo "1 a 2 slides" do REQUIREMENTS.md, então não é mudança de escopo.
- **Componente `.slide-marker` reutilizável** com `--done`/`--pending`: implementado já nesta fase (D-41), mas o uso nos MARKER-02/03/04 fica para fases 3/4/5. Anotar no CONTEXT da fase 3 que o componente já existe.
- **Bridge textual entre 413 (bruto) e 410 (Shi)**: defer para EDA-02 (fase 3); não criar slide novo, basta uma sentença dentro do EDA-02.
- **Cronologia BKT→DKT→Code-DKT com (Corbett; Anderson, 1995) parentético**: fase 4, MODEL-01 (já antecipado em D-19 da fase 1).
- **Reordenação do slide-code antes de slide-kcfig**: a fase 4 vai inserir MODEL-01 e MODEL-04 entre eles; ordem definitiva fica para o CONTEXT da fase 4. Esta fase 2 não toca.

### Reviewed Todos (not folded)

Nenhum todo cruzado para esta fase (`gsd-sdk query todo.match-phase 2` retornou 0 matches).

</deferred>

---

*Phase: 2-Intro, Dataset e Problema (Fase 1 EDM)*
*Context gathered: 2026-05-27*
