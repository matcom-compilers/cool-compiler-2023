from abc import abstractmethod

from COOL.nodes import Node

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.mips_visitor import MipsVisitor
from COOL.codegen.codegen_rules import PUSH_STACK
from COOL.codegen.codegen_rules import POP_STACK


class UnaryOperator(Node):
    def __init__(self, line: int, column: int, expr: Node, possibles_types:list, return_type:str, symbol:str) -> None:
        self.expr: Node = expr
        self.possibles_types = possibles_types
        self.return_type = return_type
        self.symbol = symbol
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor) -> str:
        expr = self.expr.codegen(mips_visitor)
        operation = self.operation()
        result = [
            *expr,
            *operation
        ]
        return result

    @abstractmethod
    def operation(self) -> str:
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

    def codegen(self, mips_visitor: MipsVisitor) -> str:
        expr1 = self.expr1.codegen(mips_visitor)
        expr2 = self.expr2.codegen(mips_visitor)
        operation = self.operation()
        result =[
            *expr1,
            Instruction("addiu", "$sp", "$sp", "-4"),
            Instruction("sw", "$t0", "0($sp)"),
            *expr2,
            Instruction("lw", "$t1", "0($sp)"),
            Instruction("addiu", "$sp", "$sp", "4"),
            *operation
        ]
        return result

    @abstractmethod
    def operation(self) -> str:
        pass

    def check(self,visitor):
        return visitor.visit_operator(self)

class Add(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '+')

    def operation(self):
        obj = [
            Instruction("add", "$t0", "$t0", "$t1"),
        ]
        return obj


class Sub(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '-')

    def operation(self):
        obj = [
            Instruction("sub", "$t0", "$t0", "$t1"),
        ]
        return obj


class Div(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '/')

    def operation(self):
        obj = [
            Instruction("div", "$t0", "$t0", "$t1"),
        ]
        return obj


class Times(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Int'
        super().__init__(line, column, expr1, expr2, ['Int'],'Int', '*')

    def operation(self):
        obj = [
            Instruction("mul", "$t0", "$t0", "$t1"),
        ]
        return obj


class Less(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Bool'
        super().__init__(line, column, expr1, expr2, ['Int'],'Bool', '<')

    def operation(self):
        obj = [
            Instruction("slt", "$t0", "$t0", "$t1"),
            Instruction("jal", "set_bool")
        ]
        return obj


class LessEqual(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:

        super().__init__(line, column, expr1, expr2, ['Int'],'Bool', '<=')

    def operation(self):
        obj = [
            Instruction("sgt", "$t2", "$t0", "$t1"),
            Instruction("seq", "$t3", "$t0", "$t1"),
            Instruction("or", "$t0", "$t2", "$t3"),
            Instruction("jal", "set_bool")
        ]
        return obj


class Equal(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        
        super().__init__(line, column, expr1, expr2, ['All'],'Bool', '=')

    def operation(self):
        obj = [
            Instruction("seq", "$t0", "$t0", "$t1"),
            Instruction("jal", "set_bool")
        ]
        return obj


class Not(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Bool'],'Bool', 'not')

    def operation(self):
        obj = [
            Instruction("xori", "$t0", "$t0", "1"),
        ]
        return obj


class Bitwise(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Int'],'Int', '~')

    def operation(self):
        obj = [
            Instruction("and", "$t0", "$t0", "$t1"),
        ]
        return obj
