from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import NULL
from COOL.codegen.utils import FALSE


class GetVariable(Node):
    def __init__(self, line: int, column: dict, id:str) -> None:
        self.id = id
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor):
        var = mips_visitor.get_variable(self.id)
        self_var = mips_visitor.get_variable("self")
        if var["stored"] == "class":
            obj = [
                Comment(f"get variable {self.id}"),
                Instruction("lw", mips_visitor.rt, f"{mips_visitor.get_offset(self_var)}({mips_visitor.rsp})"),
                Instruction("lw", mips_visitor.rt, f"{var['memory']}({mips_visitor.rt})"),
                Comment(f"end get variable {self.id}"),
            ]
        else:
            obj = [
                Comment(f"get variable {self.id}"),
                Instruction("lw", mips_visitor.rt, f"{mips_visitor.get_offset(var)}({mips_visitor.rsp})"),
                Comment(f"end get variable {self.id}"),
            ]
        return obj

    def check(self, visitor):
        return visitor.visit_get_variable(self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        _type = mips_visitor.get_variable(self.id)["type"]
        return _type if _type != "SELF_TYPE" else mips_visitor.current_class

class Initialization(Node):
    def __init__(self, line: int, column: dict, id:str, type: str, expr: Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        self.dynamic_type = 'void'

        super().__init__(line, column)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        obj = [
            *self.expr.codegen(mips_visitor),
        ]
        return obj

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
        if self.type == "Int":
            type = [
                Instruction("li", mips_visitor.rt, 0),
            ]
        elif self.type == "String":
            type = [
                *mips_visitor.allocate_object(
                    8,
                    "String",
                    [
                        Instruction("li", mips_visitor.rt, 0),
                    ]
                ),
            ]
        elif self.type == "Bool":
            type = [
                Instruction("la", mips_visitor.rt, FALSE),
            ]
        else:
            type = [
                Instruction("la", mips_visitor.rt, NULL),
            ]
        obj = [
            *type,
        ]
        return obj

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
        expr = self.expr.codegen(mips_visitor)
        var = mips_visitor.get_variable(self.id)
        if var["stored"] == "class":
            obj = [
                Comment(f"assign variable {self.id}"),
                *expr,
                Instruction("lw", mips_visitor.rt, f"4({mips_visitor.rsp})"),
                Instruction("sw", mips_visitor.rt, f"{var['memory']}({mips_visitor.rt})"),
                Comment(f"end assign variable {self.id}"),
            ]
        else:
            obj = [
                Comment(f"assign variable {self.id}"),
                *expr,
                Instruction("sw", mips_visitor.rt, f"{mips_visitor.get_offset(var)}({mips_visitor.rsp})"),
                Comment(f"end assign variable {self.id}"),
            ]
        return obj

    def check(self, visitor):
        return visitor.visit_assign(self)
