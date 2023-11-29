from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from .types import StdType, TypeEnvironment


class IAST(ABCMeta):
    @abstractmethod
    def check_type(self, te: TypeEnvironment) -> str:
        raise NotImplementedError()


class ConditionalExpressionAST(IAST):
    def __init__(self, condition: IAST, then_expr: IAST, else_expr: IAST):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

    def check_type(self, te) -> str:
        if self.condition.check_type() is not StdType.Bool:
            raise TypeError()
        elif self.condition:
            return self.then_expr.check_type()
        else:
            return self.else_expr.check_type()
        


class LoopExpressionAST(IAST):
    def __init__(self, condition: IAST, body: IAST):
        self.condition = condition
        self.body = body

    def check_type(self, te) -> str:
        raise NotImplementedError()


class BlockExpressionAST(IAST):
    def __init__(self, expr_list: List[IAST]):
        self.expr_list = expr_list

    def check_type(self, te) -> str:
        raise NotImplementedError()


class TypeMatchingAST(IAST):
    def __init__(self, expr: IAST, cases: List[Tuple[str, str, IAST]]):
        self.expr = expr
        self.cases = cases  # tuple is (object id, object type, expr)

    def check_type(self, te) -> str:
        raise NotImplementedError()


class ObjectInitAST(IAST):
    def __init__(self, type: str):
        self.type = type

    def check_type(self, te) -> str:
        raise NotImplementedError()


class UnaryOpAST(IAST):
    def __init__(self, expr: IAST):
        self.expr = expr


class VoidCheckingOpAST(UnaryOpAST):
    def check_type(self, te) -> str:
        raise NotImplementedError()


class NegationOpAST(UnaryOpAST):
    def check_type(self, te) -> str:
        raise NotImplementedError()


class BooleanNegationOpAST(UnaryOpAST):
    def check_type(self, te) -> str:
        raise NotImplementedError()


BINARY_OPERATIONS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '=': lambda a, b: a == b,
}


class BinaryOpAST(IAST):
    def __init__(self, left: IAST, right: IAST, op: str):
        self.left = left
        self.right = right
        self.op = (op, BINARY_OPERATIONS[op])


class ArithmeticOpAST(BinaryOpAST):
    def check_type(self, te) -> str:
        raise NotImplementedError()


class ComparisonOpAST(BinaryOpAST):
    def check_type(self, te) -> str:
        raise NotImplementedError()


class GroupingAST(IAST):
    def __init__(self, expr: IAST):
        self.expr = expr

    def check_type(self, te) -> str:
        return self.expr.check_type(te)


class IdentifierAST(IAST):
    def __init__(self, name: str):
        self.name = name

    def check_type(self, te) -> str:
        return te.get_object_type(self.name)


class LiteralAST(IAST):
    def __init__(self, value: str):
        self.value = value


class BooleanAST(LiteralAST):
    def check_type(self, _) -> str:
        return StdType.Bool


class StringAST(LiteralAST):
    def check_type(self, _) -> str:
        return StdType.String


class IntAST(LiteralAST):
    def check_type(self, _) -> str:
        return StdType.Int
