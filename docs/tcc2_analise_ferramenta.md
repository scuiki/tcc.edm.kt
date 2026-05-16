# TCC 2 — Análise de Viabilidade da Ferramenta EDM

> Documento gerado a partir do debate inicial sobre escopo e arquitetura da ferramenta docente.
> Data: 2026-05-12 — **Atualizado com as decisões do grupo em 2026-05-12**

---

## Situação Atual do TCC 1

O pipeline está ~60% completo:

| Feito | Pendente |
|---|---|
| EDA completa (notebook 01) | Extração de features AST/code2vec (notebook 03) |
| Pré-processamento + sequências (notebook 02) | Etapas 6–7 do KCGen-KT (corretude por KC) |
| KC generation via LLM — etapas 1–5 (notebook 03b) | DKT LSTM (notebook 05) |
| Q-matrices para os 5 assignments | Code-DKT com srcML (notebook 06) |
| BKT baseline treinado (first-AUC: 63–64%) | Comparação final + Wilcoxon (notebook 07) |

O TCC 1 entrega a evidência empírica (qual modelo performa melhor e com quais KCs). O TCC 2 usa essa evidência para construir a ferramenta. **O Code-DKT será o modelo central do TCC 2** — a análise dos códigos submetidos é o diferencial real da ferramenta. BKT e DKT entram como opções secundárias.

---

## Análise das Ideias para o TCC 2

### 1. Ingestão de Dataset (ProgSnap2)

**Viável.** O `data_loader.py` já faz isso para o CSEDM. Generalizar para qualquer ProgSnap2 é trabalho de engenharia, não pesquisa.

Quanto a outros formatos: não recomendado para o TCC 2. ProgSnap2 é o padrão da área de EDM para programação. Outros formatos (Moodle, Canvas, CodeHS) são todos diferentes entre si — construir adaptadores seria um trabalho separado.

**Sugestão arquitetural:** projetar a camada de ingestão com uma interface abstrata (`DatasetAdapter`), mas só implementar o `ProgSnap2Adapter` agora. Isso deixa a porta aberta sem explodir o escopo.

**Ponto crítico:** datasets reais do professor serão mais sujos que o CSEDM. Precisamos de uma etapa de **validação** que aponte problemas (colunas ausentes, timestamps malformados, SubjectIDs inconsistentes) antes de continuar.

---

### 2. Extração de KCs

A distinção entre "KCs do enunciado" e "KCs das respostas" é conceitualmente importante e mapeia para o que a literatura chama de *intended KCs* vs *demonstrated KCs*.

**Três modos — todos viáveis — apresentados como um pipeline em etapas (abas ou wizard):**

| Modo | Técnica | Custo de API | Qualidade |
|---|---|---|---|
| Do enunciado (intended) | LLM com o texto do problema | Barato (~5–10 chamadas/exercício) | Boa, mas limitada ao que o professor planejou |
| Das respostas (demonstrated) | Pipeline KCGen-KT do notebook 03b | Médio (~50–75 chamadas/assignment) | Melhor — captura o que os alunos realmente demonstram |
| Manual / edição | Interface de edição da Q-matrix | Zero custo de API | Perfeito — professor corrige o que o modelo errou |

A interface deve guiar o professor pelas três etapas em sequência — extrair do enunciado, complementar com o que emergiu do código dos alunos, e revisar o resultado final. As etapas são independentes: o professor pode pular qualquer uma ou usar apenas a edição manual se preferir.

A opção de **edição manual da Q-matrix** é especialmente importante. Ela resolve o problema de confiança: o professor não precisa confiar cegamente no LLM, pode revisar e ajustar. É um loop colaborativo humano-IA sólido para o contexto acadêmico.

> **Ressalva:** o pipeline KCGen-KT usa a API do Claude/OpenAI. Para a ferramenta, o professor precisaria de uma chave de API própria ou a instituição precisaria hospedar o serviço com uma chave compartilhada. Vale definir essa política antes de começar a construir.

---

### 3. Dashboard de EDA

**EDA automatizada vs. EDA predefinida**

A EDA totalmente automatizada (decidir dinamicamente quais gráficos mostrar) é um problema de pesquisa por si só. Ferramentas como `ydata-profiling` geram relatórios automáticos, mas produzem dezenas de gráficos genéricos — a maioria sem valor para um professor de programação.

**Recomendação: EDA predefinida e curada.** O notebook 01 já nos mostrou exatamente o que é relevante para esse domínio:

1. Taxa de acerto por assignment
2. Distribuição de tentativas por estudante
3. Taxa de Compile.Error
4. Curvas de aprendizado por assignment
5. Clustering de estudantes (alto desempenho / médio / risco)
6. Taxas de mastery por KC
7. Distribuição de Score (trimodal)

