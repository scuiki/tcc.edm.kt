---
phase: 01-reformata-o-da-base
phase_number: 1
status: complete
started: "2026-05-27"
completed: "2026-05-27T20:30:00Z"
plans_total: 7
plans_completed: 7
requirements_completed:
  - REFORMAT-01
  - REFORMAT-02
  - REFORMAT-03
  - REFORMAT-04
  - REFORMAT-05
  - MERGE-01
  - REMOVE-01
deliverables:
  - "apresentacao/index.html: 12 sections (era 16) com padrão de cabeçalho `> [seção]` aplicado em todos os 9 slides de conteúdo"
  - "apresentacao/STYLE.md: design contract atualizado refletindo o estado pós-fase 1"
  - "apresentacao/assets/theme-unifacens.css: regras CSS órfãs removidas; tipografia ajustada (deck-topic Arial bold uppercase; 6 classes Fonte: padronizadas em 18px Arial)"
key_decisions:
  - "D-01..D-11 aplicados: cabeçalho `.deck-topic` único com `> [nome da seção]` substitui o par `.deck-topic` (> trabalhos correlatos) + `<h2>` em todos os 9 slides de conteúdo. Cabeçalhos travados: > introdução, > mineração de dados educacionais, > as quatro fases da edm, > da edm ao knowledge tracing, > o que o code-dkt olha, > kcs semânticos extraídos, > retomando o problema (2x), > evolução por dificuldade."
  - "D-16 aplicado (Claude's Discretion): slide-code antes de slide-kcfig no bloco final. Justificativa narrativa: a atenção do Code-DKT no operador `&&` é a evidência concreta da rede 'olhando' para construtos relevantes; slide-kcfig vem depois mostrando como o pipeline LLM-para-KC (Duan) confirma a estrutura conceitual."
  - "D-17 aplicado: 5 slides reposicionados no fim do `<div class=\"slides\">` na ordem slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig. Trio Martins+fig adjacente; slide-code/slide-kcfig precedem o trio."
  - "D-25 aplicado: paráfrase indireta com autor parentético adotada como padrão de voz. MERGE-01 (Zorić fundido) e REFORMAT-03 (Yağcı fundido) reescritos como paráfrase em voz própria (D-26, D-27)."
  - "D-28 aplicado (exceção legítima): citações diretas Martins p2 'mencionada por 13 autores' (p.19) e Martins p3 'citado por 10 autores' (p.20) PRESERVADAS porque os números são o argumento quantitativo da revisão sistemática."
  - "Discretion plan 01-01 Task 1: working tree pré-fase 1 commitado como snapshot âncora `ed03327` em vez de integrate implícito. Vantagem: cada plano subsequente da fase é diff isolado contra o âncora."
  - "Discretion plan 01-07 Task 4: Branch A (CSS cleanup aplicado). grep retornou 0 ocorrências de `.rel-kicker`/`.rel-title`/`.rel-sub` no index.html, então as 4 regras CSS órfãs foram deletadas do theme-unifacens.css. Demais classes do template `.slide-related` (.rel-lead, .rel-cite, .rel-quote, etc.) preservadas porque ainda em uso ou candidatas a reuso nas fases 2-5."
  - "Tweaks tipográficos pós-checkpoint (`9224d5f`): Arial em deck-topic e tcc-label; cabeçalhos `> [seção]` em bold uppercase preto; 6 classes Fonte: padronizadas em 18px Arial; sigla EDM padrão ABNT no slide Zorić fundido."
metrics:
  duration_human: "~4 horas (sessão única, 2026-05-27)"
  slides_before: 16
  slides_after: 12
  slides_removed: 2  # Corbett ×2 (REMOVE-01)
  slides_merged: 2  # Zorić p1+p2 -> 1 (MERGE-01); Yağcí p1+p2 -> 1 (REFORMAT-03)
  slides_repositioned: 5  # slide-code, slide-kcfig, Martins p2, Martins p3, slide-fig (REFORMAT-04 + REFORMAT-05)
  net_section_reduction: 4  # -2 Corbett -2 Zorić/Yağcí merges
  commits_functional: 11
  commits_metadata: 7
