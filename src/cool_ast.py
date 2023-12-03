from typing import List, Tuple

class Node:
    def __init__(self):
        self.line = 0
        self.col = 0

    def get_position(self) -> Tuple[int, int]:
        return self.line, self.col

    def set_position(self, line: int, col: int) -> None:
        self.line = line
        self.col = col


class ProgramNode(Node):
    def __init__(self, declarations):
        Node.__init__(self)
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ClassNode(DeclarationNode):
    def __init__(self, id_, features, parent):
        Node.__init__(self)
        self.id = id_
        self.features = features
        self.parent = parent


class AttributeNode(DeclarationNode):
    def __init__(self, id_, type_, expression=None):
        Node.__init__(self)
        self.id = id_
        self.type = type_
        self.expr = expression


class MethodNode(DeclarationNode):
    def __init__(self, id_, params, body, return_type):
        Node.__init__(self)
        self.id = id_
        self.params = params
        self.body = body
        self.return_type = return_type


class ParamNode(DeclarationNode):
    def __init__(self, id_, type_):
        Node.__init__(self)
        self.id = id_
        self.type = type_


class ExpressionNode(Node):
    pass


class VariableNode(ExpressionNode):
    def __init__(self, id_, type_, expression: ExpressionNode):
        Node.__init__(self)
        self.id = id_
        self.type = type_
        self.expr = expression


class AssignmentNode(ExpressionNode):
    def __init__(self, id_, expression: ExpressionNode):
        Node.__init__(self)
        self.id = id_
        self.expr = expression


# Method Call
class DispatchNode(ExpressionNode):
    def __init__(self, id_, expression: ExpressionNode, arguments, type_=None):
        Node.__init__(self)
        self.id = id_
        self.expr = expression
        self.args = arguments
        self.type = type_


class ConditionalNode(ExpressionNode):
    def __init__(
        self,
        if_expression: ExpressionNode,
        then_expression: ExpressionNode,
        else_expression: ExpressionNode,
    ):
        Node.__init__(self)
        self.if_expr = if_expression
        self.then_expr = then_expression
        self.else_expr = else_expression


class LoopNode(ExpressionNode):
    def __init__(
        self, while_expression: ExpressionNode, loop_expression: ExpressionNode
    ):
        Node.__init__(self)
        self.while_expr = while_expression
        self.loop_expr = loop_expression


class BlockNode(ExpressionNode):
    def __init__(self, expressions_list: List[ExpressionNode]):
        Node.__init__(self)
        self.expr_list = expressions_list


class LetVariableNode(ExpressionNode):
    def __init__(self, id_, type_, expression: ExpressionNode):
        Node.__init__(self)
        self.id = id_
        self.type = type_
        self.expr = expression


class LetNode(ExpressionNode):
    def __init__(
        self, variable_list: List[LetVariableNode], in_expression: ExpressionNode
    ):
        Node.__init__(self)
        self.var_list = variable_list
        self.in_expr = in_expression


class CaseBranchNode(ExpressionNode):
    def __init__(self, id_, type_, expression: ExpressionNode):
        Node.__init__(self)
        self.id = id_
        self.type = type_
        self.expr = expression


class CaseNode(ExpressionNode):
    def __init__(
        self, case_expression: ExpressionNode, case_branches: List[CaseBranchNode]
    ):
        Node.__init__(self)
        self.expr = case_expression
        self.branches = case_branches


class UnaryNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode):
        Node.__init__(self)
        self.expr = expression

class NotNode(UnaryNode):
    pass

class ComplementNode(UnaryNode):
    pass

class AtomicNode(ExpressionNode):
    def __init__(self, var):
        Node.__init__(self)
        self.var = var

class NewNode(AtomicNode):
    pass


class BooleanNode(AtomicNode):
    pass


class IntNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class VarNode(AtomicNode):
    pass

class IsVoidNode(UnaryNode):
    pass


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        Node.__init__(self)
        self.left = left
        self.right = right


class BinaryArithmeticNode(BinaryNode):
    pass


class AdditionNode(BinaryArithmeticNode):
    pass


class SubtractionNode(BinaryArithmeticNode):
    pass


class MultiplicationNode(BinaryArithmeticNode):
    pass


class DivisionNode(BinaryArithmeticNode):
    pass


class ComparisonNode(BinaryNode):
    pass


class LessNode(ComparisonNode):
    pass


class LessEqualNode(ComparisonNode):
    pass

class EqualNode(ComparisonNode):
    pass

