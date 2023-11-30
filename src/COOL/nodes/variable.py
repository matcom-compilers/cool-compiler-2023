from COOL.nodes import Node
from COOL.semantic.visitor import Visitor


class GetVariable(Node):
    def __init__(self, line: int, column: int, id:str) -> None:
        self.id = id
        super().__init__(line, column)

    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        raise NotImplementedError()

class Initialization(Node):
    def __init__(self, line: int, column: int, id:str, type: str, expr: Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        super().__init__(line, column)

    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        raise NotImplementedError()

class Declaration(Node):
    def __init__(self, line: int, column: int, id:str, type:str) -> None:
        self.id = id
        self.type = type
        super().__init__(line, column)
    
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        raise NotImplementedError()
    
class Assign(Node):
    def __init__(self, line: int, column: int, id: str, expr: Node) -> None:
        self.expr: Node = expr
        self.id = id
        super().__init__(line, column)

    def codegen(self):
        raise NotImplementedError()

    def check(self):
        raise NotImplementedError()