from sly import Parser

from src.COOL.lexer import SLYLexer
from src.COOL.token.operators import *
from src.COOL.token.program import Program


# TODO: make it a generator
class CoolParser(Parser):
    tokens = SLYLexer.tokens
    debugfile = 'parser.out'
    
    precedence = (
       ('left', 'ASSIGN'),
       ('left', 'NOT'),
       ('left', 'EQUAL', 'LESS', 'LESSEQUAL'),
       ('left', 'PLUS', 'MINUS'),
       ('left', 'TIMES', 'DIVIDE'),
       ('left', 'BITWISE'),
       ('', 'LPAREN', 'RPAREN'),
       ('', 'NUMBER'),
    )

    @_("program")
    def start(self, p):
        return Program(p.program)

    @_('classdef ";"')
    def program(self, p):
        yield p.classdef
    
    @_('classdef ";" program')
    def program(self, p):
        yield p.classdef

    @_('CLASS TYPE INHERITS TYPE "{" feature "}"')
    def classdef(self, p):
        return p.classdef
    
    @_('CLASS TYPE { [feature]}')
    def classdef(self, p):
        return p.classdef
    
    @_('ID : TYPE  ASSIGN expr ')
    def feature(self, p):
        return p.feature

    @_('ID( [ formal [ formal]] ) : TYPE { expr }')
    def feature(self, p):
        return p.feature
    @_(' ID : TYPE')
    def formal(self,p):
        return p.expr

    @_('ID <- expr')
    def expr(self, p):
        return p.expr

    @_('expr')
    def exprs(self, p):
        return [p.expr]

    @_('exprs expr')
    def exprs(self, p):
        return p.exprs + [p.expr]
    
    @_('')
    def exprs(self, p):
        return []

    @_('expr PLUS expr')
    def expr(self, p):
        return Add(p.lineno,  p[0], p[1])

    @_('expr MINUS expr')
    def expr(self, p):
        return Sub(p.lineno,  p[0], p[1])

    @_('expr TIMES expr')
    def expr(self, p):
        return Times(p.lineno, p[0], p[1])

    @_('expr DIVIDE expr')
    def expr(self, p):
        return Div(p.lineno, p[0], p[1])

    @_('expr LESS expr')
    def expr(self, p):
        return Less(p.lineno, p[0], p[1])
    @_('expr LESSEQUAL expr')
    def expr(self, p):
        return LessEqual(p.lineno, p[0], p[1])
    
    @_('expr EQUAL expr')
    def expr(self, p):
        return Equal(p.lineno, p[0], p[1])

    @_('NOT expr')
    def expr(self, p):
        return Not(p.lineno, p[0])
    
    @_('BITWISE expr')
    def expr(self, p):
        return Bitwise(p.lineno, p[0])

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr
