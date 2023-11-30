from abc import abstractmethod

from COOL.nodes import Node


class UnaryOperator(Node):
    def __init__(self, line: int, column: int, expr: Node, possibles_types:list, return_type:str) -> None:
        self.expr: Node = expr
        self.possibles_types = possibles_types
        self.return_type = return_type
        super().__init__(line, column)

    def execute(self):
        return self.operator(self.expr.execute())

    @abstractmethod
    def operator(self):
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

    def execute(self):
        return self.operator(self.expr1.execute(), self.expr2.execute())

    @abstractmethod
    def operator(self):
        pass

    def check(self,visitor):
        return visitor.visit_operator(self)

class Add(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operator(self):
        return lambda x, y: x + y


class Sub(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operator(self):
        return lambda x, y: x - y


class Div(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operator(self):
        return lambda x, y: x / y


class Times(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Int'
        super().__init__(line, column, expr1, expr2, ['Int'],'Int')

    def operator(self):
        return lambda x, y: x * y


class Less(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        self.possibles_types = ['Int']
        self.return_type = 'Bool'
        super().__init__(line, column, expr1, expr2, ['Int'],'Bool')

    def operator(self):
        return lambda x, y: x < y


class LessEqual(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:

        super().__init__(line, column, expr1, expr2, ['Int'],'Bool')

    def operator(self):
        return lambda x, y: x <= y


class Equal(Operator):
    def __init__(self, line: int, column: int, expr1: Node, expr2: Node) -> None:
        
        super().__init__(line, column, expr1, expr2, ['All'],'Bool')

    def operator(self):
        return lambda x, y: x == y


class Not(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Bool'],'Bool')

    def operator(self):
        return lambda x: not x


class Bitwise(UnaryOperator):
    def __init__(self, line: int, column: int, expr: Node) -> None:
        super().__init__(line, column, expr, ['Int'],'Int')

    def operator(self):
        return lambda x: ~x
