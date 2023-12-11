from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor
from COOL.semantic.visitor import Visitor_Class

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import NULL
from COOL.codegen.utils import TRUE
from COOL.codegen.utils import FALSE


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

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_execute_method(self)
        expr = self.expr.codegen(mips_visitor)
        exprs = []
        for i, _expr in enumerate(self.exprs):
            exprs.extend(
                [
                    *_expr.codegen(mips_visitor),
                    Instruction("sw", mips_visitor.rt, f"{4*(i+1)}({mips_visitor.rsp})"),
                ]
            )
        n_stack = len(self.exprs) * 4 + 4
        return_type = self.expr.get_return(mips_visitor)
        obj = [
            Comment(f"execute method {self.id}"),
            # allocate the stack
            *mips_visitor.allocate_stack(n_stack),
            *expr,
            # save the expr reference
            Instruction("sw", mips_visitor.rt, f"0({mips_visitor.rsp})"),
            *exprs,
            # load the saved expr reference
            Instruction("lw", mips_visitor.rt, f"0({mips_visitor.rsp})"),
            # load the type reference
            Instruction("lw", mips_visitor.rt, f"0({mips_visitor.rt})"),
            # load the label reference
            Instruction("lw", mips_visitor.rt, f"{mips_visitor.get_function(return_type, self.id)}({mips_visitor.rt})"),
            Instruction("jal", mips_visitor.rt),
            # deallocate stack
            *mips_visitor.deallocate_stack(n_stack),
            Comment(f"end execute method {self.id}"),
            "\n",
        ]
        mips_visitor.unvisit_execute_method(self)
        return obj
    
    def get_return(self, mips_visitor: MipsVisitor):
        if self.type:
            return self.type
        _type = self.expr.get_return(mips_visitor)
        _new_type = mips_visitor.inheriance_class_methods[_type][self.id]
        return _new_type if _new_type != "SELF_TYPE" else _type


class CodeBlock(Node):
    def __init__(self, line: int, column: int, exprs: List[Node]):
        self.exprs: List[Node] = exprs
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    
    def check(self,visitor:Visitor_Class):
        return visitor.visit_code_block(self)

    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        expr = []
        for _expr in self.exprs:
            expr.extend(_expr.codegen(mips_visitor))
        return expr
    
    def get_return(self, mips_visitor: MipsVisitor):
        return self.exprs[-1].get_return(mips_visitor)


class If(Node):
    def __init__(self, line: int, column: int, if_expr: Node, then_expr: Node, else_expr: Node):
        self.if_expr: Node = if_expr
        self.then_expr: Node = then_expr
        self.else_expr: Node = else_expr
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    
    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_if(self)
        if_expr = self.if_expr.codegen(mips_visitor)
        then_expr = self.then_expr.codegen(mips_visitor)
        else_expr = self.else_expr.codegen(mips_visitor)
        obj = [
            Comment(f"if_{mips_visitor.current_state}"),
            *if_expr,
            Instruction("lw", "$t0", "4($t0)"),
            Instruction("la", "$t1", TRUE),
            Instruction("beq", "$t1", "$t0", f"then_{mips_visitor.current_state}"),
            *else_expr,
            Instruction("j", f"end_if_{mips_visitor.current_state}"),
            Label(f"then_{mips_visitor.current_state}", indent="  "),
            *then_expr,
            Label(f"end_if_{mips_visitor.current_state}", indent="  "),
            Comment(f"end if_{mips_visitor.current_state}"),
        ]
        mips_visitor.unvisit_if(self)
        return obj

    def check(self, visitor):
        return visitor.visit_conditionals(self)

    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.then_expr.get_return(mips_visitor)

class While(Node):
    def __init__(self, line: int, column: int, while_expr: Node, loop_expr: Node):
        self.while_expr: Node = while_expr
        self.loop_expr: Node = loop_expr
        super().__init__(line, column)

    def first_elem(self):
        return self.while_expr
    
    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_while(self)
        while_expr = self.while_expr.codegen(mips_visitor)
        loop_expr = self.loop_expr.codegen(mips_visitor)
        obj = [
            Comment(f"while_{mips_visitor.current_state}"),
            Label(f"while_{mips_visitor.current_state}", indent="  "),
            *while_expr,
            Instruction("lw", "$t0", "4($t0)"),
            Instruction("la", "$t1", FALSE),
            Instruction("beq", "$t0", "$t1", f"end_while_{mips_visitor.current_state}"),
            *loop_expr,
            Instruction("j", f"while_{mips_visitor.current_state}"),
            Label(f"end_while_{mips_visitor.current_state}", indent="  "),
        ]
        mips_visitor.unvisit_while(self)
        return obj

    def check(self, visitor):
        return visitor.visit_loops(self)

    # FIX
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.loop_expr.get_return(mips_visitor)


class Let(Node):
    def __init__(self, line: int, column: int, let_list: List[Node], expr: Node):
        self.let_list: List[Node] = let_list
        self.expr: Node = expr
        super().__init__(line, column)
    
    # FIX
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_let(self)
        let_list = []
        for i, _let in enumerate(self.let_list):
            let_list.extend(
                [
                    *_let.codegen(mips_visitor),
                    Instruction("sw", mips_visitor.rt, f"{4*i}({mips_visitor.rsp})"),
                ]
            )
        expr = self.expr.codegen(mips_visitor)
        n_stack = len(self.let_list) * 4 
        obj = [
            Comment(f"let_{mips_visitor.current_state}"),
            # allocate the stack
            *mips_visitor.allocate_stack(n_stack),
            *let_list,
            *expr,
            # deallocate stack
            *mips_visitor.deallocate_stack(n_stack),
            Comment(f"end let_{mips_visitor.current_state}"),
            "\n",
        ]
        mips_visitor.unvisit_let(self)
        return obj
    
    def check(self, visitor):
        return visitor.visit_let(self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.expr.get_return(mips_visitor)


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
    
    # FIX
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.cases[0].get_return(mips_visitor)


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

    def codegen(self, mips_visitor: MipsVisitor):
        obj = [
            Instruction("jal", mips_visitor.get_class_name(self.type)),
            Instruction("move", mips_visitor.rt, mips_visitor.rv),
        ]
        return obj

    def check(self,visitor:Visitor_Class):
        return visitor.visit_new(self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.type


class Isvoid(Node):
    def __init__(self, line: int, column: int, expr: Node):
        self.expr: Node = expr
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    
    def check(self, visitor):
        return visitor.visit_isvoid(self)

    def codegen(self, mips_visitor: MipsVisitor):
        expr = self.expr.codegen(mips_visitor)
        obj = [
            *expr,
            Instruction("la", "$t1", NULL),
            Instruction("lw", "$t0", "4($t0)"),
            Instruction("seq", "$t0", "$t0", "$t1"),
            *mips_visitor.allocate_stack(4),
            Instruction("sw", "$t0", f"0({mips_visitor.rsp})"),
            Instruction("jal", "set_bool"),
            *mips_visitor.allocate_stack(4),
            Instruction("sw", "$t0", "0($sp)"),
            *mips_visitor.allocate_object(8, "Bool",
                    [Instruction("lw", mips_visitor.rt, "0($sp)")]
            ),
            *mips_visitor.deallocate_stack(4),
        ]
        return obj
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return 'Bool'
