from typing import List

from src.COOL.token import Token
from src.COOL.token.feature import Method
from src.COOL.token.feature import Attribute


class Class(Token):
    def __init__(
        self,
        line: int,
        features: List[Method | Attribute],
        type: str,
        inherits: str = None
    ) -> None:
        self.features = features
        self.type = type
        self.inherits = inherits
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()
    
    def check(self):
        raise NotImplementedError()
