from typing import Any
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.nodes import Node

from COOL.codegen.utils import Instruction
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import Data
from COOL.codegen.utils import TRUE
from COOL.codegen.utils import FALSE


class Object(Node):
    def __init__(self, line: int, column: int, value: Any) -> None:
        self.value = value
        super().__init__(line, column)

    def check(self,visitor):
        return 'Object'


class Interger(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_object(self)
        obj = [
            Instruction("li", "$t0", self.value),
        ]
        mips_visitor.unvisit_object(self)
        return obj

    def check(self,visitor):
        return 'Int'


class String(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        str_name = "str_" + str(len(mips_visitor.data_secction))
        data = [
            Data(str_name, ".asciiz", self.value)
        ]
        mips_visitor.add_data(data)
        obj = [
            Instruction("la", mips_visitor.register_store_results, str_name)
        ]
        return obj
    
    def check(self,visitor):
        return 'String'


class Boolean(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        obj = [
            Instruction("la", "$t0", {TRUE if self.value else FALSE})
        ]
        return obj

    def check(self,visitor):
        return 'Bool'
