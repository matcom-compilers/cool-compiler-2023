from lexer import Lexer
from parser_ import Parser
from type_checker import TypeChecker
from cil_generator import CILCodeGenerator
from semantic import SemanticChecker
from errors import *

class CoolCompiler:
    def __init__(self, code, tab_size=4):
        self.code = ''

        for c in code:
            if c == '\t':
                self.code += ' ' * tab_size
            else:
                self.code += c

        self._inject_native_classes()

    def compile_program(self):
        lexer = self.lexical_analysis()
        ast_root = self.syntactic_analysis(lexer)
        self.semantic_analysis(ast_root)
        self.run_type_checker()
        cil_code = self.gen_cil_code()
        mips_code = self.gen_mips_code(cil_code)
        print(mips_code)

    def _inject_native_classes(self):
        pass

    def _lexical_analysis(self):
        lex = Lexer()
        lex.build()
        lex.lexer.input(self.code)

        for _ in lex.lexer:
            pass

        if lex.lexer.errors:
            raise LexicographicError('\n'.join(lex.lexer.errors))

        return lex

    def _syntactic_analysis(self, lexer):
        lexer.build()

        p = Parser()
        p.build(self.code, lexer.tokens)

        return p.parser.parse(self.code)

    def _semantic_analysis(self, ast_root):
        semantics = SemanticChecker(ast_root)

        self.cls_refs = semantics.build_inheritance_tree(self.native_classes)
        semantics.check_cycles()

    def _run_type_checker(self):
        chk = TypeChecker(self.root, self.cls_refs)
        chk.visit(self.root)

    def _gen_cil_code(self):
        cil = CILCodeGenerator(self.cls_refs)
        cil.visit(self.root)

        for lst in cil.cil_code.dict_func.values():
            lst.sort(key=lambda x: x.level, reverse=True)  # sort by greater level

        return cil.cil_code

    def _gen_mips_code(self, cil_code):
        pass