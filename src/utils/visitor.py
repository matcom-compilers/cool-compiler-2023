class Visitor:
    def visit(self, node):
        method_name = "visit__" + type(node).__name__
        method = getattr(self, method_name, self.visit__default)
        return method(node)

    def visit__default(self, node):
        raise NotImplementedError(f"No visit__{type(node).__name__} method")