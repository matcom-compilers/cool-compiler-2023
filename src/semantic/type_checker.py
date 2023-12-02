from parsing.ast import (
    AssignNode,
    AttributeNode,
    BinaryOperator,
    BinaryOperatorNode,
    BlockNode,
    BooleanNode,
    CaseNode,
    CaseOptionNode,
    ClassNode,
    DispatchNode,
    IdentifierNode,
    IfNode,
    IntegerNode,
    IsVoidNode,
    LetNode,
    MethodCallNode,
    MethodNode,
    NewNode,
    NotNode,
    PrimeNode,
    ProgramNode,
    StringNode,
    WhileNode,
)
from semantic.context import Context
from semantic.scope import Scope
from semantic.types import (
    BoolType,
    ErrorType,
    IntType,
    ObjectType,
    SelfType,
    StringType,
    Type,
)
from utils.loggers import LoggerUtility
from utils.visitor import Visitor

log = LoggerUtility().get_logger()


class TypeChecker(Visitor):
    def __init__(self, context: Context, errors=None) -> None:
        super().__init__()
        self.context = context
        self.errors = errors if errors else []
        self.current_type = None
        self.current_method = None

    def error(self, message, location, type, value):
        self.errors.append(f"({location[0]}, {location[1]}) - {message}")
        log.debug(
            message,
            extra={"type": type, "location": location, "value": value},
        )

    def visit__ProgramNode(self, node: ProgramNode, scope=None):
        scope = scope if scope else Scope()
        for cls in node.classes:
            cls.accept(self, scope=scope.create_child(cls.name))
        return scope

    def visit__ClassNode(self, node: ClassNode, scope: Scope):
        self.current_type = self.context.get_type(node.name)
        scope.define_variable("self", self.current_type)

        for feature in node.features:
            feature.accept(self, scope=scope)

    def visit__AttributeNode(self, node: AttributeNode, scope: Scope):
        assert self.current_type
        if node.name == "self":
            self.error(
                f"SemanticError: Attribute name cannot be self",
                node.location,
                "Attribute",
                "self",
            )

        attr_type = self.current_type.get_attribute(node.name).type
        if attr_type == SelfType():
            attr_type = self.current_type

        if node.init:
            expr_type = node.init.accept(self, scope=scope)
            if expr_type == SelfType():
                expr_type = self.current_type

            if not expr_type.conforms_to(attr_type):
                self.error(
                    f"TypeError: Inferred type {expr_type.name} of initialization of attribute {node.name} does not conform to declared type {attr_type.name}.",
                    location=node.location,
                    type="Attribute",
                    value=expr_type,
                )

        scope.define_variable(node.name, attr_type)

    def visit__MethodNode(self, node: MethodNode, scope: Scope):
        assert self.current_type
        self.current_method = self.current_type.get_method(node.name)
        child_scope = scope.create_child(scope.class_name, self.current_method.name)

        index = 0
        for param_name, param_type in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            if param_name != "self":
                child_scope.define_variable(param_name, param_type)
            else:
                self.error(
                    "SemanticError: self can not be the name of a formal parameter",
                    location=node.location,
                    type="InvalidFormal",
                    value=f"{param_name} : {param_type}",
                )
            index += 1

        return_type_exp = node.body.accept(self, scope=child_scope)

        return_type_exp = (
            return_type_exp if return_type_exp != SelfType() else self.current_type
        )
        return_type_met = (
            self.current_method.return_type
            if self.current_method.return_type != SelfType()
            else self.current_type
        )

        if not return_type_exp.conforms_to(return_type_met):
            self.error(
                f"TypeError: Inferred return type {return_type_exp.name} of method {node.name} does not conform to declared return type {return_type_met.name}",
                location=node.location,
                type="Method",
                value=node.name,
            )

    def visit__AssignNode(self, node: AssignNode, scope: Scope):
        assert self.current_type
        assig_type = node.expr.accept(self, scope=scope)
        assig_type = assig_type if assig_type != SelfType() else self.current_type

        if node.name == "self":
            self.error(
                "SemanticError: 'self' is readonly",
                location=node.location,
                type="Assignment",
                value=f"{node.name}:{assig_type.name}",
            )

        scope.define_variable(node.name, assig_type)
        node.computed_type = assig_type.name
        return assig_type

    def visit__DispatchNode(self, node: DispatchNode, scope: Scope):
        assert self.current_type
        obj_type: Type = node.expr.accept(self, scope=scope)
        method_name = node.method

        if node.method_type:
            if not self.context.type_exists(node.method_type):
                self.error(
                    f"TypeError: Type {node.method_type} is not defined",
                    location=node.location,
                    type="StaticDispatch",
                    value=f"{node.method_type}",
                )
                static_type = ErrorType()
            else:
                static_type = self.context.get_type(node.method_type)

            if not obj_type.conforms_to(static_type):
                self.error(
                    f"TypeError: Expression type {obj_type.name} does not conform to declared static dispatch type {static_type.name}. ",
                    location=node.location,
                    type="StaticDispatch",
                    value=f"{node.method_type}",
                )
                obj_type = ErrorType()
            else:
                obj_type = static_type

        if obj_type == SelfType():
            obj_type = self.current_type

        if obj_type == ErrorType():
            return ErrorType()

        if not obj_type.is_method_defined(method_name):
            self.error(
                f"AttributeError: Method '{method_name}' is not defined in type '{obj_type.name}'",
                location=node.location,
                type="Dispatch",
                value=f"{method_name}",
            )
            return ErrorType()

        method = obj_type.get_method(method_name)

        if len(node.args) != len(method.param_names):
            self.error(
                f"SemanticError: Number of arguments in dispatch does not match number of parameters in method '{method_name}'",
                location=node.location,
                type="Dispatch",
                value=f"{method_name}",
            )

        for arg, param_type in zip(node.args, method.param_types):
            arg_type = arg.accept(self, scope=scope)

            if arg_type == SelfType():
                arg_type = self.current_type

            if not param_type.conforms_to(arg_type):
                self.error(
                    f"TypeError: Type mismatch in argument of method '{method_name}'. Expected type '{param_type.name}', found type '{arg_type.name}'",
                    location=node.location,
                    type="Dispatch",
                    value=f"{method_name}",
                )

        return_type = (
            method.return_type if method.return_type != SelfType() else obj_type
        )
        node.computed_type = return_type.name
        return return_type

    def visit__BinaryOperatorNode(self, node: BinaryOperatorNode, scope: Scope):
        left_type = node.left.accept(self, scope=scope)
        right_type = node.right.accept(self, scope=scope)

        node.left.computed_type = node.left.computed_type
        node.right.computed_type = node.right.computed_type

        operator = node.operator

        if operator in [
            BinaryOperator.PLUS,
            BinaryOperator.MINUS,
            BinaryOperator.TIMES,
            BinaryOperator.DIVIDE,
        ]:
            if left_type != IntType() or right_type != IntType():
                self.error(
                    f"TypeError: Invalid types for binary operator '{operator.value}'",
                    location=node.location,
                    type="BinaryOperator",
                    value=f"{left_type.name} {operator} {right_type.name}",
                )
                return ErrorType()
            return IntType()

        elif operator in [
            BinaryOperator.EQ,
        ]:
            if (
                left_type in [IntType(), BoolType(), StringType()]
                and right_type != left_type
            ) or (
                right_type in [IntType(), BoolType(), StringType()]
                and left_type != right_type
            ):
                self.error(
                    f"TypeError: Illegal comparison with a basic type. Can't compare {left_type.name} and {right_type.name}",
                    location=node.location,
                    type="BinaryOperator",
                    value=f"{left_type.name} {operator} {right_type.name}",
                )
                return ErrorType()
            return BoolType()

        elif operator in [
            BinaryOperator.LT,
            BinaryOperator.LE,
        ]:
            if left_type != IntType() or right_type != IntType():
                self.error(
                    f"TypeError: non-Int arguments: {left_type.name} {operator.value} {right_type.name}",
                    location=node.location,
                    type="BinaryOperator",
                    value=f"{left_type.name} {operator} {right_type.name}",
                )
                return ErrorType()
            return BoolType()

        elif operator in ["and", "or"]:
            if left_type != BoolType() or right_type != BoolType():
                self.error(
                    f"TypeError: Invalid types for binary operator '{operator.value}'",
                    location=node.location,
                    type="BinaryOperator",
                    value=f"{left_type.name} {operator} {right_type.name}",
                )
                return ErrorType()
            return BoolType()

        else:
            self.error(
                f"TypeError: Unknown binary operator '{operator}'",
                location=node.location,
                type="BinaryOperator",
                value=operator,
            )
            return ErrorType()

    def visit__UnaryOperatorNode(self, node, scope):
        return SelfType()

    def visit__IfNode(self, node: IfNode, scope: Scope):
        predicate_type: Type = node.condition.accept(self, scope=scope)
        if not isinstance(predicate_type, BoolType):
            self.error(
                f"TypeError: Predicate expression type {predicate_type.name} is not Bool",
                location=node.condition.location,
                type="If",
                value=predicate_type.name,
            )

        then_type: Type = node.then_expr.accept(self, scope=scope)
        else_type: Type = node.else_expr.accept(self, scope=scope)

        node_type = Type.find_parent_type(then_type, else_type, self.current_type)
        node.computed_type = node_type.name
        return node_type

    def visit__BlockNode(self, node: BlockNode, scope: Scope):
        block_type = ErrorType()
        for expr in node.expressions:
            block_type = expr.accept(self, scope=scope)
        node.computed_type = block_type.name
        return block_type

    def visit__LetNode(self, node: LetNode, scope: Scope):
        let_scope = scope.create_child(
            scope.class_name, scope.method_name
        )  # Create a new scope for the let expression
        for var_name, var_type, init_expr, location in node.bindings:
            if var_name == "self":
                self.error(
                    f"SemanticError: 'self' cannot be bound in a 'let' expression.",
                    location=location,
                    type="Let",
                    value=var_type,
                )
                continue

            if not self.context.type_exists(var_type):
                self.error(
                    f"TypeError: Class {var_type} of let-bound identifier {var_name} is undefined.",
                    location=location,
                    type="Let",
                    value=var_type,
                )
                continue
            else:
                var_type = self.context.get_type(var_type)
            if init_expr is not None:
                init_type: Type = init_expr.accept(
                    self, scope=let_scope
                )  # Evaluate the initialization expression
                if not init_type.conforms_to(var_type):
                    self.error(
                        f"TypeError: Initialization expression type {init_type.name} does not conform to declared type {var_type.name}",
                        location=location,
                        type="Let",
                        value=var_name,
                    )

            let_scope.define_variable(var_name, var_type)

        node_type = node.body.accept(
            self, scope=let_scope
        )  # Evaluate the body expression and return its type
        node.computed_type = node_type.name
        return node_type

    def visit__CaseNode(self, node: CaseNode, scope: Scope):
        case_expr_type = node.expr.accept(self, scope=scope)
        case_types = []
        case_types_set = set()

        for case in node.cases:
            case_type = case.accept(self, scope=scope)
            if case.type in case_types_set:
                self.error(
                    f"SemanticError: Duplicate branch {case_type.name} in case statement.",
                    location=case.location,
                    type="Case",
                    value=case.type,
                )
            else:
                case_types_set.add(case.type)
                case_types.append(case_type)

        case_type = case_types[0]
        for c_type in case_types[1:]:
            case_type = Type.find_parent_type(case_type, c_type, self.current_type)

        node.computed_type = case_type.name
        return case_type

    def visit__CaseOptionNode(self, node: CaseOptionNode, scope: Scope):
        if not self.context.type_exists(node.type):
            self.error(
                f"TypeError: Type {node.type} of case branch is undefined",
                location=node.location,
                type="CaseOptionNode",
                value=node.type,
            )
            case_type = ErrorType()
        else:
            case_type = self.context.get_type(node.type)

        case_scope = scope.create_child(scope.class_name, scope.method_name)
        case_scope.define_variable(node.name, case_type)
        return node.expr.accept(self, scope=case_scope)

    def visit__NewNode(self, node: NewNode, scope: Scope):
        if not self.context.type_exists(node.type):
            self.error(
                f"TypeError: Type {node.type} does not exist",
                location=node.location,
                type="New",
                value=node.type,
            )
            return ErrorType()
        node.computed_type = node.type
        return self.context.get_type(node.type)

    def visit__IsVoidNode(self, node: IsVoidNode, scope: Scope):
        node.computed_type = "Bool"
        return self.context.get_type("Bool")

    def visit__NotNode(self, node: NotNode, scope: Scope):
        expr_type: Type = node.expr.accept(self, scope=scope)

        if expr_type == BoolType():
            node.computed_type = "Bool"
            return expr_type

        self.error(
            f"TypeError: Invalid type of expresión {str(node.expr)} for 'not' operator",
            location=node.expr.location,
            type="NotNode",
            value=expr_type.name,
        )
        return ErrorType()

    def visit__PrimeNode(self, node: PrimeNode, scope: Scope):
        expr_type: Type = node.expr.accept(self, scope=scope)

        if expr_type == IntType():
            node.computed_type = "Int"
            return expr_type

        self.error(
            f"TypeError: Invalid type of expresión {str(node.expr)} for '~' operator",
            location=node.expr.location,
            type="NotNode",
            value=expr_type.name,
        )
        return ErrorType()

    def visit__IdentifierNode(self, node: IdentifierNode, scope: Scope):
        assert self.current_type
        if scope.is_defined(node.name, self.current_type):
            var_or_attr = scope.find_variable_or_attribute(node.name, self.current_type)
            node.type = var_or_attr.type if var_or_attr else ErrorType()
            node.computed_type = node.type.name
            return node.type
        else:
            self.error(
                f"NameError: Identifier {node.name} is not defined in current scope",
                location=node.location,
                type="IdentifierNode",
                value=node.name,
            )
            return ErrorType()

    def visit__IntegerNode(self, node: IntegerNode, scope: Scope):
        node.computed_type = self.context.get_type("Int").name
        return self.context.get_type("Int")

    def visit__StringNode(self, node: StringNode, scope: Scope):
        node.computed_type = self.context.get_type("String").name
        return self.context.get_type("String")

    def visit__BooleanNode(self, node: BooleanNode, scope: Scope):
        node.computed_type = self.context.get_type("Bool").name
        return self.context.get_type("Bool")

    def visit__MethodCallNode(self, node: MethodCallNode, scope: Scope):
        assert self.current_type

        method_name = node.method
        obj_type = self.current_type

        if obj_type == ErrorType():
            return ErrorType()

        if not obj_type.is_method_defined(method_name):
            self.error(
                f"AttributeError: Method '{method_name}' is not defined in type '{obj_type.name}'",
                location=node.location,
                type="Dispatch",
                value=f"{method_name}",
            )
            return ErrorType()

        method = obj_type.get_method(method_name)

        if len(node.args) != len(method.param_names):
            self.error(
                f"SemanticError: Number of arguments in dispatch does not match number of parameters in method '{method_name}'",
                location=node.location,
                type="Dispatch",
                value=f"{method_name}",
            )

        for arg, param_type in zip(node.args, method.param_types):
            arg_type = arg.accept(self, scope=scope)

            if arg_type == SelfType():
                arg_type = self.current_type

            if not param_type.conforms_to(arg_type):
                self.error(
                    f"TypeError: Type mismatch in argument of method '{method_name}'. Expected type '{param_type.name}', found type '{arg_type.name}'",
                    location=node.location,
                    type="Dispatch",
                    value=f"{method_name}",
                )

        return_type = (
            method.return_type if method.return_type != SelfType() else obj_type
        )
        node.computed_type = return_type.name
        return return_type

    def visit__WhileNode(self, node: WhileNode, scope: Scope):
        condition_type: Type = node.condition.accept(self, scope)

        if condition_type.conforms_to(BoolType()):
            return self.context.get_type("Object")
        else:
            self.error(
                f"TypeError: Loop condition does not have type Bool.",
                location=node.location,
                type="Dispatch",
                value=condition_type.name,
            )
            return ErrorType()
