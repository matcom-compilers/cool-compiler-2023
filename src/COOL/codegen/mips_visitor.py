from typing import List

from COOL.codegen.utils import TRUE
from COOL.codegen.utils import FALSE
from COOL.codegen.utils import Data
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import Section
from COOL.codegen.utils import Instruction

from COOL.codegen.utils import INHERIANCE
from COOL.codegen.utils import CLASS_METHODS
from COOL.codegen.functions import FUNCTIONS


# NOTE: class memory first value is the type reference
# NOTE: method stack first value is the return value
# NOTE: method stack second value is current self reference

class MipsVisitor:
    def __init__(self) -> None:
        self.current_state = 0

        # global data
        self.test_section = []
        self.data_secction = []
        self.test_section_classes = {}

        # local data
        self.attributes = []
        
        # memory
        self.class_memory = 0

        # current
        self.current_class = None
        # self.current_method = None
        # self.current_attribute = None
        # self.current_expression = None
        
        # scope
        self.vars_method = {}
        self.vars_class = {}

        self.inheritance = INHERIANCE
        self.class_methods = CLASS_METHODS
        
    
    def generate_mips(self) -> str:
        """
        Generate the mips code from the visitor data.

        Return:
            str: mips code.
        """
        data_section =(
            "\n".join(map(str, self.create_data())) +
            "\n" +
            "\n".join(map(str, self.data_secction)) +
            "\n" +
            "\n".join(map(str, self.generate_data_classes))
        )

        text_section = "\n".join(map(str, self.create_text())) + "\n"
        for _cls in self.test_section_classes.keys():
            attributes = self.test_section_classes[_cls]["attributes"]
            memory = self.test_section_classes[_cls]["memory"]
            
            text_section += "\n".join(map(
                str,
                self.create_class(
                        _class=_cls,
                        memory=memory,
                        attributes=attributes
                    )
                )
            )
            text_section += "\n" + "\n".join(map(str,self.test_section))
        
        for _function in FUNCTIONS:
            text_section += _function
        
        return data_section + "\n" + text_section

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
            for _current_cls in reversed(self.get_class_parents(_cls)):
                data[_cls].update({_method: _current_cls for _method in self.class_methods[_current_cls].keys()})
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
            Comment(f"Create class {_class}", indent=""),
            Label(self.get_class_name(_class)),
            # Allocate memory
            Instruction("li", self.rsi, memory),
            Instruction("li", self.rmr, 9),
            Instruction("syscall"),
            # Save the type reference
            Instruction("la", self.rsr, _class),
            Instruction("sw", self.rsr, f"0({self.rmr})"),
            # Save the self reference
            *self.allocate_heap(4),
            # save allocated memory in stack to dont lose it
            *self.allocate_stack(4),
            Instruction("sw", self.rmr, f"0({self.rsp})"),
            # save $ra reference
            *self.allocate_stack(4),
            Instruction("sw", self.rr, f"0({self.rsp})"),
            *attributes,
            # load $ra reference
            Instruction("lw", self.rr, f"0({self.rsp})"),
            *self.deallocate_stack(4),
            # load self
            Instruction("lw", self.rmr, f"0({self.rsp})"),
            *self.deallocate_stack(4),
            *self.deallocate_heap(memory),
            Instruction("jr", self.rr),
        ]
        return obj
    
    def create_data(self):
        """
        Create the data section.
        """
        obj = [
            Comment("Data section", indent=""),
            Section("data"),
            Data("newline", ".asciiz", "\"\\n\""),
            Data("null", ".word", "0"),
            Data("true", ".word", "1"),
            Data("false", ".word", "0"),
        ]
        return obj
    
    def create_text(self):
        """
        Create the text section.
        """
        obj = [
            Comment("Text section", indent=""),
            Section("text"),
            Label("main"),
            Instruction("jal", self.get_class_name("Main")),
            *self.allocate_stack(4),
            Instruction("sw", self.rmr, f"0({self.rsp})"),
            Instruction("jal", self.get_method_name("Main", "main")),
            Instruction("j", "exit"),
        ]
        return obj

    # ALLOCATE
    def allocate_heap(self, _size: int):
        """
        Allocate memory.
        """
        obj = [
            Instruction("addiu", self.rmr, self.rmr, f"{_size}"),
        ]
        return obj
    
    def deallocate_heap(self, _size: int):
        """
        Deallocate memory.
        """
        obj = [
            Instruction("addiu", self.rmr, self.rmr, f"-{_size}"),
        ]
        return obj

    def allocate_stack(self, _size: int):
        """
        Allocate stack.
        """
        obj = [
            Instruction("addiu", self.rsp, self.rsp, f"-{_size}"),
        ]
        return obj
    
    def deallocate_stack(self, _size: int):
        """
        Deallocate stack.
        """
        obj = [
            Instruction("addiu", self.rsp, self.rsp, f"{_size}"),
        ]
        return obj

    def allocate_memory(self, _size: int):
        """
        Allocate memory.
        """
        obj = [
            Instruction("li", self.rsi, _size),
            Instruction("li", self.rmr, 9),
            Instruction("syscall"),
        ]
        return obj

    def allocate_object(self, _type: str, _obj: List[Instruction]):
        """
        Allocate object.
        """
        obj = [
            *self.allocate_memory(8),
            Instruction("la", self.rsr, "Int"),
            Instruction("sw", self.rsr, f"0({self.rmr})"),
            *_obj,
            Instruction("sw", self.rsr, f"4({self.rmr})"),
            Instruction("move", self.rsr, {self.rmr}),
        ]
        return obj
    
    # GET
    def get_class_parents(self, _class: str):
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
        if _method in self.class_methods[_class].keys():
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
        return scope.get(_variable)
    
    def get_function(self, _class: str, _function: str, register: str):
        data = self.generate_classes
        data = {value[0]: f"{i*4}({register})" for i, value in enumerate(data[_class].items())}
        return data[_function]
    
    # ADD
    def add_data(self, _data: List[Data]):
        """
        Add data to the data section.
        """
        self.data_secction.extend(_data)
    
    def add_attribute(self, _attribute: List[Instruction]):
        self.attributes.extend(_attribute)
    
    def add_method(self, _method: List[Instruction]):
        self.test_section.extend(_method)
    
    def add_memory(self, _memory: int):
        self.class_memory = _memory

    # VISIT
    def visit_program(self, _program):
        for _cls in _program.classes:
            self.inheritance[_cls.type] =_cls.inherits if _cls.inherits else "Object"
            self.class_methods[_cls.type] = {f.id: f.type for f in _cls.methods}
        for _cls in self.class_methods.keys():
            for _cls_hierarchy in self.get_class_parents(_cls):
                self.class_methods[_cls].update(
                    {
                        f: t for f, t in self.class_methods[_cls_hierarchy].items()
                    }
                )
        for _cls in _program.classes:
            for _cls_hierarchy in self.get_class_parents(_cls.type):
                self.class_methods[_cls.type].update(
                    {
                        f: t for f, t in self.class_methods[_cls_hierarchy].items()
                    }
                )

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
        }
        self.attributes = []
        self.current_class = None
        self.class_memory = 0
        self.vars_class = {}
    
    def visit_attribute(self, _attribute):
        # FIX
        self.vars_class.update({_attribute.id: f"{self.class_memory}($v0))"})

    def unvisit_attribute(self, _attribute):
        self.class_memory += 4

    def visit_method(self, _method):
        self.vars_method = {
            "return": f"0({self.rsp})",
            "self": f"4({self.rsp})",
            **{f.id: f"{(i+2)*4}({self.rsp})" for i, f in enumerate(_method.formals)},
        }
    
    def unvisit_method(self, _method):
        # self.current_method = None
        self.vars_method = {}
    
    def visit_execute_method(self, _execute_method):
        pass

    def unvisit_execute_method(self, _execute_method):
        pass

    def visit_object(self, _expression):
        pass
    
    def unvisit_object(self, _expression):
        pass
        # self.current_expression = None
    
    def visit_if(self, _if):
        pass

    def unvisit_if(self, _if):
        self.current_state += 1
    
    def visit_while(self, _while):
        pass

    def unvisit_while(self, _while):
        self.current_state += 1
