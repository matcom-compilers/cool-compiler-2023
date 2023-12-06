from typing import List

from COOL.codegen.utils import Instruction

from COOL.codegen.utils import DATA_SECTION
from COOL.codegen.utils import TEXT_SECTION
from COOL.codegen.codegen_rules import CREATE_CLASS
# from COOL.codegen.codegen_rules import REQUEST_MEMORY
from COOL.codegen.codegen_rules import CREATE_FUNCTION
from COOL.codegen.functions import FUNCTIONS


class MipsVisitor:
    def __init__(self) -> None:
        self.current_state = 0

        # global data
        self.data_secction = []
        self.test_section_classes = {}
        self.test_section_methods = {}

        # local data
        self.attributes = []
        self.expressions = []
        
        # memory
        self.class_memory = 0

        # current
        self.current_class = None
        self.current_method = None
        self.current_attribute = None
        self.current_expression = None
        
        # scope
        self.vars_method = {}
        self.vars_class = {}

        self.inheritance = {
            "Object": None,
            "IO": None,
            "Int": None,
            "String": None,
            "Bool": None,
        }
        self.class_methods = {
            "Object": [
                "Object_abort",
                "Object_type_name",
                "Object_copy",
            ],
            "IO": [
                "IO_out_string",
                "IO_out_int",
                "IO_in_string",
                "IO_in_int",
            ],
            "String": [
                "String_length",
                "String_concat",
                "String_substr",
            ],
        }
    
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
        for _cls in self.test_section_classes.keys():
            attributes = self.test_section_classes[_cls]["attributes"]
            memory = self.test_section_classes[_cls]["memory"]
            methods = self.test_section_classes[_cls]["methods"]
            
            text_section +=\
            CREATE_CLASS.format(
                class_name=_cls,
                attributes="\n".join(map(str, attributes)),
                # request_memory=REQUEST_MEMORY.format(memory=memory),
                request_memory=""
            )
            # TODO: clean the stack
            for _method in methods.keys():
                text_section +=\
                CREATE_FUNCTION.format(
                    function_name=_method,
                    class_name=_cls,
                    method="\n".join(map(str, methods[_method])),
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

    def get_class_method(self, _class: str, _method: str):
        """
        Get the method from the class. Include the methods from the inheritance.
        """
        if _method in self.class_methods[_class]:
            return self.get_method_name(_class, _method)
        return self.get_class_method(self.inheritance[_class], _method)
    
    def get_method_name(self, _class: str, _method: str):
        """
        Get the method name.
        """
        return f"{_class}_{_method}"

    def get_variable(self, _variable: str):
        """
        Get the variable from the current scope.
        """
        scope = {}
        scope.update(self.vars_class)
        scope.update(self.vars_method)
        return scope.get(_variable.id)
    
    def add_data(self, _data: str):
        """
        Add data to the data section.
        """
        self.data_secction.append(_data)

    def visit_program(self, _program):
        for _cls in _program.classes:
            self.inheritance[_cls.type] =\
                _cls.inherits_instance.type\
                if _cls.inherits_instance else "Object"
            self.class_methods[_cls.type] = [f.id for f in _cls.methods]

    
    def unvisit_program(self, _program):
        pass

    def visit_class(self, _class):
        self.current_class = _class.type
        self.class_memory = 0
        self.vars_class = {}
    
    def unvisit_class(self, _class):
        # TODO: request memory
        self.test_section_classes[_class.type] = {
            "memory": self.class_memory,
            "attributes": self.attributes,
            "methods": self.test_section_methods,
        }
        self.test_section_methods = {}
        self.attributes = []
        self.current_class = None
        self.class_memory = 0
        self.vars_class = {}
    
    def visit_attribute(self, _attribute):
        self.vars_class.update({_attribute.id: f"{self.class_memory}($v0))"})

    def add_attribute(self, _attribute: List[Instruction]):
        self.attributes.extend(_attribute)

    def unvisit_attribute(self, _attribute):
        self.class_memory += 4
    
    def add_memory(self, _memory: int):
        self.class_memory = _memory

    def visit_method(self, _method):
        self.current_method = self.get_method_name(self.current_class, _method.id)
        self.expressions = []
        self.vars_method = {f.id: f"{i*4}($v0)" for f, i in enumerate(_method.formals)}
    
    def unvisit_method(self, _method):
        self.test_section_methods[self.current_method] = self.expressions
        self.current_method = None
        self.expressions = []
        self.vars_method = {}

    def visit_object(self, _expression):
        pass
    
    def unvisit_object(self, _expression):
        self.current_expression = None

    def add_expression(self, _expression: List[Instruction]):
        self.expressions.extend(_expression)
    
    def visit_if(self, _if):
        pass

    def unvisit_if(self, _if):
        self.current_state += 1
    
    def visit_while(self, _while):
        pass

    def unvisit_while(self, _while):
        self.current_state += 1
