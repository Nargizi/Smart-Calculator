from ast__ import BinaryOP, UnaryOP, Num, Command, NodeVisitor, Var, Assignment
from tokenizer import TokenType
from exceptions__ import InterpreterRuntimeError
import constants


class Interpreter(NodeVisitor):
    variables = {}

    def __init__(self, parser):
        self.parser = parser

    def error(self, error_msg):
        raise InterpreterRuntimeError(error_msg)

    def visit_Command(self, node: Command):
        command = node.token.string
        if command in constants.COMMANDS:
            return constants.COMMANDS[command]
        self.error(constants.UNKNOWN_COMMAND_MESSAGE)

    def visit_UnaryOP(self, node: UnaryOP):
        if node.op.type == TokenType.MINUS:
            return - self.visit(node.operand)
        return self.visit(node.operand)

    def visit_BinaryOP(self, node: BinaryOP):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.DIV:
            return self.visit(node.left) // self.visit(node.right)

    @staticmethod
    def visit_Num(node: Num):
        return int(node.token.string)

    def visit_Assignment(self, node: Assignment):
        var = node.var.token.string
        value = self.visit(node.value)
        self.variables[var] = value

    def visit_Var(self, node: Var):
        try:
            value = self.variables[node.token.string]
        except KeyError:
            self.error('Unknown variable')
        else:
            return value

    def interpret(self):
        ast = self.parser.parse()
        return self.visit(ast)
