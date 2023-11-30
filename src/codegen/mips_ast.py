from tokenize import Comment


class MipsAstNode:
    """Nodo base para todos los nodos del AST de MIPS."""

    def accept(self, visitor, *args, **kwargs):
        """Permite a un visitor aceptar este nodo."""
        return visitor.visit(self, *args, **kwargs)


class ProgramNode(MipsAstNode):
    """Representa un programa completo en MIPS, incluyendo secciones de texto y datos."""

    def __init__(self, text_section, data_section,comment = ""):
        self.text_section = text_section
        self.data_section = data_section
        self.comment = comment


class TextNode(MipsAstNode):
    """Representa la sección de texto en un programa MIPS, contiene instrucciones."""

    def __init__(self, instructions,comment = ""):
        self.instructions = instructions
        self.comment = comment


class DataSectionNode(MipsAstNode):
    """Representa la sección de datos en un programa MIPS."""

    def __init__(self, data, comment = ""):
        self.data = data
        self.comment = comment


class DataNode(MipsAstNode):
    """Nodo para un elemento de datos en la sección de datos."""

    def __init__(self, label, storage_type, data, comment = ""):
        self.label = label
        self.storage_type = storage_type
        self.data = data
        self.comment = comment


class RegisterNode(MipsAstNode):
    def __init__(self, number, comment = ""):
        self.number = number
        self.comment = comment

class LabelNode(MipsAstNode):
    """Representa una etiqueta en MIPS."""

    def __init__(self, label,comment = ""):
        self.label = label
        self.comment = comment


class InstructionNode(MipsAstNode):
    """Nodo base para todas las instrucciones MIPS."""

    pass


class LabelInstructionNode(InstructionNode):
    """Representa una etiqueta en MIPS."""

    def __init__(self, label,comment = ""):
        self.label = label
        self.comment = comment

class SyscallNode(InstructionNode):
    """Representa la instrucción 'syscall' en MIPS."""

    pass


class AddNode(InstructionNode):
    """Nodo para la instrucción 'add' en MIPS."""

    def __init__(self, rd, rs, rt, comment = ""):
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.comment = comment


class SubNode(InstructionNode):
    """Nodo para la instrucción 'sub' en MIPS."""

    def __init__(self, rd, rs, rt,comment = ""):
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.comment = comment

class LoadByteNode(InstructionNode):
    """Nodo para la instrucción 'lb' en MIPS."""

    def __init__(self, rt, address,comment = ""):
        self.rt = rt
        self.address = address
        self.comment = comment


class LoadWordNode(InstructionNode):
    """Nodo para la instrucción 'lw' en MIPS."""

    def __init__(self, rt, address, comment = ""):
        self.rt = rt
        self.address = address
        self.comment = comment


class LoadImmediateNode(InstructionNode):
    """Nodo para la instrucción 'li' en MIPS."""

    def __init__(self, rt, immediate, comment = ""):
        self.rt = rt
        self.immediate = immediate
        self.comment = comment


class LoadAddressNode(InstructionNode):
    """Nodo para la instrucción 'la' en MIPS."""

    def __init__(self, rt, label, comment = ""):
        self.rt = rt
        self.label = label
        self.comment = comment


class StoreByteNode(InstructionNode):
    """Nodo para la instrucción 'sb' en MIPS."""

    def __init__(self, rt, ramdir, comment = ""):
        self.rt = rt
        self.ramdir = ramdir
        self.comment = comment


class StoreWordNode(InstructionNode):
    """Nodo para la instrucción 'sw' en MIPS."""

    def __init__(self, rt, ramdir, comment = ""):
        self.rt = rt
        self.ramdir = ramdir
        self.comment = comment 


class JumpNode(InstructionNode):
    """Nodo para instrucciones de salto en MIPS."""

    def __init__(self, label: str, comment = ""):
        self.label = label
        self.comment = comment


class JumpRegisterNode(InstructionNode):
    """Nodo para instrucciones de salto en MIPS."""

    def __init__(self, register: RegisterNode, comment = ""):
        self.rs = register
        self.comment = comment


class JumpAndLinkNode(InstructionNode):
    """Nodo para la instrucción 'jal' en MIPS."""

    def __init__(self, label: str,comment = ""):
        self.label = label
        self.comment = comment


class JumpRegisterAndLinkNode(InstructionNode):
    """Nodo para la instrucción 'jalr' en MIPS."""

    def __init__(self, register: RegisterNode, comment = ""):
        self.rs = register
        self.comment = comment


class BranchEqualNode(InstructionNode):
    """Nodo para la instrucción 'beq' en MIPS."""

    def __init__(self, rs, rt, offset,comment = ""):
        self.rs = rs
        self.rt = rt
        self.offset = offset
        self.comment = comment


class BeqzNode(InstructionNode):
    """Nodo para la instrucción 'beqz' en MIPS."""

    def __init__(self, rs, label,comment = ""):
        self.rs = rs
        self.label = label
        self.comment = comment


class BgtzNode(InstructionNode):
    def __init__(self, rs, label,comment = ""):
        self.rs = rs
        self.label = label
        self.comment = comment


class AddiNode(InstructionNode):
    """Nodo para la instrucción 'addi' en MIPS."""

    def __init__(self, rt, rs, immediate,comment = ""):
        self.rt = rt
        self.rs = rs
        self.immediate = immediate
        self.comment = comment


class OriNode(InstructionNode):
    """Nodo para la instrucción 'ori' en MIPS."""

    def __init__(self, rt, rs, immediate,comment = ""):
        self.rt = rt
        self.rs = rs
        self.immediate = immediate
        self.comment = comment


class MoveFromHiNode(InstructionNode):
    """Nodo para la instrucción 'mfhi' en MIPS."""

    def __init__(self, rd,comment = ""):
        self.rd = rd
        self.comment = comment


class MoveFromLoNode(InstructionNode):
    """Nodo para la instrucción 'mflo' en MIPS."""

    def __init__(self, rd,comment = ""):
        self.rd = rd
        self.comment = comment


class MoveNode(InstructionNode):
    """Nodo para la instrucción 'move' en MIPS."""

    def __init__(self, rd, rs,comment = ""):
        self.rd = rd
        self.rs = rs
        self.comment = comment


class MemoryAddressRegisterNode(MipsAstNode):
    """Nodo para el registro de dirección de memoria."""

    def __init__(self, register, index,comment = ""):
        self.register = register
        self.index = index
        self.comment = comment
