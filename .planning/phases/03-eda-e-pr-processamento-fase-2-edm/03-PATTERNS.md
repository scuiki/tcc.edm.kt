# Phase 3: EDA e Pré-processamento (Fase 2 EDM) - Pattern Map

**Mapped:** 2026-05-28
**Files analyzed:** 5 (modificações em `apresentacao/index.html`, `apresentacao/assets/theme-unifacens.css`, `apresentacao/STYLE.md`; criações em `scripts/build_eda_pca_scatter.py` e `results/sec2_perfis_pca.png`)
**Analogs found:** 5 / 5 (todos os 4 slides novos e o script têm template-base vivo no codebase)

> Esta fase **insere** 4 sections novos em `apresentacao/index.html` entre as linhas 243 (`</section>` do MARKER-01) e 245 (comentário do `slide-code`), **adiciona** ~30 linhas de CSS para 2 componentes novos (`.eda-grid` e `.eda-fig`/`.eda-insight`), **cria** 1 script Python standalone (`scripts/build_eda_pca_scatter.py`) que gera 1 PNG novo (`results/sec2_perfis_pca.png` copiado para `apresentacao/assets/eda-perfis-pca.png`), e **opcionalmente** atualiza `apresentacao/STYLE.md` §Inventário (12 -> 20 slides) e §Gaps reservados (remoção do gap consumido). Todas as analogias estão no próprio `apresentacao/index.html` (slides INTRO-01/03a/03b da fase 2, MARKER-01 redesign, slide Yağcí com `.bridge-seq`), em `apresentacao/assets/theme-unifacens.css` (componentes `.slide-related`, `.slide-marker`, `.slide-fig`, `.bridge-seq`) e em `scripts/build_methodology_figures.py` (one-shot matplotlib + Path + SEED).

---

## File Classification

