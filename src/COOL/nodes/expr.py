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

    def first_elem(self):
        return self.expr
    
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()


class CodeBlock(Node):
    def __init__(self, line: int, column: int, exprs: List[Node]):
        self.exprs: List[Node] = exprs
        super().__init__(line, column)

    def first_elem(self):
        return self.exprs[0]
    
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

    def first_elem(self):
        return self.column
    
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_conditionals(self)


class While(Node):
    def __init__(self, line: int, column: int, while_expr: Node, loop_expr: Node):
        self.while_expr: Node = while_expr
        self.loop_expr: Node = loop_expr
        super().__init__(line, column)

    def first_elem(self):
        return self.while_expr
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_loops(self)


class Let(Node):
    def __init__(self, line: int, column: int, let_list: List[Node], expr: Node):
        self.let_list: List[Node] = let_list
        self.expr: Node = expr
        super().__init__(line, column)
            
    # def first_elem(self):
    #     return self.let_list[0]
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()
    
    def check(self, visitor):
        return visitor.visit_let(self)


class Case(Node):
    def __init__(self, line: int, column: int, expr: Node, cases: List[Node]):
        self.expr: Node = expr
        self.cases: List[Node] = cases
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_case(self)


class Case_expr(Node):
    def __init__(self, line: int, column: int, id:str, type:str, expr:Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        super().__init__(line, column)

    def first_elem(self):
        return self.expr
    
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_case_expr(self)


class New(Node):
    def __init__(self, line: int, column: int, type: str):
        self.type: str = type
        super().__init__(line, column)
    
    def first_elem(self):
        return self.column
    # TODO
    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self,visitor:Visitor_Class):
        return visitor.visit_new(self)


class Isvoid(Node):
    def __init__(self, line: int, column: int, expr: Node):
        self.expr: Node = expr
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    
    def check(self, visitor):
        return visitor.visit_isvoid(self)

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
