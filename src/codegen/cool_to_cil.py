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
                        cil.MethodNode(method, self.get_func_id(ftype, method))
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
                self.get_func_id("Void", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.clear_state()
        main_instance = self.register_new("Main")
        self.instructions.append(cil.ArgNode(main_instance))
        self.instructions.append(
            cil.StaticCallNode(self.get_func_id("Main", "main"), self.add_local())
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

    def get_func_id(self, type_name: str, method_name: str):
        return f"{type_name}__{method_name}"

    def get_method_id(self, type_name: str, method_name: str):
        method_id, _ = self.methods[type_name][method_name]
        return method_id

    def clear_state(self):
        self.params, self.locals, self.instructions = [], [], []

    def get_local(self, name: Optional[str]):
        return f"_l_{len(self.locals) if name is None else name}"

    def add_local(self, name: Optional[str] = None):
        local = self.get_local(name)
        self.locals.append(cil.LocalNode(local))
        return local

    def get_param(self, name: str):
        return f"param__{name}"

    def add_param(self, name: str):
        param = self.get_param(name)
        self.params.append(cil.ParamNode(param))
        return param

    def add_data(self, name: str, value: str):
        for data in self.dotdata:
            if data.value == value:
                data_id = data.name
                break
        else:
            data_id = f"data_{len(self.dotdata)}_{name}"
            self.dotdata.append(cil.DataNode(data_id, value))

        return_sid = self.add_local()
        self.instructions.append(cil.LoadNode(return_sid, data_id))
        return return_sid

    def register_new(self, type: str, *args, dest: Optional[str] = None):
        if dest is None:
            dest = self.add_local()
        for arg in args:
            self.instructions.append(cil.ArgNode(arg))
        self.instructions.append(
            cil.StaticCallNode(self.get_func_id(type, "__init"), dest)
        )
        return dest

    def register_builtins(self):
        self.register_object__abort()

    def register_object__abort(self):
        self.clear_state()

        self_param = self.add_param("self")
        self_type = self.add_local("self")
        type_name = self.add_local("type")
        self.instructions.append(cil.TypeOfNode(self_param, self_type))
        self.instructions.append(
            cil.DynamicCallNode(
                self_type, self.get_method_id("Object", "type_name"), type_name
            )
        )
        type_name_instance = self.register_new("String", type_name)
        eol = self.register_new("String", self.add_data("EOL", '"\\n"'))
        msg = self.register_new(
            "String", self.add_data("abort_msg", '"Abort called from class "')
        )
        self.instructions.append(cil.PrintNode(msg, True))
        self.instructions.append(cil.PrintNode(type_name_instance, True))
        self.instructions.append(cil.PrintNode(eol, True))
        self.instructions.append(cil.ExitNode(1))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Object", "abort"),
                self.params,
                self.locals,
                self.instructions,
            )
        )
