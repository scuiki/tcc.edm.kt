# Phase 1: Reformatação da base - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-27
**Phase:** 1-Reformatação da base
**Areas discussed:** Cabeçalhos pendentes, Yağcí: fundir ou não, Mover DOM ou só cabeçalho, Atualização do STYLE.md, Microcópia 'Fonte:', REMOVE-01 Corbett: placeholder?

---

## Seleção inicial de áreas

| Opção apresentada | Selecionado |
|---|---|
| Working tree atual | |
| Cabeçalhos pendentes | ✓ |
| Yağcí: fundir ou não | ✓ |
| Mover DOM ou só cabeçalho | ✓ |

**Notas:** Working tree atual ficou implícito; usuário não quis discutir, fica como decisão do plano.

---

## Cabeçalhos pendentes

### REFORMAT-04 (Martins p2 + Martins p3)

| Opção | Descrição | Selecionado |
|---|---|---|
| Mesmo `> retomando o problema` | Recomendado. Continuidade no bloco de fechamento e amarra com 'retomando' o gancho lançado na introdução. | ✓ |
| p2 = `> retomando o problema`, p3 = `> dentro dos conceitos técnicos` | Diferencia: p2 mantém retomada global; p3 estreita foco para subcategoria técnica. | |
| Mesmo `> dificuldades reportadas` | Foca o conteúdo em si (a lista), não a ideia de retomada. | |

**User's choice:** Mesmo `> retomando o problema`

---

### REFORMAT-05a (slide-kcfig)

| Opção | Descrição | Selecionado |
|---|---|---|
| `> kcs e dificuldades` | Recomendado. Curto, descreve diretamente mapeamento KC ↔ dificuldade Martins; neutro para MODEL-07 ou CLOSE-01. | |
| `> dos kcs às dificuldades` | Sugere leitura direcional do mapa; pressupõe KCs já estabelecidos antes. | |
| `> kcs semânticos extraídos` | Enfatiza origem (pipeline KCGen-KT / Duan). Melhor encaixe se vier após MODEL-07. | ✓ |

**User's choice:** `> kcs semânticos extraídos`
**Notes:** Posiciona o slide como saída do pipeline, não como mapeamento.

---

### REFORMAT-05b (slide-fig)

| Opção | Descrição | Selecionado |
|---|---|---|
| `> curva de aprendizado` | Recomendado. Curto, descreve conteúdo direto; subtítulo carregaria 'por dificuldade de Martins'. | |
| `> quão difícil de aprender` | Mantém pergunta retórica do título original; força reflexão antes de ver as curvas. | |
| `> evolução por dificuldade` | Foca no eixo X (oportunidade) e na comparação entre dificuldades. Mais técnico, menos narrativo. | ✓ |

**User's choice:** `> evolução por dificuldade`

---

### REFORMAT-05c (slide-code)

| Opção | Descrição | Selecionado |
|---|---|---|
| `> o que o code-dkt olha` | Recomendado. Mantém pergunta narrativa do título original; ressalta interpretabilidade (gancho TCC 2). | ✓ |
| `> atenção do code-dkt` | Técnico, nomeia o mecanismo (atenção code2vec). Perde o gancho do 'olha'. | |
| `> code-dkt lê o código` | Reforça contraste com BKT/DKT que só veem acerto/erro. | |

**User's choice:** `> o que o code-dkt olha`

---

## Yağcí: fundir ou não

### REFORMAT-03

| Opção | Descrição | Selecionado |
|---|---|---|
| Fundir em 1 slide | Recomendado. Mantém citação p2, sequência 3 passos, parágrafo de fechamento. Corta bullets de algoritmos/acurácia do p1. | ✓ |
| Manter 2 slides | p1 mantém apresentação Yağcí; p2 mantém ponte. Ambos com mesmo cabeçalho. Mais ar, dobra tempo de fala. | |
| Fundir, versão enxuta | Slide único só com sequência + frase 'KT dá o passo seguinte'. Sem citação direta. | |

**User's choice:** Fundir em 1 slide
**Notes:** Conteúdo a manter: citação p2 (p. 2, tradução nossa), sequência `.bridge-seq` (3 passos), parágrafo `.bridge-text` ('o KT dá o passo seguinte...'). Descartar do p1: citação inicial, subtítulo, bullets algoritmos/acurácia/1854 alunos.

---

## Mover DOM ou só cabeçalho

