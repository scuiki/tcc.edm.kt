---
phase: 02-intro-dataset-e-problema-fase-1-edm
phase_number: 2
status: complete
started: "2026-05-27"
completed: "2026-05-27T23:50:00Z"
plans_total: 4
plans_completed: 4
requirements_completed:
  - MARKER-01
  - INTRO-01
  - INTRO-03
deliverables:
  - "apresentacao/index.html: 16 sections (era 12) com 4 slides novos da Fase 1 EDM (INTRO-01 #/7, INTRO-03a #/8, INTRO-03b #/9, MARKER-01 #/10)"
  - "apresentacao/assets/theme-unifacens.css: componente CSS reutilizável .slide-marker (host + modificadores --done/--pending), 51 linhas adicionadas (linhas 358-408 do arquivo final)"
  - "apresentacao/STYLE.md: §Gaps reservados reescrito por inteiro (linhas 127-132) refletindo posição correta dos slides pós-fase 2 (após Yağcí slide 6) + posição da fase 3 (após MARKER-01)"
  - "Deck navega fim a fim (#/0 → #/15) em 16 sections; fase 1 EDM ('Definição do Problema') concluída na narrativa da defesa"
key_decisions:
  - "D-31..D-47 do CONTEXT aplicados; 4 slides inseridos após Yağcí fundido (slide 6), antes do slide-code (que era #/7 e desloca para #/11)"
  - "D-34a/b/c/d: cabeçalhos travados (`> o dataset csedm`, `> o problema do kt binário`, `> sinal pedagógico perdido`); MARKER-01 sem `.deck-topic` (D-34d)"
  - "D-37 voz consequencial: paráfrase autoral em INTRO-03b ('Os modelos tratam essa tentativa de forma idêntica a uma completamente errada...'); sem citação parentética nova de Shi no corpo (já citado em INTRO-03a)"
  - "D-43 sem citação direta literal nos 3 slides INTRO-* da fase 2; voz própria como padrão herdado de D-25 da fase 1"
  - "D-44 sem em-dash em prosa: aplicado em todos os 4 slides novos + 2 iterações textuais; nenhum em-dash novo introduzido no deck pela fase 2"
  - "D-45 rodapés padronizados: 'Fonte: Price (2020); CSEDM 2021.' (INTRO-01); 'Fonte: Shi <i>et al.</i> (2022).' (INTRO-03a); 'Fonte: adaptado de Shi <i>et al.</i> (2022).' (INTRO-03b); 'Fonte: adaptado de Zorić (2020).' (MARKER-01); 18px Arial cor #5b6472 herdado da fase 1"
  - "D-50 (02-02 ad-hoc): granularidade '5 assignments com 10 problemas cada' adicionada em INTRO-01 pós-checkpoint; iteração D-58 do 02-04 explicitou a aritmética 5 × 10 = 50"
  - "D-51 (02-02 ad-hoc): 6 colunas-chave do ProgSnap2 (SubjectID, ProblemID, EventType, Score, ServerTimestamp, CodeStateID) listadas em INTRO-01; vocabulário estabelecido para fase 3"
  - "D-52 (02-03 ad-hoc): paráfrase Shi 2022 + Report 4 ('tratam respostas como corretas/incorretas, ignorando seu conteúdo'); ancorada no vocabulário do Abstract do paper, não na leitura autoral inicial"
  - "D-53 (02-03 ad-hoc): ponte KT → trabalho → CSEDM em 3 parágrafos no INTRO-03a (instrumento central do TCC ancorado nos eventos do CSEDM); padrão aplicado novamente em INTRO-03b"
  - "D-54 (02-03 drive-by): `<i>et al.</i>` ABNT normalizado em todo o deck (8 ocorrências); precedente para fases 3-5"
  - "D-55 (02-03 ad-hoc): 3º parágrafo de escopo (domínios com respostas estruturadas) sem nomear Code-DKT; gate forte fase 4 mantido"
  - "D-57 (02-04 ad-hoc): cenário concreto via Report 4 evoluiu de '80% do código correto' (arbitrário) para 'acerta parte do código, mas erra em algum dos passos' + observação técnica 'pode não ser compilada, ou compilar e estar errada' cobrindo Compile.Error + Score parcial do CSEDM"
  - "D-58 (02-04 ad-hoc): `<i>gap</i>` como termo estrangeiro em INTRO-03b; D-46 estendido para reforçar marca computacional do slide"
  - "D-59 (02-04): STYLE.md §Gaps reservados reescrito por inteiro; linha 129 obsoleta substituída + linha 130 ajustada para 'Após MARKER-01'; demais linhas (fases 4 e 5) preservadas"
  - "MARKER-01 stub aceito (02-01): redesenho visual do componente .slide-marker DIFERIDO; contrato de classes (--done/--pending/__mark) preservado; backlog visual"
