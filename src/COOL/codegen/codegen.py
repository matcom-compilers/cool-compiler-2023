from COOL.codegen.mips_visitor import MipsVisitor

class Codegen:
    @classmethod
    def codegen(cls, program) -> str:
        mips_visitor = MipsVisitor()
        return program.codegen(mips_visitor)
