# type: ignore

from .sly import Parser
from .lexer import CoolLexer
import .ast


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
        return [p[0], *p[2]]
        

    @_('class_dec SEMICOLON class_dec_list')
    def class_dec_list(self, p):
        return [p[0], *p[2]]

    @_('')
    def class_dec_list(self, p):
        return []


    @_('CLASS TYPE opt_parent LBRACE feature_list RBRACE')
    def class_dec(self, p):
        return ast.ClassDeclarationAST(
            p[1].value,
            p[2],
            p[4]
        )

    @_('INHERITS TYPE')
    def opt_parent(self, p):
        return p[1].value
    
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
        return ast.FunctionDeclarationFeatureAST(
            p[0].value,
            p[2],
            p[5].value,
            p[7]
        )

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
        return ast.VarInitFeatureAST(*p[0])


    @_('ID binding')
    def expr(self, p):
        # var mutation
        return ast.VarMutationAST(p[0].value, p[1])


    @_('expr opt_type DOT ID LPAREN arg_list RPAREN')
    def expr(self, p):
        # method dispatch
        return ast.FunctionCallAST(
            p[3].value,
            p[5],
            p[0],
            p[1]
        )

    @('AS TYPE')
    def opt_type(self, p):
        return p[1]
    
    @('')
    def opt_type(self, p):
        return None


    @_('ID LPAREN arg_list RPAREN')
    def expr(self, p):
        # function call ('self' method dispatch shorthand)
        return ast.FunctionCallAST(p[0].value, p[2])

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
        return ast.ConditionalExpressionAST(p[1], p[3], p[5])


    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        # loop expr
        return ast.LoopExpressionAST(p[1], p[3])


    @_('LBRACE expr SEMICOLON expr_list RBRACE')
    def expr(self, p):
        # expr block
        expressions = [p[1], *p[3]]
        return ast.BlockExpressionAST(expressions)

    @_('expr SEMICOLON expr_list')
    def expr_list(self, p):
        return [p[0], *p[2]]
    
    @_('')
    def expr_list(self, _):
        return []


    @_('LET var_init var_init_list IN expr')
    def expr(self, p):
        # var declarations
        vars = [p[1], *p[2]]
        return ast.VarsInitAST(vars, p[4])

    @_('COMMA var_init var_init_list')
    def var_init_list(self, p):
        return [p[1], *p[2]]

    @_('')
    def var_init_list(self, _):
        return []
    
    @_('var_dec opt_binding')
    def var_init(self, p):
        return (*p[0], p[1])

    @_('ID COLON TYPE')
    def var_dec(self, p):
        return (p[0].value, p[2].value)

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
        return ast.TypeMatchingAST(p[1], cases)
    
    @_('case SEMICOLON case_list')
    def case_list(self, p):
        return [p[0], *p[2]]

    @_('')
    def case_list(self, _):
        return []

    @_('var_dec CASE_THEN expr')
    def case(self, p):
        return (*p[0], p[2])


    @_('NEW TYPE'):
    def expr(self, p):
        # object init
        return ast.ObjectInitAST(p[1].value)


    @_('ISVOID expr'):
    def expr(self, p):
        # 'isvoid' operator
        return ast.VoidCheckingOpAST(p[1])


    @_(
        'expr SUM expr',
        'expr SUB expr',
        'expr TIMES expr',
        'expr DIV expr'
    )
    def expr(self, p):
        # arith operation
        return ast.ArithmeticOpAST(p[0], p[2], p[1].value)


    @_('NEG expr'):
    def expr(self, p):
        # negation
        return ast.NegationOpAST(p[1])


    @_(
        'expr LT expr',
        'expr LE expr',
        'expr EQ expr'
    )
    def expr(self, p):
        # comparison operation
        return ast.ComparisonOpAST(p[0], p[2], p[1].value)


    @_('NOT expr'):
    def expr(self, p):
        # boolean negation
        return ast.BooleanNegationOpAST(p[1])


    @_('LPAREN expr RPAREN'):
    def expr(self, p):
        # grouping
        return p[1]


    @_(
        'ID',
        'INTEGER',
        'STRING',
        'TRUE',
        'FALSE',
    )
    def expr(self, p):
        # literal
        token = p[0]
        type = token.type
        value = token.value

        if type == "ID":
            return ast.IdentifierAST(value)
        if type == "INTEGER":
            return ast.IntAST(value)
        if type == "STRING":
            return ast.StringAST(value)
        if type == "TRUE" or type == "FALSE":
            return ast.BooleanAST(value)
