from .sly import Parser
from .lexer import CoolLexer


class CoolParser(Parser):
    tokens = CoolLexer.tokens
