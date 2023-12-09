from typing import List

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


# NOTE: class memory first value is the type reference
# NOTE: method stack first value is the return value
# NOTE: method stack second value is current self reference

class MipsVisitor:
    def __init__(self) -> None:
        # number to generate labels
        self.current_state = 0

        # GLOBAL DATA
        self.test_section = []
        self.data_secction = []
        self.test_section_classes = {}

        # LOCAL DATA
        self.attributes = []
        
        # memory
        self.class_memory = 0

        # CURRENT
        self.current_class = None
        self.current_let = None
        self.let_queue = []
        self.current_offset = 0
        
        # SCOPE
        self.vars_method = {}
        self.vars_class = CLASS_VARS
        self.vars_let = {}
        
        # INHERITANCE
        self.inheritance = INHERIANCE
        self.class_methods = CLASS_METHODS

    
    def generate_mips(self) -> str:
        """
        Generate the mips code from the visitor data.

        Return:
            str: mips code.
        """
        data_section =(
            "\n" +
            "\n".join(map(str, self.create_data())) +
            "\n" +
            "\n".join(map(str, self.data_secction)) +
            "\n" +
            "\n".join(map(str, self.generate_data_classes)) +
            "\n"
        )

        text_section = "\n".join(map(str, self.create_text())) + "\n"
        for _cls in self.test_section_classes.keys():
            current_class = _cls
            inheriance = []
            while current_class:
                if self.test_section_classes.get(current_class) is None:
                    break
                inheriance.append(current_class)
                current_class = self.inheritance[current_class]
            
            memory = 0
            attributes = []
            for current_class in reversed(inheriance):
                attributes.extend(self.test_section_classes[current_class]["attributes"])
                memory += self.test_section_classes[current_class]["memory"]
                current_class = self.inheritance[current_class]
            
            text_section += "\n".join(map(
                str,
                self.create_class(
                        _class=_cls,
                        memory=memory+WORD,
                        attributes=attributes
                    )
                )
            )
        text_section += "\n".join(map(str, self.create_base_class()))
        text_section += "\n".join(map(str, self.test_section))
        
        for _function in FUNCTIONS:
            text_section += "\n" + _function
        
        return data_section + "\n" + text_section

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
        class_methods = self.class_methods.copy()
        for _cls in self.class_methods.keys():
            for _cls_hierarchy in self.get_class_parents(_cls):
                class_methods[_cls].update(
                    {
                        f: t for f, t in self.class_methods[_cls_hierarchy].items()
                    }
                )
        return class_methods

    @property
    def generate_data_classes(self):
        """
        Generate the classes with his method labels in .data
        """
        data = {}
        for _cls in self.inheritance.keys():
            data[_cls] = {}
            for _current_cls in self.get_class_parents(_cls):
                data[_cls].update({f: _current_cls for f in self.class_methods[_current_cls].keys()})
        data_section = [
            Data(_cls, ".word", *[self.get_method_name(_c, _m) for _m, _c in data[_cls].items()])
            for _cls in data.keys() if data[_cls]
        ]
        return data_section

    # CREATE
    def create_class(self, _class: str, memory: int, attributes: List[Instruction]):
        _attributes = []
        for attr in attributes:
            _attributes.extend(
                [
                    *self.allocate_stack(WORD),
                    Instruction("sw", self.rv, f"0({self.rsp})"),
                    *attr,
                    Instruction("lw", self.rv, f"0({self.rsp})"),
                    *self.deallocate_stack(WORD),
                    Instruction("sw", self.rt, f"0({self.rv})"),
                    *self.allocate_heap(WORD),
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
            # Save the self reference
            *self.allocate_heap(WORD),
            # save $ra reference
            *self.allocate_stack(WORD),
            Instruction("sw", self.rra, f"0({self.rsp})"),
            *_attributes,
            # load $ra reference
            Instruction("lw", self.rra, f"0({self.rsp})"),
            *self.deallocate_stack(WORD),
            # load self
            *self.deallocate_heap(memory),
            Instruction("jr", self.rra),
            "\n",
        ]
        return obj
    
    def create_base_class(self):
        """
        Create the base classes IO, Int, String, Bool.
        """
        obj = [
            *self.create_class("Object", WORD, []),
            *self.create_class("IO", WORD, []),
            # *self.create_class("Int", 4, []),
            # *self.create_class("String", 4, []),
            # *self.create_class("Bool", 4, []),
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
            *self.allocate_stack(WORD),
            Instruction("sw", self.rv, f"0({self.rsp})"),
            Instruction("jal", self.get_method_name("Main", "main")),
            Instruction("j", "exit"),
        ]
        return obj

    # ALLOCATE
    def set_offset(self, _offset: int):
        """
        Allocate offset.
        """
        self.current_offset += _offset

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

    def allocate_object(self, _type: str, _obj: List[Instruction]):
        """
        Allocate object.
        """
        obj = [
            *self.allocate_memory(8),
            Instruction("la", self.rt, "Int"),
            Instruction("sw", self.rt, f"0({self.rv})"),
            *_obj,
            Instruction("sw", self.rt, f"4({self.rv})"),
            # FIX
            Instruction("move", self.rt, self.rv),
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

    # FIX
    def get_variable(self, _variable: str):
        """
        Get the variable from the current scope.
        """
        scope = {}
        vars_class = {}
        _cls = self.current_class
        while _cls:
            vars_class.update(self.vars_class[_cls])
            _cls = self.inheritance[_cls]
        scope.update(vars_class)
        scope.update(self.vars_method)
        for _let in self.let_queue:
            scope.update(self.vars_let[_let])
        return scope.get(_variable)
    
    def get_function(self, _class: str, _function: str):
        """
        Get the function from the class.
        """
        if _class == "SELF_TYPE":
            _class = self.current_class
        data = self.inheriance_class_methods
        data = {value[0]: i*WORD for i, value in enumerate(data[_class].items())}
        return data[_function]
    
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

    def unvisit_program(self, _program):
        pass

    def visit_class(self, _class):
        self.current_class = _class.type
        self.class_memory = 0
        self.vars_class[self.current_class] = {}
    
    def unvisit_class(self, _class):
        self.test_section_classes[_class.type] = {
            "memory": self.class_memory,
            "attributes": self.attributes,
        }
        self.attributes = []
        self.current_class = None
        self.class_memory = 0
    
    def visit_attribute(self, _attribute):
        attr = {
            _attribute.id: {
                "memory": self.class_memory,
                "type": _attribute.type,
            }
        }
        self.vars_class[self.current_class].update(attr)

    def unvisit_attribute(self, _attribute):
        self.class_memory += WORD

    def visit_method(self, _method):
        self.vars_method = {
            # "return": f"0({self.rsp})",
            "self": {
                "memory": 4,
                "type": self.current_class,
            },
            **{f.id: {"memory": f"{(i+2)*WORD}({self.rsp})", "type": f.type} for i, f in enumerate(_method.formals)},
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

    def visit_let(self, _let):
        self.current_let = f"let_{self.current_state}"
        self.let_queue.append(self.current_let)
        self.vars_let[self.current_let] = {}
        for i, arg in enumerate(_let.let_list):
            self.vars_let[self.current_let].update(
                {
                    arg.id: {
                        "memory": (i)*WORD,
                        "type": arg.type,
                    }
                }
            )

    def unvisit_let(self, _let):
        self.current_state += 1
        self.current_let = self.let_queue.pop(-1) if self.let_queue else None
