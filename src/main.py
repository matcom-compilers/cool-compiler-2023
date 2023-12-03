import sys

from cool_lexer import CoolLexer
from cool_parser import CoolParser


def main(_input, _output):

    with open(_input) as file:
        text = file.read()

    # Lexer
    lexer = CoolLexer()
    tokens = lexer.run(text)
    # print(lexer.errors)

    # Parser
    parser = CoolParser(lexer)
    ast = parser.parse(text)
    # print(parser.errors)
    if parser.errors:
        parser.print_error()
        raise Exception()


if __name__ == "__main__":
    in_path = 'tests/codegen/arith.cl'
    out_path = 'src/codeMips.mips'
    _input = sys.argv[1] if len(sys.argv) > 1 else in_path
    _output = sys.argv[2] if len(sys.argv) > 2 else out_path

    main(_input, _output)