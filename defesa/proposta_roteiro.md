# Roteiro da defesa do TCC 2

> Tempo-alvo: cerca de 18 min de fala (limite de 20 min, sem perguntas no tempo).
> Fonte de todo número e afirmação: o documento final do TCC. A referência entre
> colchetes (`doc: Tabela 3`) indica de onde o conteúdo saiu e não aparece no slide.
> Marcações `[SLIDE N: cabeçalho]` indicam o slide ativo. "Na tela" é o que o slide mostra,
> "Fala" é o que o orador diz.

## Divisão por apresentador

Três blocos contíguos, uma passagem de bastão entre cada um (sem vai e volta de orador).

| Apresentador | Papel no trabalho | O que apresenta | Slides | Alvo | Limite |
|---|---|---|---|---|---|
| **Erick** | coordenação / introdução | Abertura, Introdução e Fundamentação teórica (o "porquê" e a base teórica) | 0 a 12 | 5:50 | 6:15 |
| **Victor** | metodologia e modelo | Metodologia, Desenvolvimento da ferramenta e os resultados do modelo | 13 a 25 | 6:30 | 7:00 |
| **Leonardo** | construção da ferramenta | Resultados dos conceitos, demonstração ao vivo e Considerações finais | 26 a 34 | 6:00 | 6:45 |
| **Total** | | 35 slides | | **~18:20** | **< 20:00** |

Por que o Leonardo fica com os conceitos, a demonstração e o fecho: como ele construiu a
ferramenta, é quem mais domina a extração de conceitos e a tela de análise, conduz a
demonstração ao vivo com segurança e assina a contribuição do trabalho no fecho — tudo isso é
"outra parte", e não o capítulo de Desenvolvimento, que o Victor apresenta. O Leonardo continua
sendo o respondente natural para perguntas técnicas de implementação, e ele e o Victor podem
trocar o capítulo 4 entre si se o Victor não se sentir à vontade com a arquitetura.

> Passagens de bastão: slide 12 → 13 (Erick → Victor) e slide 25 → 26 (Victor → Leonardo).
> Na troca, uma frase curta: "agora o [nome] segue com...".

## Tempo por capítulo

| Bloco | Slides | Apresentador | Tempo |
|---|---|---|---|
| Abertura, capa, agenda | 0 a 2 | Erick | 0:30 |
| 1 Introdução | 3 a 6 | Erick | 2:00 |
| 2 Fundamentação teórica | 7 a 12 | Erick | 3:30 |
| 3 Metodologia | 13 a 17 | Victor | 2:15 |
| 4 Desenvolvimento da ferramenta | 18 a 23 | Victor | 3:00 |
| 5 Resultados — modelo | 24 a 25 | Victor | 1:30 |
| 5 Resultados — conceitos | 26 a 28 | Leonardo | 2:10 |
| 5 Resultados — demonstração | 29 | Leonardo | 1:30 |
| 5 Resultados — síntese | 30 | Leonardo | 0:35 |
| 6 Considerações finais | 31 a 34 | Leonardo | 1:30 |
| **Total** | 35 slides | | **~18:20** |

Ordem do capítulo 4 ajustada para evitar vai e volta: a reprodutibilidade (MLOps) foi para o
fim do capítulo (slide 23), depois dos mecanismos (Code-DKT, conceitos e domínio), em vez de
interromper a sequência logo após a arquitetura.

Numeração das figuras, tabelas e quadros: sequencial dentro da apresentação, como no deck
anterior, e não a do documento.

---

## ABERTURA (0:30)

> **Apresenta: Erick** — da abertura até o fim da Fundamentação teórica (slides 0 a 12).

### [SLIDE 0: abertura] (0s)

**Na tela:** logo UniFacens, tagline `> educational data mining e knowledge tracing`.

**Fala:** nenhuma, o slide já está aberto quando a banca chega.

### [SLIDE 1: capa] (~15s)

**Na tela:** título, os três autores, orientadora.

**Fala:** Boa noite. Nós somos Erick Miranda Viana, Leonardo Kuntz Oliveira e Victor Santos
Borba, e vamos apresentar o trabalho "Análise do aprendizado de programação utilizando
mineração de dados educacionais", orientado pela professora mestre Talita Berbel.

### [SLIDE 2: agenda] (~15s)

**Na tela:** Introdução · Fundamentação teórica · Metodologia · Desenvolvimento da ferramenta ·
Resultados · Considerações finais.

**Fala:** A apresentação segue os capítulos do trabalho. Começamos pelo problema, passamos pela
base teórica e pela metodologia, mostramos a ferramenta que desenvolvemos, inclusive
funcionando, e fechamos com os resultados e as considerações finais.

---

## 1 INTRODUÇÃO (2:00)

### [SLIDE 3: introdução] (~35s)

**Na tela:**
- A aprendizagem de programação é uma das etapas que mais impõem dificuldades a estudantes e
  docentes, sobretudo nas disciplinas introdutórias.
- Dificuldades com lógica, abstração e domínio de conceitos técnicos aparecem de forma
  recorrente e podem levar à desmotivação, à reprovação e à evasão (Martins; Marin; Alves, 2024).
- Em nove semestres de um curso de Engenharia de Computação, a reprovação nas disciplinas
  introdutórias de programação ficou entre **18,51%** e **21,98%** (Luz *et al.*, 2026).
- Identificar essas dificuldades **durante** a disciplina permite agir antes que elas virem
  reprovação ou evasão.

**Fala:** O ensino de programação é difícil para os dois lados, para quem aprende e para quem
ensina. Uma revisão sistemática de Martins, Marin e Alves mostra que lógica, abstração e
conceitos técnicos são as dificuldades mais recorrentes, e que elas levam à desmotivação, à
reprovação e à evasão. Luz e colegas olharam nove semestres de um curso de Engenharia de
Computação e encontraram reprovação de cerca de 20% nas disciplinas introdutórias. A pergunta
que nos moveu foi: dá para o professor enxergar essas dificuldades enquanto a disciplina ainda
está acontecendo?

[doc: cap. 1 e seção 2.1]

### [SLIDE 4: o problema do certo ou errado] (~35s)

**Na tela:**
- Classificar cada tentativa apenas como correta ou incorreta ignora que o estudante pode
  dominar **parte** do assunto.
