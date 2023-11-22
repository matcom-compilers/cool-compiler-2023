from typing import List

from src.COOL.token import Token


class If(Token):
    def __init__(self, line: int, if_expr: Token, then_expr: Token, else_expr: Token):
        self.if_expr: Token = if_expr
        self.then_expr: Token = then_expr
        self.else_expr: Token = else_expr
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()


class While(Token):
    def __init__(self, line: int, while_expr: Token, loop_expr: Token):
        self.while_expr: Token = while_expr
        self.loop_expr: Token = loop_expr
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()


class Let(Token):
    def __init__(self, line: int, let_list: List[Token], expr: Token):
        self.let_list: List[Token] = let_list
        self.expr: Token = expr
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()


class Case(Token):
    def __init__(self, line: int, expr: Token, cases: List[Token]):
        self.expr: Token = expr
        self.cases: List[Token] = cases
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()


class New(Token):
    def __init__(self, line: int, type: str):
        self.type: str = type
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()


class Isvoid(Token):
    def __init__(self, line: int, expr: Token):
        self.expr: Token = expr
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()


class Expr(Token):
    def __init__(self, line: int, expr: Token, id: str, type: str = None, exprs: List[Token] = None):
        self.expr: Token = expr
        self.id: str = id
        self.type: str = type
        self.exprs: List[Token] = exprs
        super().__init__(line)
    
    def check(self):
        raise NotImplementedError()
    
    def execute(self):
        raise NotImplementedError()
