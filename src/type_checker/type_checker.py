from utils.errors import SemanticError, AttributeError
from utils.enviroment import Environment
from semantic_analysis.ast_ import Class, Attribute, Id, Type, Self_Type

class TypeChecker:
    def __init__(self, ast_root, class_references):
        """
        Initialize the TypeChecker.

        Args:
            ast_root: The root node of the Abstract Syntax Tree (AST).
            class_references: A dictionary mapping class names to their corresponding types.

        Attributes:
            class_references: A dictionary mapping class names to their corresponding types.
            traversal_counter: A counter for assigning td and tf values during depth-first traversal.

        Returns:
            None
        """
        
        self.ast_root = ast_root
        self.class_references = class_references
        self.traversal_counter = 0
        self._initialize_order(ast_root, Environment())

        self.current_environment = None
        self.current_class = None

    def _initialize_order(self, current_node, env):
        """
        Initialize the order (td and tf) during depth-first traversal.

        Args:
            current_node: The current node in the AST.
            current_environment: The environment during AST traversal.

        Returns:
            None
        """
        # Increment the traversal counter
        self.traversal_counter += 1
        current_node.td = self.traversal_counter

        # Traverse methods in the current class
        for method_name, method_ref in current_node.methods.items():
            # Check for compatibility with inherited methods
            old_method = env.get(method_name)

            if old_method and old_method.get_signature() != method_ref.get_signature():
                raise SemanticError(
                    method_ref.id.line,
                    method_ref.id.col,
                    f'{method_ref} of {current_node} is not compatible with {old_method} for inheritance'
                )

            # Define the method in the environment
            env.define(method_name, method_ref)

            # Precalculate static type of formals before doing visitor
            for formal in method_ref.formal_list:
                if formal.type.value == 'SELF_TYPE':
                    raise SemanticError(
                        formal.type.line,
                        formal.type.col,
                        f'Tried to declare {formal} with {formal.type}'
                    )

                formal.set_static_type(self._get_correct_type_for_node(formal, current_node.self_type))

        # Traverse children nodes
        for child_node in current_node.children:
            child_node.parent = current_node
            child_node.level = current_node.level + 1

            self._initialize_order(child_node, Environment(env))

        # Set the tf value for the current node
        current_node.tf = self.traversal_counter

    def _is_order_conform(self, node_u, node_v):
        """
        Check if the traversal order of node_u conforms to the order of node_v.

        Args:
            node_u: The first node.
            node_v: The second node.

        Returns:
            bool: True if node_u conforms to node_v in the traversal order, False otherwise.
        """
        return node_v.td <= node_u.td <= node_v.tf

    def _find_least_common_ancestor(self, node_u, node_v):
        """
        Find the least common ancestor of two nodes in the AST.

        Args:
            node_u: The first node.
            node_v: The second node.

        Returns:
            Node: The least common ancestor node.
        """
        while node_u.type.value != node_v.type.value:
            if node_u.level > node_v.level:
                node_u = node_u.parent
            else:
                node_v = node_v.parent

        return node_u

    def _find_method_in_hierarchy(self, class_node, method_name):
        """
        Find the method in the class hierarchy.

        Args:
            class_node: The class node.
            method_name: The name of the method to find.

        Returns:
            Method: The found method or None if not found.
        """
        while class_node and method_name not in class_node.methods:
            class_node = class_node.parent

        return class_node.methods[method_name] if class_node else None

    def _get_correct_type_for_node(self, node, default_type):
        """
        Get the correct type for a given node.

        Args:
            node: The node for which to determine the correct type.
            default_type: The default type to use if the node's type is 'SELF_TYPE'.

        Returns:
            Type: The correct type for the node.
        """
        if node.type.value == 'SELF_TYPE':
            return default_type

        if node.type.value not in self.class_references:
            raise TypeError(node.type.line, node.type.col, f'{Class(node.type)} does not exist')

        return self.class_references[node.type.value]

    # Visitor pattern
    def visit(self, node):
        """
        Dispatch method for visiting different AST node types.

        Args:
            node: The AST node to visit.

        Returns:
            The result of visiting the AST node.
        """
        
        fn = getattr(self, f'visit_{node.__class__.__name__}')
        res = fn(node)
        return res

    # Atomic Expressions
    def visit_Int(self, node):
        node.set_static_type(self.class_references['Int'])

    def visit_String(self, node):
        node.set_static_type(self.class_references['String'])

    def visit_Bool(self, node):
        node.set_static_type(self.class_references['Bool'])

    def visit_Id(self, node):
        ref = self.current_environment.get(node.value)

        if not ref:
            raise NameError(node.line, node.col, f'{node} does not exist in this environment')

        node.set_static_type(self._get_correct_type_for_node(ref, self.current_class.self_type))

    def visit_New(self, node):
        node.set_static_type(self._get_correct_type_for_node(node, self.current_class.self_type))

    # Arithmetic Operations
    def visit_Plus(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.static_type.type.value != 'Int' or node.right.static_type.type.value != 'Int':
            raise TypeError(node.line, node.col, f'{node.left} and {node.right} must both have {self.class_references["Int"]}')

        node.set_static_type(self.class_references['Int'])

    def visit_Minus(self, node):
        self.visit_Plus(node)

    def visit_Mul(self, node):
        self.visit_Plus(node)

    def visit_Div(self, node):
        self.visit_Plus(node)

    # Comparison Operations
    def visit_Eq(self, node):
        self.visit(node.left)
        self.visit(node.right)

        types = ['Int', 'String', 'Bool']

        lft_type = node.left.static_type.type.value
        rgt_type = node.right.static_type.type.value

        if lft_type in types or rgt_type in types:
            if lft_type != rgt_type:
                raise TypeError(node.line, node.col, f'{node.left} with {node.left.static_type} and {node.right} with {node.right.static_type} must both have the same type')

        node.set_static_type(self.class_references['Bool'])

    def visit_Less(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.static_type.type.value != 'Int' or node.right.static_type.type.value != 'Int':
            raise TypeError(node.line, node.col, f'{node.left} and {node.right} must both have {self.class_references["Int"]}')

        node.set_static_type(self.class_references['Bool'])

    def visit_LessEq(self, node):
        self.visit_Less(node)

    # Unary Operations
    def visit_Not(self, node):
        self.visit(node.expr)

        if node.expr.static_type.type.value != 'Bool':
            raise TypeError(node.expr.line, node.expr.col, f'{node.expr} must have {self.class_references["Bool"]}')

        node.set_static_type(self.class_references['Bool'])

    def visit_IsVoid(self, node):
        node.set_static_type(self.class_references['Bool'])
    
    def visit_IntComp(self, node):
        self.visit(node.expr)

        if node.expr.static_type.type.value != 'Int':
            raise TypeError(node.line, node.col, f'{node.expr} must have {self.class_references["Int"]}')

        node.set_static_type(self.class_references['Int'])

    # Control Flow Operations
    def visit_If(self, node):
        self.visit(node.predicate)

        predicate_type = node.predicate.static_type

        if predicate_type.type.value != 'Bool':
            raise TypeError(node.predicate.line, node.predicate.col, f'{node} predicate must have {self.class_references["Bool"]}, not {predicate_type}')

        self.visit(node.if_branch)
        self.visit(node.else_branch)

        node.set_static_type(self._find_least_common_ancestor(node.if_branch.static_type, node.else_branch.static_type))

    def visit_While(self, node):
        self.visit(node.predicate)

        predicate_type = node.predicate.static_type

        if predicate_type.type.value != 'Bool':
            raise TypeError(node.predicate.line, node.predicate.col, f'{node} predicate must have {self.class_references["Bool"]}, not {predicate_type}')

        self.visit(node.body)

        node.set_static_type(self.class_references['Object'])

    # Let Expression
    def visit_LetVar(self, node):
        if node.id.value == 'self':
            raise SemanticError(node.id.line, node.id.col, f'Tried to assign to {node.id}')

        if node.opt_expr_init:
            expr = node.opt_expr_init
            self.visit(expr)

            self.current_environment.define(node.id.value, node)
            self.visit(node.id)
            node.set_static_type(node.id.static_type)

            if not self._is_order_conform(expr.static_type, node.static_type):
                raise TypeError(node.line, node.col, f'{expr} with {expr.static_type} doesnt conform to {node} with {node.static_type}')

        else:
            self.current_environment.define(node.id.value, node)
            self.visit(node.id)
            node.set_static_type(node.id.static_type)

    def visit_Let(self, node):
        old_env = self.current_environment
        self.current_environment = Environment(old_env)

        for let_var in node.let_list:
            self.visit(let_var)

        self.visit(node.body)
        node.set_static_type(node.body.static_type)

        self.current_environment = old_env

    # Case Expression
    def visit_CaseVar(self, node):
        if node.id.value == 'self':
            raise SemanticError(node.id.line, node.id.col, f'Tried to assign to {node.id}')

        if node.type.value == 'SELF_TYPE':
            raise SemanticError(node.type.line, node.type.col, f'Tried to declare {node} with {node.type}')
        
        self.current_environment.define(node.id.value, node)
        self.visit(node.id)
        node.set_static_type(node.id.static_type)

    def visit_Case(self, node):
        self.visit(node.expr)

        type_dict = {}
        lca = None

        for branch in node.case_list:
            if branch.case_var.type.value in type_dict:
                raise SemanticError(branch.case_var.type.line, branch.case_var.type.col, f'{branch.case_var.type} appears in other branch of {node}')

            type_dict[branch.case_var.type.value] = True

            old_env = self.current_environment
            self.cur_env = Environment(old_env)

            self.visit(branch.case_var)
            self.visit(branch.expr)

            if not lca:
                lca = branch.expr.static_type

            else: lca = self._find_least_common_ancestor(lca, branch.expr.static_type)

            self.current_environment = old_env

        node.set_static_type(lca)

    # Dispatch Operation
    def visit_Dispatch(self, node):
        """
        Handle type checking for Dispatch nodes.

        Args:
            node: The Dispatch node to perform type checking on.

        Returns:
            None
        """
        for expr in node.expr_list:
            self.visit(expr)

        self.visit(node.expr)
        cls = None

        if node.opt_type:  # Static dispatch
            if node.opt_type.value == 'SELF_TYPE':
                raise SemanticError(node.opt_type.line, node.opt_type.col, f'Cannot perform static dispatch on {node.opt_type}')

            if node.opt_type.value not in self.class_references:
                raise TypeError(node.opt_type.line, node.opt_type.col, f'{Class(node.opt_type, None)} does not exist')

            cls = self.class_references[node.opt_type.value]

            if not self._is_order_conform(node.expr.static_type, cls):
                raise TypeError(node.line, node.col, f'Dispatch failed, {node.expr} with {node.expr.static_type} does not conform to {cls}')

        else:
            cls = node.expr.static_type

            # Assert that the static type of node.expr is one of the nodes of the tree and NEVER a declared SELF_TYPE
            # It can be SELF_TYPE(C) though
            assert node.expr.static_type.td > 0

            if isinstance(node.expr.static_type, Self_Type):
                cls = self.current_class

        method = self._find_method_in_hierarchy(cls, node.id.value)

        if not method:
            raise AttributeError(node.line, node.col, f'Dispatch failed: could not find a method with {node.id} in {cls} or any ancestor')

        formals = list(method.formal_list)

        if len(node.expr_list) != len(formals):
            raise SemanticError(node.line, node.col, (f'Dispatch failed, number of arguments of dispatch is {len(node.expr_list)}, '
                                                    f'number of formals is {len(formals)}'))

        for expr, formal in zip(node.expr_list, formals):
            if not self._is_order_conform(expr.static_type, formal.static_type):
                raise TypeError(expr.line, expr.col, f'{expr} with {expr.static_type} does not conform to {formal} with {formal.static_type}')

        node.set_static_type(self._get_correct_type_for_node(method, node.expr.static_type))

    # Assignment Operation
    def visit_Assignment(self, node):
        if node.id.value == 'self':
            raise SemanticError(node.id.line, node.id.col, f'Tried to assign to {node.id}')

        self.visit(node.id)
        self.visit(node.expr)

        if not self._is_order_conform(node.expr.static_type, node.id.static_type):
            raise TypeError(node.line, node.col, f'{node.expr} with {node.expr.static_type} does not conform to {node.id} with {node.id.static_type}')

        node.set_static_type(node.expr.static_type)

    # Block Operation
    def visit_Block(self, node):
        for expr in node.expr_list:
            self.visit(expr)

        node.set_static_type(node.expr_list[-1].static_type)

    # Self Type Handling
    def visit_Self_Type(self, node):
        pass  

    # Class Definition
    def visit_Class(self, node):
        old_environment = self.current_environment
        self.current_environment = Environment(old_environment)

        old_class = self.current_class
        self.current_class = node

        self.current_environment.define('self', Attribute(Id('self'), Type('SELF_TYPE'), None))

        for feature in node.feat_list:
            if isinstance(feature, Attribute):
                if self.current_environment.get(feature.id.value):
                    raise SemanticError(feature.id.line, feature.id.col, f'Tried to redefine {feature} by inheritance')

                self.current_environment.define(feature.id.value, feature)

        for feature in node.feat_list:
            self.visit(feature)

        for cls in node.children:
            self.visit(cls)

        self.current_environment = old_environment
        self.current_class = old_class

    def visit_Method(self, method_node):
        old_environment = self.current_environment
        self.current_environment = Environment(old_environment)

        # Type check formal parameters
        for formal in method_node.formal_list:
            self.visit(formal)

        # Type check the method body
        if method_node.expr:  # If it is not a native method
            self.visit(method_node.expr)

            # Calculate the static type of the method
            static_type = self._get_correct_type_for_node(method_node, self.current_class.self_type)

            # Ensure the body conforms to the declared method type
            if not self._is_order_conform(method_node.expr.static_type, static_type):
                raise TypeError(
                    method_node.expr.line,
                    method_node.expr.col,
                    f'{method_node.expr} with {method_node.expr.static_type} does not conform to {method_node} with {static_type}'
                )

        self.current_environment = old_environment

    def visit_Attribute(self, attribute_node):
        self.visit(attribute_node.id)
        attribute_node.set_static_type(attribute_node.id.static_type)

        # If the attribute has an initialization expression
        if attribute_node.opt_expr_init:
            expr = attribute_node.opt_expr_init
            self.visit(expr)

            # Check conformity between the initialization expression and the declared attribute type
            if not self._is_order_conform(expr.static_type, attribute_node.static_type):
                raise TypeError(
                    attribute_node.line,
                    attribute_node.col,
                    f'{expr} with {expr.static_type} does not conform to {attribute_node} with {attribute_node.static_type}'
                )

    def visit_Formal(self, formal_node):
        if formal_node.id.value == 'self':
            raise SemanticError(formal_node.id.line, formal_node.id.col, f'Tried to assign to {formal_node.id}')

        # Check that the formal is not already defined in the current environment
        if formal_node.id.value in self.current_environment.variables_and_methods:
            raise SemanticError(formal_node.id.line, formal_node.id.col, f'Tried to redefine {formal_node}')

        self.current_environment.define(formal_node.id.value, formal_node)

        self.visit(formal_node.id)
        formal_node.set_static_type(formal_node.id.static_type)
    
    def perform_type_checking(self):
        # Entry point for type checking
        # ...
        pass 
