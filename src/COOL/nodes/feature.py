from typing import List

from COOL.nodes import Node
from COOL.semantic.visitor import Visitor

from COOL.nodes.codegen_rules import SET_VAR_IN_DATA_SECTION
from COOL.nodes.codegen_rules import CREATE_FUNCTION

class Method(Node):
    def __init__(self, line: int, column: int, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line, column)

    def execute(self):
        return [], []

    def check(self, visitor: Visitor):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: int, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.id = id
        super().__init__(line, column)

    def execute(self):
        raise NotImplementedError()

    def check(self):
        raise NotImplementedError()


class Attribute(Node):
    def __init__(self, line: int, column: int, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        super().__init__(line, column)

    def execute(self):
        return [], []

    def check(self, visitor: Visitor):
        visitor.visit_attribute(self)
