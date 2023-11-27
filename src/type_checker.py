from errors import SemanticError, AttributeError
from enviroment import Environment
from ast_ import Class, Attribute, Id, Type

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
        self.class_references = class_references
        self.traversal_counter = 0
        self._initialize_order(ast_root, Environment())

    def _initialize_order(self, current_node, current_environment):
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
            old_method = current_environment.get(method_name)

            if old_method and old_method.get_signature() != method_ref.get_signature():
                raise SemanticError(
                    method_ref.id.line,
                    method_ref.id.col,
                    f'{method_ref} of {current_node} is not compatible with {old_method} for inheritance'
                )

            # Define the method in the environment
            current_environment.define(method_name, method_ref)

            # Precalculate static type of formals before doing visitor
            for formal in method_ref.formal_list:
                if formal.type.value == 'Self_Type':
                    raise SemanticError(
                        formal.type.line,
                        formal.type.col,
                        f'Tried to declare {formal} with {formal.type}'
                    )

                formal.set_static_type(self._get_correct_type(formal, current_node.self_type))

        # Traverse children nodes
        for child_node in current_node.children:
            child_node.parent = current_node
            child_node.level = current_node.level + 1

            self._initialize_order(child_node, Environment(current_environment))

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
            default_type: The default type to use if the node's type is 'Self_Type'.

        Returns:
            Type: The correct type for the node.
        """
        if node.type.value == 'Self_Type':
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
        try:
            method_name = 'visit_' + node.__class__.__name__
            visit_method = getattr(self, method_name)
            return visit_method(node)
        except:
            raise AttributeError(node.type.line, node.type.col, f'Visit method not implemented for node type: {node.__class__.__name__}')

    # Atomic Expressions
    def visit_Id(self, node):
        pass

    def visit_Int(self, node):
        pass

    def visit_Bool(self, node):
        pass

    def visit_String(self, node):
        pass

    def visit_New(self, node):
        pass

    # Arithmetic Operations
    def visit_Plus(self, node):
        pass

    def visit_Minus(self, node):
        pass
    
    def visit_Mult(self, node):
        pass

    def visit_Div(self, node):
        pass

    # Comparison Operations
    def visit_Less(self, node):
        pass

    def visit_LessEq(self, node):
        pass

    def visit_Eq(self, node):
        pass

    # Unary Operations
    def visit_IntComp(self, node):
        pass

    def visit_Not(self, node):
        pass

    def visit_IsVoid(self, node):
        pass

    # Control Flow Operations
    def visit_If(self, node):
        pass

    def visit_While(self, node):
        pass

    # Let Expression
    def visit_Let(self, node):
        pass
    
    def visit_LetVar(self, node):
        pass
    
    def visit_Formal(self, formal_node):
        # Handle type checking for Formal nodes
        # ...
        pass 

    # Case Expression
    def visit_Case(self, node):
        pass

    def visit_CaseVar(self, node):
        pass

    # Dispatch Operation
    def visit_Dispatch(self, node):
        pass

    # Assignment Operation
    def visit_Assignment(self, node):
        pass
    def visit_Block(self, node):
        pass

    # Self Type Handling
    def visit_Self_Type(self, node):
        pass

    # Class Definition
    def visit_Class(self, node):
        """
        Visit method for handling Class nodes.

        Args:
            node: The Class node.

        Returns:
            The result of visiting the Class node.
        """
        old_environment = self.current_environment
        self.current_environment = Environment(old_environment)

        old_class = self.current_class
        self.current_class = node

        self.current_environment.define('self', Attribute(Id('self'), Type('Self_Type'), None))

        for feature in node.feature_list:
            if isinstance(feature, Attribute):
                if self.current_environment.get(feature.id.value):
                    raise SemanticError(feature.id.line, feature.id.col, f'Tried to redefine {feature} by inheritance')

                self.current_environment.define(feature.id.value, feature)

        for feature in node.feature_list:
            self.visit(feature)

        for cls in node.children:
            self.visit(cls)

        self.current_environment = old_environment
        self.current_class = old_class

    def visit_Method(self, method_node):
        # Handle type checking for Method nodes
        # ...
        pass 

    def visit_Attribute(self, attribute_node):
        # Handle type checking for Attribute nodes
        # ...
        pass 

    def perform_type_checking(self):
        # Entry point for type checking
        # ...
        pass 
