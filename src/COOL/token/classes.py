from typing import Any
from typing import List

from src.COOL.token import Token
from src.COOL.token.method import Method
from src.COOL.token.attribute import Attribute


class Class(Token):
    def __init__(self, line: int, features: List[Method | Attribute]) -> None:
        self.features = features
        super().__init__(line)
