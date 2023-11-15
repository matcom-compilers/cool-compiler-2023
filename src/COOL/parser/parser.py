from src.COOL.lexer.sly_lexer import SLYLexer
from src.COOL.utils import read_yml
from sly import Parser
from src.COOL.token import Token
from src.COOL.token.operators import *


class CoolParser(Parser):
    tokens = SLYLexer.tokens

    # path = '/home/lauren/Documentos/cool-compiler-2023/src/COOL/rules.yml'
    # tokens = read_yml(path).tokens

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

    @_('expr EQUAL expr')
    def expr(self, p):
        return Eq(p.lineno, p.expr0, p.expr1)

    @_('expr LESSTHAN expr')
    def expr(self, p):
        return Lt(p.lineno, p.expr0, p.expr1)

    @_('expr LESSEQUAL expr')
    def expr(self, p):
        return Leq(p.lineno, p.expr0, p.expr1)