- Um estudante pode usar corretamente uma condicional, um laço ou um vetor e, ainda assim, ter
  a solução marcada como incorreta por um erro localizado (Shi *et al.*, 2022).
- O conteúdo do código acrescenta informação que o resultado final não mostra.
- Mesmo usando o código, os modelos não dizem **quais conceitos** o estudante domina, e é isso
  que o docente precisa saber.

**Fala:** Em programação, a nota da tentativa conta pouco da história. Duas tentativas erradas
podem mostrar níveis de conhecimento bem diferentes: um aluno pode ter acertado a condicional e
o laço e errado só um detalhe. Shi e colegas mostram que o código traz informação que o certo ou
errado descarta. Só que tem um segundo problema: mesmo um modelo que lê o código devolve
números por exercício, e o professor quer saber em qual conceito a turma está travando.

[doc: cap. 1, seções 2.1 e 2.5.4]

### [SLIDE 5: problema de pesquisa] (~25s)

**Na tela (texto centralizado, como o slide "o problema" do deck anterior):**

O uso do código submetido, do histórico de tentativas e de componentes de conhecimento
interpretáveis permite acompanhar a aprendizagem em programação com mais detalhes do que uma
análise baseada apenas em acertos e erros?

*Hipótese:* a combinação dessas técnicas representa a aprendizagem de forma mais detalhada e
relaciona as estimativas a conceitos que o docente consegue interpretar.

**Fala:** Nosso problema de pesquisa junta esses dois pontos. A hipótese é que, combinando o
código, o histórico de tentativas e conceitos interpretáveis, a gente consegue acompanhar a
aprendizagem com mais detalhe do que olhando só acerto e erro. Na revisão de literatura, não
encontramos estudos que apliquem essas técnicas em conjunto no contexto brasileiro.

[doc: cap. 1]

### [SLIDE 6: objetivos] (~25s)

**Na tela:**

**Objetivo geral:** identificar padrões de aprendizagem em programação pela mineração dos
códigos submetidos, apontando pontos fortes e fracos por conceito.

**Objetivos específicos:**
1. Comparar BKT, DKT e Code-DKT na base CSEDM e selecionar o modelo pela AUC.
2. Extrair automaticamente, com um grande modelo de linguagem, componentes de conhecimento
   interpretáveis das soluções corretas dos estudantes.
3. Desenvolver uma ferramenta web que apresente ao docente o domínio estimado por conceito.
4. Verificar a ferramenta com os dados da base CSEDM.

**Fala:** O objetivo geral é identificar pontos fortes e fracos na aprendizagem, por conceito,
a partir dos códigos dos alunos. Para isso, definimos quatro objetivos específicos: escolher o
modelo, extrair os conceitos, construir a ferramenta e verificá-la. São esses quatro que vamos
retomar nos resultados.

[doc: cap. 1]

---

## 2 FUNDAMENTAÇÃO TEÓRICA (3:30)

### [SLIDE 7: mineração de dados educacionais] (~35s)

**Na tela (texto à esquerda, figura à direita):**
- A mineração de dados educacionais (*educational data mining*, EDM) aplica técnicas de análise
  de dados e aprendizado de máquina aos dados gerados por estudantes (Kalita *et al.*, 2025).
- Cada interação do estudante, como uma submissão de código, um erro ou uma nova tentativa,
  vira dado sobre o processo de aprendizagem.
- A análise de aprendizagem (*learning analytics*, LA) mede, coleta e analisa esses dados para
  compreender e otimizar a aprendizagem (Long; Siemens, 2011).

**Figura 1** – Áreas relacionadas à EDM e à LA

![Figura 1](assets/figuras/fig01-edm-la-areas.png)

Fonte: adaptado de Srinivasa e Kurni (2021). [doc: Figura 1]

**Fala:** A mineração de dados educacionais fica na interseção entre computação, educação e
estatística, como mostra a figura. A ideia é que cada interação do aluno, cada submissão, cada
erro, cada nova tentativa, é um dado sobre como ele está aprendendo. Junto dela está a
*learning analytics*, que usa esses dados para entender e melhorar a aprendizagem. Em
programação, esse dado é especialmente rico, porque cada tentativa gera um código novo.

[doc: seções 2.3 e 2.4]

### [SLIDE 8: knowledge tracing] (~35s)

**Na tela:**
- O rastreamento do conhecimento (*knowledge tracing*, KT) usa o histórico de questões e
  respostas para estimar o conhecimento do estudante e prever seu desempenho na próxima
  interação (Abdelrahman; Wang; Nunes, 2023).
- O conhecimento acompanhado é dividido em componentes de conhecimento (*knowledge components*,
  KCs), conceitos ou habilidades usados na resolução, como condicionais, laços ou vetores.
- Os modelos são avaliados pela **AUC**, a área sob a curva ROC: 0,5 equivale ao acaso e 1 a
  uma previsão perfeita. Ela não depende de um limiar e se adequa a bases desbalanceadas.
- A **AUC de primeira tentativa** considera só a primeira tentativa de cada estudante em cada
  problema.

**Fala:** Dentro da EDM, nosso foco é o *knowledge tracing*: a partir do histórico de tentativas,
o modelo estima se o aluno vai acertar a próxima. O que ele acompanha são os componentes de
conhecimento, ou KCs, que são os conceitos que o problema exige. Para medir o modelo usamos a
AUC, em que 0,5 é chutar e 1 é acertar sempre. Ela funciona bem quando há muito mais erro do que
acerto, que é o nosso caso. E olhamos em especial a primeira tentativa em cada problema, quando
o modelo ainda não viu o aluno naquele exercício.

[doc: seções 2.5 e 2.5.1]

### [SLIDE 9: bkt, dkt e code-dkt] (~30s)

**Na tela:** linha do tempo do *knowledge tracing* (reaproveitada do deck anterior).
- **1995 · Corbett e Anderson.** BKT, probabilidade de domínio por KC, com conhecimento inicial,
  aprendizagem, acerto ao acaso e deslize.
- **2015 · Piech *et al.*** DKT, rede LSTM sobre o histórico de acertos e erros.
- **2022 · Shi *et al.*** Code-DKT, o DKT com o código de cada tentativa.

