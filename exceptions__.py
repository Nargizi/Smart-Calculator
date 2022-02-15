class TokenNotRecognizedError(Exception):
    def __init__(self, line, message='Unknown Syntax'):
        self.line = line
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'Error at line {self.line}: {self.message}'


class SyntaxNotRecognizedError(Exception):
    pass


class InterpreterRuntimeError(Exception):
    pass
