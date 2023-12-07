from typing import List

from COOL.codegen.utils import Data
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import Instruction

from COOL.codegen.utils import DATA_SECTION
from COOL.codegen.utils import TEXT_SECTION
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
        self.current_return_type = None
        
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
                "abort",
                "type_name",
                "copy",
            ],
            "IO": [
                "out_string",
                "out_int",
                "in_string",
                "in_int",
            ],
            "String": [
                "length",
                "concat",
                "substr",
            ],
            "Int": [],
            "Bool": [],
        }
    
    def generate_mips(self) -> str:
        """
        Generate the mips code from the visitor data.

        Return:
            str: mips code.
        """
        data_section =(
            DATA_SECTION +
            "\n".join(map(str, self.data_secction)) +
            "\n" +
            "\n".join(map(str, self.generate_data_classes))
        )

        text_section = TEXT_SECTION
        for _cls in self.test_section_classes.keys():
            attributes = self.test_section_classes[_cls]["attributes"]
            memory = self.test_section_classes[_cls]["memory"]
            methods = self.test_section_classes[_cls]["methods"]
            text_section += "\n".join(map(
                str,
                self.create_class(
                        _class=_cls,
                        memory=memory,
                        attributes=attributes
                    )
                )
            )
            # TODO: clean the stack
            for _method in methods.keys():
                text_section += "\n".join(map(
                str,
                self.create_function(
                        _function=_method,
                        _class=_cls,
                        _method=methods[_method]
                    )
                )
            )
        for _function in FUNCTIONS:
            text_section += _function
        
        return data_section + text_section

    @property
    def rr(self):
        """
        Register return
        """
        return "$ra"
    
    @property
    def rsp(self):
        """
        Register stack pointer
        """
        return "$sp"
    
    @property
    def rsi(self):
        """
        Register system input
        """
        return "$a0"
    
    @property
    def rmr(self):
        """
        Register method return
        """
        return "$v0"
    
    @property
    def rsr(self):
        """
        Register store results
        """
        return "$t0"
    
    @property
    def generate_classes(self):
        """
        Generate the classes with his methods
        """
        data = {}
        for _cls in self.inheritance.keys():
            data[_cls] = {}
            for _current_cls in reversed(self.__get_class_parents(_cls)):
                data[_cls].update({_method: _current_cls for _method in self.class_methods[_current_cls]})
        return data

    @property
    def generate_data_classes(self):
        """
        Generate the classes with his method labels in .data
        """
        data = self.generate_classes
        data_section = [
            Data(_cls, ".word", *[self.get_method_name(_c, _m) for _m, _c in data[_cls].items()])
            for _cls in data.keys() if data[_cls]
        ]
        return data_section

    # CREATE
    def create_class(self, _class: str, memory: int, attributes: List[Instruction]):
        obj = [
            Comment(f"Create class {_class}"),
            Label(self.get_class_name(_class)),
            Instruction("li", self.rsi, memory),
            Instruction("li", self.rmr, 9),
            Instruction("syscall"),
            Instruction("la", self.rsr, _class),
            Instruction("sw", self.rmr, "0($v0)"),
            Instruction("addiu", self.rmr, self.rmr, 4),
            *attributes,
        ]
        return obj

    def create_function(self, _function: str, _class: str, _method: List[Instruction]):
        obj = [
            Comment(f"Create function {_function} from class {_class}"),
            Label(_function),
            Instruction("addiu", self.rsp, self.rsp, "-4"),
            Instruction("sw", self.rr, "0($sp)"),
            *_method,
            Instruction("lw", self.rr, "0($sp)"),
            Instruction("addiu", self.rsp, self.rsp, 4),
            Instruction("jr", self.rr),
        ]
        return obj
    
    # GET
    def __get_class_parents(self, _class: str):
        """
        Get the class parents.
        """
        parents = []
        while _class:
            parents.append(_class)
            _class = self.inheritance[_class]
        return parents


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
    
    def get_class_name(self, _class: str):
        """
        Get the class name.
        """
        return f"{_class}_class"

    def get_variable(self, _variable: str):
        """
        Get the variable from the current scope.
        """
        scope = {}
        scope.update(self.vars_class)
        scope.update(self.vars_method)
        return scope.get(_variable.id)
    
    # ADD
    def add_data(self, _data: List[Data]):
        """
        Add data to the data section.
        """
        self.data_secction.extend(_data)
    
    def add_attribute(self, _attribute: List[Instruction]):
        self.attributes.extend(_attribute)
    
    def add_memory(self, _memory: int):
        self.class_memory = _memory

    def add_expression(self, _expression: List[Instruction]):
        self.expressions.extend(_expression)

    # VISIT
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
        self.test_section_classes[_class.type] = {
            "memory": self.class_memory+4,
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

    def unvisit_attribute(self, _attribute):
        self.class_memory += 4

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
    
    def visit_if(self, _if):
        pass

    def unvisit_if(self, _if):
        self.current_state += 1
    
    def visit_while(self, _while):
        pass

    def unvisit_while(self, _while):
        self.current_state += 1
