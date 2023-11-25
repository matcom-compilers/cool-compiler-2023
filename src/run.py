import os
import sys

from COOL.coollexer import CoolLexer
from COOL.coolparser import CoolParser
from COOL.semantic import Semantic
from COOL.codegen import Codegen
from COOL.nodes import Program
from COOL.utils import load_file


def check_errors(errors):
    if errors:
        for error in errors:
            print(error)
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nError: Invalid number of arguments")
        print("Usage: python3 run.py <input_file> <output_file>")
        exit(1)
    if not os.path.isfile(sys.argv[1]):
        print("\nError: Input file does not exist")
        exit(1)
    if not sys.argv[1].endswith(".cl"):
        print("\nError: Input file is not a .cl file")
        exit(1)

    file_path = sys.argv[1]
    output_path = sys.argv[2]
    file_content = load_file(file_path)

    lexer = CoolLexer()
    tokens, errors = lexer.tokenize(file_content)
    check_errors(errors)

    parser = CoolParser()
    ast, errors = parser.parse(tokens)
    check_errors(errors)

    exit(0)
