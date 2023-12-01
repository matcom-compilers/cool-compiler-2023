from codegen import cil_ast as cil
from parsing.ast import (
    AssignNode,
    AttributeNode,
    BlockNode,
    ClassNode,
    IdentifierNode,
    IntegerNode,
    MethodCallNode,
    MethodNode,
    ProgramNode,
)
from semantic.context import Context
from semantic.scope import Scope, VariableInfo
from semantic.types import VoidType
from utils.visitor import Visitor


class COOL2CIL(Visitor):
    def __init__(self):
        self.types = []
        self.code = []
        self.data = []
        self.current_type = None
        self.current_function = None
        self.string_count = 0
        self._count = 0
        self.internal_count = 0
        self.context = None
        self.methods = {}
        self.attrs = {}

    def generate_next_string_id(self):
        self.string_count += 1
        return "string_" + str(self.string_count)

    def next_id(self):
        self._count += 1
        return str(self._count)

    def to_function_name(self, method_name, type_name):
        return f"{type_name}__{method_name}"

    def to_data_name(self, type_name, value):
        return f"{type_name}_{value}"

    def to_attr_name(self, type_name, attr_name):
        return f"{type_name}__{attr_name}"

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def get_method_id(self, typex, name):
        method_id, _ = self.methods[typex][name]
        return method_id

    def register_instruction(self, instruction):
        self.current_function.instructions.append(instruction)

    def register_type(self, name):
        type_node = cil.TypeNode(name, [], [])
        self.types.append(type_node)
        return type_node

    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.code.append(function_node)
        return function_node

    def get_local(self, name):
        return f"_l_{name}"

    def register_local(self, name=None):
        local_name = (
            f"_l_{name}" if name else f"_l_{len(self.current_function.localvars)}"
        )
        local_node = cil.LocalNode(local_name)
        self.current_function.localvars.append(local_node)
        return local_name

    def register_param(self, value_info):
        value_info.name = self.build_internal_vname(value_info.name)
        arg_node = cil.ParamNode(value_info.name)
        self.params.append(arg_node)
        return value_info

    def get_param(self, name):
        return f"param_{name}"

    def build_internal_vname(self, vname):
        vname = f"param_{vname}"
        self.internal_count += 1
        return vname

    def define_internal_local(self):
        return self.register_local()

    def is_attribute(self, vname):
        return vname not in [var.name for var in self.current_function.localvars] and (
            vname not in [param.name for param in self.current_function.params]
        )

    def add_builtin_init(self):
        builtin_types = ["Object", "IO", "Int", "Bool", "String"]
        for typex in builtin_types:
            self.current_function = cil.FunctionNode(
                self.to_function_name("init", typex), [], [], []
            )
            self.params.append(cil.ParamNode("self"))

            self.register_instruction(cil.ReturnNode("self"))
            self.code.append(self.current_function)

        self.current_function = None

    def register_init(self, node: ClassNode):
        self.current_function = self.register_function(
            self.to_function_name("init", node.name)
        )

        self.params.append(cil.ParamNode("self"))
        self.current_type.define_method("init", [], [], "Object")

        for attr, (_, typex) in self.attrs[self.current_type.name].items():
            instance = self.define_internal_local()
            self.register_instruction(cil.ArgNode("self"))
            self.register_instruction(
                cil.StaticCallNode(
                    self.to_function_name(f"{attr}__init", typex), instance
                )
            )
            self.register_instruction(
                cil.SetAttrNode(
                    "self", self.to_attr_name(node.name, attr), instance, node.name
                )
            )

        self.register_instruction(cil.ReturnNode("self"))

    def add_builtin_functions(self):
        # Object
        object_type = cil.TypeNode(
            "Object",
            [],
            [
                self.cil_predef_method("abort", "Object", self.object_abort),
                self.cil_predef_method("copy", "Object", self.object_copy),
                self.cil_predef_method("type_name", "Object", self.object_type_name),
            ],
        )

        # "IO"

        io_type = cil.TypeNode(
            "IO",
            [],
            [
                self.cil_predef_method("abort", "IO", self.object_abort),
                self.cil_predef_method("copy", "IO", self.object_copy),
                self.cil_predef_method("type_name", "IO", self.object_type_name),
                self.cil_predef_method("out_string", "IO", self.register_io_out_string),
                self.cil_predef_method("out_int", "IO", self.register_io_out_int),
                self.cil_predef_method("in_string", "IO", self.register_io_in_string),
                self.cil_predef_method("in_int", "IO", self.register_io_in_int),
            ],
        )

        # String
        self.attrs["String"] = {"length": (0, "Int"), "str_ref": (1, "String")}
        string_type = cil.TypeNode(
            "String",
            [cil.AttributeNode("length"), cil.AttributeNode("str_ref")],
            [
                self.cil_predef_method("abort", "String", self.object_abort),
                self.cil_predef_method("copy", "String", self.object_copy),
                self.cil_predef_method("type_name", "String", self.object_type_name),
                self.cil_predef_method("length", "String", self.string_length),
                self.cil_predef_method("concat", "String", self.string_concat),
                self.cil_predef_method("substr", "String", self.string_substr),
            ],
        )

        # Int
        int_type = cil.TypeNode(
            "Int",
            [cil.AttributeNode("value")],
            [
                self.cil_predef_method("abort", "Int", self.object_abort),
                self.cil_predef_method("copy", "Int", self.object_copy),
                self.cil_predef_method("type_name", "Int", self.object_type_name),
            ],
        )

        # Bool
        bool_type = cil.TypeNode(
            "Bool",
            [cil.AttributeNode("value")],
            [
                self.cil_predef_method("abort", "Bool", self.object_abort),
                self.cil_predef_method("copy", "Bool", self.object_copy),
                self.cil_predef_method("type_name", "Bool", self.object_type_name),
            ],
        )

        for typex in [object_type, io_type, string_type, int_type, bool_type]:
            self.types.append(typex)

    # predefined functions cil
    def cil_predef_method(self, mname, cname, specif_code):
        self.current_type = self.context.get_type(cname)
        self.current_method = self.current_type.get_method(mname)
        self.current_function = cil.FunctionNode(
            self.to_function_name(mname, cname), [], [], []
        )

        if mname == "abort":
            specif_code(cname)
        else:
            specif_code()

        self.code.append(self.current_function)
        self.current_function = None
        self.current_type = None

        return cil.MethodNode(mname, self.to_function_name(mname, cname))

    def register_abort(self):
        self.current_function = cil.FunctionNode(
            self.to_function_name("abort", self.current_type.name), [], [], []
        )
        self.object_abort(self.current_type.name)
        self.code.append(self.current_function)
        self.current_function = None

    def register_copy(self):
        self.current_function = cil.FunctionNode(
            self.to_function_name("copy", self.current_type.name), [], [], []
        )
        self.object_copy()
        self.code.append(self.current_function)
        self.current_function = None

    def register_type_name(self):
        self.current_function = cil.FunctionNode(
            self.to_function_name("type_name", self.current_type.name), [], [], []
        )
        self.object_type_name()
        self.code.append(self.current_function)
        self.current_function = None

    def string_length(self):
        self.params.append(cil.ParamNode("self"))

        result = self.define_internal_local()

        self.register_instruction(cil.LengthNode(result, "self"))
        self.register_instruction(cil.ReturnNode(result))

    def string_concat(self):
        self.params.append(cil.ParamNode("self"))
        other_arg = VariableInfo("other_arg")
        self.register_param(other_arg)

        ret_vinfo = self.define_internal_local()

        self.register_instruction(cil.ConcatNode(ret_vinfo, "self", other_arg.name))
        self.register_instruction(cil.ReturnNode(ret_vinfo))

    def string_substr(self):
        self.params.append(cil.ParamNode("self"))
        idx_arg = VariableInfo("idx_arg")
        self.register_param(idx_arg)
        length_arg = VariableInfo("length_arg")
        self.register_param(length_arg)

        ret_vinfo = self.define_internal_local()

        self.register_instruction(
            cil.SubstringNode(ret_vinfo, "self", idx_arg.name, length_arg.name)
        )
        self.register_instruction(cil.ReturnNode(ret_vinfo))

    def object_abort(self, type):
        self.data.append(
            cil.DataNode(f"abort_{type}", f'"Abort called from class {type}\n"')
        )
        error = f"abort_{type}"
        self.register_instruction(cil.RuntimeErrorNode(error))

    def object_copy(self):
        self.params.append(cil.ParamNode("self"))
        copy_local = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(self.current_type.name, copy_local))

        for attr in self.attrs[self.current_type.name].keys():
            attr_copy_local = self.define_internal_local()
            attr_name = (
                self.to_attr_name(self.current_type.name, attr)
                if self.current_type.name not in ["Int", "String", "Bool"]
                else attr
            )
            self.register_instruction(
                cil.GetAttrNode(
                    "self",
                    attr_name,
                    attr_copy_local,
                    self.current_type.name,
                )
            )
            self.register_instruction(
                cil.SetAttrNode(
                    copy_local,
                    attr_name,
                    attr_copy_local,
                    self.current_type.name,
                )
            )

        self.register_instruction(cil.ReturnNode(copy_local))

    def object_type_name(self):
        self.params.append(cil.ParamNode("self"))
        label = f"TYPE_NAME_{self.current_type.name}"
        self.data.append(cil.DataNode(label, f'"{self.current_type.name}"'))
        type_name = self.define_internal_local()
        self.register_instruction(
            cil.LoadNode(type_name, label, self.current_type.name)
        )
        self.register_instruction(cil.ReturnNode(type_name))

    def register_io_out_string(self):
        self.params.append(cil.ParamNode("self"))
        str_arg = VariableInfo("str")
        self.register_param(str_arg)
        self.register_instruction(cil.PrintNode(str_arg.name, True))
        self.register_instruction(cil.ReturnNode("self"))

    def register_io_out_int(self):
        self.params.append(cil.ParamNode("self"))
        int_arg = VariableInfo("int")
        self.register_param(int_arg)
        self.register_instruction(cil.PrintNode(int_arg.name, False))
        self.register_instruction(cil.ReturnNode("self"))

    def register_io_in_string(self):
        self.params.append(cil.ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(cil.ReadNode(ret_vinfo, True))
        self.register_instruction(cil.ReturnNode(ret_vinfo))

    def register_io_in_int(self):
        self.params.append(cil.ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(cil.ReadNode(ret_vinfo, False))
        self.register_instruction(cil.ReturnNode(ret_vinfo))

    def clear_state(self):
        self.types = []
        self.code = []
        self.data = []
        self.current_type = None
        self.current_function = None
        self.string_count = 0
        self._count = 0
        self.context = None

    def visit__ProgramNode(
        self, node: ProgramNode, context: Context, scope: Scope, return_var=None
    ):
        self.context = context

        for type in self.context.types.values():
            self.attrs[type.name] = {
                attr.name: (i, htype.name)
                for i, (attr, htype) in enumerate(type.all_attributes())
            }
            self.methods[type.name] = {
                method.name: (i, htype.name)
                if htype.name != "Object"
                or method.name not in ["abort", "type_name", "copy"]
                else (i, type.name)
                for i, (method, htype) in enumerate(type.all_methods())
            }

        self.current_function = cil.FunctionNode("main", [], [], [])
        self.code.append(self.current_function)

        main_init = self.to_function_name("init", "Main")
        main_method_name = self.to_function_name("main", "Main")

        # Get instance from constructor
        a = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Main", a))
        self.register_instruction(cil.ArgNode(a))
        instance = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode(main_init, instance))

        # Pass instance as parameter and call Main__main
        result = self.define_internal_local()
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))

        # self.register_instruction(ReturnNode(0))
        self.register_instruction(cil.ExitNode(0))

        self.current_function = None

        self.add_builtin_functions()
        self.add_builtin_init()

        for cls in node.classes:
            cls.accept(self, context=context, scope=scope)

        program_node = cil.ProgramNode(self.types, self.data, self.code)

        self.clear_state()

        return program_node

    def visit__ClassNode(
        self, node: ClassNode, context: Context, scope: Scope, return_var=None
    ):
        self.current_type = self.context.get_type(node.name)

        self.register_abort()
        self.register_copy()
        self.register_type_name()

        type_node = self.register_type(self.current_type.name)

        current_type = self.current_type
        while current_type is not None:
            attributes = [
                cil.AttributeNode(node.name + "__" + attr.name, attr.type)
                for attr in current_type.attributes
            ]

            type_node.attributes.extend(attributes[::-1])

            current_type = current_type.parent

        type_node.attributes.reverse()

        type_node.methods = [
            cil.MethodNode(method_name, self.to_function_name(method_name, typex))
            for method_name, (_, typex) in self.methods[node.name].items()
        ]

        self.register_init(node)

        for feature in node.features:
            feature.accept(self, context=context, scope=scope)

    def visit__AttributeNode(
        self, node: AttributeNode, context: Context, scope: Scope, return_var=None
    ):
        self.current_function = self.register_function(
            self.to_function_name(f"{node.name}__init", self.current_type.name)
        )

        self.params.append(cil.ParamNode("self"))

        # Assign init_expr if not None
        if node.init:
            init_expr_value = self.define_internal_local()
            node.init.accept(
                self, context=context, scope=scope, return_var=init_expr_value
            )
            self.register_instruction(cil.ReturnNode(init_expr_value))

        else:  # Assign default value
            default_var = self.define_internal_local()
            self.register_instruction(cil.DefaultValueNode(default_var, node.attr_type))
            self.register_instruction(cil.ReturnNode(default_var))

        self.current_function = None

    def visit__MethodNode(
        self, node: MethodNode, context: Context, scope: Scope, return_var=None
    ):
        self.current_method = self.current_type.get_method(node.name)

        self.current_function = self.register_function(
            self.to_function_name(node.name, self.current_type.name)
        )

        # Add params
        self.current_function.params.append(cil.ParamNode("self"))
        for formal in node.formals:
            self.register_param(VariableInfo(formal.name))

        # Body
        value = self.define_internal_local()
        node.body.accept(self, context=context, scope=scope, return_var=value)

        # Return
        if isinstance(self.current_method.return_type, VoidType):
            value = None

        self.register_instruction(cil.ReturnNode(value))

        self.current_method = None
        self.current_function = None

    def visit__AssignNode(
        self, node: AssignNode, context: Context, scope: Scope, return_var
    ):
        node.expr.accept(self, context, scope, return_var)

        local_id = self.get_local(node.name)
        if any(local_id == l.name for l in self.current_function.localvars):
            self.register_instruction(cil.AssignNode(local_id, return_var))
            return

        param_id = self.get_param(node.name)
        if any(param_id == p.name for p in self.current_function.params):
            self.register_instruction(cil.AssignNode(param_id, return_var))
            return

        self.register_instruction(
            cil.SetAttrNode(
                "self",
                self.to_attr_name(self.current_type.name, node.name),
                return_var,
                self.current_type.name,
            )
        )

    def visit__MethodCallNode(
        self, node: MethodCallNode, context: Context, scope: Scope, return_var
    ):
        obj_type = self.current_type.name
        instance = self.define_internal_local()

        self.register_instruction(cil.AssignNode(instance, "self"))

        instance_type = self.define_internal_local()

        if obj_type in ["Int", "Bool"]:
            self.register_instruction(
                cil.TypeOfNode(instance, instance_type, True, obj_type)
            )
        else:
            self.register_instruction(cil.TypeOfNode(instance, instance_type))

        args = [instance]
        for arg in node.args:
            arg_value = self.define_internal_local()
            arg.accept(self, context, scope, arg_value)
            args.append(arg_value)

        for arg in args:
            self.register_instruction(cil.ArgNode(arg))

        method_index = self.get_method_id(obj_type, node.method)
        self.register_instruction(
            cil.DynamicCallNode(instance_type, method_index, return_var)
        )

    def visit__BlockNode(
        self, node: BlockNode, context: Context, scope: Scope, return_var
    ):
        for expr in node.expressions:
            expr.accept(self, context, scope, return_var)

    def visit__IntegerNode(
        self, node: IntegerNode, context: Context, scope: Scope, return_var
    ):
        self.register_instruction(cil.AssignNode(return_var, int(node._value)))

    def visit__IdentifierNode(
        self, node: IdentifierNode, context: Context, scope: Scope, return_var
    ):
        if node.name == "self":
            self.register_instruction(cil.AssignNode(return_var, "self"))
            return

        local_id = self.get_local(node.name)
        if any(local_id == l.name for l in self.current_function.localvars):
            self.register_instruction(cil.AssignNode(return_var, local_id))
            return

        param_id = self.get_param(node.name)
        if any(param_id == p.name for p in self.current_function.params):
            self.register_instruction(cil.AssignNode(return_var, param_id))
            return

        self.register_instruction(
            cil.GetAttrNode(
                "self",
                self.to_attr_name(self.current_type.name, node.name),
                return_var,
                self.current_type.name,
            )
        )
