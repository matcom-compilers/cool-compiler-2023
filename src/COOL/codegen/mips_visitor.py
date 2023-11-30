

class MipsVisitor:
    def __init__(self) -> None:
        # global data
        self.data_secction = []
        self.types = []
        
        # memory
        self.class_memory = 0

        # current
        self.current_class = None
        self.current_method = None
        self.current_expression = None

        self.attributes = []
    
    def generate_mips(self) -> str:
        """
        Generate the mips code from the visitor data.

        Return:
            str: mips code.
        """

    def visit_program(self, _program):
        for _class in _program.classes:
            self.types.append(_class.type)
    
    def unvisit_program(self, _program):
        pass

    def visit_class(self, _class):
        self.current_class = _class.type
        self.class_memory = 0
    
    def unvisit_class(self, _class):
        self.current_class = None
        self.class_memory = 0
    
    def visit_attribute(self, _attribute):
        pass

    def unvisit_attribute(self, _attribute):
        pass
    
    # def visit_method(self, method):
    #     pass
    
    # def visit_expression(self, expression):
    #     pass
    
    # def visit_assign(self, assign):
    #     pass
