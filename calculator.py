from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter
import constants
import exceptions__


def main():
    while True:
        input_ = input()
        if not input_:
            continue
        try:
            tokenizer = Tokenizer(input_)
            parser = Parser(tokenizer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
        except exceptions__.TokenNotRecognizedError:
            print(constants.SYNTAX_ERROR_MESSAGE)
        except (exceptions__.SyntaxNotRecognizedError, exceptions__.InterpreterRuntimeError) as e:
            print(e)
        else:
            if result is not None:
                print(result)
                if result == constants.EXIT_MESSAGE:
                    break


if __name__ == '__main__':
    main()
