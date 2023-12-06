from COOL.codegen.codegen_rules import DATA_SECTION
from COOL.codegen.codegen_rules import TEXT_SECTION
from COOL.codegen.codegen_rules import CREATE_CLASS
from COOL.codegen.codegen_rules import REQUEST_MEMORY
from COOL.codegen.codegen_rules import CREATE_FUNCTION
from COOL.codegen.codegen_rules import FUNCTIONS


# TODO: save the name of variables in stack and then load it
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
        self.current_attribute = None
        self.current_expression = None
        self.attributes = []
        self.expressions = []

        self.vars_method = {}
        self.vars_class = {}
    
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
            # TODO: clean the stack
            for _method in methods.keys():
                text_section +=\
                CREATE_FUNCTION.format(
                    function_name=_method,
                    class_name=_cls,
                    method="\n".join(methods[_method]),
                    clean_stack="    <clean_stack>\n",
                )
        for _function in FUNCTIONS:
            text_section += _function
        
        return data_section + text_section

    @property
    def register_return(self):
        return "$ra"
    
    @property
    def register_stack_pointer(self):
        return "$sp"
    
    @property
    def register_memory_pointer(self):
        return "$v0"
    
    @property
    def register_store_memory(self):
        return "$t7"
    
    @property
    def register_store_results(self):
        return "$t0"

    def get_variable(self, _variable: str):
        """
        Get the variable from the current scope.
        """
        if self.vars_method.get(_variable.id) is not None:
            return self.vars_method[_variable.id]
        if self.vars_class.get(_variable.id) is not None:
            return self.vars_class[_variable.id]
    
    def add_data(self, _data: str):
        """
        Add data to the data section.
        """
        self.data_secction.append(_data)

    def visit_program(self, _program):
        for _class in _program.classes:
            self.types.append(_class.type)
    
    def unvisit_program(self, _program):
        pass

    def visit_class(self, _class):
        self.current_class = _class.type
        self.class_memory = 0
        self.vars_class = {}
    
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
        self.vars_class = {}
    
    def visit_attribute(self, _attribute):
        self.vars_class.update({_attribute.id: f"{self.class_memory}($v0))"})

    def add_attribute(self, _attribute: str):
        self.attributes.append(_attribute)

    def unvisit_attribute(self, _attribute):
        self.class_memory += 4
    
    def add_memory(self, _memory: int):
        self.class_memory = _memory

    def visit_method(self, _method):
        # TODO: method name {class}_{method} ?
        self.current_method = _method.id
        self.expressions = []
        self.vars_method = {f.id: f"{i*4}($v0)" for f, i in enumerate(_method.formals)}
    
    def unvisit_method(self, _method):
        self.methods[self.current_method] = self.expressions
        self.current_method = None
        self.expressions = []
        self.vars_method = {}

    def visit_object(self, _expression):
        pass
    
    def unvisit_object(self, _expression):
        self.current_expression = None

    def add_expression(self, _expression: str):
        self.expressions.append(_expression)
