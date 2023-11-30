from codegen import mips_ast as mips
from utils.visitor import Visitor


class MipsCodeGenerator(Visitor):
    def visit__ProgramNode(self, node: mips.ProgramNode, *args, **kwargs):
        text_code = "\n".join(self.visit(n) for n in node.text_section.instructions)
        data_code = "\n".join(self.visit(n) for n in node.data_section.data.values())
        return f".data\n{data_code}\n.text\n{text_code}"

    def visit__TextNode(self, node, *args, **kwargs):
        return "\n".join(self.visit(instr) for instr in node.instructions)

    def visit__DataSectionNode(self, node, *args, **kwargs):
        return "\n".join(self.visit(data) for data in node.data)

    def visit__DataNode(self, node, *args, **kwargs):
        return f"{node.label.label}: {node.storage_type} " + " ".join(
            n.label for n in node.data
        )

    def visit__LabelNode(self, node, *args, **kwargs):
        return f"{node.label}:"

    def visit__SyscallNode(self, node, *args, **kwargs):
        return "syscall"

    # Métodos para instrucciones aritméticas
    def visit__AddNode(self, node, *args, **kwargs):
        return f"add {node.rd}, {node.rs}, {node.rt}"

    def visit__SubNode(self, node, *args, **kwargs):
        return f"sub {node.rd}, {node.rs}, {node.rt}"

    # Métodos para instrucciones de carga y almacenamiento
    def visit__LoadWordNode(self, node, *args, **kwargs):
        return f"lw {node.rt}, {node.offset}({node.base})"

    def visit__StoreWordNode(self, node, *args, **kwargs):
        return f"sw {node.rt}, {node.offset}({node.base})"

    # Métodos para instrucciones de salto
    def visit__JumpNode(self, node, *args, **kwargs):
        return f"j {node.target}"

    def visit__BranchEqualNode(self, node, *args, **kwargs):
        return f"beq {node.rs}, {node.rt}, {node.offset}"

    # Y así sucesivamente para otros tipos de nodos...
