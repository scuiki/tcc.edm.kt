# Phase 1: Reformatação da base - Pattern Map

**Mapped:** 2026-05-27
**Files analyzed:** 3 (`apresentacao/index.html`, `apresentacao/STYLE.md`, `apresentacao/assets/theme-unifacens.css`)
**Analogs found:** 9 / 9 (todos os patterns "antes" e "depois" já vivem dentro do próprio `index.html`)

> Esta fase não cria arquivos. Ela reformata 7 slides existentes, funde 2 pares, remove 2 slides
> e edita 3 seções do STYLE.md. Os "analogs" são, portanto, blocos do próprio `index.html`. O
> padrão "depois" (`.deck-topic`) já está implementado e em uso em 5 slides; o padrão "antes"
> (`.rel-kicker` + `.rel-title` + `.rel-sub`) ainda vive nos slides correlato/Yağcí/Corbett.

---

## File Classification

| Arquivo a modificar | Papel | Fluxo de edição | Analog (mesma família, dentro do arquivo) | Match |
|---|---|---|---|---|
| `apresentacao/index.html` § slide #3 (Martins p1, REFORMAT-01) | view (slide-related) | header-rewrite | `slide-related` Zorić (#9), Yağcí (#12), Corbett (#14) | exato |
| `apresentacao/index.html` § slide #4 (Martins p2 "O problema", REFORMAT-04) | view (slide-problem) | header-rewrite + DOM-move | `slide-problem` Martins p3 (#5) — já tem `.deck-topic` correto na forma | exato |
| `apresentacao/index.html` § slide #5 (Martins p3, REFORMAT-04) | view (slide-problem) | header-rewrite + DOM-move | `slide-problem` Martins p2 (#4) — par adjacente | exato |
| `apresentacao/index.html` § slide #6 (slide-kcfig, REFORMAT-05a) | view (slide-kcfig) | header-rewrite + DOM-move | mesmo slide #6 (só troca o texto do `.deck-topic` interno) | identidade |
| `apresentacao/index.html` § slide #7 (slide-fig, REFORMAT-05b) | view (slide-fig) | header-rewrite + DOM-move | mesmo slide #7 (só troca o texto do `.deck-topic` interno) | identidade |
| `apresentacao/index.html` § slide #8 (slide-code, REFORMAT-05c) | view (slide-code) | header-rewrite + DOM-move | mesmo slide #8 (só troca o texto do `.deck-topic` interno) | identidade |
| `apresentacao/index.html` § slide #11 (slide-phases, REFORMAT-02) | view (slide-phases) | header-rewrite | mesmo slide #11 (já usa `.deck-topic` dentro de `.phases-head`) | identidade |
| `apresentacao/index.html` § slides #9+#10 (Zorić p1+p2, MERGE-01) | view (slide-related) | merge + header-rewrite + texto novo | `slide-related` slide-bridge Yağcí (#13) — outro slide-related fundido com prosa | role-match |
| `apresentacao/index.html` § slides #12+#13 (Yağcí p1+p2, REFORMAT-03) | view (slide-related slide-bridge) | merge + header-rewrite + texto novo | slide #13 sobrevive como base; absorve markup de #12 | identidade |
| `apresentacao/index.html` § slides #14+#15 (Corbett, REMOVE-01) | view (slide-related slide-corbett) | DOM-delete | n/a | — |
| `apresentacao/STYLE.md` § "Cabeçalho de todo slide após a AGENDA" (D-21) | docs | section-rewrite | a própria seção atual | identidade |
| `apresentacao/STYLE.md` § "Regras de redação" > "Regra dos correlatos" (D-21) | docs | bullet-replace | bullet atual (linhas 80-81) | identidade |
| `apresentacao/STYLE.md` § "Inventário de slides (ordem atual)" (D-21) | docs | table-rewrite | tabela atual (linhas 94-113) | identidade |
| `apresentacao/assets/theme-unifacens.css` (cleanup opcional) | style | possível-removal | regras `.slide-related .rel-kicker` / `.rel-title` / `.rel-sub` linhas 164-167 | identidade |

---

## Pattern Assignments

### Cabeçalho-alvo único (padrão "depois")

**Origem:** já implementado em `apresentacao/index.html` linhas 107, 131, 154, 223, 237, 331.

**Markup canônico** (a forma que todo slide reformatado deve ter como única linha de cabeçalho):

```html
<p class="deck-topic"><span class="ps1">&gt;</span>nome da seção<span class="caret blink"></span></p>
```

**CSS suportando este markup** (`apresentacao/assets/theme-unifacens.css` linhas 42-51):

