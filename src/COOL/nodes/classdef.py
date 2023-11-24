from typing import List

from nodes import Node
from nodes.feature import Method
from nodes.feature import Attribute


class Class(Node):
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
