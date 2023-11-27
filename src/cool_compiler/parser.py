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

    start = 'program'


    @_('class_dec SEMICOLON class_dec_list')
    def program(self, p):
        classes = [p[0], *p[2]]
        pass

    @_('class_dec SEMICOLON class_dec_list')
    def class_dec_list(self, p):
        return [p[0], *p[2]]

    @_('')
    def class_dec_list(self, p):
        return []


    @_('CLASS TYPE opt_parent LBRACE feature_list RBRACE')
    def class_dec(self, p):
        pass

    @_('INHERITS TYPE')
    def opt_parent(self, p):
        return p[1]
    
    @_('')
    def opt_parent(self, p):
        return None
    
    @_('feature SEMICOLON feature_list')
    def feature_list(self, p):
        return [p[0], *p[2]]
    
    @_('')
    def feature_list(self, _):
        return []


    @_('ID LPAREN param_list RPAREN COLON TYPE LBRACE expr RBRACE')
    def feature(self, p):
        pass

    @_('var_dec rest_param_list')
    def param_list(self, p):
        return [p[0], *p[1]]
    
    @_('')
    def param_list(self, _):
        return []

    @_('COMMA var_dec rest_param_list')
    def rest_param_list(self, p):
        return [p[1], *p[2]]
    
    @_('')
    def rest_param_list(self, _):
        return []
    
    @_('var_init')
    def feature(self, p):
        pass


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

    @_('expr rest_arg_list')
    def arg_list(self, p):
        return [p[0], *p[1]]
    
    @_('')
    def arg_list(self, _):
        return []

    @_('COMMA expr rest_arg_list')
    def rest_arg_list(self, p):
        return [p[1], *p[2]]
    
    @_('')
    def rest_arg_list(self, _):
        return []


    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        # conditional expr
        pass


    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        # loop expr
        pass


    @_('LBRACE expr SEMICOLON expr_list RBRACE')
    def expr(self, p):
        # expr block
        expressions = [p[1], *p[3]]
        pass

    @_('expr SEMICOLON expr_list')
    def expr_list(self, p):
        return [p[0], *p[2]]
    
    @_('')
    def expr_list(self, _):
        return []


    @_('LET var_init var_init_list IN expr')
    def expr(self, p):
        # var declarations
        pass

    @_('COMMA var_init var_init_list')
    def var_init_list(self, p):
        return [p[1], *p[2]]

    @_('')
    def var_init_list(self, _):
        return []
    
    @_('var_dec opt_binding')
    def var_init(self, p):
        pass

    @_('ID COLON TYPE')
    def var_dec(self, p):
        return (p[0], p[2])

    @_('binding')
    def opt_binding(self, p):
        return p[0]

    @_('')
    def opt_binding(self, _):
        return None
    
    @_('ASSIGN expr')
    def binding(self, p):
        return p[1]


    @_('CASE expr OF case SEMICOLON case_list ESAC')
    def expr(self, p):
        # matching by type
        cases = [p[3], *p[5]]
        pass
    
    @_('case SEMICOLON case_list')
    def case_list(self, p):
        return [p[0], *p[2]]

    @_('')
    def case_list(self, _):
        return []

    @_('var_dec CASE_THEN expr')
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