---

# Phase 1: Reformatação da base — Summary

A fase 1 reorganiza a base existente do deck reveal.js (`apresentacao/index.html`) para servir de ponto de partida limpo para as fases narrativas 2 a 5. Ao final dos 7 plans, o deck saiu de 16 sections com cabeçalhos heterogêneos (par `> trabalhos correlatos` + `<h2>` com nome do autor) para 12 sections com um único padrão `.deck-topic` `> [nome da seção]` por slide, autor migrado para a linha "Fonte:" no rodapé, citações diretas reescritas como paráfrase em voz própria (exceto Martins p2/p3 onde o número é o argumento), e ordem DOM reposicionada para colocar slide-code + slide-kcfig + trio Martins+fig no fim do deck.

## What Was Delivered

### Inventário final dos 12 slides

| # | classe | cabeçalho | conteúdo |
|---|---|---|---|
| 0 | slide-cover-brand | (sem cabeçalho) | Abertura (logo + tagline UniFacens) |
| 1 | slide-title-tcc | (sem cabeçalho) | Capa do TCC (autores em grafite, Arial agora explícito) |
| 2 | slide-agenda | (sem cabeçalho temático) | Agenda (a revisar na fase 5, AGENDA-01) |
| 3 | slide-related | `> INTRODUÇÃO` | Recorte do problema (Martins, Marin e Alves, 2024); 3 `.rel-lead`, rodapé "Fonte: Martins, Marin e Alves (2024)." |
| 4 | slide-related | `> MINERAÇÃO DE DADOS EDUCACIONAIS` | EDM como processo (Zorić, 2020), p1+p2 fundidos com paráfrase única em voz própria; sigla EDM (Educational Data Mining) padrão ABNT |
| 5 | slide-phases | `> AS QUATRO FASES DA EDM` | As 4 fases da EDM (Zorić, 2020); `.phases-list` com 4 itens; nota "processo iterativo" |
| 6 | slide-related slide-bridge | `> DA EDM AO KNOWLEDGE TRACING` | Ponte EDM para KT (Yağcı, 2022), p1+p2 fundidos com paráfrase; `.bridge-seq` horizontal (mineração → predição → knowledge tracing) preservada |
| 7 | slide-code | `> O QUE O CODE-DKT OLHA` | Atenção do Code-DKT no operador `&&` da submissão real do CSEDM; rodapé "elaborado pelos autores" |
| 8 | slide-kcfig | `> KCS SEMÂNTICOS EXTRAÍDOS` | Mapeamento KCs (Duan et al., 2025) para 6 dificuldades de Martins; `.kcfig-map` com 6 `.kc-row` |
| 9 | slide-problem | `> RETOMANDO O PROBLEMA` | Martins p2: `<blockquote>` "mencionada por 13 autores" (p.19, citação direta D-28); ASCII chart 7 barras animado |
| 10 | slide-problem | `> RETOMANDO O PROBLEMA` | Martins p3: `<blockquote>` "citado por 10 autores" (p.20, citação direta D-28); ASCII chart 5 barras animado |
| 11 | slide-fig | `> EVOLUÇÃO POR DIFICULDADE` | Curva de aprendizado do Code-DKT por sub-dificuldade (`fig-codedkt-martins-curves.png`); rodapé "elaborado pelos autores" |

Os 8 cabeçalhos `> [seção]` aparecem renderizados em uppercase Arial bold preto (efeito visual aplicado via CSS `text-transform: uppercase` no commit `9224d5f`); o texto no markup permanece em minúsculas conforme convenção do design contract.

### Reduções líquidas no deck

