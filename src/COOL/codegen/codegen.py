from COOL.nodes import Program

class Codegen:
    @classmethod
    def execute(cls, program: Program) -> str:
        return program.execute()
