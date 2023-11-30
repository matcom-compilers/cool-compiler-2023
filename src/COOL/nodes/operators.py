from abc import abstractmethod

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor
from COOL.codegen.codegen_rules import PUSH_STACK
from COOL.codegen.codegen_rules import POP_STACK


class UnaryOperator(Node):
    def __init__(self, line: int, column: int, expr: Node, possibles_types:list, return_type:str) -> None:
        self.expr: Node = expr
        self.possibles_types = possibles_types
        self.return_type = return_type
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor) -> str:
        expr = self.expr.codegen(mips_visitor)
        operation = self.operation()
        result = (
            expr +
            operation
        )
        return result

    @abstractmethod
    def operation(self) -> str:
        pass

    def check(self, visitor):
        return visitor.visit_unary_operator(self)


class Operator(Node):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node, possibles_types:list, return_type:str) -> None:
        self.expr1: Node = expr1
        self.expr2: Node = expr2
        self.possibles_types = possibles_types
        self.return_type = return_type

        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor) -> str:
        expr1 = self.expr1.codegen(mips_visitor)
        expr2 = self.expr2.codegen(mips_visitor)
        operation = self.operation()
        result =(
            expr1 +
            PUSH_STACK.format(register="$t0") +
            expr2 +
            POP_STACK.format(register="$t1") +
            operation
        )
        return result

    @abstractmethod
    def operation(self) -> str:
        pass

    def check(self,visitor):
        return visitor.visit_operator(self)

class Add(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operation(self):
        return "    add $t0, $t0, $t1\n"


class Sub(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operation(self):
        return "    sub $t0, $t0, $t1\n"


class Div(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operation(self):
        return "    div $t0, $t0, $t1\n"


class Times(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Int'
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operation(self):
        return "    mul $t0, $t0, $t1\n"


class Less(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Bool'
        super().__init__(line, column, expr1, expr2, ['Int'],'Bool')

    # FIX
    def operation(self):
        return "    slt $t0, $t0, $t1\n"


class LessEqual(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:

        super().__init__(line, column, expr1, expr2, ['Int'],'Bool')

    # FIX
    def operation(self):
        return "    sle $t0, $t0, $t1\n"


class Equal(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        
        super().__init__(line, column, expr1, expr2, ['All'],'Bool')

    # FIX
    def operation(self):
        return "    seq $t0, $t0, $t1\n"


class Not(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Bool'],'Bool')

    # FIX
    def operation(self):
        return "    not $t0, $t0\n"


class Bitwise(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Int'],'Int')

    # FIX
    def operation(self):
        return "    and $t0, $t0, $t1\n"
