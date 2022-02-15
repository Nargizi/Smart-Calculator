# write your code here
import re
from enum import Enum
from exceptions__ import TokenNotRecognizedError


class TokenType(Enum):
    NUMBER = 'NUMBER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    EOF = 'EOF'
    MUL = 'MUL'
    DIV = 'DIV'
    EQUALS = 'EQUALS'
    COMMAND = 'COMMAND'
    IDENTIFIER = 'IDENTIFIER'
    LP = 'LP'
    RP = 'RP'
    IGNORED = None


Tokens = (
    (re.compile(r'/[a-zA-Z]+'), TokenType.COMMAND),
    (re.compile(r'\('), TokenType.LP),
    (re.compile(r'\)'), TokenType.RP),
    (re.compile(r'\s+'), TokenType.IGNORED),
    (re.compile(r'\d+'), TokenType.NUMBER),
    (re.compile(r'\+'), TokenType.PLUS),
    (re.compile(r'-'), TokenType.MINUS),
    (re.compile(r'\*'), TokenType.MUL),
    (re.compile(r'[a-zA-Z]+'), TokenType.IDENTIFIER),
    (re.compile(r'='), TokenType.EQUALS),
    (re.compile(r'/'), TokenType.DIV),
)


class Token:
    def __init__(self, token_type: TokenType, string: str):
        self.type = token_type
        self.string = string

    def __repr__(self):
        return f'Token({self.type.value}, {self.string})'


class Tokenizer:
    def __init__(self, string):
        self.string = string
        self.pos = 0

    def _get_next(self):
        if self.pos <= len(self.string) - 1:
            sub = self.string[self.pos:]
            for pattern, token_type in Tokens:
                match = pattern.match(sub)
                if match:
                    self.pos += match.end()
                    return Token(token_type, match.group())
            self.error()
        return Token(TokenType.EOF, '')

    def next(self):
        token = self._get_next()
        while token.type == TokenType.IGNORED:
            token = self._get_next()
        return token

    def get_iter(self):
        while True:
            token = self.next()
            if token.type == TokenType.EOF:
                yield token
                return
            yield token

    def error(self):
        raise TokenNotRecognizedError(self.string)



