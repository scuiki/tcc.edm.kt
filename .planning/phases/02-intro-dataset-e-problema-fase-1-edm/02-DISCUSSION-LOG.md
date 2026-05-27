# Phase 2: Intro, Dataset e Problema (Fase 1 EDM) - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisões estão capturadas em CONTEXT.md; este log preserva as alternativas consideradas.

**Date:** 2026-05-27
**Phase:** 02-intro-dataset-e-problema-fase-1-edm
**Areas discussed:** Posição no DOM, Estética do MARKER, Cabeçalhos temáticos, Forma do INTRO-03, Cabeçalho do INTRO-03 com 2 slides, Eixo narrativo do INTRO-01, Números do dataset, Terminologia das fases no MARKER

---

## Posição no DOM

| Option | Description | Selected |
|--------|-------------|----------|
| Após Yağcí (slide 6) | Segue gancho do ROADMAP: Yağcí mostra KT ao longo do tempo → INTRO-01 'precisamos de dados com múltiplas tentativas, eis CSEDM em ProgSnap2' → INTRO-03 'mas KT clássico ignora código' → MARKER-01 | ✓ |
| Após Martins p1 (slide 3) | Segue STYLE.md atual; abertura concentrada mas quebra o gancho do Yağcí | |

**User's choice:** Após Yağcí (slide 6).
**Notes:** STYLE.md §"Gaps reservados" descrevia a posição errada e fica obsoleto; correção entra no plano (D-32 do CONTEXT).

---

## Estética do MARKER-01

| Option | Description | Selected |
|--------|-------------|----------|
| Terminal/CLI com checkmark | Bloco mono com prompt `>` e listagem das 4 fases, marcando 'Definição do Problema' como `[✓]` | |
| Progress bar horizontal de 4 etapas | Faixa com 4 caixas em linha, primeira preenchida em azul UniFacens com `✓`. Linguagem de stepper/wizard, alinha com `.bridge-seq` | ✓ |
| Checkpoint estilo git/CI | Inspirado em `git log --oneline` ou pipeline CI; commits verticais com badges | |
| Decidir no plan-phase | Adiar a decisão para execução com 2 mockups | |

**User's choice:** Progress bar horizontal de 4 etapas.
**Notes:** Estética escolhida vira template `.slide-marker` reutilizável nos MARKER-02/03/04 das fases seguintes (D-41).

---

## Cabeçalhos temáticos `> [seção]` para INTRO-01 e INTRO-03

| Option | Description | Selected |
|--------|-------------|----------|
| `> nosso dataset` + `> o problema` | Linguagem direta, primeira pessoa no INTRO-01, nominalização no INTRO-03 | |
| `> nosso dataset` + `> kt clássico ignora código` | INTRO-03 mais descritivo, antecipa a tese argumentativa | |
| `> o dataset csedm` + `> o problema do kt binário` | Mais formais, nomeiam diretamente o conceito | ✓ |

**User's choice:** `> o dataset csedm` + `> o problema do kt binário`.
**Notes:** A escolha gerou tensão depois que o INTRO-03 virou 2 slides; resolvida em pergunta de acompanhamento (vide §"Cabeçalho do INTRO-03 com 2 slides").

---

## Forma e quantidade do INTRO-03 (Shi e o problema)

| Option | Description | Selected |
|--------|-------------|----------|
| 1 slide, paráfrase + figura conceitual | Texto curto em voz própria + diagrama 'código → score 0/1 → BKT/DKT' | |
| 1 slide, paráfrase + snippet de código real | Texto + recorte CSEDM com 2 submissões de scores parciais | |
| 2 slides — diagnóstico e consequência | Slide A: paráfrase Shi; Slide B: efeito (perda de sinal pedagógico) | ✓ |
| Decidir no plan-phase | Adiar para gsd-planner gerar 2 versões em HTML | |

**User's choice:** 2 slides — diagnóstico e consequência.
**Notes:** REQUIREMENTS.md já antecipava "1 a 2 slides"; agora trava em 2. Atualização explícita do REQUIREMENTS.md fica como Deferred (executor decide se faz nesta fase ou na transição).

---

## Cabeçalho do INTRO-03 com 2 slides