**Fala:** Comparamos três modelos que marcam a evolução da área. O BKT, de 1995, é
probabilístico: estima a chance de o aluno dominar cada KC com quatro parâmetros, entre eles a
chance de acertar no chute e de errar por descuido. O DKT, de 2015, troca isso por uma rede
neural recorrente, a LSTM, que aprende com a sequência de acertos e erros. E o Code-DKT, de
2022, mantém o DKT e acrescenta o código.

[doc: seções 2.5.2 a 2.5.4]

### [SLIDE 10: dentro do code-dkt] (~40s)

**Na tela:**
- A cada tentativa, o código Java passa pelo *parser* javalang e vira uma árvore de sintaxe
  abstrata (*abstract syntax tree*, AST).
- Comparar o código como texto daria peso a diferenças que não mudam a estrutura da solução,
  como nomes de variáveis, comentários e formatação. A AST organiza o programa em hierarquia.
- Os caminhos entre pares de folhas viram vetores, como no code2vec (Alon *et al.*, 2019): nó
  inicial, caminho e nó final.
- A atenção pondera os caminhos, e o vetor do código entra na LSTM junto com o acerto ou erro.
- Duas tentativas incorretas com códigos diferentes passam a ter representações diferentes.
- Na base CSEDM, o Code-DKT superou o DKT em cerca de 3 a 4 pontos percentuais de AUC, com menor
  variação (Shi *et al.*, 2022).

**Fala:** Por dentro, o Code-DKT precisa transformar o código em algo que a rede entenda. Tratar
o código como texto não funciona, porque trocar o nome de uma variável mudaria tudo sem mudar a
lógica. Então cada tentativa passa por um *parser* de Java e vira uma árvore de sintaxe
abstrata. Dessa árvore saem caminhos de uma folha a outra, que viram vetores, e a atenção dá
mais peso aos caminhos que mais importam. O resultado é um vetor do código, que entra na LSTM
junto com o acerto ou erro. No artigo original, isso rendeu de três a quatro pontos de AUC sobre
o DKT, com menos variação.

[doc: seções 2.4 e 2.5.4]

### [SLIDE 11: dentro do code-dkt (figura)] (~25s)

**Na tela:**

**Figura 2** – Exemplo de árvore de sintaxe abstrata para um trecho de código

![Figura 2](assets/figuras/fig04-ast.png)

Fonte: adaptado de Shi *et al.* (2022). [doc: Figura 4]

**Fala:** Aqui está um exemplo. O código à esquerda vira esta árvore: o método, a entrada, o
corpo e o que acontece dentro dele. Em vermelho está um dos caminhos, que liga a folha "entrada"
à folha "valor". É esse tipo de caminho que o Code-DKT transforma em vetor. Assim, duas
tentativas erradas, mas com estruturas diferentes, deixam de ser iguais para o modelo.

[doc: seção 2.4]

### [SLIDE 12: extração de kcs com llms] (~35s)

**Na tela:**
- Definir KCs à mão exige especialistas, leva tempo e varia conforme quem classifica.
- Duan *et al.* (2026) usam soluções corretas de estudantes para que um grande modelo de
  linguagem (*large language model*, LLM) gere os KCs de cada problema.
- KCs com nomes diferentes e mesmo significado são agrupados, e o LLM dá um rótulo a cada grupo.
- O resultado é uma **Q-matrix**, que liga cada problema aos KCs que ele exige.

**Quadro 1** – Exemplo de Q-matrix [doc: Quadro 1]

| Problema | Laço de repetição | Estrutura condicional | Operações aritméticas | Manipulação de strings |
|---|---|---|---|---|
| P1: somar os elementos de um vetor | 1 | 0 | 1 | 0 |
| P2: verificar se um número é par | 0 | 1 | 1 | 0 |
| P3: contar as vogais de uma palavra | 1 | 1 | 0 | 1 |

Fonte: elaborado pelos autores (2026).

**Fala:** Falta tornar isso legível para o professor. Definir conceitos à mão é caro e depende de
quem faz. Duan e colegas propõem que um LLM leia soluções corretas dos alunos e diga quais
conceitos cada problema exige. Depois, conceitos parecidos com nomes diferentes são agrupados e
recebem um nome só. O resultado é uma Q-matrix como esta: cada linha é um problema, cada coluna
um conceito, e o 1 diz que aquele problema exige aquele conceito.

[doc: seção 2.6]

---

## 3 METODOLOGIA (2:15)

> **Passa o bastão: Erick → Victor.** O Victor assume aqui e vai até o fim da comparação com
> Shi (slides 13 a 25): Metodologia, Desenvolvimento da ferramenta e os resultados do modelo.

### [SLIDE 13: caracterização da pesquisa] (~30s)

**Na tela:**
- Pesquisa **aplicada**, **quantitativa** e **exploratória**. A etapa analítica é experimental, e
  a ferramenta é um desenvolvimento tecnológico com verificação técnica.
- Seguimos as quatro fases do processo de EDM (Zorić, 2020):

**Figura 3** – Etapas do processo de mineração de dados educacionais

![Figura 3](assets/figuras/fig02-etapas-edm.png)

Fonte: elaborado pelos autores (2026). [doc: Figura 2]

- A preparação dos dados e a modelagem formam a etapa analítica, sobre a base CSEDM. A
  implantação é a ferramenta.

**Fala:** É uma pesquisa aplicada, porque resulta numa ferramenta para um problema concreto,
quantitativa, porque as decisões saem de medidas como a AUC, e exploratória, porque não
encontramos essa combinação aplicada no Brasil. Organizamos o trabalho nas quatro fases do
processo de EDM descritas por Zorić. O problema é o que acabamos de apresentar, a preparação e a
modelagem são a etapa analítica, e a implantação é a ferramenta.

[doc: seções 3.1 e 3.2]

### [SLIDE 14: a base csedm] (~30s)

**Na tela:**
- Submissões de uma disciplina introdutória de programação em Java de uma universidade
  norte-americana, primeiro semestre de 2019 (CSEDM Workshop, 2021).
- Dados públicos e anonimizados, no formato **ProgSnap2** (Price *et al.*, 2020): cada evento traz
  o estudante, a atividade, o problema, o tipo de evento, a pontuação, o horário e o estado do
  código.
