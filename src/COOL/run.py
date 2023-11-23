import os
import sys

from coollexer import CoolLexer
from coolparser import CoolParser
from semantic import Semantic
from codegen import Codegen
from tokens import Program
from utils import load_file


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
    parser = CoolParser()
    program: Program = parser.parse(lexer.tokenize(file_content))
    Semantic.check(program)
    Codegen.execute(program, output_path)
    print("Compilation finished successfully!")