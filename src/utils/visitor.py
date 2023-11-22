class Visitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        method = getattr(self, method_name, self.visit_default)
        return method(node)

    def visit_default(self, node):
        raise NotImplementedError(f'No visit_{type(node).__name__} method')
