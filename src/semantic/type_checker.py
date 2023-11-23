from parsing.ast import AttributeNode, ClassNode, MethodNode, NewNode, ProgramNode
from semantic.context import Context
from semantic.scope import Scope
from semantic.types import ErrorType, SelfType
from utils.loggers import LoggerUtility
from utils.visitor import Visitor

log = LoggerUtility().get_logger()


class TypeChecker(Visitor):
    def __init__(self, context: Context, errors=None) -> None:
        super().__init__()
        self.context = context
        self.errors = errors if errors else []

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

    def visit__AssignNode(self, node, scope):
        return SelfType()

    def visit__DispatchNode(self, node, scope):
        return SelfType()

    def visit__BinaryOperatorNode(self, node, scope):
        return SelfType()

    def visit__UnaryOperatorNode(self, node, scope):
        return SelfType()

    def visit__IfNode(self, node, scope):
        return SelfType()

    def visit__WhileNode(self, node, scope):
        return SelfType()

    def visit__BlockNode(self, node, scope):
        return SelfType()

    def visit__LetNode(self, node, scope):
        return SelfType()

    def visit__CaseNode(self, node, scope):
        return SelfType()

    def visit__CaseOptionNode(self, node, scope):
        return SelfType()

    def visit__NewNode(self, node: NewNode, scope: Scope):
        if not self.context.type_exists(node.type):
            self.error(
                f"SemanticError: Type {node.type} does not exist",
                location=node.location,
                type="New",
                value=node.type,
            )
            return ErrorType()

        return self.context.get_type(node.type)

    def visit__IsVoidNode(self, node, scope):
        return SelfType()

    def visit__NotNode(self, node, scope):
        return SelfType()

    def visit__IdentifierNode(self, node, scope):
        return SelfType()

    def visit__IntegerNode(self, node, scope):
        return SelfType()

    def visit__StringNode(self, node, scope):
        return SelfType()

    def visit__BooleanNode(self, node, scope):
        return SelfType()

    def visit__MethodCallNode(self, node, scope):
        return SelfType()
