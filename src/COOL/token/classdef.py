from typing import Any
from typing import List

from src.COOL.semantic.visitor import Visitor
from src.COOL.token import Token
from src.COOL.token.method import Method
from src.COOL.token.attribute import Attribute


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
    
    def check(self, visitor:Visitor):
        visitor.visit_class(self)
        for feature in self.features:
            feature.check(visitor)
