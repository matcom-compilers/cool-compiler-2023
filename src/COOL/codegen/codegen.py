from COOL.nodes import Program

class Codegen:
    @classmethod
    def execute(program: Program, output_path: str):
        program.execute()
