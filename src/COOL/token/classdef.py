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
        self.type = type
        self.inherits = inherits
        self.features = features
        self.methods= [i for i in features if isinstance(i, Method)]
        self.attributes = [i for i in features if isinstance(i, Attribute)]
        super().__init__(line)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        visitor.visit_class(self)

        self.features = {i.id: i for i in self.features}

        for feature in self.features:
            feature.check(visitor)
