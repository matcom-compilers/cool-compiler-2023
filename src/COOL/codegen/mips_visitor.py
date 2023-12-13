from typing import List
from copy import deepcopy

from COOL.codegen.utils import WORD
from COOL.codegen.utils import TRUE
from COOL.codegen.utils import FALSE
from COOL.codegen.utils import Data
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import Section
from COOL.codegen.utils import Instruction

from COOL.codegen.utils import INHERIANCE
from COOL.codegen.utils import CLASS_VARS
from COOL.codegen.utils import CLASS_METHODS
from COOL.codegen.functions import FUNCTIONS


class MipsVisitor:
    def __init__(self) -> None:
        # number to generate labels
        self.current_state = 0

        # GLOBAL DATA
        self.text_section_data = {}
        self.test_section = []
        self.data_secction = []

        # LOCAL DATA
        self.attributes = []
        
        # memory
        self.class_memory = 0

        # CURRENT
        self.current_class = None
        self.current_let = None
        self.current_case_branch = None
        self.let_queue = []
        self.case_queue = []
        self.current_offset = 0
        
        # SCOPE
        self.vars_method = {}
        self.vars_class = CLASS_VARS
        self.vars_let = {}
        self.vars_case = {}
        
        # INHERITANCE
        self.inheritance = INHERIANCE
        self.class_methods = CLASS_METHODS

    
    def generate_mips(self) -> str:
        """
        Generate the mips code from the visitor data.

        Return:
            str: mips code.
        """
        data_section = [
            *self.create_data(),
            *self.data_secction,
            *self.generate_data_classes,
            "\n"
        ]

        class_text_section = []
        for _cls in self.text_section_data.keys():
            inheriance = self.get_class_inheriance_list(_cls)[1:]
            for i in ["IO", "Int", "String", "Bool"]:
                if i in inheriance:
                    inheriance.remove(i)
            attributes = []
            for current_class in inheriance:
                attr = []
                if current_class == _cls:
                    attributes.extend(self.text_section_data[current_class]["attributes"])
                else:
                    a = list(range(1, self.text_section_data[current_class]["memory"]//WORD))
                    for i in range(1, self.text_section_data[current_class]["memory"]//WORD):
                        attr.append(
                            [
                                Instruction("jal", self.get_class_name(current_class)),
                                Instruction("lw", "$t0", f"{i*WORD}({self.rt})"),
                            ]
                        )
                    attributes.extend(attr)                
            
            class_text_section.extend(
                self.create_class(
                    _class=_cls,
                    memory=self.text_section_data[_cls]["memory"],
                    attributes=attributes
                )
            )
        aux_functions_text_section = []
        for _function in FUNCTIONS:
            aux_functions_text_section.extend(_function)

        text_section = [
            *self.create_text(),
            *class_text_section,
            *self.test_section,
            *self.create_base_class(),
            *aux_functions_text_section,
        ]
        
        return "\n".join(map(str, data_section + text_section))

    @property
    def rra(self):
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
    def ra(self):
        """
        Register system input
        """
        return "$a0"
    
    @property
    def rv(self):
        """
        Register method return
        """
        return "$v0"
    
    @property
    def rt(self):
        """
        Register store results
        """
        return "$t0"
    
    @property
    def inheriance_class_methods(self):
        """
        Return all the class methods with including the inheritance and his types.
        """
        data = {}
        for _cls in self.inheritance.keys():
            data[_cls] = {}
            for _current_cls in self.get_class_inheriance_list(_cls):
                data[_cls].update({f: _current_cls for f in self.class_methods[_current_cls].keys()})
        return data

    @property
    def generate_data_classes(self):
        """
        Generate the classes with his method labels in .data
        """
        data = self.inheriance_class_methods
        data_section = [
            *[
                Data(self.get_class_label(_cls), ".asciiz", f"\"{_cls}\\n\"")
                for _cls in data.keys() if data[_cls]
            ],
            *[
                Data(self.get_class_ref(_cls), ".word", self.get_class_label(_cls), self.get_class_ref(self.get_father(_cls)))
                for _cls in data.keys() if data[_cls]
            ],
            *[
                Data(_cls, ".word", self.get_class_ref(_cls), *[self.get_method_name(_c, _m) for _m, _c in data[_cls].items()])
                for _cls in data.keys() if data[_cls]
            ]
        ]
        return data_section

    # CREATE
    def create_class(self, _class: str, memory: int, attributes: List[Instruction]):
        _attributes = []
        for i, attr in enumerate(attributes):
            _attributes.extend(
                [   
                    # save the class instance while creating it
                    *self.allocate_stack(WORD),
                    Instruction("sw", self.rv, f"0({self.rsp})"),
                    *attr,
                    # load the class instance
                    Instruction("lw", self.rv, f"0({self.rsp})"),
                    *self.deallocate_stack(WORD),
                    # save the attribute and move the heap
                    Instruction("sw", self.rt, f"{(i+1)*WORD}({self.rv})"),
                ]
            )
        obj = [
            Comment(f"Create class {_class}", indent=""),
            Label(self.get_class_name(_class)),
            # Allocate memory
            Instruction("li", self.ra, memory),
            Instruction("li", self.rv, 9),
            Instruction("syscall"),
            # Save the type reference
            Instruction("la", self.rt, _class),
            Instruction("sw", self.rt, f"0({self.rv})"),
            # save $ra reference
            *self.allocate_stack(WORD),
            Instruction("sw", self.rra, f"0({self.rsp})"),
            *_attributes,
            # load $ra reference
            Instruction("lw", self.rra, f"0({self.rsp})"),
            *self.deallocate_stack(WORD),
            # load self
            Instruction("move", self.rt, self.rv),
            Instruction("jr", self.rra),
            "\n",
        ]
        return obj
    
    def create_base_class(self):
        """
        Create the base classes IO, Int, String, Bool.
        """
        obj = [
            *self.create_class("Object", 2*WORD,
                [
                    [Instruction("la", self.rt, "null")]
                ]
            ),
            *self.create_class("IO", 2*WORD, []),
            *self.create_class("Int", 2*WORD,
                [
                    [Instruction("li", self.rt, 0)]
                ]
            ),
            *self.create_class("String", 2*WORD,
                [
                    [Instruction("la", self.rt, "empty")]
                ]
            ),
            *self.create_class("Bool", 2*WORD,
                [
                    [Instruction("la", self.rt, "false")]
                ]
            ),
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
            Data("empty", ".asciiz", "\"\""),
            Data("null", ".word", "0"),
            Data("true", ".word", "1"),
            Data("false", ".word", "0"),
            Data("case_error", ".asciiz", "\"Case without match at line \""),
            Data("abort_label", ".asciiz", "\"Abort called from class \""),
            Data("input_buffer",".space","1024"),
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
            *self.allocate_stack(WORD),
            Instruction("sw", self.rv, f"0({self.rsp})"),
            Instruction("jal", self.get_method_name("Main", "main")),
            Instruction("j", "exit"),
        ]
        return obj

    # ALLOCATE
    def set_id(self):
        self.current_state += 1
    
    def get_id(self):
        return self.current_state

    def set_offset(self, _offset: int):
        """
        Allocate offset.
        """
        self.current_offset += _offset
    
    def unset_offset(self, _offset: int):
        """
        Deallocate offset.
        """
        self.current_offset -= _offset

    def allocate_heap(self, _size: int):
        """
        Allocate memory.
        """
        obj = [
            Instruction("addiu", self.rv, self.rv, _size),
        ]
        return obj
    
    def deallocate_heap(self, _size: int):
        """
        Deallocate memory.
        """
        obj = [
            Instruction("addiu", self.rv, self.rv, f"-{_size}"),
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
            Instruction("addiu", self.rsp, self.rsp, _size),
        ]
        return obj

    def allocate_memory(self, _size: int):
        """
        Allocate memory.
        """
        obj = [
            Instruction("li", self.ra, _size),
            Instruction("li", self.rv, 9),
            Instruction("syscall"),
        ]
        return obj

    def allocate_object(self, memory: int, _type: str, _obj: List[Instruction]):
        """
        Allocate object.
        """
        obj = [
            *self.allocate_memory(memory),
            Instruction("la", self.rt, _type),
            Instruction("sw", self.rt, f"0({self.rv})"),
            *_obj,
            Instruction("sw", self.rt, f"4({self.rv})"),
            Instruction("move", self.rt, self.rv),
        ]
        return obj
    
    # GET
    def get_offset(self, _var=None):
        """
        Get the current offset.
        """
        if _var:
            return _var['memory'] + self.current_offset - _var['offset']
        return self.current_offset

    def get_class_inheriance_list(self, _class: str):
        """
        Get the class parents.
        """
        parents = []
        while _class:
            parents.append(_class)
            _class = self.inheritance[_class]
        parents = list(reversed(parents))
        return parents
    
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
    
    def get_class_label(self, _class: str):
        """
        Get the class label.
        """
        return f"{_class}_label"
    
    def get_class_ref(self, _class: str):
        """
        Get the class reference.
        """
        return f"{_class}_ref" if _class else "0"
    
    def get_father(self, _class: str):
        """
        Get the father class.
        """
        return self.inheritance[_class]

    def get_variable(self, _variable: str):
        """
        Get the variable from the current scope.
        """
        scope = {}
        scope.update(self.vars_class[self.current_class])
        scope.update(self.vars_method)
        for _let in self.let_queue:
            scope.update(self.vars_let[_let])
        for _case in self.case_queue:
            scope.update(self.vars_case[_case])
        var = scope.get(_variable)
        if var is None:
            return {
                "memory": 0,
                "type": self.current_class,
                "stored": "method",
                "offset": 0,
            }
        return var
    
    def get_function(self, _class: str, _function: str):
        """
        Get the function from the class.
        """
        if _class == "SELF_TYPE":
            _class = self.current_class
        data = self.inheriance_class_methods
        data = {value[0]: (i+1)*WORD for i, value in enumerate(data[_class].items())}
        data = data[_function] 
        return data if data != "SELF_TYPE" else self.get_function(self.current_class, _function)
    
    def get_return(self, _class: str, function: str):
        """
        Get the return type from the function.
        """
        inheriance = self.get_class_inheriance_list(_class)
        for _class in inheriance:
            if self.class_methods[_class].get(function):
                return self.class_methods[_class][function]
        return "Object"
    
    # ADD
    def add_data(self, _data: List[Data]):
        """
        Add data to the data section.
        """
        self.data_secction.extend(_data)
    
    def add_attribute(self, _attribute: List[Instruction]):
        """
        Add attribute to the class.
        """
        self.attributes.append(_attribute)
    
    def add_method(self, _method: List[Instruction]):
        """
        Add method to text section.
        """
        self.test_section.extend(_method)
    
    def add_memory(self, _memory: int):
        """
        Add memory to the class.
        """
        self.class_memory = _memory

    # VISIT
    def visit_program(self, _program):
        for _cls in _program.classes:
            self.inheritance[_cls.type] =_cls.inherits if _cls.inherits else "Object"
            self.class_methods[_cls.type] = {f.id: f.type for f in _cls.methods}
        
        class_attributes = {_cls.type: _cls.attributes for _cls in _program.classes}
        for _cls in _program.classes:
            memory_counter = WORD
            self.vars_class[_cls.type] = {}
            for _current_cls in self.get_class_inheriance_list(_cls.type):
                if _current_cls in class_attributes:
                    for attr in class_attributes[_current_cls]:
                        self.vars_class[_cls.type].update(
                            {
                                attr.id: {
                                    "memory": memory_counter,
                                    "type": attr.type,
                                    "stored": "class",
                                    "offset": 0,
                                }
                            }
                        )
                        memory_counter += WORD
            self.text_section_data[_cls.type] = {
                "memory": memory_counter,
            }
        

    def unvisit_program(self, _program):
        pass

    def visit_class(self, _class):
        self.current_class = _class.type
    
    def unvisit_class(self, _class):
        self.text_section_data[_class.type].update({"attributes": self.attributes})
        self.attributes = []
        self.current_class = None
    
    def visit_attribute(self, _attribute):
        pass

    def unvisit_attribute(self, _attribute):
        pass

    def visit_method(self, _method):
        self.set_offset(len(_method.formals)*WORD+4)
        self.vars_method = {
            "self": {
                "memory": 4,
                "type": self.current_class,
                "stored": "method",
                "offset": self.current_offset,
            },
            **{
                f.id: {
                    "memory": (i+2)*WORD ,
                    "type": f.type,
                    "stored": "method",
                    "offset": self.current_offset,
                }
                for i, f in enumerate(_method.formals)
            },
        }
    
    def unvisit_method(self, _method):
        self.unset_offset(len(_method.formals)*WORD+4)
        self.vars_method = {}
    
    def visit_execute_method(self, _execute_method):
        self.set_offset(len(_execute_method.exprs)*WORD+4)

    def unvisit_execute_method(self, _execute_method):
        self.unset_offset(len(_execute_method.exprs)*WORD+4)
    
    def visit_if(self, _if):
        self.set_id()

    def unvisit_if(self, _if):
        pass
    
    def visit_while(self, _while):
        self.set_id()

    def unvisit_while(self, _while):
        pass

    def visit_let(self, _let):
        self.set_id()
        self.current_let = f"let_{self.current_state}"
        self.let_queue.append(self.current_let)
        self.set_offset(len(_let.let_list)*WORD)
        self.vars_let[self.current_let] = {}
        for i, arg in enumerate(_let.let_list):
            self.vars_let[self.current_let].update(
                {
                    arg.id: {
                        "memory": (i)*WORD,
                        "type": arg.type,
                        "stored": "let",
                        "offset": self.current_offset,
                    }
                }
            )

    def unvisit_let(self, _let):
        self.unset_offset(len(_let.let_list)*WORD)
        self.vars_let.pop(self.current_let)
        self.let_queue.pop(-1)
        self.current_let = self.let_queue[-1] if self.let_queue else None
    
    def visit_case(self, _case):
        self.set_id()
    
    def unvisit_case(self, _case):
        pass
    
    def visit_case_expr(self, _case_branch):
        self.set_id()
        self.current_case_branch = f"case_{self.current_state}"
        self.case_queue.append(self.current_case_branch)
        self.set_offset(WORD)
        self.vars_case[self.current_case_branch] = {
            _case_branch.id: {
                "memory": 0,
                "type": _case_branch.type,
                "stored": "case",
                "offset": self.current_offset
            }
        }

    def unvisit_case_expr(self, _case_branch):
        self.unset_offset(WORD)
        self.vars_case.pop(self.current_case_branch)
        self.case_queue.pop(-1)
        self.current_case_branch = self.case_queue[-1] if self.case_queue else None
