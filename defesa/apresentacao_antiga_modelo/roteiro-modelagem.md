# Roteiro de defesa — Modelagem + Ferramenta

> Tempo estimado: ~4 minutos. Voz: estudante de engenharia de computação.
> Split: modelo ~3 min, ferramenta ~1 min.
> Marcações `[SLIDE: ...]` indicam o slide ativo; o orador avança enquanto fala.

---

## PARTE 1 — O MODELO (~3 min)

### [SLIDE: conhecimento como componentes] (~40s)

Antes do modelo, vale explicar o que são os KCs, porque eles são a unidade central de todo o trabalho. Um *knowledge component* é a menor peça de conhecimento que o estudante precisa dominar para resolver um problema. Dá para pensar nele como uma "habilidade" ou um "conceito": por exemplo, usar um laço `for`, montar uma condição composta, ou percorrer um vetor. O *knowledge tracing* acompanha, tentativa após tentativa, o quão bem o estudante domina cada um desses componentes. Essa ideia vem de Corbett e Anderson, em 1995, num tutor inteligente de programação.

Um ponto importante é que a forma como definimos o KC muda o quanto conseguimos diagnosticar: um KC muito grosso, como "o problema inteiro", diz pouco sobre o que o estudante sabe; um KC fino, como "condição composta", diz exatamente onde reforçar. No treino dos modelos, seguindo Shi e colegas, usamos o próprio problema como KC: cada problema do CSEDM é um KC, e treinamos um modelo por *assignment*.

### [SLIDE: o modelo escolhido] (~20s)

O modelo que escolhemos foi o Code-DKT, de 2022. A diferença dele para os anteriores, o BKT, que é bayesiano, e o DKT, que é uma rede neural, é que esses dois só enxergam se o estudante acertou ou errou. O Code-DKT **lê o código**.

### [SLIDE: dentro do code-dkt → o que o code-dkt olha] (~35s)

Por baixo, ele extrai a árvore sintática do código, transforma os caminhos dessa árvore em vetores, pondera com um mecanismo de atenção e passa para uma LSTM. Na prática, ele aprende a olhar para a parte do código que importa. Nesta submissão incorreta, de um problema de condições compostas, o token que recebeu mais atenção foi justamente o operador "e" lógico, o `&&`. O modelo foca no construto que define o conceito, e é isso que torna o diagnóstico interpretável.

### [SLIDE: code-dkt no csedm — Tabela 2] (~40s)

Comparando os três modelos no CSEDM, com média de 10 execuções e usando *first-attempt* AUC, que é a métrica que evita o viés das múltiplas tentativas, o Code-DKT supera o DKT em quatro dos cinco *assignments*, e os dois ficam bem acima do BKT. No A439, nosso resultado fica dentro da margem do que o Shi reporta no artigo, o que dá confiança de que a réplica está correta.

### [SLIDE: extração de KCs → retomando o problema (Martins) → kcs semânticos extraídos] (~45s)

Só que o ProblemID é opaco: dizer que o estudante vai mal no "problema 47" não ajuda o professor. Então automatizamos a extração de KCs semânticos a partir das submissões, num *pipeline* de cinco etapas baseado no Duan. E aqui retomamos o problema: o Martins mostra que a maior dificuldade dos estudantes são os conceitos técnicos, e dentro deles, as estruturas de controle. Os KCs que extraímos cobrem exatamente essas dificuldades: condicionais, laços, expressões lógicas.

### [SLIDE: dificuldade por conceito] (~25s)

Ligando esses KCs às dificuldades do Martins, o Code-DKT estima a dificuldade de cada conceito. As curvas mais baixas são os conceitos mais difíceis, e são justamente estruturas de controle e lógica, batendo com o Martins. E validamos isso: a dificuldade que o modelo prevê concorda com a que de fato se observa nos dados.

---

## PARTE 2 — A FERRAMENTA (~1 min)

### [SLIDE: proposta da aplicação] (~55s)

Todo esse processo nós propomos empacotar numa ferramenta para o professor. O fluxo tem seis etapas: importa os dados no formato ProgSnap2, extrai os KCs automaticamente, o docente valida e ajusta esses conceitos, prepara as sequências de cada estudante, o Code-DKT prediz o estado da turma e de cada um, e um *dashboard* mostra esse estado de aprendizado. Na prática, o professor enxerga onde a turma está travando, por **conceito** e não por problema, e ajusta a aula antes do fim do semestre. Essa é a quarta fase da metodologia, a Implantação, que é o nosso TCC 2.

---

## Notas de execução

- **Tempo:** versão com a explicação ampliada de KC fica em ~4min05. Para voltar a ~3min50, encurtar o bloco "dentro do code-dkt" juntando o *pipeline* numa frase só (árvore sintática → vetores → atenção → LSTM).
- **Tabela 2:** a fala usa "4 de 5" e "acima do BKT" para caber no tempo; os valores por modelo estão no slide se a banca quiser detalhar.
- **Gancho de interpretabilidade:** a atenção no `&&` tem fala própria porque conecta o modelo à ferramenta.
- **Validação ρ=0,725:** mencionada como "concorda com o observado", sem o número, para não pesar.
