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


class LoadByteNode(InstructionNode):
    """Nodo para la instrucción 'lb' en MIPS."""

    def __init__(self, rt, address):
        self.rt = rt
        self.address = address


class LoadWordNode(InstructionNode):
    """Nodo para la instrucción 'lw' en MIPS."""

    def __init__(self, rt, address):
        self.rt = rt
        self.address = address


class LoadInmediateNode(InstructionNode):
    """Nodo para la instrucción 'li' en MIPS."""

    def __init__(self, rt, immediate):
        self.rt = rt
        self.immediate = immediate


class LoadAddressNode(InstructionNode):
    """Nodo para la instrucción 'la' en MIPS."""

    def __init__(self, rt, label):
        self.rt = rt
        self.label = label


class StoreWordNode(InstructionNode):
    """Nodo para la instrucción 'sw' en MIPS."""

    def __init__(self, rt, ramdir):
        self.rt = rt
        self.ramdir = ramdir


class JumpNode(InstructionNode):
    """Nodo para instrucciones de salto en MIPS."""

    def __init__(self, label: str):
        self.label = label


class JumpRegisterNode(InstructionNode):
    """Nodo para instrucciones de salto en MIPS."""

    def __init__(self, register: RegisterNode):
        self.rs = register


class JumpAndLinkNode(InstructionNode):
    """Nodo para la instrucción 'jal' en MIPS."""

    def __init__(self, label: str):
        self.label = label


class JumpRegisterAndLinkNode(InstructionNode):
    """Nodo para la instrucción 'jalr' en MIPS."""

    def __init__(self, register: RegisterNode):
        self.rs = register


class BranchEqualNode(InstructionNode):
    """Nodo para la instrucción 'beq' en MIPS."""

    def __init__(self, rs, rt, offset):
        self.rs = rs
        self.rt = rt
        self.offset = offset


class BeqzNode(InstructionNode):
    """Nodo para la instrucción 'beqz' en MIPS."""

    def __init__(self, rs, label):
        self.rs = rs
        self.label = label


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


class MoveNode(InstructionNode):
    """Nodo para la instrucción 'move' en MIPS."""

    def __init__(self, rd, rs):
        self.rd = rd
        self.rs = rs


class MemoryAddressRegisterNode(MipsAstNode):
    """Nodo para el registro de dirección de memoria."""

    def __init__(self, register, index):
        self.register = register
        self.index = index
