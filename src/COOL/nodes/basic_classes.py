from typing import List

class BasicClass:
    def __init__(self,features: list=[], type: str = 'Object', inherits: str = None) -> None:
        self.features = features
        self.type = type
        self.inherits = inherits
        self.methods = []
        self.attributes = []
        self.lineage = []

    def check(self,visitor):
        return self.type
        

class BasicObject(BasicClass):
    def __init__(self, features: list=[], type: str = 'Object', inherits: str = None) -> None:
        super().__init__(features, type, inherits)


class BasicIO(BasicClass):
    def __init__(self, features: list=[], type: str = 'IO', inherits: str = None) -> None:
        super().__init__(features, type, inherits)


class BasicBool(BasicClass):
    def __init__(self, features: list=[], type: str = 'Bool', inherits: str = None) -> None:
        super().__init__( features, type, inherits)


class BasicInt(BasicClass):
    def __init__(self, features: list=[], type: str = 'Int', inherits: str = None) -> None:
        super().__init__(features, type, inherits)

class BasicString(BasicClass):
    def __init__(self, features: list=[], type: str = 'String', inherits: str = None) -> None:
        super().__init__( features, type, inherits)
