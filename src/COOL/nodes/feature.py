from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.codegen_rules import NULL


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
        mips_visitor.add_expression(expr)
        mips_visitor.unvisit_method(self)

    def check(self, visitor):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: dict, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.expr: Node = None
        self.id = id
        super().__init__(line, column)

    def first_elem(self):
        return self.column

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self,visitor):
        visitor.visit_execute_method(node = self)


class Attribute(Node):
    def __init__(self, line: int, column: dict, id: str) -> None:
        self.id = id
        super().__init__(line, column)

    def first_elem(self):
        return self.column

    def check(self, visitor):
        visitor.visit_attribute(self)


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
        mips_visitor.add_attribute(
            f"    # attribute {self.id}: {self.type}\n"
            f"    la {mips_visitor.register_store_results}, {NULL}\n"
            f"    sw {mips_visitor.register_store_results}, 0({mips_visitor.register_memory_pointer})\n"
            f"    addiu $v0, $v0, 4\n"
        )
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
        mips_visitor.add_attribute(
            f"    # attribute {self.id}: {self.type}\n"
            f"    addiu $sp, $sp, -4\n"
            f"    sw $v0, 0($sp)\n"
            + expr +
            f"    lw $v0, 0($sp)\n"
            f"    addiu $sp, $sp, 4\n"
            f"    sw {mips_visitor.register_store_results}, 0($v0)\n"
            f"    addiu $v0, $v0, 4\n"
        )
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        visitor.visit_attribute_initialization(self)


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
