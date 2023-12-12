# Data section
.data
newline:  .asciiz "\n"
null:  .word 0
true:  .word 1
false:  .word 0
abort_label:  .asciiz "Abort called from class "
str_0:  .asciiz "enter a string\n"
str_1:  .asciiz "that was a palindrome\n"
str_2:  .asciiz "that was not a palindrome\n"
Object_label:  .asciiz "Object\n"
IO_label:  .asciiz "IO\n"
Int_label:  .asciiz "Int\n"
String_label:  .asciiz "String\n"
Bool_label:  .asciiz "Bool\n"
Main_label:  .asciiz "Main\n"
Object:  .word Object_label, Object_abort, Object_type_name, Object_copy
IO:  .word IO_label, Object_abort, Object_type_name, Object_copy, IO_out_string, IO_out_int, IO_in_string, IO_in_int
Int:  .word Int_label, Object_abort, Object_type_name, Object_copy
String:  .word String_label, Object_abort, Object_type_name, Object_copy, String_length, String_concat, String_substr
Bool:  .word Bool_label, Object_abort, Object_type_name, Object_copy
Main:  .word Main_label, Object_abort, Object_type_name, Object_copy, IO_out_string, IO_out_int, IO_in_string, IO_in_int, Main_pal, Main_main
# Text section
.text
main:
    jal Main_class
    addiu $sp $sp -4
    sw $v0 0($sp)
    jal Main_main
    j exit
# Create class Main
Main_class:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Main
    sw $t0 0($v0)
    addiu $sp $sp -4
    sw $ra 0($sp)
    addiu $sp $sp -4
    sw $v0 0($sp)
    # attribute i: Int
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 0
    sw $t0 4($v0)
    move $t0 $v0
    # end attribute i: Int


    lw $v0 0($sp)
    addiu $sp $sp 4
    sw $t0 4($v0)
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $t0 $v0
    jr $ra


