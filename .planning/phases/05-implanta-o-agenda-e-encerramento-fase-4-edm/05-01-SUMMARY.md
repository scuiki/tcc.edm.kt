---
phase: 05-implanta-o-agenda-e-encerramento-fase-4-edm
plan: 01
status: complete
requirements: [MARKER-04]
commits:
  - e752fce
  - d27f166
---

# Plan 05-01 — MARKER-04 (Fase 4 EDM planejada)

## Resultado

- Modificador CSS `.marker-pill--planned` adicionado em `apresentacao/assets/theme-unifacens.css` linhas 431-441 (12 linhas novas; bloco entre `.marker-pill--pending .marker-pill-icon` e `.marker-arrow`).
- Section MARKER-04 inserida em `apresentacao/index.html` linhas 732-776 (após `</section>` do MARKER-03, antes do `</div>` de fechamento de `<div class="slides">`); classe `slide-marker--phase4`; 45 linhas novas.
- Deck: 27 → 28 sections. Posição intermediária do MARKER-04: `#/27`. Posição final esperada: `#/29` (após inserção de TOOL-01 e TOOL-03 em plans 05-04 e 05-05).
- Visualmente: 3 pills `--done` (Definição do Problema, Preparação dos Dados, Modelagem e Avaliação) com `&check;` + badge `[done]`; pill 4 (Implantação) `--planned` com `&#x25CB;` + badge `[planned]`, borda tracejada cinza azulado `#5b6472`, **sem animação**.

## Estética escolhida no checkpoint

**Alt A do RESEARCH §Code Example 1** (default): `border-style: dashed`, cor `#5b6472`, ícone círculo vazio `&#x25CB;` com a mesma cor e borda tracejada. Aprovado pelo reviewer no checkpoint visual (`approved-alt-a`) com 0 iterações textuais.

Alternativas B (cor `--uni-blue` com opacity 0.7 + ícone reload estático) e C (ícone calendário/relógio + borda sólida) **não exploradas** porque Alt A já satisfez os critérios de distinguibilidade (vs `--pending` sólido e vs `--running` animado) e honestidade epistemológica (D-96a: Implantação proposta no TCC 1 mas não executada).

## Linhas exatas adicionadas

### `theme-unifacens.css` linhas 431-441

```css
/* Planned: ainda nao executada (TCC 2); texto e borda em cinza azulado tracejado,
   icone como circulo vazio com borda tracejada, sem animacao; visualmente
   diferente de --pending (solido) e de --running (anima). */
.marker-pill--planned {
  color: #5b6472;
  border-style: dashed;
}
.marker-pill--planned .marker-pill-icon {
  color: #5b6472;
  border: 1.5px dashed #5b6472;
}
```

### `index.html` linhas 732-776 (45 linhas)

Copy-paste integral da section MARKER-03 (linhas 687-730) com **4 deltas** aplicados (per D-96 + RESEARCH §Code Example 4):

1. Comentário HTML: `... fase 3 concluida ...` → `... fase 4 planejada ...`
2. Classe: `slide-marker--phase3` → `slide-marker--phase4`
3. Pill 3 (Modelagem e Avaliação): mantém `--done` + `&check;` + `[done]` (entregue na fase 4 do projeto)
4. Pill 4 (Implantação): `--running` → `--planned`; ícone `&#x21BB;` → `&#x25CB;`; badge `[running]` → `[planned]`

Tudo o resto idêntico (título, watermark, rodapé, estrutura `.marker-track`/`.marker-stage`/`.marker-arrow`).

## Acceptance gates

| Gate | Esperado | Obtido | Status |
|---|---|---|---|
| `grep -c "marker-pill--planned" theme-unifacens.css` | ≥ 2 | 2 | ✓ |
| `grep "animation" theme-unifacens.css \| grep planned` | 0 linhas | 0 | ✓ |
| `grep -c "border-style: dashed\|border: 1.5px dashed" theme-unifacens.css` | ≥ 1 | 2 | ✓ |
| Regras existentes `--done`/`--running`/`--pending` intactas | mesmas linhas | 4 ocorrências (intactas) | ✓ |
| `grep -c "<section " index.html` | 28 | 28 | ✓ |
| `grep -c "slide-marker--phase4" index.html` | 1 | 1 | ✓ |
| `grep -c "marker-pill--planned" index.html` | 1 | 1 | ✓ |
| `grep -c '\[planned\]' index.html` | 1 | 1 | ✓ |
| `grep -c '\[running\]' index.html` | 1 (PLAN.md) | 3 (real) | desvio benigno |
| `grep -c "AS QUATRO FASES DA EDM" index.html` | 4 | 4 | ✓ |
| Ordem phase1 < phase2 < phase3 < phase4 no DOM | crescente | linhas 185 < 334 < 689 < 734 | ✓ |
| Sem `—` em prosa nova | igual antes/depois | igual | ✓ |
| HTTP 200 em http://127.0.0.1:8003/index.html | 200 | 200 | ✓ |

**Desvio benigno do `[running] == 1`:** a gate da PLAN.md assumia que só MARKER-03 teria `[running]` no deck. Na realidade MARKER-01 (linha 204) e MARKER-02 (linha 361) também carregam `[running]` para sinalizar a fase imediatamente seguinte (padrão CI/CD pré-existente das fases 2-4). MARKER-04 NÃO introduziu novo `[running]`; usa `[planned]`. Não é regressão.

## Iterações pós-checkpoint

Zero. Reviewer aprovou Alt A diretamente; sem mudanças de cor, ícone ou borda.

## Decisões ad-hoc registradas

Nenhuma. Todas as decisões prévias (D-96a..D-96f, D-92.1, D-100) foram aplicadas literalmente; nenhuma decisão nova surgiu durante a execução.

## Commits

- `e752fce` apresentacao: modificador .marker-pill--planned (Alt A: dashed cinza azulado)
- `d27f166` apresentacao: slide MARKER-04 - quatro fases EDM com Implantacao planned (Zoric, 2020)
