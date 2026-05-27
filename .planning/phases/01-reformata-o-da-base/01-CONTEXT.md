# Phase 1: Reformatação da base - Context

**Gathered:** 2026-05-27 (atualizado 2026-05-27 com 2ª rodada de feedback da orientadora)
**Status:** Ready for planning

<domain>
## Phase Boundary

Reformatar 7 slides existentes em `apresentacao/index.html` para o novo padrão narrativo de cabeçalho, fundindo Zorić p1+p2, removendo os 2 slides Corbett & Anderson, e movimentando 5 slides (Martins p2, Martins p3, slide-fig, slide-code, slide-kcfig) para o fim do `<section>` raiz como preparação do bloco de modelagem/fechamento.

Resultado da fase: deck navegável no browser do primeiro ao último slide, com a base reorganizada e o padrão de cabeçalho `> [seção]` consolidado nos 7 slides afetados, pronto para receber novos slides nas fases 2 a 5 nos gaps já abertos. Sem criação de slides novos, sem texto do TCC, sem PDF.

</domain>

<decisions>
## Implementation Decisions

### Padrão de cabeçalho (regra fundamental da fase)

- **D-01:** Todos os slides reformatados adotam `<p class="deck-topic"><span class="ps1">&gt;</span>[nome da seção]<span class="caret blink"></span></p>` (Cascadia 24px, caret piscando) como única linha de cabeçalho. Substitui o tópico anterior (`> trabalhos correlatos` ou similar) E o `<h2>` com nome do autor. Subtítulo (`.rel-sub`) some quando o slide tinha um.
- **D-02:** Autor passa a aparecer apenas no rodapé `Fonte:` do próprio slide. Nenhuma menção ao nome do autor permanece no corpo, no kicker ou em `<h2>`.
- **D-03:** Slides existentes que usam template `.slide-related` perdem o par `.rel-kicker` + `.rel-title`; os slides que usam `.deck-topic` + `<h2>` (slide-problem, slide-phases, slide-fig, slide-code, slide-kcfig) perdem o `<h2>` interno e mantêm só o `.deck-topic`. Classes CSS visuais (`.slide-related`, `.slide-fig`, etc.) permanecem para preservar layout, só o markup do cabeçalho muda.

### Cabeçalhos travados por requirement

- **D-04 (REFORMAT-01, Martins p1):** `> introdução` (já travado no PROJECT.md)
- **D-05 (REFORMAT-02, Zorić p3 / slide-phases):** `> as quatro fases da edm` (já travado no PROJECT.md)
- **D-06 (REFORMAT-03, Yağcí fundido):** `> da edm ao knowledge tracing`
- **D-07 (REFORMAT-04, Martins p2 + Martins p3):** `> retomando o problema` (MESMO cabeçalho nos dois slides; reforça continuidade no bloco de fechamento e amarra com 'retomando' o gancho lançado na introdução)
- **D-08 (REFORMAT-05a, slide-kcfig):** `> kcs semânticos extraídos` (posiciona como saída do pipeline KCs, futuro MODEL-07; não como mapeamento dirigido por Martins)
- **D-09 (REFORMAT-05b, slide-fig):** `> evolução por dificuldade` (foca no eixo X / oportunidade; encaixa em CLOSE-03 sem repetir 'retomando o problema')
- **D-10 (REFORMAT-05c, slide-code):** `> o que o code-dkt olha` (mantém pergunta narrativa do título original; ressalta interpretabilidade, gancho para TCC 2)
- **D-11 (MERGE-01, Zorić p1+p2):** `> mineração de dados educacionais` (já travado no PROJECT.md)

### Yağcí: fundir em 1 slide (REFORMAT-03)

- **D-12:** Os dois slides Yağcí existentes (slide-related introdução + slide-related slide-bridge ponte) viram um único `<section>` com cabeçalho `> da edm ao knowledge tracing`.
- **D-13:** Corpo do slide fundido (ordem do markup): citação direta do p2 ("Outra dimensão da análise de aprendizagem é prever o desempenho acadêmico dos estudantes [...] e determinar os estudantes potencialmente em risco de reprovação", Yağcı, 2022, p. 2, tradução nossa) → sequência horizontal `.bridge-seq` com 3 passos (`mineração de dados educacionais → predição de desempenho → knowledge tracing`) → parágrafo `.bridge-text` ("Yağcı (2022) posiciona [...]. O knowledge tracing dá o passo seguinte: em vez de uma única previsão ao fim do curso, acompanha o conhecimento do estudante ao longo do tempo, a cada nova tentativa.").
- **D-14:** Conteúdo descartado do p1: citação inicial (p. 1), subtítulo "Predição do desempenho acadêmico com mineração de dados educacionais", e os três bullets de algoritmos / acurácia 70-75% / 1854 alunos. O nome 'Yağcı' continua presente nos atributos da citação direta e no rodapé `Fonte: Yağcı (2022).`.

