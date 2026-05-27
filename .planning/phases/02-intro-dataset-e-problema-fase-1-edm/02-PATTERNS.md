# Phase 2: Intro, Dataset e Problema (Fase 1 EDM) - Pattern Map

**Mapped:** 2026-05-27
**Files analyzed:** 3 (`apresentacao/index.html`, `apresentacao/assets/theme-unifacens.css`, `apresentacao/STYLE.md`)
**Analogs found:** 6 / 6 (todos os patterns "antes" e "depois" vivem dentro do próprio `index.html` pós-fase 1 e do `theme-unifacens.css`)

> Esta fase **insere** 4 sections novos e **adiciona** 1 bloco de classes CSS para um componente reutilizável (`.slide-marker`). Não modifica conteúdo existente exceto pela correção pontual de uma sentença no STYLE.md (linha 129). Os analogs são, portanto, blocos vivos do próprio `index.html` (slide 4 Zorić fundido, slide 6 Yağcí fundido com `.bridge-seq`) e do `theme-unifacens.css` (`.slide-related`, `.bridge-seq`, `.deck-topic`, classes `.rel-cite` / `.kcfig-fonte` / `.fig-fonte`).

---

## File Classification

| Modificação | Papel | Fluxo de edição | Analog (dentro do próprio arquivo) | Match |
|---|---|---|---|---|
| `apresentacao/index.html` § INTRO-01 (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-related` Zorić fundido (linhas 101-111) | exato |
| `apresentacao/index.html` § INTRO-03a (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-related` Zorić fundido (linhas 101-111) | exato |
| `apresentacao/index.html` § INTRO-03b (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-related` Zorić fundido (linhas 101-111) | exato |
| `apresentacao/index.html` § MARKER-01 (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-bridge .bridge-seq` no slide Yağcí (linhas 134-147) — estrutura horizontal de caixas + setas | role-match (estende com `--done`/`--pending`) |
| `apresentacao/assets/theme-unifacens.css` § bloco `.slide-marker` (novo) | utility classes (componente reutilizável MARKER-02/03/04) | CSS-append | bloco `.slide-bridge .bridge-seq` linhas 197-210 + `.kcfig-fonte` linhas 297-300 (rodapé centralizado) | role-match |
| `apresentacao/STYLE.md` linha 129 | docs (sentença obsoleta) | sentence-replace | as próprias linhas 127-132 (§"Gaps reservados") | identidade |

**Não há "no analog found" nesta fase.** Toda transformação tem template-base vivo no codebase.

---

## Pattern Assignments

### `apresentacao/index.html` § INTRO-01 (`> o dataset csedm`)

**Analog primário:** slide 4 Zorić fundido (`apresentacao/index.html` linhas 100-111).

**Estrutura externa canônica** (linhas 100-111, copiar literalmente as 3 bordas: comentário, `<section>`, `<div class="deck-slide slide-related">` + `<svg class="wm">`):

```html
<!-- ============ SLIDE · Mineração de Dados Educacionais (Zorić, 2020) — fusão p1+p2 ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>mineração de dados educacionais<span class="caret blink"></span></p>

    <p class="rel-lead">Nosso trabalho aplica o processo de mineração de dados educacionais (<i>Educational Data Mining</i>, EDM), área interdisciplinar que combina mineração de dados, estatística e aprendizado de máquina para apoiar decisões pedagógicas (Zorić, 2020). Tarefas típicas incluem classificação, agrupamento, predição e associação.</p>

    <p class="rel-cite">Fonte: Zorić (2020).</p>
  </div>
</section>
```

**Adaptações específicas de INTRO-01:**

1. Comentário acima do `<section>`:
   ```html
   <!-- ============ SLIDE · INTRO-01 · O dataset CSEDM em ProgSnap2 (Price, 2020) ============ -->
   ```
2. Cabeçalho (literal, travado por D-34a):
   ```html
   <p class="deck-topic"><span class="ps1">&gt;</span>o dataset csedm<span class="caret blink"></span></p>
   ```
3. Corpo `<p class="rel-lead">` em primeira pessoa do plural (D-35). Phrasing-alvo (RESEARCH §1.2):
   > "Nosso dataset é o **CSEDM** (curso introdutório CS1 em Java, coleta de 2019, divulgado na competição CSEDM 2021), armazenado em **ProgSnap2** (Price, 2020), formato que registra cada evento de programação do estudante (edição, compilação, execução), preservando o histórico completo das tentativas a cada problema."
4. Bloco visual dos 3 números (D-38 + RESEARCH §2). Opção C recomendada `413 estudantes · 50 problemas · 201 mil eventos`. Markup-alvo (a polir no plano):
   ```html
   <ul class="intro-stats">
     <li><span class="stat-num">413</span> <span class="stat-lbl">estudantes</span></li>
     <li><span class="stat-num">50</span> <span class="stat-lbl">problemas</span></li>
     <li><span class="stat-num">201 mil</span> <span class="stat-lbl">eventos</span></li>
   </ul>
   ```
   Alternativa minimalista (inline em `.rel-lead`): "413 estudantes, 50 problemas, 201 mil eventos."
5. Rodapé Fonte: (D-35, literal):
   ```html
   <p class="rel-cite">Fonte: Price (2020); CSEDM 2021.</p>
   ```

**Gates obrigatórios:**
- [ ] Sem `<blockquote>` (D-43 proíbe citação direta literal)
- [ ] Sem em-dash em prosa (D-44)
- [ ] `*knowledge tracing*` em itálico minúsculas se aparecer (D-46); ProgSnap2 e CSEDM como nomes próprios (não itálico)
- [ ] `(Price, 2020)` parentético no corpo, não autor prominente

---

### `apresentacao/index.html` § INTRO-03a (`> o problema do kt binário`)

**Analog primário:** slide 4 Zorić fundido (linhas 100-111). Estrutura idêntica a INTRO-01, mas com voz **autor prominente** (Shi como sujeito da oração principal).

**Adaptações específicas:**

1. Comentário:
   ```html
   <!-- ============ SLIDE · INTRO-03a · O problema do KT binário (Shi et al., 2022) ============ -->
   ```
2. Cabeçalho (D-34b):
   ```html
   <p class="deck-topic"><span class="ps1">&gt;</span>o problema do kt binário<span class="caret blink"></span></p>
   ```
3. Corpo `<p class="rel-lead">` em voz autor-prominente (D-36). Phrasing-alvo (RESEARCH §1.1):
   > "Shi et al. (2022) apontam que modelos clássicos de *knowledge tracing*, como BKT e DKT, usam apenas a informação de **acerto ou erro** e ignoram a estrutura do código produzido pelo estudante."

   Reforço opcional (segunda sentença, mantém voz autoral): "Toda a riqueza do código submetido fica fora do modelo."
4. Rodapé Fonte: (D-36, literal):
   ```html
   <p class="rel-cite">Fonte: Shi et al. (2022).</p>
   ```

**Gates obrigatórios:**
- [ ] Sem `<blockquote>` (D-43 proíbe citação direta literal — paráfrase indireta apenas)
- [ ] BKT e DKT mencionados literalmente
- [ ] **Code-DKT NÃO mencionado** (Pitfall 3 do RESEARCH; é fase 4)
- [ ] `*knowledge tracing*` em itálico minúsculas
- [ ] Sem em-dash

---

### `apresentacao/index.html` § INTRO-03b (`> sinal pedagógico perdido`)

**Analog primário:** slide 4 Zorić fundido (linhas 100-111). Estrutura idêntica, com voz **autoral consequencial** (sem repetir Shi parentético; ele já foi citado no slide anterior).

**Adaptações específicas:**

1. Comentário:
   ```html
   <!-- ============ SLIDE · INTRO-03b · Sinal pedagógico perdido (adaptado de Shi et al., 2022) ============ -->
   ```
2. Cabeçalho (D-34c):
   ```html
   <p class="deck-topic"><span class="ps1">&gt;</span>sinal pedagógico perdido<span class="caret blink"></span></p>
   ```
3. Corpo `<p class="rel-lead">` autoral, consequencial (D-37). Phrasing-alvo (RESEARCH §1.1):
   > "Como consequência, esses modelos tratam de forma idêntica uma submissão **quase correta** e uma **completamente errada**; o sinal pedagógico estrutural se perde no processo."

   Variantes equivalentes aceitas (CONTEXT linha 78): "acerto parcial vs erro total", "sinal de progresso vs sinal de erro". Manter o argumento.
4. Rodapé Fonte: (D-37, literal):
   ```html
   <p class="rel-cite">Fonte: adaptado de Shi et al. (2022).</p>
   ```

**Gates obrigatórios:**
- [ ] Sem `<blockquote>` (D-43)
- [ ] **Sem** citação parentética nova de Shi no corpo (Shi já foi citado em INTRO-03a)
- [ ] Argumento "quase certo / completamente errado" ou equivalente preservado
- [ ] Rodapé com "adaptado de" presente (porque a consequência é leitura autoral)
- [ ] **Code-DKT NÃO mencionado** (Pitfall 3)
- [ ] Sem em-dash

---

### `apresentacao/index.html` § MARKER-01 (progress bar 4 fases EDM, sem cabeçalho temático)

**Analog primário:** slide 6 Yağcí fundido (`apresentacao/index.html` linhas 134-147), especificamente o `<p class="bridge-seq">` na linha 143 — estrutura horizontal de caixas conectadas por setas.

**Estrutura de referência (linhas 134-147):**

```html
<!-- ============ SLIDE · Da EDM ao knowledge tracing (Yağcı, 2022) — fusão p1+p2 ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>da edm ao knowledge tracing<span class="caret blink"></span></p>

    <p class="rel-lead">Yağcı (2022) mostrou o valor de prever desempenho acadêmico para identificar alunos em risco. Nós seguimos o passo seguinte: em vez de uma previsão única ao fim do curso, <b>acompanhamos o conhecimento ao longo do tempo</b>, a cada nova tentativa, via <i>knowledge tracing</i>.</p>

    <p class="bridge-seq"><span class="step">mineração de dados educacionais</span><span class="arr">&rarr;</span><span class="step">predição de desempenho</span><span class="arr">&rarr;</span><span class="step"><i>knowledge tracing</i></span></p>

    <p class="rel-cite">Fonte: Yağcı (2022).</p>
  </div>
</section>
```

**Padrão estrutural a herdar (do `.bridge-seq`):**
- Caixas brancas com borda preta 1.5px, sem `border-radius` (estética ABNT Word)
- Setas `→` pretas (`#1f1f1f`) entre caixas
- Larguras iguais (`flex: 1 1 0`)
- Fonte Arial bold dentro das caixas

**Diferença vs `.bridge-seq`:**
- **4 caixas** (não 3)
- **Sem** `.deck-topic` no padrão `> [seção]` (D-34d)
- **Sem** parágrafo de prosa antes do progress bar (o componente é o "cabeçalho visual")
- Caixa 1 com estado `--done` (fundo `--uni-blue`, texto branco, `✓` no `.marker-step__mark`)
- Caixas 2-4 com estado `--pending` (outline `#5b6472`, fundo branco, numeração 2/3/4)

**Markup-alvo (RESEARCH §3.3, copiar como-é, polir só na execução):**

```html
<!-- ============ SLIDE · MARKER · Definição do Problema concluída (Zorić, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase1">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <div class="marker-track">
      <span class="marker-step marker-step--done">
        <span class="marker-step__mark">&check;</span>
        Definição do Problema
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">2</span>
        Preparação dos Dados
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">3</span>
        Modelagem e Avaliação
      </span>
      <span class="marker-arr">&rarr;</span>
      <span class="marker-step marker-step--pending">
        <span class="marker-step__mark">4</span>
        Implantação
      </span>
    </div>

    <p class="marker-fonte">Fonte: adaptado de Zorić (2020).</p>
  </div>
</section>
```

**Gates obrigatórios:**
- [ ] Sem `.deck-topic` (D-34d)
- [ ] 4 caixas na ordem literal de D-40: "Definição do Problema" → "Preparação dos Dados" → "Modelagem e Avaliação" → "Implantação"
- [ ] Caixa 1 com `--done` + `&check;` (não "1 ✓"; só o check, conforme A5 do Assumptions Log)
- [ ] Caixas 2-4 com `--pending` + numeração "2"/"3"/"4"
- [ ] 3 `<span class="marker-arr">&rarr;</span>` entre as 4 caixas
- [ ] Marca d'água `<svg class="wm">` presente (A6 do Assumptions Log; consistência com slides de conteúdo)
- [ ] Rodapé `.marker-fonte` centralizado com "Fonte: adaptado de Zorić (2020)."

---

### `apresentacao/assets/theme-unifacens.css` § bloco `.slide-marker` (novo, reutilizável MARKER-02/03/04)

**Analog primário 1 — estrutura horizontal:** `.slide-bridge .bridge-seq` (`theme-unifacens.css` linhas 197-210).

**CSS literal de referência (caixas + setas):**

```css
.slide-bridge .bridge-seq {
  display: flex; align-items: stretch; justify-content: center; gap: 0;
  margin-top: 38px; font-family: Arial, "Helvetica Neue", sans-serif;
}
.slide-bridge .bridge-seq .step {
  flex: 1 1 0; text-align: center; font-size: 19px; font-weight: 700; color: #111;
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0; padding: 16px 14px;
  display: flex; align-items: center; justify-content: center;
}
.slide-bridge .bridge-seq .arr {
  flex: none; align-self: center; color: #1f1f1f; font-size: 26px; font-weight: 700; padding: 0 16px;
}
```

**Analog primário 2 — rodapé centralizado:** `.slide-kcfig .kcfig-fonte` (linhas 297-300) e `.slide-fig .fig-fonte` (linha 319). Ambos centralizados, ambos Arial 18px `#5b6472`.

**CSS literal de referência (rodapé centralizado):**

```css
.slide-kcfig .kcfig-fonte {
  margin-top: 6px; padding-top: 10px; text-align: center;
  font-family: Arial, "Helvetica Neue", sans-serif; font-size: 18px; color: #5b6472;
}
.slide-fig .fig-fonte { margin-top: 8px; text-align: center; font-family: Arial, "Helvetica Neue", sans-serif; font-size: 18px; color: #5b6472; }
```

**Analog primário 3 — host `.slide-*` (layout flexbox vertical + marca d'água):** `.slide-phases` (linhas 137-138) e `.slide-related` (linhas 162-163). Padrão consistente:

```css
.slide-XYZ {
  display: flex; flex-direction: column; background: var(--uni-light);
  padding: 52px 64px 40px; --caret-color: var(--uni-blue);
}
.slide-XYZ .wm { position: absolute; top: 26px; right: 34px; width: 58px; color: var(--uni-gray); opacity: .9; pointer-events: none; }
```

**CSS-alvo a adicionar** (do RESEARCH §3.2; bloco completo, **append** ao final do `theme-unifacens.css` ou imediatamente após `.slide-bridge` linhas 197-210 — plano decide localização):

```css
/* ===========================================================================
   SLIDE · Marker · progress bar das 4 fases EDM
   Estende a estética do .bridge-seq (caixas pretas, fundo branco, setas pretas)
   acrescentando estados --done (azul UniFacens + checkmark) e --pending
   (outline cinza). Reusado por MARKER-01..04 (fases 2-5).
   =========================================================================== */
.slide-marker {
  display: flex; flex-direction: column; background: var(--uni-light);
  padding: 80px 64px 40px; --caret-color: var(--uni-blue);
  font-family: Arial, "Helvetica Neue", sans-serif;
  align-items: center; justify-content: center;
}
.slide-marker .wm { position: absolute; top: 26px; right: 34px; width: 58px; color: var(--uni-gray); opacity: .9; pointer-events: none; }

.marker-track {
  display: flex; align-items: stretch; justify-content: center; gap: 0;
  width: 100%; max-width: 1120px;
}
.marker-step {
  flex: 1 1 0; text-align: center; font-size: 19px; font-weight: 700;
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0;
  padding: 28px 12px; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 8px; min-height: 110px; line-height: 1.25;
}
.marker-step__mark {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 50%;
  font-family: var(--mono); font-size: 18px; line-height: 1; font-weight: 700;
}
.marker-step--done {
  background: var(--uni-blue); color: #fff; border-color: var(--uni-blue);
}
.marker-step--done .marker-step__mark {
  background: #fff; color: var(--uni-blue);
}
.marker-step--pending {
  background: #fff; color: #5b6472; border-color: #5b6472;
}
.marker-step--pending .marker-step__mark {
  border: 1.5px solid #5b6472; color: #5b6472;
}
.marker-arr {
  flex: none; align-self: center; color: #1f1f1f; font-size: 26px; font-weight: 700;
  padding: 0 14px;
}

.slide-marker .marker-fonte {
  margin-top: 36px; text-align: center;
  font-family: Arial, "Helvetica Neue", sans-serif; font-size: 18px; color: #5b6472;
}
```

**Convenções herdadas do arquivo (CONVENTIONS / theme-unifacens.css):**
- Variáveis CSS do `:root` (linhas 11-20): usar `var(--uni-blue)`, `var(--uni-light)`, `var(--uni-gray)`, `var(--mono)` — nunca redeclarar valores hex literais
- Tipografia Arial em corpo, `var(--mono)` (Cascadia) em acentos de terminal
- Estética ABNT Word: `border: 1.5px solid #1f1f1f`, `border-radius: 0`
- `.wm` posicionada `top: 26px; right: 34px; width: 58px` (consistente com `.slide-related`, `.slide-phases`, `.slide-problem`)
- Padding canônico de slide de conteúdo: `52px 64px 40px` (.slide-related / .slide-phases / .slide-problem). MARKER-01 usa `80px 64px 40px` porque centraliza verticalmente (componente único no slide)
- Comentário de bloco com cabeçalho `=====` antes de cada componente principal (padrão observado em todo o arquivo)

**Gates obrigatórios:**
- [ ] Usar apenas variáveis CSS existentes (`--uni-blue`, `--uni-light`, `--uni-gray`, `--mono`); não introduzir novas
- [ ] Sem `border-radius` nas caixas (estética ABNT)
- [ ] Sem em-dash no comentário de bloco do CSS
- [ ] Bloco delimitado por linha `===========...=====` no padrão dos demais componentes (linhas 81-83, 96-99, 115-117, 134-136, 158-161, 194-196, 212-214, 236-238, 265-269, 302-305, 321-323 do CSS atual)

---

### `apresentacao/STYLE.md` § linha 129 (sentença obsoleta)

**Analog:** as próprias linhas 127-132 do STYLE.md (§"Gaps reservados para fases 2-5"). Edição é apenas de texto.

**Texto atual a substituir** (linha 129, literal):

```markdown
- Após `> introdução` (slide 3): INTRO-01 "nosso dataset" + INTRO-03 "Shi e o problema" + MARKER-01 (fase 2).
```

**Texto substituto literal** (RESEARCH §5.2, vindo de `<specifics>` do CONTEXT):

```markdown
- Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).
```

**Discretion (plan-phase decide):**
- **Mínimo (D-32):** trocar apenas a linha 129.
- **Recomendado (RESEARCH §5.2 + Open Question 2):** reescrever o bloco inteiro (linhas 127-132) porque o gap da fase 3 também desloca. Texto pronto em RESEARCH §5.2:

  ```markdown
  **Gaps reservados para fases 2-5:**

  - Após `> da edm ao knowledge tracing` (slide 6): INTRO-01 "o dataset csedm" + INTRO-03a "o problema do kt binário" + INTRO-03b "sinal pedagógico perdido" + MARKER-01 (fase 2).
  - Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3).
  - Antes do trio Martins+fig (entre slide-code/slide-kcfig e Martins p2): MODEL-01, MODEL-03, MODEL-04, MODEL-05 (fase 4); slide-code vira MODEL-03 reaproveitado; slide-kcfig é a saída do pipeline MODEL-05; slide-fig é o CLOSE-03.
  - Após slide-fig: MARKER-03 (fim da fase 4 da EDM); depois TOOL-01, TOOL-03, MARKER-04, END-01 (fase 5); AGENDA-01 revisado.
  ```

- **Opcional (Open Question 2):** atualizar também a tabela "Inventário de slides" (linhas 110-124) para refletir 16 slides pós-fase 2. Tabela pronta em RESEARCH §5.3.

**Commit:** D-22 da fase 1 estabelece "STYLE.md atualizado entra no mesmo commit que o último slide reformatado OU em commit próprio ao final da fase" — convenção válida nesta fase também. Sugestão: commit próprio `apresentacao: atualizar STYLE.md gaps reservados pós-fase 2`.

---

## Shared Patterns

### Estrutura externa de slide (NUNCA alterar)

**Origem:** `apresentacao/index.html` toda, especialmente linhas 82-98 (Martins p1), 100-111 (Zorić fundido), 134-147 (Yağcí fundido). **Aplica a:** todos os 4 sections novos.

```html
<!-- ============ SLIDE · descrição em PT-BR ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-XYZ">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <!-- conteúdo do slide aqui -->
  </div>
</section>
```

**Regras invioláveis** (RESEARCH Pitfall 6, STYLE.md linhas 10-18, CONVENTIONS):
- Reveal.js força `display:block` na `<section>`; layout fica no `<div>` interno. NUNCA mudar isso.
- `<svg class="wm">` (marca d'água Facens) em todos os 4 novos (inclusive MARKER-01, A6 do Assumptions Log).
- `data-background-color="#F1F6FB"` (fundo de conteúdo padrão).
- Indentação 6 espaços para o `<section>` raiz (consistente com sections existentes).
- EOL Unix (preservar; não introduzir CRLF).

---

### Cabeçalho `> [seção]` (aplica a INTRO-01, INTRO-03a, INTRO-03b)

**Origem:** `apresentacao/index.html` linhas 87, 105, 119, 139, 155, 206, 273, 296, 318. **CSS-suporte:** `theme-unifacens.css` linhas 42-43.

```html
<p class="deck-topic"><span class="ps1">&gt;</span>nome da seção<span class="caret blink"></span></p>
```

**Regras herdadas da fase 1 (D-42, STYLE.md §"Cabeçalho de todo slide após a AGENDA"):**
- "nome da seção" é **minúsculo**, sem caracteres especiais.
- `<span class="caret blink"></span>` como **último filho** de `<p class="deck-topic">`.
- `>` em azul UniFacens (CSS `.deck-topic .ps1` linha 43).
- MARKER-01 fica **sem** `.deck-topic` (D-34d).

**Cabeçalhos travados nesta fase:**

| REQ | Texto literal dentro do `.deck-topic` |
|---|---|
| INTRO-01 | `o dataset csedm` |
| INTRO-03a | `o problema do kt binário` |
| INTRO-03b | `sinal pedagógico perdido` |
| MARKER-01 | (não aplicável — D-34d) |

---

### Voz autoral + paráfrase indireta (aplica a INTRO-01, INTRO-03a, INTRO-03b)

**Origem:** D-25 da fase 1 + STYLE.md §"Regras de redação" linhas 88-95. **Aplica a:** todos os 3 INTRO.

**Regras:**
- **Primeira pessoa do plural** quando apropriado ("Nosso dataset...", "Toda a riqueza do código submetido fica fora do modelo.").
- **Autor parentético**: `(Sobrenome, ano)` em paráfrase indireta; `;` para 2 autores (`(Corbett; Anderson, 1995)`); `et al.` para 3+ (`Shi et al., 2022`).
- **Autor prominente** aceitável (sujeito da oração) quando o autor é o foco do slide ("Shi et al. (2022) apontam que...").
- **Sem `<blockquote>`** (D-43 trava: citação direta literal proibida nos 3 INTRO desta fase).
- Texto corre como `<p class="rel-lead">` (Arial 25px justificado; CSS linha 164).

**Pitfall (RESEARCH Pitfall 5):** os trechos literais em inglês do RESEARCH §1 são **referências de fidelidade**, não markup. Traduzir em paráfrase pt-BR autoral; não copiar entre aspas.

---

### Rodapé "Fonte:" — uma linha por slide (D-45)

**Origem:** `apresentacao/index.html` linhas 96 (Martins p1), 109 (Zorić), 130 (slide-phases), 145 (Yağcí), 196 (slide-code), 264 (slide-kcfig), 287/308 (Martins p2/p3), 321 (slide-fig). **CSS-suporte:** `theme-unifacens.css` linhas 182 (`.rel-cite`), 156 (`.phases-fonte`), 263 (`.prob-cite`), 297-300 (`.kcfig-fonte`), 319 (`.fig-fonte`), 351 (`.code-fonte`).

**Inventário de classes** (RESEARCH §6.1; todas Arial 18px `#5b6472`):

| Classe | Alinhamento | Onde já é usada |
|---|---|---|
| `.rel-cite` | esquerda, `margin-top: auto` | `.slide-related` (Martins p1, Zorić, Yağcí) |
| `.prob-cite` | esquerda, `margin-top: 26px` | `.slide-problem` (Martins p2, p3) |
| `.phases-fonte` | esquerda, `margin-top: 10px` | `.slide-phases` |
| `.kcfig-fonte` | **centralizada** | `.slide-kcfig` |
| `.fig-fonte` | **centralizada** | `.slide-fig` |
| `.code-fonte` | **centralizada**, `margin-top: auto` | `.slide-code` |

**Decisão recomendada (RESEARCH §6.2):**
- **INTRO-01, INTRO-03a, INTRO-03b:** reutilizar `.rel-cite` (mesmo template `.slide-related`; sem CSS novo).
- **MARKER-01:** criar `.marker-fonte` (centralizado, modular para MARKER-02/03/04). Definido no bloco CSS novo acima.

**Formato literal por slide:**

| Slide | Texto literal do rodapé |
|---|---|
| INTRO-01 | `Fonte: Price (2020); CSEDM 2021.` |
| INTRO-03a | `Fonte: Shi et al. (2022).` |
| INTRO-03b | `Fonte: adaptado de Shi et al. (2022).` |
| MARKER-01 | `Fonte: adaptado de Zorić (2020).` (A3 do Assumptions Log) |

---

### Sem em-dash em prosa (D-44, vinculante)

**Aplica a:** texto novo dos 4 slides (parágrafos `.rel-lead`, número decorativo no INTRO-01, comentários HTML, comentário CSS do bloco `.slide-marker`).

**Regra:** preferir vírgula, dois-pontos ou parênteses. Memória `feedback_no_em_dashes` é vinculante.

**Validação obrigatória pré-commit (RESEARCH Pitfall 1):**
```bash
grep -n '—' apresentacao/index.html | grep -E '(o dataset csedm|o problema do kt|sinal pedagógico|marker-step|MARKER · Definição)'
# deve retornar vazio
```

**Atenção:** previews de phrasing no CONTEXT e RESEARCH contêm em-dash (ex.: "CSEDM — curso introdutório CS1 em Java"). Converter antes de gravar HTML. Exemplo: `"CSEDM, curso introdutório..."` ou `"CSEDM (curso introdutório...)"`.

---

### Estrangeirismos e nomes próprios (D-46)

**Aplica a:** todos os 3 INTRO.

| Categoria | Tratamento | Onde aparece |
|---|---|---|
| `*knowledge tracing*` | itálico minúsculas (`<i>knowledge tracing</i>`) | INTRO-03a (corpo) |
| BKT, DKT, Code-DKT | sem itálico, preservar maiúsculas | INTRO-03a (corpo) — Code-DKT **NÃO** menciona em INTRO-03a/b |
| ProgSnap2, CSEDM | nomes próprios, sem itálico | INTRO-01 (corpo) |
| Price, Shi, Zorić | nomes de autor sem itálico, encoding correto (ı, ğ, Ç) | rodapé "Fonte:" |

---

### Comentário acima de cada `<section>`

**Padrão obrigatório** (vivo em todos os 12 sections atuais):

```html
<!-- ============ SLIDE · descrição em PT-BR ============ -->
```

**Comentários sugeridos para os 4 novos (RESEARCH §4.3):**

```html
<!-- ============ SLIDE · INTRO-01 · O dataset CSEDM em ProgSnap2 (Price, 2020) ============ -->
<!-- ============ SLIDE · INTRO-03a · O problema do KT binário (Shi et al., 2022) ============ -->
<!-- ============ SLIDE · INTRO-03b · Sinal pedagógico perdido (adaptado de Shi et al., 2022) ============ -->
<!-- ============ SLIDE · MARKER · Definição do Problema concluída (Zorić, 2020) ============ -->
```

**Convenções herdadas (CONVENTIONS, observação em `index.html`):**
- 12 sinais `=` de cada lado (consistente com os 12 sections atuais).
- Descrição curta em PT-BR.
- Autor + ano entre parênteses no fim quando aplicável.

---

### Validação visual fim-a-fim (D-47)

**Aplica a:** fim de fase (após inserção dos 4 sections + bloco CSS + correção STYLE.md).

```bash
cd apresentacao && python3 -m http.server 8000
# abrir http://127.0.0.1:8000/#/0 e percorrer até #/15
```

**Checks por slide novo** (RESEARCH §7.2 lista completa; abaixo o resumo cruzado):

| URL | Slide | Foco primário da inspeção |
|---|---|---|
| `#/7` | INTRO-01 | Cabeçalho `> o dataset csedm`; 3 números (413, 50, 201 mil); `(Price, 2020)` parentético; rodapé `Fonte: Price (2020); CSEDM 2021.`; voz "Nosso dataset é..." |
| `#/8` | INTRO-03a | Cabeçalho `> o problema do kt binário`; "Shi et al. (2022) apontam..."; BKT + DKT mencionados; sem aspas literais; rodapé `Fonte: Shi et al. (2022).`; sem Code-DKT |
| `#/9` | INTRO-03b | Cabeçalho `> sinal pedagógico perdido`; "Como consequência..."; rodapé `Fonte: adaptado de Shi et al. (2022).`; sem Code-DKT |
| `#/10` | MARKER-01 | Sem `.deck-topic`; 4 caixas; caixa 1 azul UniFacens com `✓`; caixas 2-4 outline `#5b6472`; 3 setas `→`; rodapé `.marker-fonte` centralizado |

**Cache do http.server (STYLE.md linha 154):** se editar CSS, subir em outra porta (`python3 -m http.server 8001`) para forçar reload.

---

## Sequência recomendada de implementação (Open Question 5 do RESEARCH)

**Ordem:** **MARKER-01 primeiro**, depois INTRO-01, INTRO-03a, INTRO-03b. Em seguida, STYLE.md.

**Razões:**
1. O bloco CSS `.slide-marker` é o **único risco visual** da fase; resolver primeiro derisca o resto.
2. Validar MARKER-01 no browser (4 caixas + setas + checkmark) antes de empilhar os 3 INTRO.
3. Os 3 INTRO são **paste-and-modify** do template `.slide-related` (linhas 100-111 do index.html); risco baixíssimo após o CSS do marker estar OK.
4. STYLE.md no fim porque depende de todos os 4 slides já estarem definidos para a sentença substituta fazer sentido.

**Granularidade de commits (CONTEXT discretion):**
- **Sugerido:** 4 commits (um por slide) + 1 commit para STYLE.md = 5 commits totais.
- **Aceitável alternativa:** 3 commits (MARKER-01 com seu CSS / INTRO-01 / INTRO-03a+03b juntos) + 1 STYLE.md.
- **Mensagens (convenção do projeto, CONVENTIONS):** lowercase português, prefixo `apresentacao:` ou `slide-XYZ:`. Exemplos:
  - `apresentacao: slide-marker componente reutilizável (MARKER-01 fase 2)`
  - `apresentacao: slide INTRO-01 - dataset CSEDM (Price, 2020)`
  - `apresentacao: slide INTRO-03a - problema do KT binário (Shi et al., 2022)`
  - `apresentacao: slide INTRO-03b - sinal pedagógico perdido`
  - `apresentacao: atualizar STYLE.md gaps reservados pós-fase 2`

---

## No Analog Found

Nenhum. Todos os 4 slides novos e o bloco CSS têm template-base vivo no codebase:

- **INTRO-01/03a/03b** → analog `.slide-related` (slide 4 Zorić fundido + slide 6 Yağcí fundido) — exato
- **MARKER-01** → analog `.slide-bridge .bridge-seq` (caixas + setas horizontais) + `.kcfig-fonte` / `.fig-fonte` (rodapé centralizado) — role-match
- **Bloco CSS `.slide-marker`** → analog `.bridge-seq` + `.slide-related` (host pattern) + `.kcfig-fonte` (rodapé) — role-match
- **STYLE.md linha 129** → identidade (edição de texto no próprio arquivo)

---

## Metadata

**Analog search scope:**
- `apresentacao/index.html` (468 linhas, HEAD em 2026-05-27)
- `apresentacao/assets/theme-unifacens.css` (357 linhas)
- `apresentacao/STYLE.md` (162 linhas)
- `.planning/phases/01-reformata-o-da-base/01-PATTERNS.md` (referência de formato)
- `.planning/codebase/STRUCTURE.md`, `.planning/codebase/CONVENTIONS.md`

**Files scanned:** 5 (todos os arquivos relevantes; nenhum re-read).
**Pattern extraction date:** 2026-05-27.

**Convention reminder (CLAUDE.md):** "Antes de redigir ou alterar slide que cite um autor, ler a referência completa em `docs/`" — vinculante para INTRO-01 (Price, 2020) e INTRO-03a/b (Shi et al., 2022); o RESEARCH §1 já fez essa leitura, então o plano pode aproveitar os trechos literais lá listados como referência de fidelidade.

**Decisões de design herdadas vinculantes:**
- D-31 a D-47 do CONTEXT desta fase
- D-01 a D-30 da fase 1 (especialmente D-01..D-03 padrão de cabeçalho, D-25 voz autoral)
- STYLE.md §"Cabeçalho de todo slide após a AGENDA" linhas 37-60 (padrão `> [seção]`)
- STYLE.md §"Regras de redação" linhas 83-95 (sem em-dash, voz própria default)
- Memórias `feedback_no_em_dashes`, `feedback_correlatos_antes`, `reference_manual_citacoes` (vinculantes)