```css
.deck-topic { font-family: var(--mono); font-weight: 400; font-size: 24px; color: #5b6472; margin: 0 0 16px; }
.deck-topic .ps1 { color: var(--uni-blue); font-weight: 700; margin-right: 10px; }

.caret {
  display:inline-block; width:.55em; height:1.02em;
  background: var(--caret-color, var(--uni-blue));
}
.caret.blink { animation: caretBlink 1.05s steps(1) infinite; }
@keyframes caretBlink { 50% { opacity: 0; } }
```

**Variante do slide-phases** (cabeçalho envolvido por `.phases-head`; o `.deck-topic` interno foi mantido pela orientação visual atual). Slide #11, linhas 330-333:

```html
<div class="phases-head">
  <p class="deck-topic"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
  <h2 class="phases-title">As quatro fases do processo de EDM</h2>
</div>
```

Em REFORMAT-02 a `<h2 class="phases-title">` desaparece (D-03) e só o `<p class="deck-topic">` sobra dentro do `.phases-head`. A wrapper `<div class="phases-head">` pode ser mantida ou removida; o planner decide com base no efeito visual sobre o gap até `.phases-list`.

**Importante:** "nome da seção" é minúsculo, sem caracteres especiais (segue convenção de `> [seção]` mono Cascadia em `#5b6472`, STYLE.md "Tipografia"). Cabeçalhos travados por D-04..D-11:

| REQ | Texto exato dentro do `.deck-topic` |
|---|---|
| REFORMAT-01 (Martins p1) | `introdução` |
| REFORMAT-02 (Zorić p3 / slide-phases) | `as quatro fases da edm` |
| REFORMAT-03 (Yağcí fundido) | `da edm ao knowledge tracing` |
| REFORMAT-04 (Martins p2 e p3, ambos) | `retomando o problema` |
| REFORMAT-05a (slide-kcfig) | `kcs semânticos extraídos` |
| REFORMAT-05b (slide-fig) | `evolução por dificuldade` |
| REFORMAT-05c (slide-code) | `o que o code-dkt olha` |
| MERGE-01 (Zorić p1+p2) | `mineração de dados educacionais` |

---

### Padrão "antes" #1 — par `.rel-kicker` + `.rel-title` (+ opcional `.rel-sub`)

