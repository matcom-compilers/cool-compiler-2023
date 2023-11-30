from typing import Any
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.nodes import Node
from COOL.nodes.codegen_rules import TRUE
from COOL.nodes.codegen_rules import FALSE


class Object(Node):
    def __init__(self, line: int, column: int, value: Any) -> None:
        self.value = value
        super().__init__(line, column)


class Interger(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        return f"    la  $t0, {self.value}"

    def check(self):
        raise NotImplementedError()


class String(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        str_name = "str_" + str(len(mips_visitor.data_secction))
        mips_visitor.data_secction.append(
            f"{str_name}:  .asciiz \"{self.value}\""
        )
        return f"    la  $t0, {str_name}"

    def check(self):
        raise NotImplementedError()


class Boolean(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)
    
    def codegen(self, mips_visitor: MipsVisitor):
        return f"    la  $t0, {TRUE if self.value else FALSE}"

    def check(self):
        raise NotImplementedError()
