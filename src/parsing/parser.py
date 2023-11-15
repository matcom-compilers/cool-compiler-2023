from collections import namedtuple
from typing import List, Optional

import parsing.ast as ast
from parsing.lex import Token, TokenType
from utils.loggers import LoggerUtility

log = LoggerUtility().get_logger()


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = iter(
            # Get rid of comments
            filter(
                lambda t: t.type
                not in (TokenType.SINGLE_LINE_COMMENT, TokenType.MULTI_LINE_COMMENT),
                tokens,
            )
        )
        self.current_token = next(self.tokens)
        self.errors = []

    def eat(self, token_type: TokenType):
        if self.current_token:
            log.debug(
                "Eat: ",
                extra={
                    "type": self.current_token.type,
                    "location": self.current_token.position,
                    "value": self.current_token.value,
                },
            )
        if self.current_token.type != token_type:
            self.errors.append(
                f"({self.current_token.position[0]}, {self.current_token.position[1]}) - SyntacticError: ERROR at or near {self.current_token.value}"
            )
            log.debug(
                f"(SyntacticError: ERROR at or near {self.current_token.value}",
                extra={
                    "type": self.current_token.type,
                    "location": self.current_token.position,
                    "value": self.current_token.value,
                },
            )

        self.current_token = next(self.tokens)

    def parse(self):
        try:
            return self.program()
        except StopIteration:
            self.errors.append("Unexpected end of input")

    def program(self) -> ast.ProgramNode:
        """
        program := [[class]]+
        """
        classes = []
        location = ast.Location(*self.current_token.position)
        while self.current_token.type != TokenType.EOF:
            classes.append(self.parse_class())
        return ast.ProgramNode(classes, location)

    def parse_class(self):
        """
        class ::= class TYPE [inherits TYPE] { [[feature; ]]∗}
        """
        self.eat(TokenType.CLASS)
        location = ast.Location(*self.current_token.position)
        class_name = self.current_token.value
        self.eat(TokenType.OBJECTID)

        # Check for inheritance
        parent = None
        if self.current_token.type == TokenType.INHERITS:
            self.eat(TokenType.INHERITS)
            parent = self.current_token.value
            self.eat(TokenType.OBJECTID)

        self.eat(TokenType.OCUR)
        features = []
        while self.current_token.type != TokenType.CCUR:
            features.append(self.parse_feature())
            self.eat(TokenType.SEMICOLON)
        self.eat(TokenType.CCUR)
        self.eat(TokenType.SEMICOLON)
        return ast.ClassNode(class_name, parent, features, location)

    def parse_feature(self):
        """
        Features are attributes and methods
        feature := ID method
                 | ID attribute

                 | ID : TYPE [ <- expr]
        """
        feature_name = self.current_token.value
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.OBJECTID)

        if self.current_token.type == TokenType.OPAR:
            return self.parse_method(feature_name, location)
        else:
            return self.parse_attribute(feature_name, location)

    def parse_method(self, name, location):
        """
        method := ( [ formal [[, formal]]*] ) : TYPE { expr }
        """
        self.eat(TokenType.OPAR)
        formals = self.parse_formals()
        self.eat(TokenType.CPAR)
        self.eat(TokenType.COLON)
        return_type = self.current_token.value
        self.eat(TokenType.OBJECTID)
        self.eat(TokenType.OCUR)
        body = self.parse_expression()
        self.eat(TokenType.CCUR)
        return ast.MethodNode(name, formals, return_type, body, location)

    def parse_attribute(self, name, location):
        self.eat(TokenType.COLON)
        attr_type = self.current_token.value
        self.eat(TokenType.OBJECTID)
        init = None
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            init = self.parse_expression()
        return ast.AttributeNode(
            name,
            attr_type,
            init,
            location,
        )

    def parse_formals(self):
        """
        formals := formal [[, formal]]*

        """
        formals = []
        while self.current_token.type != TokenType.CPAR:
            formals.append(self.parse_formal())
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        return formals

    def parse_formal(self):
        """
        formal
        """
        name = self.current_token.value
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.OBJECTID)
        self.eat(TokenType.COLON)
        formal_type = self.current_token.value
        self.eat(TokenType.OBJECTID)
        return ast.FormalNode(name, formal_type, location)

    def parse_expression(self, left=None, precedence=0):
        """
        expr ::=ID <- expr
            | expr [@TYPE].ID( [ expr [[ , expr ]]∗] )
            | ID( [ expr  [[ , expr ]] ∗] )
            | if expr then expr else expr fi
            | while expr loop expr pool
            | { [[ expr ; ]]+}
            | let ID : TYPE [<-expr] [[,ID : TYPE [<- expr ]]]∗in expr
            | case expr of [[ID : TYPE => expr; ]]+esac
            |new TYPE
            |isvoid expr
            |expr+expr
            |expr− expr
            |expr∗expr
            |expr/expr
            | ̃expr
            |expr<expr
            |expr<=expr
            |expr=expr
            |not expr
            |(expr)
            |ID
            |integer
            |string
            |true
            |false
        """
        if not left:
            if self.current_token.type == TokenType.OBJECTID:
                # Assignment, method call or attribute access
                expr = self.parse_id_expression()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.IF:
                expr = self.parse_if()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.WHILE:
                expr = self.parse_while()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.OCUR:
                expr = self.parse_block()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.LET:
                expr = self.parse_let()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.CASE:
                expr = self.parse_case()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.NEW:
                expr = self.parse_new()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.ISVOID:
                expr = self.parse_isvoid()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.TILDE:
                expr = self.parse_negate()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.INT_CONST:
                expr = self.parse_integer()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.STRING_CONST:
                expr = self.parse_string()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.TRUE:
                expr = self.parse_true()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.FALSE:
                expr = self.parse_false()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.NOT:
                expr = self.parse_not()
                return self.parse_expression(left=expr)
            elif self.current_token.type == TokenType.OPAR:
                self.eat(TokenType.OPAR)
                expr = self.parse_expression()
                self.eat(TokenType.CPAR)
                return self.parse_expression(left=expr)

            else:
                self.errors.append(
                    f"({self.current_token.position[0]}, {self.current_token.position[1]}) - SyntacticError: ERROR at or near {self.current_token.value}"
                )
                self.eat(self.current_token.type)
        else:
            if self.current_token.type in (TokenType.AT, TokenType.DOT):
                expr = self.parse_attribute_access(left)
                return self.parse_expression(left=expr)
            else:
                return self.parse_binary_operation(left)

    def parse_id_expression(self):
        """
        ID <- expr
        ID( [ expr  [[ , expr ]] *] )
        ID
        """
        name = self.current_token.value
        location = ast.Location(*self.current_token.position)

        if name[0].isupper():
            self.errors.append(
                f"({location[0]}, {location[1]}) - SyntacticError: ERROR at or near {name}"
            )

        self.eat(TokenType.OBJECTID)

        if self.current_token.type == TokenType.ASSIGN:  # ID <- expr
            return self.parse_assign(name, location)
        elif self.current_token.type == TokenType.OPAR:  # ID( [ expr  [[ , expr ]] *] )
            return self.parse_method_call(name, location)
        else:  # ID
            return ast.IdentifierNode(name, location)

    def parse_assign(self, name, location):
        """
        ID <- expr
        """

        self.eat(TokenType.ASSIGN)
        expr = self.parse_expression()
        return ast.AssignNode(name, expr, location)

    def parse_method_call(self, name, location):
        """
        ID( [ expr  [[ , expr ]] *] )
        """
        self.eat(TokenType.OPAR)
        arguments = self.parse_arguments()
        return ast.MethodCallNode(name, arguments, location)

    def parse_arguments(self):
        """
        [ expr  [[ , expr ]] *]
        """
        arguments = []
        while True:
            if self.current_token.type == TokenType.CPAR:
                break
            arguments.append(self.parse_expression())
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                if self.current_token.type == TokenType.CPAR:
                    self.errors.append(
                        f'({self.current_token.position.line}, {self.current_token.position.column}) - SyntacticError: ERROR at or near "{self.current_token.value}\nExtra comma on arguments"'
                    )
                    log.debug(
                        f"(SyntacticError: ERROR at or near {self.current_token.value}",
                        extra={
                            "type": self.current_token.type,
                            "location": self.current_token.position,
                            "value": self.current_token.value,
                        },
                    )
                continue
            else:
                break

        self.eat(TokenType.CPAR)
        return arguments

    def parse_if(self):
        """
        if expr then expr else expr fi
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.IF)
        condition = self.parse_expression()
        self.eat(TokenType.THEN)
        then_expr = self.parse_expression()
        self.eat(TokenType.ELSE)
        else_expr = self.parse_expression()
        self.eat(TokenType.FI)
        return ast.IfNode(condition, then_expr, else_expr, location)

    def parse_while(self):
        """
        while expr loop expr pool
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.WHILE)
        condition = self.parse_expression()
        self.eat(TokenType.LOOP)
        body = self.parse_expression()
        self.eat(TokenType.POOL)
        return ast.WhileNode(condition, body, location)

    def parse_block(self):
        """
        { [[ expr ; ]]+}
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.OCUR)
        expressions = []
        while self.current_token.type != TokenType.CCUR:
            expressions.append(self.parse_expression())
            self.eat(TokenType.SEMICOLON)

        self.eat(TokenType.CCUR)
        return ast.BlockNode(expressions, location)

    def parse_let(self):
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.LET)
        bindings = []
        while True:
            var_name = self.current_token.value

            if var_name[0].isupper():
                error_location = self.current_token.position
                self.errors.append(
                    f"({error_location[0]}, {error_location[1]}) - SyntacticError: ERROR at or near {var_name}:\nObject identifiers starts with a lowercase letter"
                )

            self.eat(TokenType.OBJECTID)
            self.eat(TokenType.COLON)
            var_type = self.current_token.value

            if var_type[0].islower():
                error_location = self.current_token.position
                self.errors.append(
                    f"({error_location[0]}, {error_location[1]}) - SyntacticError: ERROR at or near {var_name}:\nType identifiers starts with a uppercase letter "
                )

            self.eat(TokenType.OBJECTID)

            init_expr = None
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                init_expr = self.parse_expression()
            bindings.append((var_name, var_type, init_expr))

            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                continue
            else:
                break

        self.eat(TokenType.IN)
        body = self.parse_expression()
        return ast.LetNode(bindings, body, location)

    def parse_case(self):
        """
        case expr of [[ID : TYPE => expr; ]]+esac
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.CASE)
        expr = self.parse_expression()
        self.eat(TokenType.OF)
        branches = []
        while self.current_token.type != TokenType.ESAC:
            branches.append(self.parse_branch())
            self.eat(TokenType.SEMICOLON)
        self.eat(TokenType.ESAC)
        return ast.CaseNode(expr, branches, location)

    def parse_branch(self):
        """
        ID : TYPE => expr
        """
        location = ast.Location(*self.current_token.position)
        identifier = self.current_token.value
        self.eat(TokenType.OBJECTID)
        self.eat(TokenType.COLON)
        formal_type = self.current_token.value
        self.eat(TokenType.OBJECTID)
        self.eat(TokenType.DARROW)
        expr = self.parse_expression()
        return ast.CaseOptionNode(identifier, formal_type, expr, location)

    def parse_new(self):
        """
        new TYPE
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.NEW)
        new_type = self.current_token.value
        self.eat(TokenType.OBJECTID)
        return ast.NewNode(new_type, location)

    def parse_isvoid(self):
        """
        isvoid expr
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.ISVOID)
        expr = self.parse_expression()
        return ast.IsVoidNode(expr, location)

    def parse_negate(self):
        """
        ~expr
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.TILDE)
        expr = self.parse_expression()
        return ast.NotNode(expr, location)

    def parse_not(self):
        """
        not expr
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.NOT)
        expr = self.parse_expression()
        return ast.NotNode(expr, location)

    def parse_integer(self):
        """
        integer
        """
        location = ast.Location(*self.current_token.position)
        value = self.current_token.value
        self.eat(TokenType.INT_CONST)
        return ast.IntegerNode(value, location)

    def parse_string(self):
        """
        string
        """
        location = ast.Location(*self.current_token.position)
        value = self.current_token.value
        self.eat(TokenType.STRING_CONST)
        return ast.StringNode(value, location)

    def parse_true(self):
        """
        true
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.TRUE)
        return ast.BooleanNode(True, location)

    def parse_false(self):
        """
        false
        """
        location = ast.Location(*self.current_token.position)
        self.eat(TokenType.FALSE)
        return ast.BooleanNode(False, location)

    def parse_attribute_access(self, left):
        """
        expr[@TYPE].ID( [ expr [[ , expr ]]∗] )
        """
        location = ast.Location(*self.current_token.position)
        obj_type = None
        if self.current_token.type == TokenType.AT:
            self.eat(TokenType.AT)
            obj_type = self.current_token.value
            self.eat(TokenType.OBJECTID)
        self.eat(TokenType.DOT)
        method = self.current_token.value
        self.eat(TokenType.OBJECTID)
        self.eat(TokenType.OPAR)
        arguments = self.parse_arguments()
        return ast.DispatchNode(left, method, arguments, location, obj_type)

    def parse_binary_operation(self, left):
        """
        expr+expr
        expr− expr
        expr∗expr
        expr/expr
        expr<expr
        expr<=expr
        expr=expr
        """
        location = ast.Location(*self.current_token.position)
        if self.current_token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(
                ast.BinaryOperator.PLUS, left, right, location
            )
        elif self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(
                ast.BinaryOperator.MINUS, left, right, location
            )
        elif self.current_token.type == TokenType.STAR:
            self.eat(TokenType.STAR)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(
                ast.BinaryOperator.TIMES, left, right, location
            )
        elif self.current_token.type == TokenType.DIV:
            self.eat(TokenType.DIV)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(
                ast.BinaryOperator.DIVIDE, left, right, location
            )
        elif self.current_token.type == TokenType.LOWER:
            self.eat(TokenType.LOWER)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(ast.BinaryOperator.LT, left, right, location)
        elif self.current_token.type == TokenType.LEQ:
            self.eat(TokenType.LEQ)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(ast.BinaryOperator.LE, left, right, location)
        elif self.current_token.type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)
            right = self.parse_expression()
            return ast.BinaryOperatorNode(ast.BinaryOperator.EQ, left, right, location)
        else:
            return left