- **De 16 para 12 sections** (–4 líquido).
- –2 sections de Corbett & Anderson (REMOVE-01, plan 01-01).
- –1 section ao fundir Zorić p1 + p2 (MERGE-01, plan 01-02).
- –1 section ao fundir Yağcı p1 + p2 (REFORMAT-03, plan 01-03).
- 9 slides de conteúdo agora carregam cabeçalho `.deck-topic` único (capa, título TCC e agenda não têm cabeçalho temático por design).

### Decisões Discretion aplicadas durante a fase

1. **Plan 01-01 Task 1 — commit-wip:** o working tree pré-fase 1 (3 arquivos não comitados em `apresentacao/`) foi versionado como snapshot âncora `ed03327` em vez de implícito. Cada plano subsequente da fase produz diff isolado contra esse âncora.
2. **Plan 01-06 Task 2 — ordem slide-code/slide-kcfig:** Claude's Discretion D-16 do plano resolvida como **slide-code antes de slide-kcfig**. Justificativa narrativa em `01-06-SUMMARY.md`: a atenção do Code-DKT no `&&` é a evidência concreta, slide-kcfig confirma com KCs semânticos.
3. **Plan 01-07 Task 4 — CSS cleanup Branch A:** grep no `index.html` retornou 0 ocorrências de `.rel-kicker`, `.rel-title`, `.rel-sub`. As 4 regras CSS órfãs foram deletadas. Demais classes do template `.slide-related` (`.rel-lead`, `.rel-cite`, `.rel-quote`, `.rel-points`, `.rel-finding`, `.rel-aim`, `.rel-src`, `.rel-intro`) preservadas no CSS porque ainda em uso ou candidatas a reuso nas fases 2-5.
4. **Tweaks tipográficos pós-checkpoint (orchestrator, antes do approval final):** 4 ajustes aplicados inline em commit dedicado `9224d5f`: (a) `.deck-topic` em Arial bold uppercase preto (era Cascadia mono 24px cinza weight 400) com letter-spacing 0.02em; (b) `.slide-title-tcc .tcc-label` com Arial explícito; (c) 6 classes "Fonte:" padronizadas em 18px Arial (`.phases-fonte`, `.kcfig-fonte`, `.fig-fonte`, `.code-fonte`, mais `.rel-cite` e `.prob-cite` que já estavam); (d) slide Zorić fundido: `<b>Mineração de Dados Educacionais</b>` substituído por `mineração de dados educacionais (Educational Data Mining, EDM)` com itálico no termo estrangeiro e sigla padrão ABNT, removido `<b>` de "predição".

## Plans concluídos

| Plan | Requirement | Commit funcional | Resumo |
|---|---|---|---|
| 01-01 | REMOVE-01 | `91b9675` | Working tree commit-wip `ed03327` + delete dos 2 sections Corbett ×2 (era 16 sections, fica 14) |
| 01-02 | MERGE-01 | `f9907b8` | Fundir Zorić p1+p2 num único slide; cabeçalho `> mineração de dados educacionais`; 2 citações diretas substituídas por paráfrase única em voz própria (D-26); section count 14 → 13 |
| 01-03 | REFORMAT-03 | `b60439e` | Fundir Yağcı p1+p2 num único slide `slide-related slide-bridge`; cabeçalho `> da edm ao knowledge tracing`; paráfrase D-27; `.bridge-seq` preservada; section count 13 → 12 |
| 01-04 | REFORMAT-01 | `c31658c` | Reformatar Martins p1 com cabeçalho `> introdução` único; rodapé "Fonte: Martins, Marin e Alves (2024)." mantido; 3 `.rel-lead` preservados (D-29) |
| 01-05 | REFORMAT-02 | `23eed8b` | Reformatar slide-phases com cabeçalho `> as quatro fases da edm`; `<h2 class="phases-title">` removido; `.phases-list` (4 itens) e rodapé preservados |
| 01-06 | REFORMAT-04 + REFORMAT-05 | `590ae34`, `2a86049` | Reformatar cabeçalhos de 5 slides (Martins p2/p3, slide-kcfig, slide-fig, slide-code) e mover trio Martins+fig + slide-code/slide-kcfig para o fim do deck na ordem D-16/D-17 |
| 01-07 | (consolidação) | `907a4b5`, `30ba911`, `9224d5f` | STYLE.md (D-21) reescrito com 3 seções (cabeçalho, regras de redação, inventário); 4 regras CSS órfãs `.rel-kicker`/`.rel-title`/`.rel-sub` removidas; 4 tweaks tipográficos pós-checkpoint |

