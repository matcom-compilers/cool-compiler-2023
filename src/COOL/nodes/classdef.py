from typing import List
from typing import Tuple

from COOL.semantic.visitor import Visitor
from COOL.nodes import Node
from COOL.nodes.feature import Method
from COOL.nodes.feature import Attribute


# TODO: data and text can be a list?
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

    def execute(self) -> Tuple[List[str], List[str]]:
        data, text = [], []
        for _feature in self.features:
            feature_data, feature_text = _feature.execute()
            data.extend(feature_data)
            text.extend(feature_text)
        return data, text

    def check(self, visitor: Visitor):
        visitor.visit_class(self)

        for feature in self.features:
            feature.check(visitor)
