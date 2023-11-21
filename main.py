from src.COOL import CoolLexer
from src.COOL import CoolParser
from src.COOL import Semantic
from src.COOL import Codegen
from src.COOL.token import Program
from src.COOL.utils import load_file


file = "class"

lexer = CoolLexer()
ast = lexer.tokenize(file)
for i in ast:
    print(i)
parser = CoolParser()
program: Program  = parser.parse(ast)

# Semantic.check(program)
# Codegen.check(program)