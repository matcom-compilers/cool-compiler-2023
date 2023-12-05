from enum import Enum


# NOTE: the strings cant be generated in .text section
def string_length(string: str):
    return len(string) + 1


NULL = "null"

TRUE = "true"

FALSE = "false"

NEWLINE = "\\n"

INDENT = "    "

COMMENT = "# {comment}\n"


class Types(Enum):
    INT = ".word"
    BOOL = ".byte"
    STRING = ".asciiz"


DATA_SECTION =\
f"""
# Data section
.data
newline:  .asciiz  "{NEWLINE}"
{NULL}:     .word    0
{TRUE}:     .byte    1
{FALSE}:    .byte    0
"""


SET_VAR_IN_DATA_SECTION=\
"""    {owner}_{var_name}: {type} {value}
"""


TEXT_SECTION =\
"""\n
# Text section
.text

.globl main
main:
"""


REQUEST_MEMORY=\
"""    # Request memory
    li $a0, {memory}
    li $v0, 9
    syscall"""


PUSH_STACK=\
"""    # Push stack
    addiu $sp, $sp, -4
    sw ${register}, 0($sp)
"""


POP_STACK=\
"""    # Pop stack
    lw ${register}, 0($sp)
    addiu $sp, $sp, 4
"""


STORE_DATA=\
"""
    # Store data
    li $t0, {data}
    sw $t0, {offset}(${register})"""


LOAD_DATA=\
"""
    # Load data
    lw $t0, {offset}(${register})
"""


CREATE_CLASS=\
"""
# Create class {class_name}
{class_name}:
{request_memory}

{attributes}
"""


CREATE_FUNCTION=\
"""
# Create function {function_name} from class {class_name}
{function_name}:
    addiu $sp, $sp, -4
    sw $ra, 0($sp)
{method}
{clean_stack}
    lw $ra, 0($sp)
    addiu $sp, $sp, 4
    jr $ra
"""


STORE_VALUES_IN_REGISTER=\
"""    li ${register}, {value}
"""


STORE_VALUES_IN_VARS=\
"""    sw ${register}, {offset}(${fp})
"""


# FUNCTIONS

EXIT=\
"""
# Exit program
exit:
    li $v0, 10
    syscall
"""

SET_BOOL=\
"""
set_bool:
    lw $t0, 0($sp)
    addiu $sp, $sp, 4

    lb  $t1, true
    beq $t0, $t1, set_bool_true
    la $t0, false
    jr $ra

    set_bool_true:
    la $t0, true
    jr $ra
"""

STR_LEN=\
"""
str_len:
    lb $t2, 0($t0)
    beq $t2, $zero, str_len_end
    addi $t1, $t1, 1
    addi $t0, $t0, 1
    j str_len

    str_len_end:
    move $t0, $t1
    jr $ra
"""


STR_DATA_TO_STACK=\
"""
str_stack_in:
    li $t1, 0
    li $t2, 0

str_stack_in_len:
    lb $t2, 0($t0)
    beq $t2, $zero, str_stack_in_len_end
    addi $t1, $t1, 1
    addi $t0, $t0, 1
    j str_stack_in_len

    str_stack_in_len_end:
    addi $t0, $t0, -1

str_stack_in_loop:
    lb $t2, 0($t0)
    beq $t1, $zero, str_stack_in_loop_end
    addiu $sp, $sp, -1
    sb $t2, 0($sp)
    addi $t0, $t0, -1
    addi $t1, $t1, -1
    j str_stack_in_loop

    str_stack_in_loop_end:
    jr $ra
"""


STR_STACK_TO_HEAP=\
"""
str_heap_in:
    li $t1, 0
    li $t2, 0

str_heap_in_loop:
    lb $t2, 0($sp)
    beq $t2, $zero, str_heap_in_loop_end
    addi $sp, $sp, 1
    sb $t2, 0($v0)
    addi $t1, $t1, 1
    addi $v0, $v0, 1
    j str_heap_in_loop

    str_heap_in_loop_end:
    sub $v0, $v0, $t1
    jr $ra
"""


STR_HEAP_TO_STACK=\
"""
str_heap_out:
    li $t1, 0
    li $t2, 0

str_heap_out_len:
    lb $t2, 0($v0)
    addi $t1, $t1, 1
    addi $v0, $v0, 1
    beq $t2, $zero, str_heap_out_loop
    j str_heap_out_len

str_heap_out_loop:
    lb $t2, 0($v0)
    addi $sp, $sp, -1
    sb $t2, 0($sp)
    addi $v0, $v0, -1
    beq $t1, $zero, str_heap_out_loop_end
    addi $t1, $t1, -1
    j str_heap_out_loop

    str_heap_out_loop_end:
    jr $ra
"""


FUNCTIONS = [
    SET_BOOL,
    STR_LEN,
    STR_DATA_TO_STACK,
    STR_STACK_TO_HEAP,
    STR_HEAP_TO_STACK,
    EXIT,
]
