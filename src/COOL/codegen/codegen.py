from COOL.nodes import Program
from COOL.codegen.mips_visitor import MipsVisitor

class Codegen:
    @classmethod
    def execute(cls, program: Program) -> str:
        mips_visitor = MipsVisitor()
        return program.codegen(mips_visitor)
