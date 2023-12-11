# FUNCTIONS
from COOL.codegen.utils import Comment
from COOL.codegen.utils import Label
from COOL.codegen.utils import Instruction


EXIT=[
    Comment("Function to exit program", indent=""),
    Label("exit"),
    Instruction("li", "$v0", "10"),
    Instruction("syscall"),
    "\n",
]


SET_BOOL=[
    Comment("Function to set bool", indent=""),
    Label("set_bool"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("addiu", "$sp", "$sp", "4"),
    Instruction("lb", "$t1", "true"),
    Instruction("beq", "$t0", "$t1", "set_bool_true"),
    Instruction("la", "$t0", "false"),
    Instruction("jr", "$ra"),
    Label("set_bool_true", indent="  "),
    Instruction("la", "$t0", "true"),
    Instruction("jr", "$ra"),
    "\n",
]


STR_LEN=[
    Comment("Function to get string length", indent=""),
    Label("String_length"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("addi", "$t1", "$zero", "-1"),
    Label("String_length_loop"),
    Instruction("lb", "$t2", "0($t0)"),
    Instruction("addi", "$t0", "$t0", "1"),
    Instruction("addi", "$t1", "$t1", "1"),
    Instruction("bnez", "$t2", "String_length_loop"),
    Instruction("move", "$t0", "$t1"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("la", "$t1", "Int"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]


OUT_INT=[
    Comment("Function to print Int", indent=""),
    Label("IO_out_int"),
    Instruction("lw", "$t0", "4($sp)"),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("move", "$a0", "$t0"),
    Instruction("li", "$v0", 1),
    Instruction("syscall"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "0($t0)"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    # FIX type
    Instruction("la", "$t1", "Int"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]


OUT_STRING=[
    Comment("Function to print String", indent=""),
    Label("IO_out_string"),
    Instruction("lw", "$t0", "4($sp)"),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("move", "$a0", "$t0"),
    Instruction("li", "$v0", 4),
    Instruction("syscall"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "0($t0)"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    # FIX type
    Instruction("la", "$t1", "String"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]


STR_CONCAT=[
    Comment("Function to concat strings", indent=""),
    Label("String_concat"),
    Instruction("li", "$t3", 0),
    Instruction("addiu", "$sp", "$sp", -4),
    Instruction("sw", "$ra", "0($sp)"),
    Instruction("lw", "$t0", "4($sp)"),
    Instruction("addiu", "$sp", "$sp", -4),
    Instruction("sw", "$t0", "0($sp)"),
    Instruction("jal", "String_length"),
    Instruction("addiu", "$sp", "$sp", 4),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("add", "$t3", "$zero", "$t0"),
    Instruction("lw", "$t0", "8($sp)"),
    Instruction("addiu", "$sp", "$sp", -4),
    Instruction("sw", "$t0", "0($sp)"),
    Instruction("jal", "String_length"),
    Instruction("addiu", "$sp", "$sp", 4),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("add", "$t3", "$t3", "$t0"),
    Instruction("addiu", "$t3", "$t3", 1),
    Instruction("lw", "$ra", "0($sp)"),
    Instruction("addiu", "$sp", "$sp", 4),
    Instruction("move", "$a0", "$t3"),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("move", "$t3", "$v0"),
    Instruction("lw", "$t1", "4($sp)"),
    Instruction("lw", "$t1", "4($t1)"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("li", "$t2", 0),
    Label("String_concat_string1"),
    Instruction("lb", "$t2", "0($t0)"),
    Instruction("beq", "$t2", "$0", "String_concat_string2"),
    Instruction("sb", "$t2", "0($v0)"),
    Instruction("addi", "$t0", "$t0", 1),
    Instruction("addi", "$v0", "$v0", 1),
    Instruction("j", "String_concat_string1"),
    Label("String_concat_string2"),
    Instruction("lb", "$t2", "0($t1)"),
    Instruction("sb", "$t2", "0($v0)"),
    Instruction("addi", "$t1", "$t1", 1),
    Instruction("addi", "$v0", "$v0", 1),
    Instruction("beq", "$t2", "$0", "String_concat_done"),
    Instruction("j", "String_concat_string2"),
    Label("String_concat_done"),
    Instruction("addi", "$v0", "$v0", 1),
    Instruction("sb", "$0", "0($v0)"),
    Instruction("move", "$t0", "$t3"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("la", "$t1", "String"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]
"""
concat:
    li $t3, 0
    
    # save return address
    addiu $sp, $sp, -4
    sw $ra, 0($sp)
    
    # calculate str length
    lw $t0, 4($sp)
    addiu $sp, $sp, -4
    sw $t0, 0($sp)
    jal String_length
    addiu $sp, $sp, 4
    add $t3, $zero, $t0
    
    # calculate other str length
    lw $t0, 8($sp)
    addiu $sp, $sp, -4
    sw $t0, 0($sp)
    jal String_length
    addiu $sp, $sp, 4
    add $t3, $t3, $t0
    addiu $t3, $t3, 1

    # load return address
    lw $ra, 0($sp)
    addiu $sp, $sp, 4
    
    # allocate memory
    move $a0, $t3
    li $v0, 9
    syscall
    move $t3, $v0

    lw $t1, 0($sp)
    lw $t1, 4($t1)
    lw $t0, 4($sp)
    lw $t0, 4($t0)
    li $t2, 0

  string1:
    lb $t2, 0($t0)
    beq $t2, $0, string2
    sb $t2, 0($v0)
    addi $t0, $t0, 1
    addi $v0, $v0, 1
    j string1

  string2:
    lb $t2, 0($t1)
    beq $t2, $0, done
    sb $t2, 0($v0)
    addi $t1, $t1, 1
    addi $v0, $v0, 1
    j string2

  done:
    addi $v0, $v0, 1
    sb $0, 0($v0)
    move $t0, $t3
    jr $ra
  """


IN_INT=[
    Comment("Function to read Int", indent=""),
    Label("IO_in_int"),
    Instruction("li", "$v0", 5),
    Instruction("syscall"),
    Instruction("move", "$t0", "$v0"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("la", "$t1", "Int"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]

# TODO
# FIX: return String object
IN_STRING=[
    Comment("Function to read String", indent=""),
    Label("IO_in_string"),
    Instruction("jr", "$ra"),
    "\n",
]

#TODO
OBJECT_COPY=[
    Comment("Function to copy object", indent=""),
    Label("Object_copy"),
    Instruction("jr", "$ra"),
    "\n",
]


OBJECT_TYPE_NAME=[
    Comment("Function to get type name", indent=""),
    Label("Object_type_name"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "0($t0)"),
    Instruction("lw", "$t0", "0($t0)"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("la", "$t1", "String"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]


OBJECT_ABORT=[
    Comment("Function to abort", indent=""),
    Label("Object_abort"),
    Instruction("la", "$a0", "abort_label"),
    Instruction("li", "$v0", 4),
    Instruction("syscall"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "0($t0)"),
    Instruction("lw", "$a0", "0($t0)"),
    Instruction("li", "$v0", 4),
    Instruction("syscall"),
    Instruction("li", "$v0", 10),
    Instruction("syscall"),
    "\n",
]



STRING_SUBSTR=[
    Comment("Function to get substr", indent=""),
    Label("String_substr"),
    Instruction("lw", "$t0", "0($sp)"),
    Instruction("lw", "$t0", "4($t0)"),
    Instruction("lw", "$t1", "4($sp)"),
    Instruction("lw", "$t1", "4($t1)"),
    Instruction("lw", "$t2", "8($sp)"),
    Instruction("lw", "$t2", "4($t2)"),
    Instruction("addi", "$a0", "$t2", "1"),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("move", "$t3", "$v0"),
    Instruction("add", "$t0", "$t0", "$t1"),
    Label("String_substr_loop"),
    Instruction("lb", "$t1", "0($t0)"),
    Instruction("sb", "$t1", "0($v0)"),
    Instruction("addi", "$t2", "$t2", "-1"),
    Instruction("addi", "$t0", "$t0", "1"),
    Instruction("addi", "$v0", "$v0", "1"),
    Instruction("beq", "$t2", "$0", "String_substr_end"),
    Instruction("j", "String_substr_loop"),
    Label("String_substr_end"),
    Instruction("li", "$t1", "0"),
    Instruction("sb", "$t1", "0($v0)"),
    Instruction("move", "$t0", "$t3"),
    # allocate the type
    Instruction("li", "$a0", 8),
    Instruction("li", "$v0", 9),
    Instruction("syscall"),
    Instruction("la", "$t1", "String"),
    Instruction("sw", "$t1", "0($v0)"),
    Instruction("sw", "$t0", "4($v0)"),
    Instruction("move", "$t0", "$v0"),
    Instruction("jr", "$ra"),
    "\n",
]
"""
substr:
    lw $t0, 8($sp)
    lw $t0, 4($t0)
    lw $t1, 4($sp)
    lw $t1, 4($t1)
    lw $t2, 0($sp)
    lw $t2, 4($t2)

    addi $a0, $t2, 1
    li $v0, 9
    syscall
    move $t3, $v0
    add $t0, $t0, $t1


  substring_loop:
    lb $t1 0($t0)
    sb $t1 0($v0)
    addi $t2 $t2 -1
    addi $t0 $t0 1
    addi $v0 $v0 1
    beq $t2 $0 substring_end
    j substring_loop

  substring_end:
    li $t1 0
    sb $t1 0($v0)
    move $t0 $t3
    jr $ra
"""


FUNCTIONS = [
    SET_BOOL,
    STR_LEN,
    STR_CONCAT,
    OUT_INT,
    OUT_STRING,
    IN_INT,
    IN_STRING,
    OBJECT_COPY,
    OBJECT_TYPE_NAME,
    OBJECT_ABORT,
    STRING_SUBSTR,
    EXIT,
]
