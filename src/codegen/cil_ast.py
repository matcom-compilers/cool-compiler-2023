from typing import List

tab = "\t"


class Node:
    def accept(self, visitor, *args, **kwargs):
        return visitor.visit(self, *args, **kwargs)


class ProgramNode(Node):
    def __init__(
        self,
        dottypes: List["TypeNode"],
        dotdata: List["DataNode"],
        dotcode: List["FunctionNode"],
    ):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

    def __str__(self) -> str:
        cil = "\n.TYPES\n"
        cil += "\n".join(str(type) for type in self.dottypes) + "\n"
        cil += "\n.DATA\n"
        cil += "\n".join(str(data) for data in self.dotdata) + "\n"
        cil += "\n.CODE\n"
        cil += "\n".join(str(code) for code in self.dotcode) + "\n"
        return cil


class TypeNode(Node):
    def __init__(
        self, name, attributes: List["AttributeNode"], methods: List["MethodNode"]
    ):
        self.name = name
        self.attributes = attributes
        self.methods = methods

    def __str__(self) -> str:
        cil = f"type {self.name} " + "{\n"
        for attribute in self.attributes:
            cil += f"  attribute {attribute.name};\n"
        for method in self.methods:
            cil += f"  method {method.id} : {method.function_id};\n"
        cil += "}\n"
        return cil


class AttributeNode(Node):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class MethodNode(Node):
    def __init__(self, id, function_id):
        self.id = id
        self.function_id = function_id

    def __str__(self) -> str:
        return f"method {self.id} : {self.function_id}"

    def __repr__(self) -> str:
        return self.__str__()


class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

    def __str__(self) -> str:
        return f"{self.name} = {self.value};\n"


class FunctionNode(Node):
    def __init__(
        self,
        fname,
        params: List["ParamNode"],
        localvars: List["LocalNode"],
        instructions: List["InstructionNode"],
    ):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions

    def __str__(self) -> str:
        cil = f"function {self.name} " + "{\n"
        cil += "\t\n".join(tab + str(param) for param in self.params) + "\n\n"
        cil += "\t\n".join(tab + str(local) for local in self.localvars) + "\n\n"
        cil += (
            "\t\n".join(tab + str(instruction) for instruction in self.instructions)
            + "\n"
        )
        cil += "}\n"
        return cil


class ParamNode(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return f"PARAM {self.name};"


class LocalNode(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return f"LOCAL {self.name};"


class VariableNode(Node):
    def __init__(self, name) -> None:
        self.name = name


class InstructionNode(Node):
    pass


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

    def __str__(self):
        return f"{self.dest} = {self.source} "


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class PlusNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} + {self.right};"


class MinusNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} - {self.right};"


class StarNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} * {self.right};"


class DivNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} / {self.right};"


class EqualNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} == {self.right};"


class LessNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} < {self.right};"


class LessEqualNode(ArithmeticNode):
    def __str__(self) -> str:
        return f"{self.dest} = {self.left} <= {self.right};"


class GetAttrNode(InstructionNode):
    def __init__(self, instance, attr, dest, type) -> None:
        super().__init__()
        self.instance = instance
        self.attr = attr
        self.dest = dest
        self.type = type

    def __str__(self) -> str:
        return f"{self.dest} = GETATTR {self.instance} {self.attr};"


class SetAttrNode(InstructionNode):
    def __init__(self, instance, attr, source, type) -> None:
        super().__init__()
        self.instance = instance
        self.attr = attr
        self.source = source
        self.type = type

    def __str__(self) -> str:
        return f"SETATTR {self.instance} {self.attr} {self.source}"


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

    def __str__(self) -> str:
        return f"{self.dest} = ALLOCATE {self.type};"


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest, flag=False, type=None):
        self.obj = obj
        self.dest = dest
        self.flag = flag
        self.type = type

    def __str__(self) -> str:
        return f"{self.dest} = TYPEOF {self.obj};"


class LabelNode(InstructionNode):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f"LABEL {self.name};"


