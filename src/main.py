import sys

from lexer.cool_lexer import CoolLexer
from parser.cool_parser import CoolParser


def main(_input, _output):
    # text = ''
    with open(_input) as file:
        text = file.read()

    # Lexer
    lexer = CoolLexer()
    tokens = lexer.tokenize(text)
    if lexer.errors:
        for error in lexer.errors:
            print(error)
        exit(1)
        # raise Exception()

    # # Parser
    parser = CoolParser(lexer)
    ast = parser.parse(text)
    # print(parser.errors)
    if parser.errors:
        for error in parser.errors:
            print(error)
        exit(1)


if __name__ == "__main__":
    # Lexer tests
    # in_path = 'tests/lexer/iis1.cl'
    # in_path = 'tests/lexer/mixed1.cl'
    # in_path = '/media/paula/DATA/School/computacion/4to_2023/ENTREGA_COMP/cool-compiler-2023-master/cool-compiler-2023-master/tests/lexer/comment1.cl'
    in_path = 'tests/lexer/string1.cl'

    # Parser tests
    # in_path = 'tests/parser/assignment1.cl'
    # in_path = 'tests/parser/attribute1.cl'
    # in_path = 'tests/parser/block1.cl'
    # in_path = 'tests/parser/case1.cl'
    # in_path = 'tests/parser/class1.cl'
    # in_path = 'tests/parser/conditional1.cl'
    # in_path = 'tests/parser/dispatch1.cl'
    # in_path = 'tests/parser/let1.cl'
    # in_path = 'tests/parser/loop1.cl'
    # in_path = 'tests/parser/method1.cl'
    # in_path = 'tests/parser/mixed1.cl'
    # in_path = 'tests/parser/operation1.cl'
    # in_path = 'tests/parser/program1.cl'

    # in_path = 'tests/codegen/arith.cl'
    # in_path = 'tests/codegen/book_list.cl'
    
    out_path = ''
    # out_path = ''
    _input = sys.argv[1] if len(sys.argv) > 1 else in_path
    _output = sys.argv[2] if len(sys.argv) > 2 else out_path

    main(_input, _output)


