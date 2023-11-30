from ast_ import *
from constants import LABEL_STR_LITERAL, LABEL_INT_LITERAL
from collections import defaultdict
from enviroment import Environment

class CILCodeGenerator:
    """
    Generates Code Intermediate Language (CIL) from an Abstract Syntax Tree (AST) for the Cool programming language.
    """

    def __init__(self, cls_refs):
        """
        Initializes the CILCodeGenerator with the provided class references.

        Args:
            cls_refs (dict): A dictionary containing references to Cool classes.
        """
        self.cls_refs = cls_refs
        self.attrs = List()  # to hold attributes
        self.cil_code = CILCode(List(), List(), defaultdict(lambda: []), {})
        self.pos = -1
        self.max_idx = -1
        self.cur_env = None  # environment for locals only
        self.cur_cls = None

        # save empty string literal
        self._save_str_literal('')

        # save 0 int literal
        self._save_int_literal(0)

    @staticmethod
    def get_default_value(_type):
        """
        Gets the default value for a given Cool type.

        Args:
            _type (str): The name of the Cool type.

        Returns:
            Expr: The default value for the specified type in CIL.
        """
        expr = Void()

        if _type == 'Bool':
            expr = Bool('false')
        elif _type == 'String':
            expr = String('')
        elif _type == 'Int':
            expr = Int('0')

        return expr

    def _save_str_literal(self, value):
        """
        Saves a string literal in the CIL code and returns its label.

        Args:
            value (str): The string value to be saved.

        Returns:
            str: The label assigned to the saved string literal.
        """
        if value not in self.cil_code.str_literals:
            label = f'{LABEL_STR_LITERAL}{len(self.cil_code.str_literals)}'
            self.cil_code.str_literals[value] = label

            self._save_int_literal(len(value))

    def _save_int_literal(self, value):
        """
        Saves an integer literal in the CIL code and returns its label.

        Args:
            value (int): The integer value to be saved.

        Returns:
            str: The label assigned to the saved integer literal.
        """
        if value not in self.cil_code.int_literals:
            label = f'{LABEL_INT_LITERAL}{len(self.cil_code.int_literals)}'
            self.cil_code.int_literals[value] = label

    def get_declaration_expression(self, node):
        """
        Gets the declaration expression for a given node.

        Args:
            node (ASTNode): The node for which to generate the declaration expression.

        Returns:
            Expr: The declaration expression in CIL.
        """
        expr = self.get_default_value(node.type.value)

        if node.opt_expr_init:
            expr = self.visit(node.opt_expr_init)

        return expr

    def visit(self, node):
        """
        Applies the Visitor pattern to traverse the AST and generate CIL code.

        Args:
            node (ASTNode): The current node being visited in the AST.

        Returns:
            Expr: The result of visiting the given AST node.
        """
        fn = getattr(self, 'visit_' + node.__class__.__name__)
        res = fn(node)

        return res
    
    # Atomic Expressions
    def visit_Int(self, node):
        int_value = int(node.value)
        self._save_int_literal(int_value)
        return int_value

    def visit_Bool(self, node):
        return Bool(node.value)

    def visit_String(self, node):
        str_literal = String(node.value)
        self._save_str_literal(str_literal)
        return str_literal

    def visit_Id(self, node):
        reference = Reference(node.value)

        if reference.name == 'self':
            return reference

        target = self.current_environment.get(reference.name)

        if target is None:
            assert reference.name in self.attribute_dictionary
            reference.refers_to = ('attr', self.attribute_dictionary[reference.name])
        else:
            reference.refers_to = ('local', target)

        return reference

    def visit_New(self, node):
        return New(node.type_name)

    # Arithmetic Operations
    def visit_Plus(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Plus(left_expression, right_expression)

    def visit_Minus(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Minus(left_expression, right_expression)

    def visit_Mult(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Star(left_expression, right_expression)

    def visit_Div(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Div(left_expression, right_expression)

    # Comparison Operations
    def visit_Eq(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Eq(left_expression, right_expression)

    def visit_Less(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Less(left_expression, right_expression)

    def visit_LessEq(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return LessEq(left_expression, right_expression)

    # Unary Operations
    def visit_IsVoid(self, node):
        expression_to_check = self.visit(node.expr)
        return IsVoid(expression_to_check)

    def visit_IntComp(self, node):
        expression_to_compare = self.visit(node.expr)
        return IntComp(expression_to_compare)

    def visit_Not(self, node):
        expression_to_negate = self.visit(node.expr)
        return Not(expression_to_negate)

    # Control Flow Operations
    def visit_If(self, node):
        condition = self.visit(node.predicate)
        if_branch = self.visit(node.if_branch)
        else_branch = self.visit(node.else_branch)
        return If(condition, if_branch, else_branch)

    def visit_While(self, node):
        condition = self.visit(node.predicate)
        body = self.visit(node.body)
        return While(condition, body)

    # Let Expression
    def visit_LetVar(self, node):
        pass

    def visit_Let(self, node):
        pass

    # Case Expression
    def visit_CaseVar(self, node):
        pass

    def visit_CaseBranch(self, node):
        pass

    def visit_Case(self, node):
        pass

   # Dispatch Operation
    def visit_Dispatch(self, node):
        expression = self.visit(node.expr)
        optional_class = node.opt_type.value if node.opt_type else None
        method_name = node.id.value
        arguments = List([self.visit(arg) for arg in node.expr_list])
        return FunctionCall(expression, optional_class, method_name, arguments)

    # Assignment Operation
    def visit_Assignment(self, node):
        variable_reference = self.visit(node.id)
        expression = self.visit(node.expr)
        return Binding(variable_reference, expression)

    # Block Operation
    def visit_Block(self, node):
        expressions = List([self.visit(expr) for expr in node.expr_list])
        return Block(expressions)

    # Self Type Handling
    def visit_Self_Type(self, node):
        pass

    # Class Definition
    def visit_Class(self, node):
        pass

    def visit_Formal(self, node):
        pass

    def visit_Attribute(self, node):
        pass
    