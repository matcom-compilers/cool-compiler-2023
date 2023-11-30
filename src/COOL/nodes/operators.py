from abc import abstractmethod

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor


class UnaryOperator(Node):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        self.expr: Node = expr
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor, out_register: str="$t0"):
        expr = self.expr.codegen(mips_visitor)
        operation = self.operator(out_register)
        # TODO: what to return

    @abstractmethod
    def operator(self, out_register: str="$t0") -> str:
        pass

    def check(self):
        raise NotImplementedError()


class Operator(Node):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.expr1: Node = expr1
        self.expr2: Node = expr2
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor, out_register: str="$t0"):
        expr1 = self.expr1.codegen(mips_visitor, "$t0")
        expr2 = self.expr2.codegen(mips_visitor, "$t1")
        operation = self.operator(out_register)
        # TODO: what to return

    @abstractmethod
    def operator(self, out_register: str="$t0") -> str:
        pass

    def check(self):
        raise NotImplementedError()


class Add(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    add {out_register}, $t0, $t1"


class Sub(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    sub {out_register}, $t0, $t1"


class Div(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    div {out_register}, $t0, $t1"


class Times(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    mul {out_register}, $t0, $t1"


class Less(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    slt {out_register}, $t0, $t1"


class LessEqual(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    sle {out_register}, $t0, $t1"


class Equal(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2)

    def operator(self, out_register: str="$t0"):
        return f"    seq {out_register}, $t0, $t1"


class Not(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr)

    def operator(self, out_register: str="$t0"):
        # TODO: check this
        return f"    not {out_register}, $t0"


class Bitwise(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr)

    def operator(self, out_register: str="$t0"):
        # TODO: check this
        return f"    and {out_register}, $t0, $t1"
