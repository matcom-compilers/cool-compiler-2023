from codegen import cil_ast as cil
from codegen import mips_ast as mips
from utils.visitor import Visitor

REGISTER_NAMES = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9"]
ARG_REGISTERS_NAMES = ["a0", "a1", "a2", "a3"]

INSTANCE_METADATA_SIZE = 4

WORD_SIZE = 4
READ_BUFFER_SIZE = 4000

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
        self.locals = []
        self.params = []
        self.memory_manager = MemoryManager()
        self.pushed_args = 0
        self.loop_count = 0
        self.exit_count = 0

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
            [mips.LabelNode(f"{method.function_id }") for method in node.methods],
        )

    def visit__DataNode(self, node: cil.DataNode):
        self.data_section[node.name] = mips.DataNode(
            mips.LabelNode(node.name), ".asciiz", [node.value]
        )

    def visit__FunctionNode(self, node: cil.FunctionNode, *args, **kwargs):
        instructions = []

        locals_save, params_save = self.locals, self.params
        self.locals, self.params = [], []
        self.clean_pushed_args()

        instructions.append(mips.LabelInstructionNode(node.name))

        self.memory_manager.save()
        fp_save = self.memory_manager.get_unused_register()
        instructions.append(mips.MoveNode(fp_save, FP_REG, comment="Save FP"))
        instructions.append(mips.MoveNode(FP_REG, SP_REG, comment="Put SP on FP"))

        for i in range(len(node.params)):
            param = node.params[i]
            self.params.append(param.name)
            self.memory_manager.clean()

        for local in node.localvars:
            self.locals.append(local.name)

        locals_size = len(node.localvars)
        instructions.append(mips.AddiNode(SP_REG, SP_REG, locals_size * WORD_SIZE, comment=f"Push {locals_size} local(s) to the Stack"))

        instructions.append(
            mips.StoreWordNode(RA_REG, mips.MemoryAddressRegisterNode(SP_REG, 0), comment="Save return Address to come back later")
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, WORD_SIZE))

        instructions.append(
            mips.StoreWordNode(fp_save, mips.MemoryAddressRegisterNode(SP_REG, 0), comment="Put save frame pointer on Stack")
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, WORD_SIZE))

        for instruction in node.instructions:
            instructions.extend(instruction.accept(self, *args, **kwargs))

        self.memory_manager.clean()
        self.locals, self.params = locals_save, params_save
        return instructions

    def visit__AllocateNode(self, node: cil.AllocateNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        if (
            node.type == "String"
            or node.type == "Int"
            or node.type == "Bool"
            or node.type == "Object"
        ):
            reserved_bytes = WORD_SIZE * 2
        elif node.type == "Void":
            reserved_bytes = WORD_SIZE
        else:
            typ = self.types[node.type]
            reserved_bytes = (len(typ.attributes) + 1) * WORD_SIZE

        instructions.append(
            mips.LoadImmediateNode(
                V0_REG,
                9,
                comment="Put 9 (sbrk) syscode on v0"
            )
        )
        instructions.append(
            mips.LoadImmediateNode(
                ARG_REGISTERS[0],
                reserved_bytes,
                comment=f"Put reserved bytes on a0. Reserving {reserved_bytes} bytes"
            )
        )
        instructions.append(mips.SyscallNode(comment=f"Allocating {node.type}"))

        reg1 = self.memory_manager.get_unused_register()

        if node.type != "Void":
            instructions.append(mips.LoadAddressNode(reg1, mips.LabelNode(node.type), comment="Save new instance address on Register"))
            instructions.append(
                mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0), "Save type address in firts position of memory allocated")
            )
        else:
            instructions.append(mips.LoadImmediateNode(reg1, 0, comment="Void type initialize on 0"))
            instructions.append(
                mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0), "Save value 0 in firts position of memory allocated")
            )

        
        instructions.append(mips.AddiNode(V0_REG, V0_REG, WORD_SIZE, comment="Move offset of instance (keep type addres at index -1)"))

        # Save instance address in destination
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir), comment="Save instance address in destination")
        )

        self.memory_manager.clean()
        return instructions

    def visit__ReturnNode(self, node: cil.ReturnNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        if node.value != "void":
            value_dir = self.search_mem(node.value)
            instructions.append(
                # Obtain return value
                mips.LoadWordNode(
                    reg1,
                    mips.MemoryAddressRegisterNode(FP_REG, value_dir),
                    f"Obtain return value",
                )
            )
        else:
            instructions.append(
                # Return Void (value 0)
                mips.LoadImmediateNode(
                    reg1,
                    0,
                    f"Void value is 0",
                )
            )

        # remove prev $fp from stack
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE, comment="remove prev $fp from stack"))
        instructions.append(
            mips.LoadWordNode(FP_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # remove prev $ra from stack
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE, comment="remove prev $ra from stack"))
        instructions.append(
            mips.LoadWordNode(RA_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # Remove locals from Stack
        locals_size = len(self.locals)
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -locals_size * WORD_SIZE, comment="remove locals from stack"))

        # Save return value in Stack
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0), comment="Put return value in stack")
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, 4))

        instructions.append(mips.JumpRegisterNode(RA_REG, comment="return"))

        self.memory_manager.clean()
        return instructions

    def visit__StaticCallNode(self, node: cil.StaticCallNode, *args, **kwargs):
        self.memory_manager.save()
        instructions = []

        dest_dir = self.search_mem(node.dest)

        # Jump to function and save link
        instructions.append(mips.JumpAndLinkNode(node.function, comment=f"CALL {node.function}") )

        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE))
        reg1 = self.memory_manager.get_unused_register()
        # Obtain return value from stack
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0), comment="Obtein return value from Stack")
        )
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir), comment="Store return Value on Frame")
        )

        # Remove args from stack
        instructions.append(
            mips.AddiNode(
                SP_REG,
                SP_REG,
                -self.pushed_args * WORD_SIZE,
                comment=f"Remove {self.pushed_args} args from stack"
            )
        )
        self.clean_pushed_args()

        self.memory_manager.clean()
        return instructions

    def visit__ArgNode(self, node: cil.ArgNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        # Obtain value of Arg
        local_dir = self.search_mem(node.name)
        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(FP_REG, local_dir),
                f"Obtain value of Arg at {local_dir}({FP_REG})",
            )
        )

        # Push to Stack
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0), comment="Push to stack")
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, WORD_SIZE))

        self.push_arg()
        self.memory_manager.clean()
        return instructions

    def visit__ExitNode(self, node: cil.ExitNode, *args, **kwargs):
        instructions = []
        instructions.append(mips.LoadImmediateNode(V0_REG, 10, comment="Store syscall for exit"))  # exit syscall
        instructions.append(mips.SyscallNode(comment="Exit"))
        return instructions

    # Aquí agregarías métodos visit__ específicos para cada tipo de instrucción
    # Por ejemplo:
    def visit__TypeOfNode(self, node: cil.TypeOfNode, *args, **kwargs):
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions = []

        obj_dir = self.search_mem(node.obj)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, obj_dir))
        )

        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(reg1, -WORD_SIZE))
        )

        # Save type value in destination
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
            )
        )

        self.memory_manager.clean()
        return instructions

    def visit__DynamicCallNode(self, node: cil.DynamicCallNode, *args, **kwargs):
        instructions = []

        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        dest_dir = self.search_mem(node.dest)

        # get type dir for Dynamic Call
        local_dir = self.search_mem(node.type)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, local_dir))
        )

        # Get method of index
        instructions.append(
            mips.LoadWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(reg1, node.method * WORD_SIZE),
            )
        )

        # Jump to function
        instructions.append(mips.JumpRegisterAndLinkNode(reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE))
        # Obtain return value from stack
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # Save return value in destination
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )
        # Remove Args from Stack
        instructions.append(
            mips.AddiNode(SP_REG, SP_REG, -self.pushed_args * WORD_SIZE)
        )
        self.clean_pushed_args()

        self.memory_manager.clean()
        return instructions

    def visit__LoadNode(self, node: cil.LoadNode, *args, **kwargs):
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        instructions = []

        if isinstance(node.msg, int):
            
            instructions.append(mips.LoadImmediateNode(reg1, node.msg))
        else:
            
            instructions.append(mips.LoadAddressNode(reg1, mips.LabelNode(node.msg)))

        dest_dir = self.search_mem(node.dest)
        # Save loaded value in destination
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def visit__PrintNode(self, node: cil.PrintNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        str_dir = self.search_mem(node.str_addr)

        if node.is_string:
            sys_code = 4
        else:
            sys_code = 1

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions.append(mips.LoadImmediateNode(V0_REG, sys_code, comment="Load Code for Print"))
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, str_dir), comment="Load value to PRINT")
        )
        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(reg1, 0), comment="For DEBUG")
        )
        
        instructions.append(
            mips.LoadWordNode(ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(reg1, 0), comment="Put value on arg reg")
        )
        instructions.append(mips.SyscallNode(comment="PRINT"))

        self.memory_manager.clean()
        return instructions

    def visit__ReadNode(self, node: cil.ReadNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        dest_dir = self.search_mem(node.dest)

        if node.is_string:
            sys_code = 8

            instructions.append(mips.LoadImmediateNode(V0_REG, 9))
            instructions.append(
                mips.LoadImmediateNode(ARG_REGISTERS[0], READ_BUFFER_SIZE)
            )
            instructions.append(mips.SyscallNode())

            instructions.append(mips.MoveNode(ARG_REGISTERS[0], V0_REG))
            instructions.append(
                mips.LoadImmediateNode(ARG_REGISTERS[1], READ_BUFFER_SIZE + 1)
            )

            instructions.append(mips.LoadImmediateNode(V0_REG, sys_code))  # Read str
            instructions.append(mips.SyscallNode())

            # Save readed value
            instructions.append(
                mips.StoreWordNode(
                    ARG_REGISTERS[0],
                    mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
                )
            )

        else:
            sys_code = 5

            instructions.append(mips.LoadImmediateNode(V0_REG, sys_code))
            instructions.append(mips.SyscallNode())
            instructions.append(
                mips.StoreWordNode(
                    V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )

        self.memory_manager.clean()
        return instructions

    def visit__LengthNode(self, node: cil.LengthNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        loop = f"loop_{self.get_loop_count()}"
        exit = f"exit_{self.get_exit_count()}"

        string_dir = self.search_mem(node.string)
        instructions.append(
            mips.LoadWordNode(
                ARG_REGISTERS[0],
                mips.MemoryAddressRegisterNode(FP_REG, string_dir),
            )
        )

        instructions.append(mips.LoadImmediateNode(reg1, 0))

        instructions.append(mips.LabelInstructionNode(loop))
        instructions.append(
            mips.LoadByteNode(reg2, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0))
        )

        instructions.append(mips.BeqzNode(reg2, exit))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(reg1, reg1, 1))
        instructions.append(mips.JumpNode(loop))
        instructions.append(mips.LabelInstructionNode(exit))

        dest_dir = self.search_mem(node.dest)
        # Save Calculated Length
        instructions.append(
            mips.StoreWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
            )
        )

        self.memory_manager.clean()
        return instructions

    def visit__MinusNode(self, node: cil.MinusNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()

        right_dir = self.search_mem(node.right)
        left_dir = self.search_mem(node.left)

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, right_dir))
        )
        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, left_dir))
        )

        instructions.append(mips.SubNode(reg3, reg2, reg1))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg3, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def visit__PlusNode(self, node: cil.PlusNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()

        right_dir = self.search_mem(node.right)
        left_dir = self.search_mem(node.left)

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, right_dir))
        )
        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, left_dir))
        )

        instructions.append(mips.AddNode(reg3, reg1, reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                reg3,
                mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
            )
        )

        self.memory_manager.clean()
        return instructions

    def visit__ConcatNode(self, node: cil.ConcatNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        loop1 = f"LOOP_{self.get_loop_count()}"
        exit1 = f"EXIT_{self.get_exit_count()}"
        loop2 = f"LOOP_{self.get_loop_count()}"
        exit2 = f"EXIT_{self.get_exit_count()}"

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        lenght_dir = self.search_mem(node.dest_lenght)

        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(FP_REG, lenght_dir),
            )
        )

        # Reserve space for concatenated string
        instructions.append(mips.AddiNode(reg1, reg1, 1))
        instructions.append(mips.LoadImmediateNode(V0_REG, 9))
        instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg1))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.LoadAddressNode(reg2, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        string1_dir = self.search_mem(node.string1)
        instructions.append(
            mips.LoadWordNode(
                ARG_REGISTERS[1], mips.MemoryAddressRegisterNode(FP_REG, string1_dir)
            )
        )
        string2_dir = self.search_mem(node.string2)
        instructions.append(
            mips.LoadWordNode(
                ARG_REGISTERS[2], mips.MemoryAddressRegisterNode(FP_REG, string2_dir)
            )
        )

        instructions.append(mips.LabelInstructionNode(loop1))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[1], 0))
        )

        instructions.append(mips.BeqzNode(reg1, exit1))
        instructions.append(
            mips.StoreByteNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        instructions.append(mips.AddiNode(V0_REG, V0_REG, 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[1], ARG_REGISTERS[1], 1))
        instructions.append(mips.JumpNode(loop1))
        instructions.append(mips.LabelInstructionNode(exit1))

        instructions.append(mips.LabelInstructionNode(loop2))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[2], 0))
        )
        instructions.append(
            mips.StoreByteNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )
        instructions.append(mips.BeqzNode(reg1, exit2))
        instructions.append(mips.AddiNode(V0_REG, V0_REG, 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[2], ARG_REGISTERS[2], 1))
        instructions.append(mips.JumpNode(loop2))
        instructions.append(mips.LabelInstructionNode(exit2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def visit__SubstringNode(self, node: cil.SubstringNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        loop = f"LOOP_{self.get_loop_count()}"
        exit = f"EXIT_{self.get_exit_count()}"

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()
        reg4 = self.memory_manager.get_unused_register()
        reg5 = self.memory_manager.get_unused_register()

        lenght_dir = self.search_mem(node.n)
        instructions.append(
            mips.LoadWordNode(reg3, mips.MemoryAddressRegisterNode(FP_REG, lenght_dir))
        )

        instructions.append(mips.MoveNode(reg5, reg3))
        instructions.append(mips.AddiNode(reg5, reg5, 1))

        instructions.append(mips.LoadImmediateNode(V0_REG, 9))
        instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg5))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.LoadAddressNode(reg2, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        dir_index = self.search_mem(node.index)
        instructions.append(
            mips.LoadWordNode(reg4, mips.MemoryAddressRegisterNode(FP_REG, dir_index))
        )

        string_dir = self.search_mem(node.string)
        instructions.append(
            mips.LoadWordNode(
                ARG_REGISTERS[1], mips.MemoryAddressRegisterNode(FP_REG, string_dir)
            )
        )
        instructions.append(mips.AddNode(ARG_REGISTERS[1], ARG_REGISTERS[1], reg4))

        instructions.append(mips.LabelInstructionNode(loop))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[1], 0))
        )
        instructions.append(mips.BeqzNode(reg3, exit))
        instructions.append(
            mips.StoreByteNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        instructions.append(mips.AddiNode(V0_REG, V0_REG, 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[1], ARG_REGISTERS[1], 1))
        instructions.append(mips.AddiNode(reg3, reg3, -1))
        instructions.append(mips.JumpNode(loop))
        instructions.append(mips.LabelInstructionNode(exit))

        instructions.append(mips.LoadImmediateNode(reg1, 0))
        instructions.append(
            mips.StoreByteNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def visit__SetAttrNode(self, node: cil.SetAttrNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        source_dir = self.search_mem(node.source)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, source_dir), comment="Obtein value from src")
        )
        instance_dir = self.search_mem(node.instance)
        instructions.append(
            mips.LoadWordNode(
                reg2, mips.MemoryAddressRegisterNode(FP_REG, instance_dir), comment="Address of instance's attribute to set"
            )
        )
        instructions.append(
            mips.StoreWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(reg2, node.attr * WORD_SIZE),
                comment=f"Set attribute in index {node.attr}",
            )
        )

        self.memory_manager.clean()
        return instructions
    
    def visit__GetAttrNode(self, node: cil.GetAttrNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instance_dir = self.search_mem(node.instance)
        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(FP_REG, instance_dir),
                f"Dir of instance of attribute to get",
            )
        )
        instructions.append(
            mips.LoadWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(reg1, node.attr * WORD_SIZE),
                f"Load attribute in index {node.attr}",
            )
        )
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
                f"Save obtained attribute in destination",
            )
        )

        self.memory_manager.clean()
        return instructions


    def visit__GotoNode(self, node: cil.GotoNode, *args, **kwargs):
        return [mips.JumpNode(node.label)]

    def visit__GotoIfGtNode(self, node: cil.GotoIfGtNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        cond_dir = self.search_mem(node.cond)
        reg1 = self.memory_manager.get_unused_register()

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, cond_dir))
        )
        instructions.append(mips.BgtzNode(reg1, node.label))

        self.memory_manager.clean()
        return instructions

    def visit__GotoIfEqNode(self, node: cil.GotoIfEqNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        cond_dir = self.search_mem(node.cond)
        reg1 = self.memory_manager.get_unused_register()

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, cond_dir))
        )
        instructions.append(mips.BeqzNode(reg1, node.label))

        self.memory_manager.clean()
        return instructions

    def visit__LabelNode(self, node: cil.LabelNode, *args, **kwargs):
        return [mips.LabelInstructionNode(node.name)]

    def visit__AssignNode(self, node: cil.AssignNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        source_dir = self.search_mem(node.source)
        dest_dir = self.search_mem(node.dest)

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, source_dir))
        )
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def clean_pushed_args(self):
        self.pushed_args = 0

    def push_arg(self):
        self.pushed_args += 1

    def search_mem(self, id: str):
        try:
            index = self.locals.index(id)
            return index * WORD_SIZE
        except ValueError:
            index = self.params.index(id)

            return (index - len(self.params)) * WORD_SIZE

    def get_loop_count(self):
        self.loop_count += 1
        return self.loop_count

    def get_exit_count(self):
        self.exit_count += 1
        return self.exit_count
