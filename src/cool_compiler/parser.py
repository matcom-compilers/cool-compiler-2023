# type: ignore

from .sly import Parser
from .lexer import CoolLexer


class CoolParser(Parser):
    tokens = CoolLexer.tokens

    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LT', 'LE', 'EQ'),
        ('left', 'SUM', 'SUB'),
        ('left', 'TIMES', 'DIV'),
        ('right', 'ISVOID'),
        ('right', 'NEG'),
        ('left', 'AT'),
        ('left', 'DOT')
    )


    @_('ID binding')
    def expr(self, p):
        # var mutation
        pass


    @_('expr opt_type DOT ID LPAREN arg_list RPAREN')
    def expr(self, p):
        # method dispatch
        pass

    @('AS TYPE')
    def opt_type(self, p):
        return p[1]
    
    @('')
    def opt_type(self, p):
        return None


    @_('ID LPAREN arg_list RPAREN')
    def expr(self, p):
        # function call ('self' method dispatch shorthand)
        pass

    @_('expr COMMA arg_list')
    def arg_list(self, p):
        return [p[0], *p[2]]
    
    @_('expr')
    def arg_list(self, p):
        return [p[0]]


    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        # conditional expr
        pass


    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        # loop expr
        pass


    @_('LBRACE expr_stmt expr_stmt_list RBRACE')
    def expr(self, p):
        # expr block
        pass

    @_('expr_stmt expr_stmt_list')
    def expr_stmt_list(self, p):
        return [p[0], *p[1]]
    
    @_('')
    def expr_stmt_list(self, p):
        return []
    
    @_('expr SEMICOLON')
    def expr_stmt(self, p):
        return p[0]


    @_('LET var_dec var_dec_list IN expr')
    def expr(self, p):
        # var declarations
        pass

    @_('COMMA var_dec var_dec_list')
    def var_dec_list(self, p):
        return [p[1], *p[2]]

    @_('')
    def var_dec_list(self, p):
        return []
    
    @_('ID COLON TYPE opt_binding')
    def var_dec(self, p):
        pass

    @_('binding')
    def opt_binding(self, p):
        return p[0]

    @_('')
    def opt_binding(self, _):
        return None
    
    @_('ASSIGN expr')
    def binding(self, p):
        return p[1]


    @_('CASE expr OF case case_list ESAC')
    def expr(self, p):
        # matching by type
        pass
    
    @_('case case_list')
    def case_list(self, p):
        return [p[0], *p[1]]

    @_('')
    def case_list(self, _):
        return []

    @_('ID COLON TYPE CASE_THEN expr SEMICOLON')
    def case(self, p):
        pass


    @_('NEW TYPE'):
    def expr(self, p):
        # object init
        pass


    @_('ISVOID expr'):
    def expr(self, p):
        # 'isvoid' operator
        pass


    @_(
        'expr SUM expr',
        'expr SUB expr',
        'expr TIMES expr',
        'expr DIV expr'
    )
    def expr(self, p):
        # arith operation
        pass


    @_('NEG expr'):
    def expr(self, p):
        # negation
        pass


    @_(
        'expr LT expr',
        'expr LE expr',
        'expr EQ expr'
    )
    def expr(self, p):
        # comparison operation
        pass


    @_('NOT expr'):
    def expr(self, p):
        # boolean negation
        pass


    @_('LPAREN expr RPAREN'):
    def expr(self, p):
        # grouping
        pass


    @_(
        'ID',
        'INTEGER',
        'STRING',
        'TRUE',
        'FALSE',
    )
    def expr(self, p):
        # literal
        pass
