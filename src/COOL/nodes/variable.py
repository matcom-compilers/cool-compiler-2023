from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label


class GetVariable(Node):
    def __init__(self, line: int, column: int, id:str) -> None:
        self.id = id
        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        var = mips_visitor.get_variable(self)
        obj = [
            Instruction("move", mips_visitor.rsr, var)
        ]
        return obj

    def check(self, visitor):
        return visitor.visit_get_variable(self)

class Initialization(Node):
    def __init__(self, line: int, column: int, id:str, type: str, expr: Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        self.dynamic_type = 'void'

        super().__init__(line, column)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_initialization(self)

class Declaration(Node):
    def __init__(self, line: int, column: int, id:str, type:str) -> None:
        self.id = id
        self.type = type
        self.dynamic_type = 'void'

        super().__init__(line, column)
    
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_declaration(self)
    
class Assign(Node):
    def __init__(self, line: int, column: int, id: str, expr: Node) -> None:
        self.expr: Node = expr
        self.id = id
        self.dynamic_type = 'void'

        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        var = mips_visitor.get_variable(self)
        expr = self.expr.codegen(mips_visitor)
        obj = [
            *expr,
            Instruction("move", var, mips_visitor.rsr)
        ]
        return obj

    def check(self, visitor):
        return visitor.visit_assign(self)
