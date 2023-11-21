from abc import abstractmethod

from src.COOL.token import Token


class Operator(Token):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        self.expr1: Token = expr1
        self.expr2: Token = expr2
        super().__init__(line)
    
    def execute(self):
        return self.operator(self.expr1.execute(), self.expr2.execute())

    @abstractmethod
    def operator(self):
        pass

    def check(self):
        raise NotImplementedError()

class Add(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x + y

class Sub(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x - y

class Div(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x / y

class Times(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x * y

class Less(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x < y

class LessEqual(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x <= y

class Equal(Operator):
    def __init__(self, line: int, expr1: Token, expr2: Token) -> None:
        super().__init__(line, expr1, expr2)
    
    def operator(self):
        return lambda x, y: x == y

class Not(Operator):
    def __init__(self, line: int, expr: Token) -> None:
        self.expr = expr
    
    def execute(self):
        return self.operator(self.expr.execute())

    def operator(self):
        return lambda x: not x

class Bitwise(Operator):
    def __init__(self, line: int, expr: Token) -> None:
        self.expr = expr
    
    def execute(self):
        return self.operator(self.expr.execute())

    def operator(self):
        return lambda x: ~x
