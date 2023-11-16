from sly import Parser

from src.COOL.lexer import SLYLexer
from src.COOL.token.operators import *


class CoolParser(Parser):
    tokens = SLYLexer.tokens
    debugfile = 'parser.out'

    @_('expr PLUS term')
    def expr(self, p):
        return Add(p.lineno, p.expr, p.term)

    @_('expr MINUS term')
    def expr(self, p):
        return Sub(p.lineno, p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return Mult(p.lineno, p.term, p.factor)

    @_('term DIVIDE factor')
    def term(self, p):
        return Div(p.lineno, p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr
