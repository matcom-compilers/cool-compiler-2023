from collections import defaultdict
from typing import Optional

from codegen import cil_ast as cil
from parsing.ast import ClassNode, ProgramNode
from semantic.context import Context
from utils.visitor import Visitor


class COOL2CIL(Visitor):
    def __init__(self) -> None:
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.type = None
        self.params = []
        self.locals = []
        self.instructions = []

        self.attrs = {}
        self.methods = {}

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
                        cil.MethodNode(method, self.get_method_id(ftype, method))
                        for method, (_, ftype) in sorted_methods
                    ],
                )
            )

        # TYPES section Completed

        self.clear_state()
        self_local = self.add_local("self")

        self.instructions.append(cil.AllocateNode("Void", self_local))
        self.instructions.append(cil.ReturnNode(self_local))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_method_id("Void", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.clear_state()
        main_instance = self.register_new("Main")
        self.instructions.append(cil.ArgNode(main_instance))
        self.instructions.append(
            cil.StaticCallNode(self.get_method_id("Main", "main"), self.add_local())
        )
        self.instructions.append(cil.ExitNode(0))
        self.dotcode.append(
            cil.FunctionNode("main", self.params, self.locals, self.instructions)
        )

        self.register_builtins()

        for cool_class in node.classes:
            cool_class.accept(self, context)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    def visit__ClassNode(self, node: ClassNode, context: Context):
        pass

    def get_method_id(self, type_name: str, method_name: str):
        return f"{type_name}__{method_name}"

    def clear_state(self):
        self.params, self.locals, self.instructions = [], [], []

    def get_local(self, name: Optional[str]):
        return f"local_{len(self.locals) if name is None else name}"

    def add_local(self, name: Optional[str] = None):
        local = self.get_local(name)
        self.locals.append(cil.LocalNode(local))
        return local

    def register_new(self, type: str, *args, dest: Optional[str] = None):
        if dest is None:
            dest = self.add_local()
        for arg in args:
            self.instructions.append(cil.ArgNode(arg))
        self.instructions.append(
            cil.StaticCallNode(self.get_method_id(type, "__init"), dest)
        )
        return dest

    def register_builtins(self):
        # TODO: register builtin codes for nodes
        pass
