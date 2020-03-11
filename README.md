# LogComp
#### Repositório para a disciplina de Lógica da Computação  

###### Guilherme Leite

###### Diagrama Sintático


![Image of DS](./DS.jpg)

###### EBNF

    EXPRESSION   : TERM  {("+"|"-")TERM} ;
    TERM         : FACTOR{("*"|"/")FACTOR} ;
    FACTOR       : ("+"|"-") FACTOR | "(" EXPRESSION ")" | number ;
