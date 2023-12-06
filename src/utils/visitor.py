class Visitor:
    def visit(self, node, *args, **kwargs):
        method_name = "visit__" + type(node).__name__
        method = getattr(self, method_name, self.visit__default)
        return method(node, *args, **kwargs)

    def visit__default(self, node, *args, **kwargs):
        raise NotImplementedError(f"No visit__{type(node).__name__} method")
