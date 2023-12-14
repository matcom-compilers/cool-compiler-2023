import os
import sys
from pathlib import Path

from COOL import CoolLexer
from COOL import CoolParser
from COOL import Semantic
from COOL import Codegen
from COOL.utils import load_file
from COOL.utils import save_output


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

    errors = Semantic.check(ast)
    check_errors(errors)

    mips_code = Codegen.codegen(ast)
    save_output(os.path.join(Path(__file__).parent.parent, "tests", "codegen", output_path), mips_code)
    
    exit(0)