class GotoNode(InstructionNode):
    def __init__(self, label) -> None:
        super().__init__()
        self.label = label

    def __str__(self) -> str:
        return f"GOTO {self.label};"


class GotoIfNode(InstructionNode):
    def __init__(self, cond, label) -> None:
        super().__init__()
        self.cond = cond
        self.label = label

    def __str__(self) -> str:
        return f"IF {self.cond} GOTO {self.label};"


class GotoIfLtNode(InstructionNode):
    def __init__(self, cond, label) -> None:
        super().__init__()
        self.cond = cond
        self.label = label

    def __str__(self) -> str:
        return f"IF {self.cond} < 0 GOTO {self.label};"


class GotoIfEqNode(InstructionNode):
    def __init__(self, cond, label) -> None:
        super().__init__()
        self.cond = cond
        self.label = label

    def __str__(self) -> str:
        return f"IF {self.cond} = 0 GOTO {self.label};"


class StrEqNode(InstructionNode):
    def __init__(self, dest, str1, str2) -> None:
        super().__init__()
        self.dest = dest
        self.str1 = str1
        self.str2 = str2

    def __str__(self) -> str:
        return f"{self.dest} = STREQ({self.str1}, {self.str2});"


class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

    def __str__(self) -> str:
        return f"{self.dest} = CALL {self.function};"


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.type = xtype
        self.method = method
        self.dest = dest

    def __str__(self) -> str:
        return f"{self.dest} = VCALL {self.type} {self.method};"


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return f"ARG {self.name};"


class ReturnNode(InstructionNode):
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"RETURN {self.value};"


class ExitNode(InstructionNode):
    def __init__(self, code) -> None:
        self.code = code

    def __str__(self) -> str:
        return f"EXIT {self.code};"


class LoadNode(InstructionNode):
    def __init__(self, dest, label, data):
        self.dest = dest
        self.label = label
        self.data = data

    def __str__(self) -> str:
        return f"{self.dest} = LOAD {self.label};"


class LengthNode(InstructionNode):
    def __init__(self, dest, string):
        self.dest = dest
        self.string = string

    def __str__(self) -> str:
        return f"{self.dest} = LENGTH {self.string};"


class ConcatNode(InstructionNode):
    def __init__(self, dest, string1, string2):
        self.dest = dest
        self.string1 = string1
        self.string2 = string2

    def __str__(self) -> str:
        return f"{self.dest} = CONCAT {self.string1} {self.string2};"


class PrefixNode(InstructionNode):
    def __init__(self, dest, string, n):
        self.dest = dest
        self.string = string
        self.n = n


class SubstringNode(InstructionNode):
    def __init__(self, dest, string, n, index):
        self.dest = dest
        self.string = string
        self.n = n
        self.index = index

    def __str__(self) -> str:
        return f"{self.dest} = SUBSTRING {self.string} {self.n};"


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

    def __str__(self) -> str:
        return f"{self.dest} = STR {self.ivalue};"


class ReadNode(InstructionNode):
    def __init__(self, dest, is_string):
        self.is_string = is_string
        self.dest = dest

    def __str__(self) -> str:
        return f"{self.dest} = READ;"


class PrintNode(InstructionNode):
    def __init__(self, str_addr, is_string):
        self.is_string = is_string
        self.str_addr = str_addr

    def __str__(self) -> str:
        return f"PRINT {self.str_addr};"


class ComplementNode(InstructionNode):
    def __init__(self, dest, source):
        self.source = source
        self.dest = dest


class DefaultValueNode(InstructionNode):
    def __init__(self, dest, type) -> None:
        self.dest = dest
        self.type = type
        super().__init__()

    def __str__(self) -> str:
        return f"{self.dest} = DEFAULT {self.type}"


class RuntimeErrorNode(InstructionNode):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self) -> str:
        return f"ERROR {self.msg}"


class IsVoidNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

    def __str__(self) -> str:
        return f"{self.dest} = ISVOID {self.value}"