### Movimentação de DOM (REFORMAT-04 + REFORMAT-05)

- **D-15:** Fase 1 já move + reformata os 5 slides afetados; não fica para a fase 4. Justificativa: economiza um segundo round de movimentação na fase 4 e o cabeçalho `> retomando o problema` só faz sentido com Martins p2/p3 reposicionados.
- **D-16:** Ordem no fim do `<section>` raiz, após movimentação: slide-code e slide-kcfig (ordem livre, executor decide qual fica antes) → bloco fechamento adjacente Martins p2 → Martins p3 → slide-fig (NESTA ORDEM, sem nada entre eles).
- **D-17:** Restrições obrigatórias: (a) Martins p2 e Martins p3 ficam adjacentes; (b) slide-fig vem imediatamente após Martins p3; (c) slide-code e slide-kcfig precedem o trio Martins+fig.
- **D-18:** A fase 4 vai inserir MODEL-01 e MODEL-02 antes de slide-code; MODEL-04, MODEL-05, MODEL-06, MODEL-08 entre slide-code/slide-kcfig e o trio Martins+fig (com slide-kcfig provavelmente posicionado próximo a MODEL-07 nessa inserção); MARKER-03 logo após slide-fig. O CONTEXT da fase 4 deve respeitar D-16/D-17 ao planejar.

### REMOVE-01 Corbett & Anderson

- **D-19:** Apagar os 2 `<section>` `slide-related slide-corbett` sem deixar comentário/placeholder no markup nem nota no REQUIREMENTS.md. A cronologia da fase 4 (MODEL-01) trará a citação `(Corbett; Anderson, 1995)` quando construir a linhagem `BKT → DKT → Code-DKT`. O CONTEXT da fase 4 lembrará disso quando for escrito.
- **D-20:** Verificação de fim de fase: `grep -c 'slide-corbett' apresentacao/index.html` retorna 0.

### Atualização do STYLE.md (escopo da fase 1)

- **D-21:** `apresentacao/STYLE.md` é atualizado dentro da fase 1, junto com o markup. As seguintes seções precisam ser reescritas para o novo padrão:
  - Seção "Cabeçalho de todo slide após a AGENDA": substituir descrição do par tópico + título por descrição do `> [nome da seção]` único, mencionando que o autor desaparece do corpo e fica em "Fonte:".
  - Seção "Regras de redação", bullet "Regra dos correlatos": REMOVER ("todo autor novo é introduzido em um slide `> trabalhos correlatos` ANTES do slide que usa seus resultados"). Substituir por nota de que autores são introduzidos no momento da relevância via cabeçalho temático e nunca em slide dedicado.
  - Seção "Inventário de slides (ordem atual)": reescrever para refletir o estado pós-fase 1 (Corbett removido, Zorić p1+p2 fundido, Yağcí fundido, 5 slides movidos para o fim, novo padrão de cabeçalho aplicado).
- **D-22:** STYLE.md atualizado entra no mesmo commit que o último slide reformatado ou em commit próprio ao final da fase; decisão do plano.

### Microcópia 'Fonte:'

- **D-23:** Cada slide mantém a linha "Fonte:" que já carrega no HEAD atual (ex.: `Fonte: Zorić (2020).`, `Fonte: Yağcı (2022).`, `Fonte: adaptado de Martins, Marin e Alves (2024).`). Fase 1 só garante: (a) cada slide reformatado tem UMA linha "Fonte:" no rodapé; (b) sobrenome e ano corretos; (c) "adaptado de" preservado quando aplicável.
- **D-24:** Para slides com múltiplas referências (ex. slide-kcfig cita Duan + Martins), manter o formato existente "Fonte: elaborado pelos autores, com base em Duan et al. (2025) e Martins, Marin e Alves (2024)." (sem mudança).

### Voz: paráfrase como padrão, citação direta como exceção (adicionado em 2ª rodada de feedback)

Política aplicável a todos os slides desta fase com texto citacional. Resumo: o foco da defesa é o NOSSO trabalho; citações diretas literais tiram protagonismo dos autores da defesa e gastam tempo de leitura.

