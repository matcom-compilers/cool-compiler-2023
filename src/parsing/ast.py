from collections import namedtuple
from enum import Enum
from typing import List, Optional

from parsing.lex import TokenType
from semantic.types import BoolType, IntType, StringType, Type
from utils.loggers import LoggerUtility
from utils.visitor import Visitor

log = LoggerUtility().get_logger()

Location = namedtuple("Location", ["line", "column"])

Location.__str__ = lambda self: f"Ln {self.line}, Col {self.column}"  # type: ignore


class Node:
    def __init__(self, location):
        self.location = location
        log.debug(
            "Created Node: ",
            extra={
                "location": location,
                "type": type(self).__name__,
                "value": str(self),
            },
        )

    def value(self):
        return ""

    def accept(self, visitor: Visitor, *args, **kwargs):
        log.debug(
            f"Visitor {visitor.__class__.__name__} on {type(self).__name__}",
            extra={
                "location": self.location,
                "type": type(self).__name__,
                "value": visitor.__class__.__name__,
            },
        )
        return visitor.visit(self, *args, **kwargs)


class ProgramNode(Node):
    def __init__(self, classes, location):
        self.classes: List[ClassNode] = classes
        super().__init__(location)

    def __str__(self) -> str:
        return "\n".join(str(c) for c in self.classes)


class ClassNode(Node):
    def __init__(self, name: str, parent: str, features: List["FeatureNode"], location):
        self.name = name
        self.parent = parent
        self.features = features
        super().__init__(location)

    def __str__(self) -> str:
        s = f"class {self.name} "
        if self.parent:
            s += f"inherits {self.parent}"
        s += "{\n"
        for feature in self.features:
            s += str(feature)
        s += "\n};"
        return s


class FeatureNode(Node):
    def __init__(self, location):
        super().__init__(location)


class MethodNode(FeatureNode):
    def __init__(
        self,
        name,
        formals: List["FormalNode"],
        return_type,
        body: "ExpressionNode",
        location,
    ):
        self.name = name
        self.formals = formals
        self.return_type = return_type
        self.body = body
        super().__init__(location)

    def __str__(self) -> str:
        s = f"    {self.name}("
        for formal in self.formals:
            s += f"{formal.name}: {formal.formal_type},"
        if len(self.formals):
            s = s[:-1]
        s += f"): {self.return_type} "
        s += "{\n\t"
        s += str(self.body)
        s += "\n\t};\n"
        return s


class AttributeNode(FeatureNode):
    def __init__(self, name, attr_type, init: "ExpressionNode", location):
        super().__init__(location)
        self.name = name
        self.attr_type = attr_type
        self.init = init


class FormalNode(Node):
    def __init__(self, name, formal_type, location):
        super().__init__(location)
        self.name = name
        self.formal_type = formal_type


class ExpressionNode(Node):
    def __init__(self, location, type: Optional[Type] = None):
        self.type = type
        super().__init__(location)


class AssignNode(ExpressionNode):
    def __init__(self, name, expr: ExpressionNode, location):
        super().__init__(location)
        self.name = name
        self.expr = expr


class DispatchNode(ExpressionNode):
    def __init__(
        self,
        expr: ExpressionNode,
        method,
        args: List[ExpressionNode],
        location,
        method_type=None,
    ):
        super().__init__(location)
        self.expr = expr
        self.method = method
        self.args = args
        self.method_type = method_type


class BinaryOperator(Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"
    LT = "<"
    LE = "<="
    EQ = "="
    GT = ">"
    GE = ">="


class BinaryOperatorNode(ExpressionNode):
    def __init__(
        self,
        operator: BinaryOperator,
        left: ExpressionNode,
        right: ExpressionNode,
        location: Location,
    ):
        self.operator = operator
        self.left = left
        self.right = right
        super().__init__(location)

    def __str__(self) -> str:
        return f"{self.left}{self.operator.value}{self.right}"


class UnaryOperatorNode(ExpressionNode):
    def __init__(self, operator, operand, location):
        super().__init__(location)
        self.operator = operator
        self.operand = operand


class IfNode(ExpressionNode):
    def __init__(
        self,
        condition: ExpressionNode,
        then_expr: ExpressionNode,
        else_expr: ExpressionNode,
        location,
    ):
        super().__init__(location)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, location):
        super().__init__(location)
        self.condition = condition
        self.body = body


class BlockNode(ExpressionNode):
    def __init__(self, expressions: List[ExpressionNode], location):
        super().__init__(location)
        self.expressions = expressions


class LetNode(ExpressionNode):
    def __init__(self, bindings, body, location):
        super().__init__(location)
        self.bindings = bindings
        self.body = body


class CaseNode(ExpressionNode):
    def __init__(self, expr, cases: List["CaseOptionNode"], location):
        super().__init__(location)
        self.expr = expr
        self.cases = cases


class CaseOptionNode(Node):
    def __init__(self, name, type, expr, location):
        super().__init__(location)
        self.name = name
        self.type = type
        self.expr = expr


class NewNode(ExpressionNode):
    def __init__(self, type, location):
        super().__init__(location)
        self.type = type

    def value(self):
        return f"{self.__dict__}"


class IsVoidNode(ExpressionNode):
    def __init__(self, expr: ExpressionNode, location):
        self.expr = expr
        super().__init__(location)

    def __str__(self) -> str:
        return f"isvoid {self.expr}"


class NotNode(ExpressionNode):
    def __init__(self, expr: ExpressionNode, location):
        self.expr = expr
        super().__init__(location)

    def __str__(self) -> str:
        return f"not {self.expr}"


class PrimeNode(ExpressionNode):
    def __init__(self, expr: ExpressionNode, location):
        self.expr = expr
        super().__init__(location)

    def __str__(self) -> str:
        return f"`{self.expr}"


class IdentifierNode(ExpressionNode):
    def __init__(self, name, location):
        self.name = name
        super().__init__(location)

    def __str__(self) -> str:
        return self.name


class IntegerNode(ExpressionNode):
    def __init__(self, value, location):
        self._value = value
        super().__init__(location, IntType())

    def __str__(self) -> str:
        return str(self._value)


class StringNode(ExpressionNode):
    def __init__(self, value, location):
        self._value = value
        super().__init__(location, StringType())

    def __str__(self) -> str:
        return self._value


class BooleanNode(ExpressionNode):
    def __init__(self, value, location):
        self._value = value
        super().__init__(location, BoolType())

    def __str__(self) -> str:
        return str(self._value)


class MethodCallNode(ExpressionNode):
    def __init__(self, method, args, location):
        self.method = method
        self.args = args
        super().__init__(location)

    def __str__(self) -> str:
        s = f"{self.method}("
        for arg in self.args:
            s += f"{arg},"
        if len(self.args):
            s = s[:-1]
        s += ")"
        return s


class ErrorExpresion(ExpressionNode):
    def __init__(self, location):
        super().__init__(location)


def get_operan_precedence(operand):
    PRECEDENCE_MAP = {
        "DOT": 9,
        "AT": 8,
        "TILDE": 7,
        "VOID": 6,
        TokenType.STAR: 5,
        TokenType.DIV: 5,
        TokenType.PLUS: 4,
        TokenType.MINUS: 4,
        TokenType.LEQ: 3,
        TokenType.LOWER: 3,
        TokenType.EQUAL: 3,
        "NOT": 2,
        "ASSIGN": 1,
        None: 0,
    }

    if operand in PRECEDENCE_MAP:
        return PRECEDENCE_MAP[operand]
    return 0