**Aparece em:** slides `slide-related` puros (Martins p1 #3, Zorić p1 #9, Zorić p2 #10, Yağcí p1 #12, Yağcí p2/bridge #13, Corbett #14, Corbett #15).

**Excerto canônico** (de `apresentacao/index.html` linhas 88-89, Martins p1):

```html
<p class="rel-kicker kicker"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
<h2 class="rel-title">Martins, Marin e Alves (2024)</h2>
```

**Variante com subtítulo** (linhas 289-291, Zorić p1):

```html
<p class="rel-kicker kicker"><span class="ps1">&gt;</span>trabalhos correlatos</p>
<h2 class="rel-title">Zorić (2020)</h2>
<p class="rel-sub">Mineração de Dados Educacionais (EDM)</p>
```

**Regra de transformação (D-01, D-02, D-03):** as 2 ou 3 linhas acima viram **uma única** linha `<p class="deck-topic">...</p>` com o texto travado por D-04..D-11. Subtítulo `.rel-sub` é descartado sem substituição. O nome do autor não migra para nenhum outro elemento; segue apenas no rodapé `.rel-cite`.

**CSS órfão pós-fase** (`theme-unifacens.css` linhas 164-167) — candidatas a remoção opcional após o último slide-related deixar de usá-las:

```css
.slide-related .rel-kicker { font-size: 24px; color: #5b6472; margin: 0 0 16px; }
.slide-related .rel-kicker .ps1 { color: var(--uni-blue); }
.slide-related .rel-title { font-family: Arial, "Helvetica Neue", sans-serif; font-size: 30px; font-weight: 700; color: var(--uni-ink); margin-top: 0; }
.slide-related .rel-sub { font-family: Arial, "Helvetica Neue", sans-serif; font-size: 22px; color: #5b6472; margin-top: 2px; }
```

Decisão deferida no CONTEXT (linha 185): o plano da fase decide se faz cleanup agora ou difere. Não bloqueia a navegação.

---

### Padrão "antes" #2 — `.deck-topic` + `<h2>` interno

**Aparece em:** slide-problem (Martins p2 #4 e Martins p3 #5), slide-kcfig (#6), slide-fig (#7), slide-code (#8), slide-phases (#11).

**Excerto canônico** (de `apresentacao/index.html` linhas 107-108, Martins p2):

```html
<p class="deck-topic"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
<h2 class="prob-head">O problema</h2>
```

**Demais ocorrências:**

| Slide | Linha | `<h2>` que desaparece (D-03) |
|---|---|---|
| #5 slide-problem (Martins p3) | 132 | `<h2 class="prob-head">Dentro dos conceitos técnicos</h2>` |
| #6 slide-kcfig | 155 | `<p class="kcfig-title">KCs (KCGen-KT) e as dificuldades em conceitos de programação</p>` (não é `<h2>` mas cumpre o mesmo papel; mesmo tratamento per D-03) |
| #7 slide-fig | 224 | `<h2 class="fig-title">Quão difícil de aprender? Curva de aprendizado do Code-DKT por dificuldade</h2>` |
| #8 slide-code | 238 | `<h2 class="code-title">O que o Code-DKT &ldquo;olha&rdquo; ao prever erro</h2>` |
| #11 slide-phases | 332 | `<h2 class="phases-title">As quatro fases do processo de EDM</h2>` |

**Regra de transformação:** o `<p class="deck-topic">` permanece, mas seu texto muda para o cabeçalho travado da REQ correspondente; o `<h2>` (ou equivalente `.kcfig-title`) imediatamente abaixo é deletado por inteiro. Tudo abaixo (`<blockquote class="prob-quote">`, `.ascii-chart`, `.kc-row`, `.fig-wrap`, `.code-card`, `.phases-list`) é preservado intacto.

**Caso especial slide-kcfig (#6):** `.kcfig-title` é `<p>`, não `<h2>`, mas funciona como título. Apaga-se por consistência com D-03 (cabeçalho único `> kcs semânticos extraídos`).

---

### Rodapé "Fonte:" preservado (todas as REQs)

**Aparece em:** todo slide reformatado.

**Variantes existentes** (`apresentacao/index.html`):

```html
<!-- slide-related (linhas 98, 303, 321, 364, 382) -->
<p class="rel-cite">Fonte: Martins, Marin e Alves (2024).</p>
<p class="rel-cite">Fonte: Zorić (2020).</p>
<p class="rel-cite">Fonte: Yağcı (2022).</p>

<!-- slide-problem (linhas 122, 144) -->
<p class="prob-cite">Fonte: adaptado de Martins, Marin e Alves (2024).</p>

<!-- slide-kcfig (linha 213) — múltiplas referências, D-24 -->
<p class="kcfig-fonte">Fonte: elaborado pelos autores, com base em Duan <i>et al.</i> (2025) e Martins, Marin e Alves (2024).</p>

<!-- slide-fig (linha 227) -->
<p class="fig-fonte">Fonte: elaborado pelos autores (Code-DKT, Shi <i>et al.</i>, 2022; dificuldades de Martins, Marin e Alves, 2024).</p>

<!-- slide-code (linha 279) -->
<p class="code-fonte">Fonte: elaborado pelos autores (Code-DKT, Shi <i>et al.</i>, 2022; submissão real do CSEDM, problema <i>dateFashion</i>).</p>

<!-- slide-phases (linha 343) -->
<p class="phases-fonte">Fonte: Zorić (2020).</p>
```

**Regra:** Fase 1 não altera o texto destes rodapés (D-23, D-24). Só garante que (a) cada slide reformatado tem UMA linha "Fonte:" no rodapé, (b) sobrenome e ano corretos, (c) "adaptado de" preservado quando aplicável. A classe CSS (`.rel-cite`, `.prob-cite`, `.fig-fonte`, etc.) continua a mesma porque a classe-pai do `.deck-slide` continua a mesma.

---

### MERGE-01 Zorić p1+p2 — padrão de fusão (slide-related + slide-methods)

**Slide #9 (antes — markup completo, linhas 285-305):**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="rel-kicker kicker"><span class="ps1">&gt;</span>trabalhos correlatos</p>
    <h2 class="rel-title">Zorić (2020)</h2>
    <p class="rel-sub">Mineração de Dados Educacionais (EDM)</p>

    <blockquote class="rel-quote">&ldquo;A Mineração de Dados Educacionais (EDM) é uma área de pesquisa interdisciplinar criada como a aplicação da mineração de dados no campo educacional&rdquo; <span class="src">(Zorić, 2020, p. 12, tradução nossa)</span>.</blockquote>

    <p class="rel-intro">Transforma dados brutos em informação útil para:</p>
    <ul class="rel-points">
      <li><span class="ps1">&gt;</span>compreender melhor os estudantes e suas condições de aprendizagem;</li>
      <li><span class="ps1">&gt;</span>prever o desempenho do estudante e detectar a evasão;</li>
      <li><span class="ps1">&gt;</span>apoiar o ensino e a tomada de decisão.<span class="caret blink"></span></li>
    </ul>
    <p class="rel-src">Com base em Zorić (2020, p. 12-14).</p>

    <p class="rel-cite">Fonte: Zorić (2020).</p>
  </div>
</section>
```

**Slide #10 (antes — markup completo, linhas 308-323):**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-methods">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="rel-kicker kicker"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
    <h2 class="rel-title">Ferramentas e metodologias da EDM</h2>

    <blockquote class="rel-quote">&ldquo;Utiliza diferentes métodos e técnicas de aprendizado de máquina, estatística, mineração de dados e análise de dados para analisar os dados coletados durante o ensino e a aprendizagem&rdquo; <span class="src">(Zorić, 2020, p. 12, tradução nossa)</span>.</blockquote>

    <p class="meth-text">A EDM emprega tarefas como classificação, agrupamento, <b>predição</b> e associação, apoiadas por técnicas como redes neurais, árvores de decisão, regressão e análise de clusters.</p>

    <p class="meth-text">A <b>predição</b> do desempenho acadêmico e da evasão está entre suas aplicações mais relevantes. Para conduzir essa análise, a EDM segue um <b>processo de quatro fases</b>.</p>

    <p class="rel-cite">Fonte: Zorić (2020).</p>
  </div>
</section>
```

**Após MERGE-01 (D-11, D-26):** vira UM único `<section>` com `slide-related` (sem `slide-methods`), com cabeçalho `> mineração de dados educacionais`, sem nenhuma `<blockquote class="rel-quote">`, com paráfrase indireta única em voz própria, rodapé `Fonte: Zorić (2020).` mantido. Sugestão de texto em D-26 do CONTEXT. O `<svg class="wm">` permanece. O caret piscante migra para o `.deck-topic` único.

Forma final esperada (esqueleto, sem o texto exato da paráfrase que o planner formaliza):

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="deck-topic"><span class="ps1">&gt;</span>mineração de dados educacionais<span class="caret blink"></span></p>

    <p class="rel-lead">Nosso trabalho aplica o processo de <b>Mineração de Dados Educacionais</b>, área interdisciplinar que combina mineração de dados, estatística e aprendizado de máquina para apoiar decisões pedagógicas (Zorić, 2020). Tarefas típicas incluem classificação, agrupamento, <b>predição</b> e associação.</p>

    <p class="rel-cite">Fonte: Zorić (2020).</p>
  </div>
</section>
```

**Classes preservadas com função intacta:** `.rel-lead` (`theme-unifacens.css` linha 168), `.rel-cite` (linha 186). O `.meth-text` deixa de ser usado neste slide (mas a regra CSS em `.slide-methods .meth-text` é específica ao seletor combinado, fica inerte sem `.slide-methods` no `<div>`).

---

### REFORMAT-03 Yağcí fundido — `.bridge-seq` preservada

**Slide #12 (antes — markup completo, linhas 348-366):**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="rel-kicker kicker"><span class="ps1">&gt;</span>trabalhos correlatos</p>
    <h2 class="rel-title">Yağcı (2022)</h2>
    <p class="rel-sub">Predição do desempenho acadêmico com mineração de dados educacionais</p>

    <blockquote class="rel-quote">&ldquo;A mineração de dados educacionais tornou-se uma ferramenta eficaz para explorar as relações ocultas nos dados educacionais e prever o desempenho acadêmico dos estudantes&rdquo; <span class="src">(Yağcı, 2022, p. 1, tradução nossa)</span>.</blockquote>

    <ul class="rel-points">
      <li><span class="ps1">&gt;</span>Yağcı (2022) propõe um modelo de aprendizado de máquina que prevê a nota final do aluno a partir da nota parcial, do departamento e da faculdade.</li>
      <li><span class="ps1">&gt;</span>Compara seis algoritmos (random forest, k-NN, SVM, regressão logística, Naïve Bayes), com acurácia de 70-75% sobre 1854 alunos.</li>
      <li><span class="ps1">&gt;</span>O objetivo é identificar precocemente os estudantes em risco de reprovação e apoiar a decisão pedagógica.<span class="caret blink"></span></li>
    </ul>

    <p class="rel-cite">Fonte: Yağcı (2022).</p>
  </div>
</section>
```

**D-14:** descartar do #12 — citação inicial (p. 1), `.rel-sub` "Predição do desempenho acadêmico [...]", e todos os 3 bullets de `.rel-points` (algoritmos, 70-75%, 1854 alunos).

**Slide #13 (antes — markup completo, linhas 369-384, o sobrevivente):**

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related slide-bridge">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>

    <p class="rel-kicker kicker"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
    <h2 class="rel-title">Da predição ao <i>knowledge tracing</i></h2>

    <blockquote class="rel-quote">&ldquo;Outra dimensão da análise de aprendizagem é prever o desempenho acadêmico dos estudantes [...] e determinar os estudantes potencialmente em risco de reprovação&rdquo; <span class="src">(Yağcı, 2022, p. 2, tradução nossa)</span>.</blockquote>

    <p class="bridge-seq"><span class="step">mineração de dados educacionais</span><span class="arr">&rarr;</span><span class="step">predição de desempenho</span><span class="arr">&rarr;</span><span class="step"><i>knowledge tracing</i></span></p>

    <p class="bridge-text">Yağcı (2022) posiciona a predição do desempenho como uma dimensão da análise de aprendizagem dentro do EDM. O <i>knowledge tracing</i> dá o passo seguinte: em vez de uma única previsão ao fim do curso, acompanha o conhecimento do estudante ao longo do tempo, a cada nova tentativa.</p>

    <p class="rel-cite">Fonte: Yağcı (2022).</p>
  </div>
</section>
```

**Após REFORMAT-03 (D-12, D-13, D-27):**

- `<section>` único com classes `slide-related slide-bridge` (preserva CSS de `.slide-bridge .bridge-seq` em `theme-unifacens.css` linhas 201-210).
- Cabeçalho `> da edm ao knowledge tracing` no `.deck-topic`.
- `.rel-kicker`/`.rel-title`/`.rel-sub` removidas (de ambos os slides de origem).
- A `<blockquote class="rel-quote">` da p. 2 que estava no #13 é **substituída** pela paráfrase D-27 (sugestão de texto em D-27 do CONTEXT). Sem `<blockquote>`; texto livre como `<p>` (sugestão: `.rel-lead` ou inline `.bridge-text`).
- `.bridge-seq` (3 passos `mineração de dados educacionais → predição de desempenho → knowledge tracing`) é **preservada como-é**. O markup canônico está acima e deve ser copiado linha-a-linha — não retransliterar nem reordenar.
- `.bridge-text` é mantida ou fundida com a nova paráfrase a critério do planner.
- Rodapé `Fonte: Yağcı (2022).` mantido.

**Atenção ao texto (CONTEXT linha 177):** o caractere "ı" (sem ponto) e "ğ" (com breve) em "Yağcı" devem ser copiados do markup existente, nunca redigitados ou transliterados como "Yagci".

---

### REMOVE-01 — deleção limpa, sem placeholder

**Alvos:** `apresentacao/index.html` linhas 386-407 (slide #14) e 409-439 (slide #15).

**Procedimento (D-19, D-20):** apagar os dois blocos `<!-- ============ SLIDE · ... ============ -->` + `<section>...</section>` inteiros, incluindo o comentário acima de cada um. Nenhum placeholder, nenhum comentário "TODO" ou "futuro slide", nenhuma nota em REQUIREMENTS.md. Verificação obrigatória de fim de fase:

```bash
grep -c 'slide-corbett' apresentacao/index.html
# deve retornar: 0
```

Cronologia "BKT (Corbett & Anderson, 1995) → DKT → Code-DKT" volta na fase 4 (MODEL-01); fora do escopo desta fase.

---

### Template comment "============ SLIDE · ... ============"

**Padrão obrigatório acima de cada `<section>`** (preservar em todo slide reformatado):

```html
<!-- ============ SLIDE · descrição curta em PT-BR ============ -->
```

**Exemplos vivos:**

```html
<!-- ============ SLIDE · Trabalho correlato: Martins, Marin e Alves (2024) ============ -->   (linha 82)
<!-- ============ SLIDE 4 · O problema (Martins, Marin e Alves, 2024) ============ -->          (linha 102)
<!-- ============ SLIDE · Figura: KCs (KCGen-KT) ligados às dificuldades (Martins et al., 2024) ============ -->  (linha 148)
<!-- ============ SLIDE · Ponte EDM -> KT que o trabalho de Yağcí (2022) mostra ============ -->  (linha 368)
```

**Regra para a fase 1:**

- Em REFORMAT-04 e REFORMAT-05 (movimentação de DOM), arrastar o comentário JUNTO com a `<section>`. O comentário fica imediatamente acima da `<section>` que descreve.
- Em REFORMAT-01/02/03/05, atualizar a descrição do comentário se ela ficar enganadora após o cabeçalho mudar. Exemplo: em REFORMAT-01 (Martins p1), o comentário atual "Trabalho correlato: Martins, Marin e Alves (2024)" passa a ser tecnicamente impreciso porque o slide deixa de ser apresentado como "trabalho correlato". Sugestão: "Introdução · Martins, Marin e Alves (2024) — recorte do problema".
- Em REMOVE-01, deletar o comentário junto com a `<section>`.
- Em MERGE-01 e REFORMAT-03, manter UM comentário para o slide fundido (descartar o segundo).

---

## DOM Move Pattern (REFORMAT-04 + REFORMAT-05)

**Estado final exigido pelo CONTEXT (D-16, D-17):** ao fim da fase 1, a ordem dos slides em `apresentacao/index.html` deve ser:

1. slides #0-#2 (cover, title, agenda) — intocados
2. slide #3 Martins p1 — reformatado in-place (REFORMAT-01)
3. slide MERGE-01 (Zorić fundido) — herda posição ~#9 ou imediatamente após Martins p1; ordem exata fica a critério do planner desde que respeite os success criteria do ROADMAP
4. slide #11 slide-phases reformatado (REFORMAT-02)
5. slide REFORMAT-03 (Yağcí fundido)
6. (Corbett removido — REMOVE-01)
7. **No fim do `<section>` raiz, NESTA ORDEM:**
   - slide-code OU slide-kcfig (ordem livre entre eles — Claude's Discretion)
   - slide-kcfig OU slide-code
   - **trio adjacente, sem nada entre eles:**
     - Martins p2 (`> retomando o problema`)
     - Martins p3 (`> retomando o problema`)
     - slide-fig (`> evolução por dificuldade`)

**Restrições obrigatórias** (D-17):

- (a) Martins p2 e Martins p3 **adjacentes**.
- (b) slide-fig **imediatamente após Martins p3**.
- (c) slide-code e slide-kcfig **precedem** o trio Martins+fig.

**Operação concreta:** recortar cada `<section>` inteiro (incluindo seu comentário `<!-- ============ SLIDE · ... ============ -->` acima) e colar no fim do `<div class="slides">` raiz, antes do `</div></div><script>` do final do arquivo (linha 441-444). Não modificar nada além do cabeçalho dentro de cada section movida.

**Sanidade pós-movimentação:** navegação no browser `cd apresentacao && python3 -m http.server 8000` e percorrer fim-a-fim sem erro de console; ROADMAP success criteria #1.

---

## Shared Patterns

### Estrutura externa de cada slide (NUNCA alterar)

**Origem:** `apresentacao/index.html` toda. **Aplica a:** todos os slides reformatados/movidos/fundidos.

```html
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-XYZ">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <!-- conteúdo do slide aqui -->
  </div>
</section>
```

**Regra (STYLE.md linhas 10-18):** reveal.js força `display:block` na `<section>`; layout fica no `<div>` interno. NUNCA mudar isso. O `<svg class="wm">` (marca d'água Facens) está em todos os slides de conteúdo e deve ser preservado.

### Caret piscante

**Origem:** `theme-unifacens.css` linhas 45-51. **Aplica a:** todo cabeçalho `.deck-topic` reformatado.

```html
<span class="caret blink"></span>
```

Sempre como **último filho** de `<p class="deck-topic">`, fora do texto da seção, depois do nome da seção. Convenção STYLE.md linhas 49-50: caret também pode aparecer no fim do último item de uma lista (padrão atual do Zorić e da Agenda); no novo padrão da fase 1, o caret migra para o `.deck-topic` em todos os slides reformatados.

### Citação direta — EXCEÇÃO mantida em REFORMAT-04

**Origem:** `apresentacao/index.html` linhas 109 (Martins p2) e 133 (Martins p3). **Aplica a:** REFORMAT-04, e somente REFORMAT-04 (D-28).

```html
<blockquote class="prob-quote">&ldquo;A compreensão dos conceitos técnicos da programação pode ser considerada um desafio complexo. Esta é a dificuldade mais comum entre os estudantes, mencionada por 13 autores&rdquo; <span class="src">(Martins; Marin; Alves, 2024, p. 19)</span>.</blockquote>
```

```html
<blockquote class="prob-quote">&ldquo;Destaca-se que o entendimento das estruturas de controle é o conceito mais desafiador para os alunos, citado por 10 autores&rdquo; <span class="src">(Martins; Marin; Alves, 2024, p. 20)</span>.</blockquote>
```

**Por que mantém:** D-28 — os números "mencionada por 13 autores" e "citado por 10 autores" são o argumento quantitativo da revisão sistemática; paráfrase enfraqueceria. Esta é a única exceção legítima à regra D-25 nesta fase.

### Paráfrase como padrão (D-25, D-26, D-27)

**Aplica a:** MERGE-01 (Zorić fundido) e REFORMAT-03 (Yağcí fundido).

**Regra:** voz em primeira pessoa do plural ("nosso trabalho aplica", "nós seguimos"), autor parentético no texto, sem `<blockquote class="rel-quote">`, sem "tradução nossa". Texto corre como `<p class="rel-lead">` ou similar (paragrafação tradicional).

**Sugestões de redação literal já validadas em CONTEXT.md D-26 e D-27**: o planner pode copiá-las verbatim ou refraseá-las, desde que mantenha voz própria + atribuição parentética + ausência de aspas literais.

### Sem em-dash em prosa nova (STYLE.md linha 79 + CLAUDE.md)

**Aplica a:** qualquer texto novo escrito nesta fase (parágrafos D-26 e D-27 em particular).

**Regra:** preferir vírgula, dois-pontos ou parênteses. Validar visualmente o texto antes de commitar; se houver em-dash (`—`) na prosa, reescrever.

### Rodapé "Fonte:" — uma linha por slide (D-23)

**Aplica a:** todos os slides reformatados.

**Regra:** cada slide reformatado mantém UMA linha "Fonte:" no rodapé, com sobrenome + ano corretos, "adaptado de" preservado quando aplicável (slide-problem). Para slide-kcfig com referências múltiplas (D-24), o formato existente "Fonte: elaborado pelos autores, com base em Duan et al. (2025) e Martins, Marin e Alves (2024)." fica intacto.

---

## Pattern Assignment para STYLE.md (D-21)

O `apresentacao/STYLE.md` é editado dentro da fase 1, no mesmo escopo da reformatação. Três seções precisam de mudança:

### STYLE.md — seção "Cabeçalho de todo slide após a AGENDA" (linhas 37-52)

**Texto atual (a substituir):**

```markdown
## Cabeçalho de todo slide após a AGENDA

Padrão obrigatório: **linha de tópico + título**, com **16px** de espaço entre eles.

\`\`\`html
<p class="deck-topic"><span class="ps1">&gt;</span>trabalhos correlatos<span class="caret blink"></span></p>
<h2 class="prob-head">Título do slide</h2>
\`\`\`

- Tópico genérico: classe `.deck-topic`. Nos slides de correlato (template
  `.slide-related`) o equivalente é `.rel-kicker.kicker` + `.rel-title`.
- Hoje todos os slides de conteúdo usam o tópico **`> trabalhos correlatos`**.
- O caret piscante (`<span class="caret blink">`) fica no fim do tópico, ou no fim
  do último item de uma lista (padrão da Agenda e do correlato do Zorić).
- Gap tópico→título = 16px: garantido por `margin:0 0 16px` no tópico e
  `margin-top:0` no título (zerar a margem padrão de `<p>` quando o título for `<p>`).
```

**Forma da reescrita (D-21):** descrever o `> [nome da seção]` como **única** linha de cabeçalho; mencionar que o autor desaparece do corpo e do título e migra exclusivamente para "Fonte:" no rodapé; manter a descrição visual de `.deck-topic` (Cascadia 24px, caret piscando, `>` azul); deixar claro que `<h2>` e `.rel-sub` deixam de existir como cabeçalho. Manter o snippet de exemplo, atualizando para mostrar o slide sem `<h2>` interno.

### STYLE.md — bullet "Regra dos correlatos" (linhas 80-81)

**Texto atual (a substituir):**

```markdown
- **Regra dos correlatos:** todo autor novo é introduzido em um slide
  `> trabalhos correlatos` ANTES do slide que usa seus resultados.
```

**Forma da reescrita (D-21):** remover esse bullet inteiro; substituir por nota de que autores são introduzidos no momento da relevância via cabeçalho temático (`> [seção]`) e nunca em slide dedicado. Linguagem sugerida: "Autores são introduzidos no momento da relevância, via cabeçalho temático `> [nome da seção]`; nunca em slide dedicado de "trabalhos correlatos". O nome do autor não aparece no corpo nem no cabeçalho, apenas em `Fonte:`."

### STYLE.md — tabela "Inventário de slides (ordem atual)" (linhas 94-113)

**Tabela atual (a substituir por completo):**

| # | classe | conteúdo |
|---|---|---|
| 0 | slide-cover-brand | Abertura (logo + tagline) |
| 1 | slide-title-tcc | Capa do TCC (grafite, formal) |
| 2 | slide-agenda | Agenda (faixa azul + lista `>`) |
| 3 | slide-related | Correlato: Martins, Marin e Alves (2024) |
| 4 | slide-problem | O problema (dificuldades, Quadro 3) |
| 5 | slide-problem | Dentro dos conceitos técnicos |
| ... (até #15 Corbett) ... |

**Forma da reescrita (D-21):** redesenhar a tabela para o estado pós-fase 1:

- Corbett removido (sem linhas para #14/#15 antigos).
- Zorić p1+p2 fundido em uma linha.
- Yağcí fundido em uma linha.
- 5 slides (Martins p2, Martins p3, slide-kcfig, slide-fig, slide-code) reposicionados no fim do deck.
- Coluna "conteúdo" reescrita para refletir o novo cabeçalho `> [seção]` em vez de citar o autor.
- Pode (deve) marcar com "(reservado: MODEL-01..08 entrarão aqui)" os gaps abertos para a fase 4, conforme D-18.

**Linhagem de KT no rodapé da seção** (linhas 115-119) — atualizar ou deixar como "em aberto até a fase 4 trazer Piech, Shi e nova Corbett-MODEL-01". Decisão do planner.

### STYLE.md — momento do commit (D-22)

**Regra:** o STYLE.md atualizado entra no mesmo commit que o último slide reformatado OU em commit próprio ao final da fase. O planner decide. Sugestão: commit próprio `apresentacao: atualizar STYLE.md para padrão > [seção]` no fim da fase, depois de toda a navegação fim-a-fim ter sido validada.

---

## CSS Cleanup — opcional (theme-unifacens.css)

**Arquivo:** `apresentacao/assets/theme-unifacens.css` linhas 164-167.

**Regras que podem ficar órfãs após a fase 1:**

```css
.slide-related .rel-kicker { font-size: 24px; color: #5b6472; margin: 0 0 16px; }
.slide-related .rel-kicker .ps1 { color: var(--uni-blue); }
.slide-related .rel-title { font-family: Arial, "Helvetica Neue", sans-serif; font-size: 30px; font-weight: 700; color: var(--uni-ink); margin-top: 0; }
.slide-related .rel-sub { font-family: Arial, "Helvetica Neue", sans-serif; font-size: 22px; color: #5b6472; margin-top: 2px; }
```

**Verificação se podem ser removidas:** após reformatação completa, rodar `grep -c 'rel-kicker\|rel-title\|rel-sub' apresentacao/index.html`. Se retornar 0, as regras são órfãs e podem ser deletadas com segurança.

**Decisão deferida (CONTEXT linha 185):** o plano da fase escolhe entre (a) limpar dentro da fase 1 num commit dedicado, (b) deixar como TODO para uma fase posterior. Recomendação: limpar agora se a navegação no browser passar limpa.

**Outras classes potencialmente afetadas se removidas (verificar antes de cleanup):** `.rel-quote`, `.rel-intro`, `.rel-points`, `.rel-lead`, `.rel-finding`, `.rel-aim`, `.rel-src`, `.rel-cite` — TODAS continuam em uso após a fase (em pelo menos um `slide-related` reformatado e nos rodapés), então não devem ser tocadas.

---

## No Analog Found

Nenhum. Toda transformação que esta fase exige já tem o "antes" e o "depois" no próprio `index.html`. O padrão `.deck-topic` já está vivo em 5 slides como modelo. As fusões MERGE-01 e REFORMAT-03 e a redação D-26/D-27 são texto novo, mas seguem o padrão de paráfrase já existente em `.rel-lead` (`slide-related` Martins p1, linhas 91-96) e `.bridge-text` (slide #13, linha 380), portanto também tem analog interno.

---

## Metadata

**Analog search scope:** `apresentacao/index.html` (584 linhas), `apresentacao/STYLE.md` (146 linhas), `apresentacao/assets/theme-unifacens.css` (361 linhas).
**Files scanned:** 3 (todos os arquivos editáveis nesta fase).
**Pattern extraction date:** 2026-05-27.
**Convention reminder (CLAUDE.md):** "Antes de redigir ou alterar slide que cite um autor, ler a referência completa em docs/" — vinculante para MERGE-01 (Zorić) e REFORMAT-03 (Yağcí) antes de redigir as paráfrases D-26 e D-27.
