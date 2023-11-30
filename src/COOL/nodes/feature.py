from typing import List

from COOL.nodes import Node
from COOL.codegen.mips_visitor import MipsVisitor

from COOL.codegen.codegen_rules import NULL


class Method(Node):
    def __init__(self, line: int, column: int, id: str, type: str, expr: Node, formals: List[Node]) -> None:
        self.type: str = type
        self.expr: Node = expr
        self.id = id
        self.formals: List[Node] = formals
        super().__init__(line, column)

    # TODO: add formals
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_method(self)
        expr = self.expr.codegen(mips_visitor)
        mips_visitor.add_expression(expr)
        mips_visitor.unvisit_method(self)

    def check(self, visitor):
        visitor.visit_method(self)


class ExecuteMethod(Node):
    def __init__(self, line: int, column: int, id: str, exprs: List[Node]) -> None:
        self.exprs: List[Node] = exprs
        self.expr: Node = None
        self.id = id
        super().__init__(line, column)

    # TODO
    def codegen(self):
        raise NotImplementedError()

    def check(self,visitor):
        visitor.visit_execute_method(node = self)


class Attribute(Node):
    def __init__(self, line: int, column: int, id: str) -> None:
        self.id = id
        super().__init__(line, column)

    def check(self, visitor):
        visitor.visit_attribute(self)


class AttributeDeclaration(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column, id)

    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        mips_visitor.add_attribute(
            f"    # attribute {self.id}: {self.type}\n" +
            f"    li $t0, {NULL}\n" +
            f"    sw $t0, {mips_visitor.class_memory}($v0)\n"
        )
        mips_visitor.class_memory += 4
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        ...
        # visitor.visit_attribute_declaration(self)


class AttributeInicialization(Attribute):
    def __init__(self, line: int, column: int, id: str, type: str = None, expr: Node = None) -> None:
        self.type = type
        self.expr = expr
        self.id = id
        super().__init__(line, column, id)
    
    def codegen(self, mips_visitor: MipsVisitor):
        mips_visitor.visit_attribute(self)
        expr = self.expr.codegen(mips_visitor)
        # TODO
        match self.type:
            case "Int":
                mips_visitor.add_attribute(
                    f"    # attribute {self.id}: {self.type}\n" +
                    expr +
                    f"    sw $t0, {mips_visitor.class_memory}($v0)\n"
                )
                mips_visitor.class_memory += 4
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
        mips_visitor.unvisit_attribute(self)

    def check(self, visitor):
        visitor.visit_attribute_inicialization(self)


class Formal(Node):
    def __init__(self, line: int, column: int, id: str, type: str = None) -> None:
        self.type = type
        self.id = id
        super().__init__(line, column)

    # TODO
    def codegen(self):
        raise NotImplementedError()

    def check(self, visitor):
        raise NotImplementedError()