| Option | Description | Selected |
|--------|-------------|----------|
| Mesmo cabeçalho nos 2 (`> o problema do kt binário`) | Espelha REFORMAT-04 (Martins p2/p3 com `> retomando o problema` repetido) | |
| Distintos: diagnóstico + consequência | `> o problema do kt binário` + `> sinal pedagógico perdido` | ✓ |
| Voltar a 1 slide só | Reconsiderar a decisão anterior; paráfrase + diagrama | |

**User's choice:** Distintos: diagnóstico + consequência.
**Notes:** Cada slide carrega um conceito; facilita retomada caso a banca pergunte.

---

## Eixo narrativo do INTRO-01

| Option | Description | Selected |
|--------|-------------|----------|
| Gancho Yağcí + 3 números + ProgSnap2 | Texto retoma Yağcí no corpo do slide; primeira pessoa do plural | |
| Foco no diferencial do ProgSnap2 (formato) | Texto centrado em por que ProgSnap2 importa; CSEDM como instância | |
| Foco no dataset + característica + números (sem gancho explícito) | Apresenta CSEDM diretamente; ProgSnap2 entre parênteses; gancho com Yağcí vem só da posição no deck | ✓ |

**User's choice:** Foco no dataset + característica + números, sem gancho explícito.
**Notes:** Preview tinha em-dash (`CSEDM —`) que precisa ser convertido a vírgula/parênteses no slide real (D-44).

---

## Números do dataset

| Option | Description | Selected |
|--------|-------------|----------|
| 410 estudantes / 50 problemas / 360k+ eventos | Pós-filtro Shi `min_attempts >= 3` | |
| 413 estudantes (Spring 2019 bruto) / 50 problemas / 360k+ eventos | Números brutos do MainTable, sem filtro | ✓ |
| Eu confiro os números e te trago no plan-phase | Adiar para o gsd-planner extrair do notebook | |

**User's choice:** 413 (bruto) / 50 / ~360k.
**Notes:** Phase 3 (EDA-02) precisa fazer a ponte explícita 413 → 410 sob protocolo Shi para que MODEL-04 da fase 4 não tenha number-shift inexplicado (D-38b). Eventos exatos a conferir no notebook 01_eda ou direto no MainTable.

---

## Terminologia das 4 fases no progress bar do MARKER-01

| Option | Description | Selected |
|--------|-------------|----------|
| Definição / Preparação / Modelagem / Implantação | Substantivos curtos, espelham `slide-phases` | |
| Definição do Problema / Preparação dos Dados / Modelagem e Avaliação / Implantação | Espelha ROADMAP/REQUIREMENTS literalmente | ✓ |
| 1. Problema / 2. Dados / 3. Modelos / 4. Ferramenta | Palavras-chave numeradas, mais lacônicas | |

**User's choice:** Versão longa, literal do ROADMAP.
**Notes:** Se a largura ficar apertada a 1280px, executor decide entre reduzir tipografia, quebrar linha ou abreviar; sem mudar os nomes (D-40).

---

## Claude's Discretion

- Ordem de implementação dos 4 slides (sugestão: MARKER-01 primeiro para travar CSS reutilizável).
- Granularidade dos commits (sugestão: atômico por slide, 4 commits).
- Microcópia exata de INTRO-03b (variantes equivalentes a "quase certo / completamente errado" aceitas).
- Decisão sobre inset visual no INTRO-03a (default sem; oportunista se ficar visualmente vazio).
- Largura/tipografia exata do progress bar do MARKER-01 (CSS livre dentro de D-39/D-40).
- Atualização da frase obsoleta em STYLE.md §"Gaps reservados" (D-32): commit junto ou separado, decisão do plano.

## Deferred Ideas

- Inset visual / diagrama em INTRO-03a/b (default fora; oportunista).
- Snippet de código CSEDM no INTRO-03 (redundante com MODEL-03/slide-code e CLOSE-01/02).
- Atualização explícita do REQUIREMENTS.md para refletir INTRO-03 = 2 sub-slides.
- Componente `.slide-marker` será criado nesta fase e reutilizado por MARKER-02/03/04 (fases 3/4/5).
- Ponte textual 413 → 410 sob protocolo Shi: fase 3 (EDA-02), uma sentença dentro do slide.
- Cronologia BKT→DKT→Code-DKT com Corbett & Anderson parentético: fase 4 (MODEL-01).
- Reordenação slide-code ↔ slide-kcfig: fase 4 ao inserir MODEL-01 e MODEL-04.
