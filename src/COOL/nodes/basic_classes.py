from typing import List
from COOL.nodes.feature import Method, Formal, Attribute

class BasicClass:
    def __init__(self,features: list=[], type: str = 'Object', inherits: str = None) -> None:
        self.features = features
        self.type = type
        self.inherits = inherits
        self.methods = [i for i in features if isinstance(i, Method)]
        self.attributes = [i for i in features if isinstance(i, Attribute)]
        self.lineage = []
        self.methods_dict = {i.id:i for i in features if isinstance(i, Method)}
        self.attributes_dict = {i.id:i for i in features if isinstance(i, Attribute)}

    def check(self, visitor):
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
    def __init__(self) -> None:
        self.features:list = []
        self.inherits: str = None
        self.type: str = 'Bool'
        
        super().__init__(self.features, self.type, self.inherits)


class BasicInt(BasicClass):
    def __init__(self) -> None:
        self.features:list = []
        self.inherits: str = None
        self.type: str = 'Int'
        
        super().__init__(self.features, self.type, self.inherits)

class BasicString(BasicClass):
    def __init__(self) -> None:
        self.features:list = [
                Method(line=0, column=0, id='length', type='Int', expr=None, formals=[]),
                Method(line=0, column=0, id='concat', type='String', expr=None, formals=[Formal(line=0, column=0, id='s', type='String')]),
                Method(line=0, column=0, id='substr', type='String', expr=None, formals=[Formal(line=0, column=0, id='i', type='Int'),Formal(line=0, column=0, id='l', type='Int')])
        ]
      
        self.inherits: str = None
        self.type: str = 'String'
        super().__init__(self.features, self.type, self.inherits)
