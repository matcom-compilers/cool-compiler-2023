import os
import sys

from src.COOL import SLYLexer
from src.COOL import CoolParser
from src.COOL import Semantic
from src.COOL import Codegen
from src.COOL.token import Program
from src.COOL.utils import load_file


def run(file):
    ast = SLYLexer.tokenize(file)
    program: Program  = CoolParser.parse(ast)
    Semantic.check(program)
    Codegen.check(program)


# if __name__ == "__main__":
#     if len(sys.argv) == 1 and os.path.isfile(sys.argv[1]) and sys.argv[1].endswith(".cl"):
#         file_path = sys.argv[1]
#         file_content = load_file(file_path)
#         ast = SLYLexer.tokenize(file_content)
#         program: Program  = CoolParser.parse(ast)
#         Semantic.check(program)
#         Codegen.check(program)
