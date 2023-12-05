from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor


class GetVariable(Node):
    def __init__(self, line: int, column: int, id:str) -> None:
        self.id = id
        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        var = mips_visitor.get_variable(self)
        obj = f"    move {mips_visitor.register_store_results}, {var}\n"
        return obj

    def check(self, visitor):
        return visitor.visit_get_variable(self)

class Initialization(Node):
    def __init__(self, line: int, column: int, id:str, type: str, expr: Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        super().__init__(line, column)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        raise NotImplementedError()

class Declaration(Node):
    def __init__(self, line: int, column: int, id:str, type:str) -> None:
        self.id = id
        self.type = type
        super().__init__(line, column)
    
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        raise NotImplementedError()
    
class Assign(Node):
    def __init__(self, line: int, column: int, id: str, expr: Node) -> None:
        self.expr: Node = expr
        self.id = id
        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        var = mips_visitor.get_variable(self)
        expr = self.expr.codegen(mips_visitor)
        obj = (
            expr +
            f"    move {var}, {mips_visitor.register_store_results}\n"
        )
        return obj

    def check(self):
        raise NotImplementedError()