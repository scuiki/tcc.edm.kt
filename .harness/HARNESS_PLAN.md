# Plano: Harness de Agentes para EDA, Pré-Processamento e Extração de Insights

## Contexto

O TCC 1 tem pipeline de 7 notebooks (00→07). Os notebooks `00_problem_definition.ipynb` e as seções 1-2 do `01_eda.ipynb` existem, mas foram escritos antes do harness. O objetivo é criar um harness multi-agente que **revise e padronize tudo desde o 00** e complete os notebooks restantes (seções 3-8 da EDA e o `02_preprocessing.ipynb`), garantindo qualidade didática uniforme, decisões fundamentadas em papers e rastreabilidade via git.

Nota: `docs/paper_references.md` (fatos extraídos dos PDFs) está sendo criado em outro contexto e estará disponível quando o harness rodar — não faz parte deste plano.

O harness de referência em `experiments/harness` usa padrão **Generator + Evaluator** com estado em JSON, comunicação via disco (não herança de contexto), e loops de retry. Este plano adapta esse padrão para notebooks Jupyter e o estende com uma **terceira camada de validação independente** para eliminar viés de auto-avaliação.

---

## Arquitetura: Três Camadas

O problema central do padrão Generator + Evaluator embutido no mesmo loop é o **viés por vazamento de critérios**: o Generator sabe exatamente o que o Evaluator vai checar (os prompts estão no mesmo `runner.py`) e pode otimizar superficialmente sem garantir qualidade real de pesquisa.

A solução é separar responsabilidades em três camadas com escopos e contextos distintos:

```
Layer 1 — Verificação Mecânica   (runner.py, automático)
  jupyter nbconvert --execute → notebook roda sem erros?
  Artefatos esperados existem em results/?

Layer 2 — Format Evaluator       (evaluator.py, dentro do loop de retry)
  Sessão Claude separada. Verifica APENAS conformidade estrutural:
  - Template markdown pré/pós-código presente em cada seção?
  - SEED=42 aparece no código?
  - Funções obrigatórias definidas?
  NÃO avalia qualidade de conteúdo, correção estatística nem validade de pesquisa.

Layer 3 — Content Validator      (validator.py, fora do loop, cego à implementação)
  Sessão Claude independente. Roda APÓS a implementação estar completa.
  Contexto: CLAUDE.md + paper_references.md + notebooks executados + artefatos.
  NÃO recebe: prompts do Generator, critérios do Format Evaluator, plan JSONs.
  Avalia: precisão estatística, validade de pesquisa, qualidade didática real.
  Output: results/validation_reports/<notebook>_validation.md
```

### Por que o Content Validator (Layer 3) resolve o viés

O Layer 3 é **cego** ao que o Generator foi instruído a fazer. Avalia o notebook como um revisor externo avaliaria um artigo — contra os objetivos de pesquisa do CLAUDE.md e os fatos dos papers, não contra o checklist de implementação. Não dispara retries automaticamente: produz um relatório para revisão humana. Se issues críticos forem encontrados, o pesquisador pode rerrodar o agente de implementação com o relatório como contexto adicional.

**Princípio dos critérios de validação:** o Content Validator não exige reprodução exata dos valores do paper. Exige que:
1. O valor seja **calculado dos dados**, não hardcoded ou omitido.
2. Se divergir do paper, o notebook **explique a divergência** (filtro diferente, split diferente, arredondamento, etc.).
3. A divergência faça sentido analítico — o validator avalia a justificativa, não rejeita automaticamente.

### Quatro agentes de implementação (planos JSON independentes, executados em ordem)

| Agente | Plano JSON | Escopo | Output |
|---|---|---|---|
| **Problem Definition Agent** | `problem_definition.json` | Revisa e padroniza `00_problem_definition.ipynb` | Notebook padronizado |
| **EDA Agent** | `eda.json` | Revisa seções 1-2 **e** completa seções 3-8 do `01_eda.ipynb` | Notebook completo + plots |
| **Preprocessing Agent** | `preprocessing.json` | Cria `02_preprocessing.ipynb` do zero | Notebook + artefatos CSV/pkl |
| **Insights Agent** | `insights_extraction.json` | Síntese pós-EDA + pré-proc | `docs/eda_insights.md` |

