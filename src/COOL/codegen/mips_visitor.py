from COOL.codegen.codegen_rules import DATA_SECTION
from COOL.codegen.codegen_rules import TEXT_SECTION
from COOL.codegen.codegen_rules import CREATE_CLASS
from COOL.codegen.codegen_rules import REQUEST_MEMORY
from COOL.codegen.codegen_rules import CREATE_FUNCTION


class MipsVisitor:
    def __init__(self) -> None:
        # global data
        self.data_secction = []
        self.classes = {}
        self.methods = {}
        self.types = []
        
        # memory
        self.class_memory = 0

        # current
        self.current_class = None
        self.current_method = None
        self.current_expression = None
        self.attributes = []
        self.expressions = []
    
    def generate_mips(self) -> str:
        """
        Generate the mips code from the visitor data.

        Return:
            str: mips code.
        """
        data_section = DATA_SECTION
        for _data in self.data_secction:
            data_section += _data

        text_section = TEXT_SECTION
        for _cls in self.classes.keys():
            attributes = self.classes[_cls]["attributes"]
            memory = self.classes[_cls]["memory"]
            methods = self.classes[_cls]["methods"]
            
            text_section +=\
            CREATE_CLASS.format(
                class_name=_cls,
                attributes="\n".join(attributes),
                request_memory=REQUEST_MEMORY.format(memory=memory),
            )
            
            for _method in methods.keys():
                text_section +=\
                CREATE_FUNCTION.format(
                    function_name=_method,
                    class_name=_cls,
                )
                text_section += "\n".join(methods[_method])
        
        return data_section + text_section
    
    def add_data(self, _data: str):
        self.data_secction.append(_data)

    def visit_program(self, _program):
        for _class in _program.classes:
            self.types.append(_class.type)
    
    def unvisit_program(self, _program):
        pass

    def visit_class(self, _class):
        self.current_class = _class.type
        self.class_memory = 0
    
    def unvisit_class(self, _class):
        # TODO: request memory
        self.classes[_class.type] = {
            "memory": self.class_memory,
            "attributes": self.attributes,
            "methods": self.methods,
        }
        self.methods = {}
        self.attributes = []
        self.current_class = None
        self.class_memory = 0
    
    def visit_attribute(self, _attribute):
        pass

    def add_attribute(self, _attribute: str):
        self.attributes.append(_attribute)

    def unvisit_attribute(self, _attribute):
        pass

    def visit_method(self, _method):
        # TODO: method name {class}_{method} ?
        self.current_method = _method.id
        self.expressions = []
    
    def unvisit_method(self, _method):
        self.methods[self.current_method] = self.expressions
        self.current_method = None
        self.expressions = []

    def add_expression(self, _expression: str):
        self.expressions.append(_expression)