## Commits funcionais da fase 1

Em ordem cronológica (excluindo commits de metadata `docs(NN-NN):` que apenas atualizam SUMMARY/STATE/REQUIREMENTS/ROADMAP):

| Hash | Mensagem | Plan |
|---|---|---|
| `ed03327` | `apresentacao: WIP working tree antes da fase 1` | 01-01 |
| `91b9675` | `apresentacao: remover slides Corbett (REMOVE-01)` | 01-01 |
| `f9907b8` | `apresentacao: fundir slides Zorić p1+p2 com paráfrase (MERGE-01, D-26)` | 01-02 |
| `b60439e` | `apresentacao: fundir slides Yağcı p1+p2 com paráfrase (REFORMAT-03, D-27)` | 01-03 |
| `c31658c` | `apresentacao: reformatar Martins p1 com > introdução (REFORMAT-01, D-04)` | 01-04 |
| `23eed8b` | `apresentacao: reformatar slide-phases com > as quatro fases da edm (REFORMAT-02, D-05)` | 01-05 |
| `590ae34` | `apresentacao: reformatar cabeçalhos dos 5 slides do bloco final (REFORMAT-04 + REFORMAT-05)` | 01-06 |
| `2a86049` | `apresentacao: mover trio Martins+fig e slide-code/slide-kcfig para o fim (REFORMAT-04 + REFORMAT-05, D-16/D-17)` | 01-06 |
| `907a4b5` | `apresentacao: atualizar STYLE.md para padrão > [seção] (D-21, D-25)` | 01-07 |
| `30ba911` | `apresentacao: limpar regras CSS órfãs (.rel-kicker/.rel-title/.rel-sub)` | 01-07 |
| `9224d5f` | `apresentacao: ajustes tipográficos pós-checkpoint fase 1` | 01-07 |

**Total: 11 commits funcionais + 7 commits metadata `docs(NN-NN):` (um por plan + 1 de fase) = 18 commits na fase 1.**

## Validação final fim-a-fim (checkpoint humano)

O checkpoint humano `01-07-PLAN.md` Task 5 foi `approved` pelo usuário após smoke test fim-a-fim no browser. Resumo:

- **Comando:** `cd apresentacao && python3 -m http.server 8000`, abrir http://127.0.0.1:8000 com DevTools (F12) na aba Console, navegar com seta direita do slide 0 ao slide 11.
- **Resultado:** 12 slides navegáveis fim-a-fim, console DevTools sem erro vermelho, todos os 8 cabeçalhos `> [seção]` visíveis com caret piscante.
- **Gates automatizados:** 13 / 13 PASSED (ver `01-07-SUMMARY.md` "Automated Gate Output").
- **8 Success Criteria do ROADMAP fase 1:** todos confirmados pelo usuário (ver `01-07-SUMMARY.md` "Success Criteria checklist").

## Trade-offs e learnings para a fase 2

### Learnings que devem ser herdados pelos plans das fases 2-5

1. **Acceptance gates literais (`grep -c "> nome"`) falham contra HTML escapado.** O `>` no markup é renderizado como entidade `&gt;`, e o texto vem colado em `</span>$hdr` sem espaço. Os plans 01-04, 01-05, 01-06 e 01-07 todos registraram a mesma imprecisão nas suas seções "Deviations". **Padrão a herdar:** planners das fases 2-5 devem usar grep markup-aware como `grep -c "$hdr<span class=\"caret blink\""` ou similar (anchor no caret span que vem imediatamente após o texto). A substância (cabeçalho presente e correto no markup) sempre foi entregue; só o gate literal falha.

