from codegen import mips_ast as mips
from utils.visitor import Visitor


class MipsCodeGenerator(Visitor):
    def visit__ProgramNode(self, node: mips.ProgramNode, *args, **kwargs):
        text_section = "\t.text\n\t.globl main\n\t" + node.text_section.accept(self)
        data_section = "\t.data\n" + node.data_section.accept(self)
        return f"{data_section}\n\n{text_section}\n"

    def visit__TextNode(self, node, *args, **kwargs):
        return "\n\t".join(self.visit(instr) for instr in node.instructions)

    def visit__DataSectionNode(self, node: mips.DataSectionNode, *args, **kwargs):
        return "\n".join(self.visit(data) for data in node.data.values())

    def visit__DataNode(self, node: mips.DataNode, *args, **kwargs):
        def visit_value(value):
            return (
                f"{value}"
                if isinstance(value, int) or isinstance(value, str)
                else self.visit(value)
            )

        data_value = ",".join(visit_value(value) for value in node.data)
        return f"{self.visit(node.label)}: {node.storage_type} {data_value}"

    def visit__LabelNode(self, node, *args, **kwargs):
        return f"{node.label}"

    def visit__LabelInstructionNode(self, node, *args, **kwargs):
        return f"\r{node.label}:" + "\t# " + node.comment

    def visit__SyscallNode(self, node, *args, **kwargs):
        return "syscall" + "\t# " + node.comment

    # Métodos para instrucciones aritméticas
    def visit__AddNode(self, node, *args, **kwargs):
        return (
            f"add {node.rd.accept(self)}, {node.rs.accept(self)}, {node.rt.accept(self)}"
            + "\t# "
            + node.comment
        )

    def visit__SubNode(self, node, *args, **kwargs):
        return (
            f"sub {node.rd.accept(self)}, {node.rs.accept(self)}, {node.rt.accept(self)}"
            + "\t# "
            + node.comment
        )

    # Métodos para instrucciones de carga y almacenamiento
    def visit__LoadWordNode(self, node: mips.LoadWordNode, *args, **kwargs):
        return (
            f"lw {node.rt.accept(self)}, {node.address.accept(self)}"
            + "\t# "
            + node.comment
        )

    def visit__LoadAddressNode(self, node: mips.LoadAddressNode):
        return (
            f"la {node.rt.accept(self)}, {node.label.accept(self)}"
            + "\t# "
            + node.comment
        )

    def visit__LoadByteNode(self, node: mips.LoadByteNode):
        return (
            f"lb {node.rt.accept(self)}, {node.address.accept(self)}"
            + "\t# "
            + node.comment
        )

    # Métodos para instrucciones de salto
    def visit__JumpNode(self, node: mips.JumpNode, *args, **kwargs):
        return f"j {node.label}" + "\t# " + node.comment

    def visit__JumpRegisterNode(self, node, *args, **kwargs):
        return f"jr {node.rs.accept(self)}" + "\t# " + node.comment

    def visit__JumpAndLinkNode(self, node: mips.JumpAndLinkNode, *args, **kwargs):
        return f"jal {node.label}" + "\t# " + node.comment

    def visit__JumpRegisterAndLinkNode(
        self, node: mips.JumpRegisterAndLinkNode, *args, **kwargs
    ):
        return f"jalr {node.rs.accept(self)}" + "\t# " + node.comment

    def visit__BranchEqualNode(self, node, *args, **kwargs):
        return f"beq {node.rs}, {node.rt}, {node.offset}" + "\t# " + node.comment

    def visit__BeqzNode(self, node: mips.BeqzNode, *args, **kwargs):
        return f"beqz {node.rs.accept(self)}, {node.label}" + "\t# " + node.comment

    def visit__BgtzNode(self, node: mips.BgtzNode, *args, **kwargs):
        return f"beqz {node.rs.accept(self)}, {node.label}" + "\t# " + node.comment

    def visit__MoveNode(self, node: mips.MoveNode, *args, **kwargs):
        return (
            f"move {node.rd.accept(self)}, {node.rs.accept(self)}"
            + "\t# "
            + node.comment
        )

    def visit__AddiNode(self, node: mips.AddiNode, *args, **kwargs):
        return (
            f"addi {node.rt.accept(self)}, {node.rs.accept(self)}, {node.immediate}"
            + "\t# "
            + node.comment
        )

    def visit__StoreWordNode(self, node: mips.StoreWordNode, *args, **kwargs):
        return (
            f"sw {node.rt.accept(self)}, {node.ramdir.accept(self)}"
            + "\t# "
            + node.comment
        )

    def visit__StoreByteNode(self, node: mips.StoreByteNode, *args, **kwargs):
        return (
            f"sb {node.rt.accept(self)}, {node.ramdir.accept(self)}"
            + "\t# "
            + node.comment
        )

    def visit__RegisterNode(self, node: mips.RegisterNode, *args, **kwargs):
        return f"${node.number}"

    def visit__MemoryAddressRegisterNode(
        self, node: mips.MemoryAddressRegisterNode, *args, **kwargs
    ):
        return f"{str(node.index)}({node.register.accept(self)})"

    def visit__MemoryAddressLabelNode(
        self, node: mips.MemoryAddressLabelNode, *args, **kwargs
    ):
        return node.address.accept(self)

    def visit__LoadImmediateNode(self, node: mips.LoadImmediateNode, *args, **kwargs):
        return f"li {node.rt.accept(self)}, {node.immediate}" + "\t# " + node.comment

    def visit__SetEqNode(self, node: mips.SetEqNode, *args, **kwargs):
        return f"seq {node.destination.accept(self)}, {node.m1.accept(self)}, {node.m2.accept(self)}"

    def visit__MipsAstNode(self, node: mips.MipsAstNode, *args, **kwargs):
        return f"# {node.comment}"

    def visit__BneqzNode(self, node: mips.BneqzNode, *args, **kwargs):
        return f"bnez {node.rs.accept(self)}, {node.label}" + "\t# " + node.comment
