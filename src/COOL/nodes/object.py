from typing import Any
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.nodes import Node
from COOL.codegen.codegen_rules import TRUE
from COOL.codegen.codegen_rules import FALSE


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
        return f"    la  $t0, {self.value}\n"

    def check(self,visitor):
        return 'Int'


class String(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        str_name = "str_" + str(len(mips_visitor.data_secction))
        mips_visitor.add_data(
            f"{str_name}:  .asciiz \"{self.value}\"\n"
        )
        return f"    la  $t0, {str_name}"

    
    def check(self,visitor):
        return 'String'


class Boolean(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        return f"    la  $t0, {TRUE if self.value else FALSE}\n"

    def check(self,visitor):
        return 'Bool'