- **D-25 (regra geral):** Paráfrase indireta com autor parentético é o padrão para textos novos e existentes. Voz em primeira pessoa do plural quando aplicável ("nosso trabalho aplica", "nós seguimos", "implementamos"). Citação direta literal só quando a frase específica É o argumento (caso quantitativo Martins).
- **D-26 (MERGE-01 Zorić fundido — REESCRITA):** Substituir as 2 citações diretas atuais do slide-related Zorić p1 ("A Mineração de Dados Educacionais (EDM) é uma área de pesquisa interdisciplinar...", Zorić, 2020, p. 12, tradução nossa) E do slide-methods Zorić p2 ("Utiliza diferentes métodos e técnicas de aprendizado de máquina...", Zorić, 2020, p. 12, tradução nossa) por paráfrase indireta única, voz própria. Sugestão de texto: "Nosso trabalho aplica o processo de **Mineração de Dados Educacionais**, área interdisciplinar que combina mineração de dados, estatística e aprendizado de máquina para apoiar decisões pedagógicas (Zorić, 2020). Tarefas típicas incluem classificação, agrupamento, **predição** e associação." Sem `<blockquote class="rel-quote">`; texto corre como `<p class="rel-lead">` ou similar. Rodapé `Fonte: Zorić (2020).` mantido.
- **D-27 (REFORMAT-03 Yağcí fundido — REESCRITA):** Substituir a citação direta atual do slide-bridge Yağcí p2 ("Outra dimensão da análise de aprendizagem é prever o desempenho acadêmico dos estudantes [...] e determinar os estudantes potencialmente em risco de reprovação", Yağcı, 2022, p. 2, tradução nossa) por paráfrase centrada no avanço do nosso trabalho. Sugestão de texto: "Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar alunos em risco. Nós seguimos o passo seguinte: em vez de uma previsão única ao fim do curso, **acompanhamos o conhecimento ao longo do tempo**, a cada nova tentativa, via *knowledge tracing*." Sem `<blockquote class="rel-quote">`; mantém a sequência `.bridge-seq` (3 passos) e o parágrafo `.bridge-text` (que naturalmente é paráfrase). Rodapé `Fonte: Yağcı (2022).` mantido.
- **D-28 (REFORMAT-04 Martins p2/p3 — EXCEÇÃO LEGÍTIMA):** **MANTER** as citações diretas atuais (Martins; Marin; Alves, 2024, p. 19 e p. 20). Os números "mencionada por 13 autores" e "citado por 10 autores" são o argumento quantitativo da revisão sistemática; paráfrase enfraqueceria o impacto. Esta é a exceção justificada à regra D-25.
- **D-29 (REFORMAT-01 Martins p1, REFORMAT-02 Zorić p3, REFORMAT-05a/b/c, MERGE-01 demais elementos):** Slides que JÁ estão em paráfrase ou que não têm citação direta no HEAD atual — sem reescrita textual; apenas cabeçalho conforme D-04 a D-11.
- **D-30 (impacto no plano):** O plan-phase 1 deve listar D-26 e D-27 como sub-tasks textuais EXPLÍCITAS dentro dos slides MERGE-01 e REFORMAT-03, não apenas mudança de cabeçalho. Tempo de execução estimado: +5-10 min por slide para escrever a paráfrase e validar visualmente.

### Claude's Discretion (executor decide no plano)

- Working tree atual (mudanças não commitadas em `apresentacao/index.html` e `apresentacao/assets/theme-unifacens.css`): o gsd-planner decide se descarta, stashea, integra como ponto de partida ou commita separado como WIP antes de começar. Recomendação implícita: integrar (pois carrega nomes dos autores Erick/Leonardo/Victor e os 2 slides Yağcí que vão ser fundidos de qualquer jeito).
- Ordem exata entre slide-code e slide-kcfig (qual vem primeiro) — D-16 deixa livre.
- Cadência de validação no browser: success criteria #1 do ROADMAP pede navegação fim-a-fim sem erro de console; executor escolhe entre validar por slide (commit + browser entre cada) ou em lote (fim da fase). Convenção do projeto (commits atômicos por slide) sugere validar por lote no fim.
- Granularidade dos commits: convenção é "atômico por slide concluído" (do CLAUDE.md). Esperado: ~8-9 commits na fase (7 REFORMATS + MERGE-01 + REMOVE-01 + STYLE.md).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Decisões de projeto e contexto da fase

