from semantic_analysis.ast_ import *
from utils.constants import LABEL_STR_LITERAL, LABEL_INT_LITERAL
from collections import defaultdict
from utils.enviroment import Environment

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
        self.attributes = List()  # to hold attributes
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
        expr = CILCodeGenerator.get_default_value(node.type.value)

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
        ref = Int(node.value)
        self._save_int_literal(int(ref.value))
        return ref

    def visit_Bool(self, node):
        return Bool(node.value)

    def visit_String(self, node):
        ref = String(node.value)
        self._save_str_literal(ref.value)
        return ref

    def visit_Id(self, node):
        reference = Reference(node.value)

        if reference.name == 'self':
            return reference

        target = self.cur_env.get(reference.name)

        if target is None:
            assert reference.name in self.attribute_dict
            reference.refers_to = ('attr', self.attribute_dict[reference.name])
        else:
            reference.refers_to = ('local', target)

        return reference

    def visit_New(self, node):
        return New(node.type.value)

    # Arithmetic Operations
    def visit_Plus(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Plus(left_expression, right_expression)

    def visit_Minus(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Minus(left_expression, right_expression)

    def visit_Mul(self, node):
        left_expression = self.visit(node.left)
        right_expression = self.visit(node.right)
        return Mul(left_expression, right_expression)

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
        expr_init = self.get_declaration_expression(node)
        self.pos += 1  # Increment the position
        self.max_idx = max(self.max_idx, self.pos)
        self.cur_env.define(node.id.value, self.pos)
        variable_ref = self.visit(node.id)
        return Binding(variable_ref, expr_init)

    def visit_Let(self, node):
        old_environment = self.cur_env
        self.cur_env = Environment(old_environment)

        let_vars = [self.visit(let_var) for let_var in node.let_list]
        body = self.visit(node.body)

        self.pos -= self.cur_env.definitions_count  # Undo the position changes
        self.cur_env = old_environment

        return Let(List(let_vars), body)

    # Case Expression
    def visit_CaseVar(self, node):
        self.pos += 1  # Increment the position
        self.max_idx = max(self.max_idx, self.pos)
        self.cur_env.define(node.id.value, self.pos)

        class_type = self.cls_refs[node.type.value]

        return self.visit(node.id), class_type.td, class_type.tf, class_type.level

    def visit_CaseBranch(self, node):
        old_environment = self.cur_env
        self.cur_env = Environment(old_environment)

        variable_ref, type_description, type_functions, level = self.visit(node.case_var)
        expression = self.visit(node.expr)

        branch = CaseBranch(variable_ref, expression)
        branch.set_times(type_description, type_functions)
        branch.level = level

        self.pos -= self.cur_env.definitions_count  # Undo the position changes
        self.cur_env = old_environment

        return branch

    def visit_Case(self, node):
        expression = self.visit(node.expr)
        branches = List([self.visit(branch) for branch in node.case_list])
        branches.sort(key=lambda x: x.level, reverse=True)  # Sort by greater level

        case_statement = Case(expression, branches)

        return case_statement

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
        old_attributes = self.attributes
        self.attributes = List(old_attributes[:])

        old_environment = self.cur_env
        self.cur_env = Environment(old_environment)

        old_class = self.cur_cls
        self.cur_cls = node

        # Save each class type as a String object in the data segment
        self._save_str_literal(node.type.value)

        # Own attributes
        own_attributes = [feature for feature in node.feat_list if isinstance(feature, Attribute)]

        self.attribute_dict = {}

        # Filling attribute_dict; needed so that references know what attribute they are referring to
        position = 0

        # Ensure that the _type_info attribute will always be at position 0 in the "attribute table"
        assert node.reserved_attrs[0].ref.name == '_type_info'

        for attribute in node.reserved_attrs:  # Reserved attributes
            self.attribute_dict[attribute.ref.name] = position
            position += 1

        for declaration in self.attributes:  # Declarations of attributes from inheritance (instances of AttrDecl)
            self.attribute_dict[declaration.ref.name] = position
            position += 1

        for attribute in own_attributes:  # Own attributes; note that these are instances of Attribute right now
            self.attribute_dict[attribute.id.value] = position
            position += 1

        for feature in node.feat_list:
            self.visit(feature)

        init_function = FuncInit(
            node.type.value,
            self.attributes,
            self.attribute_dict,
            f'{node.type.value}_Init',
            List(node.reserved_attrs),
            node.type_obj
        )

        # Needed for the static data segment of the type
        init_function.td = self.cur_cls.td
        init_function.tf = self.cur_cls.tf

        self.cil_code.init_functions.append(init_function)
        self.cil_code.dict_init_func[init_function.name] = init_function

        for child_class in node.children:
            self.visit(child_class)

        self.pos -= self.cur_env.definitions_count  # Undo
        self.cur_env = old_environment
        self.attributes = old_attributes
        self.cur_cls = old_class

    def visit_Formal(self, node):
        self.pos += 1  # Increment position
        self.max_idx = max(self.max_idx, self.pos)
        self.cur_env.define(node.id.value, self.pos)

        return self.visit(node.id)

    def visit_Method(self, node):
        old_environment = self.cur_env
        self.cur_env = Environment(old_environment)

        assert self.pos == -1
        assert self.max_idx == -1

        formal_parameters = List([self.visit(formal) for formal in node.formal_list])
        body = self.visit(node.expr) if node.expr else None  # If method is not native, visit the body, else None

        new_function = Function(node.id.value, formal_parameters, body, self.max_idx + 1)

        # Needed for fast dispatch
        new_function.td = self.cur_cls.td
        new_function.tf = self.cur_cls.tf
        new_function.level = self.cur_cls.level
        new_function.label = f'{self.cur_cls.type.value}.{new_function.name}'

        self.cil_code.functions.append(new_function)
        self.cil_code.dict_func[new_function.name].append(new_function)

        self.max_idx = -1
        self.pos -= self.cur_env.definitions_count  # Undo
        self.cur_env = old_environment

    def visit_Attribute(self, node):
        assert self.pos == -1
        assert self.max_idx == -1

        reference = self.visit(node.id)
        expression = self.get_declaration_expression(node)

        declaration = AttrDecl(reference, node.type.value, expression, self.max_idx + 1)
        self.attributes.append(declaration)

        self.max_idx = -1    