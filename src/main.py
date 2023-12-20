import sys

from cool_lexer import CoolLexer
from cool_parser import CoolParser


def main(_input, _output):

    with open(_input) as file:
        text = file.read()

    # Lexer
    lexer = CoolLexer(text)
    # _lexer._print(text)
    lexer.tokenize()
    # i = 0
    # for t in tokens:
    #     if i == 20: break
    #     print(t)
    #     i +=1
    # print(lexer.errors)
    if lexer.errors:
        for error in lexer.errors:
            print(error)

    # # Parser
    # parser = CoolParser(lexer)
    # ast = parser.parse(text)
    # # print(parser.errors)
    # if parser.errors:
    #     for error in parser.errors:
    #         print(error)
    #     # parser.print_error()
    #     # raise Exception()


if __name__ == "__main__":
    # Lexer tests
    # in_path = 'tests/lexer/iis1.cl'
    # in_path = 'tests/lexer/mixed1.cl'
    # in_path = 'tests/lexer/string4.cl'
    in_path = 'tests/lexer/comment1.cl'

    # in_path = 'tests/codegen/arith.cl'
    # in_path = 'tests/codegen/book_list.cl'
    
    # in_path = 'tests/parser/assignment1.cl'
    out_path = 'src/codeMips.mips'
    _input = sys.argv[1] #if len(sys.argv) > 1 else in_path
    _output = sys.argv[2] #if len(sys.argv) > 2 else out_path

    main(_input, _output)