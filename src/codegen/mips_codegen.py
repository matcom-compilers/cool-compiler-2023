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

    def visit__DataNode(self, node: mips.DataNode, *args, **kwargs):
        def visit_value(value):
            return (
                str(value)
                if isinstance(value, int) or isinstance(value, str)
                else self.visit(value)
            )

        data_value = ",".join(visit_value(value) for value in node.data)
        return f"{self.visit(node.label)} {node.storage_type} {data_value}"

    def visit__LabelNode(self, node, *args, **kwargs):
        return f"{node.label}"

    def visit__LabelInstructionNode(self, node, *args, **kwargs):
        return f"{node.label}:"

    def visit__SyscallNode(self, node, *args, **kwargs):
        return "syscall"

    # Métodos para instrucciones aritméticas
    def visit__AddNode(self, node, *args, **kwargs):
        return f"add {node.rd.accept(self)}, {node.rs.accept(self)}, {node.rt.accept(self)}"

    def visit__SubNode(self, node, *args, **kwargs):
        return f"sub {node.rd.accept(self)}, {node.rs.accept(self)}, {node.rt.accept(self)}"

    # Métodos para instrucciones de carga y almacenamiento
    def visit__LoadWordNode(self, node: mips.LoadWordNode, *args, **kwargs):
        return f"lw {node.rt.accept(self)}, {node.address.accept(self)}"

    def visit__LoadAddressNode(self, node: mips.LoadAddressNode):
        return f"la {node.rt.accept(self)}, {node.label.accept(self)}"

    def visit__LoadByteNode(self, node: mips.LoadByteNode):
        return f"lb {node.rt.accept(self)}, {node.address.accept(self)}"

    # Métodos para instrucciones de salto
    def visit__JumpNode(self, node: mips.JumpNode, *args, **kwargs):
        return f"j {node.label}"

    def visit__JumpRegisterNode(self, node, *args, **kwargs):
        return f"jr {node.rs.accept(self)}"

    def visit__JumpAndLinkNode(self, node: mips.JumpAndLinkNode, *args, **kwargs):
        return f"jal {node.label}"

    def visit__JumpRegisterAndLinkNode(
        self, node: mips.JumpRegisterAndLinkNode, *args, **kwargs
    ):
        return f"jalr {node.rs.accept(self)}"

    def visit__BranchEqualNode(self, node, *args, **kwargs):
        return f"beq {node.rs}, {node.rt}, {node.offset}"

    def visit__BeqzNode(self, node: mips.BeqzNode, *args, **kwargs):
        return f"beqz {node.rs.accept(self)}, {node.label}"

    def visit__BgtzNode(self, node: mips.BgtzNode, *args, **kwargs):
        return f"beqz {node.rs.accept(self)}, {node.label}"

    def visit__MoveNode(self, node: mips.MoveNode, *args, **kwargs):
        return f"move {node.rd.accept(self)}, {node.rs.accept(self)}"

    def visit__AddiNode(self, node: mips.AddiNode, *args, **kwargs):
        return f"addi {node.rt.accept(self)}, {node.rs.accept(self)}, {node.immediate}"

    def visit__StoreWordNode(self, node: mips.StoreWordNode, *args, **kwargs):
        return f"sw {node.rt.accept(self)}, {node.ramdir.accept(self)}"

    def visit__StoreByteNode(self, node: mips.StoreByteNode, *args, **kwargs):
        return f"sb {node.rt.accept(self)}, {node.ramdir.accept(self)}"

    def visit__RegisterNode(self, node: mips.RegisterNode, *args, **kwargs):
        return f"${node.number}"

    def visit__MemoryAddressRegisterNode(
        self, node: mips.MemoryAddressRegisterNode, *args, **kwargs
    ):
        return f"{str(node.index)}({node.register.accept(self)})"

    def visit__LoadImmediateNode(self, node: mips.LoadImmediateNode, *args, **kwargs):
        return f"li {node.rt.accept(self)}, {node.immediate}"
