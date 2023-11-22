from semantic.context import Context
from utils.loggers import LoggerUtility
from utils.visitor import Visitor

log = LoggerUtility().get_logger()


class TypeChecker(Visitor):
    def __init__(self, context: Context, errors=None) -> None:
        super().__init__()
        self.context = context
        self.errors = errors if errors else []

    def error(self, message, location, type, value):
        self.errors.append(f"({location[0]}, {location[1]}) - {message}")
        log.debug(
            message,
            extra={"type": type, "location": location, "value": value},
        )

    def visit_ProgramNode(self, node):
        pass  # TODO: Implement

    def visit_ClassNode(self, node):
        pass  # TODO: Implement

    def visit_FeatureNode(self, node):
        pass  # TODO: Implement

    def visit_MethodNode(self, node):
        pass  # TODO: Implement

    def visit_AttributeNode(self, node):
        pass  # TODO: Implement

    def visit_FormalNode(self, node):
        pass  # TODO: Implement

    def visit_ExpressionNode(self, node):
        pass  # TODO: Implement

    def visit_AssignNode(self, node):
        pass  # TODO: Implement

    def visit_DispatchNode(self, node):
        pass  # TODO: Implement

    def visit_BinaryOperatorNode(self, node):
        pass  # TODO: Implement

    def visit_UnaryOperatorNode(self, node):
        pass  # TODO: Implement

    def visit_IfNode(self, node):
        pass  # TODO: Implement

    def visit_WhileNode(self, node):
        pass  # TODO: Implement

    def visit_BlockNode(self, node):
        pass  # TODO: Implement

    def visit_LetNode(self, node):
        pass  # TODO: Implement

    def visit_CaseNode(self, node):
        pass  # TODO: Implement

    def visit_CaseOptionNode(self, node):
        pass  # TODO: Implement

    def visit_NewNode(self, node):
        pass  # TODO: Implement

    def visit_IsVoidNode(self, node):
        pass  # TODO: Implement

    def visit_NotNode(self, node):
        pass  # TODO: Implement

    def visit_IdentifierNode(self, node):
        pass  # TODO: Implement

    def visit_IntegerNode(self, node):
        pass  # TODO: Implement

    def visit_StringNode(self, node):
        pass  # TODO: Implement

    def visit_BooleanNode(self, node):
        pass  # TODO: Implement

    def visit_MethodCallNode(self, node):
        pass  # TODO: Implement