- `.planning/PROJECT.md` — Validated/Active/Out of Scope, Constraints (estilo, ABNT, 10 min, sem em-dash), Key Decisions tabela; especialmente Active > Reformatações REFORMAT-01..05 e Key Decisions sobre o novo cabeçalho.
- `.planning/REQUIREMENTS.md` — REFORMAT-01..05, MERGE-01, REMOVE-01 com texto completo; tabela de traceability mapeando para Phase 1.
- `.planning/ROADMAP.md` §"Phase 1: Reformatação da base" — Goal, Mode, Requirements list, Success Criteria 1-8 (gates de fim de fase).

### Estilo visual e citação (vinculante na fase)

- `apresentacao/STYLE.md` — Identidade visual, paleta UniFacens, tipografia, regras de citação ABNT, inventário de slides, regra "todo slide tem `Fonte:`". OBS: este arquivo é EDITADO na fase 1 (D-21); ler como referência do estado atual e como destino a atualizar.
- `apresentacao/4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf` — Manual oficial UniFacens de citação ABNT (citação direta curta/longa, "tradução nossa", paráfrase indireta).

### Markup-alvo da fase

- `apresentacao/index.html` — único arquivo HTML a editar; ~16 `<section>` no estado atual (HEAD) + working tree com 2 sections Yağcí novos.
- `apresentacao/assets/theme-unifacens.css` — tema; working tree tem mudanças. Não deve mudar em fase 1 exceto para refletir o novo padrão se algum estilo de `.rel-kicker`/`.rel-title` ficar órfão.

### Fontes primárias dos autores tocados na fase

- `docs/edm_review.pdf` (provavelmente Zorić 2020) — base do `> mineração de dados educacionais` e `> as quatro fases da edm`. LER antes de tocar nesses slides.
- `docs/edm_prediction.pdf` (provavelmente Yağcı 2022) — base do `> da edm ao knowledge tracing` e da citação p. 2 mantida no slide fundido. LER antes de tocar.
- `docs/Artigo+2+Desafios+na+aprendizagem...pdf` (Martins, Marin e Alves 2024) — base do Martins p1 (`> introdução`) e dos dois slides reformatados como `> retomando o problema`. LER antes de tocar.
- `docs/893CorbettAnderson1995.pdf` (Corbett & Anderson 1995) — PDF escaneado. Não precisa ser lido na fase 1 (slides serão apagados), mas referência fica para a fase 4 (MODEL-01).

### Codebase context já gerado

- `.planning/codebase/STRUCTURE.md` — diretórios; "Slide novo na apresentação" section.
- `.planning/codebase/CONVENTIONS.md` — convenções de redação (sem em-dash), commit message style (lowercase português, tipo `apresentacao:` ou `slide-XYZ:`).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- Classe `.deck-topic` (CSS em `theme-unifacens.css`): já implementa o padrão `> [seção]` com caret piscante. Usada hoje pelos slide-problem, slide-fig, slide-code, slide-kcfig, slide-phases no working tree atual.
- Classe `.caret.blink`: animação CSS pronta (1.05s steps(1) infinite).
- Marca d'água Facens `<svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>`: presente em todos os slides de conteúdo; manter.
- Inventário visual em `apresentacao/STYLE.md` "Inventário de slides (ordem atual)" tabela: serve como mapa antes/depois.

### Established Patterns

- Estrutura de cada slide: `<section data-background-color="#F1F6FB"><div class="deck-slide slide-XYZ">...</div></section>`. Reveal.js força `display:block` no `<section>`; layout no `<div>` interno. NUNCA mudar isso.
- Comentários no markup acima de cada `<section>`: `<!-- ============ SLIDE · descrição ============ -->`. Manter formato.
- Citação direta curta: `<blockquote class="rel-quote">&ldquo;...&rdquo; <span class="src">(Autor, ano, p. X, tradução nossa)</span>.</blockquote>`. Para classes `slide-problem` use `.prob-quote` + `<span class="src">`.
- Rodapé fonte: `<p class="rel-cite">Fonte: ...</p>` em template correlato, `<p class="prob-cite">`/`<p class="fig-fonte">`/`<p class="code-fonte">`/`<p class="kcfig-fonte">`/`<p class="phases-fonte">` em outros templates.

### Integration Points

- Único arquivo HTML a editar: `apresentacao/index.html`.
- CSS pode precisar de ajuste em `apresentacao/assets/theme-unifacens.css` SE alguma regra órfã de `.rel-kicker`/`.rel-title` ficar sem uso após reformatação (verificar e remover/anotar).
- Browser: `cd apresentacao && python3 -m http.server 8000` → http://127.0.0.1:8000 (per STYLE.md). Navegação por hash `#/N` (0-based).
- Sem build system; ediçāo direta de HTML+CSS, recarregar página.