# Create function pal from class Main
Main_pal:
    addiu $sp $sp -4
    sw $ra 0($sp)
    # if_1
    # execute method length
    addiu $sp $sp -4
    # get variable s
    lw $t0 12($sp)
    # end get variable s
    sw $t0 0($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 4
    # end execute method length


    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 0
    sw $t0 4($v0)
    move $t0 $v0
    lw $t1 4($t0)
    lw $t0 0($sp)
    lw $t0 4($t0)
    addiu $sp $sp 4
    seq $t0 $t0 $t1
    addiu $sp $sp -4
    sw $t0 0($sp)
    jal set_bool
    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    lw $t0 0($sp)
    sw $t0 4($v0)
    move $t0 $v0
    addiu $sp $sp 4
    lw $t0 4($t0)
    la $t1 true
    beq $t1 $t0 then_1
    # if_2
    # execute method length
    addiu $sp $sp -4
    # get variable s
    lw $t0 12($sp)
    # end get variable s
    sw $t0 0($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 4
    # end execute method length


    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 1
    sw $t0 4($v0)
    move $t0 $v0
    lw $t1 4($t0)
    lw $t0 0($sp)
    lw $t0 4($t0)
    addiu $sp $sp 4
    seq $t0 $t0 $t1
    addiu $sp $sp -4
    sw $t0 0($sp)
    jal set_bool
    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    lw $t0 0($sp)
    sw $t0 4($v0)
    move $t0 $v0
    addiu $sp $sp 4
    lw $t0 4($t0)
    la $t1 true
    beq $t1 $t0 then_2
    # if_3
    # execute method substr
    addiu $sp $sp -12
    # get variable s
    lw $t0 20($sp)
    # end get variable s
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 0
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 4($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 1
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 8($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 24($t0)
    jal $t0
    addiu $sp $sp 12
    # end execute method substr


    addiu $sp $sp -4
    sw $t0 0($sp)
    # execute method substr
    addiu $sp $sp -12
    # get variable s
    lw $t0 24($sp)
    # end get variable s
    sw $t0 0($sp)
    # execute method length
    addiu $sp $sp -4
    # get variable s
    lw $t0 28($sp)
    # end get variable s
    sw $t0 0($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 4
    # end execute method length


    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 1
    sw $t0 4($v0)
    move $t0 $v0
    lw $t1 4($t0)
    lw $t0 0($sp)
    lw $t0 4($t0)
    addiu $sp $sp 4
    sub $t0 $t0 $t1
    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    lw $t0 0($sp)
    sw $t0 4($v0)
    move $t0 $v0
    addiu $sp $sp 4
    sw $t0 4($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 1
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 8($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 24($t0)
    jal $t0
    addiu $sp $sp 12
    # end execute method substr


    lw $t1 4($t0)
    lw $t0 0($sp)
    lw $t0 4($t0)
    addiu $sp $sp 4
    seq $t0 $t0 $t1
    addiu $sp $sp -4
    sw $t0 0($sp)
    jal set_bool
    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    lw $t0 0($sp)
    sw $t0 4($v0)
    move $t0 $v0
    addiu $sp $sp 4
    lw $t0 4($t0)
    la $t1 true
    beq $t1 $t0 then_3
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    la $t0 false
    sw $t0 4($v0)
    move $t0 $v0
    j end_if_3
  then_3:
    # execute class method pal
    addiu $sp $sp -8
    # execute method substr
    addiu $sp $sp -12
    # get variable s
    lw $t0 28($sp)
    # end get variable s
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 1
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 4($sp)
    # execute method length
    addiu $sp $sp -4
    # get variable s
    lw $t0 32($sp)
    # end get variable s
    sw $t0 0($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 4
    # end execute method length


    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 2
    sw $t0 4($v0)
    move $t0 $v0
    lw $t1 4($t0)
    lw $t0 0($sp)
    lw $t0 4($t0)
    addiu $sp $sp 4
    sub $t0 $t0 $t1
    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    lw $t0 0($sp)
    sw $t0 4($v0)
    move $t0 $v0
    addiu $sp $sp 4
    sw $t0 8($sp)
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 24($t0)
    jal $t0
    addiu $sp $sp 12
    # end execute method substr


    sw $t0 4($sp)
    lw $t0 12($sp)
    sw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 32($t0)
    jal $t0
    addiu $sp $sp 8
    # end execute class method pal


  end_if_3:
    # end_if_3
    j end_if_2
  then_2:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    la $t0 true
    sw $t0 4($v0)
    move $t0 $v0
  end_if_2:
    # end_if_2
    j end_if_1
  then_1:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    la $t0 true
    sw $t0 4($v0)
    move $t0 $v0
  end_if_1:
    # end_if_1
    lw $ra 0($sp)
    addiu $sp $sp 4
    jr $ra


# Create function main from class Main
Main_main:
    addiu $sp $sp -4
    sw $ra 0($sp)
    # assign variable i
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    li $t0 1
    sw $t0 4($v0)
    move $t0 $v0
    lw $t0 4($t0)
    and $t0 $t0 $t1
    addiu $sp $sp -4
    sw $t0 0($sp)
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    lw $t0 0($sp)
    sw $t0 4($v0)
    move $t0 $v0
    addiu $sp $sp 4
    lw $t1 4($sp)
    sw $t0 4($t1)
    sw $t1 4($sp)
    # end assign variable i
    # execute class method out_string
    addiu $sp $sp -8
    li $a0 8
    li $v0 9
    syscall 
    la $t0 String
    sw $t0 0($v0)
    la $t0 str_0
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 4($sp)
    lw $t0 12($sp)
    sw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 8
    # end execute class method out_string


    # if_4
    # execute class method pal
    addiu $sp $sp -8
    # execute class method in_string
    addiu $sp $sp -4
    lw $t0 16($sp)
    sw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 24($t0)
    jal $t0
    addiu $sp $sp 4
    # end execute class method in_string


    sw $t0 4($sp)
    lw $t0 12($sp)
    sw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 32($t0)
    jal $t0
    addiu $sp $sp 8
    # end execute class method pal


    lw $t0 4($t0)
    la $t1 true
    beq $t1 $t0 then_4
    # execute class method out_string
    addiu $sp $sp -8
    li $a0 8
    li $v0 9
    syscall 
    la $t0 String
    sw $t0 0($v0)
    la $t0 str_2
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 4($sp)
    lw $t0 12($sp)
    sw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 8
    # end execute class method out_string


    j end_if_4
  then_4:
    # execute class method out_string
    addiu $sp $sp -8
    li $a0 8
    li $v0 9
    syscall 
    la $t0 String
    sw $t0 0($v0)
    la $t0 str_1
    sw $t0 4($v0)
    move $t0 $v0
    sw $t0 4($sp)
    lw $t0 12($sp)
    sw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 16($t0)
    jal $t0
    addiu $sp $sp 8
    # end execute class method out_string


  end_if_4:
    # end_if_4
    lw $ra 0($sp)
    addiu $sp $sp 4
    jr $ra


# Create class Object
Object_class:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Object
    sw $t0 0($v0)
    addiu $sp $sp -4
    sw $ra 0($sp)
    addiu $sp $sp -4
    sw $v0 0($sp)
    la $t0 null
    lw $v0 0($sp)
    addiu $sp $sp 4
    sw $t0 4($v0)
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $t0 $v0
    jr $ra


# Create class IO
IO_class:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 IO
    sw $t0 0($v0)
    addiu $sp $sp -4
    sw $ra 0($sp)
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $t0 $v0
    jr $ra


# Create class Int
Int_class:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Int
    sw $t0 0($v0)
    addiu $sp $sp -4
    sw $ra 0($sp)
    addiu $sp $sp -4
    sw $v0 0($sp)
    li $t0 0
    lw $v0 0($sp)
    addiu $sp $sp 4
    sw $t0 4($v0)
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $t0 $v0
    jr $ra


# Create class String
String_class:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 String
    sw $t0 0($v0)
    addiu $sp $sp -4
    sw $ra 0($sp)
    addiu $sp $sp -4
    sw $v0 0($sp)
    li $t0 0
    lw $v0 0($sp)
    addiu $sp $sp 4
    sw $t0 4($v0)
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $t0 $v0
    jr $ra


# Create class Bool
Bool_class:
    li $a0 8
    li $v0 9
    syscall 
    la $t0 Bool
    sw $t0 0($v0)
    addiu $sp $sp -4
    sw $ra 0($sp)
    addiu $sp $sp -4
    sw $v0 0($sp)
    la $t0 false
    lw $v0 0($sp)
    addiu $sp $sp 4
    sw $t0 4($v0)
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $t0 $v0
    jr $ra


# Function to set bool
set_bool:
    lw $t0 0($sp)
    addiu $sp $sp 4
    lb $t1 true
    beq $t0 $t1 set_bool_true
    la $t0 false
    jr $ra
  set_bool_true:
    la $t0 true
    jr $ra


# Function to get string length
String_length:
    lw $t0 0($sp)
    lw $t0 4($t0)
    addi $t1 $zero -1
String_length_loop:
    lb $t2 0($t0)
    addi $t0 $t0 1
    addi $t1 $t1 1
    bnez $t2 String_length_loop
    move $t0 $t1
    li $a0 8
    li $v0 9
    syscall 
    la $t1 Int
    sw $t1 0($v0)
    sw $t0 4($v0)
    move $t0 $v0
    jr $ra


# Function to concat strings
String_concat:
    li $t3 0
    addiu $sp $sp -4
    sw $ra 0($sp)
    lw $t0 4($sp)
    addiu $sp $sp -4
    sw $t0 0($sp)
    jal String_length
    addiu $sp $sp 4
    lw $t0 4($t0)
    add $t3 $zero $t0
    lw $t0 8($sp)
    addiu $sp $sp -4
    sw $t0 0($sp)
    jal String_length
    addiu $sp $sp 4
    lw $t0 4($t0)
    add $t3 $t3 $t0
    addiu $t3 $t3 1
    lw $ra 0($sp)
    addiu $sp $sp 4
    move $a0 $t3
    li $v0 9
    syscall 
    move $t3 $v0
    lw $t1 4($sp)
    lw $t1 4($t1)
    lw $t0 0($sp)
    lw $t0 4($t0)
    li $t2 0
String_concat_string1:
    lb $t2 0($t0)
    beq $t2 $0 String_concat_string2
    sb $t2 0($v0)
    addi $t0 $t0 1
    addi $v0 $v0 1
    j String_concat_string1
String_concat_string2:
    lb $t2 0($t1)
    sb $t2 0($v0)
    addi $t1 $t1 1
    addi $v0 $v0 1
    beq $t2 $0 String_concat_done
    j String_concat_string2
String_concat_done:
    addi $v0 $v0 1
    sb $0 0($v0)
    move $t0 $t3
    li $a0 8
    li $v0 9
    syscall 
    la $t1 String
    sw $t1 0($v0)
    sw $t0 4($v0)
    move $t0 $v0
    jr $ra


# Function to print Int
IO_out_int:
    lw $t0 4($sp)
    lw $t0 4($t0)
    move $a0 $t0
    li $v0 1
    syscall 
    lw $t0 0($sp)


# Function to print String
IO_out_string:
    lw $t0 4($sp)
    lw $t0 4($t0)
    move $a0 $t0
    li $v0 4
    syscall 
    lw $t0 0($sp)
    jr $ra


# Function to read Int
IO_in_int:
    li $v0 5
    syscall 
    move $t0 $v0
    li $a0 8
    li $v0 9
    syscall 
    la $t1 Int
    sw $t1 0($v0)
    sw $t0 4($v0)
    move $t0 $v0
    jr $ra


# Function to read String
IO_in_string:
    #la $a0 string_space
    la $a1 1024
    li $v0 8
    syscall 
    move $t0 $a0
    addi $t1 $zero -1
IO_in_string_loop:
    lb $t2 0($t0)
    addi $t0 $t0 1
    addi $t1 $t1 1
    bnez $t2 IO_in_string_loop
    move $t3 $t1
    addi $t3 $t0 -2
    sb $zero 0($t3)
    move $t0 $a0
    addi $a0 $t1 1
    li $v0 9
    syscall 
    move $t1 $v0
IO_in_string_loop2:
    lb $t3 0($t0)
    sb $t3 0($t1)
    addi $t0 $t0 1
    addi $t1 $t1 1
    bnez $t3 IO_in_string_loop2
    move $a0 $v0
    jr $ra


# Function to copy object
Object_copy:
    jr $ra


# Function to get type name
Object_type_name:
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $t0 0($t0)
    li $a0 8
    li $v0 9
    syscall 
    la $t1 String
    sw $t1 0($v0)
    sw $t0 4($v0)
    move $t0 $v0
    jr $ra


# Function to abort
Object_abort:
    la $a0 abort_label
    li $v0 4
    syscall 
    lw $t0 0($sp)
    lw $t0 0($t0)
    lw $a0 0($t0)
    li $v0 4
    syscall 
    li $v0 10
    syscall 


# Function to get substr
String_substr:
    lw $t0 0($sp)
    lw $t0 4($t0)
    lw $t1 4($sp)
    lw $t1 4($t1)
    lw $t2 8($sp)
    lw $t2 4($t2)
    addi $a0 $t2 1
    li $v0 9
    syscall 
    move $t3 $v0
    add $t0 $t0 $t1
String_substr_loop:
    lb $t1 0($t0)
    sb $t1 0($v0)
    addi $t2 $t2 -1
    addi $t0 $t0 1
    addi $v0 $v0 1
    beq $t2 $0 String_substr_end
    j String_substr_loop
String_substr_end:
    li $t1 0
    sb $t1 0($v0)
    move $t0 $t3
    li $a0 8
    li $v0 9
    syscall 
    la $t1 String
    sw $t1 0($v0)
    sw $t0 4($v0)
    move $t0 $v0
    jr $ra


# Function to exit program
exit:
    li $v0 10
    syscall 

