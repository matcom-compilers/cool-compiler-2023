from utils.visitor import Visitor


class CILVisitor(Visitor):
    def visit__ProgramNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo ProgramNode
        # ...

    def visit__TypeNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo TypeNode
        # ...

    def visit__AttributeNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo AttributeNode
        # ...

    def visit__MethodNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo MethodNode
        # ...

    def visit__DataNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo DataNode
        # ...

    def visit__FunctionNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo FunctionNode
        # ...

    def visit__ParamNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo ParamNode
        # ...

    def visit__LocalNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo LocalNode
        # ...

    def visit__VariableNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo VariableNode
        # ...

    def visit__InstructionNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo InstructionNode
        # ...

    # Aquí agregarías métodos visit__ específicos para cada tipo de instrucción
    # Por ejemplo:
    def visit__AssignNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo AssignNode
        # ...

    def visit__ArithmeticNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo ArithmeticNode
        # ...

    # Y así sucesivamente para los otros tipos de nodos...
