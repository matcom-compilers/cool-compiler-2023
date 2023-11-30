from typing import List
from typing import Tuple

from COOL.semantic.visitor import Visitor_Program, Visitor_Class
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
        self.inherits_instance: Class = None
        super().__init__(line,column)

    def execute(self) -> Tuple[List[str], List[str]]:
        data, text = [], []
        for _feature in self.features:
            feature_data, feature_text = _feature.execute()
            data.extend(feature_data)
            text.extend(feature_text)
        return data, text

    def check(self, visitor:Visitor_Program):
        visitor.visit_class(self)
        self.class_visitor =  Visitor_Class( scope= {
            'type': self.type, 
            'inherits': self.inherits, 
            'features': self.features_dict, 
            'methods': self.methods_dict, 
            'attributes': self.attributes_dict, 
            'inherits_instance': self.inherits_instance, 
            'line': self.line, 
            'column': self.column,
            'lineage': self.lineage,
            'all_types':visitor.types,
            'inheritance_tree':visitor.tree,
            'basic_types':visitor.basic_types
            })
        for feature in self.features:
            feature.check(self.class_visitor)
        visitor.errors += self.class_visitor.errors
