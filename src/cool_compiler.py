from lexic_analysis.lexer import Lexer
from sintactic_analysis.parser_ import Parser
from type_checker.type_checker import TypeChecker
from cil_generation.cil_generator import CILCodeGenerator
from semantic_analysis.semantic import SemanticChecker
from utils.errors import *
from semantic_analysis.ast_ import *

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
        return mips_code

    def _inject_native_classes(self):
        """
        Injects the native classes such as Object, Int, String, Bool, and IO along with their methods into the compiler.
        """
        self.native_classes = [
            Class(Type('Object')),
            Class(Type('Int'), reserved_attrs=[AttrIntLiteral()], can_inherit=False, type_obj=TYPE_INT),
            Class(Type('String'), reserved_attrs=[AttrStringLength(), AttrStringLiteral()], can_inherit=False, type_obj=TYPE_STRING),
            Class(Type('Bool'), reserved_attrs=[AttrBoolLiteral()], can_inherit=False, type_obj=TYPE_BOOL),
            Class(Type('IO'))
        ]

        methods = {
            'Object': [
                Method(Id('abort'), NodeContainer(), Type('Object')),
                Method(Id('type_name'), NodeContainer(), Type('String')),
                Method(Id('copy'), NodeContainer(), Type('SELF_TYPE'))
            ],
            'String': [
                Method(Id('length'), NodeContainer(), Type('Int')),
                Method(Id('concat'), NodeContainer([Formal(Id('s'), Type('String'))]), Type('String')),
                Method(Id('substr'), NodeContainer([
                    Formal(Id('i'), Type('Int')),
                    Formal(Id('l'), Type('Int'))
                ]), Type('String'))
            ],
            'IO': [
                Method(Id('out_string'), NodeContainer([Formal(Id('x'), Type('String'))]), Type('SELF_TYPE')),
                Method(Id('out_int'), NodeContainer([Formal(Id('x'), Type('Int'))]), Type('SELF_TYPE')),
                Method(Id('in_string'), NodeContainer(), Type('String')),
                Method(Id('in_int'), NodeContainer(), Type('Int'))
            ]
        }

        for cls in self.native_classes:
            if cls.type.value in methods:
                cls.feature_list = methods[cls.type.value]

        self.root = self.native_classes[0]  # reference to the root of the inheritance tree

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