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
        pass

    def visit__MethodNode(self, node: MethodNode):
        pass
