# Apresentação TCC em HTML (reveal.js)

Protótipo da apresentação do TCC reconstruída a partir do template oficial
`Layout PPTs UniFacens_TCC.pptx`, usando reveal.js. Por enquanto cobre os 3
primeiros slides (abertura de marca, capa do TCC e agenda).

## Como abrir

Opção 1, direto no navegador: dê duplo clique em `index.html` (precisa de
internet, pois o reveal.js é carregado por CDN).

Opção 2, servidor local (recomendado para evitar restrições de `file://`):

```bash
cd apresentacao
python3 -m http.server 8000
# abrir http://127.0.0.1:8000 no navegador
```

## Navegação

- Setas do teclado ou clique nos controles para trocar de slide
- `Esc` abre a visão geral (overview) de todos os slides
- `S` abre a visão do apresentador (speaker notes)
- `F` entra em tela cheia
- Para exportar PDF: abrir `?print-pdf` ao final da URL e usar Imprimir do navegador

## Estrutura

```
apresentacao/
├── index.html                      # os slides (marcação)
├── assets/
│   ├── theme-unifacens.css         # tema com a identidade visual UniFacens
│   ├── logo-unifacens-white.svg    # wordmark branco (extraído do pptx)
│   └── symbol.svg                  # símbolo monocromático (marca d'água)
└── README.md
```

## Paleta extraída do template

| Cor | Hex | Uso |
|---|---|---|
| Azul de marca | `#2667FF` | abertura + faixa da agenda |
| Grafite | `#202124` | capa do TCC |
| Claro azulado | `#F1F6FB` | fundo de conteúdo |
| Cinza do símbolo | `#DDE2EC` | marca d'água |

Fonte: Segoe UI (com fallback para fontes de sistema sans-serif).
