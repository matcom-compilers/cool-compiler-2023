from abc import abstractmethod

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor


class UnaryOperator(Node):
    def __init__(self, line: int, column: int, expr: Node, possibles_types:list, return_type:str, symbol:str) -> None:
        self.expr: Node = expr
        self.possibles_types = possibles_types
        self.return_type = return_type
        self.symbol = symbol
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor, out_register: str="$t0"):
        expr = self.expr.codegen(mips_visitor)
        operation = self.operator(out_register)
        # TODO: what to return

    @abstractmethod
    def operator(self, out_register: str="$t0") -> str:
        pass

    def check(self, visitor):
        return visitor.visit_unary_operator(self)


class Operator(Node):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node, possibles_types:list, return_type:str, symbol:str) -> None:
        self.expr1: Node = expr1
        self.expr2: Node = expr2
        self.possibles_types = possibles_types
        self.return_type = return_type
        self.symbol = symbol
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor, out_register: str="$t0"):
        expr1 = self.expr1.codegen(mips_visitor, "$t0")
        expr2 = self.expr2.codegen(mips_visitor, "$t1")
        operation = self.operator(out_register)
        # TODO: what to return

    @abstractmethod
    def operator(self, out_register: str="$t0") -> str:
        pass

    def check(self,visitor):
        return visitor.visit_operator(self)

class Add(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '+')

    def operator(self, out_register: str="$t0"):
        return f"    add {out_register}, $t0, $t1"


class Sub(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '-')

    def operator(self, out_register: str="$t0"):
        return f"    sub {out_register}, $t0, $t1"


class Div(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '/')

    def operator(self, out_register: str="$t0"):
        return f"    div {out_register}, $t0, $t1"


class Times(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Int'
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '*')

    def operator(self, out_register: str="$t0"):
        return f"    mul {out_register}, $t0, $t1"


class Less(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Bool'
        super().__init__(line, column, expr1, expr2, ['Int'],'Bool', '<')

    def operator(self, out_register: str="$t0"):
        return f"    slt {out_register}, $t0, $t1"


class LessEqual(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:

        super().__init__(line, column, expr1, expr2, ['Int'],'Bool', '<=')

    def operator(self, out_register: str="$t0"):
        return f"    sle {out_register}, $t0, $t1"


class Equal(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        
        super().__init__(line, column, expr1, expr2, ['All'],'Bool', '=')

    def operator(self, out_register: str="$t0"):
        return f"    seq {out_register}, $t0, $t1"


class Not(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Bool'],'Bool', 'not')

    def operator(self, out_register: str="$t0"):
        # TODO: check this
        return f"    not {out_register}, $t0"


class Bitwise(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Int'],'Int', '~')

    def operator(self, out_register: str="$t0"):
        # TODO: check this
        return f"    and {out_register}, $t0, $t1"
