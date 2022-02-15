from tokenizer import TokenType, Token
from ast__ import BinaryOP, UnaryOP, Num, Command, Assignment, Var
from exceptions__ import SyntaxNotRecognizedError


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.look_ahead = self.tokenizer.next()

    def parse(self):
        return self.program()

    def error(self, error_msg):
        raise SyntaxNotRecognizedError(error_msg)

    def eat(self, token_type: TokenType, error_msg='Invalid expression'):
        if self.look_ahead.type.value == token_type.value:
            self.look_ahead = self.tokenizer.next()
        else:
            self.error(error_msg)

    def program(self):
        """
        <program> ::= <expr>
                    | <command>
                    | <assignment>
        """
        if self.look_ahead.type.value == TokenType.COMMAND.value:
            result = self.command()
        else:
            result = self.expr()
        self.eat(TokenType.EOF)
        return result

    def assignment(self):
        """
        <assignment> ::= IDENTIFIER (EQUALS | <bin_op>) <factor>
        <bin_op> ::= PLUS | MINUS | MUL | DIV
        """
        identifier = self.look_ahead
        self.eat(TokenType.IDENTIFIER)
        if self.look_ahead.type.value in (TokenType.MINUS.value, TokenType.PLUS.value,
                                          TokenType.MUL.value, TokenType.DIV.value):
            op = self.look_ahead
            if self.look_ahead.type.value == TokenType.PLUS.value:
                self.eat(TokenType.PLUS)
            elif self.look_ahead.type.value == TokenType.MINUS.value:
                self.eat(TokenType.MINUS)
            elif self.look_ahead.type.value == TokenType.MUL.value:
                self.eat(TokenType.MUL)
            elif self.look_ahead.type.value == TokenType.DIV.value:
                self.eat(TokenType.DIV)
            return BinaryOP(Var(identifier), op, self.expr())
        elif self.look_ahead.type.value == TokenType.EOF.value:
            return Var(identifier)
        self.eat(TokenType.EQUALS, 'Invalid identifier')
        value = self.factor()
        return Assignment(identifier, value)

    def command(self):
        token = self.look_ahead
        self.eat(TokenType.COMMAND)
        return Command(token)

    def expr(self):
        """
        <expr> ::= <term> ((MINUS | PLUS) <term>)*
        """
        result = self.term()
        if self.look_ahead.type.value not in (TokenType.MINUS.value, TokenType.PLUS.value, TokenType.EOF.value):
            self.eat(TokenType.EQUALS, 'Invalid identifier')
            value = self.factor()
            result = Assignment(result, value)
            self.eat(TokenType.EOF, 'Invalid assignment')
            return result
        while self.look_ahead.type.value in (TokenType.MINUS.value, TokenType.PLUS.value):
            op = self.look_ahead
            if self.look_ahead.type.value == TokenType.PLUS.value:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            right = self.term()
            result = BinaryOP(result, op, right)
        return result

    def term(self):
        """
        <term> ::= <factor> ((DIV | MUL) <factor>)*
        """
        result = self.factor()
        while self.look_ahead.type.value in (TokenType.DIV.value, TokenType.MUL.value):
            op = self.look_ahead
            if self.look_ahead.type.value == TokenType.MUL.value:
                self.eat(TokenType.MUL)
            else:
                self.eat(TokenType.DIV)
            right = self.factor()
            result = BinaryOP(result, op, right)
        return result

    def factor(self):
        """
        <factor> ::= NUMBER
                | <variable>
                | (MINUS | PLUS) <factor>
                | LP <expr> RP
        """
        if self.look_ahead.type.value == TokenType.LP.value:
            self.eat(TokenType.LP)
            result = self.expr()
            self.eat(TokenType.RP)
            return result
        if self.look_ahead.type.value in (TokenType.MINUS.value, TokenType.PLUS.value):
            op = self.look_ahead
            if self.look_ahead.type.value == TokenType.MINUS.value:
                self.eat(TokenType.MINUS)
            else:
                self.eat(TokenType.PLUS)
            return UnaryOP(op, self.factor())
        elif self.look_ahead.type.value == TokenType.IDENTIFIER.value:
            return self.variable()
        token = self.look_ahead
        self.eat(TokenType.NUMBER)
        return Num(token)

    def variable(self):
        """
        <variable> ::= IDENTIFIER
        """
        token = self.look_ahead
        self.eat(TokenType.IDENTIFIER)
        return Var(token)