- **413** estudantes, **50** problemas, cinco atividades de dez problemas. Só **23,68%** das
  execuções passam em todos os testes.

**Tabela 1** – Atividades da base CSEDM [doc: Tabela 1]

| Atividade | Identificador na base | Problemas | Estudantes |
|---|---|---|---|
| A1 | 439 | 10 | 386 |
| A2 | 487 | 10 | 340 |
| A3 | 492 | 10 | 361 |
| A4 | 494 | 10 | 315 |
| A5 | 502 | 10 | 306 |

Fonte: elaborado pelos autores (2026).

**Fala:** Usamos a base CSEDM, a mesma do Code-DKT. São submissões em Java de 413 alunos, em
cinco atividades de dez problemas. Ela vem no formato ProgSnap2, que registra cada evento do
aluno junto com o código daquele momento, e é isso que permite reconstruir a sequência de
tentativas. Só 23,68% das execuções estão corretas, a mesma proporção do artigo, e esse
desbalanceamento é o motivo de usarmos a AUC.

[doc: seção 3.3]

### [SLIDE 15: preparação dos dados] (~25s)

**Na tela:**
- Cada execução do programa é uma tentativa: rótulo **1** se passa em todos os testes, **0** nos
  demais casos.
- Sequências com mais de 50 tentativas mantêm as 50 mais recentes.
- Estudantes de cada atividade divididos em **80%** treino e **20%** teste, a mesma partição para
  os três modelos.
- Um modelo por atividade, com o próprio problema como KC, como em Shi *et al.* (2022).
- Cada modelo é executado **dez vezes**, com sementes de 42 a 51.

**Fala:** A preparação segue o protocolo de Shi. Cada execução vira uma tentativa, certa ou
errada, e guardamos as últimas 50 de cada aluno. Separamos os alunos em 80% para treino e 20%
para teste, com a mesma partição para todos os modelos. No treino, o KC é o próprio problema,
que é só um identificador. E rodamos cada modelo dez vezes, com sementes diferentes, para medir
também a estabilidade.

[doc: seções 3.3.1 e 3.4]

### [SLIDE 16: extração de kcs semânticos] (~30s)

**Na tela:**

**Figura 4** – Pipeline de extração de componentes de conhecimento via LLM

![Figura 4](assets/figuras/fig05-pipeline-kcs.png)

Fonte: elaborado pelos autores (2026). [doc: Figura 5]

- Cinco soluções corretas **diversas** por problema: o CodeBERT vetoriza as soluções, que são
  agrupadas, e sorteia-se uma de cada grupo.
- O LLM recebe o enunciado e as soluções e devolve os KCs com uma justificativa.
- O Sentence-BERT agrupa os KCs da atividade, e o LLM rotula cada grupo.
- A Q-matrix **não muda o treino**: ela traduz as estimativas por problema em conceitos.

**Fala:** Para os conceitos, seguimos o processo do Duan em cinco etapas. Primeiro escolhemos
cinco soluções corretas bem diferentes entre si para cada problema, para cobrir estratégias
diferentes. O LLM lê o enunciado e essas soluções e diz quais conceitos o problema exige,
justificando cada um. Depois agrupamos conceitos parecidos e montamos a Q-matrix. Um ponto
importante: ela não entra no treino do modelo, ela só traduz o resultado para conceitos.

[doc: seção 3.3.2]

### [SLIDE 17: requisitos e verificação] (~25s)

**Na tela (duas colunas):**

*A ferramenta deve:*
- importar os registros da turma em ProgSnap2;
- extrair os KCs de cada atividade e submetê-los à revisão do docente;
- treinar o modelo selecionado sobre os dados da própria turma;
- apresentar o domínio estimado por estudante e por conceito, ao lado das estatísticas
  observadas.

*Verificação em três frentes:*
1. Code-DKT implementado × valores de Shi *et al.* (2022).
2. KCs da atividade A1 × KCs de Duan *et al.* (2026) e marcações da base, com os trechos de código.
3. Demonstração com os dados da base, da importação à análise.

**Fala:** Os requisitos saem do objetivo e foram apoiados por um questionário com professores
de programação. A ferramenta precisa importar os dados, extrair e revisar os conceitos, treinar
o modelo na turma e mostrar o domínio estimado por conceito. E definimos como verificar: o
modelo contra o artigo do Shi, os conceitos contra o Duan e contra as marcações da própria base,
e a ferramenta funcionando com os dados reais.

[doc: seções 3.5 e 3.6]

---

## 4 DESENVOLVIMENTO DA FERRAMENTA (3:00)

### [SLIDE 18: visão geral da ferramenta] (~25s)

**Na tela:**

**Figura 5** – Fluxo de uso da ferramenta

![Figura 5](assets/figuras/fig06-fluxo-uso.png)

Fonte: elaborado pelos autores (2026). [doc: Figura 6]

- O docente cria a turma, importa o pacote ProgSnap2, revisa e aprova os conceitos, treina o
  modelo e consulta o domínio estimado.
- Antes de gravar, a ferramenta valida o pacote. Atividades sem acertos e erros nas primeiras
  tentativas ficam só para consulta.
- Cada turma guarda suas atividades, conceitos e versões de modelo, e os resultados de turmas
  anteriores continuam disponíveis.

**Fala:** Este é o fluxo do professor na ferramenta. Ele cria a turma e sobe o pacote de dados.
A ferramenta valida o pacote antes de gravar e extrai os conceitos de cada atividade. O professor
revisa e aprova, treina o modelo e consulta o resultado. Cada turma fica registrada
separadamente, então dá para voltar nas turmas anteriores.

[doc: seções 4.1 e 4.2]

### [SLIDE 19: arquitetura] (~30s)

**Na tela:**

**Figura 6** – Visão geral da ferramenta

![Figura 6](assets/figuras/fig07-visao-geral.png)

Fonte: elaborado pelos autores (2026). [doc: Figura 7]

**Fala:** O código tem três partes. Uma biblioteca independente com o Code-DKT, a extração de
conceitos e a AUC, em Python com PyTorch. A aplicação, com FastAPI e SQLite, organizada pelas
mesmas funcionalidades que o professor usa. E a interface em React com TypeScript. A extração
usa o CodeBERT, o Sentence-BERT e o Claude Haiku 4.5. Tudo roda em contêineres Docker, num
servidor local com uma GPU RTX 4050 de 6 GB, e o professor acessa pelo navegador.

