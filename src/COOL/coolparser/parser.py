from sly import Parser

from error import Error
from coollexer import CoolLexer
from tokens import Token

from nodes.operators import Add
from nodes.operators import Sub
from nodes.operators import Times
from nodes.operators import Div
from nodes.operators import Less
from nodes.operators import LessEqual
from nodes.operators import Equal
from nodes.operators import Not
from nodes.operators import Bitwise

from nodes.program import Program
from nodes.classdef import Class
from nodes.feature import Attribute
from nodes.feature import Method
from nodes.feature import ExecuteMethod
from nodes.object import Interger
from nodes.object import String
from nodes.object import Boolean
from nodes.expr import If
from nodes.expr import While
from nodes.expr import Let
from nodes.expr import Case
from nodes.expr import New
from nodes.expr import Isvoid
from nodes.expr import Expr


# TODO: make it a generator
# TODO: fix return clases
# TODO: fix and check precedence
# TODO: column of tokens
# TODO: test parser from block to case, operation
class CoolParser(Parser):
    tokens = CoolLexer.tokens
    # debugfile = 'parser.out'
    
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

    @_('program')
    def start(self, p: Token):
        return Program(classes=p.program)

    @_('classdef ";"')
    def program(self, p: Token):
        return [p.classdef]
    
    @_('classdef ";" program')
    def program(self, p: Token):
        return [p.classdef] + p.program

    @_('CLASS TYPE "{" features "}"')
    def classdef(self, p: Token):
        return Class(
            line=p.lineno,
            type=p.TYPE,
            features=p.features
        )

    @_('CLASS TYPE INHERITS TYPE "{" features "}"')
    def classdef(self, p: Token):
        return Class(
            line=p.lineno,
            features=p.features,
            type=p.TYPE0,
            inherits=p.TYPE1
        )

    @_('feature ";" features')
    def features(self, p: Token):
        return [p.feature] + p.features

    @_('')
    def features(self, p: Token):
        return []
    
    @_('ID ":" TYPE ASSIGN expr')
    def feature(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            expr=p.expr
        )
    
    @_('ID ":" TYPE')
    def feature(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE
        )

    @_('ID "(" formals ")" ":" TYPE "{" expr "}"')
    def feature(self, p: Token):
        return Method(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            formals=p.formals,
            expr=p.expr
        )

    @_('formal "," formals')
    def formals(self, p: Token):
        return [p.formal] + p.formals
    
    @_('formal')
    def formals(self, p: Token):
        return [p.formal]
    
    @_("")
    def formals(self, p: Token):
        return []

    @_('ID ":" TYPE')
    def formal(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE
        )
    
    @_('expr "," exprs')
    def exprs(self, p: Token):
        return [p.expr] + p.exprs
    
    @_('expr')
    def exprs(self, p: Token):
        return [p.expr]
    
    @_("")
    def exprs(self, p: Token):
        return []

    @_('ID ASSIGN expr')
    def expr(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            expr=p.expr
        )
    
    @_('expr "." ID "(" exprs ")"')
    def expr(self, p: Token):
        return Expr(
            line=p.lineno,
            expr=p.expr,
            id=p.ID,
            exprs=p.exprs
        )

    @_('expr "@" TYPE "." ID "(" exprs ")"')
    def expr(self, p: Token):
        return Expr(
            line=p.lineno,
            expr=p.expr,
            id=p.ID,
            type=p.TYPE,
            exprs=p.exprs
        )
    
    @_('ID "(" exprs ")"')
    def expr(self, p: Token):
        return ExecuteMethod(
            line=p.lineno,
            id=p.ID,
            exprs=p.exprs
        )

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p: Token):
        return If(
            line=p.lineno,
            if_expr=p.expr0,
            then_expr=p.expr1,
            else_expr=p.expr2
        )

    @_('WHILE expr LOOP expr POOL')
    def expr(self, p: Token):
        return While(
            line=p.lineno,
            while_expr=p.expr0,
            loop_expr=p.expr1
        )

    @_('"{" nested_expr "}"')
    def expr(self, p: Token):
        return p.nested_expr

    @_('expr ";" nested_expr')
    def nested_expr(self, p: Token):
        return [p.expr] + p.nested_expr
    
    @_('expr ";"')
    def nested_expr(self, p: Token):
        return [p.expr]

    @_('LET let_list IN expr')
    def expr(self, p: Token):
        return Let(
            line=p.lineno,
            let_list=p.let_list,
            expr=p.expr
        )

    @_('let_expr "," let_list')
    def let_list(self, p: Token):
        return [p.let_expr] + p.let_list
    
    @_('let_expr')
    def let_list(self, p: Token):
        return [p.let_expr]

    @_('ID ":" TYPE ASSIGN expr')
    def let_expr(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            expr=p.expr
        )

    @_('ID ":" TYPE')
    def let_expr(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE
        )

    @_('CASE expr OF cases ESAC')
    def expr(self, p: Token):
        return Case(
            line=p.lineno,
            expr=p.expr,
            cases=p.cases
        )   

    @_('case ";" cases')
    def cases(self, p: Token):
        return [p.case] + p.cases

    @_('case ";"')
    def cases(self, p: Token):
        return [p.case]

    @_('ID ":" TYPE CASE_ARROW expr')
    def case(self, p: Token):
        return Attribute(
            line=p.lineno,
            id=p.ID,
            type=p.TYPE,
            expr=p.expr
        )

    @_('NEW TYPE')
    def expr(self, p: Token):
        return New(
            line=p.lineno,
            type=p.TYPE
        )

    @_('ISVOID expr')
    def expr(self, p: Token):
        return Isvoid(
            line=p.lineno,
            expr=p.expr
        )

    @_('expr PLUS expr')
    def expr(self, p: Token):
        return Add(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr MINUS expr')
    def expr(self, p: Token):
        return Sub(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr TIMES expr')
    def expr(self, p: Token):
        return Times(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr DIVIDE expr')
    def expr(self, p: Token):
        return Div(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr LESS expr')
    def expr(self, p: Token):
        return Less(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('expr LESSEQUAL expr')
    def expr(self, p: Token):
        return LessEqual(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )
    
    @_('expr EQUAL expr')
    def expr(self, p: Token):
        return Equal(
            line=p.lineno,
            expr1=p.expr0,
            expr2=p.expr1
        )

    @_('NOT expr')
    def expr(self, p: Token):
        return Not(
            line=p.lineno,
            expr=p.expr,
        )
    
    @_('BITWISE expr')
    def expr(self, p: Token):
        return Bitwise(
            line=p.lineno,
            expr=p.expr,
        )

    @_('NUMBER')
    def expr(self, p: Token):
        return Interger(line=p.lineno, value=p.NUMBER)
    
    @_('STRING')
    def expr(self, p: Token):
        return String(line=p.lineno, value=p.STRING)
    
    @_('"(" expr ")"')
    def expr(self, p: Token):
        return p.expr
    
    @_('ID')
    def expr(self, p: Token):
        return Attribute(line=p.lineno, id=p.ID)

    @_('TRUE')
    def expr(self, p: Token):
        return Boolean(line=p.lineno, value=True)

    @_('FALSE')
    def expr(self, p: Token):
        return Boolean(line=p.lineno, value=False)

    # FIX: change some tokens from value to tipe e.g. <- to ASSIGN
    def error(self, p: Token):
        if p:
            Error.error(
            line=p.lineno,
            column=p.column,
            error_type="SyntacticError",
            message=f"ERROR at or near \"{p.value}\""
        )
        else:
            Error.error(
                line=0,
                column=0,
                error_type="SyntacticError",
                message=f"ERROR at or near EOF"
            )
