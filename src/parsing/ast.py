from collections import namedtuple

Location = namedtuple("Location", ["line", "column"])


class Node:
    def __init__(self, location):
        self.location = location


class ProgramNode(Node):
    def __init__(self, classes, location):
        super().__init__(location)
        self.classes = classes


class ClassNode(Node):
    def __init__(self, name, parent, features, location):
        super().__init__(location)
        self.name = name
        self.parent = parent
        self.features = features


class FeatureNode(Node):
    def __init__(self, location):
        super().__init__(location)


class MethodNode(FeatureNode):
    def __init__(self, name, formals, return_type, body, location):
        super().__init__(location)
        self.name = name
        self.formals = formals
        self.return_type = return_type
        self.body = body


class AttributeNode(FeatureNode):
    def __init__(self, name, attr_type, init, location):
        super().__init__(location)
        self.name = name
        self.attr_type = attr_type
        self.init = init


class FormalNode(Node):
    def __init__(self, name, formal_type, location):
        super().__init__(location)
        self.name = name
        self.formal_type = formal_type


class ExpressionNode(Node):
    def __init__(self, location):
        super().__init__(location)


class AssignNode(ExpressionNode):
    def __init__(self, name, expr, location):
        super().__init__(location)
        self.name = name
        self.expr = expr


class BinaryOperatorNode(ExpressionNode):
    def __init__(self, operator, left, right, location):
        super().__init__(location)
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOperatorNode(ExpressionNode):
    def __init__(self, operator, operand, location):
        super().__init__(location)
        self.operator = operator
        self.operand = operand


class IfNode(ExpressionNode):
    def __init__(self, condition, then_expr, else_expr, location):
        super().__init__(location)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, location):
        super().__init__(location)
        self.condition = condition
        self.body = body


class BlockNode(ExpressionNode):
    def __init__(self, expressions, location):
        super().__init__(location)
        self.expressions = expressions


class LetNode(ExpressionNode):
    def __init__(self, identifier, type, assign_expr, body, location):
        super().__init__(location)
        self.identifier = identifier
        self.type = type
        self.assign_expr = assign_expr
        self.body = body


class CaseNode(ExpressionNode):
    def __init__(self, expr, cases, location):
        super().__init__(location)
        self.expr = expr
        self.cases = cases


class CaseOptionNode(Node):
    def __init__(self, name, type, expr, location):
        super().__init__(location)
        self.name = name
        self.type = type
        self.expr = expr


class NewNode(ExpressionNode):
    def __init__(self, type, location):
        super().__init__(location)
        self.type = type


class IsVoidNode(ExpressionNode):
    def __init__(self, expr, location):
        super().__init__(location)
        self.expr = expr


class NotNode(ExpressionNode):
    def __init__(self, expr, location):
        super().__init__(location)
        self.expr = expr


class IdentifierNode(ExpressionNode):
    def __init__(self, name, location):
        super().__init__(location)
        self.name = name


class IntegerNode(ExpressionNode):
    def __init__(self, value, location):
        super().__init__(location)
        self.value = value


class StringNode(ExpressionNode):
    def __init__(self, value, location):
        super().__init__(location)
        self.value = value


class BooleanNode(ExpressionNode):
    def __init__(self, value, location):
        super().__init__(location)
        self.value = value


class MethodCallNode(ExpressionNode):
    def __init__(self, method, args, location):
        super().__init__(location)
        self.method = method
        self.args = args