### Slides existentes mapeados (estado HEAD; índice 0-based)

| # | classe | requirement na fase | ação |
|---|---|---|---|
| 0 | slide-cover-brand | (já validado) | inalterado |
| 1 | slide-title-tcc | (já validado) | inalterado |
| 2 | slide-agenda | (já validado, AGENDA-01 é fase 5) | inalterado |
| 3 | slide-related (Martins p1) | REFORMAT-01 | trocar cabeçalho para `> introdução`, remover `.rel-title`+`.rel-sub` |
| 4 | slide-problem (Martins p2 "O problema") | REFORMAT-04 | trocar cabeçalho para `> retomando o problema`, mover para fim, antes de slide-fig e depois de Martins p3 vizinho |
| 5 | slide-problem (Martins p3 "Dentro dos conceitos técnicos") | REFORMAT-04 | trocar cabeçalho para `> retomando o problema`, mover para fim, adjacente a Martins p2 |
| 6 | slide-kcfig | REFORMAT-05a | trocar cabeçalho para `> kcs semânticos extraídos`, mover para fim, antes do trio Martins+fig |
| 7 | slide-fig | REFORMAT-05b | trocar cabeçalho para `> evolução por dificuldade`, mover para fim, imediatamente após Martins p3 |
| 8 | slide-code | REFORMAT-05c | trocar cabeçalho para `> o que o code-dkt olha`, mover para fim, antes do trio Martins+fig |
| 9 | slide-related (Zorić p1) | MERGE-01 | fundir com #10 em um único section com cabeçalho `> mineração de dados educacionais` |
| 10 | slide-related slide-methods (Zorić p2) | MERGE-01 | fundir com #9; este slide deixa de existir |
| 11 | slide-phases (Zorić p3) | REFORMAT-02 | trocar cabeçalho para `> as quatro fases da edm` |
| 12 | slide-related (Yağcí p1) | REFORMAT-03 | fundir com #13 em um único section com cabeçalho `> da edm ao knowledge tracing` |
| 13 | slide-related slide-bridge (Yağcí p2) | REFORMAT-03 | fundir com #12; este slide é o sobrevivente (mantém citação p.2, sequência, parágrafo) |
| 14 | slide-related slide-corbett (motivação) | REMOVE-01 | apagar |
| 15 | slide-related slide-corbett (modelo BKT) | REMOVE-01 | apagar |

(Working tree tem os slides Yağcí adicionados; estado HEAD original termina em #15 Corbett. Verificar exato estado no início do plano.)

</code_context>

<specifics>
## Specific Ideas

- Working tree atual carrega nomes dos autores (Erick Miranda Viana, Leonardo Kuntz Oliveira, Victor Santos Borba) na capa TCC e os dois slides Yağcí que serão fundidos. O plano deve decidir como tratar essas mudanças antes de começar (recomendação: integrar).
- Cabeçalho `> retomando o problema` é deliberadamente em minúsculas (segue convenção de `> [seção]` mono Cascadia em #5b6472, conforme STYLE.md "Tipografia").
- Citação literal de Yağcı a manter: "Outra dimensão da análise de aprendizagem é prever o desempenho acadêmico dos estudantes [...] e determinar os estudantes potencialmente em risco de reprovação" (p. 2, tradução nossa). NÃO usar a citação da p. 1 do p1.
- Sequência horizontal do slide fundido Yağcí já existe como `.bridge-seq` no slide #13; reutilizar markup como-é, só trocar o cabeçalho acima.
- Yağcí: caractere "ı" sem ponto (Yağcı, não Yagci) e "ğ" com breve — copiar do markup existente, evitar transliterar.

</specifics>

<deferred>
## Deferred Ideas

- Cronologia "BKT (Corbett & Anderson, 1995) → DKT (Piech, 2015) → Code-DKT (Shi, 2022)" com a citação Corbett: fase 4, MODEL-01.
- Atualização do CSS para limpar regras órfãs de `.rel-kicker`/`.rel-title` se elas ficarem sem uso: pode entrar na fase 1 ou ser deferida; decidir no plano.
- AGENDA-01 (revisão do slide de agenda): fase 5; depende do inventário final.
- Texto do TCC, PDF dos slides, speaker notes: fora de escopo do projeto (TCC 2 / outra milestone).

</deferred>

---

*Phase: 1-Reformatação da base*
*Context gathered: 2026-05-27*