### Movimentação dos 5 slides (Martins p2, Martins p3, slide-fig, slide-code, slide-kcfig)

| Opção | Descrição | Selecionado |
|---|---|---|
| Só reformata cabeçalho | Recomendado. Diffs menores, fase 4 cuida da reordenação. Deck temporariamente fora de ordem entre fase 1 e 4. | |
| Mover + reformatar agora | Reformata cabeçalho E move slides para perto do fim. Maior diff por slide, ordem ainda furada. | ✓ |
| Mover apenas Martins p2/p3 | Meio termo: Martins movidos, slide-fig/code/kcfig ficam até fase 4. | |

**User's choice:** Mover + reformatar agora
**Notes:** Justificativa implícita: cabeçalho `> retomando o problema` só faz sentido com slides reposicionados.

---

### Ordem dos 5 slides realocados

| Opção | Descrição | Selecionado |
|---|---|---|
| Ordem narrativa final | Recomendado. slide-code → slide-kcfig → Martins p2 → Martins p3 → slide-fig. Fase 4 insere nos gaps. | |
| Agrupado por bloco | Bloco modelagem (slide-code + slide-kcfig) → bloco fechamento (Martins p2 + Martins p3 + slide-fig). | |
| Apenas garantir agrupamento Martins+fig | Martins p2/p3 adjacentes; slide-fig logo após. slide-code e slide-kcfig livres. Aceita churn na fase 4. | ✓ |

**User's choice:** Apenas garantir agrupamento Martins+fig
**Notes:** Restrições: (a) Martins p2 e p3 adjacentes; (b) slide-fig imediatamente após Martins p3; (c) slide-code e slide-kcfig precedem o trio.

---

## Atualização do STYLE.md

| Opção | Descrição | Selecionado |
|---|---|---|
| Atualizar STYLE.md na fase 1 | Recomendado. Reescrever seção cabeçalho, remover regra dos correlatos antiga, atualizar inventário. Commit junto com a fase. | ✓ |
| Atualizar STYLE.md em sub-task separada | Sub-task própria no plano, executada após os slides. Commit atômico só para STYLE.md. | |
| Adiar para fase 5 | Risco: STYLE.md dessincronizado durante fases 2-4. | |

**User's choice:** Atualizar STYLE.md na fase 1
**Notes:** Atualizar: seção 'Cabeçalho de todo slide após a AGENDA', remover regra dos correlatos em 'Regras de redação', reescrever 'Inventário de slides'.

---

## Microcópia 'Fonte:'

| Opção | Descrição | Selecionado |
|---|---|---|
| Manter o que cada slide já tem | Recomendado. Não uniformizar; conteúdo atual já segue manual ABNT. Garantir UMA linha 'Fonte:' correta no rodapé. | ✓ |
| Formato uniforme curto | Padronizar para 'Fonte: Sobrenome (ano).' sem páginas, sem 'adaptado de'. Risco: descumpre manual MSGQ-21.01. | |
| Formato com página | Sempre incluir página. Mais rigoroso, mas polui rodapé. | |

**User's choice:** Manter o que cada slide já tem

---

## REMOVE-01 Corbett: placeholder?

| Opção | Descrição | Selecionado |
|---|---|---|
| Apagar limpo, sem placeholder | Recomendado. CONTEXT da fase 4 lembrará da citação na cronologia MODEL-01. Sem comentários órfãos. | ✓ |
| Comentário TODO no markup | Apagar e deixar `<!-- TODO fase 4 MODEL-01: ... -->`. Lembrete visível no diff da fase 4. | |
| Capturar como deferred no REQUIREMENTS | Nota em REQUIREMENTS.md sob MODEL-01. Sem poluição do markup. | |

**User's choice:** Apagar limpo, sem placeholder

---

## Claude's Discretion

- Working tree atual (mudanças não commitadas em `apresentacao/`): plano decide entre descartar, stashear, integrar ou commitar como WIP.
- Ordem exata entre slide-code e slide-kcfig.
- Cadência de validação no browser (por slide ou em lote).
- Granularidade dos commits dentro da convenção atômica.

## Deferred Ideas

- Cronologia BKT → DKT → Code-DKT com citação Corbett: fase 4 MODEL-01.
- Limpeza de regras CSS órfãs de `.rel-kicker`/`.rel-title`: pode entrar na fase 1 ou deferida.
- AGENDA-01: fase 5.
- Texto TCC, PDF, speaker notes: outra milestone.
