from parsing.ast import ClassNode, ProgramNode
from utils.loggers import LoggerUtility
from utils.visitor import Visitor

from .context import Context
from .types import (
    BoolType,
    IntType,
    IOType,
    ObjectType,
    SelfType,
    SemanticError,
    StringType,
    Type,
)

log = LoggerUtility().get_logger()


def define_builtin_types(context: Context):
    """
    Defines built-in types for COOL
    """
    object_type = context.types["Object"] = ObjectType()
    io_type = context.types["IO"] = IOType()
    int_type = context.types["Int"] = IntType()
    string_type = context.types["String"] = StringType()
    bool_type = context.types["Bool"] = BoolType()
    self_type = context.types["SELF_TYPE"] = SelfType()

    object_type.define_method("abort", [], [], object_type, (0, 0))
    object_type.define_method("type_name", [], [], string_type, (0, 0))
    object_type.define_method("copy", [], [], self_type, (0, 0))

    int_type.set_parent(object_type)

    string_type.set_parent(object_type)
    string_type.define_method("length", [], [], int_type, (0, 0))
    string_type.define_method("concat", ["s"], [string_type], string_type, (0, 0))
    string_type.define_method(
        "substr", ["i", "l"], [int_type, int_type], string_type, (0, 0)
    )

    bool_type.set_parent(object_type)

    io_type.set_parent(object_type)
    io_type.define_method("out_string", ["x"], [string_type], self_type, (0, 0))
    io_type.define_method("out_int", ["x"], [int_type], self_type, (0, 0))
    io_type.define_method("in_string", [], [], string_type, (0, 0))
    io_type.define_method("in_int", [], [], int_type, (0, 0))


class TypeCollector(Visitor):
    def __init__(self) -> None:
        self.context = None
        self.errors = []

    def error(self, message, location, type, value):
        self.errors.append(f"({location[0]}, {location[1]}) - SemanticError: {message}")
        log.debug(
            f"(SemanticError: {message}",
            extra={"type": type, "location": location, "value": value},
        )

    def visit__ProgramNode(self, node: ProgramNode):
        """
        Define builtins and extract types from Clasess
        """
        self.context = Context()

        define_builtin_types(self.context)

        for cls in node.classes:
            cls.accept(self)

        # Class Main should be defined
        if not self.context.type_exists("Main"):
            self.error(
                f"Main class must exists in a valid COOL program",
                (0, 0),
                "Main",
                "Main",
            )

    def visit__ClassNode(self, node: ClassNode):
        """
        Add new types or error
        """
        assert self.context is not None

        if self.context.type_exists(node.name):
            if Type.is_builtin_type(node.name):
                self.error(
                    f"Redefinition of built in type {node.name} is not allowed",
                    node.location,
                    node.__class__.__name__,
                    node.name,
                )
            else:
                defined_type = self.context.get_type(node.name)

                self.error(
                    f"Classes may not be redefined. {node.name} was first defined at {defined_type.defined_location}",
                    node.location,
                    node.__class__.__name__,
                    node.name,
                )
        else:
            self.context.create_type(node.name)