| Arquivo (criação/modificação) | Papel | Fluxo de edição | Análogo mais próximo | Match |
|---|---|---|---|---|
| `apresentacao/index.html` § EDA-01 (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-related` INTRO-01 linhas 149-164 | exato |
| `apresentacao/index.html` § EDA-02 (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-related` INTRO-03b linhas 183-198 (3 × `.rel-lead`) | exato |
| `apresentacao/index.html` § EDA-03 (novo) | presentation slide (HTML estático) | DOM-insert | `.slide-fig` linhas 306-319 do CSS (figura + caption) | role-match |
| `apresentacao/index.html` § MARKER-02 (novo) | presentation slide (HTML estático) | DOM-insert | MARKER-01 linhas 200-243 (markup literal a clonar) | exato |
| `apresentacao/assets/theme-unifacens.css` § `.eda-grid` (novo, ~14 linhas) | utility classes (componente reutilizável) | CSS-append | `.bridge-seq .step` linhas 201-206 + `.kc-box` linhas 292-295 (estética ABNT borda fina) | role-match |
| `apresentacao/assets/theme-unifacens.css` § `.eda-fig` + `.eda-insight` (novo, ~16 linhas) | utility classes (figura + texto destacado) | CSS-append | `.slide-fig .fig-wrap` + `.slide-fig img` linhas 314-315 (img embed) | role-match |
| `scripts/build_eda_pca_scatter.py` (novo) | utility Python (one-shot figure generator) | criação | `scripts/build_methodology_figures.py` (mesmo prefixo `build_*`, matplotlib, ROOT/Path, SEED implícito) | exato |
| `results/sec2_perfis_pca.png` (gerado) | binary asset (PNG) | criação via script | — (saída binária, sem análogo de markup) | n/a |
| `apresentacao/STYLE.md` linhas 108-132 (opcional) | docs (inventário + gaps) | sentence-replace | as próprias linhas 108-125 (§Inventário pós-fase 2) + 127-132 (§Gaps) | identidade |

**Sem "no analog found".** Todos os 4 slides novos e o script têm template vivo no repo; o PNG é saída do script.

---

## Pattern Assignments

### `apresentacao/index.html` § MARKER-02 (controller, reuso mecânico) — IMPLEMENTAR PRIMEIRO

**Tipo:** modificação (DOM-insert)
**Papel:** markup de slide (`.slide-marker`)
**Análogo primário:** MARKER-01 em `apresentacao/index.html` linhas 200-243 (markup literal a clonar com 4 deltas mecânicos).

**Imports / estrutura externa canônica** (linhas 200-204):

```html
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 1 concluida (Zoric, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-marker slide-marker--phase1">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
```

**Core pattern — track das 4 pills + setas** (linhas 207-239):

```html
<div class="marker-track">
  <div class="marker-stage">
    <div class="marker-pill marker-pill--done">
      <span class="marker-pill-icon">&check;</span>
      <span class="marker-pill-name">Definição do Problema</span>
    </div>
    <span class="marker-badge">[done]</span>
  </div>
  <span class="marker-arrow">&rarr;</span>
  <div class="marker-stage">
    <div class="marker-pill marker-pill--running">
      <span class="marker-pill-icon">&#x21BB;</span>
      <span class="marker-pill-name">Preparação dos Dados</span>
    </div>
    <span class="marker-badge">[running]</span>
  </div>
  ...
</div>
```

**Rodapé Fonte** (linha 241, idêntico para MARKER-02):

```html
<p class="rel-cite">Fonte: adaptado de Zorić (2020).</p>
```

**Adaptações para MARKER-02 (4 deltas literais vs MARKER-01 HEAD, conforme RESEARCH §5.2):**

| # | Linha relativa (MARKER-01) | De | Para |
|---|---|---|---|
| 1 | 200 (comentário) | `MARKER · As quatro fases da EDM, fase 1 concluida (Zoric, 2020)` | `MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020)` |
| 2 | 202 (classe `<div>`) | `slide-marker slide-marker--phase1` | `slide-marker slide-marker--phase2` |
| 3 | 217-221 (pill 2 "Preparação dos Dados") | `marker-pill--running` + `&#x21BB;` + badge `[running]` | `marker-pill--done` + `&check;` + badge `[done]` |
| 4 | 224-229 (pill 3 "Modelagem e Avaliação") | `marker-pill--pending` + `&#x25CB;` + badge `marker-badge--empty []` | `marker-pill--running` + `&#x21BB;` + badge `[running]` |

Pill 1 ("Definição do Problema", linhas 208-214) e pill 4 ("Implantação", linhas 232-238) **inalteradas**.

**Gates obrigatórios:**
- [ ] Zero linhas adicionadas em `apresentacao/assets/theme-unifacens.css` (D-67d)
- [ ] `grep -c 'slide-marker--phase2' apresentacao/index.html` retorna 1
- [ ] `grep -c 'slide-marker--phase1' apresentacao/index.html` retorna 1 (MARKER-01 inalterado)
- [ ] Visual: pill 1 e pill 2 com check branco em fundo azul UniFacens; pill 3 com ícone reload girando (animação `marker-spin`); pill 4 cinza estático
- [ ] Badge `[done] [done] [running]` nas pills 1-3; pill 4 sem badge visível (`marker-badge--empty` esconde via `visibility: hidden` linha 445 do CSS)

**Riscos / pitfalls:**
- **Pitfall 7 (RESEARCH):** drive-by no comentário "Zoric" -> "Zorić" tentador mas **NÃO** aplicar nesta fase (sem retorno narrativo; comentário não aparece em produção)
- **CONTEXT D-67a inacurado:** descreve estado FINAL mas presumiu MARKER-01 com pill 2 `--pending`. HEAD tem pill 2 `--running`. RESEARCH §5.2 corrige os deltas. **Não confiar no D-67a literal; usar a tabela acima.**

---

### `apresentacao/index.html` § EDA-02 (controller, determinístico) — IMPLEMENTAR SEGUNDO

**Tipo:** modificação (DOM-insert)
**Papel:** markup de slide (`.slide-related` com 3 × `.rel-lead`)
**Análogo primário:** INTRO-03b em `apresentacao/index.html` linhas 183-198 (3 parágrafos `.rel-lead` em voz autoral, rodapé `adaptado de Shi`).

**Estrutura externa canônica** (linhas 183-186):

```html
<!-- ============ SLIDE · INTRO-03b · Sinal pedagogico perdido (adaptado de Shi et al., 2022) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
```

**Cabeçalho `> [seção]`** (linha 188, padrão a herdar):

```html
<p class="deck-topic"><span class="ps1">&gt;</span>sinal pedagógico perdido<span class="caret blink"></span></p>
```

**Core pattern — 3 parágrafos `.rel-lead` em sequência** (linhas 190-194):

```html
<p class="rel-lead">Considere o cenário em que um estudante resolvendo um problema acerta parte do código, mas erra em algum dos passos. Sua submissão pode não ser compilada, ou compilar e estar errada, mas de qualquer forma sua resposta é registrada como <b>incorreta</b>.</p>

<p class="rel-lead">Os modelos tratam essa tentativa de forma idêntica a uma <b>completamente errada</b>, e a previsão mais provável é de que o aluno não aprendeu nada do conteúdo abordado, mesmo tendo acertado parte da questão. O aprendizado parcial presente no código fica invisível.</p>

<p class="rel-lead">Isso abre um espaço entre o que o <i>knowledge tracing</i> clássico enxerga e o que de fato o estudante aprendeu. Essa lacuna motivou a criação de modelos que são sensíveis a códigos.</p>
```

**Rodapé Fonte** (linha 196):

```html
<p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
```

**Adaptações para EDA-02:**

1. Comentário acima do `<section>`:
   ```html
   <!-- ============ SLIDE · EDA-02 · Pré-processamento, aproximação ao protocolo (Shi et al., 2022) ============ -->
   ```
2. Cabeçalho (D-63b, recomendado pelo RESEARCH §7.2):
   ```html
   <p class="deck-topic"><span class="ps1">&gt;</span>aproximação ao protocolo<span class="caret blink"></span></p>
   ```
   Fallback aceito: `> pré-processamento`. Checkpoint decide.
3. Corpo em 3 `.rel-lead` (phrasing-alvo do RESEARCH §1.2 + §7.2, números travados em D-65a):
   ```html
   <p class="rel-lead">Nosso pré-processamento segue o protocolo de Shi <i>et al.</i> (2022) como <i>baseline</i> de comparação, com ênfase em análise.</p>

   <p class="rel-lead">Dos 413 alunos brutos do CSEDM, mantivemos <b>410</b> com pelo menos 3 tentativas de execução, mesma seleção do paper. Em seguida, dividimos em <b>328 estudantes para treino e 82 para teste</b>, na proporção 80/20 com semente fixa.</p>

   <p class="rel-lead">Limitamos cada sequência às <b>50 últimas tentativas</b>. A mediana é 32 tentativas por aluno e <i>assignment</i>; 28% dos pares ultrapassam 50, com cauda longa até 272.</p>
   ```
4. Rodapé:
   ```html
   <p class="rel-cite">Fonte: adaptado de Shi <i>et al.</i> (2022).</p>
   ```

**Gates obrigatórios:**
- [ ] Sem `<blockquote>` (D-69 proíbe direta literal)
- [ ] Sem em-dash (D-70) — `grep -n '—'` na seção deve retornar vazio
- [ ] `<i>baseline</i>`, `<i>assignment</i>`, `<i>et al.</i>` em itálico minúsculas (D-72)
- [ ] **NÃO** mencionar Release/Train (D-65b)
- [ ] **NÃO** mencionar Compile.Error nem threshold binário (D-65b)
- [ ] **NÃO** mencionar Code-DKT (Pitfall 3 RESEARCH; gate forte para fase 4)
- [ ] Citação parentética `(Shi <i>et al.</i>, 2022)` única no 1º `.rel-lead`; demais sem repetir

**Riscos / pitfalls:**
- Tentação de "fechar a frase" com "...para alimentar o Code-DKT". Pitfall 3 RESEARCH explícito.
- Frase `"...split com pelo menos 3 tentativas"` é paráfrase autoral; o paper Shi 2022 não usa literalmente "min_attempts ≥ 3" (essa é nossa terminologia interna). Não é problema — o número 410 coincide.

---

### `apresentacao/index.html` § EDA-01 (controller, layout-sensitive) — IMPLEMENTAR TERCEIRO

**Tipo:** modificação (DOM-insert) + CSS-append (`.eda-grid`)
**Papel:** markup de slide (`.slide-related` com 1 `.rel-lead` + tabela ABNT)
**Análogo primário 1 (estrutura externa):** INTRO-01 em `apresentacao/index.html` linhas 149-164 (slide-related com cabeçalho, parágrafos, rodapé).
**Análogo primário 2 (estética ABNT da tabela):** `.bridge-seq .step` linhas 201-206 do CSS + `.kc-box` linhas 292-295 (borda fina 1.5px preta, sem `border-radius`, fundo branco).
**Análogo primário 3 (sequência horizontal alternativa, descartada):** `.bridge-seq` linha 143 do index.html (cards horizontais com setas). RESEARCH §4.1 explica por que foi descartada.

**Estrutura externa canônica clonável de INTRO-01** (linhas 149-152):

```html
<!-- ============ SLIDE · INTRO-01 · O dataset CSEDM em ProgSnap2 (Price, 2020) ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-related">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
```

**Padrão de cabeçalho + parágrafo + rodapé** (linhas 154-162):

```html
<p class="deck-topic"><span class="ps1">&gt;</span>o dataset csedm<span class="caret blink"></span></p>

<p class="rel-lead">Nosso dataset é o <b>CSEDM</b>, coletado de um curso introdutório CS1 em Java, durante a primavera de 2019 e divulgado na competição CSEDM 2021. Armazenado em <b>ProgSnap2</b> (Price, 2020), um formato de base de dados que registra cada evento de programação do estudante (edição, compilação, execução), preservando o histórico completo das tentativas a cada problema.</p>

<p class="rel-lead intro-stats-line"><b>413</b> estudantes, <b>5</b> assignments com <b>10</b> problemas cada, e <b>201 mil</b> eventos.</p>

<p class="rel-cite">Fonte: Price (2020); CSEDM 2021.</p>
```

**Padrão de borda ABNT a herdar de `.bridge-seq .step`** (CSS linhas 201-206):

```css
.slide-bridge .bridge-seq .step {
  flex: 1 1 0; text-align: center; font-size: 19px; font-weight: 700; color: #111;
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0; padding: 16px 14px;
  display: flex; align-items: center; justify-content: center;
}
```

**Adaptações para EDA-01:**

1. Comentário:
   ```html
   <!-- ============ SLIDE · EDA-01 · Como navegamos o CSEDM (Spring 2019) ============ -->
   ```
2. Cabeçalho (D-63a, recomendado pelo RESEARCH §7.1):
   ```html
   <p class="deck-topic"><span class="ps1">&gt;</span>como navegamos o csedm<span class="caret blink"></span></p>
   ```
3. Parágrafo abertura (1 × `.rel-lead`, phrasing do RESEARCH §2.4 / §7.1):
   ```html
   <p class="rel-lead">Encontramos a base via Shi <i>et al.</i> (2022). Ao navegar o CSEDM, os 5 <i>assignments</i> cobrem dificuldades muito diferentes: a taxa de acerto cai de 26% no primeiro para 20% no terceiro, e sobe para 30% no último.</p>
   ```
4. Tabela `<table class="eda-grid">` com números MainTable Spring 2019 (D-64a reconciliação, RESEARCH §2.1):
   ```html
   <table class="eda-grid">
     <thead>
       <tr><th>Assignment</th><th>Alunos</th><th>Problemas</th><th>Taxa de acerto</th></tr>
     </thead>
     <tbody>
       <tr><td>A1 (439)</td><td>386</td><td>10</td><td>26,15%</td></tr>
       <tr><td>A2 (487)</td><td>340</td><td>10</td><td>20,06%</td></tr>
       <tr><td>A3 (492)</td><td>361</td><td>10</td><td>20,34%</td></tr>
       <tr><td>A4 (494)</td><td>315</td><td>10</td><td>24,72%</td></tr>
       <tr><td>A5 (502)</td><td>306</td><td>10</td><td>30,62%</td></tr>
     </tbody>
   </table>
   ```
5. Rodapé:
   ```html
   <p class="rel-cite">Fonte: análise sobre CSEDM (Spring 2019).</p>
   ```

**Gates obrigatórios:**
- [ ] Sem `<blockquote>` (D-69)
- [ ] Sem em-dash (D-70)
- [ ] **NÃO** repetir 413/50/201 mil (D-64c gate forte — esses números já estão em INTRO-01)
- [ ] **NÃO** mencionar "ProgSnap2" no corpo (Pitfall 2 RESEARCH; nominalmente único em INTRO-01)
- [ ] **NÃO** mencionar Code-DKT (Pitfall 3 RESEARCH)
- [ ] Números MainTable Spring 2019 (386/340/361/315/306) — **NÃO** usar Release/Train (233/224/234/221/222). Pitfall 4 RESEARCH.
- [ ] Percentuais formatados pt-BR com vírgula decimal: `26,15%` (não `26.15%`)
- [ ] `<i>assignments</i>`, `<i>et al.</i>` em itálico (D-72)
- [ ] `(Shi <i>et al.</i>, 2022)` parentético no corpo; rodapé sem citação Shi (porque a contagem é nossa)

**Riscos / pitfalls:**
- **Pitfall 4 RESEARCH** (numbers Release/Train vs MainTable): `eda_insights.md` Seção 1.1 está desatualizado. Validar contra cell 51 do notebook 01 ou rodar pandas no MainTable.csv (snippet em RESEARCH §2.1).
- **Pitfall 2 RESEARCH** (ProgSnap2 leak): tentação de re-introduzir o formato. `grep -c 'ProgSnap2' apresentacao/index.html` deve continuar = 1 (única ocorrência em INTRO-01 corpo `<b>ProgSnap2</b>` linha 156).
- Densidade visual: 1 `.rel-lead` (4 linhas) + tabela 5 × 4 (250px altura) + rodapé cabe bem em 720px. Se reviewer no checkpoint achar denso, considerar omitir o `.rel-lead` e deixar só a tabela com legenda.

---

### `apresentacao/index.html` § EDA-03 (controller, figura + insight) — IMPLEMENTAR QUARTO (depende do PNG)

**Tipo:** modificação (DOM-insert) + CSS-append (`.eda-fig`, `.eda-insight`)
**Papel:** markup de slide (`.slide-related` com `<figure>` + `.eda-insight`)
**Análogo primário 1 (estrutura externa):** INTRO-03b linhas 183-198 (host `.slide-related`).
**Análogo primário 2 (figura + caption):** `.slide-fig` em theme-unifacens.css linhas 306-319 (template do slide "evolução por dificuldade", índice 15 do mapa de slides).

**Padrão de figura embutida em `.slide-fig`** (CSS linhas 306-319):

```css
.slide-fig {
  display: flex; flex-direction: column; background: var(--uni-light);
  padding: 34px 56px 24px; --caret-color: var(--uni-blue);
  font-family: Arial, "Helvetica Neue", sans-serif;
}
.slide-fig .wm { position: absolute; top: 24px; right: 30px; width: 50px; color: var(--uni-gray); opacity: .9; pointer-events: none; }
.slide-fig .fig-wrap { flex: 1 1 auto; display: flex; align-items: center; justify-content: center; min-height: 0; margin-top: 2px; }
.slide-fig .fig-wrap img { max-width: 92%; max-height: 488px; object-fit: contain; }
.slide-fig .fig-fonte { margin-top: 8px; text-align: center; font-family: Arial, "Helvetica Neue", sans-serif; font-size: 18px; color: #5b6472; }
```

**Adaptações para EDA-03:**

1. Comentário:
   ```html
   <!-- ============ SLIDE · EDA-03 · Três perfis de alunos, scatter PCA (CSEDM Spring 2019) ============ -->
   ```
2. Estrutura externa (reusar `.slide-related` — não `.slide-fig`, porque queremos `.rel-lead`/`.rel-cite` consistentes):
   ```html
   <section data-background-color="#F1F6FB">
     <div class="deck-slide slide-related">
       <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
   ```
3. Cabeçalho (D-63c, recomendado pelo RESEARCH §7.3):
   ```html
   <p class="deck-topic"><span class="ps1">&gt;</span>três jeitos de aprender<span class="caret blink"></span></p>
   ```
   Fallback: `> perfis dos alunos`. Checkpoint decide.
4. Figura + insight (RESEARCH §6.5 + §7.3):
   ```html
   <figure class="eda-fig">
     <img src="assets/eda-perfis-pca.png" alt="Scatter PCA 2D dos 3 perfis de alunos (Alto desempenho, Médio, Em risco)">
   </figure>

   <p class="eda-insight">O grupo majoritário não é quem erra muito; é quem tenta pouco.</p>

   <p class="rel-lead eda-subinsight">Em risco no CSEDM tem alta taxa de acerto eventual mas poucas tentativas por <i>assignment</i> (2 a 4).</p>
   ```
5. Rodapé (D-66d literal):
   ```html
   <p class="rel-cite">Fonte: análise sobre CSEDM (Spring 2019); <i>K-Means</i> k=3 com SEED=42.</p>
   ```

**Gates obrigatórios:**
- [ ] PNG existe em `apresentacao/assets/eda-perfis-pca.png` (gerado por script + copiado de `results/`); Pitfall 6 RESEARCH
- [ ] `grep -E 'src=.*results' apresentacao/index.html` retorna vazio (não referenciar `results/` direto; STRUCTURE.md)
- [ ] Sem `<blockquote>` (D-69), sem em-dash (D-70)
- [ ] **NÃO** mencionar Shi nem Code-DKT (cluster é nosso, gate forte)
- [ ] `<i>assignment</i>`, `<i>K-Means</i>` em itálico minúsculas (D-72)
- [ ] Insight em uma frase única (não 2, não 3); voz neutra sem "vemos que..."
- [ ] Validar contagem visual no scatter contra resumo numérico printado pelo script (RESEARCH §3.2: Alto≈96, Médio≈19, Em risco≈124 com SEED=42)

**Riscos / pitfalls:**
- **Pitfall 8 RESEARCH** (números D-66c errados): D-66c lista 453/139/66/248 do `eda_insights.md`; cell 46 atual mostra 239/96/19/124. Plano DEVE re-executar o script `build_eda_pca_scatter.py` e usar os números atuais. Insight "majoritário ~55%" continua válido (124/239 = 51,9%).
- **Pitfall 5 RESEARCH** (paleta off-brand): default matplotlib (`tab10`) destoa. Usar paleta UniFacens-compatível: `#2667FF` / `#F2A516` / `#D7191C` (RESEARCH §6.3).
- **Pitfall 6 RESEARCH** (PNG em `results/` referenciado direto): plan DEVE incluir `cp results/sec2_perfis_pca.png apresentacao/assets/eda-perfis-pca.png` ANTES de commitar o slide.

---

### `apresentacao/assets/theme-unifacens.css` § `.eda-grid` (utility, ~14 linhas)

**Tipo:** modificação (CSS-append)
**Papel:** componente reutilizável (tabela ABNT compacta)
**Análogo primário 1 (estética ABNT borda fina):** `.bridge-seq .step` linhas 201-206 (`border: 1.5px solid #1f1f1f; border-radius: 0; background: #fff;`).
**Análogo primário 2 (border-collapse / cabeçalho):** `.kc-box` linhas 292-295 (mesma borda, fundo branco, `border-radius: 0`).

**CSS literal de referência (`.bridge-seq .step`, linhas 201-206):**

```css
.slide-bridge .bridge-seq .step {
  flex: 1 1 0; text-align: center; font-size: 19px; font-weight: 700; color: #111;
  background: #fff; border: 1.5px solid #1f1f1f; border-radius: 0; padding: 16px 14px;
  display: flex; align-items: center; justify-content: center;
}
```

**Bloco a adicionar (do RESEARCH §4.2 + Code Example 3):**

```css
/* ===========================================================================
   SLIDE · EDA · tabela compacta A1..A5 (template B do RESEARCH §4.2)
   Estética ABNT (borda fina preta 1.5px, sem radius), última coluna em
   azul UniFacens. Reusável por slides EDA-* que precisem de tabela ABNT.
   =========================================================================== */
.eda-grid {
  width: 92%; margin: 32px auto 0;
  border-collapse: collapse;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 21px;
}
.eda-grid th, .eda-grid td {
  border: 1.5px solid #1f1f1f;
  padding: 12px 18px;
  text-align: center;
}
.eda-grid th { background: #fff; font-weight: 700; color: var(--uni-ink); }
.eda-grid td { background: #fff; color: var(--uni-ink); }
.eda-grid tr td:first-child { text-align: left; font-weight: 700; }
.eda-grid tr td:last-child { color: var(--uni-blue); font-weight: 700; }
```

**Gates obrigatórios:**
- [ ] Usar apenas variáveis CSS existentes (`var(--uni-blue)`, `var(--uni-ink)`); não introduzir novas
- [ ] `border-radius: 0` (estética ABNT; coerência com `.bridge-seq` / `.kc-box` / `.marker-pill`)
- [ ] Sem em-dash no comentário de bloco
- [ ] Comentário de bloco no padrão `=====...=====` dos demais componentes (linhas 81-83, 96-99, 115-117, 134-136, 158-161, 194-196, 212-214, 236-238, 265-269, 302-305, 321-323, 359-367)

---

### `apresentacao/assets/theme-unifacens.css` § `.eda-fig` + `.eda-insight` (utility, ~16 linhas)

**Tipo:** modificação (CSS-append)
**Papel:** componente reutilizável (figura embedded + texto destacado)
**Análogo primário (figura + caption):** `.slide-fig .fig-wrap` + `.slide-fig img` linhas 314-315 e `.slide-fig .fig-fonte` linha 319.

**CSS literal de referência (`.slide-fig`, linhas 306-319):**

```css
.slide-fig {
  display: flex; flex-direction: column; background: var(--uni-light);
  padding: 34px 56px 24px; --caret-color: var(--uni-blue);
  font-family: Arial, "Helvetica Neue", sans-serif;
}
.slide-fig .fig-wrap { flex: 1 1 auto; display: flex; align-items: center; justify-content: center; min-height: 0; margin-top: 2px; }
.slide-fig .fig-wrap img { max-width: 92%; max-height: 488px; object-fit: contain; }
.slide-fig .fig-fonte { margin-top: 8px; text-align: center; font-family: Arial, "Helvetica Neue", sans-serif; font-size: 18px; color: #5b6472; }
```

**Bloco a adicionar (do RESEARCH §6.5):**

```css
/* ===========================================================================
   SLIDE · EDA-03 · scatter PCA + insight em destaque
   `.eda-fig` envolve o PNG (centraliza + limita altura). `.eda-insight`
   é a frase de destaque (Arial bold 23px); `.eda-subinsight` é o subtítulo
   secundário (Arial 19px cinza, opcional).
   =========================================================================== */
.eda-fig {
  margin: 16px auto 0; max-width: 78%;
  display: flex; justify-content: center;
}
.eda-fig img { width: 100%; height: auto; max-height: 460px; object-fit: contain; }

.eda-insight {
  margin: 20px auto 0; max-width: 92%; text-align: center;
  font-family: Arial, "Helvetica Neue", sans-serif;
  font-size: 23px; font-weight: 700; color: var(--uni-ink);
  line-height: 1.35;
}
.eda-subinsight {
  margin-top: 10px; font-size: 19px; color: #5b6472; text-align: center;
  font-weight: 400;
}
```

**Gates obrigatórios:**
- [ ] Variáveis CSS existentes (`var(--uni-ink)`)
- [ ] `max-height: 460px` para a img — PNG 1200×700 (proporção ~1.71) cabe com folga em 720px de slide menos `.deck-topic` + `.eda-insight` + `.rel-cite`
- [ ] `text-align: center` no insight (única exceção ao left-align padrão de `.rel-lead`)
- [ ] Sem em-dash no comentário CSS

---

### `scripts/build_eda_pca_scatter.py` (utility Python, criação, ~80 linhas)

**Tipo:** criação
**Papel:** script standalone one-shot para gerar PNG do scatter PCA dos 3 perfis K-Means
**Análogo primário:** `scripts/build_methodology_figures.py` (mesmo prefixo `build_<artefato>`, mesma estrutura ROOT + Path + matplotlib `Agg`, mesmo padrão `_save(fig, name)`).

**Imports pattern** (de `scripts/build_methodology_figures.py` linhas 1-29):

```python
"""Gera as figuras de docs/METODOLOGIA_FERRAMENTAS.md.

Saída: PNGs em docs/figures/. Tudo via matplotlib puro (sem dependência de
graphviz CLI). As árvores AST/srcML usam layout hierárquico calculado a mão.

Uso:
    python scripts/build_methodology_figures.py            # gera todas
    python scripts/build_methodology_figures.py --only f4  # só uma
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from anytree import Node
from anytree.walker import Walker
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
```

**Padrão `_save` (linhas 82-87):**

```python
def _save(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    out = FIG_DIR / name
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[ok] {out.relative_to(ROOT)}")
```

**Adaptações para `build_eda_pca_scatter.py` (snippet completo no RESEARCH §6.3, linhas 644-737):**

1. Docstring no estilo do análogo:
   ```python
   """Gera scatter PCA 2D dos 3 perfis K-Means para o slide EDA-03 (fase 3 GSD).

   Saída: results/sec2_perfis_pca.png (1200×700 aprox). Cores UniFacens.
   SEED=42 fixo (random.seed, np.random.seed, KMeans random_state, PCA random_state).

   Uso:
       python scripts/build_eda_pca_scatter.py
   """
   ```
2. Imports (subset do análogo, sem `anytree`/`xml.etree`):
   ```python
   from __future__ import annotations
   import random
   from pathlib import Path

   import numpy as np
   import pandas as pd
   import matplotlib
   matplotlib.use("Agg")
   import matplotlib.pyplot as plt
   from sklearn.cluster import KMeans
   from sklearn.decomposition import PCA
   from sklearn.preprocessing import StandardScaler

   ROOT = Path(__file__).resolve().parents[1]
   DATA_ROOT = ROOT / "data" / "CSEDM"
   RESULTS = ROOT / "results"
   SEED = 42

   random.seed(SEED)
   np.random.seed(SEED)
   ```
3. Lógica de cluster_features (mesma da cell 44 do notebook 01_eda.ipynb, RESEARCH §6.3):
   - Carregar `early.csv` + `late.csv` em `ROOT / "data" /`
   - Carregar `Subject.csv` em `DATA_ROOT / "LinkTables" /`
   - Pivot `(SubjectID, AssignmentID) -> CorrectEventually.mean()` -> `_rate`
   - Pivot `(SubjectID, AssignmentID) -> Attempts.mean()` -> `_att`
   - Join com `X-Grade` e `.dropna()`
4. K-Means k=3 com `random_state=SEED`, nomeação por X-Grade média ordenada (Alto / Médio / Em risco)
5. PCA `n_components=2` com `random_state=SEED`
6. Scatter com paleta UniFacens-friendly (Pitfall 5 RESEARCH):
   ```python
   palette = {
       "Alto desempenho": "#2667FF",  # uni-blue
       "Médio":           "#F2A516",  # âmbar
       "Em risco":        "#D7191C",  # vermelho
   }
   ```
7. Save em `RESULTS / "sec2_perfis_pca.png"` com `dpi=120`, `bbox_inches="tight"`, `facecolor="white"`, `figsize=(12, 7)`
8. Print resumo numérico ao final (para validação cruzada com slide):
   ```python
   print()
   print("=== Resumo por perfil (alimenta texto do slide EDA-03) ===")
   print(cluster_features.groupby("perfil")[["X-Grade"]].agg(["count", "mean"]))
   ```

**Gates obrigatórios:**
- [ ] SEED=42 em 4 pontos: `random.seed`, `np.random.seed`, `KMeans(random_state=SEED)`, `PCA(random_state=SEED)`
- [ ] `matplotlib.use("Agg")` antes de qualquer `import matplotlib.pyplot` (consistência com análogo linha 19-20)
- [ ] `ROOT = Path(__file__).resolve().parents[1]` (padrão fixado no análogo linha 28)
- [ ] Output em `results/sec2_perfis_pca.png` (não em `apresentacao/assets/` direto — plano copia depois conforme STRUCTURE.md)
- [ ] Print do resumo numérico ao final (validação visual contra slide)
- [ ] Sem em-dash no docstring (D-70)
- [ ] Cores `#2667FF` / `#F2A516` / `#D7191C` (não default `tab10` — Pitfall 5 RESEARCH)

**Riscos / pitfalls:**
- **Pitfall 8 RESEARCH:** se planner copiar números do D-66c sem rodar o script, slide entrega `(n=139)` em Alto enquanto script gera `(n=96)`. Plano DEVE incluir sub-task "rodar `python scripts/build_eda_pca_scatter.py` e capturar print do resumo numérico para validação".
- **Pitfall 6 RESEARCH:** PNG fica em `results/`; slide aponta para `apresentacao/assets/eda-perfis-pca.png`. Plano DEVE incluir `cp results/sec2_perfis_pca.png apresentacao/assets/eda-perfis-pca.png`.
- Dependência de `early.csv` + `late.csv` em `data/` (não `data/CSEDM/`); RESEARCH §6.3 confirma localização (verificada em cell 35 do notebook 01).

---

### `results/sec2_perfis_pca.png` (binary asset, criação)

**Tipo:** criação (gerada pelo script)
**Papel:** PNG de figura científica (scatter PCA 2D com 3 clusters K-Means)
**Análogo:** não há análogo de markup; PNG é saída binária do script `build_eda_pca_scatter.py`.

**Especificação:**
- Dimensões aproximadas: 1200×700 (figsize 12×7 × dpi 120 ~= 1440×840; `bbox_inches='tight'` aplica crop final para ~1200×700)
- 3 grupos coloridos: azul `#2667FF` (Alto desempenho ~96 alunos), âmbar `#F2A516` (Médio ~19), vermelho `#D7191C` (Em risco ~124)
- Legenda inferior-esquerda com `(n=...)` em cada label
- Eixos rotulados PC1 / PC2 (fontsize 14); grid alpha 0.18
- Fundo branco (`facecolor="white"`)

**Validação pós-geração:**
- Abrir o PNG (e.g. `xdg-open results/sec2_perfis_pca.png`) e confirmar: 3 grupos visíveis; cores casam com paleta; legenda legível; contagem n condiz com o print do script
- Copiar para `apresentacao/assets/eda-perfis-pca.png` antes do commit do slide

---

### `apresentacao/STYLE.md` § linhas 108-132 (opcional, drive-by ao fim da fase)

**Tipo:** modificação (sentence-replace, opcional)
**Papel:** docs (inventário + gaps reservados)
**Análogo:** as próprias linhas 108-125 (§Inventário pós-fase 2, 12 → 20 slides após inserção) e 127-132 (§Gaps reservados — remover gap consumido).
**Status:** D-61 do CONTEXT diz "nenhuma correção do STYLE.md é necessária nesta fase". Atualização é opcional mas recomendada pelo RESEARCH §8 para manter STYLE.md sempre consistente (padrão da fase 2 em `f4dde9c`).

**Diff sugerido (RESEARCH §8.1) — §Inventário "pós-fase 2" → "pós-fase 3":**

Substituir linhas 108-125 atuais (12 linhas de tabela) por 20 linhas (4 novas inseridas no índice 11-14, índices 11-15 deslocados para 15-19). Tabela pronta no RESEARCH §8.1.

**Diff sugerido (RESEARCH §8.2) — §Gaps reservados linha 130:**

Remover ou marcar como done a linha:
```markdown
- Após MARKER-01 e antes do trio Martins+fig: EDA-01, EDA-02, EDA-03 + MARKER-02 (fase 3).
```

Resultado fica com 3 gaps remanescentes (fases 4 e 5) — texto pronto no RESEARCH §8.2.

**Discretion (planner):**
- **Commit separado** `docs(style): atualizar inventário e gaps pós-fase 3` no fim da fase (sugerido RESEARCH §8 + Open Question 2).
- **Alternativa:** junto com último plan (MARKER-02 normalmente é o último, dependendo da ordem de execução). Reviewer decide no checkpoint.

**Gates:**
- [ ] Indices da tabela §Inventário batem com o estado real do `index.html` pós-inserção (20 sections, slide-code em `#/15`)
- [ ] Sem em-dash em texto novo do STYLE.md
- [ ] Sentenças do §Gaps reservados refletem que o gap da fase 3 foi consumido

---

## Shared Patterns

### Estrutura externa de slide (NUNCA alterar)

**Origem:** `apresentacao/index.html` toda, especialmente linhas 134-147 (Yağcí), 149-164 (INTRO-01), 166-181 (INTRO-03a), 183-198 (INTRO-03b), 200-243 (MARKER-01). **Aplica a:** todos os 4 sections novos.

```html
<!-- ============ SLIDE · descrição em PT-BR ============ -->
<section data-background-color="#F1F6FB">
  <div class="deck-slide slide-XYZ">
    <svg class="wm" viewBox="0 0 136.7 139.78" aria-hidden="true"><use href="#sym"/></svg>
    <!-- conteúdo do slide aqui -->
  </div>
</section>
```

**Regras invioláveis (STYLE.md linhas 10-18, CONVENTIONS):**
- Reveal.js força `display:block` na `<section>`; layout fica no `<div>` interno. NUNCA mudar.
- `<svg class="wm">` (marca d'água Facens) em todos os 4 novos (inclusive MARKER-02).
- `data-background-color="#F1F6FB"` (fundo de conteúdo padrão).
- Indentação 6 espaços para o `<section>` raiz (consistente com sections existentes).
- EOL Unix (preservar; não introduzir CRLF).

---

### Cabeçalho `> [seção]` (aplica a EDA-01, EDA-02, EDA-03; NÃO aplica a MARKER-02)

**Origem:** CSS `theme-unifacens.css` linhas 42-43 (`.deck-topic`), aplicado em todos os slides INTRO/EDA (índices 3-9, 11-13, 15-19 do mapa pós-fase 3). MARKER-02 usa `.marker-title` (linha 376) em vez de `.deck-topic`.

```html
<p class="deck-topic"><span class="ps1">&gt;</span>nome da seção<span class="caret blink"></span></p>
```

**Cabeçalhos recomendados nesta fase (RESEARCH §7):**

| REQ | Texto dentro do `.deck-topic` (recomendado) | Fallback aceito |
|---|---|---|
| EDA-01 | `como navegamos o csedm` | `o curso por dentro` / `os 5 assignments` |
| EDA-02 | `aproximação ao protocolo` | `pré-processamento` / `do bruto ao split` |
| EDA-03 | `três jeitos de aprender` | `perfis dos alunos` / `quem tenta, quem desiste` |
| MARKER-02 | (sem `.deck-topic` — usa `.marker-title` com `AS QUATRO FASES DA EDM`) | — |

**Regras herdadas (D-68, STYLE.md linhas 37-60):**
- Texto do cabeçalho minúsculo, em Cascadia 24px, cor `#5b6472` (cor padrão; mas CSS `.deck-topic` linha 42 atual usa `color: var(--uni-ink)` ABNT-friendly)
- `<span class="caret blink"></span>` como **último filho** de `<p class="deck-topic">`
- `>` em azul UniFacens (CSS `.deck-topic .ps1` linha 43)
- MARKER-02 fica **sem** `.deck-topic` (D-63d / D-34d herdado)

---

### Voz autoral + paráfrase indireta (aplica a EDA-01, EDA-02, EDA-03)

**Origem:** D-25 fase 1 + D-43 fase 2 + D-69 fase 3. STYLE.md §Regras de redação linhas 83-95.

**Regras:**
- **Primeira pessoa do plural** quando apropriado ("Nosso pré-processamento...", "Encontramos a base via...", "Mantivemos 410...")
- **Autor parentético** com `<i>et al.</i>` ABNT (D-54 herdado, sweep de batch fase 2): `(Shi <i>et al.</i>, 2022)`
- **Autor prominente** aceitável quando autor é foco do slide ("Shi <i>et al.</i> (2022) apontam que...") — usado em INTRO-03a; EDA-* prefere parentético
- **Sem `<blockquote>`** (D-69 trava: citação direta literal **proibida** nos 4 slides)
- Texto corre como `<p class="rel-lead">` (Arial 25px, CSS linha 164 — `.slide-related .rel-lead`)

**Phrasing-alvo consolidado (RESEARCH §7.4):**

| Slide | Citação no corpo | Rodapé Fonte: |
|---|---|---|
| EDA-01 | `(Shi <i>et al.</i>, 2022)` em parágrafo abertura | `Fonte: análise sobre CSEDM (Spring 2019).` |
| EDA-02 | `(Shi <i>et al.</i>, 2022)` única, no 1º `.rel-lead` | `Fonte: adaptado de Shi <i>et al.</i> (2022).` |
| EDA-03 | (sem citação Shi — cluster é nosso) | `Fonte: análise sobre CSEDM (Spring 2019); <i>K-Means</i> k=3 com SEED=42.` |
| MARKER-02 | (sem corpo textual) | `Fonte: adaptado de Zorić (2020).` |

**Pitfall (RESEARCH Pitfall 1):** os phrasings de §1.2, §2.4, §7.1-7.3 do RESEARCH podem conter em-dash digitado em prosa. Validar com `grep -n '—'` antes do commit. Converter para vírgula/dois-pontos/parênteses (D-70).

---

### Rodapé "Fonte:" — uma linha por slide (D-71)

**Origem:** `apresentacao/index.html` linhas 145 (Yağcí `.rel-cite`), 162 (INTRO-01 `.rel-cite`), 179 (INTRO-03a `.rel-cite`), 196 (INTRO-03b `.rel-cite`), 241 (MARKER-01 `.rel-cite`). **CSS-suporte:** `.slide-related .rel-cite` linha 182 do CSS (`margin-top: auto`, Arial 18px `#5b6472`) e `.slide-marker .rel-cite` linha 452 (`margin-top: 0`, mesmo Arial 18px `#5b6472`).

**Decisão:** **reutilizar `.rel-cite`** para os 3 slides EDA (mesmo template `.slide-related`; zero CSS novo). MARKER-02 também usa `.rel-cite` herdada do `.slide-marker .rel-cite`.

**Formato literal por slide:**

| Slide | Texto literal do rodapé |
|---|---|
| EDA-01 | `Fonte: análise sobre CSEDM (Spring 2019).` |
| EDA-02 | `Fonte: adaptado de Shi <i>et al.</i> (2022).` |
| EDA-03 | `Fonte: análise sobre CSEDM (Spring 2019); <i>K-Means</i> k=3 com SEED=42.` |
| MARKER-02 | `Fonte: adaptado de Zorić (2020).` |

---

### Sem em-dash em prosa (D-70, vinculante)

**Aplica a:** texto novo dos 4 slides + comentário do script Python + comentário CSS dos blocos novos.

**Regra:** preferir vírgula, dois-pontos ou parênteses. Memória `feedback_no_em_dashes` vinculante.

**Validação obrigatória pré-commit (RESEARCH Pitfall 1):**

```bash
grep -n '—' apresentacao/index.html | grep -E '(como navegamos|aproximação ao|três jeitos|MARKER · As quatro fases.*fase 2)'
# deve retornar vazio

grep -n '—' apresentacao/assets/theme-unifacens.css | grep -E '(eda-grid|eda-fig|eda-insight)'
# deve retornar vazio

grep -n '—' scripts/build_eda_pca_scatter.py
# deve retornar vazio
```

---

### Estrangeirismos e nomes próprios (D-72)

| Categoria | Tratamento | Onde aparece nesta fase |
|---|---|---|
| `<i>baseline</i>` | itálico minúsculas | EDA-02 corpo |
| `<i>knowledge tracing</i>` | itálico minúsculas | (não usado nesta fase; já em INTRO-03a) |
| `<i>cluster</i>` | itálico minúsculas | (potencialmente EDA-03 se aparecer; default fora do slide) |
| `<i>K-Means</i>` | itálico minúsculas | EDA-03 rodapé |
| `<i>scatter</i>` | itálico minúsculas | (não aparece no texto do slide; só no `alt` da img) |
| `<i>assignment</i>` / `<i>assignments</i>` | itálico minúsculas | EDA-01 e EDA-02 corpo, EDA-03 subinsight |
| `<i>pipeline</i>` | itálico minúsculas | (não usado nesta fase) |
| `<i>et al.</i>` | itálico ABNT em qualquer citação parentética múltipla | EDA-01 corpo, EDA-02 corpo + rodapé |
| BKT, DKT, Code-DKT | sem itálico, maiúsculas | (NÃO mencionar nos 4 slides desta fase — gate forte fase 4) |
| ProgSnap2, CSEDM | nomes próprios, sem itálico | CSEDM em EDA-01/02/03 (ProgSnap2 não — Pitfall 2) |
| Shi, Zorić, Price | nomes de autor sem itálico, encoding correto | Shi em EDA-01/02; Zorić em MARKER-02 |

---

### Comentário acima de cada `<section>`

**Padrão obrigatório** (vivo em todos os 16 sections atuais):

```html
<!-- ============ SLIDE · descrição em PT-BR ============ -->
```

**Comentários sugeridos para os 4 novos (RESEARCH §9.3):**

```html
<!-- ============ SLIDE · EDA-01 · Como navegamos o CSEDM (Spring 2019) ============ -->
<!-- ============ SLIDE · EDA-02 · Pré-processamento, aproximação ao protocolo (Shi et al., 2022) ============ -->
<!-- ============ SLIDE · EDA-03 · Três perfis de alunos, scatter PCA (CSEDM Spring 2019) ============ -->
<!-- ============ SLIDE · MARKER · As quatro fases da EDM, fase 2 concluida (Zoric, 2020) ============ -->
```

**Convenções herdadas:**
- 12 sinais `=` de cada lado
- Descrição curta em PT-BR
- Autor + ano entre parênteses no fim quando aplicável

---

### Validação visual fim-a-fim (D-74)

**Aplica a:** fim de fase (após inserção dos 4 sections + bloco CSS + script + PNG + STYLE.md opcional).

```bash
cd apresentacao && python3 -m http.server 8000
# abrir http://127.0.0.1:8000/#/0 e percorrer até #/19
```

**Checks por slide novo:**

| URL | Slide | Foco primário da inspeção |
|---|---|---|
| `#/11` | EDA-01 | Cabeçalho `> como navegamos o csedm`; tabela ABNT 5 linhas × 4 colunas; últimas coluna em azul UniFacens; rodapé `Fonte: análise sobre CSEDM (Spring 2019).`; sem ProgSnap2 no corpo |
| `#/12` | EDA-02 | Cabeçalho `> aproximação ao protocolo`; 3 `.rel-lead`; ponte 413 → 410 → 328/82 visível; truncagem 50 mencionada; rodapé `Fonte: adaptado de Shi <i>et al.</i> (2022).`; sem Code-DKT |
| `#/13` | EDA-03 | Cabeçalho `> três jeitos de aprender`; PNG scatter renderiza; insight em destaque (Arial bold 23px); 3 grupos coloridos visíveis (azul/âmbar/vermelho); rodapé com `<i>K-Means</i>` em itálico e `SEED=42` |
| `#/14` | MARKER-02 | Sem `.deck-topic`; título `AS QUATRO FASES DA EDM`; pill 1 e pill 2 com check em fundo azul; pill 3 com ícone reload girando; pill 4 com círculo cinza; badges `[done] [done] [running]` (pill 4 sem badge); rodapé `Fonte: adaptado de Zorić (2020).` |
| `#/15` | slide-code (deslocado de `#/11`) | Conteúdo inalterado; só posição mudou |

**Cache do http.server (STYLE.md linha 154):** se editar CSS, subir em outra porta (`python3 -m http.server 8001`) para forçar reload.

---

## Sequência recomendada de implementação (RESEARCH §7 + Open Question 6)

**Ordem:** **MARKER-02 → EDA-02 → EDA-01 → EDA-03**

**Razões (do mais determinístico ao mais arriscado):**
1. **MARKER-02 primeiro:** puro reuso de CSS (zero linhas novas); 4 deltas mecânicos validados em RESEARCH §5.2; valida pipeline de inserção e ambiente browser
2. **EDA-02 segundo:** números travados em D-65a (413 → 410 → 328/82); phrasing Shi 2022 §4.1/§4.2 confirmado literalmente no RESEARCH §1.1; 3 `.rel-lead` é template puro reuso
3. **EDA-01 terceiro:** calibra layout da tabela `.eda-grid` (CSS novo); números MainTable confirmados em RESEARCH §2.1
4. **EDA-03 quarto:** depende de gerar PNG novo via `scripts/build_eda_pca_scatter.py`; mais sub-tasks (script + cópia + slide); fecha com slide mais visual

**Granularidade de commits (CONVENTIONS.md + CONTEXT discretion):**
- **Sugerido:** 4 commits (um por slide). Padrão de fase 2.
- Mensagens (convenção lowercase português, prefixo `apresentacao:`):
  - `apresentacao: slide MARKER-02 - preparação dos dados ✓ (zero CSS novo)`
  - `apresentacao: slide EDA-02 - pré-processamento, aproximação ao protocolo (Shi et al., 2022)`
  - `apresentacao: slide EDA-01 - como navegamos o csedm (tabela A1..A5)`
  - `apresentacao: slide EDA-03 - perfis dos alunos (scatter PCA com SEED=42)`
- **Opcional:** 1 commit extra `docs(style): atualizar inventário e gaps pós-fase 3` ao fim (RESEARCH §8 + Open Question 2).

---

## No Analog Found

Nenhum (5/5 com analog). Todos os 4 slides novos, o script Python e o bloco CSS têm template-base vivo no codebase:

- **MARKER-02** → analog MARKER-01 (linhas 200-243 do index.html) — exato, 4 deltas mecânicos
- **EDA-01** → analog INTRO-01 (linhas 149-164) + `.bridge-seq .step` (linhas 201-206 do CSS, estética ABNT) — exato + role-match
- **EDA-02** → analog INTRO-03b (linhas 183-198, 3 × `.rel-lead`) — exato
- **EDA-03** → analog INTRO-03b host (linhas 183-198) + `.slide-fig .fig-wrap` (linhas 314-315, figura embed) — role-match
- **scripts/build_eda_pca_scatter.py** → analog `scripts/build_methodology_figures.py` (mesmo prefixo, ROOT/Path, matplotlib Agg) — exato
- **`.eda-grid`** → analog `.bridge-seq .step` + `.kc-box` (borda fina ABNT) — role-match
- **`.eda-fig` + `.eda-insight`** → analog `.slide-fig .fig-wrap` (figura) + classe nova `.eda-insight` sem analog direto (text-align center bold é primeira ocorrência) — role-match
- **results/sec2_perfis_pca.png** → saída binária; sem analog de markup
- **STYLE.md §Inventário** → identidade (edição de texto no próprio arquivo, modelo `pós-fase 2` linhas 108-125)

---

## Metadata

**Analog search scope:**
- `apresentacao/index.html` (564 linhas, HEAD em 2026-05-28)
- `apresentacao/assets/theme-unifacens.css` (453 linhas)
- `apresentacao/STYLE.md` (162 linhas)
- `scripts/build_methodology_figures.py` (cabeçalho/imports/_save lidos)
- `.planning/phases/02-intro-dataset-e-problema-fase-1-edm/02-PATTERNS.md` (referência de formato)
- `.planning/phases/03-eda-e-pr-processamento-fase-2-edm/03-CONTEXT.md` e `03-RESEARCH.md` (decisões e fontes)

**Files scanned:** 7. Nenhum re-read; ranges não-sobrepostos quando aplicável.
**Pattern extraction date:** 2026-05-28.

**Convention reminder (CLAUDE.md):** "Antes de redigir ou alterar slide que cite um autor, ler a referência completa em `docs/`" — vinculante para EDA-02 (Shi <i>et al.</i>, 2022); o RESEARCH §1.1 já fez a leitura literal das páginas 4-5 do `docs/Code-DKT.pdf` e extraiu os trechos relevantes ("410 students", "ratio of 4:1", "last 50 submissions"). O plano pode usar §1.2 do RESEARCH como referência de fidelidade para a paráfrase de EDA-02.

**Decisões de design herdadas vinculantes:**
- D-60..D-74 do CONTEXT desta fase
- D-31..D-47 da fase 2 (especialmente D-38b que mandata a ponte 413 → 410 → 328/82 nesta fase, D-44 sem em-dash, D-46 itálico, D-54 `<i>et al.</i>` ABNT)
- D-01..D-30 da fase 1 (especialmente D-01..D-03 padrão de cabeçalho, D-25 voz autoral)
- STYLE.md §"Cabeçalho de todo slide após a AGENDA" linhas 37-60
- STYLE.md §"Regras de redação" linhas 83-95 (sem em-dash, voz própria default)
- Memória `feedback_marker_design` (MARKER-XX redesign de `5d44606`; tabela de modificadores)
- Memória `project_split_discovery` (paper usa 80/20 de 410; migração Release/ → MainTable+Shi)
- Memórias `feedback_no_em_dashes`, `feedback_tcc_writing_style`, `reference_manual_citacoes`, `feedback_correlatos_antes` (vinculantes)
