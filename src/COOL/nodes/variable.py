from COOL.nodes import Node


class GetVariable(Node):
    def __init__(self, line: int, column: int, id:str) -> None:
        self.id = id
        super().__init__(line, column)

    # TODO
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_get_variable(self)

class Initialization(Node):
    def __init__(self, line: int, column: int, id:str, type: str, expr: Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        super().__init__(line, column)

    # TODO
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor):
        raise NotImplementedError()

class Declaration(Node):
    def __init__(self, line: int, column: int, id:str, type:str) -> None:
        self.id = id
        self.type = type
        super().__init__(line, column)
    
    # TODO
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor):
        raise NotImplementedError()
    
class Assign(Node):
    def __init__(self, line: int, column: int, id: str, expr: Node) -> None:
        self.expr: Node = expr
        self.id = id
        super().__init__(line, column)

    # TODO
    def codegen(self):
        raise NotImplementedError()

    def check(self):
        raise NotImplementedError()