---

## Mecanismo de Referência a Papers

`docs/paper_references.md` estará disponível antes de rodar o harness. Os prompts do Generator incluem a instrução:

> *"Leia `docs/paper_references.md` antes de escrever qualquer célula markdown. Cada seção analítica deve citar o paper relevante (autor, ano)."*

O Format Evaluator verifica: *"Cada seção analítica tem ao menos uma citação no markdown?"*

---

## Padrão Didático de Células (obrigatório em todas as seções)

O Generator é instruído a seguir este template para cada seção analítica:

```markdown
### N.X — Título da Seção

**Contexto:** Por que esta análise importa para o problema de KT.
**Hipótese:** O que esperamos encontrar com base nos papers.
**Referência:** Autor (ano); Autor (ano).
```

→ código de análise →

```markdown
**Achado:** [resultado quantitativo principal]
**Implicação para modelagem:** Como este achado afeta escolha de BKT/DKT/Code-DKT.
```

Este template é verificado pelo Format Evaluator em **todos** os notebooks.

---

## Schema dos Planos JSON

Cada plano JSON segue este schema (adaptado do harness de referência com adição de `verify_cmd`):

```json
{
  "slug": "eda",
  "title": "EDA — revisar seções 1-2 e completar 3-8",
  "type": "feature",
  "created": "2026-04-29",
  "status": "planned",
  "verify_cmd": [
    "jupyter", "nbconvert", "--to", "notebook", "--execute",
    "--inplace", "notebooks/01_eda.ipynb",
    "--ExecutePreprocessor.timeout=600"
  ],
  "context": "Por que este trabalho é necessário...",
  "tasks": [
    {
      "id": "1",
      "title": "Título da tarefa",
      "status": "pending",
      "acceptance_criteria": [
        "Critério testável e específico 1",
        "Critério testável e específico 2"
      ],
      "files": ["notebooks/01_eda.ipynb"],
      "depends_on": []
    }
  ]
}
```

**Regras:**
- `verify_cmd` fica no nível raiz do plano (varia por notebook); o runner lê daqui em vez de ter `VERIFY_CMD` fixo no código.
- `acceptance_criteria`: lista de strings testáveis e específicas. O Format Evaluator verifica cada uma. Nunca use critérios vagos como "boa qualidade".
- `depends_on`: lista de `id`s de tasks que devem estar `"complete"` antes desta começar. O runner respeita essa ordem.
- `files`: hints de quais arquivos a task vai tocar — não vinculante, mas orienta o Generator.
- `SOURCE_DIRS` global: `["notebooks/", "src/"]` (em vez de `["src/"]` do template original).
- `CLAUDE_MD_PATH`: `"CLAUDE.md"` (mantém do template original).
- TDD obrigatório do template original **não se aplica** — substituído por sanidade estatística nos ACs.

---

## Prompt do Generator (adições-chave ao template base)

```
Antes de implementar qualquer célula:
1. Leia CLAUDE.md para regras do projeto (SEED=42, uso do Release/Train, etc.)
2. Leia docs/paper_references.md para referências a citar no markdown
3. Para REVISÃO de seções existentes: mantenha o conteúdo analítico correto,
   adicione/ajuste células markdown para seguir o template didático padrão
4. Para NOVAS seções: escreva primeiro markdown (contexto, hipótese, ref),
   depois código, depois markdown (achado, implicação)
5. Não invente estatísticas — calcule do dataset; se divergirem do paper, explique no markdown
6. Nenhum placeholder: cada função completamente implementada, sem pass/TODO/NotImplementedError
7. Busque antes de implementar (grep) — funções podem já existir em src/
```

---

## Format Evaluator — Prompt e Veredito

### Prompt (escopo reduzido — apenas formato)

