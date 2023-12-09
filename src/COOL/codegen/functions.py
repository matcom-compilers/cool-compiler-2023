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
# Function for set bool
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
# Function fotrstring length
String_length:
    lw $t0, 4($sp)
    li $t1, 0
    li $t2, 0

  String_length_loop:
    lb $t1, 0($t0)
    beq $t1, $zero, String_length_loop_end
    addi $t0, $t0, 1
    addi $t2, $t2, 1
    j String_length_loop

  String_length_loop_end:
    move $v0, $t2
    jr $ra
"""

LEN=\
"""
# Function for length
length:
    lw $t0, 0($sp)
    addiu $sp, $sp, 4
    li $t1, 0
    li $t2, 0

  length_loop:
    lb $t1, 0($t0)
    beq $t1, $zero, length_loop_end
    addi $t0, $t0, 1
    addi $t2, $t2, 1
    j length_loop

  length_loop_end:
    move $v0, $t2
    jr $ra
"""
    
OUT_INT=\
"""
# Function for print int
IO_out_int:
    # load int
    lw $a0, 4($sp)
    # print int
    li  $v0, 1
    syscall
    # print newline
    la  $a0, newline
    # print string
    li  $v0, 4
    syscall
    jr $ra
"""

OUT_STRING=\
"""
IO_out_string:
    lw $t0, 4($sp)
    lw $t0, 4($t0)

  out_string_loop:
    lb $a0, 0($t0)
    addiu $t0, $t0, 1
    beq $a0, $zero, out_string_loop_end
    li $v0, 11
    syscall
    j out_string_loop

  out_string_loop_end:
    jr $ra
"""

# FIX
STR_CONCAT=\
"""
# Function for string concat
String_concat:
    li $t3, 0
    # save return address
    addiu $sp, $sp, -4
    sw $ra, 0($sp)
    # calculate str length
    lw $t0, 4($sp)
    addiu $sp, $sp, -4
    sw $t0, 0($sp)
    jal String_length
    add $t3, $t3, $v0
    # calculate other str length
    lw $t0, 8($sp)
    addiu $sp, $sp, -4
    sw $t0, 0($sp)
    jal String_length
    add $t3, $t3, $v0
    # allocate memory
    lw $ra, 0($sp)
    addiu $sp, $sp, 4
    lw $t1, 0($sp)
    addiu $sp, $sp, 4
    lw $t0, 0($sp)
    addiu $sp, $sp, 4
    move $a0, $t3
    li $v0, 9
    syscall
    li $t2, 0
    move $t3, $v0

  string1:
    lb $t2, 0($t0)
    beq $t2, $0, string2
    sb $t2, 0($t3)
    addi $t0, $t0, 1
    addi $t3, $t3, 1
    j string1

  string2:
    lb $t2, 0($t1)
    beq $t2, $0, done
    sb $t2, 0($t3)
    addi $t1, $t1, 1
    addi $t3, $t3, 1
    j string2

  done:
    sb $0, 0($t3)
    jr $ra
"""

#TODO
IN_INT=\
"""
# Function for read int
IO_in_int:
    jr $ra
"""

#TODO
IN_STRING=\
"""
# Function for read string
IO_in_string:
    jr $ra
"""

#TODO
OBJECT_COPY=\
"""
# Function for object copy
Object_copy:
    jr $ra
"""

#TODO
OBJECT_TYPE_NAME=\
"""
# Function for object type name
Object_type_name:
    jr $ra
"""

#TODO
OBJECT_ABORT=\
"""
# Function for object abort
Object_abort:
    jr $ra
"""

#TODO
STRING_SUBSTR=\
"""
# Function for string substr
String_substr:
    jr $ra
"""


ABORT=\
"""
abort:
    la $t0, abort_label

  abort_print_loop_0:
    lb $a0, 0($t0)
    addiu $t0, $t0, 1
    beq $a0, $zero, abort_print_loop_0_end
    li $v0, 11
    syscall
    j abort_print_loop_0

  abort_print_loop_0_end:
    lw $t0, 0($sp)
    addiu $sp, $sp, 4

  abort_print_loop_1:
    lb $a0, 0($t0)
    addiu $t0, $t0, 1
    beq $a0, $zero, abort_print_loop_1_end
    li $v0, 11
    syscall
    j abort_print_loop_1

  abort_print_loop_1_end:
    li  $v0, 10
    syscall
"""


FUNCTIONS = [
    SET_BOOL,
    STR_LEN,
    LEN,
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
