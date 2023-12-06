from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import NULL
from COOL.codegen.utils import FALSE


class Method(Node):
    def __init__(self, line: int, column: int, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_method(self)
        expr = self.expr.codegen(mips_visitor)
        mips_visitor.add_expression(expr)
        mips_visitor.unvisit_method(self)

    def check(self, visitor):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: int, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.expr: Node = None
        self.id = id
        super().__init__(line, column)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_execute_method(self)
        exprs = [expr.codegen(mips_visitor) for expr in self.exprs]
        obj = [
            Comment(f"EXECUTE_METHOD_{mips_visitor.current_state}"),
            Instruction("addiu", "$sp", "$sp", "-4"),
            Instruction("sw", "$v0", "0($sp)"),
            *exprs,
            Instruction("jal", mips_visitor.get_class_method()),
        ]
        mips_visitor.unvisit_execute_method(self)

    def check(self,visitor):
        visitor.visit_execute_method(node = self)


class Attribute(Node):
    def __init__(self, line: int, column: int, id: str) -> None:
        self.id = id
        super().__init__(line, column)

    def check(self, visitor):
        visitor.visit_attribute(self)


class AttributeDeclaration(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        self.dynamic_type = 'void'

        super().__init__(line, column, id)

    # FIX: initializations, "", 0, false
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        if self.type == "Int" or self.type == "String":
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                Instruction("la", mips_visitor.register_store_results, "0"),
                Instruction("sw", mips_visitor.register_store_results, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
            ]
        elif self.type == "Bool":
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                Instruction("la", mips_visitor.register_store_results, FALSE),
                Instruction("sw", mips_visitor.register_store_results, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
            ]
        else:
            obj = [
                Comment(f"attribute {self.id}: {self.type}"),
                Instruction("la", mips_visitor.register_store_results, NULL),
                Instruction("sw", mips_visitor.register_store_results, "0($v0)"),
                Instruction("addiu", "$v0", "$v0", "4"),
            ]
        mips_visitor.add_attribute(obj)
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        ...
        # visitor.visit_attribute_declaration(self)


class AttributeInicialization(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        self.dynamic_type = type
        super().__init__(line, column, id)
    
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
            Instruction("sw", mips_visitor.register_store_results, "0($v0)"),
            Instruction("addiu", "$v0", "$v0", "4"),
        ]
        mips_visitor.add_attribute(obj)
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        visitor.visit_attribute_initialization(self)


class Formal(Node):
    def __init__(self, line: int, column: int, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column)

    def codegen(self):
        pass

    def check(self, visitor):
        raise NotImplementedError()
