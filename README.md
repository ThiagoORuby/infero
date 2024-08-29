# Infero

Infero é uma ferramenta de inferência lógica que aceita uma linguagem personalizada (.ifo) para definir um conjunto de regras proposicionais, fatos conhecidos, e um objetivo de derivação. O programa utiliza um analisador léxico, sintático e semântico para mapear essas expressões lógicas para uma estrutura de classes em Python, e então aplica regras de inferência como modus ponens, modus tollens, silogismo hipotético e outros, para determinar se o objetivo pode ser derivado, se há contradições ou se o problema é inconclusivo. Infero pode ser utilizado como uma ferramenta educacional para estudos de lógica proposicional, ou como base para sistemas de inferência mais complexos

## Instalação

## Como Usar ?

## BNF da linguagem

```
<program> ::= <rules_section> <facts_section> <query_section>
<rules_section> ::= "rules:" <stmts> "end"
<facts_section> ::= "facts:" <stmts> "end"
<query_section> ::= "query:" <stmts> "end"
<stmts> ::= <stmt> <stmts>
<stmt> ::= <expr>
<expr> ::= <term> <imp>
<imp> ::= "->" <term> | empty
<term> ::= <fact> <binary_op>
<binary_op> ::= "&" <fact> | "|" <fact> | empty
<fact> ::= "(" <expr> ")" | "~" <fact> | <symbol>
<symbol> ::= "a" | "b" | ... | "z" | "A" | ... | "Z"
```
