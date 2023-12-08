from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label


class GetVariable(Node):
    def __init__(self, line: int, column: dict, id:str) -> None:
        self.id = id
        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        var_index = mips_visitor.get_variable(self.id)["memory"]
        obj = [
            Instruction("lw", mips_visitor.rt, f"{mips_visitor.current_offset + 4}({mips_visitor.rsp})"),
            Instruction("lw", mips_visitor.rt, f"{var_index}({mips_visitor.rt})")
        ]
        return obj

    def check(self, visitor):
        return visitor.visit_get_variable(self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return mips_visitor.get_variable(self.id)["type"]

class Initialization(Node):
    def __init__(self, line: int, column: dict, id:str, type: str, expr: Node) -> None:
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
    def __init__(self, line: int, column: dict, id:str, type:str) -> None:
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
    def __init__(self, line: int, column: dict, id: str, expr: Node) -> None:
        self.expr: Node = expr
        self.id = id
        self.dynamic_type = 'void'

        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        var = mips_visitor.get_variable(self.id)["memory"]
        expr = self.expr.codegen(mips_visitor)
        obj = [
            *expr,
            Instruction("sw", mips_visitor.rt, f"{var}({mips_visitor.rsp})")
        ]
        return obj

    def check(self, visitor):
        return visitor.visit_assign(self)
