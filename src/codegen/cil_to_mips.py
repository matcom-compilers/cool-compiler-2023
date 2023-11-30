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
            [mips.LabelNode(f"{method.id}") for method in node.methods],
        )

    def visit__DataNode(self, node: cil.DataNode):
        pass

    def visit__FunctionNode(self, node: cil.FunctionNode, *args, **kwargs):
        instructions = []

        locals_save, params_save = self.locals, self.params
        self.locals, self.params = [], []
        self.clean_pushed_args()

        instructions.append(mips.LabelNode(node.name))

        self.memory_manager.save()
        fp_save = self.memory_manager.get_unused_register()
        instructions.append(mips.MoveNode(fp_save, FP_REG))
        instructions.append(mips.MoveNode(FP_REG, SP_REG))

        for i in range(len(node.params)):
            param = node.params[i]
            self.params.append(param.name)
            self.memory_manager.clean()

        for local in node.localvars:
            self.locals.append(local.name)

        locals_size = len(node.localvars)
        instructions.append(mips.AddiNode(SP_REG, SP_REG, locals_size * WORD_SIZE))

        instructions.append(
            mips.StoreWordNode(RA_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, WORD_SIZE))

        instructions.append(
            mips.StoreWordNode(fp_save, mips.MemoryAddressRegisterNode(SP_REG, 0))
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
            mips.LoadInmediateNode(
                V0_REG,
                9,
            )
        )
        instructions.append(
            mips.LoadInmediateNode(
                ARG_REGISTERS[0],
                reserved_bytes,
            )
        )
        instructions.append(mips.SyscallNode())

        reg1 = self.memory_manager.get_unused_register()

        if node.type != "Void":
            instructions.append(mips.LoadAddressNode(reg1, mips.LabelNode(node.type)))
            instructions.append(
                mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
            )
        else:
            instructions.append(mips.LoadInmediateNode(reg1, 0))
            instructions.append(
                mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
            )

        # Move offset of instance (type addres is in index -1)
        instructions.append(mips.AddiNode(V0_REG, V0_REG, WORD_SIZE))

        # Save instance address in destination
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
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
                )
            )
        else:
            instructions.append(
                # Return Void (value 0)
                mips.LoadInmediateNode(
                    reg1,
                    0,
                )
            )

        # remove prev $fp from stack
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE))
        instructions.append(
            mips.LoadWordNode(FP_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # remove prev $ra from stack
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE))
        instructions.append(
            mips.LoadWordNode(RA_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # Remove locals from Stack
        locals_size = len(self.locals)
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -locals_size * WORD_SIZE))

        # Save return value in Stack
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, 4))

        instructions.append(mips.JumpRegisterNode(RA_REG))

        self.memory_manager.clean()
        return instructions

    def visit__StaticCallNode(self, node: cil.StaticCallNode, *args, **kwargs):
        self.memory_manager.save()
        instructions = []

        dest_dir = self.search_mem(node.dest)

        # Jump to function and save link
        instructions.append(mips.JumpAndLinkNode(node.function))

        instructions.append(mips.AddiNode(SP_REG, SP_REG, -WORD_SIZE))
        reg1 = self.memory_manager.get_unused_register()
        # Obtain return value from stack
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        # Remove args from stack
        instructions.append(
            mips.AddiNode(
                SP_REG,
                SP_REG,
                -self.pushed_args * WORD_SIZE,
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
            )
        )

        # Push to Stack
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, WORD_SIZE))

        self.push_arg()
        self.memory_manager.clean()
        return instructions

    def visit__ExitNode(self, node: cil.ExitNode, *args, **kwargs):
        instructions = []
        instructions.append(mips.LoadInmediateNode(V0_REG, 10))  # exit syscall
        instructions.append(mips.SyscallNode())
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
            instructions.append(mips.LoadInmediateNode(reg1, node.msg))
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

        instructions.append(mips.LoadInmediateNode(V0_REG, sys_code))
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, str_dir))
        )
        instructions.append(
            mips.LoadWordNode(ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(reg1, 0))
        )
        instructions.append(mips.SyscallNode())

        self.memory_manager.clean()
        return instructions

    def visit__ReadNode(self, node: cil.ReadNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        dest_dir = self.search_mem(node.dest)

        if node.is_string:
            sys_code = 8

            instructions.append(mips.LoadInmediateNode(V0_REG, 9))
            instructions.append(
                mips.LoadInmediateNode(ARG_REGISTERS[0], READ_BUFFER_SIZE)
            )
            instructions.append(mips.SyscallNode())

            instructions.append(mips.MoveNode(ARG_REGISTERS[0], V0_REG))
            instructions.append(
                mips.LoadInmediateNode(ARG_REGISTERS[1], READ_BUFFER_SIZE + 1)
            )

            instructions.append(mips.LoadInmediateNode(V0_REG, sys_code))  # Read str
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

            instructions.append(mips.LoadInmediateNode(V0_REG, sys_code))
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

        instructions.append(mips.LoadInmediateNode(reg1, 0))

        instructions.append(mips.LabelNode(loop))
        instructions.append(
            mips.LoadByteNode(reg2, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0))
        )

        instructions.append(mips.BeqzNode(reg2, exit))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(reg1, reg1, 1))
        instructions.append(mips.JumpNode(loop))
        instructions.append(mips.LabelNode(exit))

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
