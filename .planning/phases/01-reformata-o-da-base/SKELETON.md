---
phase: 01-reformata-o-da-base
type: skeleton
created: 2026-05-27
---

# Walking Skeleton: Apresentação TCC 1 (fase 1)

## O que é o esqueleto andante aqui

Este projeto NÃO é um SaaS. É um deck reveal.js single-file. O Walking Skeleton da fase 1 é simples:

> **Um deck `apresentacao/index.html` que abre no browser, carrega sem erro de console, navega do slide 0 até o último slide via setas, e exibe o novo padrão de cabeçalho `> [seção]` em todos os 7 slides reformatados, com Corbett removido e Zorić/Yağcí fundidos.**

A "thinnest end-to-end slice" é o próprio deck navegável fim-a-fim. Não há backend, banco, autenticação, ou rede.

## Comando do dev server

```bash
cd apresentacao && python3 -m http.server 8000
# abrir http://127.0.0.1:8000
```

Navegação:
- setas direita/esquerda do teclado (reveal.js)
- ou hash `#/N` (0-based, ex.: `http://127.0.0.1:8000/#/9` para o slide 9)

Atenção: `http.server` não envia cache headers. Ao editar CSS, browser pode servir versão antiga. Para forçar reload: subir em outra porta ou usar Ctrl+Shift+R.

## Arquitetura travada para todas as fases (1-5)

| Item | Decisão |
|---|---|
| Framework | reveal.js 5.1.0 via CDN (`<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js">`) |
| Slide dim | 1280×720 (`Reveal.initialize({ width:1280, height:720 })`) |
| Single HTML | `apresentacao/index.html` é o ÚNICO ponto de entrada |
| CSS | `apresentacao/assets/theme-unifacens.css` (paleta UniFacens) |
| Estrutura por slide | `<section><div class="deck-slide slide-XYZ">…</div></section>` (reveal força `display:block` na `<section>`; layout vai no `<div>` interno) |
| Cabeçalho padrão (fase 1+) | `<p class="deck-topic"><span class="ps1">&gt;</span>nome da seção<span class="caret blink"></span></p>` como UMA única linha |
| Autor no slide | aparece SOMENTE em `<p class="rel-cite">Fonte: …</p>` no rodapé; NUNCA no corpo nem em `<h2>` |
| Tipografia | Cascadia (mono, `--mono`) para tópico `> ...`; Arial 30px para títulos; Arial 21-23px para corpo |
| Marca d'água | `<svg class="wm">` Facens no canto superior direito de todo slide de conteúdo |
| Linha "Fonte:" | UMA linha por slide; sobrenome + ano corretos; "adaptado de" preservado quando aplicável |
| Citação direta | só quando a frase específica É o argumento (caso quantitativo Martins p2/p3); paráfrase indireta com autor parentético é o padrão |
| Sem em-dash em prosa | usar vírgula, dois-pontos ou parênteses |
| Termos estrangeiros | em itálico e minúsculas (`<i>knowledge tracing</i>`); nomes de modelos (BKT, Code-DKT) ficam como estão |

## Layout de diretórios (fixo)

```
apresentacao/
├── index.html                              <- ÚNICO HTML editável nesta fase
├── STYLE.md                                <- design contract (editado na fase 1, D-21)
├── README.md
├── 4. MSGQ-21.01- MANUAL DE TEXTOS TÉCNICOS-REV.17 2.pdf
└── assets/
    ├── theme-unifacens.css                 <- cleanup opcional .rel-kicker/.rel-title órfãos
    └── fig-codedkt-martins-curves.png      <- imagem do slide-fig
```

Nada fora de `apresentacao/` é tocado nesta fase. `STYLE.md` é entregável da própria fase (D-21).

## Inventário de slides após a fase 1 (estado-alvo)

Ordem final esperada no `<section>` raiz, após todos os plans executados:

