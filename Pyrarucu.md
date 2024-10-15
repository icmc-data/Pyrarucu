# Pyrarucu
A parte do processamento está no arquivo [strategies.py](strategies.py), mais especificamente na classe `Pyrarucu()`.
Todas as mudanças exceto quanto a notebooks devem ser nesse arquivo. Vamos refazer o bot, então é possível que você não encontre as funções descritas aqui no arquivo Python.

Para compreender um pouco melhor como bots de Xadrez funcionam, vamos explicar alguns conceitos:
#### Bitboard
Um bitboard é um array de bits muito comum em jogos de computador, onde cada bit representa uma peça ou um espaço. No nosso caso, o Bitboard é uma ferramenta que ajuda a produzir uma representação vetorial do tabuleiro de Xadrez. 

Existem 12 tipos de peças diferentes no jogo, sendo o peão branco, o bispo branco, ... e o rei preto. Assim, cada peça pode receber sua representação em bitboards, que é um vetor de tamanho 64 (há um espaço para cada casa do tabuleiro) e recebe o valor 1 caso a peça se encontre ali e 0 caso contrário.

![resources/bitboard.gif](resources/bitboard.gif)

Esses vetores, quando empilhados (formando um único vetor de tamanho 12x64) podem ser utilizados para treinar algoritmos de aprendizado de máquina.

#### Função de Análise
A função de análise `def evaluation()` recebe como entrada um tabuleiro de xadrez e retorna um valor que indica a situação atual do jogo. É comum que um valor positivo represente vantagem das brancas e vice-versa.

![resources/evaluation.png](resources/evaluation.png)

A magnitude da função é dada de tal forma que 1 ponto de vantagem é equivalente a um peão de vantagem.

#### Função de Pesquisa
A partir da função de análise, buscaremos encontrar qual lance leva a melhor posição. 

Para isso, podemos criar uma árvore onde cada nó é uma posição com um valor assinalado pela função de análise. A partir da posição atual - o nó raiz da nossa árvore - diferentes lances levam a diferentes posições, que por sua vez podem ser vantajosas ou não.
Considerando que o adversário sempre fará os melhores lances, a função de pesquisa encontra o lance que nos dá a melhor posição independente da resposta do oponente.

#### MinMax 
Uma forma muito comum de encontrar o caminho descrito no tópico anterior é através do algoritmo MinMax.
![Tree with minmax algorithm](resources/minmax.png)

De forma simplificada, o algoritmo encontra o caminho que busca maximizar as posições vantajosas ao mesmo tempo que minimiza as posições com análise ruim.

#### Heurísticas 
As heurísticas desempenham um papel importante na hora de ajudar o programador a encontrar uma solução aproximada para um problema incerto. Para os bots de Xadrez, são bem úteis para diminuir o tempo de pesquisa e normalmente demandam conhecimento do jogo.

Por exemplo, podemos implementar uma heurística que priorize lances de xeque no turno do bot.
Atualmente, é utilizada uma heurística para ordenar os movimentos por importância antes de analisar cada um. Assim, espera-se que haja uma melhora significativa no tempo de raciocínio do Pyrarucu. 

#### Dataset Chess Evaluations
Um dataset é uma base de dados imensa que pode ser utilizada para o treinamento de modelos de aprendizado de máquina. O dataset [Chess Evaluations](https://www.kaggle.com/datasets/ronakbadhe/chess-evaluations) possui milhares de posições no formato [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) acompanhadas de respectivas análises pelo computador [Stockfish](https://stockfishchess.org/).

#### Rede Neural
Na nossa aplicação, atualmente utilizamos uma função de análise baseada em redes neurais que possui a etapa de treinamento com o dataset descrito no tópico passado.

Inicialmente transformamos os tabuleiros em diversos bitboards através da função `fen_to_bit_array()`. Com as representações vetoriais, podemos treinar a nossa rede neural para predizer o resultado esperado de acordo com o dataset.

Sequência de passos para construir os bitboards, treinar a rede neural e efetuar uma predição.
``` python
X = df['FEN'].apply(fen_to_bit_array).to_list()
y = df['Evaluation']
reg = MLPRegressor().fit(X, Y)

reg.predict(X_test)
```

Com o qual obtemos o valor
``` bash
0.07698299
```
