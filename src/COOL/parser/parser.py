from sly import Parser
from sly.lex import Token as SlyToken
from itertools import chain

from src.COOL.lexer import CoolLexer

from src.COOL.token.operators import Add
from src.COOL.token.operators import Sub
from src.COOL.token.operators import Times
from src.COOL.token.operators import Div
from src.COOL.token.operators import Less
from src.COOL.token.operators import LessEqual
from src.COOL.token.operators import Equal
from src.COOL.token.operators import Not
from src.COOL.token.operators import Bitwise

from src.COOL.token.program import Program
from src.COOL.token.classdef import Class
from src.COOL.token.attribute import Attribute
from src.COOL.token.method import Method
from src.COOL.token.object import Interger
from src.COOL.token.object import String


# TODO: make it a generator
# TODO: fix return clases
class CoolParser(Parser):
    tokens = CoolLexer.tokens
    debugfile = 'parser.out'
    
    precedence = (
       ('right', 'ASSIGN'),
       ('nonassoc', 'NOT'),
       ('nonassoc', 'EQUAL', 'LESS', 'LESSEQUAL'),
       ('left', 'PLUS', 'MINUS'),
       ('left', 'TIMES', 'DIVIDE'),
       ('left', 'BITWISE'),
       ('nonassoc', 'NUMBER'),
    )

    @_("program")
    def start(self, p: SlyToken):
        return Program(classes=p.program)

    @_('classdef ";"')
    def program(self, p: SlyToken):
        return [p.classdef]
    
    @_('classdef ";" program')
    def program(self, p: SlyToken):
        return [p.classdef] + p.program

    @_('CLASS TYPE "{" features "}"')
    def classdef(self, p: SlyToken):
        return Class(
            line=p.lineno,
            type=p.TYPE,
            features=p.features
        )

    @_('CLASS TYPE INHERITS TYPE "{" features "}"')
    def classdef(self, p: SlyToken):
        return Class(
            line=p.lineno,
            features=p.features,
            type=p.TYPE0,
            inherits=p.TYPE1
        )

    @_('feature ";" features')
    def features(self, p: SlyToken):
        return [p.feature] + p.features

    @_('')
    def features(self, p: SlyToken):
        return []
    
    @_('ID ":" TYPE ASSIGN expr')
    def feature(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            expr=p.expr
        )
    
    @_('ID ":" TYPE')
    def feature(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE
        )

    # TODO
    @_('ID "(" formals ")" ":" TYPE "{" expr "}"')
    def feature(self, p: SlyToken):
        return Method(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            formals=p.formals,
            expr=p.expr
        )

    @_('formal "," formals')
    def formals(self, p: SlyToken):
        return [p.formal] + p.formals
    
    @_('formal')
    def formals(self, p: SlyToken):
        return [p.formal]
    
    @_("")
    def formals(self, p: SlyToken):
        return []

    # TODO: make formal class?
    @_('ID ":" TYPE')
    def formal(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE
        )
    
    @_('expr "," exprs')
    def exprs(self, p: SlyToken):
        return [p.expr] + p.exprs
    
    @_('expr')
    def exprs(self, p: SlyToken):
        return [p.expr]
    
    @_("")
    def exprs(self, p: SlyToken):
        return []

    @_('ID ASSIGN expr')
    def expr(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            expr=p.expr
        )
    
    @_('expr "." ID "(" exprs ")"')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('expr "@" TYPE "." ID "(" exprs ")"')
    def expr(self, p: SlyToken):
        #TODO
        pass
    
    @_('ID "(" exprs ")"')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('WHILE expr LOOP expr POOL')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('"{" nested_expr "}"')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('expr ";" nested_expr')
    def nested_expr(self, p: SlyToken):
        #TODO
        pass

    @_('expr')
    def nested_expr(self, p: SlyToken):
        #TODO
        pass

    @_('LET let_list IN expr')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('let_expr "," let_list')
    def let_list(self, p: SlyToken):
        #TODO
        pass
    
    @_('let_expr')
    def let_list(self, p: SlyToken):
        #TODO
        pass

    @_('ID ":" TYPE ASSIGN expr')
    def let_expr(self, p: SlyToken):
        #TODO
        pass

    @_('ID ":" TYPE')
    def let_expr(self, p: SlyToken):
        #TODO
        pass

    # FIX and add the others
    @_('CASE expr OF cases ESAC')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('case ";" cases')
    def cases(self, p: SlyToken):
        #TODO
        pass

    @_('case ";"')
    def cases(self, p: SlyToken):
        #TODO
        pass

    @_('ID ":" TYPE CASE_ARROW expr')
    def case(self, p: SlyToken):
        #TODO
        pass

    @_('NEW TYPE')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('ISVOID expr')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('expr PLUS expr')
    def expr(self, p: SlyToken):
        return Add(p.lineno,  p[0], p[1])

    @_('expr MINUS expr')
    def expr(self, p: SlyToken):
        return Sub(p.lineno,  p[0], p[1])

    @_('expr TIMES expr')
    def expr(self, p: SlyToken):
        return Times(p.lineno, p[0], p[1])

    @_('expr DIVIDE expr')
    def expr(self, p: SlyToken):
        return Div(p.lineno, p[0], p[1])

    @_('expr LESS expr')
    def expr(self, p: SlyToken):
        return Less(p.lineno, p[0], p[1])

    @_('expr LESSEQUAL expr')
    def expr(self, p: SlyToken):
        return LessEqual(p.lineno, p[0], p[1])
    
    @_('expr EQUAL expr')
    def expr(self, p: SlyToken):
        return Equal(p.lineno, p[0], p[1])

    @_('NOT expr')
    def expr(self, p: SlyToken):
        return Not(p.lineno, p[0])
    
    @_('BITWISE expr')
    def expr(self, p: SlyToken):
        return Bitwise(p.lineno, p[0])

    @_('NUMBER')
    def expr(self, p: SlyToken):
        return Interger(line=p.lineno, value=p.NUMBER)
    
    @_('STRING')
    def expr(self, p: SlyToken):
        return String(line=p.lineno, value=p.STRING)
    
    @_('"(" expr ")"')
    def expr(self, p: SlyToken):
        #TODO
        pass
    
    @_('ID')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('TRUE')
    def expr(self, p: SlyToken):
        #TODO
        pass

    @_('FALSE')
    def expr(self, p: SlyToken):
        #TODO
        pass


    def error(self, p):
        if p:
            print("Syntax error at token", p.type)
            # Just discard the token and tell the parser it's okay.
            self.errok()
        else:
            print("Syntax error at EOF")