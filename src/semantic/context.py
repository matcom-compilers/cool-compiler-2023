from .types import SemanticError, Type


class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name: str) -> Type:
        assert name not in self.types
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name: str) -> Type:
        assert name in self.types
        return self.types[name]

    def type_exists(self, name: str) -> bool:
        return name in self.types

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)