[doc: seção 4.1]

### [SLIDE 20: o code-dkt na ferramenta] (~40s)

**Na tela:**

**Figura 7** – O Code-DKT implementado na ferramenta

![Figura 7](assets/figuras/fig13-codedkt-implementado.png)

Fonte: elaborado pelos autores (2026), adaptado de Shi *et al.* (2022). [doc: Figura 13]

- Parâmetros de Shi *et al.* (2022): 100 caminhos por código, LSTM de 128 unidades, 40 épocas,
  lote de 128 estudantes.
- Três adaptações:
  1. gradiente acumulado em duas partes de 64 estudantes, pois o lote não cabe nos 6 GB da GPU;
  2. *dropout* desligado na avaliação, para que a mesma entrada gere a mesma previsão;
  3. sementes fixas e operações determinísticas na GPU.
- Códigos que não viram AST (de 10,3% a 21,4% por atividade) entram só com o problema e o
  resultado.

**Fala:** O Code-DKT da ferramenta segue os parâmetros do Shi, com três adaptações. A primeira é
de memória: o lote de 128 alunos não cabe na nossa GPU de 6 GB, então dividimos em duas partes
de 64 e acumulamos o gradiente, o que dá o mesmo resultado com menos memória. A segunda e a
terceira garantem que o treino e a previsão se repetem. Quando o código do aluno não compila e
não vira árvore, a tentativa entra só com o acerto ou erro. Na A1, o treino leva cerca de um
minuto e meio.

[doc: seção 4.3]

### [SLIDE 21: os conceitos na ferramenta] (~30s)

**Na tela:**
- Segue Duan *et al.* (2026), com o **Claude Haiku 4.5** no lugar do GPT-4o.
- Agrupa os conceitos **por atividade**, para que importar uma atividade nova não altere as que
  já foram revisadas.
- Traduz os conceitos e as justificativas para o português.
- Aponta o **trecho de código** que evidencia cada conceito e confere se ele existe na solução.
- Resultado em **rascunho**: o docente cria, renomeia, exclui e associa conceitos, e o treino só
  é liberado após a aprovação da Q-matrix.

**Fala:** A extração segue o Duan, com duas diferenças principais: usamos o Claude Haiku 4.5 no
lugar do GPT-4o e agrupamos por atividade. Acrescentamos duas coisas para ajudar o professor a
revisar: a tradução para o português e o trecho de código que justifica cada conceito. E o
resultado é sempre um rascunho. O próprio Duan recomenda que um especialista revise os
conceitos, então o treino só começa depois que o professor aprova.

[doc: seção 4.4]

### [SLIDE 22: domínio por conceito] (~30s)

**Na tela:**
- Depois do treino, o Code-DKT dá, para cada estudante, a chance de acertar **cada problema** da
  atividade (Piech *et al.*, 2015).
- Esse valor é o **domínio estimado** do estudante no problema.
- O domínio em um conceito é a **média** do domínio nos problemas associados a ele na Q-matrix.

**Figura 8** – Do domínio por problema ao domínio por conceito (diagrama novo, no estilo das
caixas ABNT do deck: três problemas com seu domínio estimado → um conceito com a média)
Fonte: elaborado pelos autores (2026).

**Fala:** Como o modelo e a Q-matrix se encontram? Ao final do treino, para cada aluno, o
Code-DKT diz qual a chance de ele acertar cada problema da atividade, inclusive os que ainda não
fez. Isso é o domínio estimado por problema. A Q-matrix diz quais problemas exigem cada conceito,
e o domínio no conceito é a média desses problemas. Os conceitos não entram no treino. Eles
reorganizam o resultado numa forma que o professor entende.

[doc: seção 4.5]

