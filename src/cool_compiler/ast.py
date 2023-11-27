from abc import ABCMeta, abstractmethod


class StdType:
    Bool = "Bool"
    Int = "Int"
    String = "String"
    IO = "IO"
    Object = "Object"


class IAST(ABCMeta):
    @abstractmethod
    def type(self) -> str:
        raise NotImplementedError()


class GroupingAST(IAST):
    def __init__(self, expr: IAST):
        self.expr = expr

    def type(self) -> str:
        return self.expr.type()


class IdentifierAST(IAST):
    def __init__(self, name: str):
        self.name = name

    def type(self) -> str:
        raise NotImplementedError()


class LiteralAST(IAST):
    def __init__(self, value: str):
        self.value = value


class BooleanAST(LiteralAST):
    def type(self) -> str:
        return StdType.Bool


class StringAST(LiteralAST):
    def type(self) -> str:
        return StdType.String


class IntAST(LiteralAST):
    def type(self) -> str:
        return StdType.Int
