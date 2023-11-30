from collections import defaultdict
from typing import Optional

from codegen import cil_ast as cil
from parsing.ast import (
    AssignNode,
    AttributeNode,
    BinaryOperator,
    BinaryOperatorNode,
    BlockNode,
    BooleanNode,
    ClassNode,
    IdentifierNode,
    IntegerNode,
    LetNode,
    MethodCallNode,
    MethodNode,
    NotNode,
    ProgramNode,
    StringNode,
    WhileNode,
)
from semantic.context import Context
from semantic.scope import Scope
from semantic.types import SelfType, Type
from utils.visitor import Visitor


class COOL2CIL(Visitor):
    def __init__(self) -> None:
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.type = SelfType()
        self.params = []
        self.locals = []
        self.instructions = []

        self.attrs = {}
        self.methods = {}

        self.label = defaultdict(lambda: 0)

    def visit__ProgramNode(
        self, node: ProgramNode, context: Context, scope: Scope
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

        self.register_builtins(context.types)

        for scope_index, cool_class in enumerate(node.classes):
            cool_class.accept(self, context=context, scope=scope.children[scope_index])

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    def visit__ClassNode(self, node: ClassNode, context: Context, scope: Scope):
        self.type = context.get_type(node.name)
        self.clear_state()
        self_local = self.add_local("self")

        self.instructions.append(cil.AllocateNode(self.type.name, self_local))

        for attr, (i, htype) in self.attrs[self.type.name].items():
            attr_local = self.add_local(attr)
            self.instructions.append(cil.ArgNode(self_local))
            self.instructions.append(
                cil.StaticCallNode(
                    self.get_func_id(htype.name, f"{attr}___init"),
                    attr_local,
                )
            )
            self.instructions.append(cil.SetAttrNode(self_local, i, attr_local))
        self.instructions.append(cil.ReturnNode(self_local))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(self.type.name, "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        for feat in node.features:
            function = feat.accept(self, context=context, scope=scope)
            self.dotcode.append(function)

    def visit__AttributeNode(
        self, node: AttributeNode, context: Context, scope: Scope
    ) -> cil.FunctionNode:
        self.clear_state()
        self.add_param("self")
        if node.init is not None:
            attr_type = scope.find_variable_or_attribute(node.name, self.type)
            assert attr_type is not None  # Semantic correctness
            sid = node.init.accept(self, context=context, scope=scope)
            if attr_type.type.name in ["Int", "Bool", "String"]:
                sid = self.register_new(node.attr_type.type.name, sid)  # boxing
        else:
            sid = self.register_default(node.attr_type)
        self.instructions.append(cil.ReturnNode(sid))
        return cil.FunctionNode(
            self.get_func_id(self.type.name, f"{node.attr_type}___init"),
            self.params,
            self.locals,
            self.instructions,
        )

    def visit__MethodNode(
        self, node: MethodNode, context: Context, scope: Scope
    ) -> cil.FunctionNode:
        self.clear_state()
        self.add_param("self")
        for formal in node.formals:
            self.add_param(formal.name)

        sid = node.body.accept(
            self, context=context, scope=scope.get_child(self.type.name, node.name)
        )
        self.instructions.append(cil.ReturnNode(sid))
        return cil.FunctionNode(
            self.get_func_id(self.type.name, node.name),
            self.params,
            self.locals,
            self.instructions,
        )

    def visit__BlockNode(self, node: BlockNode, context: Context, scope: Scope):
        sid = None
        for expr in node.expressions:
            sid = expr.accept(self, context=context, scope=scope)
        assert sid is not None  # Semantic correct => Block nonempty
        return sid

    def visit__AssignNode(self, node: AssignNode, context: Context, scope: Scope):
        rhs_local = node.expr.accept(self, context=context, scope=scope)

        lhs_data = scope.find_variable_or_attribute(node.name, self.type)
        assert lhs_data is not None
        if lhs_data.type.name in ["Int", "Bool", "String"]:
            rhs_local = self.register_new(lhs_data.type.name, rhs_local)  # boxing

        local_sid = self.get_local(node.name)
        if any(local_sid == l.name for l in self.locals):
            self.instructions.append(cil.AssignNode(local_sid, rhs_local))
            return local_sid

        param_sid = self.get_param(node.name)
        if any(param_sid == p.name for p in self.params):
            self.instructions.append(cil.AssignNode(param_sid, rhs_local))
            return param_sid

        attr_id = self.get_attr_id(self.type.name, node.name)
        self.instructions.append(
            cil.SetAttrNode(self.get_param("self"), attr_id, rhs_local)
        )
        return rhs_local

    def visit__MethodCallNode(
        self, node: MethodCallNode, context: Context, scope: Scope
    ):
        return_local = self.add_local()

        meth = self.type.get_method(node.method)
        sid = self.get_param("self")
        # Translate all call arguments to cil
        args = [cil.ArgNode(sid)]
        for arg_expr, param_type in zip(node.args, meth.param_types):
            arg_sid = arg_expr.accept(self, context=context, scope=scope)
            if param_type.name in ["Int", "Bool", "String"]:
                arg_sid = self.register_new(param_type.name, arg_sid)  # boxing
            args.append(cil.ArgNode(arg_sid))

        typeof_local = self.add_local()
        self.instructions.append(cil.TypeOfNode(sid, typeof_local))

        self.instructions.extend(args)
        method_id = self.get_method_id(self.type.name, node.method)
        self.instructions.append(
            cil.DynamicCallNode(typeof_local, method_id, return_local)
        )
        return return_local

    def visit__LetNode(self, node: LetNode, context: Context, scope: Scope):
        let_scope = scope.get_child(scope.class_name, scope.method_name)
        for var_name, var_type, init_expr, _ in node.bindings:
            lhs_local = self.get_local(var_name)
            if not any(lhs_local == l.name for l in self.locals):
                lhs_local = self.add_local(var_name)
            if init_expr is not None:
                rhs_local = init_expr.accept(self, context=context, scope=let_scope)
                if var_type in ["Int", "Bool", "String"]:
                    rhs_local = self.register_new(var_type, rhs_local)  # boxing
                self.instructions.append(cil.AssignNode(lhs_local, rhs_local))
            else:
                self.register_default(var_name, dest=lhs_local)

        return node.body.accept(self, context=context, scope=let_scope)

    def visit__WhileNode(self, node: WhileNode, context: Context, scope: Scope):
        while_label = self.get_label("while_label")
        loop_label = self.get_label("loop_label")
        pool_label = self.get_label("pool_label")

        # Label while
        self.instructions.append(cil.LabelNode(while_label))

        # IF condition GOTO loop
        while_ret = node.condition.accept(self, context=context, scope=scope)
        self.instructions.append(cil.GotoIfGtNode(while_ret, loop_label))

        # GOTO pool
        self.instructions.append(cil.GotoNode(pool_label))

        # Label loop
        self.instructions.append(cil.LabelNode(loop_label))
        node.body.accept(self, context=context, scope=scope)

        # GOTO while
        self.instructions.append(cil.GotoNode(while_label))

        # Label pool
        self.instructions.append(cil.LabelNode(pool_label))

        return self.register_new("Void")

    def visit__NotNode(self, node: NotNode, context: Context, scope: Scope):
        ret_local = self.add_local()
        sid = node.expr.accept(self, context=context, scope=scope)
        self.instructions.append(cil.MinusNode(ret_local, self.register_int(1), sid))
        return ret_local

    def visit__BinaryOperatorNode(
        self, node: BinaryOperatorNode, context: Context, scope: Scope
    ):
        left = node.left.accept(self, context=context, scope=scope)
        right = node.right.accept(self, context=context, scope=scope)

        ret_local = self.add_local()

        if node.operator == BinaryOperator.PLUS:
            self.instructions.append(cil.PlusNode(ret_local, left, right))
        elif node.operator == BinaryOperator.MINUS:
            self.instructions.append(cil.MinusNode(ret_local, left, right))

        elif node.operator == BinaryOperator.TIMES:
            self.instructions.append(cil.StarNode(ret_local, left, right))

        elif node.operator == BinaryOperator.DIVIDE:
            self.instructions.append(cil.DivNode(ret_local, left, right))

        elif node.operator == BinaryOperator.LT:
            cond_local = self.add_local()
            self.instructions.append(cil.MinusNode(cond_local, left, right))

            then_label = self.get_label("then")
            continue_label = self.get_label("continue")

            # IF condition GOTO then_label
            self.instructions.append(cil.GotoIfLtNode(cond_local, then_label))

            # Label else_label
            self.instructions.append(cil.AssignNode(ret_local, self.register_int(0)))
            # GoTo continue_label
            self.instructions.append(cil.GotoNode(continue_label))

            # Label then_label
            self.instructions.append(cil.LabelNode(then_label))
            self.instructions.append(cil.AssignNode(ret_local, self.register_int(1)))

            # Label continue_label
            self.instructions.append(cil.LabelNode(continue_label))

        elif node.operator == BinaryOperator.LE:
            cond_local = self.add_local()
            self.instructions.append(cil.MinusNode(cond_local, left, right))
            self.instructions.append(
                cil.MinusNode(cond_local, cond_local, self.register_int(1))
            )

            ret_local = self.add_local()
            then_label = self.get_label("then")
            continue_label = self.get_label("continue")

            # IF condition GOTO then_label
            self.instructions.append(cil.GotoIfLtNode(cond_local, then_label))

            # Label else_label
            self.instructions.append(cil.AssignNode(ret_local, self.register_int(0)))
            # GoTo continue_label
            self.instructions.append(cil.GotoNode(continue_label))

            # Label then_label
            self.instructions.append(cil.LabelNode(then_label))
            self.instructions.append(cil.AssignNode(ret_local, self.register_int(1)))

            # Label continue_label
            self.instructions.append(cil.LabelNode(continue_label))

        elif node.operator == BinaryOperator.EQ:
            cond_local = self.add_local()

            assert node.left.type
            if node.left.type.name == "String":
                self.instructions.append(cil.StrEqNode(cond_local, left, right))
                self.instructions.append(
                    cil.MinusNode(cond_local, self.register_int(1), cond_local)
                )
            else:
                self.instructions.append(cil.MinusNode(cond_local, left, right))

            ret_local = self.add_local()
            then_label = self.get_label("then")
            continue_label = self.get_label("continue")

            # IF condition GOTO then_label
            self.instructions.append(cil.GotoIfEqNode(cond_local, then_label))

            # Label else_label
            self.instructions.append(cil.AssignNode(ret_local, self.register_int(0)))
            # GoTo continue_label
            self.instructions.append(cil.GotoNode(continue_label))

            # Label then_label
            self.instructions.append(cil.LabelNode(then_label))
            self.instructions.append(cil.AssignNode(ret_local, self.register_int(1)))

            # Label continue_label
            self.instructions.append(cil.LabelNode(continue_label))

        return ret_local

    def visit__IntegerNode(self, node: IntegerNode, context: Context, scope: Scope):
        return self.register_int(int(node._value))

    def visit__BooleanNode(self, node: BooleanNode, context: Context, scope: Scope):
        return self.register_int(1 if node.value == "true" else 0)

    def visit__StringNode(self, node: StringNode, context: Context, scope: Scope):
        return self.add_data("STR", f'"{node._value}"')

    def visit__IdentifierNode(
        self, node: IdentifierNode, context: Context, scope: Scope
    ):
        local_sid = self.get_local(node.name)
        if any(local_sid == l.name for l in self.locals):
            return local_sid

        param_sid = self.get_param(node.name)
        if any(param_sid == p.name for p in self.params):
            return param_sid

        local_sid = self.add_local()
        attr_id = self.get_attr_id(self.type.name, node.name)
        self.instructions.append(
            cil.GetAttrNode(self.get_param("self"), attr_id, local_sid)
        )
        return local_sid

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

    def get_attr_id(self, type_name: str, name: str):
        attr_id, _ = self.attrs[type_name][name]
        return attr_id

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

    def register_builtins(self, types):
        # Abort
        self.register_object__abort()

        # IO
        self.register_io__out_string()
        self.register_io__out_int()
        self.register_io__in_string()
        self.register_io__in_int()

        # String
        self.register_string__length()
        self.register_string__concat()
        self.register_string__substr()

        # Inits
        self.register_int_init()
        self.register_bool_init()
        self.register_string_init()
        self.register_object_init()

        for type_name, t in types.items():
            self.register_conforms_to(type_name, t.parent and t.parent.name)

            self.register_type_name(t.name)
            self.register_copy(t.name)

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

    def register_io__out_string(self):
        self.clear_state()
        self_param = self.add_param("self")
        str_param = self.add_param("str")
        str_param_instance = self.register_new("String", str_param)

        self.instructions.append(cil.PrintNode(str_param_instance, True))
        self.instructions.append(cil.ReturnNode(self_param))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "out_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io__out_int(self):
        self.clear_state()
        self_param = self.add_param("self")
        int_param = self.add_param("int")
        int_param_instance = self.register_new("Int", int_param)

        self.instructions.append(cil.PrintNode(int_param_instance, False))
        self.instructions.append(cil.ReturnNode(self_param))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "out_int"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io__in_string(self):
        self.clear_state()
        self_param = self.add_param("self")
        dest = self.add_local()
        self.instructions.append(cil.ReadNode(dest, is_string=True))
        self.instructions.append(cil.ReturnNode(dest))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "in_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io__in_int(self):
        self.clear_state()
        self_param = self.add_param("self")
        dest = self.add_local()
        self.instructions.append(cil.ReadNode(dest, is_string=False))
        self.instructions.append(cil.ReturnNode(dest))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "in_int"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string__length(self):
        self.clear_state()
        self_param = self.add_param("self")
        length_local = self.add_local()
        self.instructions.append(cil.LengthNode(length_local, self_param))
        self.instructions.append(cil.ReturnNode(length_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "length"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string__concat(self):
        self.clear_state()
        self_param = self.add_param("self")
        str_param = self.add_param("s")

        # Calcular la longitud de las cadenas
        self_length = self.add_local()
        str_length = self.add_local()
        self.instructions.append(cil.LengthNode(self_length, self_param))
        self.instructions.append(cil.LengthNode(str_length, str_param))

        # Concatenar las cadenas
        concat_local = self.add_local()
        total_length = self.add_local()  # Longitud total para la cadena resultante
        self.instructions.append(cil.PlusNode(total_length, self_length, str_length))

        self.instructions.append(
            cil.ConcatNode(concat_local, self_param, str_param, total_length)
        )
        self.instructions.append(cil.ReturnNode(concat_local))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "concat"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string__substr(self):
        self.clear_state()
        self_param = self.add_param("self")
        index_param = self.add_param("i")
        length_param = self.add_param("l")
        substr_local = self.add_local()
        self.instructions.append(
            cil.SubstringNode(substr_local, self_param, length_param, index_param)
        )
        self.instructions.append(cil.ReturnNode(substr_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "substr"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_object_init(self):
        self.clear_state()
        self_local = self.add_local("self")
        self.instructions.append(cil.AllocateNode("Object", self_local))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Object", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_int_init(self):
        self.clear_state()
        value_param = self.add_param("value")
        self_local = self.add_local("self")
        self.instructions.append(cil.AllocateNode("Int", self_local))
        self.instructions.append(cil.SetAttrNode(self_local, 0, value_param))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Int", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_bool_init(self):
        self.clear_state()
        value_param = self.add_param("value")
        self_local = self.add_local("self")
        self.instructions.append(cil.AllocateNode("Bool", self_local))
        self.instructions.append(cil.SetAttrNode(self_local, 0, value_param))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Bool", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string_init(self):
        self.clear_state()
        value_param = self.add_param("value")
        self_local = self.add_local("self")
        self.instructions.append(cil.AllocateNode("String", self_local))
        self.instructions.append(cil.SetAttrNode(self_local, 0, value_param))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def get_label(self, name: str):
        label = f"LABEL_{name}_{self.label[name]}"
        self.label[name] += 1
        return label

    def register_int(self, value: int, name: Optional[str] = None):
        return_sid = self.add_local(name)
        self.instructions.append(cil.LoadNode(return_sid, value))
        return return_sid

    def register_type_name(self, type: str):
        self.clear_state()
        self.add_param("self")
        type_name = self.add_data(f"TYPE_NAME_{type}", f'"{type}"')
        self.instructions.append(cil.ReturnNode(type_name))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(type, "type_name"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_copy(self, type: str):
        self.clear_state()
        self_param = self.add_param("self")
        copy_local = self.add_local("copy")
        self.instructions.append(cil.AllocateNode(type, copy_local))
        for attr, _ in self.attrs[type].values():
            attr_copy_local = self.add_local("attr_copy")
            self.instructions.append(cil.GetAttrNode(self_param, attr, attr_copy_local))
            self.instructions.append(cil.SetAttrNode(copy_local, attr, attr_copy_local))

        self.instructions.append(cil.ReturnNode(copy_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(type, "copy"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_conforms_to(self, type, parent=None):
        self.clear_state()
        other_param = self.add_param("other_type")

        type_local = self.add_local()
        self.instructions.append(cil.LoadNode(type_local, type))

        then_label = self.get_label("then")

        # IF condition GOTO then_label
        types_eq_local = self.add_local()
        self.instructions.append(cil.MinusNode(types_eq_local, type_local, other_param))
        self.instructions.append(cil.GotoIfEqNode(types_eq_local, then_label))

        # Label else_label
        if parent is None:
            self.instructions.append(cil.ReturnNode(self.register_int(0)))
        else:
            recursive_local = self.add_local("rec_call")
            parent_type_local = self.add_local()
            self.instructions.append(cil.LoadNode(parent_type_local, parent))
            method_id = self.get_method_id("Object", "__conforms_to")
            self.instructions.append(cil.ArgNode(other_param))
            self.instructions.append(
                cil.DynamicCallNode(parent_type_local, method_id, recursive_local)
            )
            self.instructions.append(cil.ReturnNode(recursive_local))

        # Label then_label
        self.instructions.append(cil.LabelNode(then_label))
        self.instructions.append(cil.ReturnNode(self.register_int(1)))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(type, "__conforms_to"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_default(self, type: str, dest: Optional[str] = None):
        if type == "Int" or type == "Bool":
            val = self.register_int(0)
            if dest is not None:
                self.instructions.append(cil.AssignNode(dest, val))
                return dest
            return val
        elif type == "String":
            val = self.add_data("DEFAULT_STR", '""')
            if dest is not None:
                self.instructions.append(cil.AssignNode(dest, val))
                return dest
            return val
        else:
            return self.register_new("Void", dest=dest)