```
Você é um avaliador de conformidade estrutural. Verifique APENAS:
- Cada seção analítica tem célula markdown antes do código? (campos Contexto, Hipótese, Referência presentes?)
- Cada seção analítica tem célula markdown após o código? (campos Achado, Implicação para modelagem presentes?)
- SEED=42 aparece explicitamente no código (quando aplicável a cálculos aleatórios)?
- Funções obrigatórias listadas nos acceptance_criteria estão definidas?
- Há citação a ao menos um paper em cada seção analítica?

NÃO avalie: qualidade do conteúdo, correção de estatísticas, profundidade analítica, validade de pesquisa.
Quando em dúvida sobre um critério de formato, marque FAIL — é melhor falso positivo que deixar passar.
```

### Formato do Veredito (obrigatório — parser do runner lê este bloco)

```
VERDICT
task: {id}
title: {title}

notebook_executes: PASS|FAIL
acceptance_criteria: PASS|FAIL
template_compliance: PASS|FAIL|WARN
no_placeholders: PASS|FAIL

ac_checklist:
- [x] Texto do AC (PASS)
- [ ] Texto do AC (FAIL — o que está faltando)

issues:
- Descrição do issue 1
- Descrição do issue 2

OVERALL: PASS|FAIL
```

**Regras de scoring:**
- `OVERALL = FAIL` se qualquer um de `notebook_executes`, `acceptance_criteria`, `no_placeholders` for FAIL.
- `template_compliance: WARN` não causa OVERALL FAIL (apenas registra).
- Feedback estruturado é salvo em `eval_feedback/{slug}_{task_id}.json` para o generator usar no retry.

---

## Content Validator (Layer 3) — validator.py

### Interface

```bash
# Validar um notebook
python3 .harness/validator.py --notebook notebooks/01_eda.ipynb

# Validar todos em batch
python3 .harness/validator.py --all

# Dry-run (imprime prompt sem executar — confirmar que NÃO contém plan JSONs)
python3 .harness/validator.py --notebook notebooks/01_eda.ipynb --dry-run
```

### Comportamento

1. Lê o notebook executado (JSON do `.ipynb`)
2. Lê o critério correspondente de `.harness/validation_criteria/<notebook>_criteria.md`
3. Spawna sessão Claude com contexto: `CLAUDE.md` + `docs/paper_references.md` + notebook + artefatos relevantes de `results/`
4. **Não passa** prompts do Generator, critérios do Format Evaluator nem plan JSONs
5. Escreve relatório em `results/validation_reports/<nome>_validation.md`
6. Retorna exit code 0 (pass) ou 1 (issues críticos encontrados)

### Critérios por notebook (validation_criteria/)

Arquivos escritos em termos de **objetivos de pesquisa**, não de passos de implementação.

**`validation_criteria/eda_criteria.md`:**
- Taxa de corretos em Release/Train é calculada dos dados e reportada? Se divergir de 23.70% (Shi et al., 2022), há explicação no markdown?
- Duplicate rows são explicadas? A hipótese (Run.Program gera filho Compile com mesmo timestamp) é enunciada?
- Seção de Compile.Error quantifica a proporção? Conecta ao srcML-DKT?
- Curvas de aprendizagem estão presentes e discutidas (independente da direção da tendência)?
- Imbalance ratio é calculado e justifica o uso de AUC?

**`validation_criteria/preprocessing_criteria.md`:**
- `filter_for_bkt_dkt` usa apenas Run.Program? Há log ou assertion confirmando?
- `filter_for_code_dkt` inclui Compile.Error com correct=0? Decisão documentada?
- Alguma sequência tem mais de 50 elementos após truncagem? (deve ser zero)
- Taxa de corretos do split processado é reportada? Se divergir do bruto, há explicação?

**`validation_criteria/problem_definition_criteria.md`:**
- KC=ProblemID está documentado com justificativa metodológica?
- First-attempt AUC é definida como métrica primária com justificativa?
- All-attempts AUC é definida como secundária com papel complementar explicado?

---

## Formato do progress.md

Cada task concluída deve ter uma entrada appended ao `.harness/progress.md` com este formato:

```markdown
## YYYY-MM-DD - {slug}: Task {id} - {title}

- O que foi implementado
- Decisões-chave e por quê
- Veredito do Format Evaluator (PASS na primeira | PASS após N retries | issues encontrados)
- Bugs ou inconsistências encontrados no dataset (se houver)
- O que trabalhar a seguir
```

