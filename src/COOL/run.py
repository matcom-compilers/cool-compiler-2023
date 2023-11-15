# from src.COOL import Lexer

# lexer = Lexer('src/COOL/rules.yml')

from src.COOL import SLYLexer
from src.COOL import CoolParser

lexer = SLYLexer()
parser = CoolParser()