import unittest
from ..parser import Parser
from ..ast__ import NodeVisitor, UnaryOP, BinaryOP, Num, Command, Assignment, Var
from ..tokenizer import TokenType, Token, Tokenizer

class MockTokenizer(Tokenizer):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def next(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

class LispTranslator(NodeVisitor):
    @staticmethod
    def visit_Command(node: Command):
        return f'(\\ {node.token.string})'

    def visit_Assignment(self, node: Assignment):
        return f'(= {node.var.string} {self.visit(node.value)})'

    @staticmethod
    def visit_Var(node: Var):
        return f'{node.token.string}'

    def visit_UnaryOP(self, node: UnaryOP):
        expr = self.visit(node.operand)
        if node.op.type == TokenType.MINUS:
            operator = '-'
        else:
            operator = '+'
        return f'({operator} {expr})'

    def visit_BinaryOP(self, node: BinaryOP):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op.type == TokenType.PLUS:
            operator = '+'
        if node.op.type == TokenType.MINUS:
            operator = '-'
        if node.op.type == TokenType.MUL:
            operator = '*'
        if node.op.type == TokenType.DIV:
            operator = '/'
        return f'({operator} {left} {right})'

    @staticmethod
    def visit_Num(node: Num):
        return node.token.string


class ParserTests(unittest.TestCase):
    # def test_basic(self):
    #     expr = ['/exit', '/help']
    #     asts = [Exit(Token(TokenType.HELP, '/exit')), Help(Token(TokenType.HELP, '/help'))]
    #     self.helper(expr, asts)
    def test_assignment(self):
        tokens1 = [Token(TokenType.IDENTIFIER, 'a'), Token(TokenType.EQUALS, '='),
                   Token(TokenType.NUMBER, '123'), Token(TokenType.EOF, '')]
        tokens2 = tokens1[:2] + [Token(TokenType.IDENTIFIER, 'b')] + tokens1[-1:]
        ast1 = [Assignment(tokens1[0], Num(tokens1[2]))]
        ast2 = [Assignment(tokens2[0], Var(tokens2[2]))]
        self.helper([tokens1, tokens2], ast1 + ast2)

    def helper(self, expressions, answers):
        translator = LispTranslator()
        for expr, ast in zip(expressions, answers):
            parser = Parser(MockTokenizer(expr))
            self.assertEqual(translator.visit(parser.parse()), translator.visit(ast))


if __name__ == '__main__':
    unittest.main()
