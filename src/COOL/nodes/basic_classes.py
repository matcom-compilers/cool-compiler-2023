from typing import List
from COOL.nodes.feature import Method, Formal

class BasicClass:
    def __init__(self,features: list=[], type: str = 'Object', inherits: str = None) -> None:
        self.features = features
        self.type = type
        self.inherits = inherits
        self.methods = []
        self.attributes = []
        self.lineage = []
        self.methods_dict = {}

    def check(self,visitor):
        return self.type


class BasicObject(BasicClass):
    def __init__(self) -> None:
        self.features:list = [
            Method(line=0, column=0, id='abort', type='Object', expr=None, formals=[]),
            Method(line=0, column=0, id='type_name', type='String', expr=None, formals=[]),
            Method(line=0, column=0, id='copy', type='SELF_TYPE', expr=None, formals=[])
        ]
        self.inherits: str = None
        self.type: str = 'Object'
        
        super().__init__(self.features, self.type, self.inherits)


class BasicIO(BasicClass):
    def __init__(self) -> None:
        self.features:list = [
            Method(line=0, column=0, id='out_string', type='SELF_TYPE', expr=None, formals=[Formal(line=0, column=0, id='x', type='String')]),
            Method(line=0, column=0, id='out_int', type='Int', expr=None, formals=[Formal(line=0, column=0, id='x', type='Int')]),
            Method(line=0, column=0, id='in_string', type='String', expr=None, formals=[]),
            Method(line=0, column=0, id='in_int', type='Int', expr=None, formals=[])
        ]
        self.inherits: str = None
        self.type: str = 'IO'
        
        super().__init__(self.features, self.type, self.inherits)

class BasicBool(BasicClass):
    def __init__(self, features: list=[], type: str = 'Bool', inherits: str = None) -> None:
        super().__init__( features, type, inherits)


class BasicInt(BasicClass):
    def __init__(self, features: list=[], type: str = 'Int', inherits: str = None) -> None:
        super().__init__(features, type, inherits)

class BasicString(BasicClass):
    def __init__(self, features: list=[], type: str = 'String', inherits: str = None) -> None:
        super().__init__( features, type, inherits)
