# LogComp
#### Repositório para a disciplina de Lógica da Computação  

###### Guilherme Leite

###### Diagrama Sintático


![Image of DS](./DS.jpg)

###### EBNF

    BLOCK = "{", { COMMAND }, "}" ;
    COMMAND = ( λ | ASSIGNMENT | WHILE | IF | PRINT), ";" | BLOCK ;
    ASSIGNMENT = IDENTIFIER, "=", EXPRESSION, ";" ;
    PRINT = "echo", EXPRESSION, ";" ;
    WHILE = "while","(", RelEXPRESSION, ")"| BLOCK ;
    IF = "if","(", RelEXPRESSION, ")"| BLOCK ,  ( λ |  ( "else" |BLOCK));
    RelEXPRESSION = EXPRESSION, { ("==" | "<" | ">"), EXPRESSION } ;
    EXPRESSION = TERM, { ("+" | "-" | "or"), TERM } ;
    TERM = FACTOR, { ("*" | "/" | "and"), FACTOR } ;
    FACTOR = (("+" | "-" | "not"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
    IDENTIFIER = "$", LETTER, { LETTER | DIGIT | "_" } ;
    NUMBER = DIGIT, { DIGIT } ;
    LETTER = ( a | ... | z | A | ... | Z ) ;
    DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
