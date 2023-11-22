from parsing.ast import AttributeNode, ClassNode, MethodNode, ProgramNode
from semantic.context import Context
from semantic.types import (
    BoolType,
    IntType,
    ObjectType,
    SelfType,
    SemanticError,
    StringType,
)
from utils.loggers import LoggerUtility
from utils.visitor import Visitor

log = LoggerUtility().get_logger()


class TypeBuilder(Visitor):
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

    def visit__ProgramNode(self, node: ProgramNode):
        for cls in node.classes:
            cls.accept(self)

        main_type = self.context.get_type("Main")

        try:
            main_type.get_method("main")
        except SemanticError:
            self.error(
                "Method main must be defined in Main class", (0, 0), "main", "main"
            )

    def visit__ClassNode(self, node: ClassNode):
        self.current_type = self.context.get_type(node.name)

        # If not explicit inherits then parent class is Object
        parent = self.context.get_type("Object")
        if node.parent is not None:
            if not self.context.type_exists(node.parent):
                self.error(
                    f"TypeError: Class {node.name} inhertits from an undefined class {node.parent}.",
                    node.location,
                    "Inheritance",
                    f"{node.name} > {node.parent}",
                )

            else:
                parent = self.context.get_type(node.parent)
                if (
                    parent == BoolType()
                    or parent == IntType()
                    or parent == StringType()
                    or parent == SelfType()
                ):
                    self.error(
                        f"SemanticError: Class {node.name} can not inherit from built in class {parent.name}.",
                        node.location,
                        "Inheritance",
                        f"{node.name} > {node.parent}",
                    )
                elif parent.name == "Main":
                    self.error(
                        f"SemanticError: Class {parent.name} is not inheritable.",
                        node.location,
                        "Inheritance",
                        f"{parent.name}",
                    )

            if parent.conforms_to(self.current_type):
                self.error(
                    f"SemanticError: Class {node.name}, or an ancestor of {node.name}, is involved in an inheritance cycle.",
                    node.location,
                    "Cyclical inheritance",
                    node.parent,
                )

        if self.current_type != ObjectType():
            self.current_type.set_parent(parent)

        for feature in node.features:
            self.visit(feature)

    def visit__AttributeNode(self, node: AttributeNode):
        if not self.context.type_exists(node.attr_type):
            self.error(
                f"TypeError: Type {node.attr_type} of attribute {node.name} is undefined.",
                node.location,
                "AttributeNode",
                node.attr_type,
            )
            return

        if self.current_type.is_attribute_defined(node.name):
            attr = self.current_type.get_attribute(node.name)
            attr_parent = self.current_type.get_attribute_parent(node.name)
            if attr_parent == self.current_type:
                self.error(
                    f"SemanticError: Redefinition of parent class {attr_parent.name} attribute {node.name}.\nFirst defined at ({attr.location[0], attr.location[1]})",
                    node.location,
                    "AttributeNode",
                    node.attr_type,
                )
            else:
                self.error(
                    f"SemanticError: Attribute {node.name} is multiple defined.\nFirst defined at ({attr.location[0], attr.location[1]})",
                    node.location,
                    "AttributeNode",
                    node.attr_type,
                )
            return

        attr_type = self.context.get_type(node.attr_type)
        self.current_type.define_attribute(node.name, attr_type, node.location)

    def visit__MethodNode(self, node: MethodNode):
        if self.current_type.is_method_defined(node.name):
            method = self.current_type.get_method(node.name)
            method_parent = self.current_type.get_method_parent(node.name)
            if method_parent == self.current_type:
                self.error(
                    f"SemanticError: Redefinition of parent class {method_parent.name} method {node.name}.\nFirst defined at ({method.location[0], method.location[1]})",
                    node.location,
                    "MethodNode",
                    node.name,
                )
            else:
                self.error(
                    f"SemanticError: Method {node.name} is multiple defined.\nFirst defined at ({method.location[0], method.location[1]})",
                    node.location,
                    "MethodNode",
                    node.name,
                )
            return

        param_types = []
        param_names = []
        for param in node.formals:
            if not self.context.type_exists(param.formal_type):
                self.error(
                    f"TypeError: Type {param.formal_type} of parameter {param.name} is undefined.",
                    param.location,
                    "MethodNode",
                    param.name,
                )
                return
            param_type = self.context.get_type(param.formal_type)
            param_types.append(param_type)
            param_names.append(param.name)

        return_type = None
        if node.return_type:
            if not self.context.type_exists(node.return_type):
                self.error(
                    f"TypeError: Type {node.return_type} of method {node.name} return value is undefined.",
                    node.location,
                    "MethodNode",
                    node.name,
                )
                return
            return_type = self.context.get_type(node.return_type)

        self.current_type.define_method(
            node.name, param_names, param_types, return_type, node.location
        )