> Figura 8 já montada com valores reais da A1 (média da turma, conceito "Uso do tipo de dado
> boolean"): problema 3 (in1To10) 44%, problema 13 (caughtSpeeding) 51%, problema 232
> (alarmClock) 48% → conceito "Uso do tipo de dado boolean" 48%.

### [SLIDE 23: reprodutibilidade] (~25s)

**Na tela:**
- Práticas de operação de sistemas de aprendizado de máquina, ou MLOps (Kreuzberger; Kühl;
  Hirschl, 2023).
- Tarefas pesadas em processos separados, uma por vez, com o estado registrado no banco.
- Cada versão de modelo fica ligada ao **commit** do código e ao **hash** dos dados. A extração
  registra o LLM e a versão do prompt.
- Sementes fixas, versões fixadas do PyTorch e do CUDA, modelos carregados de revisões
  específicas.
- **Dois testes de regressão**: o treino do Code-DKT na A1 com dez sementes e a extração da A1 a
  partir das respostas armazenadas do LLM.

**Fala:** Para fechar o desenvolvimento: como o treino e a extração levam minutos e usam a GPU,
adotamos práticas de MLOps. Cada tarefa pesada roda em um processo separado, uma por vez. Cada
modelo fica ligado ao commit do código e aos dados que o geraram. E, para garantir que o
resultado se repete, fixamos sementes e versões e temos dois testes de regressão que refazem o
treino e a extração da A1.

[doc: seção 4.1]

---

## 5 RESULTADOS (4:15 + 1:30 de demonstração)

### [SLIDE 24: seleção do modelo] (~45s)

**Na tela:** linha do Code-DKT destacada em azul, com média e desvio padrão médio em negrito.

**Tabela 2** – AUC de primeira tentativa por atividade [doc: Tabela 3]

| Atividade | BKT (%) | DKT (%) | Code-DKT (%) |
|---|---|---|---|
| A1 | 62,43 ± 0,00 | 70,74 ± 3,59 | 75,42 ± 1,13 |
| A2 | 62,18 ± 0,78 | 77,33 ± 2,73 | 78,32 ± 0,76 |
| A3 | 59,57 ± 0,60 | 81,43 ± 4,51 | 85,08 ± 0,79 |
| A4 | 53,18 ± 0,26 | 73,07 ± 4,34 | 75,56 ± 0,84 |
| A5 | 59,61 ± 0,49 | 83,13 ± 2,77 | 85,12 ± 0,52 |
| Média | 59,39 | 77,14 | 79,90 |
| Desvio padrão médio | 0,43 | 3,59 | 0,81 |

Fonte: elaborado pelos autores (2026).

- Na AUC geral, o padrão se repete: 63,11% no BKT, 71,79% no DKT e **74,31%** no Code-DKT.

**Fala:** Começando pelo primeiro objetivo, a escolha do modelo. Na primeira tentativa, o
Code-DKT tem a maior AUC nas cinco atividades, com média de 79,90 contra 77,14 do DKT, e o BKT
fica bem atrás, perto de 60. Além de acertar mais, o Code-DKT é mais estável: o desvio padrão
entre as dez execuções é mais de quatro vezes menor que o do DKT. Na AUC geral, sobre todas as
tentativas, o padrão se repete. Como a única diferença entre o DKT e o Code-DKT é o código, isso
indica que o código acrescenta informação. Por isso o Code-DKT é o modelo da ferramenta.

[doc: seção 5.1]

### [SLIDE 25: comparação com shi et al.] (~45s)

**Na tela (duas tabelas lado a lado):**

**Tabela 3** – AUC geral do Code-DKT em comparação com Shi *et al.* (2022) [doc: Tabela 5]

| Atividade | Shi *et al.* (2022) (%) | Este trabalho (%) | Diferença (p.p.) |
|---|---|---|---|
| A1 | 74,31 | 71,42 | −2,89 |
| A2 | 76,56 | 73,53 | −3,03 |
| A3 | 80,40 | 78,21 | −2,19 |
| A4 | 72,75 | 72,17 | −0,58 |
| A5 | 79,14 | 76,24 | −2,90 |
| Média | 76,63 | 74,31 | −2,32 |

Fonte: elaborado pelos autores (2026), com os valores de Shi *et al.* (2022).

**Tabela 4** – AUC do Code-DKT na atividade A1 em comparação com a literatura [doc: Tabela 6]

| Métrica | Shi *et al.* (2022) (%) | Este trabalho (%) | Diferença (p.p.) |
|---|---|---|---|
| AUC geral | 74,31 ± 0,90 | 71,42 ± 0,72 | −2,89 |
| AUC de primeira tentativa | 75,74 ± 0,69 | 75,42 ± 1,13 | −0,32 |

Fonte: elaborado pelos autores (2026), com os valores de Shi *et al.* (2022).

**Fala:** O segundo passo foi conferir se o Code-DKT que implementamos se comporta como o do
artigo. Na AUC geral, ficamos em média 2,32 pontos abaixo do Shi, com diferenças de 0,58 a 3,03
pontos. Mas o artigo só traz a AUC de primeira tentativa para a A1, e nela a diferença cai para
0,32 ponto, com desvio padrão baixo, como no artigo. Ou seja, a implementação reproduz o que
caracteriza o Code-DKT, previsão melhor na primeira tentativa e pouca variação, com valores
absolutos um pouco menores.

[doc: seção 5.2]

> **Passa o bastão: Victor → Leonardo.** O Leonardo assume aqui e fecha a apresentação
> (slides 26 a 34): resultados dos conceitos, demonstração ao vivo e Considerações finais.

### [SLIDE 26: conceitos extraídos na a1] (~40s)

**Na tela (à esquerda, funil em caixas ABNT; à direita, os 13 conceitos):**

**Figura 9** – Resumo da extração na atividade A1 [doc: Tabela 8, desenhada como sequência]
10 problemas → 50 soluções lidas → 65 KCs gerados → 26 nomes distintos → **13 conceitos** → 46
associações problema–conceito · 12 min 41 s
Fonte: elaborado pelos autores (2026).

**Quadro 2** – Conceitos extraídos na atividade A1 [doc: Quadro 3, compacto]

| Conceito | Nº de problemas |
|---|---|
| Estruturas de instrução if-else | 10 |
| Operadores lógicos e condicionais | 10 |
| Comparações numéricas | 9 |
| Operações aritméticas básicas | 5 |
| Uso do tipo de dado boolean | 3 |
| Inicialização e atribuição de variável | 2 |
| Outros sete conceitos | 1 cada |

Fonte: elaborado pelos autores (2026).

**Fala:** Agora os conceitos. Avaliamos a extração na A1, cujos dez problemas tratam de
condicionais. O LLM leu cinco soluções por problema e gerou 65 KCs, que tinham 26 nomes
distintos e foram agrupados em 13 conceitos. É a mesma proporção do Duan, cerca de um conceito
para cada dois nomes. Os dois conceitos que aparecem nos dez problemas são o if-else e os
operadores lógicos, coerente com uma atividade de condicionais. Sete conceitos aparecem em um
único problema, e vamos voltar a isso.

[doc: seção 5.3]

### [SLIDE 27: o problema love6] (~45s)

**Na tela:**

**Quadro 3** – Componentes de conhecimento do problema 233 (love6) [doc: Quadro 4]

*Enunciado:* The number 6 is a truly great number. Given two int values, a and b, return true if
either one is 6. Or if their sum or difference is 6. Note: the function Math.abs(num) computes
the absolute value of a number.

*Solução de estudante:*
```java
public boolean love6(int a, int b) {
  if (a == 6 || b == 6 || a + b == 6 || Math.abs(a - b) == 6)
    return true;
  return false;
}
```

| KCs escritos por humanos | Conceitos extraídos neste trabalho | KCs gerados por Duan *et al.* (2026) |
|---|---|---|
| If/Else | Estruturas de instrução if-else | If and else if statement |
| Math (+ − ∗ /) | Operações aritméticas básicas | Basic arithmetic operations |
| LogicAndNotOr | Operadores lógicos e condicionais | Logical operators |
| LogicCompare | Comparações numéricas | Numerical comparisons |
| — | Invocação de método* | Absolute value computation |

Fonte: elaborado pelos autores (2026).

- No problema 1 (sortaSum), os quatro KCs de Duan *et al.* (2026) têm correspondente.
- Das sete marcações humanas da base na A1, **seis** têm um conceito extraído correspondente. A
  exceção é a formatação de strings.

**Fala:** Para comparar, usamos o mesmo exemplo que o Duan usa no artigo, o problema love6. Na
primeira coluna estão os KCs marcados por humanos na base, na do meio os nossos e na última os
do Duan. Quatro dos cinco conceitos do Duan têm correspondente direto entre os nossos. O quinto,
o valor absoluto, aparece só de forma indireta, como invocação de método, cuja justificativa
cita o Math.abs. No sortaSum, os quatro KCs do Duan também batem. E, contra as marcações humanas
da base, seis de sete têm correspondente.

[doc: seção 5.4]

### [SLIDE 28: trechos de código] (~45s)

**Na tela (duas colunas):**

*À esquerda, associação adequada (problema 1, sortaSum):*
```java
if (a + b >= 10 && a + b <= 19)
    return 20;
else return (a + b);
```
Estruturas de instrução if-else · Operadores lógicos e condicionais · Comparações numéricas.
Os **46** trechos apontados foram encontrados nas soluções.

*À direita:* **Quadro 4** – Exemplos de associações questionáveis [doc: Quadro 7]

| Problema | Conceito | Por quê |
|---|---|---|
| 236 (greenTicket) | Operações aritméticas básicas | só uma solução usa subtração, o problema pede igualdades |
| 233 (love6) | Invocação de método | nome genérico para o valor absoluto |
| 234 (cigarParty) | Métodos básicos de string | conceitos de string que o problema não exige |
| todos, exceto o 5 | Instrução de retorno | toda solução retorna, mas só o 5 recebeu o conceito |

Fonte: elaborado pelos autores (2026).

**Fala:** Para cada associação entre problema e conceito, a ferramenta aponta o trecho de código
que a justifica, e os 46 trechos foram encontrados nas soluções. No sortaSum, por exemplo, a
mesma linha mostra a condicional, o operador lógico e as comparações. Mas a análise também achou
associações questionáveis. No cigarParty, vieram conceitos de string que o problema não
exige. E o retorno ficou associado só a um
problema, apesar de toda solução retornar. É exatamente por isso que os conceitos ficam em
rascunho até o professor aprovar.

[doc: seção 5.5]

### [SLIDE 29: demonstração] (1:30)

**Na tela:** slide de transição com `> demonstração da ferramenta`. Os slides de reserva ficam
numa pilha vertical logo abaixo deste (seta para baixo no reveal), com as telas das Figuras 15
a 23 do documento, para o caso de a rede ou o Tailscale falharem. Seguindo para a direita, a
apresentação pula a pilha.

**Roteiro de cliques** (turma "CSEDM CodeWorkout", já com a A1 treinada; o navegador já aberto
na tela da turma antes da apresentação):

1. **Tela da turma** (~10s). A A1 treinada e as atividades A2 a A5 aguardando a extração.
2. **Conceitos da A1** (~30s). A Q-matrix com os 13 conceitos e os 10 problemas. Abrir a origem
   de "Operadores lógicos e condicionais" no problema 1 (sortaSum): enunciado, justificativa
   traduzida e o trecho destacado na linha 3 da solução 1.
3. **Análise, aba Problemas** (~15s). Abrir o problema 13 (caughtSpeeding), menor taxa de acerto
   (12%) e maior mediana de tentativas (5).
4. **Análise, aba Conceitos** (~15s). Taxa de acerto de 17% a 36% ao lado do domínio médio de 41%
   a 60%, e o alerta dos sete conceitos de um único problema.
5. **Análise, aba Alunos** (~20s). Ordem crescente de domínio. Os primeiros completaram os 10
   problemas e ainda assim têm domínio de 18% a 23%. Abrir o estudante 14339: 56 execuções, 23
   com erro de compilação, menores domínios em boolean e instrução de retorno.

**Telas da pilha de reserva** (Figuras 15 a 23 do documento, na ordem da demonstração):

![Figura 15, importação](assets/telas/fig15-importacao.png)

![Figura 16, turma](assets/telas/fig16-turma.png)

![Figura 17, conceitos](assets/telas/fig17-conceitos.png)

![Figura 18, origem de um conceito](assets/telas/fig18-origem-conceito.png)

![Figura 19, treinamento](assets/telas/fig19-treinamento.png)

![Figura 20, análise por problema](assets/telas/fig20-analise-problemas.png)

![Figura 21, análise por conceito](assets/telas/fig21-analise-conceitos.png)

![Figura 22, análise por estudante](assets/telas/fig22-analise-alunos.png)

![Figura 23, detalhe de um estudante](assets/telas/fig23-detalhe-estudante.png)

**Fala de abertura (antes dos cliques):** Agora vamos mostrar a ferramenta com os dados da
base. A importação e o treino já foram feitos, porque a extração leva cerca de 13 minutos e o
treino um minuto e meio.

**Fala durante a aba Alunos:** Esses alunos completaram tudo e mesmo assim aparecem com domínio
baixo, porque o modelo olha a sequência inteira, incluindo as tentativas erradas até acertar.

[doc: seção 5.6]

### [SLIDE 30: síntese dos resultados] (~35s)

**Na tela:**

**Quadro 5** – Funcionalidades propostas e atendimento pela ferramenta [doc: Quadro 8]

| Nº | Funcionalidade proposta | Onde aparece na ferramenta |
|---|---|---|
| 1 | Visualização dos conceitos que cada estudante domina ou em que tem dificuldade | Abas de conceitos e de estudantes |
| 2 | Histórico detalhado de tentativas por exercício de cada estudante | Execuções, erros de compilação e tentativas por problema |
| 3 | Predição de risco de dificuldade ou reprovação | Domínio estimado baixo por problema, conceito e estudante |
| 4 | Comparação de progresso entre turmas ou semestres | Turmas registradas separadamente, com dados, conceitos e modelos preservados |
| 5 | Sugestão de intervenção pedagógica personalizada | Conceitos de menor domínio da turma e de cada estudante |

Fonte: elaborado pelos autores (2026).

- As funcionalidades 1 e 2 estão implementadas. A 3, a 4 e a 5 são atendidas como **apoio à
  análise**: a ferramenta reúne a informação, e a interpretação é do docente.

**Fala:** Fechando os resultados, este quadro liga as cinco funcionalidades levantadas no
questionário com os professores ao que a ferramenta entrega. A visualização por conceito e o
histórico de tentativas estão implementados. As outras três, risco, comparação entre turmas e
sugestão de intervenção, são atendidas como apoio: a ferramenta mostra os conceitos de menor
domínio, e quem decide o que fazer é o professor.

[doc: seção 5.7]

---

## 6 CONSIDERAÇÕES FINAIS (1:30)

### [SLIDE 31: considerações finais] (~35s)

**Na tela:**
- Na base analisada, os resultados sustentam a hipótese.
- O código melhora a previsão: o Code-DKT obteve 79,90% na primeira tentativa e 74,31% na AUC
  geral, contra 77,14% e 71,79% do DKT, com menor variação.
- Os 13 conceitos da A1 correspondem aos KCs de Duan *et al.* (2026) e às marcações da base, e
  os 46 trechos de código foram encontrados nas soluções.
- **Contribuição:** reunir análise de código, rastreamento do conhecimento e componentes de
  conhecimento em um único fluxo, voltado ao docente.

**Fala:** Voltando à pergunta do início: na base analisada, sim. O código melhorou a previsão
e a estabilidade do modelo, e os conceitos extraídos permitiram mostrar esse resultado numa
forma que o professor interpreta. A principal contribuição é a integração: em vez de usar o
código, o modelo e os conceitos separadamente, a ferramenta junta tudo num fluxo só, e o código
do aluno passa a contar a história de como ele aprendeu, não só se ele acertou.

[doc: cap. 6]

### [SLIDE 32: limitações] (~30s)

**Na tela:**
- Verificada apenas na base CSEDM, de uma universidade norte-americana, em Java.
- A extração foi analisada em detalhe só na A1, cujos problemas tratam de condicionais.
- A diferença de 2,32 pontos para Shi *et al.* (2022) não teve as causas investigadas, e os
  hiperparâmetros não são ajustados para cada turma.
- De 10,3% a 21,4% das execuções não viram AST e entram sem o código.
- O Claude Haiku 4.5 substituiu o GPT-4o sem avaliação de equivalência.
- A ferramenta ainda não foi avaliada por docentes em uso real.

**Fala:** Os resultados têm limites claros. Testamos uma única base, americana e em Java, e
analisamos os conceitos em detalhe em uma atividade. Não investigamos a diferença para o Shi,
trocamos o modelo de linguagem sem comparar com o original e, principalmente, a ferramenta ainda
não foi usada por professores numa turma real. Então não dá para afirmar que o comportamento se
repete em turmas brasileiras.

[doc: cap. 6]

### [SLIDE 33: trabalhos futuros] (~25s)

**Na tela:**
- Aplicar a ferramenta a turmas brasileiras e avaliá-la com os docentes, após aprovação do
  Comitê de Ética em Pesquisa (CEP).
- Ampliar a análise dos conceitos às demais atividades, com avaliação humana por mais de um
  avaliador, e comparar modelos de linguagem.
- Relacionar conceitos entre atividades, para acompanhar um conhecimento ao longo da disciplina.
- Mostrar o código de cada tentativa e comparar turmas em uma tela própria.
- Predição de reprovação com as notas finais e recomendações de intervenção redigidas pela
  ferramenta.

**Fala:** Daí vêm os próximos passos. O principal é levar a ferramenta para turmas brasileiras,
com aprovação do comitê de ética, e avaliar com os próprios professores se a visão por conceito
ajuda a planejar as aulas. Também queremos ampliar a análise para as outras atividades,
acompanhar um mesmo conceito ao longo da disciplina e evoluir a ferramenta com previsão de
reprovação e sugestões de intervenção.

[doc: cap. 6]

### [SLIDE 34: obrigado] (~10s)

**Na tela:** réplica da abertura, tagline `> obrigado`.

**Fala:** Esperamos que o professor consiga identificar e tratar mais cedo as dificuldades da
turma. Muito obrigado.

---

## Notas de execução

- **Onde cortar se passar do tempo (ambos no bloco do Victor):** a reprodutibilidade (slide 23)
  pode virar uma frase dentro da arquitetura (−25s). A segunda tabela do slide 25 pode virar só a
  fala sobre o −0,32 (−10s). O bloco do Victor (13 a 25) é o mais carregado, então ele controla
  os dois cortes.
- **Demonstração (slide 29):** quem conduz é o **Leonardo**, que construiu a ferramenta. Abrir a
  ferramenta numa aba antes de começar e conferir o acesso pelo Tailscale na máquina que vai
  apresentar. Se a ferramenta não abrir, descer na pilha de reserva do slide 29 e narrar as
  mesmas telas.
- **Ensaio:** rodar ponta a ponta com cronômetro, com a demonstração ao vivo, pelo menos duas
  vezes. Meta: fala somada em torno de 17 min, para que a demonstração e as duas passagens de
  bastão caibam com folga nos 20 min.
- **Nomes das atividades:** o slide usa A1 a A5, e a ferramenta mostra "Assignment 439" etc.
  Na demo, vale dizer "a A1, que na base é a 439".
- **Mudanças em relação ao deck anterior:** saem os gráficos de EDA, a Tabela 2 antiga, a
  atenção no `&&`, o "retomando o problema" e a curva de dificuldade, que não estão no documento
  final. O Duan passa a ser citado como 2026, como no documento.

## Perguntas prováveis da banca (para preparar, não vão para os slides)

- **Por que 2,32 pontos abaixo do Shi?** Não foi investigado separadamente (limitação declarada).
  Na primeira tentativa, que é a métrica principal, a diferença é 0,32.
- **Por que o BKT tem desvio padrão 0,00 na A1?** O BKT é ajustado pelo pyBKT sobre as mesmas
  sequências. O documento não discute isso, então a resposta precisa ser combinada antes.
- **Por que o Haiku e não o GPT-4o?** É o modelo acessível no ambiente, e a equivalência não foi
  avaliada (limitação).
- **Por que alunos que completaram tudo têm domínio baixo?** O modelo usa a sequência inteira,
  incluindo as tentativas erradas até acertar.
- **O domínio é uma probabilidade de acerto, não uma nota.** Na ferramenta, um ícone separa o que
  o modelo estima do que foi observado.
