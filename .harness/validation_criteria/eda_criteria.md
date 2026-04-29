# Critérios de Validação — 01_eda.ipynb

Este documento define os critérios de pesquisa para validação independente do notebook de
Análise Exploratória de Dados. Os critérios são escritos em termos de **objetivos de pesquisa**,
não de passos de implementação. O validador avalia o notebook como um revisor externo avaliaria
um artigo — contra os objetivos do projeto e os fatos dos papers.

---

## 1. Dados e Qualidade

**1.1 Taxa de corretos em Release/Train**
O notebook calcula a taxa de acertos diretamente dos dados do split Release/Train e reporta o
valor numérico? Se o valor calculado divergir de 23.70% (Shi et al., 2022), o markdown explica
a divergência (filtro diferente, definição de "correto", arredondamento)? Uma divergência
explicada é aceitável; uma divergência não explicada é um problema crítico.

**1.2 Duplicate rows explicadas**
O notebook identifica os registros com mesmo (SubjectID, ProblemID, ServerTimestamp)? A hipótese
de que cada evento Run.Program gera um evento filho Compile com o mesmo timestamp é enunciada
explicitamente? O notebook não remove essas duplicatas sem justificativa?

**1.3 Cobertura de CodeStateID**
O notebook verifica ou menciona que todos os eventos têm CodeStateID disponível? (Cobertura
esperada: 100%.)

---

## 2. Compile.Error e Decisão do srcML

**2.1 Proporção de Compile.Error quantificada**
O notebook calcula a proporção de eventos Compile.Error sobre o total? O valor esperado é ~30%.
O achado é conectado à decisão de usar srcML-DKT (Pankiewicz et al., 2025)?

**2.2 Motivação para srcML documentada**
O markdown explica por que os eventos Compile.Error são relevantes para o Code-DKT mas não para
BKT e DKT padrão? A explicação cita ou referencia Pankiewicz et al. (2025)?

---

## 3. Estrutura de Assignments e Dificuldade

**3.1 Taxa de acerto por problema calculada e visualizada**
O notebook calcula a taxa de acerto por problema por assignment a partir dos dados? Um plot ou
tabela é apresentado? Um ranking de dificuldade é discutido?

**3.2 Variabilidade entre assignments mencionada**
A análise menciona ou verifica se há diferenças de tamanho de dataset entre assignments
(número de estudantes, número de submissões)?

---

## 4. Curvas de Aprendizado

**4.1 Learning curves presentes e discutidas**
O notebook plota curvas de aprendizado por assignment (taxa de acerto ao longo das tentativas)?
Os achados são reportados independentemente da direção da tendência (melhora, piora, estagnação)?
O markdown comenta o que a curva indica para o modelo?

---

## 5. Score e Desbalanceamento

**5.1 Análise de Score a partir dos dados**
O notebook calcula e visualiza a distribuição do Score a partir dos dados brutos (não hardcoded)?
A proporção de scores parciais (0 < Score < 1) é calculada e reportada?

**5.2 Imbalance ratio e justificativa de AUC**
O imbalance ratio (proporção de acertos vs erros) é calculado por assignment a partir dos dados?
A escolha de AUC como métrica principal é justificada com base no imbalance observado?

---

## 6. Rastreabilidade Metodológica

**6.1 SEED fixo**
Qualquer operação com componente aleatório (clustering, splits, amostragem) usa SEED=42 de
forma explícita no código (não apenas mencionado no markdown)?

**6.2 Split correto**
O notebook usa o split Release/ (não All/) para cálculos que serão comparados com o paper de
Shi et al. (2022)? A distinção entre os dois splits é documentada?

**6.3 Ausência de estatísticas hardcoded**
Os valores numéricos reportados nos markdowns são calculados das células de código imediatamente
anteriores, não digitados manualmente? (Verificar se há f-strings ou variáveis referenciando
resultados calculados, em vez de strings com números fixos.)
