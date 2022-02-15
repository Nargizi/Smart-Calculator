class AST:
    pass


class Command(AST):
    def __init__(self, token):
        self.token = token


class BinaryOP(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token


class Var(AST):
    def __init__(self, token):
        self.token = token


class UnaryOP(AST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class Assignment(AST):
    def __init__(self, var, value):
        self.var = var
        self.value = value


class NodeVisitor:
    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass
