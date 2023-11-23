from sly import Parser
from sly.lex import Token as SlyToken

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
from src.COOL.token.feature import Attribute
from src.COOL.token.feature import Method
from src.COOL.token.feature import ExecuteMethod
from src.COOL.token.object import Interger
from src.COOL.token.object import String
from src.COOL.token.object import Boolean
from src.COOL.token.expr import If
from src.COOL.token.expr import While
from src.COOL.token.expr import Let
from src.COOL.token.expr import Case
from src.COOL.token.expr import New
from src.COOL.token.expr import Isvoid
from src.COOL.token.expr import Expr


# TODO: make it a generator
# TODO: fix return clases
# TODO: fix and check precedence
class CoolParser(Parser):
    tokens = CoolLexer.tokens
    debugfile = 'parser.out'
    
    precedence = (
       ('right', 'ASSIGN'),
       ('nonassoc', 'NOT'),
       ('nonassoc', 'EQUAL', 'LESS', 'LESSEQUAL'),
       ('left', 'PLUS', 'MINUS'),
       ('left', 'TIMES', 'DIVIDE'),
       ('right', 'ISVOID'),
       ('left', 'BITWISE'),
       ('nonassoc', '@'),
       ('nonassoc', 'NUMBER'),
       ('nonassoc', '(',')'),
       ('nonassoc', '.'),
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
        return Expr(
            line=p.lineno,
            expr=p.expr,
            id=p.ID,
            exprs=p.exprs
        )

    @_('expr "@" TYPE "." ID "(" exprs ")"')
    def expr(self, p: SlyToken):
        return Expr(
            line=p.lineno,
            expr=p.expr,
            id=p.ID,
            type=p.TYPE,
            exprs=p.exprs
        )
    
    @_('ID "(" exprs ")"')
    def expr(self, p: SlyToken):
        return ExecuteMethod(
            line=p.lineno,
            id=p.ID,
            exprs=p.exprs
        )

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p: SlyToken):
        return If(
            line=p.lineno,
            if_expr=p.expr0,
            then_expr=p.expr1,
            else_expr=p.expr2
        )

    @_('WHILE expr LOOP expr POOL')
    def expr(self, p: SlyToken):
        return While(
            line=p.lineno,
            while_expr=p.expr0,
            loop_expr=p.expr1
        )

    @_('"{" nested_expr "}"')
    def expr(self, p: SlyToken):
        return p.nested_expr

    @_('expr ";" nested_expr')
    def nested_expr(self, p: SlyToken):
        return [p.expr] + p.nested_expr

    @_('expr')
    def nested_expr(self, p: SlyToken):
        return [p.expr]

    @_('LET let_list IN expr')
    def expr(self, p: SlyToken):
        return Let(
            line=p.lineno,
            let_list=p.let_list,
            expr=p.expr
        )

    @_('let_expr "," let_list')
    def let_list(self, p: SlyToken):
        return [p.let_expr] + p.let_list
    
    @_('let_expr')
    def let_list(self, p: SlyToken):
        return [p.let_expr]

    @_('ID ":" TYPE ASSIGN expr')
    def let_expr(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            expr=p.expr
        )

    @_('ID ":" TYPE')
    def let_expr(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE
        )

    @_('CASE expr OF cases ESAC')
    def expr(self, p: SlyToken):
        return Case(
            line=p.lineno,
            expr=p.expr,
            cases=p.cases
        )   

    @_('case ";" cases')
    def cases(self, p: SlyToken):
        return [p.case] + p.cases

    @_('case ";"')
    def cases(self, p: SlyToken):
        return [p.case]

    @_('ID ":" TYPE CASE_ARROW expr')
    def case(self, p: SlyToken):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            expr=p.expr
        )

    @_('NEW TYPE')
    def expr(self, p: SlyToken):
        return New(
            line=p.lineno,
            type=p.TYPE
        )

    @_('ISVOID expr')
    def expr(self, p: SlyToken):
        return Isvoid(
            line=p.lineno,
            expr=p.expr
        )

    @_('expr PLUS expr')
    def expr(self, p: SlyToken):
        return Add(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr MINUS expr')
    def expr(self, p: SlyToken):
        return Sub(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr TIMES expr')
    def expr(self, p: SlyToken):
        return Times(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr DIVIDE expr')
    def expr(self, p: SlyToken):
        return Div(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr LESS expr')
    def expr(self, p: SlyToken):
        return Less(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr LESSEQUAL expr')
    def expr(self, p: SlyToken):
        return LessEqual(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )
    
    @_('expr EQUAL expr')
    def expr(self, p: SlyToken):
        return Equal(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('NOT expr')
    def expr(self, p: SlyToken):
        return Not(
            line=p.lineno,
            expr=p.expr,
        )
    
    @_('BITWISE expr')
    def expr(self, p: SlyToken):
        return Bitwise(
            line=p.lineno,
            expr=p.expr,
        )

    @_('NUMBER')
    def expr(self, p: SlyToken):
        return Interger(line=p.lineno, value=p.NUMBER)
    
    @_('STRING')
    def expr(self, p: SlyToken):
        return String(line=p.lineno, value=p.STRING)
    
    @_('"(" expr ")"')
    def expr(self, p: SlyToken):
        return p.expr
    
    @_('ID')
    def expr(self, p: SlyToken):
        return Attribute(line=p.lineno, id=p.ID)

    @_('TRUE')
    def expr(self, p: SlyToken):
        return Boolean(line=p.lineno, value=True)

    @_('FALSE')
    def expr(self, p: SlyToken):
        return Boolean(line=p.lineno, value=False)


    def error(self, p):
        if p:
            raise SystemExit(f"\nSyntax error at token: {p.type}, line: {p.lineno}")
        else:
            raise SystemExit("Syntax error at EOF")