Construir esses gráficos como visualizações interativas (Plotly/Altair) com filtros por turma, assignment ou período já entrega enorme valor sem a complexidade da EDA dinâmica.

---

### 3.5. Agente Interpretador sobre a EDA

**Viável e valioso.** O padrão seria:

```
[Dados estruturados da EDA] → [Prompt com contexto] → [LLM] → [Insight em linguagem natural]
```

Exemplo: o sistema calcula que a turma tem 54% de alunos com menos de 5 tentativas por exercício. Injeta esse dado no prompt com o contexto da disciplina e pede ao LLM para interpretar → "Mais da metade da turma está enviando poucas tentativas — isso pode indicar desengajamento ou que os exercícios estão calibrados aquém do nível real da turma."

**Diferença crucial:** o LLM só recebe dados reais calculados pelo sistema, não tem acesso a informações genéricas. Isso reduz drasticamente o risco de alucinação e mantém as respostas ancoradas na turma real do professor.

---

### 4. Porcentagem de Aprendizado por KC

**O coração da ferramenta — e o diferencial real em relação a abordagens puramente estatísticas.**

**O modelo principal é o Code-DKT.** A análise das submissões de código (AST paths via srcML, atenção sobre embeddings) é o que distingue essa ferramenta de um dashboard genérico. Os outros modelos ficam disponíveis como opções secundárias para comparação ou como fallback caso o professor não forneça código-fonte.

O Code-DKT não entrega mastery diretamente — entrega P(próximo acerto). A tradução para a interface do professor se dá por uma proxy interpretável: se P(acerto) > limiar por N tentativas consecutivas, o aluno é considerado como tendo demonstrado domínio do KC. Simples, defensável, e adequado para comunicação com docentes.

Para o professor, as saídas se traduzem em:

- **Heatmap de mastery** por (aluno × KC) ao final do assignment
- **KCs críticos**: aqueles com menor mastery médio da turma — ordenados por urgência
- **Alunos em atenção**: aqueles com mastery baixo em múltiplos KCs críticos

**Sobre BKT e DKT como opções secundárias:** o BKT tem o benefício de parâmetros explicitamente interpretáveis (`P(learn)`, `P(guess)`, `P(slip)`) que podem ser exibidos como contexto adicional para o professor, enquanto o DKT serve como comparação de desempenho. Ambos podem ser selecionáveis na interface, mas o Code-DKT é o padrão.

> **O que NÃO é viável:** calcular mastery em tempo real durante a aula (requer pipeline de streaming). O fluxo do TCC 2 seria: professor carrega o dataset ao final do assignment → sistema roda o modelo → gera o relatório.

---

### 5. Sugestão de Exercícios

A funcionalidade opera em dois sentidos complementares, ambos viáveis para o TCC 2:

**Sentido direto — sugestão de temas:** dados os KCs com baixo mastery na turma, o sistema apresenta uma sugestão genérica orientada ao professor:

> "Procure exercícios ou listas que abordem: *casting e conversão de tipos, expressões booleanas com múltiplos operadores, e uso de métodos com retorno não-void*."

Essa recomendação é gerada a partir dos KCs críticos identificados pelo modelo, sem exigir que o professor tenha uma base de exercícios pré-carregada. Simples, direto, e acionável.

**Sentido reverso — análise de cobertura (reverse lookup):** o professor cola o enunciado de um exercício (ou de uma lista inteira) e o sistema responde quais KCs do assignment aquele material cobre — e, principalmente, quais KCs críticos *não* são endereçados. Isso permite ao professor avaliar se uma atividade encontrada vai de fato suprir as lacunas da turma antes de aplicá-la.

Ambas as funcionalidades reutilizam o pipeline KCGen-KT (extração via LLM) e a Q-matrix já construída.

> **Geração de novos exercícios via LLM** (criar enunciados do zero) fica como trabalho futuro — o risco de qualidade é alto demais para uso acadêmico sem revisão humana sistemática.

---

### 6. Assistente IA (Chat)

**Funcionalidade auxiliar — não é o foco da ferramenta.** Posicionada de forma isolada na interface, como um recurso de suporte: *"Dúvidas sobre os dados ou sobre a análise? Converse com nosso assistente."*

O design correto é um assistente ancorado nos dados reais da sessão (RAG), não um chatbot genérico:

```
Contexto injetado: {EDA resumida, KC mastery por aluno, KCs críticos, histórico da conversa}
Pergunta do professor: "Por que o KC 'loops aninhados' está com aprendizado tão baixo?"
Resposta: baseada nos dados reais carregados, não em generalização
```