2. **Browser smoke test fim-a-fim como checkpoint humano é o gate prático de saída de fase.** Os automated gates verificam estrutura de markup, mas só o navegador captura regressões visuais sutis (peso de fonte, espaçamento, animações ASCII no Martins p2/p3, caret piscando). Replicar nas fases 2-5 como último plan de cada fase (a fase 1 já fez isso no plan 01-07).

3. **Tipografia deve ser revisada ANTES do approval do checkpoint, não depois.** Os 4 tweaks tipográficos pós-checkpoint (`9224d5f`) foram baratos via CSS, mas o ideal teria sido capturá-los como gates automatizados ou ter um sub-checkpoint tipográfico antes do checkpoint visual final. Para as fases 2-5: incluir nos automated gates verificações de `font-family`, `font-size` e `text-transform` nas classes novas que cada fase introduzir.

4. **Citações diretas vs paráfrase: política D-25 + D-28 funcionou.** Paráfrase indireta com autor parentético como padrão (Zorić, Yağcı), citação direta literal apenas onde o número é o argumento (Martins p2 "13 autores", p3 "10 autores"). Para as fases 2-5: Shi e o problema (INTRO-03) deve nascer em paráfrase; CLOSE-01/02 mantêm citação direta atual.

5. **Discretion calls explícitas nos plans economizam tempo.** Os plans 01-01 (commit-wip), 01-06 (ordem slide-code/slide-kcfig) e 01-07 (CSS cleanup branch A) tinham seções "Claude's Discretion" no plan que pré-deliberavam o trade-off. Replicar nas fases 2-5: identificar de antemão decisões que dependem de inspeção runtime e expor como Discretion.

### Issues diferidas

1. **Symlink `docs/edm_review.pdf`:** o PROJECT.md lista esse PDF como "provavelmente Zorić (2020)", mas durante a fase 1 não foi inspecionado o conteúdo real do symlink. Se a fase 2 (ou qualquer fase posterior) precisar consultar Zorić de novo, **verificar primeiro qual paper o symlink resolve**; pode estar apontando para Kalita et al. (2025) ou outro paper de review de EDM. Documentar no plan da fase 2 se for o caso.

2. **Comentário HTML do Martins p3 mantém em-dash** (`<!-- ... Martins p3 — dentro dos conceitos técnicos ...`). O plan 01-06 escreveu o texto verbatim do plano. Política do projeto é evitar em-dash em prosa; comentários HTML são fronteira ambígua. Decisão tomada: manter (comentários não são prosa exibida; substância não afetada). Mas se uma fase 2-5 reformatar esse slide ou seu comentário, substituir o `—` por `:` ou parênteses.

3. **Regras CSS preservadas mas não usadas no markup atual** (`.rel-quote`, `.rel-points`, `.rel-finding`, `.rel-aim`, `.rel-src`, `.rel-intro`): essas 6 classes ficaram no CSS porque podem ser reusadas pelas fases 2-5. Se ao final de todas as fases continuarem sem uso, considerar cleanup numa fase de polimento final.

## Próximo Passo

```
/gsd-discuss-phase 2
```

**Fase 2: Intro, Dataset e Problema (Fase 1 EDM).** Adiciona 3 slides novos (INTRO-01 "nosso dataset" CSEDM + ProgSnap2 fundido; INTRO-03 Shi e o problema em paráfrase; MARKER-01 marcador de fim da fase 1 EDM "Definição do Problema ✓"). Inserção após o slide `> introdução` (Martins p1) e antes do `> da edm ao knowledge tracing` (Yağcı fundido), aproveitando os gaps reservados pelo SKELETON.md.

---
*Phase 1 closed: 2026-05-27*
