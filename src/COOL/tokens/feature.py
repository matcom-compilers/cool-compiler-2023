from typing import List

from tokens import Token


class Method(Token):
    def __init__(self, line: int, id: str, type: str, expr: Token, formals: List[Token]) -> None:
        self.type: str = type
        self.expr: Token = expr
        self.id = id
        self.formals: List[Token] = formals
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()
    
    def check(self):
        raise NotImplementedError()


class ExecuteMethod(Token):
    def __init__(self, line: int, id: str, exprs: List[Token]) -> None:
        self.exprs: List[Token] = exprs
        self.id = id
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()
    
    def check(self):
        raise NotImplementedError()


class Attribute(Token):
    def __init__(self, line: int, id: str, type: str = None, expr: Token = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()
    
    def check(self):
        raise NotImplementedError()