O fato de estar ancorado nos dados reais é o que dá utilidade real — um LLM sem esse contexto seria apenas um chatbot sobre educação genérico. Para turmas grandes, os dados precisam ser sumarizados antes de injetar no contexto (limite de tokens).

**Implementação:** chamada à API do Claude com system prompt contendo os dados da sessão. Não requer infraestrutura adicional além do que já existe para o agente interpretador da EDA.

---

## O que NÃO é Viável para o TCC 2

| Ideia | Por quê não |
|---|---|
| Outros formatos além de ProgSnap2 | Escopo de engenharia explode; cada formato é diferente |
| EDA totalmente automatizada | É um problema de pesquisa separado, não de engenharia |
| Geração de exercícios sem revisão humana | Risco de qualidade alto para contexto acadêmico |
| Deploy para produção (auth, multi-tenancy) | Fora do escopo de um TCC |
| Suporte a disciplinas não-programação | Pipeline de features (srcML, ASTs Java) é especializado |
| Streaming em tempo real | Arquitetura completamente diferente, requer infraestrutura |

---

## Stack Recomendada

Para um TCC 2 com timeline acadêmico, o caminho mais direto é:

**[Streamlit](https://streamlit.io/)** como frontend. É Python puro, os gráficos do notebook 01 viram Plotly interativos com poucas linhas, e todo o backend já está em Python. Alternativamente, **Gradio** se o foco for mais em demonstração do que em dashboard completo.

FastAPI + React seria mais profissional, mas dobraria o tempo de desenvolvimento sem agregar à pesquisa.

### Estrutura Proposta

```
tcc2.edm.kt/
├── app/
│   ├── pages/
│   │   ├── 01_upload.py           # Dataset + validação ProgSnap2
│   │   ├── 02_kc_manager.py       # Pipeline: enunciado → respostas → revisão manual
│   │   ├── 03_eda.py              # Dashboard EDA predefinido + interpretador LLM
│   │   ├── 04_kt_results.py       # Mastery Code-DKT por KC/aluno + KCs críticos
│   │   ├── 05_recommendations.py  # Sugestão de temas + análise reversa de exercícios
│   │   └── 06_chat.py             # Assistente IA (área isolada, RAG)
│   └── main.py
├── src/                           # Reaproveitado do TCC 1
│   ├── data_loader.py             # Estender para validação genérica ProgSnap2
│   ├── kc_generator.py            # Notebook 03b → módulo reutilizável
│   ├── models/
│   │   ├── code_dkt.py            # Modelo principal (Code-DKT / srcML-DKT)
│   │   ├── dkt.py                 # Modelo secundário
│   │   └── bkt.py                 # Modelo secundário (já pronto)
│   ├── analytics.py               # Funções EDA do notebook 01
│   └── chat.py                    # Integração com API LLM (EDA interpreter + chat)
└── ...
```

O TCC 1 já entrega `data_loader.py`, `models/bkt.py` e o pipeline KCGen-KT (notebook 03b → `kc_generator.py`). O TCC 2 constrói sobre fundações que já existem, sendo o `code_dkt.py` o principal módulo novo a ser integrado.

---

## Priorização

| Funcionalidade | Viabilidade TCC 2 | Prioridade |
|---|---|---|
| Ingestão ProgSnap2 com validação | Alta | Core |
| Pipeline de KCs em 3 etapas (wizard/abas) | Alta | Core |
| — KC do enunciado (LLM) | Alta | Core |
| — KC das respostas (KCGen-KT) | Alta | Core |
| — Edição/revisão manual da Q-matrix | Alta | Core |
| Dashboard EDA predefinida (Plotly) | Alta | Core |
| Agente interpretador LLM sobre EDA | Alta | Core |
| Mastery por KC/aluno — **Code-DKT (primário)** | Alta | Core |
| KCs críticos da turma | Alta | Core |
| Alunos em atenção (risco por KC) | Alta | Core |
| Sugestão genérica de temas por KC crítico | Alta | Importante |
| Análise reversa (enunciado → KCs cobertos) | Alta | Importante |
| Seletor de modelo (DKT / BKT como secundários) | Média | Importante |
| Assistente IA (chat RAG, área isolada) | Média | Secundário |
| Geração de novos exercícios via LLM | Baixa | Trabalho futuro |
| Outros formatos além de ProgSnap2 | Baixa | Trabalho futuro |

---

## Próximos Passos

1. **Terminar TCC 1** — DKT, Code-DKT, comparação final — para definir o modelo vencedor (motor do TCC 2)
2. **Definir política de API keys** — chave do professor, institucional, ou LLM local (Ollama)?
3. **Prototipar o módulo de upload + validação** — base para tudo mais
4. **Converter notebook 03b em módulo `kc_generator.py`** — reuso direto no TCC 2
