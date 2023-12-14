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
        n_stack = len(self.exprs) * 4 + 4
        exprs = []
        for i, _expr in enumerate(self.exprs):
            exprs.extend(
                [
                    *_expr.codegen(mips_visitor),
                    Instruction("sw", mips_visitor.rt, f"{4*(i+1)}({mips_visitor.rsp})"),
                ]
            )
        expr_type = self.expr.get_return(mips_visitor)
        function_index = mips_visitor.get_function(expr_type, self.id)
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
            (
                Instruction("lw", mips_visitor.rt, f"0({mips_visitor.rt})")
                if self.type is None
                else
                Instruction("la", mips_visitor.rt, self.type)
            ),
            # load the label reference
            Instruction("lw", mips_visitor.rt, f"{function_index}({mips_visitor.rt})"),
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
        expr_type = self.expr.get_return(mips_visitor)
        return_type = mips_visitor.get_return(expr_type, self.id)
        return return_type if return_type != "SELF_TYPE" else expr_type


class CodeBlock(Node):
    def __init__(self, line: int, column: int, exprs: List[Node]):
        self.exprs: List[Node] = exprs
        super().__init__(line, column)

    def first_elem(self):
        return self.column
    
    def check(self,visitor:Visitor_Class):
        return visitor.visit_code_block(self)

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
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_if(self)
        id = mips_visitor.get_id()
        # labels
        if_label = f"if_{id}"
        then_label = f"then_{id}"
        end_if_label = f"end_if_{id}"
        if_expr = self.if_expr.codegen(mips_visitor)
        then_expr = self.then_expr.codegen(mips_visitor)
        else_expr = self.else_expr.codegen(mips_visitor)
        obj = [
            Comment(if_label),
            *if_expr,
            Instruction("lw", "$t0", "4($t0)"),
            Instruction("la", "$t1", TRUE),
            Instruction("beq", "$t1", "$t0", then_label),
            *else_expr,
            Instruction("j", end_if_label),
            Label(then_label, indent="  "),
            *then_expr,
            Label(end_if_label, indent="  "),
            Comment(end_if_label),
            "\n"
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
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_while(self)
        id = mips_visitor.get_id()
        # labels
        while_label = f"while_{id}"
        end_while_label = f"end_while_{id}"
        while_expr = self.while_expr.codegen(mips_visitor)
        loop_expr = self.loop_expr.codegen(mips_visitor)
        obj = [
            Comment(while_label),
            Label(while_label, indent="  "),
            *while_expr,
            Instruction("lw", "$t0", "4($t0)"),
            Instruction("la", "$t1", FALSE),
            Instruction("beq", "$t0", "$t1", end_while_label),
            *loop_expr,
            Instruction("j", while_label),
            Label(end_while_label, indent="  "),
            Comment(end_while_label),
            "\n"
        ]
        mips_visitor.unvisit_while(self)
        return obj

    def check(self, visitor):
        return visitor.visit_loops(self)

    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.loop_expr.get_return(mips_visitor)


class Let(Node):
    def __init__(self, line: int, column: int, let_list: List[Node], expr: Node):
        self.let_list: List[Node] = let_list
        self.expr: Node = expr
        super().__init__(line, column)
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_let(self)
        id = mips_visitor.get_id()
        n_stack = len(self.let_list) * 4 
        # labels
        let_label = f"let_{id}"
        end_let_label = f"end let_{id}"
        let_list = []
        for i, _let in enumerate(self.let_list):
            let_list.extend(
                [
                    *_let.codegen(mips_visitor),
                    Instruction("sw", mips_visitor.rt, f"{4*i}({mips_visitor.rsp})"),
                ]
            )
        expr = self.expr.codegen(mips_visitor)
        obj = [
            Comment(let_label),
            # allocate the stack
            *mips_visitor.allocate_stack(n_stack),
            *let_list,
            *expr,
            # deallocate stack
            *mips_visitor.deallocate_stack(n_stack),
            Comment(end_let_label),
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
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_case(self)
        id = mips_visitor.get_id()
        # labels
        case_label = f"case_{id}"
        case_compare = "case_compare_{id}_{i}"
        end_case_label = f"end_case_{id}"
        global_expr = self.expr.codegen(mips_visitor)
        case_list_compare = []
        case_list_exec = []
        for i, _case in enumerate(self.cases):
            case_list_compare.extend(
                [
                    Instruction("la", "$t1", _case.type),
                    Instruction("lw", "$t1", "0($t1)"),
                    Instruction("beq", "$t2", "$t1", case_compare.format(id=id, i=i)),
                ]
            )
            case_list_exec.extend(
                [
                    Label(case_compare.format(id=id, i=i), indent="  "),
                    *_case.codegen(mips_visitor),
                    Instruction("j", end_case_label),
                ]
            )
        obj = [
            Comment(case_label),
            *global_expr,
            *mips_visitor.allocate_stack(4),
            Instruction("sw", "$t0", "0($sp)"),
            # load type reference
            Instruction("lw", "$t2", "0($t0)"),
            Instruction("lw", "$t2", "0($t2)"),
            Label(case_label, indent="  "),
            *case_list_compare,
            Instruction("lw", "$t2", "4($t2)"),
            Instruction("li", "$t1", 0),
            Instruction("bne", "$t2", "$t1", case_label),
            Instruction("la", "$a0", "case_error"),
            Instruction("li", "$v0", 4),
            Instruction("syscall"),
            Instruction("li", "$v0", 10),
            Instruction("syscall"),
            *case_list_exec,
            Label(end_case_label, indent="  "),
            *mips_visitor.deallocate_stack(4),
            Comment(end_case_label),
            "\n",
        ]
        mips_visitor.unvisit_case(self)
        return obj

    def check(self, visitor):
        return visitor.visit_case(self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.expr.get_return(mips_visitor)


class Case_expr(Node):
    def __init__(self, line: int, column: int, id:str, type:str, expr:Node) -> None:
        self.id = id
        self.type = type
        self.expr = expr
        super().__init__(line, column)

    def first_elem(self):
        return self.expr
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_case_expr(self)
        expr = self.expr.codegen(mips_visitor)
        obj = [
            Comment(f"case expr {self.id}"),
            *expr,
            Comment(f"end case expr {self.id}"),
        ]
        mips_visitor.unvisit_case_expr(self)
        return obj

    def check(self, visitor):
        return visitor.visit_case_expr(self)
    
    def get_return(self, mips_visitor: MipsVisitor) -> str:
        return self.type


class New(Node):
    def __init__(self, line: int, column: int, type: str):
        self.type: str = type
        super().__init__(line, column)
    
    def first_elem(self):
        return self.column

    def codegen(self, mips_visitor: MipsVisitor):
        memory = mips_visitor.get_class_data(self.type)["memory"]
        obj = [
            Comment(f"Instanciate class {self.type}"),
            # Allocate memory
            Instruction("li", mips_visitor.ra, memory),
            Instruction("li", mips_visitor.rv, 9),
            Instruction("syscall"),
            # Save the type reference
            Instruction("la", mips_visitor.rt, self.type),
            Instruction("sw", mips_visitor.rt, f"0({mips_visitor.rv})"),
            # save self in stack
            *mips_visitor.allocate_stack(4),
            Instruction("sw", mips_visitor.rv, f"0({mips_visitor.rsp})"),
            # call init
            Instruction("jal", mips_visitor.get_class_name(self.type)),
            # load self from stack
            Instruction("lw", mips_visitor.rt, f"0({mips_visitor.rsp})"),
            *mips_visitor.deallocate_stack(4),
            Comment(f"End Instanciate class {self.type}"),
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
