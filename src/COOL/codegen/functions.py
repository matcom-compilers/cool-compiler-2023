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
# Function fot string length
String_length:
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
    lw $a0, 0($sp)
    addiu $sp, $sp, 4
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
    lw $t0, 0($sp)
    addiu $sp, $sp, 4

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

IN_INT=\
"""
# Function for read int
IO_in_int:

"""

IN_STRING=\
"""
# Function for read string
IO_in_string:

"""

OBJECT_COPY=\
"""
# Function for object copy
Object_copy:

"""

OBJECT_TYPE_NAME=\
"""
# Function for object type name
Object_type_name:

"""

OBJECT_ABORT=\
"""
# Function for object abort
Object_abort:

"""

STRING_SUBSTR=\
"""
# Function for string substr
String_substr:

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
