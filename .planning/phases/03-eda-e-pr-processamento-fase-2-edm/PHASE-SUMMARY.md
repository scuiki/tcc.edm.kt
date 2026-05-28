---
phase: 03-eda-e-pr-processamento-fase-2-edm
status: complete
plans:
  - 01: MARKER-02 (Fase 2 EDM done)
  - 02: EDA-02 (pré-processamento, aproximação ao protocolo)
  - 03: EDA-01 (tabela A1..A5)
  - 04: EDA-03 (curvas de aprendizado) + EDA-04 (X-Grade × engajamento)
requirements:
  - EDA-01
  - EDA-02
  - EDA-03
  - MARKER-02
  - PENDING-02
---

## O que esta fase entregou

A Fase 3 do GSD da apresentação fechou o bloco da Fase 2 da EDM
(Preparação dos Dados) no deck reveal.js, totalizando **21 slides**
(eram 16 pós-fase 2 + 5 novos). A sequência narrativa final entre o
MARKER-01 (Fase 1 EDM concluída) e o MARKER-02 (Fase 2 EDM concluída) é:

```
#/9  MARKER-01     Fase 1 EDM concluída (Definição do Problema)
#/10 INTRO-01      O dataset CSEDM em ProgSnap2 (Price, 2020) — MOVIDO
                   da seção Introdução para abrir a Fase 2 EDM
#/11 EDA-01        Como navegamos o CSEDM (Tabela 1, A1..A5)
#/12 EDA-03        Como o aprendizado se manifesta (Figura 1, curvas)
#/13 EDA-04        Engajamento e desempenho (Figura 2, X-Grade boxplot)
#/14 EDA-02        Aproximação ao protocolo (pré-processamento Shi)
#/15 MARKER-02     Fase 2 EDM concluída (Preparação dos Dados)
```

## Componentes reutilizáveis estabelecidos

**CSS (`apresentacao/assets/theme-unifacens.css`):**
- `.eda-title` — título acima de tabela/figura ABNT.
- `.eda-grid` + variantes — tabela ABNT/IBGE 1993 (3 bordas horizontais,
  fundo transparente, última coluna em azul UniFacens).
- `.eda-fig` + `.eda-fig--wide` + `.eda-fig--compact` — container de
  figura com 3 perfis de largura/altura.
- `.eda-insight` — frase de conclusão pós-figura.
- `.eda-source` — fonte centralizada abaixo da tabela/figura no padrão
  ABNT.

**Scripts Python reproducíveis (`scripts/`):**
- `build_eda_correct_rate_by_assignment.py` — gerou PNG explorado num
  checkpoint do Plan 03-03 (não usado no slide final; fica disponível).
- `build_eda_learning_curves.py` — gera Figura 1 do EDA-03.
- `build_eda_xgrade_by_completed.py` — gera Figura 2 do EDA-04.

Todos os PNGs usam fundo transparente, tipografia em preto puro
`#000000`, fontes ampliadas para projeção e paleta UniFacens.

## Decisões consolidadas (D-66, D-67)

- **D-66e:** Slide de dataset pertence à Fase 2 EDM (Preparação dos
  Dados), não à Introdução. Aplica a INTRO/MODEL/CLOSE futuros.
- **D-66f:** Slides EDA não afirmam dificuldade entre assignments antes
  da Fase 3 (Modelagem) introduzir KCs. Descrição neutra é suficiente.
- **D-66g:** Padrão ABNT para tabelas em slides (título com en-dash, 3
  bordas horizontais, fundo transparente, fonte centralizada abaixo).
- **D-66h:** Scatter PCA descartado por incoerência narrativa (239 ≠
  413/410 dos demais slides EDA). Substituído por curvas de aprendizado
  + boxplot X-Grade.
- **D-66i:** EDA-04 acrescentado em consenso (5 slides na Fase 2 EDM,
  não 4 previstos).
- **D-66j:** EDA-02 (pré-processamento) fecha o bloco da Fase 2 EDM,
  imediatamente antes do MARKER-02. Ordem narrativa: descrever dataset
  → navegá-lo → observar aprendizado → relação engajamento/desempenho
  → apresentar pré-processamento → fechar Fase 2.
- **D-67d/e:** Componente `.slide-marker` reusado mecanicamente
  (4 deltas vs MARKER-01); MARKER-02 sem CSS novo. "Estudantes" (não
  "alunos") em prosa acadêmica, com exceção para citação direta literal.

## Iterações pós-checkpoint

Cada plan teve checkpoints visuais com 1 a 4 iterações:
- 03-01 (MARKER-02): 1 iteração (mecânico).
- 03-02 (EDA-02): 1 iteração (microcópia + reposicionamento + 23,68%).
- 03-03 (EDA-01): 3 iterações (mover INTRO-01, refazer tabela ABNT,
  ajustes de coluna `Participação` e estilo).
- 03-04 (EDA-03 + EDA-04): 4 iterações (rejeitar scatter PCA, alinhar
  dois gráficos novos, ajustar tipografia, alinhar insight).

Total: 9 iterações para 5 slides + 1 reordenação + 10 substituições
"alunos" → "estudantes". Convergência ágil dentro do padrão de 1 a 3
iterações por slide observado na fase 2.

## Critérios de saída — todos atendidos

- [x] Todos os 4 plans (03-01..03-04) marcados como complete.
- [x] PENDING-02 resolvido (figura de insight escolhida em discussão:
      curvas de aprendizado + boxplot X-Grade).
- [x] STYLE.md sincronizado com o estado real (21 sections; gap da
      Fase 3 consumido).
- [x] Componentes CSS ABNT estabelecidos e prontos para reuso na
      Fase 4 (slides MODEL-*).
- [x] Scripts Python reprodutíveis para todas as figuras (sem PNGs
      "mágicos" no repositório).
- [x] Zero em-dash em prosa nova (D-70 herdado).
- [x] Zero citação direta literal em slides EDA (D-69 herdado).

## Próximo: Fase 4 (Modelagem)

Slides MODEL-01..05 entrarão no gap entre MARKER-02 (`#/15` atual) e
slide-code (`#/16` atual), reaproveitando slide-code como MODEL-03.
Linhagem de KT a introduzir: Corbett e Anderson (1995) no MODEL-01,
Piech (2015) no DKT, Shi (2022) no Code-DKT, Duan (2025) no MODEL-05.
