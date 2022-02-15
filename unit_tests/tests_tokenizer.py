import unittest
import itertools
from ..tokenizer import Tokenizer, TokenType


class TokenizerTestCase(unittest.TestCase):
    def test_numbers(self):
        expr = ['123', '12', '  13', ' 1   ', ' 3  ', '123  ']
        tokens = [TokenType.NUMBER, TokenType.EOF]
        self.helper(expr, itertools.repeat(tokens))

    def test_binary_addition(self):
        expr = ['5 + 7', '100+2', '23 +1', '123    + \n   431']
        tokens = [TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.EOF]
        self.helper(expr, itertools.repeat(tokens))

    def test_unary_operators(self):
        expr = ['-1', '-123', '-343']
        tokens = [TokenType.MINUS, TokenType.NUMBER, TokenType.EOF]
        self.helper(expr, itertools.repeat(tokens))

        expr = ['+32', ' +345', '+4']
        tokens = [TokenType.PLUS] + tokens[1:]
        self.helper(expr, itertools.repeat(tokens))

        expr = ['--12', '+-12', '---32', '++32']
        token1 = [TokenType.MINUS] * 2 + [TokenType.NUMBER, TokenType.EOF]
        token2 = [TokenType.PLUS, TokenType.MINUS] + token1[2:]
        token3 = [TokenType.MINUS] * 3 + token1[2:]
        token4 = [TokenType.PLUS] * 2 + token1[2:]
        self.helper(expr, [token1, token2, token3, token4])

    def test_assignment(self):
        expr = ['a = 3', 'NAN = 23', 'b =  1']
        tokens = [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.NUMBER, TokenType.EOF]
        self.helper(expr, itertools.repeat(tokens))

        expr = ['A = B', 'An = a', 'C = c', 'd = db']
        tokens = [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.IDENTIFIER, TokenType.EOF]
        self.helper(expr, itertools.repeat(tokens))

    def helper(self, expressions, tokens):
        for expr, types in zip(expressions, tokens):
            tokenizer = Tokenizer(expr)
            for token, token_type in itertools.zip_longest(tokenizer.get_iter(), types):
                self.assertIsNotNone(token)
                self.assertIsNotNone(token_type)
                self.assertEqual(token.type.value, token_type.value)


if __name__ == '__main__':
    unittest.main()
