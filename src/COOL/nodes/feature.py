from typing import List

from nodes import Node
from semantic.visitor import Visitor


class Method(Node):
    def __init__(self, line: int, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.id = id
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()

    def check(self):
        raise NotImplementedError()


class Attribute(Node):
    def __init__(self, line: int, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        visitor.visit_attribute(self)
