from typing import List

from COOL.nodes import Node
from COOL.semantic.visitor import Visitor
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.nodes.codegen_rules import Types
from COOL.nodes.codegen_rules import NULL
from COOL.nodes.codegen_rules import NEWLINE
from COOL.nodes.codegen_rules import CREATE_FUNCTION
from COOL.nodes.codegen_rules import STORE_DATA
from COOL.nodes.codegen_rules import SET_VAR_IN_DATA_SECTION


class Method(Node):
    def __init__(self, line: int, column: int, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line, column)

    def codegen(self):
        data, text = [], []
        for _formal in self.formals:
            data.append(
                SET_VAR_IN_DATA_SECTION.format(
                    owner=self.id, var_name=_formal.id,
                    type=Types[_formal.type.upper()].value,
                    value=0)
                )
        text.append(CREATE_FUNCTION.format(function_name=self.id))
        # TODO: execute expr
        return data, text

    def check(self, visitor: Visitor):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: int, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.id = id
        super().__init__(line, column)

    def codegen(self):
        raise NotImplementedError()

    def check(self):
        raise NotImplementedError()


class Attribute(Node):
    def __init__(self, line: int, column: int, id: str) -> None:
        self.id = id
        super().__init__(line, column)

    def check(self, visitor: Visitor):
        visitor.visit_attribute(self)

class AttributeDeclaration(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column, id)

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        mips_visitor.attributes.append(
            f"    li $t0, {NULL}" +
            NEWLINE +
            f"    sw $t0, {mips_visitor.class_memory}($v0)"
        )
        mips_visitor.class_memory += 4
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor: Visitor):
        visitor.visit_attribute_declaration(self)


class AttributeInicialization(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        super().__init__(line, column, id)
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        # TODO: how to return expr codegen?
        expr = self.expr.codegen(mips_visitor)
        match self.type:
            case "Int":
                mips_visitor.attributes.append(
                    expr +
                    NEWLINE +
                    f"    sw $t0, {mips_visitor.class_memory}($v0)"
                )
            case "String":
                pass
            case "Bool":
                pass
            case "Object":
                pass
            case "IO":
                pass
            case "SELF_TYPE":
                pass
        mips_visitor.class_memory += 4
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor: Visitor):
        visitor.visit_attribute_inicialization(self)


class Formal(Node):
    def __init__(self, line: int, column: int, id: str, type: str) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column)

    def codegen(self, mips_visitor: MipsVisitor):
        raise NotImplementedError()

    def check(self, visitor: Visitor):
        raise NotImplementedError()