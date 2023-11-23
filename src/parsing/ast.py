from collections import namedtuple
from enum import Enum
from typing import List

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
        super().__init__(location)
        self.classes: List[ClassNode] = classes


class ClassNode(Node):
    def __init__(self, name: str, parent: str, features: List["FeatureNode"], location):
        super().__init__(location)
        self.name = name
        self.parent = parent
        self.features = features


class FeatureNode(Node):
    def __init__(self, location):
        super().__init__(location)


class MethodNode(FeatureNode):
    def __init__(self, name, formals: List["FormalNode"], return_type, body, location):
        super().__init__(location)
        self.name = name
        self.formals = formals
        self.return_type = return_type
        self.body = body


class AttributeNode(FeatureNode):
    def __init__(self, name, attr_type, init, location):
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
    def __init__(self, location):
        super().__init__(location)


class AssignNode(ExpressionNode):
    def __init__(self, name, expr: ExpressionNode, location):
        super().__init__(location)
        self.name = name
        self.expr = expr


class DispatchNode(ExpressionNode):
    def __init__(self, expr, method, args, location, method_type=None):
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
    EQ = "=="
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
    def __init__(self, condition, then_expr, else_expr, location):
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
    def __init__(self, expressions, location):
        super().__init__(location)
        self.expressions = expressions


class LetNode(ExpressionNode):
    def __init__(self, bindings, body, location):
        super().__init__(location)
        self.bindings = bindings
        self.body = body


class CaseNode(ExpressionNode):
    def __init__(self, expr, cases, location):
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
    def __init__(self, expr, location):
        self.expr = expr
        super().__init__(location)

    def __str__(self) -> str:
        return f"isvoid {self.expr}"


class NotNode(ExpressionNode):
    def __init__(self, expr, location):
        self.expr = expr
        super().__init__(location)

    def __str__(self) -> str:
        return f"not {self.expr}"


class IdentifierNode(ExpressionNode):
    def __init__(self, name, location):
        self.name = name
        super().__init__(location)

    def __str__(self) -> str:
        return self.name


class IntegerNode(ExpressionNode):
    def __init__(self, value, location):
        self._value = value
        super().__init__(location)

    def __str__(self) -> str:
        return str(self._value)


class StringNode(ExpressionNode):
    def __init__(self, value, location):
        self._value = value
        super().__init__(location)

    def __str__(self) -> str:
        return str(self._value)


class BooleanNode(ExpressionNode):
    def __init__(self, value, location):
        self._value = value
        super().__init__(location)

    def __str__(self) -> str:
        return str(self._value)


class MethodCallNode(ExpressionNode):
    def __init__(self, method, args, location):
        super().__init__(location)
        self.method = method
        self.args = args
