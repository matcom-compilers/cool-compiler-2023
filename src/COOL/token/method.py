from typing import Any
from typing import List

from src.COOL.token import Token


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
