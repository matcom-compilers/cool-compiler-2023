from collections import defaultdict
from typing import Optional

from codegen import cil_ast as cil
from parsing.ast import ProgramNode
from semantic.context import Context
from utils.visitor import Visitor


class COOL2CIL(Visitor):
    def __init__(self) -> None:
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.type = None
        self.params = None
        self.locals = None
        self.instructions = None

        self.attrs = None
        self.methods = None

        self.label = defaultdict(lambda: 0)

    def visit__ProgramNode(
        self, node: ProgramNode, context: Context
    ) -> cil.ProgramNode:
        self.attrs, self.methods = dict(), dict()
        for type_name, ctype in context.types.items():
            self.attrs[type_name] = {
                attr.name: (i, attr_type.name)
                for i, (attr, attr_type) in enumerate(ctype.all_attributes())
            }
            object_specials, generated_specials = (
                ["type_name", "copy"],
                ["__conforms_to"],
            )
            self.methods[type_name] = {
                method.name: (i + len(generated_specials), attr_type.name)
                if (attr_type.name != "Object" or method.name not in object_specials)
                else (i + len(generated_specials), ctype.name)
                for i, (method, attr_type) in enumerate(ctype.all_methods())
            }

            for i, special in enumerate(generated_specials):
                self.methods[type_name][special] = (i, type_name)

            sorted_methods = sorted(
                self.methods[type_name].items(), key=lambda kv: kv[1][0]
            )
            self.dottypes.append(
                cil.TypeNode(
                    type_name,
                    [
                        cil.AttributeNode(name, ctype)
                        for name in list(self.attrs[type_name].keys())
                    ],
                    [
                        cil.MethodNode(
                            f"{ftype}__{method}", self.get_method_id(ftype, method)
                        )
                        for method, (_, ftype) in sorted_methods
                    ],
                )
            )

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    def get_method_id(self, type_name: str, method_name: str):
        return f"{type_name}__{method_name}"
