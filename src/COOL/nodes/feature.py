from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import NULL
from COOL.codegen.utils import FALSE


class Method(Node):
    def __init__(self, line: int, column: dict, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_method(self)
        expr = self.expr.codegen(mips_visitor)
        obj = [
            Comment(f"Create function {self.id} from class {mips_visitor.current_class}", indent=""),
            Label(mips_visitor.get_method_name(mips_visitor.current_class, self.id)),
            # save $ra reference
            *mips_visitor.allocate_stack(4),
            Instruction("sw", mips_visitor.rra, f"0({mips_visitor.rsp})"),
            *expr,
            # load $ra reference
            Instruction("lw", mips_visitor.rra, f"0({mips_visitor.rsp})"),
            *mips_visitor.deallocate_stack(4),
            Instruction("jr", mips_visitor.rra),
            "\n",
        ]
        mips_visitor.add_method(obj)
        mips_visitor.unvisit_method(self)

    def check(self, visitor):
        return visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: dict, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.expr: Node = None
        self.id = id
        super().__init__(line, column)

    def first_elem(self):
        return self.column

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_execute_method(self)
        exprs = []
        for i, _expr in enumerate(self.exprs):
            exprs.extend(
                [
                    *_expr.codegen(mips_visitor),
                    Instruction("sw", "$t0", f"{4*(i+1)}({mips_visitor.rsp})"),
                ]
            )
        n_stack = len(self.exprs) * 4 + 4
        # mips_visitor.set_offset(n_stack)
        obj = [
            Comment(f"execute class method {self.id}"),
            # allocate the stack
            *mips_visitor.allocate_stack(n_stack),
            *exprs,       
            # get function label
            Instruction("lw", mips_visitor.rt, f"{n_stack+4}({mips_visitor.rsp})"),
            Instruction("lw", mips_visitor.rt, f"0({mips_visitor.rt})"),
            # save self reference
            Instruction("sw", mips_visitor.rt, f"0({mips_visitor.rsp})"),
            # load the method to jump
            Instruction("lw", mips_visitor.rt, f"{mips_visitor.get_function(mips_visitor.current_class, self.id)}({mips_visitor.rt})"),
            Instruction("jal", mips_visitor.rt),
            # deallocate stack
            *mips_visitor.deallocate_stack(n_stack),
            "\n",
        ]
        # mips_visitor.set_offset(-n_stack)
        mips_visitor.unvisit_execute_method(self)
        return obj

    def check(self,visitor):
        return visitor.visit_execute_method(node = self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return mips_visitor.inheriance_class_methods[mips_visitor.current_class][self.id]


class Attribute(Node):
    def __init__(self, line: int, column: dict, id: str) -> None:
        self.id = id
        super().__init__(line, column)

    def first_elem(self):
        return self.column

    def check(self, visitor):
        return visitor.visit_attribute(self)


class AttributeDeclaration(Attribute):
    def __init__(self, line: int, column: dict, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        self.dynamic_type = 'void'

        super().__init__(line, column, id)

    def first_elem(self):
        return self.column

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        if self.type == "Int":
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                Instruction("la", mips_visitor.rt, "0"),
                Instruction("sw", mips_visitor.rt, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
                "\n",
            ]
        elif self.type == "String":
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                *mips_visitor.allocate_object(8, [Instruction("la", mips_visitor.rt, 0),]),
                Instruction("sw", mips_visitor.rt, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
                "\n",
            ]
        elif self.type == "Bool":
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                Instruction("la", mips_visitor.rt, FALSE),
                Instruction("sw", mips_visitor.rt, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
                "\n",
            ]
        else:
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                Instruction("la", mips_visitor.rt, NULL),
                Instruction("sw", mips_visitor.rt, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
                "\n",
            ]
        mips_visitor.add_attribute(obj)
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        ...
        # visitor.visit_attribute_declaration(self)


class AttributeInicialization(Attribute):
    def __init__(self, line: int, column: dict, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        self.dynamic_type = type
        super().__init__(line, column, id)
    
    def first_elem(self):
        return self.column

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        expr = self.expr.codegen(mips_visitor)
        obj = [
            Comment(f"attribute {self.id}: {self.type}"),
            Instruction("addiu", "$sp", "$sp", "-4"),
            Instruction("sw", "$v0", "0($sp)"),
            *expr,
            Instruction("lw", "$v0", "0($sp)"),
            Instruction("addiu", "$sp", "$sp", "4"),
            Instruction("sw", mips_visitor.rt, "0($v0)"),
            Instruction("addiu", "$v0", "$v0", "4"),
            "\n",
        ]
        mips_visitor.add_attribute(obj)
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        return visitor.visit_attribute_initialization(self)


class Formal(Node):
    def __init__(self, line: int, column: dict, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column)

    def first_elem(self):
        return self.column

    def codegen(self):
        pass

    def check(self, visitor):
        raise NotImplementedError()
