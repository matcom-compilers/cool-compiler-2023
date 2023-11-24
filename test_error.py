import sys
module = "./src/COOL/"
sys.path.append(module)

from src.COOL import CoolLexer
from src.COOL import CoolParser
from src.COOL.utils import load_file

file = "/home/dionisio35/Documents/GitHub/cool-compiler-2023/tests/parser/class3.cl"
loaded_file = load_file(file)

lexer = CoolLexer()
parser = CoolParser()


parser.parse(lexer.tokenize(loaded_file))