---

## Planos JSON — Tarefas por Agente

### `problem_definition.json` — 2 tarefas

**Task 1 — Aplicar template didático em todas as seções existentes**
- `files`: `["notebooks/00_problem_definition.ipynb"]`
- `depends_on`: `[]`
- `acceptance_criteria`:
  - Cada seção analítica tem célula markdown pré-código com campos Contexto, Hipótese e Referência
  - Cada seção analítica tem célula markdown pós-código com campos Achado e Implicação para modelagem
  - Nenhuma seção analítica existente foi removida ou substancialmente alterada no conteúdo

**Task 2 — Validar e documentar decisões de modelagem**
- `files`: `["notebooks/00_problem_definition.ipynb"]`
- `depends_on`: `["1"]`
- `acceptance_criteria`:
  - Seção sobre KC=ProblemID presente com justificativa ("um modelo por assignment, mesmo protocolo Shi et al. 2022")
  - Seção sobre métricas define first-attempt AUC como primária com justificativa (autocorrelação temporal, imbalance)
  - Seção sobre métricas define all-attempts AUC como secundária com papel complementar
  - Tabela summary de decisões de modelagem presente ao final do notebook

---

### `eda.json` — 8 tarefas

**Task 1 — Revisar Seção 1 (Estatísticas básicas e qualidade)**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `[]`
- `acceptance_criteria`:
  - Template didático aplicado (markdown pré + pós código em cada subseção)
  - Citação a ProgSnap2 presente no markdown
  - Duplicate rows (236.024 registros com mesmo timestamp) explicadas como comportamento esperado

**Task 2 — Revisar Seção 2 (Desempenho de estudantes e clustering)**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["1"]`
- `acceptance_criteria`:
  - Template didático aplicado
  - SEED=42 explícito no código de clustering
  - Três perfis de estudante nomeados e interpretados no markdown pós-código

**Task 3 — Seção 3: Estrutura de assignments e dificuldade**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["2"]`
- `acceptance_criteria`:
  - Plot de taxa de acerto por problema por assignment presente
  - Ranking de dificuldade calculado e discutido no markdown
  - Citação ao Code-DKT paper (Shi et al. 2022) no markdown

**Task 4 — Seção 4: Curvas de aprendizado e sequências**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["3"]`
- `acceptance_criteria`:
  - Learning curve por assignment plotada e discutida
  - Distribuição de tamanho de sequências por estudante calculada
  - Truncagem em 50 tentativas citada e justificada com referência a Shi et al. 2022

**Task 5 — Seção 5: Análise do Score e desbalanceamento**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["4"]`
- `acceptance_criteria`:
  - Histograma do Score calculado dos dados (não hardcoded)
  - Análise de scores parciais (0 < Score < 1) reportada com proporção calculada dos dados
  - Imbalance ratio por assignment calculado
  - Escolha de AUC justificada com base no imbalance observado

**Task 6 — Seção 6: Evolução do código e Compile.Error**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["5"]`
- `acceptance_criteria`:
  - Compile.Error rate por assignment calculada dos dados
  - CodeStateIDs únicos por problema calculados
  - Markdown conecta Compile.Error ao srcML-DKT (Pankiewicz et al. 2025)

**Task 7 — Seção 7: Padrões temporais e procrastinação**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["6"]`
- `acceptance_criteria`:
  - Distribuição de atividade por semana ou dia plotada
  - Correlação entre timing e desempenho calculada e discutida no markdown

**Task 8 — Seção 8: Correlação de features com Label**
- `files`: `["notebooks/01_eda.ipynb"]`
- `depends_on`: `["7"]`
- `acceptance_criteria`:
  - Correlação Spearman entre features e Label (early/late) calculada
  - Importância via Decision Tree calculada com SEED=42
  - Top-5 features identificadas e listadas no markdown
  - Nota sobre avaliação first-attempt presente (apenas primeira tentativa por problema por estudante)

---

### `preprocessing.json` — 5 tarefas

