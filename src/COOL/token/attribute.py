from typing import Any
from typing import List

from src.COOL.token import Token


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