metrics:
  duration_human: "~3-4 horas (sessão única, 2026-05-27)"
  slides_before: 12
  slides_after: 16
  slides_added: 4  # INTRO-01, INTRO-03a, INTRO-03b, MARKER-01
  net_section_growth: 4
  commits_functional: 12  # 02-01: 2, 02-02: 3, 02-03: 4, 02-04: 3 (c92b9ff + 6a70b7f + f4dde9c)
  commits_metadata: 4  # docs(02-01), docs(02-02), docs(02-03), docs(phase-02)
  iterations_post_checkpoint: 8  # 02-02: 2, 02-03: 3, 02-04: 2 (rewrite + drive-by INTRO-01) — todas aprovadas pelo reviewer
---

# Phase 2: Intro, Dataset e Problema (Fase 1 EDM) — Summary

A fase 2 adiciona 4 slides novos à apresentação reveal.js, completando a narrativa da Fase 1 EDM (Definição do Problema). O deck saiu de 12 sections (pós-fase 1) para 16 sections, com a sequência narrativa "Yağcí ponte → CSEDM (INTRO-01) → problema do KT binário (INTRO-03a) → consequência pedagógica (INTRO-03b) → marcador de fase EDM concluída (MARKER-01)" preservada literalmente. Voz própria em paráfrase indireta como padrão (D-25 da fase 1), Code-DKT NÃO mencionado em nenhum dos 4 slides (gate forte; fase 4), e `<i>et al.</i>` ABNT normalizado em todo o deck via drive-by sweep do plan 02-03.

## What Was Delivered

### Inventário final dos 16 slides (estado pós-fase 2)

