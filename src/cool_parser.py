from ply.yacc import yacc
from cool_ast import *
from errors import SyntacticError
from utils import tokens


class CoolParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = tokens
        self.errors = []

        self.parser = yacc(start='program', module=self)

        self.precedence = (
            ('right', 'ASSIGN'),
            ('right', 'NOT'),
            ('nonassoc', 'LESSEQ', 'LESS', 'EQUAL'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'STAR', 'DIV'),
            ('right', 'ISVOID'),
            ('left', 'AT'),
            ('left', 'DOT'),
            ('left', 'COMPL')
        )


    def parse(self, program):
        return self.parser.parse(program, self.lexer.lexer)


    def p_program(self, p):
        '''
        program : class_list
        '''        
        p[0] = ProgramNode(p[1])


    def p_class_list(self, p):
        '''
        class_list : class SEMICOLON class_list
                      | class SEMICOLON 
        '''
        if len(p) == 3:
            p[0] = [p[1]]
        
        else:
            p[0] = [p[1]] + p[3]


    def p_class(self, p):
        '''
        class : CLASS TYPE LBRACE feature_list RBRACE
                 | CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE
        '''
        if len(p) == 8:
            p[0] = ClassNode(id_=p[2], parent=p[6], features=p[4])
        else:
            p[0] = ClassNode(id_=p[2], features=p[4])
        
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_feature_list(self, p):
        '''
        feature_list : attributte SEMICOLON feature_list
                        | method SEMICOLON feature_list
                        | empty
        '''
        if len(p) == 4:
            p[0] = [p[1]] + p[3] 
        
        else: 
            p[0] = []
        

    def p_attributte(self, p):
        '''
        attributte : ID COLON TYPE
                   | ID COLON TYPE ASSIGN expression
        '''                      
        if len(p) == 4:
            p[0] = AttributeNode(id_=p[1], type_= p[3])
        else:
            p[0] = AttributeNode(id_=p[1], type_=p[3], expression=p[5])

        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        

    def p_method(self, p):
        '''
        method : ID LPAREN params RPAREN COLON TYPE LBRACE expression RBRACE
        '''
        p[0] = MethodNode(id_=p[1], params=p[3], return_type=p[6], body=p[8])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_params(self, p):
        '''
        params : param_list
               | param_list_empty
        '''
        
        p[0] = p[1]


    def p_param_list(self, p):
        '''
        param_list : param
                   | param COMMA param_list
        '''        
        if len(p) == 2:
            p[0] = [p[1]]

        else:
            p[0] = [p[1]] + p[3]

    
    def p_param_list_empty(self, p):
        '''
        param_list_empty : empty
        '''
        p[0] = []


    def p_param(self, p):
        '''
        param : ID COLON TYPE
        '''
        p[0] = ParamNode(id_=p[1], type_= p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_list(self, p):
        '''
        expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON
        '''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]

        elif len(p) == 3:
            p[0] = [p[1]]


    def p_expression_assigment(self, p):
        '''
        expression : ID ASSIGN expression
        '''
        p[0] = AssignmentNode(id_=p[1], expression=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)

    
    def p_expression_conditional(self, p):
        '''
        expression : IF expression THEN expression ELSE expression FI
        '''
        p[0] = ConditionalNode(if_expression=p[2], then_expression=p[4], else_expression=p[6])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_loop(self, p):
        '''
        expression : WHILE expression LOOP expression POOL
        '''
        p[0] = LoopNode(while_expression=p[2], loop_expression=p[4])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_block(self, p):
        '''
        expression : LBRACE expression_list RBRACE
        '''
        p[0] = BlockNode(expressions_list=p[2])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_let(self, p):
        '''
        expression : LET let_var_list IN expression
        '''
        p[0] = LetNode(variable_list=p[2], in_expression=p[4])
        p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_let_var_list(self, p):
        '''
        let_var_list : let_var COMMA let_var_list
                     | let_var
        '''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]

        else:
            p[0] = p[1]


    def p_let_var(self, p):
        '''
        let_var : ID COLON TYPE
                | ID COLON TYPE ASSIGN expression
        '''
        if len(p) == 6:
            p[0] = LetVariableNode(id_=p[1], type_=p[3], expression=p[5])
        
        else:
            p[0] = LetVariableNode(id_=p[1], type_=p[3])

        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_case(self, p):
        '''
        expression : CASE expression OF list_case_branch ESAC
        '''
        p[0] = CaseNode(case_expression=p[2], case_branches=p[4])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_list_case_branch(self, p):
        '''
        list_case_branch : case_branch list_case_branch
                         | case_branch
        '''
        if len(p) == 3:
            p[0] = [p[1]] + p[2]

        else:
            p[0] = [p[1]]


    def p_case_branch(self, p):
        '''
        case_branch : ID COLON TYPE ARROW expression SEMICOLON
        '''
        p[0] = CaseBranchNode(id_=p[1], type_=p[3], expression=p[5])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_dispatch(self, p):
        '''
        expression : expression DOT ID LPAREN arguments_list RPAREN
                   | ID LPAREN arguments_list RPAREN
                   | expression AT TYPE DOT ID LPAREN arguments_list RPAREN
        '''         
        if len(p) == 7:
            p[0] = DispatchNode(id_=p[3], expression=p[1], arguments=p[5], type_=None)

        elif len(p) == 9:
            p[0] = DispatchNode(id_=p[5], expression=p[1], arguments=p[7], type_=p[3])

        else:
            p[0] = DispatchNode(id_=p[1], expression=None, arguments=p[3], type_=None)

        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_arguments_list(self, p):
        '''
        arguments_list : expression COMMA arguments_list
                       | expression
        '''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]


    def p_dispatch_empty(self, p):
        '''
        expression : expression DOT ID LPAREN empty RPAREN
                   | ID LPAREN empty RPAREN
                   | expression AT TYPE DOT ID LPAREN empty RPAREN
        '''         
        if len(p) == 7:
            p[0] = DispatchNode(id_=p[3], expression=p[1], arguments=[], type_=None)

        elif len(p) == 9:
            p[0] = DispatchNode(id_=p[5], expression=p[1], arguments=[], type_=p[3])

        else:
            p[0] = DispatchNode(id_=p[1], expression=None, arguments=[], type_=None)

        # p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_atom(self, p):
        '''
        expression : atom
        '''
        p[0] = p[1]

    def p_expression_new(self, p):
        '''
        atom : NEW TYPE
        '''
        p[0] = NewNode(var=p[2])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_is_void(self, p):
        '''
        atom : ISVOID expression
        '''
        p[0] = IsVoidNode(expression=p[2])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_not(self, p):
        '''
        expression : NOT expression
        '''    
        p[0] = NotNode(expression=p[2])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_complement(self, p):
        '''
        expression : COMPL expression
        '''
        p[0] = ComplementNode(expression=p[2])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_plus(self, p):
        '''
        expression : expression PLUS expression
        '''
        p[0] = AdditionNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        

    def p_expression_minus(self, p):
        '''
        expression : expression MINUS expression
        '''
        p[0] = SubtractionNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        

    def p_expression_div(self, p):
        '''expression : expression DIV expression'''
        p[0] = DivisionNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_star(self, p):
        '''
        expression : expression STAR expression
        '''
        p[0] = MultiplicationNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        

    def p_expression_less(self, p):
        '''
        expression : expression LESS expression
        '''
        p[0] = LessNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_lesseq(self, p):
        '''
        expression : expression LESSEQ expression
        '''
        p[0] = LessEqualNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_equals(self, p):
        '''
        expression : expression EQUAL expression
        '''
        p[0] = EqualNode(left=p[1], right=p[3])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        

    def p_expression_parentheses(self, p):
        '''
        expression : LPAREN expression RPAREN
        '''
        p[0] = p[2]

    def p_expression_string(self, p):
        '''
        atom : STRING
        '''
        p[0] = StringNode(p[1])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_variable(self, p):
        '''
        atom : ID 
        '''
        p[0] = VarNode(p[1])
        # p[0].set_position(p.slice[1].line, p.slice[1].col)


    def p_expression_true(self, p):
        '''
        atom : TRUE
        '''
        p[0] = BooleanNode(True)
        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        
        
    def p_expression_false(self, p):
        '''
        atom : FALSE
        '''
        p[0] = BooleanNode(False)
        # p[0].set_position(p.slice[1].line, p.slice[1].col)
        
        
    def p_expression_int(self, p):
        '''
        atom : INT
        '''
        p[0] = IntNode(p[1])
        

    def p_empty(self, p):
        '''
        empty :
        '''
        p[0] = []


    # def p_error(self, t):
    #     if t is None:
    #         self.errors.append(SyntacticError(message='EOF', line=0, column=0))
    #     else:
    #         self.errors.append(SyntacticError(message=t.value, line=t.lineno, column=t.col))

    
    def p_error(self, p):
        if p:
            self.add_error(p)
        else:
            self.errors.append(SyntacticError(message='ERROR at or near EOF', line=0, column=0))

    def add_error(self, p):
        self.errors.append(SyntacticError(
            message=f'ERROR at or near {p.value}', line=p.lineno, column=p.column))


    def print_error(self):
        for error in self.errors:
            print(error.message, 'line ', error.line, 'col ', error.col)
