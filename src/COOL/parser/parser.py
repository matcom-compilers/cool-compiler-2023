from src.COOL.lexer.sly_lexer import SLYLexer
from src.COOL.utils import read_yml
from sly import Parser

class CoolParser(Parser):
    tokens = SLYLexer.tokens

    # path = '/home/lauren/Documentos/cool-compiler-2023/src/COOL/rules.yml'
    # tokens = read_yml(path).tokens

    @_('expr PLUS term')
    def expr(self, p):
        return p.expr + p.term

    @_('expr MINUS term')
    def expr(self, p):
        return p.expr - p.term

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return p.term * p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.term / p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