**Task 1 — Setup e carregamento dos dados**
- `files`: `["notebooks/02_preprocessing.ipynb", "src/data_loader.py"]`
- `depends_on`: `[]`
- `acceptance_criteria`:
  - Seção markdown explica os dois splits (All e Release) e quando usar cada um
  - Funções de carregamento definidas com docstrings

**Task 2 — Filtragem por modelo**
- `files`: `["notebooks/02_preprocessing.ipynb", "src/data_loader.py"]`
- `depends_on`: `["1"]`
- `acceptance_criteria`:
  - `filter_for_bkt_dkt()` definida, usa apenas Run.Program
  - `filter_for_code_dkt()` definida, inclui Run.Program + Compile.Error com correct=0
  - Assertions ou logs inline verificam que nenhum outro EventType passou pelos filtros

**Task 3 — Construção de sequências KT**
- `files`: `["notebooks/02_preprocessing.ipynb", "src/data_loader.py"]`
- `depends_on`: `["2"]`
- `acceptance_criteria`:
  - `build_sequences(df, assignment_id)` definida e retorna sequências ordenadas por timestamp
  - Cada sequência inclui flag de primeira tentativa por problema por estudante (para first-attempt AUC)
  - Markdown explica estrutura de dados das sequências

**Task 4 — Truncagem e validação**
- `files`: `["notebooks/02_preprocessing.ipynb"]`
- `depends_on`: `["3"]`
- `acceptance_criteria`:
  - Lógica de truncagem implementada (últimas 50 tentativas)
  - Assertion confirma que nenhuma sequência tem mais de 50 elementos
  - Taxa de corretos do split processado calculada e reportada

**Task 5 — Serialização dos artefatos**
- `files`: `["notebooks/02_preprocessing.ipynb"]`
- `depends_on`: `["4"]`
- `acceptance_criteria`:
  - `results/sequences_bkt_dkt.pkl` existe após execução do notebook
  - `results/sequences_code_dkt.pkl` existe após execução do notebook
  - Schema dos artefatos documentado em markdown
  - Markdown final apresenta estatísticas dos artefatos (n sequências, n estudantes, distribuição de comprimento)

---

### `insights_extraction.json` — 3 tarefas

O Insights Agent usa apenas ferramentas de **leitura** — lê notebooks e artefatos, escreve apenas `docs/eda_insights.md`.

**Task 1 — Síntese: imbalance, sequências e perfis**
- `files`: `["docs/eda_insights.md"]`
- `depends_on`: `[]`
- `acceptance_criteria`:
  - Seção por cada achado EDA crítico (imbalance, sequências, perfis de estudante)
  - Cada achado quantificado e ancorado em célula específica do notebook (referência explícita)

**Task 2 — Implicações das decisões de pré-processamento**
- `files`: `["docs/eda_insights.md"]`
- `depends_on`: `["1"]`
- `acceptance_criteria`:
  - Seção explica por que Compile.Error entra no Code-DKT e não nos outros modelos
  - Justificativa do threshold Score==1.0 documentada
  - Rationale para usar Release split vs All documentado

**Task 3 — Recomendações para notebooks 03-07**
- `files`: `["docs/eda_insights.md"]`
- `depends_on`: `["2"]`
- `acceptance_criteria`:
  - Lista de decisões de modelagem ancoradas nos achados da EDA
  - Sinalizações de risco por assignment (ex: A4/A5 com menos dados) presentes

---

## Sequência de Execução

