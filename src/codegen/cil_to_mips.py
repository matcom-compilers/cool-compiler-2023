from codegen import cil_ast as cil
from codegen import mips_ast as mips
from utils.visitor import Visitor

REGISTER_NAMES = [
    "t0",
    "t1",
    "t2",
    "t3",
    "t4",
    "t5",
    "t6",
    "t7",
    "t8",
    "t9",
]
ARG_REGISTERS_NAMES = ["a0", "a1", "a2", "a3"]

# Register used for builtin proc
S0_REG = mips.RegisterNode("s0")
S1_REG = mips.RegisterNode("s1")
S2_REG = mips.RegisterNode("s2")
S3_REG = mips.RegisterNode("s3")
S4_REG = mips.RegisterNode("s4")

INSTANCE_METADATA_SIZE = 4

WORD_SIZE = 4
READ_BUFFER_SIZE = 4000

REGISTERS = [mips.RegisterNode(name) for name in REGISTER_NAMES]
ARG_REGISTERS = [mips.RegisterNode(name) for name in ARG_REGISTERS_NAMES]
A0_REG = ARG_REGISTERS[0]
A1_REG = ARG_REGISTERS[1]
FP_REG = mips.RegisterNode("fp")
SP_REG = mips.RegisterNode("sp")
RA_REG = mips.RegisterNode("ra")
V0_REG = mips.RegisterNode("v0")
V1_REG = mips.RegisterNode("v1")
ZERO = mips.RegisterNode("zero")

SYSCALL_SBRK = 9
SYSCALL_PRINT_STRING = 4
SYSCALL_PRINT_INT = 1

# Type info is stored at index 0
TYPEINFO_ATTR_INDEX = 0

####################
# String Constants #
####################
STRING_TYPE = "String"
STRING_SIZE = 12  # tipo lenght ref
# str attributes offsets
LENGTH_ATTR_INDEX = 4
CHARS_ATTR_INDEX = 8
EMPTY_STR_VALUE = '""'

# VOID Type
VOID = "Void"


