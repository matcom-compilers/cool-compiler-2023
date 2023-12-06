from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor
from COOL.semantic.visitor import Visitor_Class

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import NULL
from COOL.codegen.utils import TRUE


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

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        expr = "\n".join([expr.codegen(mips_visitor) for expr in self.exprs])
        return expr


class If(Node):
    def __init__(self, line: int, column: int, if_expr: Node, then_expr: Node, else_expr: Node):
        self.if_expr: Node = if_expr
        self.then_expr: Node = then_expr
        self.else_expr: Node = else_expr
        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_if(self)
        if_expr = self.if_expr.codegen(mips_visitor)
        then_expr = self.then_expr.codegen(mips_visitor)
        else_expr = self.else_expr.codegen(mips_visitor)
        obj = [
            *if_expr,
            Comment(f"IF_{mips_visitor.current_state}"),
            Instruction("la", "$t0", TRUE),
            Instruction("beq", "$t0", "$t0", f"else_{mips_visitor.current_state}"),
            Instruction("nop"),
            Label(f"then_{mips_visitor.current_state}"),
            *then_expr,
            Instruction("j", f"end_if_{mips_visitor.current_state}"),
            Instruction("nop"),
            Label(f"else_{mips_visitor.current_state}"),
            *else_expr,
            Label(f"end_if_{mips_visitor.current_state}"),
        ]
        mips_visitor.unvisit_if(self)
        return obj

    def check(self, visitor):
        return visitor.visit_conditionals(self)


class While(Node):
    def __init__(self, line: int, column: int, while_expr: Node, loop_expr: Node):
        self.while_expr: Node = while_expr
        self.loop_expr: Node = loop_expr
        super().__init__(line, column)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_while(self)
        while_expr = self.while_expr.codegen(mips_visitor)
        loop_expr = self.loop_expr.codegen(mips_visitor)
        obj = (
            f"    # WHILE_{mips_visitor.current_state}\n"
            f"    while_{mips_visitor.current_state}:\n"
            f"    {while_expr}"
            f"    la  $t0, {TRUE}\n"
            f"    beq $t0, $t0, loop_{mips_visitor.current_state}\n"
            f"    nop\n"
            f"    end_while_{mips_visitor.current_state}:\n"
            f"    j   end_while_{mips_visitor.current_state}\n"
            f"    nop\n"
            f"    loop_{mips_visitor.current_state}:\n"
            f"    {loop_expr}"
            f"    j   while_{mips_visitor.current_state}\n"
            f"    nop\n"
        )
        mips_visitor.unvisit_while(self)
        return obj

    def check(self, visitor):
        return visitor.visit_loops(self)


class Let(Node):
    def __init__(self, line: int, column: int, let_list: List[Node], expr: Node):
        self.let_list: List[Node] = let_list
        self.expr: Node = expr
        super().__init__(line, column)
    
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
    
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor):
        return visitor.visit_case_expr(self)


class New(Node):
    def __init__(self, line: int, column: int, type: str):
        self.type: str = type
        super().__init__(line, column)
    
    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        obj = (
            f"    jal {self.type}\n"
            f"    move {mips_visitor.register_store_results}, $v0\n"
        )
        return obj

    def check(self,visitor:Visitor_Class):
        return visitor.visit_new(self)


class Isvoid(Node):
    def __init__(self, line: int, column: int, expr: Node):
        self.expr: Node = expr
        super().__init__(line, column)


    def check(self, visitor):
        return visitor.visit_isvoid(self)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        expr = self.expr.codegen(mips_visitor)
        obj = (
            expr +
            f"    move {mips_visitor.register_store_results}, $t0\n"
            f"    la  $t1, {NULL}\n"
            f"    seq $t0, $t0, $t1\n"
        )
        raise NotImplementedError()
