class MipsAstNode:
    """Nodo base para todos los nodos del AST de MIPS."""

    def accept(self, visitor, *args, **kwargs):
        """Permite a un visitor aceptar este nodo."""
        return visitor.visit(self, *args, **kwargs)


class ProgramNode(MipsAstNode):
    """Representa un programa completo en MIPS, incluyendo secciones de texto y datos."""

    def __init__(self, text_section, data_section):
        self.text_section = text_section
        self.data_section = data_section


class TextNode(MipsAstNode):
    """Representa la sección de texto en un programa MIPS, contiene instrucciones."""

    def __init__(self, instructions):
        self.instructions = instructions


class DataSectionNode(MipsAstNode):
    """Representa la sección de datos en un programa MIPS."""

    def __init__(self, data):
        self.data = data


class DataNode(MipsAstNode):
    """Nodo para un elemento de datos en la sección de datos."""

    def __init__(self, label, storage_type, data):
        self.label = label
        self.storage_type = storage_type
        self.data = data


class RegisterNode(MipsAstNode):
    def __init__(self, number):
        self.number = number


class LabelNode(MipsAstNode):
    """Representa una etiqueta en MIPS."""

    def __init__(self, label):
        self.label = label


class InstructionNode(MipsAstNode):
    """Nodo base para todas las instrucciones MIPS."""

    pass


class SyscallNode(InstructionNode):
    """Representa la instrucción 'syscall' en MIPS."""

    pass


class AddNode(InstructionNode):
    """Nodo para la instrucción 'add' en MIPS."""

    def __init__(self, rd, rs, rt):
        self.rd = rd
        self.rs = rs
        self.rt = rt


class SubNode(InstructionNode):
    """Nodo para la instrucción 'sub' en MIPS."""

    def __init__(self, rd, rs, rt):
        self.rd = rd
        self.rs = rs
        self.rt = rt


class LoadWordNode(InstructionNode):
    """Nodo para la instrucción 'lw' en MIPS."""

    def __init__(self, rt, offset, base):
        self.rt = rt
        self.offset = offset
        self.base = base


class StoreWordNode(InstructionNode):
    """Nodo para la instrucción 'sw' en MIPS."""

    def __init__(self, rt, offset, base):
        self.rt = rt
        self.offset = offset
        self.base = base


class JumpNode(InstructionNode):
    """Nodo para instrucciones de salto en MIPS."""

    def __init__(self, target):
        self.target = target


class BranchEqualNode(InstructionNode):
    """Nodo para la instrucción 'beq' en MIPS."""

    def __init__(self, rs, rt, offset):
        self.rs = rs
        self.rt = rt
        self.offset = offset


class AddiNode(InstructionNode):
    """Nodo para la instrucción 'addi' en MIPS."""

    def __init__(self, rt, rs, immediate):
        self.rt = rt
        self.rs = rs
        self.immediate = immediate


class OriNode(InstructionNode):
    """Nodo para la instrucción 'ori' en MIPS."""

    def __init__(self, rt, rs, immediate):
        self.rt = rt
        self.rs = rs
        self.immediate = immediate


class MoveFromHiNode(InstructionNode):
    """Nodo para la instrucción 'mfhi' en MIPS."""

    def __init__(self, rd):
        self.rd = rd


class MoveFromLoNode(InstructionNode):
    """Nodo para la instrucción 'mflo' en MIPS."""

    def __init__(self, rd):
        self.rd = rd
