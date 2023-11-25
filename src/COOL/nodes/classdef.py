from typing import List

from semantic.visitor import Visitor
from nodes import Node
from nodes.feature import Method
from nodes.feature import Attribute


class Class(Node):
    def __init__(
        self,
        line: int,
        column: int,
        features: List[Method | Attribute],
        type: str,
        inherits: str = None
    ) -> None:
        self.type = type
        self.inherits = inherits
        self.features = features
        self.methods = [i for i in features if isinstance(i, Method)]
        self.attributes = [i for i in features if isinstance(i, Attribute)]
        super().__init__(line,column)

    def execute(self):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        visitor.visit_class(self)

        for feature in self.features.values():
            feature.check(visitor)