| # | classe | cabeçalho | conteúdo | origem |
|---|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho) | Abertura | Fase 1 |
| 1 | slide-title-tcc | (sem cabeçalho) | Capa do TCC | Fase 1 |
| 2 | slide-agenda | (sem cabeçalho temático) | Agenda (a revisar na fase 5) | Fase 1 |
| 3 | slide-related | `> introdução` | Martins p1 | Fase 1 |
| 4 | slide-related | `> mineração de dados educacionais` | Zorić fundido | Fase 1 |
| 5 | slide-phases | `> as quatro fases da edm` | Zorić p3 (4 fases) | Fase 1 |
| 6 | slide-related slide-bridge | `> da edm ao knowledge tracing` | Yağcí fundido | Fase 1 |
| **7** | **slide-related** | **`> o dataset csedm`** | **INTRO-01: CSEDM em ProgSnap2, 413 estudantes / 5 assignments × 10 problemas / 201 mil eventos, 6 colunas-chave** | **Fase 2 (plan 02-02)** |
| **8** | **slide-related** | **`> o problema do kt binário`** | **INTRO-03a: ponte KT → trabalho → CSEDM; Shi et al. (2022); BKT e DKT tratam respostas só como corretas/incorretas; escopo domínios com respostas estruturadas** | **Fase 2 (plan 02-03)** |
| **9** | **slide-related** | **`> sinal pedagógico perdido`** | **INTRO-03b: cenário (acerta parte do código, erra em algum passo, Compile.Error ou Score parcial → incorreta) → perda pedagógica (aprendizado parcial fica invisível) → pivô (gap entre KT clássico e o que pedagogicamente aconteceu)** | **Fase 2 (plan 02-04)** |
| **10** | **slide-marker slide-marker--phase1** | **(sem cabeçalho temático)** | **MARKER-01: progress bar 4 fases EDM, "Definição do Problema" em `--done` com ✓, 3 demais em `--pending` com números 2/3/4** | **Fase 2 (plan 02-01)** |
| 11 | slide-code | `> o que o code-dkt olha` | Atenção do Code-DKT no operador `&&` | Fase 1 (deslocado de #/7) |
| 12 | slide-kcfig | `> kcs semânticos extraídos` | Mapeamento KCs (Duan, 2025) | Fase 1 (deslocado de #/8) |
| 13 | slide-problem | `> retomando o problema` | Martins p2 (13 autores) | Fase 1 (deslocado de #/9) |
| 14 | slide-problem | `> retomando o problema` | Martins p3 (10 autores) | Fase 1 (deslocado de #/10) |
| 15 | slide-fig | `> evolução por dificuldade` | Curva Code-DKT por dificuldade | Fase 1 (deslocado de #/11) |

### Crescimento líquido no deck

- **De 12 para 16 sections** (+4 líquido).
- +1 INTRO-01 (slide #/7, plan 02-02).
- +1 INTRO-03a (slide #/8, plan 02-03).
- +1 INTRO-03b (slide #/9, plan 02-04).
- +1 MARKER-01 (slide #/10, plan 02-01).
- Os 4 slides existentes do bloco final (slide-code, slide-kcfig, Martins p2, Martins p3, slide-fig) foram deslocados de #/7..#/11 para #/11..#/15.

### Componente CSS reutilizável `.slide-marker`

Plan 02-01 introduziu o componente CSS `.slide-marker` em `apresentacao/assets/theme-unifacens.css` (linhas 358-408, 51 linhas adicionadas), com:

- `.slide-marker` (host)
- `.marker-track` (container das 4 caixas + setas)
- `.marker-step` (caixa individual)
- `.marker-step__mark` (símbolo dentro da caixa: ✓ ou número)
- `.marker-step--done` (caixa preenchida em `--uni-blue`)
- `.marker-step--pending` (caixa em outline cinza)
- `.marker-arr` (seta entre caixas)
- `.slide-marker .marker-fonte` (rodapé "Fonte:" centralizado)

Variáveis CSS herdadas (sem novas): `--uni-blue`, `--uni-light`, `--uni-gray`, `--mono`. Sem `border-radius` por decisão visual. O componente está pronto para ser reusado por MARKER-02 (fase 3), MARKER-03 (fase 4), MARKER-04 (fase 5) sem alteração adicional no CSS — apenas trocando qual caixa carrega o modificador `--done`.

### STYLE.md sincronizado

Plan 02-04 reescreveu §Gaps reservados por inteiro (linhas 127-132 do STYLE.md):

- Frase obsoleta da linha 129 ("Após `> introdução` (slide 3): INTRO-01...") substituída pela posição correta ("Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 'o dataset csedm' + INTRO-03a 'o problema do kt binário' + INTRO-03b 'sinal pedagógico perdido' + MARKER-01 (fase 2).")
- Linha 130 ajustada de "Após `> da edm ao knowledge tracing` (slide 6): EDA-01..." para "Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3)." (porque MARKER-01 agora ocupa o gap originalmente reservado para EDA).
- Linhas 131-132 (gaps das fases 4 e 5) preservadas inalteradas.

A fase 3 lê o STYLE.md já consistente.

## Plans concluídos

| Plan | Requirement | Commits funcionais | Iterações | Resumo |
|---|---|---|---|---|
| 02-01 | MARKER-01 | `d37304d`, `3d47be4` | 0 | Componente CSS reutilizável `.slide-marker` (host + modificadores --done/--pending) + section MARKER-01 (4 caixas, primeira em --done com ✓); stub aceito, redesenho visual diferido para fim da fase 2 ou batch com MARKER-02/03/04; contrato de classes preservado |
| 02-02 | INTRO-01 | `c362e9d`, `e07e37b`, `3835336` | 2 (textual) | Section INTRO-01 "o dataset csedm" em voz 1ª pessoa do plural; CSEDM em ProgSnap2 (Price, 2020); números brutos 413/50/201 mil validados via pandas; iterações pós-checkpoint adicionaram granularidade Spring 2019 explícito, 5 assignments × 10 problemas, e 6 colunas-chave do ProgSnap2 (D-50, D-51) |
| 02-03 | INTRO-03 (parcial: 03a) | `6f0ae3d`, `53b46e8`, `f7e042a`, `4a9af6e` | 3 (textual + drive-by) | Section INTRO-03a "o problema do kt binário"; 3 parágrafos (ponte KT → crítica Shi → escopo); iterações pós-checkpoint reescreveram com fraseado do Report 4 + Shi 2022 (D-52), adicionaram ponte KT → trabalho → CSEDM (D-53), e normalizaram `<i>et al.</i>` ABNT em todo o deck (D-54, 8 ocorrências em drive-by) |
| 02-04 | INTRO-03 (fechado: 03b) | `c92b9ff`, `6a70b7f`, `f4dde9c` | 1 (textual) + drive-by INTRO-01 | Section INTRO-03b "sinal pedagógico perdido" entre INTRO-03a e MARKER-01; 3 parágrafos consequenciais (cenário concreto → perda pedagógica → gap KT clássico); iteração pós-checkpoint expandiu cenário (Compile.Error + parcial via "pode não ser compilada, ou compilar e estar errada", D-57) e introduziu `<i>gap</i>` (D-58); STYLE.md §Gaps reservados reescrito por inteiro (D-59); deck final 16 sections; fase 2 fechada |

## Commits funcionais da fase 2

Em ordem cronológica (excluindo commits de metadata `docs(NN-NN):`):

| Hash | Mensagem | Plan |
|---|---|---|
| `d37304d` | `apresentacao: componente .slide-marker reutilizavel (fase 2)` | 02-01 |
| `3d47be4` | `apresentacao: slide MARKER-01 - definicao do problema (fase 2)` | 02-01 |
| `c362e9d` | `apresentacao: slide INTRO-01 - dataset CSEDM (Price, 2020)` | 02-02 |
| `e07e37b` | `apresentacao: ajustar INTRO-01 - primavera 2019, 5 assignments, colunas ProgSnap2` | 02-02 |
| `3835336` | `apresentacao: ajustar fraseado da coleta no slide INTRO-01` | 02-02 |
| `6f0ae3d` | `apresentacao: slide INTRO-03a - problema do kt binario (Shi et al. 2022)` | 02-03 |
| `53b46e8` | `apresentacao: reescrever INTRO-03a com fraseado do Report 4 + Shi 2022` | 02-03 |
| `f7e042a` | `apresentacao: adicionar ponte KT-trabalho-CSEDM em INTRO-03a` | 02-03 |
| `4a9af6e` | `apresentacao: italizar "et al." conforme ABNT no deck` | 02-03 |
| `c92b9ff` | `apresentacao: slide INTRO-03b - sinal pedagogico perdido` | 02-04 |
| `6a70b7f` | `apresentacao: reescrever INTRO-03b com cenario expandido + gap` | 02-04 |
| `f4dde9c` | `docs(style): atualizar gaps reservados pos-fase 2` | 02-04 |

**Total: 12 commits funcionais + 4 commits metadata `docs(NN-NN):` (3 por plan + 1 de fase) = 16 commits na fase 2.**

## Validação final fim-a-fim (checkpoint humano)

O checkpoint humano `02-04-PLAN.md` Task 3 foi `approved` pelo usuário após smoke test fim-a-fim no browser. Resumo:

- **Comando:** `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000 e navegar do slide #/0 ao #/15 (16 slides totais).
- **Resultado:** 16 slides navegáveis fim-a-fim, console DevTools sem erro vermelho, os 4 slides novos (INTRO-01 #/7, INTRO-03a #/8, INTRO-03b #/9, MARKER-01 #/10) com layout coerente em 1280×720, rodapé "Fonte:" em cada slide, MARKER-01 com primeira caixa em `--done` com ✓ e as outras em `--pending` com números 2/3/4.
- **Verifier subagent desabilitado por config** (`workflow.verifier=false` na sessão; STATE.md: "Verifier: off (visual validation in browser)"). Validação visual humana é o gate de saída da fase.
- **Aprovação:** "approved fase 2" / "ok fim-a-fim" pelo reviewer humano.

## Trade-offs e learnings para a fase 3

### Learnings que devem ser herdados pelos plans da fase 3

1. **Iterações textuais pós-checkpoint são esperadas, não bugs.** Cada um dos 4 plans teve iterações pós-checkpoint visual (02-01: 0, 02-02: 2, 02-03: 3, 02-04: 1 + drive-by) somando 8 iterações totais; todas aprovadas, todas dentro do escopo do requirement original. Padrão a herdar: planners da fase 3 devem antecipar 1-2 iterações de polimento textual por slide INTRO/EDA com voz própria; granularidade aritmética e ancoragem no dataset frequentemente precisam de ajuste após o reviewer ver o slide no browser.

2. **Decisões ad-hoc D-50..D-59 acumulam.** 8 decisões ad-hoc registradas nesta fase (5 textuais de 02-02/03, 3 estruturais de 02-04). Padrão a herdar: os planners da fase 3 devem ler este PHASE-SUMMARY para evitar redefinir conceitos já estabelecidos (5 assignments × 10 problemas, 6 colunas-chave do ProgSnap2, ponte KT → trabalho → CSEDM, `<i>et al.</i>` ABNT, `<i>gap</i>` para termos estrangeiros).

3. **Verifier off + checkpoint humano funciona se o reviewer é diligente.** Toda a fase 2 rodou sem gsd-verifier subagent. O checkpoint humano fim a fim em browser foi o único gate de saída de fase. Replicar nas fases 3-5 mantém o ritmo da iteração; mas exige que o reviewer humano abra o browser e valide os slides novos imediatamente após cada plan.

4. **Citações ABNT precisam de drive-by sweep ao introduzir padrão novo.** D-54 (`<i>et al.</i>` em itálico) foi descoberta no INTRO-03a e aplicada em batch nas 8 ocorrências do deck. Padrão a herdar: ao introduzir convenção tipográfica nova em um slide INTRO de fase 2-5, varrer o deck inteiro no mesmo commit; evita inconsistência visual entre slides irmãos.

5. **Decisões "stub aceito, redesenho diferido" são legítimas e devem ser documentadas explicitamente.** MARKER-01 (02-01) ficou como stub funcional aprovado mas com backlog visual (redesenho do componente `.slide-marker` com viés computacional). Padrão a herdar: a fase 3 deve antecipar que MARKER-02 herdará o stub atual; redesenho visual será revisitado em batch com MARKER-02/03/04 ou antes da defesa.

### Backlog visual herdado para fases futuras

- **Redesenhar `.slide-marker`** com viés de computação (referências possíveis: AST, terminal/CLI, pipeline com setas tipográficas, blocos de código, indicador de progresso de build). Triggers possíveis: (a) ao implementar MARKER-02 na fase 3 (retroage para MARKER-01), (b) em batch com MARKER-02/03/04 ao fim da fase 5, (c) sessão dedicada de polimento visual antes da defesa. Contrato de classes (`--done`/`--pending`/`__mark`) preservado; redesenho não quebra callers.
- **D-58 termo estrangeiro `<i>gap</i>` ou similar:** pode aparecer naturalmente em MODEL-* da fase 4 (`<i>pipeline</i>`, `<i>benchmark</i>`, etc.). Aplicar se ficar natural; D-46 herdado.

### Issues diferidas

Nenhuma issue técnica diferida pela fase 2. A única decisão de backlog é o redesenho visual do `.slide-marker` (acima), que não bloqueia nada.

## Próximo Passo

```
/gsd-discuss-phase 3
```

**Fase 3: EDA e Pré-processamento (Fase 2 EDM).** Adiciona 4 slides novos (EDA-01, EDA-02, EDA-03 + MARKER-02). Inserção após MARKER-01 (#/10) e antes do slide-code (#/11), aproveitando o gap já registrado em apresentacao/STYLE.md §Gaps reservados.

Vocabulário herdado da fase 2 (não redefinir):
- "5 assignments × 10 problemas" / 6 colunas-chave do ProgSnap2 (D-50, D-51)
- Ponte KT → trabalho → CSEDM (D-53)
- `<i>et al.</i>` ABNT (D-54)
- "tratam respostas como corretas/incorretas, ignorando seu conteúdo" (D-52, vocabulário Shi 2022 Abstract)

EDA-02 DEVE fazer a ponte explícita "do CSEDM bruto (413) seguimos o protocolo de Shi et al. (2022) com filtro `min_attempts >= 3` → 410 estudantes" (D-38b do CONTEXT da fase 2). MARKER-02 herda o stub atual do `.slide-marker`; redesenho visual permanece em backlog.

---

*Phase 2 closed: 2026-05-27*