COPY_BYTES = "__COPY_BYTES_PROC"


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
        self.attr_indexes = {}
        self.main_size = 0

    def visit__ProgramNode(self, node: cil.ProgramNode, *args, **kwargs):
        text_section = []

        for ty in node.dottypes:
            _ = ty.accept(self, *args, **kwargs)
            self.generate_attr_indexes(ty.name)

        self.data_section[VOID] = mips.DataNode(mips.LabelNode(VOID), ".word", ["-1"])
        self.data_section["EMPTY_STRING"] = mips.DataNode(
            mips.LabelNode("EMPTY_STRING"), ".asciiz", [EMPTY_STR_VALUE]
        )
        self.data_section["INPUT_STR_BUFFER"] = mips.DataNode(
            mips.LabelNode("INPUT_STR_BUFFER"),
            ".space",
            [mips.LabelNode(READ_BUFFER_SIZE)],
        )

        for data in node.dotdata:
            _ = data.accept(self, *args, **kwargs)

        text_section.extend(self.register_copy_bytes())

        for function in node.dotcode:
            instructions = function.accept(self, *args, **kwargs)
            text_section.extend(instructions)

        return mips.ProgramNode(
            mips.TextNode(text_section), mips.DataSectionNode(self.data_section)
        )

    def visit__TypeNode(self, node: cil.TypeNode, *args, **kwargs):
        self.types[node.name] = node

        if node.name == "Main":
            self.main_size = (len(node.attributes) + 1) * WORD_SIZE

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

        instructions.append(mips.MoveNode(FP_REG, SP_REG, comment="New Frame"))

        # Reserve space for locals
        locals_size = len(node.localvars)
        instructions.append(
            mips.AddiNode(
                SP_REG,
                SP_REG,
                locals_size * WORD_SIZE,
                comment=f"Push {locals_size} local(s) to the Stack",
            )
        )

        # Save return address
        instructions.extend(self.push_register(RA_REG))

        # Save  fp_save
        instructions.extend(self.push_register(fp_save))

        self.memory_manager.clean()  # Everything is on the stack, free registers

        for local in node.localvars:
            self.locals.append(local.name)

        for param in node.params:
            self.params.append(param.name)

        for instruction in node.instructions:
            instructions.extend(instruction.accept(self, *args, **kwargs))

        self.memory_manager.clean()
        self.locals, self.params = locals_save, params_save
        return instructions

    def visit__AllocateNode(self, node: cil.AllocateNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reserved_bytes = (len(self.types[node.type].attributes) + 1) * WORD_SIZE

        instructions.append(
            mips.LoadImmediateNode(
                V0_REG, SYSCALL_SBRK, comment="Put 9 (sbrk) syscode on v0"
            )
        )
        instructions.append(
            mips.LoadImmediateNode(
                ARG_REGISTERS[0],
                reserved_bytes,
                comment=f"Put reserved bytes on a0. Reserving {reserved_bytes} bytes",
            )
        )
        instructions.append(mips.SyscallNode(comment=f"Allocating {node.type}"))

        # Save instance address in destination
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                V0_REG,
                mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
                comment="Save instance address in destination",
            )
        )

        # Save instance type
        reg = self.memory_manager.get_unused_register()
        instructions.append(mips.LoadAddressNode(reg, mips.LabelNode(node.type)))
        instructions.append(
            mips.StoreWordNode(
                reg, mips.MemoryAddressRegisterNode(V0_REG, TYPEINFO_ATTR_INDEX)
            )
        )

        self.memory_manager.clean()
        return instructions

    # Asumme All Returned values will be on Register $a1
    def visit__ReturnNode(self, node: cil.ReturnNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()
        if isinstance(node.value, int):
            instructions.append(
                mips.LoadImmediateNode(
                    A1_REG, node.value, comment="Return Immediate Value"
                )
            )
        else:
            ret_dir = self.search_mem(node.value)
            instructions.append(
                mips.LoadWordNode(
                    A1_REG, mips.MemoryAddressRegisterNode(FP_REG, ret_dir)
                )
            )

        # remove prev $fp from stack
        instructions.append(
            mips.AddiNode(
                SP_REG, SP_REG, -WORD_SIZE, comment="remove prev $fp from stack"
            )
        )
        instructions.append(
            mips.LoadWordNode(FP_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # remove prev $ra from stack
        instructions.append(
            mips.AddiNode(
                SP_REG, SP_REG, -WORD_SIZE, comment="remove prev $ra from stack"
            )
        )
        instructions.append(
            mips.LoadWordNode(RA_REG, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        # Remove locals from Stack
        locals_size = len(self.locals)
        instructions.append(
            mips.AddiNode(
                SP_REG,
                SP_REG,
                -locals_size * WORD_SIZE,
                comment="remove locals from stack",
            )
        )

        instructions.append(mips.JumpRegisterAndLinkNode(RA_REG, comment="return"))

        self.memory_manager.clean()
        return instructions

    # Ok
    def visit__StaticCallNode(self, node: cil.StaticCallNode, *args, **kwargs):
        self.memory_manager.save()
        instructions = []

        # Jump to function and save link
        instructions.append(
            mips.JumpAndLinkNode(node.function, comment=f"CALL {node.function}")
        )

        # Obtain return value
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                A1_REG,
                mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
                comment="Store return Value on Frame from $a1",
            )
        )

        # Remove args from stack
        instructions.append(
            mips.AddiNode(
                SP_REG,
                SP_REG,
                -self.pushed_args * WORD_SIZE,
                comment=f"Remove {self.pushed_args} args from stack",
            )
        )
        self.clean_pushed_args()

        self.memory_manager.clean()
        return instructions

    # Ok
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
                f"Obtain Arg {node.name}",
            )
        )

        # Push to Stack
        push = self.push_register(reg1)
        instructions.extend(push)
        self.push_arg()

        self.memory_manager.clean()
        return instructions

    def visit__ExitNode(self, node: cil.ExitNode, *args, **kwargs):
        instructions = []
        instructions.append(
            mips.LoadImmediateNode(V0_REG, 10, comment="Store syscall for exit")
        )  # exit syscall
        instructions.append(mips.SyscallNode(comment="Exit"))
        return instructions

    # Aquí agregarías métodos visit__ específicos para cada tipo de instrucción
    # Por ejemplo:
    def visit__TypeOfNode(self, node: cil.TypeOfNode, *args, **kwargs):
        self.memory_manager.save()
        instructions = []

        if node.flag:  # Object type is on node
            reg1 = self.memory_manager.get_unused_register()
            instructions.append(
                mips.LoadAddressNode(
                    reg1, mips.LabelNode(node.type), comment=f"Address of {node.type}"
                )
            )
            dest_dir = self.search_mem(node.dest)
            instructions.append(
                mips.StoreWordNode(
                    reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )
        else:
            reg1 = self.memory_manager.get_unused_register()
            instance_dir = self.search_mem(node.obj)
            dest_dir = self.search_mem(node.dest)
            # Load address of instance
            instructions.append(
                mips.LoadWordNode(
                    reg1, mips.MemoryAddressRegisterNode(FP_REG, instance_dir)
                )
            )
            # Load address of type in instance
            instructions.append(
                mips.LoadWordNode(
                    reg1, mips.MemoryAddressRegisterNode(reg1, TYPEINFO_ATTR_INDEX)
                )
            )
            # Store type address in destination
            instructions.append(
                mips.StoreWordNode(
                    reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )

        self.memory_manager.clean()
        return instructions

    # Ok
    def visit__DynamicCallNode(self, node: cil.DynamicCallNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()

        # get type dir for Dynamic Call
        instance_dir = self.search_mem(node.type)

        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(FP_REG, instance_dir),
                comment=f"VCALL {node.type} {node.method} {node.dest}",
            )
        )

        # Get method of index
        reg2 = self.memory_manager.get_unused_register()
        instructions.append(
            mips.LoadWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(reg1, node.method * WORD_SIZE),
            )
        )
        mips.MoveNode(reg1, reg2)

        # Jump to function
        instructions.append(mips.JumpRegisterAndLinkNode(reg2))

        # Put return value on destination
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(A1_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )
        # Remove Args from Stack
        instructions.append(
            mips.AddiNode(SP_REG, SP_REG, -self.pushed_args * WORD_SIZE)
        )
        self.clean_pushed_args()

        self.memory_manager.clean()
        return instructions

    def visit__LoadNode(self, node: cil.LoadNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        _size = STRING_SIZE

        # Allocate String
        instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
        instructions.append(mips.LoadImmediateNode(ARG_REGISTERS[0], _size))
        instructions.append(mips.SyscallNode())

        # Point dest to allocated string
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        reg1 = self.memory_manager.get_unused_register()
        # Load String Type
        instructions.append(mips.LoadAddressNode(reg1, mips.LabelNode(STRING_TYPE)))

        # Copy String Type address to allocated instance
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        # Store String Length
        instructions.append(mips.LoadImmediateNode(reg1, len(node.data)))
        instructions.append(
            mips.StoreWordNode(
                reg1, mips.MemoryAddressRegisterNode(V0_REG, LENGTH_ATTR_INDEX)
            )
        )

        # Store str ref
        instructions.append(mips.LoadAddressNode(reg1, mips.LabelNode(node.label)))
        instructions.append(
            mips.StoreWordNode(
                reg1, mips.MemoryAddressRegisterNode(V0_REG, CHARS_ATTR_INDEX)
            )
        )

        self.memory_manager.clean()
        return instructions

    def visit___ParamNode(self, param: cil.ParamNode, *args, **kwargs):
        instructions = []
        return instructions

    # Ok
    def visit__PrintNode(self, node: cil.PrintNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        if node.is_string:
            sys_code = SYSCALL_PRINT_STRING
            str_dir = self.search_mem(node.str_addr)
            instructions.append(
                mips.LoadWordNode(
                    A0_REG, mips.MemoryAddressRegisterNode(FP_REG, str_dir)
                )
            )
            instructions.append(
                mips.LoadWordNode(
                    A0_REG, mips.MemoryAddressRegisterNode(A0_REG, CHARS_ATTR_INDEX)
                )
            )

        else:
            sys_code = SYSCALL_PRINT_INT
            if isinstance(node.str_addr, int):
                instructions.append(
                    mips.LoadImmediateNode(
                        A0_REG, node.str_addr, comment="Load Unboxed int"
                    )
                )
            else:  # Int in Memory
                int_index = self.search_mem(node.str_addr)
                instructions.append(
                    mips.LoadWordNode(
                        A0_REG, mips.MemoryAddressRegisterNode(FP_REG, int_index)
                    )
                )
        instructions.append(mips.LoadImmediateNode(V0_REG, sys_code))
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
        source_dir = self.search_mem(node.string)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, source_dir))
        )
        instructions.append(
            mips.LoadWordNode(
                reg1, mips.MemoryAddressRegisterNode(reg1, LENGTH_ATTR_INDEX)
            )
        )
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
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
        left_index = self.search_mem(node.string1)
        right_index = self.search_mem(node.string2)

        r1 = self.memory_manager.get_unused_register()
        r2 = self.memory_manager.get_unused_register()

        # load lenghts
        instructions.append(
            mips.LoadWordNode(r1, mips.MemoryAddressRegisterNode(FP_REG, left_index))
        )
        instructions.append(
            mips.LoadWordNode(r1, mips.MemoryAddressRegisterNode(r1, LENGTH_ATTR_INDEX))
        )
        instructions.append(
            mips.LoadWordNode(r2, mips.MemoryAddressRegisterNode(FP_REG, right_index))
        )
        instructions.append(
            mips.LoadWordNode(r2, mips.MemoryAddressRegisterNode(r2, LENGTH_ATTR_INDEX))
        )

        r3 = self.memory_manager.get_unused_register()  # sum of lengths
        instructions.append(mips.AddNode(r3, r1, r2))

        # create buffer
        instructions.append(mips.MoveNode(A0_REG, r3))  # $a0 = length
        instructions.append(mips.AddiNode(A0_REG, A0_REG, 1))  # $a0 = length + 1
        instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
        instructions.append(mips.SyscallNode())  # Reserve space for String

        r4 = self.memory_manager.get_unused_register()
        instructions.append(mips.MoveNode(r4, V0_REG))  # saving the dest char arr

        instructions.append(mips.MoveNode(S0_REG, r4))

        instructions.append(
            mips.LoadWordNode(
                S1_REG, mips.MemoryAddressRegisterNode(FP_REG, left_index)
            )
        )
        instructions.append(
            mips.LoadWordNode(
                S1_REG, mips.MemoryAddressRegisterNode(S1_REG, CHARS_ATTR_INDEX)
            )
        )
        instructions.append(mips.MoveNode(A0_REG, r1))
        instructions.append(mips.JumpAndLinkNode(COPY_BYTES))

        instructions.append(
            mips.LoadWordNode(
                S1_REG, mips.MemoryAddressRegisterNode(FP_REG, right_index)
            )
        )
        instructions.append(
            mips.LoadWordNode(
                S1_REG, mips.MemoryAddressRegisterNode(S1_REG, CHARS_ATTR_INDEX)
            )
        )
        instructions.append(mips.MoveNode(A0_REG, r2))
        instructions.append(mips.JumpAndLinkNode(COPY_BYTES))

        instructions.append(
            mips.StoreByteNode(ZERO, mips.MemoryAddressRegisterNode(S0_REG, 0))
        )
        # r4 start of bytes
        # r3 length

        dest_offset = self.search_mem(node.dest)
        _size = STRING_SIZE
        instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
        instructions.append(mips.LoadImmediateNode(A0_REG, _size))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.StoreWordNode(
                V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_offset)
            )
        )
        r5 = self.memory_manager.get_unused_register()
        instructions.append(mips.LoadAddressNode(r5, mips.LabelNode(STRING_TYPE)))
        instructions.append(
            mips.StoreWordNode(r5, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        # storing string length

        instructions.append(
            mips.StoreWordNode(
                r3, mips.MemoryAddressRegisterNode(V0_REG, LENGTH_ATTR_INDEX)
            )
        )
        # storing string chars ref
        instructions.append(
            mips.StoreWordNode(
                r4, mips.MemoryAddressRegisterNode(V0_REG, CHARS_ATTR_INDEX)
            )
        )

        self.memory_manager.clean()
        return instructions

    def visit__SubstringNode(self, node: cil.SubstringNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()

        if isinstance(node.n, int):
            instructions.append(mips.LoadImmediateNode(reg1, node.n))
        else:
            length_dir = self.search_mem(node.n)
            instructions.append(
                mips.LoadWordNode(
                    reg1, mips.MemoryAddressRegisterNode(FP_REG, length_dir)
                )
            )

        # Reserve memory for new string
        instructions.append(mips.MoveNode(A0_REG, reg1))
        instructions.append(mips.AddiNode(A0_REG, A0_REG, 1))
        instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
        instructions.append(mips.SyscallNode())

        reg2 = self.memory_manager.get_unused_register()
        instructions.append(mips.MoveNode(reg2, V0_REG))  # Init of bytes

        source_index = self.search_mem(node.string)
        instructions.append(
            mips.LoadWordNode(
                S1_REG, mips.MemoryAddressRegisterNode(FP_REG, source_index)
            )
        )
        instructions.append(
            mips.LoadWordNode(
                S1_REG, mips.MemoryAddressRegisterNode(S1_REG, CHARS_ATTR_INDEX)
            )
        )

        reg3 = self.memory_manager.get_unused_register()

        if isinstance(node.index, int):
            instructions.append(mips.LoadImmediateNode(reg1, node.index))
        else:
            index_dir = self.search_mem(node.index)
            instructions.append(
                mips.LoadWordNode(
                    reg3, mips.MemoryAddressRegisterNode(FP_REG, index_dir)
                )
            )

        instructions.append(mips.AddNode(S1_REG, S1_REG, reg3))
        instructions.append(mips.MoveNode(A0_REG, reg1))
        instructions.append(mips.MoveNode(S0_REG, V0_REG))
        instructions.append(mips.JumpAndLinkNode(COPY_BYTES))

        instructions.append(
            mips.StoreByteNode(ZERO, mips.MemoryAddressRegisterNode(S0_REG, 0))
        )
        # r2 init of bytes
        # r1 length

        dest_offset = self.search_mem(node.dest)
        _size = STRING_SIZE
        instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
        instructions.append(mips.LoadImmediateNode(A0_REG, _size))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.StoreWordNode(
                V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_offset)
            )
        )
        r5 = self.memory_manager.get_unused_register()
        instructions.append(mips.LoadAddressNode(r5, mips.LabelNode(STRING_TYPE)))
        instructions.append(
            mips.StoreWordNode(r5, mips.MemoryAddressRegisterNode(V0_REG, 0))
        )

        # storing string length

        instructions.append(
            mips.StoreWordNode(
                reg1, mips.MemoryAddressRegisterNode(V0_REG, LENGTH_ATTR_INDEX)
            )
        )
        # storing string chars ref
        instructions.append(
            mips.StoreWordNode(
                reg2, mips.MemoryAddressRegisterNode(V0_REG, CHARS_ATTR_INDEX)
            )
        )

        self.memory_manager.clean()
        return instructions

    # Ok
    def visit__SetAttrNode(self, node: cil.SetAttrNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instance_dir = self.search_mem(node.instance)
        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(FP_REG, instance_dir),
                comment="Set Attribute",
            )
        )

        value__offset = self.search_mem(node.source)
        instructions.append(
            mips.LoadWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(FP_REG, value__offset),
                comment="Address of instance",
            )
        )

        attr_dir = self.attr_indexes[node.type][node.attr]
        instructions.append(
            mips.StoreWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(reg1, attr_dir),
                comment=f"Set attribute in index {node.attr}",
            )
        )

        self.memory_manager.clean()
        return instructions

    # Ok
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

        attr_dir = self.attr_indexes[node.type][node.attr]
        instructions.append(
            mips.LoadWordNode(
                reg2,
                mips.MemoryAddressRegisterNode(reg1, attr_dir),
                f"Load attribute at index {node.attr}",
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

    def visit__GotoIfNode(self, node: cil.GotoIfNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        cond_dir = self.search_mem(node.cond)
        reg1 = self.memory_manager.get_unused_register()

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, cond_dir))
        )
        instructions.append(mips.BneqzNode(reg1,  node.label))

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

    # Ok
    def visit__AssignNode(self, node: cil.AssignNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()

        if isinstance(node.source, int):
            instructions.append(mips.LoadImmediateNode(reg1, node.source))
        else:
            source_dir = self.search_mem(node.source)
            instructions.append(
                mips.LoadWordNode(
                    reg1, mips.MemoryAddressRegisterNode(FP_REG, source_dir)
                )
            )

        dest_dir = self.search_mem(node.dest)

        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def visit__DefaultValueNode(self, node: cil.DefaultValueNode, *args, **kwargs):
        instructions = []
        self.memory_manager.save()
        reg = self.memory_manager.get_unused_register()
        dest_dir = self.search_mem(node.dest)

        if node.type in ["Int", "Bool"]:
            instructions.append(mips.LoadImmediateNode(reg, 0))
            instructions.append(
                mips.StoreWordNode(
                    reg, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )

        elif node.type == STRING_TYPE:
            _size = STRING_SIZE
            instructions.append(mips.MipsAstNode(comment="Allocate Empty String"))
            instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
            instructions.append(mips.LoadImmediateNode(A0_REG, _size))
            instructions.append(mips.SyscallNode())

            instructions.append(
                mips.StoreWordNode(
                    V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )
            reg = self.memory_manager.get_unused_register()
            instructions.append(mips.LoadAddressNode(reg, mips.LabelNode(STRING_TYPE)))
            instructions.append(
                mips.StoreWordNode(
                    reg, mips.MemoryAddressRegisterNode(V0_REG, TYPEINFO_ATTR_INDEX)
                )
            )

            instructions.append(mips.LoadImmediateNode(reg, 0))
            instructions.append(
                mips.StoreWordNode(
                    reg, mips.MemoryAddressRegisterNode(V0_REG, LENGTH_ATTR_INDEX)
                )
            )
            instructions.append(mips.LoadAddressNode(reg, EMPTY_STR_VALUE))
            instructions.append(
                mips.StoreWordNode(
                    reg, mips.MemoryAddressRegisterNode(V0_REG, CHARS_ATTR_INDEX)
                )
            )

        elif node.type != "Void":
            _size = (len(self.types[node.type].attributes) + 1) * 4
            instructions.append(mips.LoadImmediateNode(V0_REG, SYSCALL_SBRK))
            instructions.append(mips.LoadImmediateNode(ARG_REGISTERS[0], _size))
            instructions.append(mips.SyscallNode())

            instructions.append(
                mips.StoreWordNode(
                    V0_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )

            reg2 = self.memory_manager.get_unused_register()

            instructions.append(
                mips.LoadAddressNode(reg2, mips.LabelNode(node.type.name))
            )
            instructions.append(
                mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(V0_REG, 0))
            )

        else:
            instructions.append(
                mips.LoadAddressNode(reg, mips.LabelNode(node.type.name))
            )
            instructions.append(
                mips.StoreWordNode(
                    reg, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
                )
            )

        self.memory_manager.clean()
        return instructions

    def visit__IsVoidNode(self, node: cil.IsVoidNode, *args, **kwargs):
        self.memory_manager.save()

        r1 = self.memory_manager.get_unused_register()
        r2 = self.memory_manager.get_unused_register()
        source_dir = self.search_mem(node.value)
        dest_dir = self.search_mem(node.dest)

        instructions = [
            mips.LoadWordNode(r1, mips.MemoryAddressRegisterNode(FP_REG, source_dir)),
            mips.LoadAddressNode(r2, mips.LabelNode(VOID)),
            mips.SetEqNode(r1, r1, r2),
            mips.StoreWordNode(r1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir)),
        ]
        self.memory_manager.clean()
        return instructions

    def visit__RuntimeErrorNode(self, node: cil.RuntimeErrorNode, *args, **kwargs):
        # TODO  Print Error
        instructions = []
        instructions.append(
            mips.LoadImmediateNode(V0_REG, 10, comment="Store syscall for exit")
        )  # exit syscall
        instructions.append(mips.SyscallNode(comment="Exit"))
        return instructions

    def get_loop_count(self):
        self.loop_count += 1
        return self.loop_count

    def get_exit_count(self):
        self.exit_count += 1
        return self.exit_count

    def clean_pushed_args(self):
        self.pushed_args = 0

    def push_arg(self):
        self.pushed_args += 1

    def search_mem(self, id: str):
        if id in self.locals:
            index = self.locals.index(id)
            return index * WORD_SIZE
        elif id in self.params:
            index = self.params.index(id)
            return (index - len(self.params)) * WORD_SIZE

    def generate_attr_indexes(self, type):
        attributes = [attr.name for attr in self.types[type].attributes]

        self.attr_indexes[type] = {}
        for i, attr in enumerate(attributes):
            self.attr_indexes[type][attr] = WORD_SIZE * (i + 1)

    def push_register(self, reg):
        instructions = []
        instructions.append(
            mips.StoreWordNode(
                reg, mips.MemoryAddressRegisterNode(SP_REG, 0), comment="Push to stack"
            )
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, WORD_SIZE))
        return instructions

    def register_copy_bytes(self):
        """
        Source in $s0
        Dest in $s1
        Length in a0
        """
        self.memory_manager.save()

        r1 = self.memory_manager.get_unused_register()

        instructions = [
            mips.LabelInstructionNode(COPY_BYTES),
            mips.MoveNode(A1_REG, S0_REG),
            mips.LabelInstructionNode(f"{COPY_BYTES}__LOOP"),
            mips.BeqzNode(A0_REG, f"{COPY_BYTES}__END"),
            mips.LoadByteNode(r1, mips.MemoryAddressRegisterNode(S1_REG, 0)),
            mips.StoreByteNode(r1, mips.MemoryAddressRegisterNode(S0_REG, 0)),
            mips.AddiNode(S1_REG, S1_REG, 1),
            mips.AddiNode(S0_REG, S0_REG, 1),
            mips.AddiNode(A0_REG, A0_REG, -1),
            mips.JumpNode(f"{COPY_BYTES}__LOOP"),
            mips.LabelInstructionNode(f"{COPY_BYTES}__END"),
            mips.JumpRegisterNode(RA_REG),
        ]

        self.memory_manager.clean()
        return instructions
