from codegen import cil_ast as cil
from codegen import mips_ast as mips
from utils.visitor import Visitor

REGISTER_NAMES = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9"]
ARG_REGISTERS_NAMES = ["a0", "a1", "a2", "a3"]

INSTANCE_METADATA_SIZE = 4

REGISTERS = [mips.RegisterNode(name) for name in REGISTER_NAMES]
ARG_REGISTERS = [mips.RegisterNode(name) for name in ARG_REGISTERS_NAMES]
FP_REG = mips.RegisterNode("fp")
SP_REG = mips.RegisterNode("sp")
RA_REG = mips.RegisterNode("ra")
V0_REG = mips.RegisterNode("v0")
V1_REG = mips.RegisterNode("v1")


class MemoryManager:
    def __init__(self):
        self.registers = REGISTERS
        self.used = []
        self.saved = []

    def get_unused_register(self):
        possibles = list(set(self.registers).difference(set(self.used)))
        reg = possibles[0]
        self.used.append(reg)
        return reg

    def clean(self):
        self.used = self.saved
        self.saved = []

    def save(self):
        self.saved = self.used.copy()


class CILVisitor(Visitor):
    def __init__(self):
        self.data_section = {}
        self.types = {}

    def visit__ProgramNode(self, node: cil.ProgramNode, *args, **kwargs):
        text_section = []
        for data in node.dotdata:
            _ = data.accept(self, *args, **kwargs)

        for ty in node.dottypes:
            _ = ty.accept(self, *args, **kwargs)

        for function in node.dotcode:
            instructions = function.accept(self, *args, **kwargs)
            text_section.extend(instructions)

        return mips.ProgramNode(
            mips.TextNode(text_section), mips.DataSectionNode(self.data_section)
        )

    def visit__TypeNode(self, node: cil.TypeNode, *args, **kwargs):
        self.types[node.name] = node

        self.data_section[node.name] = mips.DataNode(
            mips.LabelNode(node.name),
            ".word",
            [mips.LabelNode(f"{method.id}") for method in node.methods],
        )

    def visit__DataNode(self, node: cil.DataNode):
        pass

    def visit__FunctionNode(self, node, *args, **kwargs):
        return []

    def visit__ParamNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo ParamNode
        # ...

    def visit__LocalNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo LocalNode
        # ...

    def visit__VariableNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo VariableNode
        # ...

    def visit__InstructionNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo InstructionNode
        # ...

    # Aquí agregarías métodos visit__ específicos para cada tipo de instrucción
    # Por ejemplo:
    def visit__AssignNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo AssignNode
        # ...

    def visit__ArithmeticNode(self, node, *args, **kwargs):
        pass  # Procesar el nodo ArithmeticNode
        # ...
