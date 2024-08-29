from infero.lexer import Lexer
from infero.sentences import And, Implication, Not, Or, Sentence, Symbol
from infero.tokens import Token


class Parser:
    def __init__(self, data: str):
        self.scanner: Lexer = Lexer(data)
        self.lookahead: Token = self.scanner.scan()
        self.symtable: dict[str, Sentence] = {}
        self.symhash: dict[str, bool | None] = {}
        self.program: dict[str, list] = {
            "rules": [],
            "facts": [],
            "query": [],
        }

    def start(self):
        self.rules_section()
        self.facts_section()
        self.query_section()
        self.semantic_analysis()

    def semantic_analysis(self):
        for rule in self.program["rules"]:
            if (
                isinstance(rule, And)
                or isinstance(rule, Not)
                or isinstance(rule, Symbol)
            ):
                raise SyntaxError(
                    f"L{self.scanner.line}, regras podem ser apenas implicações ou disjunções"
                )
        for fact in self.program["facts"]:
            symbols = list(fact.symbols())
            if len(symbols) > 1:
                raise SyntaxError(
                    f"L{self.scanner.line}, fatos podem ser apenas átomos ou negações atômicas"
                )
            self.symhash[symbols[0]] = True
            if isinstance(fact, Not):
                self.symhash[symbols[0]] = fact.evaluate(self.symhash)
        query = self.program["query"]
        if len(query) > 1:
            raise SyntaxError(f"L{self.scanner.line}, query deve ser única")

    def match(self, value: str):
        if self.lookahead.value == value:
            self.lookahead = self.scanner.scan()
            return True
        return False

    def rules_section(self):
        """
        <rules_section> ::= "rules:" <stmts> "end"
        """
        if not self.match("rules:"):
            raise SyntaxError(f"L{self.scanner.line}, 'rules:' esperado")
        self.stmts("rules")

    def facts_section(self):
        """
        <facts_section> ::= "facts:" <stmts> "end"
        """
        if not self.match("facts:"):
            raise SyntaxError(f"L{self.scanner.line}, 'facts:' esperado")
        self.stmts("facts")

    def query_section(self):
        """
        <query_section> ::= "query:" <stmts> "end"
        """
        if not self.match("query:"):
            raise SyntaxError(f"L{self.scanner.line}, 'query:' esperado")
        self.stmts("query")

    def stmts(self, kind: str):
        """
        <stmts> ::= <stmt> <stmts>
        <stmt> ::= <expr>
        """
        stmts_list: list = self.program[kind]
        while not self.match("end"):
            expr = self.expr()
            stmts_list.append(expr)

    def expr(self):
        """
        <expr> ::= <term> <imp>
        <imp> ::= "->" <term> | empty
        """
        left = self.term()
        if self.lookahead.value == "->":
            self.match("->")
            right = self.term()
            return Implication(left, right)
        else:
            return left

    def term(self):
        """
        <term> ::= <fact> <binary_op>
        <binary_op> ::= "&" <fact> | "|" <fact> | empty
        """
        left = self.fact()
        while True:
            if self.lookahead.value == "&":
                self.match("&")
                right = self.fact()
                left = And(left, right)
            elif self.lookahead.value == "|":
                self.match("|")
                right = self.fact()
                left = Or(left, right)
            else:
                break
        return left

    def fact(self):
        """
        <fact> ::= "(" <expr> ")" | "~" <fact> | <symbol>
        <symbol> ::= a-zA-Z
        """
        if self.lookahead.value == "(":
            self.match("(")
            expr = self.expr()
            if not self.match(")"):
                raise SyntaxError(f"L{self.scanner.line}, ')' esperado")
            return expr
        else:
            if self.lookahead.value == "~":
                self.match("~")
                operand = self.fact()
                return Not(operand)
            symbol: str = self.lookahead.value
            if not symbol.isalpha():
                raise SyntaxError(
                    f"L{self.scanner.line}, {symbol} simbolos precisam ser letras"
                )
            finded = self.symtable.get(symbol)
            self.lookahead = self.scanner.scan()
            if finded:
                return finded

            self.symtable[symbol] = Symbol(symbol)
            self.symhash[symbol] = None
            return self.symtable[symbol]