| # | classe | conteúdo | cabeçalho |
|---|---|---|---|
| 0 | slide-cover-brand | Abertura | (sem cabeçalho) |
| 1 | slide-title-tcc | Capa do TCC | (sem cabeçalho) |
| 2 | slide-agenda | Agenda | (sem cabeçalho temático) |
| 3 | slide-related (Martins p1) | Introdução | `> introdução` |
| 4 | slide-related (Zorić fundido p1+p2) | EDM | `> mineração de dados educacionais` |
| 5 | slide-phases (Zorić p3) | As 4 fases | `> as quatro fases da edm` |
| 6 | slide-related slide-bridge (Yağcí fundido) | Yağcí + ponte | `> da edm ao knowledge tracing` |
| 7 | slide-code OU slide-kcfig | (executor decide ordem entre eles) | `> o que o code-dkt olha` OU `> kcs semânticos extraídos` |
| 8 | slide-kcfig OU slide-code | (o outro) | `> kcs semânticos extraídos` OU `> o que o code-dkt olha` |
| 9 | slide-problem (Martins p2) | O problema | `> retomando o problema` |
| 10 | slide-problem (Martins p3) | Dentro dos conceitos técnicos | `> retomando o problema` |
| 11 | slide-fig | Curva Code-DKT | `> evolução por dificuldade` |

Total: 12 slides (era 16; Corbett ×2 removidos; Zorić p1+p2 fundido; Yağcí p1+p2 fundido).

Restrições obrigatórias do DOM final (D-17):
- (a) Martins p2 e Martins p3 adjacentes
- (b) slide-fig imediatamente após Martins p3
- (c) slide-code e slide-kcfig precedem o trio Martins+fig

## Ritual de verificação fim-a-fim

Após cada plan (e obrigatoriamente ao fim do último):

```bash
# 1. subir dev server
cd apresentacao && python3 -m http.server 8000

# 2. abrir browser
# http://127.0.0.1:8000

# 3. abrir DevTools (F12), aba Console
# 4. navegar com → do slide 0 até o último
# 5. console deve ficar limpo (zero error)

# 6. verificar contagem de slides
# em outro terminal:
grep -c '<section data-background' apresentacao/index.html
# após fase 1: deve retornar 12 (era 16)

# 7. verificar cabeçalhos travados
grep -c '> introdução' apresentacao/index.html                  # 1
grep -c '> mineração de dados educacionais' apresentacao/index.html  # 1
grep -c '> as quatro fases da edm' apresentacao/index.html      # 1
grep -c '> da edm ao knowledge tracing' apresentacao/index.html # 1
grep -c '> retomando o problema' apresentacao/index.html        # 2 (Martins p2 e p3)
grep -c '> kcs semânticos extraídos' apresentacao/index.html    # 1
grep -c '> evolução por dificuldade' apresentacao/index.html    # 1
grep -c '> o que o code-dkt olha' apresentacao/index.html       # 1

# 8. verificar Corbett removido
grep -c 'slide-corbett' apresentacao/index.html                 # 0

# 9. verificar tópico antigo zerado nos slides reformatados
# (>trabalhos correlatos só pode sobreviver dentro de comentários ou no STYLE.md/.history)
grep -v '^<!--' apresentacao/index.html | grep -c '>trabalhos correlatos'   # 0
```

## Critério de "esqueleto andante operacional" (gate de fim de fase 1)

Atende todos os Success Criteria 1-8 do ROADMAP fase 1:

1. ✅ `apresentacao/index.html` abre no browser sem erro de console e a navegação reveal.js funciona do primeiro ao último slide
2. ✅ Slide Martins p1 exibe `> introdução`; autor só em "Fonte:"
3. ✅ Slide Zorić p3 exibe `> as quatro fases da edm`
4. ✅ Slide Yağcí exibe `> da edm ao knowledge tracing` com gancho sobre acompanhamento ao longo do tempo
5. ✅ Slide Zorić fundido p1+p2 com `> mineração de dados educacionais` num único slide
6. ✅ Corbett removido; `grep -c slide-corbett` retorna 0
7. ✅ Martins p2/p3 movidos para o fim do deck
8. ✅ slide-fig, slide-code, slide-kcfig reformatados ao novo padrão de cabeçalho

A partir daqui, fases 2-5 inserem novos slides nos gaps já abertos (após Martins p1, após Yağcí, antes do trio Martins+fig) sem precisar de outra rodada de movimentação.