```bash
# --- Implementação ---

# 1. Problem definition
python3 .harness/runner.py --plan .harness/plans/problem_definition.json --loop

# 2. EDA (revisa seções 1-2, completa 3-8)
python3 .harness/runner.py --plan .harness/plans/eda.json --loop

# 3. Preprocessing
python3 .harness/runner.py --plan .harness/plans/preprocessing.json --loop

# 4. Insights (depende dos três anteriores)
python3 .harness/runner.py --plan .harness/plans/insights_extraction.json --loop

# --- Validação independente (após implementação completa) ---

python3 .harness/validator.py --notebook notebooks/00_problem_definition.ipynb
python3 .harness/validator.py --notebook notebooks/01_eda.ipynb
python3 .harness/validator.py --notebook notebooks/02_preprocessing.ipynb
# Ou batch:
python3 .harness/validator.py --all

# --- Flags úteis de manutenção ---

# Tarefa específica
python3 .harness/runner.py --plan .harness/plans/eda.json --task 3

# Dry-run (imprime prompts sem executar)
python3 .harness/runner.py --plan .harness/plans/eda.json --dry-run

# Apenas avaliação (sem rodar generator)
python3 .harness/runner.py --plan .harness/plans/eda.json --eval-only 3

# Pular avaliação (útil para debug do generator)
python3 .harness/runner.py --plan .harness/plans/eda.json --task 3 --skip-eval

# Rerrodar fix após avaliação manual
python3 .harness/runner.py --plan .harness/plans/eda.json --fix 3
```

---

## Verificação End-to-End

1. **Smoke test:** `python3 .harness/runner.py --plan .harness/plans/eda.json --dry-run` — imprime prompt sem erros e sem vazar conteúdo dos plan JSONs no prompt do validator
2. **EDA executável:** `jupyter nbconvert --to notebook --execute notebooks/01_eda.ipynb --output /tmp/eda_check.ipynb` — completa sem exceções
3. **Preprocessing:** `results/sequences_bkt_dkt.pkl` e `results/sequences_code_dkt.pkl` existem e têm schema correto
4. **Insights:** `docs/eda_insights.md` gerado com as três seções esperadas
5. **Template didático:** Todos os notebooks têm células markdown pré/pós-código em cada seção
6. **Validator cego:** `python3 .harness/validator.py --notebook notebooks/01_eda.ipynb --dry-run` — confirmar que o prompt NÃO contém trechos dos plan JSONs nem dos prompts do Generator
7. **Relatórios gerados:** `results/validation_reports/` contém um `.md` por notebook validado
8. **Git history:** Um commit por tarefa concluída (rastreabilidade completa)

---

## Arquivos a Criar

```
tcc.edm.kt/
└── .harness/
    ├── runner.py                    # Adaptar de experiments/harness — verify_cmd por plano, flags --fix/--skip-eval/--eval-only
    ├── evaluator.py                 # Adaptar — escopo reduzido (formato apenas), novo VERDICT format
    ├── validator.py                 # NOVO — validação independente (Layer 3), cego à implementação
    ├── progress.md                  # Session notes (formato definido acima)
    ├── plans/
    │   ├── problem_definition.json
    │   ├── eda.json
    │   ├── preprocessing.json
    │   └── insights_extraction.json
    ├── validation_criteria/         # NOVO — critérios do Content Validator
    │   ├── eda_criteria.md
    │   ├── preprocessing_criteria.md
    │   └── problem_definition_criteria.md
    └── eval_feedback/               # JSON por task — {slug}_{task_id}.json — usado pelo generator no retry
```

## Arquivos Críticos do Projeto

| Arquivo | Ação |
|---|---|
| `.harness/runner.py` | Criar (adaptar de experiments/harness) — `verify_cmd` por plano, adicionar `--fix`, `--skip-eval`, `--eval-only` |
| `.harness/evaluator.py` | Criar (adaptar de experiments/harness) — escopo reduzido a formato, novo bloco VERDICT |
| `.harness/validator.py` | Criar (NOVO) — Layer 3, cego à implementação |
| `.harness/validation_criteria/eda_criteria.md` | Criar |
| `.harness/validation_criteria/preprocessing_criteria.md` | Criar |
| `.harness/validation_criteria/problem_definition_criteria.md` | Criar |
| `.harness/plans/problem_definition.json` | Criar |
| `.harness/plans/eda.json` | Criar |
| `.harness/plans/preprocessing.json` | Criar |
| `.harness/plans/insights_extraction.json` | Criar (agente read-only) |
| `notebooks/00_problem_definition.ipynb` | Modificar (via agente — padronização) |
| `notebooks/01_eda.ipynb` | Modificar (via agente — revisão + completar) |
| `notebooks/02_preprocessing.ipynb` | Criar (via agente) |
| `docs/eda_insights.md` | Criar (via agente) |
