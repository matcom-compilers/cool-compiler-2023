from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor
from COOL.semantic.visitor import Visitor_Class
from COOL.codegen.codegen_rules import NULL

class Dispatch(Node):
    def __init__(self, line: int, column: int, expr: Node, id: str, type: str = None, exprs: List[Node] = None):
        self.expr: Node = expr
        self.id: str = id
        self.type: str = type
        self.exprs: List[Node] = exprs
        super().__init__(line, column)

    def check(self, visitor:Visitor_Class):
        return visitor.visit_dispatch(self)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class CodeBlock(Node):
    def __init__(self, line: int, column: int, exprs: List[Node]):
        self.exprs: List[Node] = exprs
        super().__init__(line, column)

    def check(self,visitor:Visitor_Class):
        return visitor.visit_code_block(self)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

class If(Node):
    def __init__(self, line: int, column: int, if_expr: Node, then_expr: Node, else_expr: Node):
        self.if_expr: Node = if_expr
        self.then_expr: Node = then_expr
        self.else_expr: Node = else_expr
        super().__init__(line, column)

    def check(self):
        raise NotImplementedError()

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class While(Node):
    def __init__(self, line: int, column: int, while_expr: Node, loop_expr: Node):
        self.while_expr: Node = while_expr
        self.loop_expr: Node = loop_expr
        super().__init__(line, column)

    def check(self):
        raise NotImplementedError()

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class Let(Node):
    def __init__(self, line: int, column: int, let_list: List[Node], expr: Node):
        self.let_list: List[Node] = let_list
        self.expr: Node = expr
        super().__init__(line, column)

    def check(self):
        raise NotImplementedError()

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class Case(Node):
    def __init__(self, line: int, column: int, expr: Node, cases: List[Node]):
        self.expr: Node = expr
        self.cases: List[Node] = cases
        super().__init__(line, column)

    def check(self):
        raise NotImplementedError()

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class New(Node):
    def __init__(self, line: int, column: int, type: str):
        self.type: str = type
        super().__init__(line, column)

    def check(self,visitor:Visitor_Class):
        return visitor.visit_new(self)

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class Isvoid(Node):
    def __init__(self, line: int, column: int, expr: Node):
        self.expr: Node = expr
        super().__init__(line, column)

    def check(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        expr = self.expr.codegen(mips_visitor)
        obj = (
            expr +
            f"    move {mips_visitor.register_store_results}, $t0\n"
            f"    la  $t1, {NULL}\n"
            f"    seq $t0, $t0, $t1\n"
        )
        raise NotImplementedError()
