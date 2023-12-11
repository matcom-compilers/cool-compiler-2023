.data
abort: .asciiz "Abort called from class "
case_error: .asciiz "error case not have dinamyc type"
void_error: .asciiz "void error"
substring_error: .asciiz "error substring is out of range"
String: .asciiz "String"
Bool: .asciiz "Bool"
Int: .asciiz "Int"
Void: .asciiz "Void"
string_space: .space 1024
newline: .asciiz "\n"
IO: .asciiz "IO"
Object: .asciiz "Object"
Foo: .asciiz "Foo"
Bar: .asciiz "Bar"
Razz: .asciiz "Razz"
Bazz: .asciiz "Bazz"
Main: .asciiz "Main"
str1: .asciiz "do nothing"
StaticVoid: .word Void, StaticVoid, VoidError, VoidError, VoidError, VoidError, VoidError, VoidError, VoidError, VoidError, VoidError, VoidError, VoidError
StaticObject: .word Object_inherits, 8, Object_type_name, Object_abort, Object_copy
StaticIO: .word IO_inherits, 8, IO_type_name, IO_abort, IO_copy, IO_out_string, IO_out_int, IO_in_string, IO_in_int
StaticFoo: .word Foo_inherits, 28, Foo_type_name, Foo_abort, Foo_copy, Foo_out_string, Foo_out_int, Foo_in_string, Foo_in_int, Foo_printh, Foo_doh
StaticBar: .word Bar_inherits, 44, Bar_type_name, Bar_abort, Bar_copy, Bar_out_string, Bar_out_int, Bar_in_string, Bar_in_int, Bar_printh, Bar_doh
StaticRazz: .word Razz_inherits, 36, Razz_type_name, Razz_abort, Razz_copy, Razz_out_string, Razz_out_int, Razz_in_string, Razz_in_int, Razz_printh, Razz_doh
StaticBazz: .word Bazz_inherits, 20, Bazz_type_name, Bazz_abort, Bazz_copy, Bazz_out_string, Bazz_out_int, Bazz_in_string, Bazz_in_int, Bazz_printh, Bazz_doh
StaticMain: .word Main_inherits, 24, Main_type_name, Main_abort, Main_copy, Main_main
Object_inherits: .word -1, -1, -1, 1, -1, -1, -1, -1, -1, -1
IO_inherits: .word -1, -1, -1, -1, 1, -1, -1, -1, -1, -1
Foo_inherits: .word -1, -1, -1, 4, 3, 1, -1, -1, 2, -1
Bar_inherits: .word -1, -1, -1, 6, 5, 3, 1, 2, 4, -1
Razz_inherits: .word -1, -1, -1, 5, 4, 2, -1, 1, 3, -1
Bazz_inherits: .word -1, -1, -1, 3, 2, -1, -1, -1, 1, -1
Main_inherits: .word -1, -1, -1, 2, -1, -1, -1, -1, -1, 1
.text
.globl main
main:
	jal __init_Main__
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	jal Main_main
	li $v0, 10
	syscall
Foo_printh:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 16($sp)
	lw $t0, 8($t0)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Bazz_out_int
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 0
	move $a0, $t0
	jr $ra
Foo_doh:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	li $t1, 2
	add $t0, $t0, $t1
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Bar_printh:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 16($sp)
	lw $t0, 8($t0)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Bazz_out_int
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 0
	move $a0, $t0
	jr $ra
Bar_doh:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	li $t1, 2
	add $t0, $t0, $t1
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Razz_printh:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 16($sp)
	lw $t0, 8($t0)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Bazz_out_int
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 0
	move $a0, $t0
	jr $ra
Razz_doh:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	li $t1, 2
	add $t0, $t0, $t1
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Bazz_printh:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 16($sp)
	lw $t0, 8($t0)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Bazz_out_int
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 0
	move $a0, $t0
	jr $ra
Bazz_doh:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	lw $t0, 8($t0)
	li $t1, 1
	add $t0, $t0, $t1
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	lw $t0, 0($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_main:
	li $a0, 11
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str1
	copy_0:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_0
	move $t0, $v0
	move $a0, $t0
	jr $ra
__init_Foo__:
	li $a0, 28
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Foo
	sw $t0, 0($s1)
	la $t0, StaticFoo
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 1
	sw $t0, 8($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_0
	li $t1, 100
	lw $s5, 32($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_1
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_0
	move $t1, $s5
	la $s7, case_0
	end_if_temps_0:
	end_if_temps_1:
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_3
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_2
	move $t1, $s5
	la $s7, case_1
	end_if_temps_2:
	end_if_temps_3:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_5
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_4
	move $t1, $s5
	la $s7, case_2
	end_if_temps_4:
	end_if_temps_5:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_7
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_6
	move $t1, $s5
	la $s7, case_3
	end_if_temps_6:
	end_if_temps_7:
	jr $s7
error_case_0:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_0:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Foo__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_0
case_1:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_0
case_2:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_0
case_3:
	lw $t0, 0($sp)
	j end_case_0
end_case_0:
	addi $sp, $sp, 4
	sw $t0, 12($s1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bazz_printh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	sw $a0, 16($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_1
	li $t1, 100
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_9
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_8
	move $t1, $s5
	la $s7, case_4
	end_if_temps_8:
	end_if_temps_9:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_11
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_10
	move $t1, $s5
	la $s7, case_5
	end_if_temps_10:
	end_if_temps_11:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_13
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_12
	move $t1, $s5
	la $s7, case_6
	end_if_temps_12:
	end_if_temps_13:
	jr $s7
error_case_1:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_4:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_1
case_5:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_1
case_6:
	lw $t0, 0($sp)
	j end_case_1
end_case_1:
	addi $sp, $sp, 4
	sw $t0, 20($s1)
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 40($t0)
	jalr $t0
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Foo_doh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Foo_printh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	sw $t0, 24($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_Bar__:
	li $a0, 44
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Bar
	sw $t0, 0($s1)
	la $t0, StaticBar
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 1
	sw $t0, 8($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_2
	li $t1, 100
	lw $s5, 32($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_15
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_14
	move $t1, $s5
	la $s7, case_7
	end_if_temps_14:
	end_if_temps_15:
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_17
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_16
	move $t1, $s5
	la $s7, case_8
	end_if_temps_16:
	end_if_temps_17:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_19
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_18
	move $t1, $s5
	la $s7, case_9
	end_if_temps_18:
	end_if_temps_19:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_21
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_20
	move $t1, $s5
	la $s7, case_10
	end_if_temps_20:
	end_if_temps_21:
	jr $s7
error_case_2:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_7:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Foo__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_2
case_8:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_2
case_9:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_2
case_10:
	lw $t0, 0($sp)
	j end_case_2
end_case_2:
	addi $sp, $sp, 4
	sw $t0, 12($s1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bazz_printh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	sw $a0, 16($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_3
	li $t1, 100
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_23
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_22
	move $t1, $s5
	la $s7, case_11
	end_if_temps_22:
	end_if_temps_23:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_25
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_24
	move $t1, $s5
	la $s7, case_12
	end_if_temps_24:
	end_if_temps_25:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_27
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_26
	move $t1, $s5
	la $s7, case_13
	end_if_temps_26:
	end_if_temps_27:
	jr $s7
error_case_3:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_11:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_3
case_12:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_3
case_13:
	lw $t0, 0($sp)
	j end_case_3
end_case_3:
	addi $sp, $sp, 4
	sw $t0, 20($s1)
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 40($t0)
	jalr $t0
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Foo_doh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Foo_printh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	sw $t0, 24($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_4
	li $t1, 100
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_29
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_28
	move $t1, $s5
	la $s7, case_14
	end_if_temps_28:
	end_if_temps_29:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_31
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_30
	move $t1, $s5
	la $s7, case_15
	end_if_temps_30:
	end_if_temps_31:
	jr $s7
error_case_4:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_14:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_4
case_15:
	lw $t0, 0($sp)
	j end_case_4
end_case_4:
	addi $sp, $sp, 4
	sw $t0, 28($s1)
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bazz_doh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 28($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Razz_doh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Razz_printh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	sw $t0, 32($s1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bar_doh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	sw $a0, 36($s1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bar_printh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	sw $a0, 40($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_Razz__:
	li $a0, 36
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Razz
	sw $t0, 0($s1)
	la $t0, StaticRazz
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 1
	sw $t0, 8($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_5
	li $t1, 100
	lw $s5, 32($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_33
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_32
	move $t1, $s5
	la $s7, case_16
	end_if_temps_32:
	end_if_temps_33:
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_35
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_34
	move $t1, $s5
	la $s7, case_17
	end_if_temps_34:
	end_if_temps_35:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_37
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_36
	move $t1, $s5
	la $s7, case_18
	end_if_temps_36:
	end_if_temps_37:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_39
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_38
	move $t1, $s5
	la $s7, case_19
	end_if_temps_38:
	end_if_temps_39:
	jr $s7
error_case_5:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_16:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Foo__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_5
case_17:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_5
case_18:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_5
case_19:
	lw $t0, 0($sp)
	j end_case_5
end_case_5:
	addi $sp, $sp, 4
	sw $t0, 12($s1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bazz_printh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	sw $a0, 16($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_6
	li $t1, 100
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_41
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_40
	move $t1, $s5
	la $s7, case_20
	end_if_temps_40:
	end_if_temps_41:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_43
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_42
	move $t1, $s5
	la $s7, case_21
	end_if_temps_42:
	end_if_temps_43:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_45
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_44
	move $t1, $s5
	la $s7, case_22
	end_if_temps_44:
	end_if_temps_45:
	jr $s7
error_case_6:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_20:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_6
case_21:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_6
case_22:
	lw $t0, 0($sp)
	j end_case_6
end_case_6:
	addi $sp, $sp, 4
	sw $t0, 20($s1)
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 40($t0)
	jalr $t0
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Foo_doh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Foo_printh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	sw $t0, 24($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_7
	li $t1, 100
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_47
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_46
	move $t1, $s5
	la $s7, case_23
	end_if_temps_46:
	end_if_temps_47:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_49
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_48
	move $t1, $s5
	la $s7, case_24
	end_if_temps_48:
	end_if_temps_49:
	jr $s7
error_case_7:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_23:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_7
case_24:
	lw $t0, 0($sp)
	j end_case_7
end_case_7:
	addi $sp, $sp, 4
	sw $t0, 28($s1)
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bazz_doh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	lw $t1, 28($t1)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	move $t1, $s2
	lw $t1, 4($t1)
	lw $t1, 40($t1)
	jalr $t1
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Razz_doh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -16
	sw $t0, 0($sp)
	sw $s1, 4($sp)
	sw $ra, 8($sp)
	sw $s2, 12($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 16($sp)
	jal Razz_printh
	addi $sp, $sp, 4
	lw $t0, 0($sp)
	lw $s1, 4($sp)
	lw $ra, 8($sp)
	lw $s2, 12($sp)
	addi $sp, $sp, 16
	add $t0, $t0, $a0
	sw $t0, 32($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_Bazz__:
	li $a0, 20
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Bazz
	sw $t0, 0($s1)
	la $t0, StaticBazz
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 1
	sw $t0, 8($s1)
	lw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $t0, 0($sp)
	lw $t0, 4($t0)
	lw $t0, 0($t0)
	la $s7, error_case_8
	li $t1, 100
	lw $s5, 32($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_51
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_50
	move $t1, $s5
	la $s7, case_25
	end_if_temps_50:
	end_if_temps_51:
	lw $s5, 28($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_53
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_52
	move $t1, $s5
	la $s7, case_26
	end_if_temps_52:
	end_if_temps_53:
	lw $s5, 20($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_55
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_54
	move $t1, $s5
	la $s7, case_27
	end_if_temps_54:
	end_if_temps_55:
	lw $s5, 24($t0)
	slt $s6, $s5, $t1
	beqz $s6, end_if_temps_57
	slt $s6, $zero, $s5
	beqz $s6, end_if_temps_56
	move $t1, $s5
	la $s7, case_28
	end_if_temps_56:
	end_if_temps_57:
	jr $s7
error_case_8:
	la $a0, case_error
	li $v0, 4
	syscall
		li $v0, 10
		syscall
case_25:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Foo__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_8
case_26:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_8
case_27:
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	j end_case_8
case_28:
	lw $t0, 0($sp)
	j end_case_8
end_case_8:
	addi $sp, $sp, 4
	sw $t0, 12($s1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 12($sp)
	jal Bazz_printh
	addi $sp, $sp, 4
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	sw $a0, 16($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_Main__:
	li $a0, 24
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Main
	sw $t0, 0($s1)
	la $t0, StaticMain
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bazz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	sw $t0, 8($s1)
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Foo__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	sw $t0, 12($s1)
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Razz__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	sw $t0, 16($s1)
	addi $sp, $sp, -12
	sw $s1, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	lw $s2, 8($sp)
	jal __init_Bar__
	lw $s1, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	move $t0, $a0
	sw $t0, 20($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_IO__:
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, IO
	sw $t0, 0($v0)
	la $t0, StaticIO
	sw $t0, 4($v0)
	move $a0, $v0
	jr $ra
__init_Object__:
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Object
	sw $t0, 0($v0)
	la $t0, StaticObject
	sw $t0, 4($v0) 
	move $a0, $v0
	jr $ra
Object_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Object_copy:
	jr $ra
Object_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
IO_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
IO_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
IO_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
IO_in_string:
li $v0, 8
la $a0, string_space
li $a1, 1024
syscall
	move $t0, $a0
	addi $t1, $zero, -1
	length_in_string_0:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, length_in_string_0
	move $t3, $t1
addi $t3, $t0, -2
sb $zero, 0($t3)
move $t0, $a0
addi $a0, $t1, 1
li $v0, 9
syscall
move $t1, $v0
copy_in_0:
lb $t3, 0($t0)
sb $t3, 0($t1)
addi $t0, $t0, 1
addi $t1, $t1, 1
	bnez $t3, copy_in_0
move $a0, $v0
	jr $ra
IO_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
IO_copy:
	jr $ra
IO_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Foo_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
Foo_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
Foo_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
Foo_in_string:
li $v0, 8
la $a0, string_space
li $a1, 1024
syscall
	move $t0, $a0
	addi $t1, $zero, -1
	length_in_string_1:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, length_in_string_1
	move $t3, $t1
addi $t3, $t0, -2
sb $zero, 0($t3)
move $t0, $a0
addi $a0, $t1, 1
li $v0, 9
syscall
move $t1, $v0
copy_in_1:
lb $t3, 0($t0)
sb $t3, 0($t1)
addi $t0, $t0, 1
addi $t1, $t1, 1
	bnez $t3, copy_in_1
move $a0, $v0
	jr $ra
Foo_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Foo_copy:
	jr $ra
Foo_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Bar_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
Bar_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
Bar_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
Bar_in_string:
li $v0, 8
la $a0, string_space
li $a1, 1024
syscall
	move $t0, $a0
	addi $t1, $zero, -1
	length_in_string_2:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, length_in_string_2
	move $t3, $t1
addi $t3, $t0, -2
sb $zero, 0($t3)
move $t0, $a0
addi $a0, $t1, 1
li $v0, 9
syscall
move $t1, $v0
copy_in_2:
lb $t3, 0($t0)
sb $t3, 0($t1)
addi $t0, $t0, 1
addi $t1, $t1, 1
	bnez $t3, copy_in_2
move $a0, $v0
	jr $ra
Bar_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Bar_copy:
	jr $ra
Bar_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Razz_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
Razz_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
Razz_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
Razz_in_string:
li $v0, 8
la $a0, string_space
li $a1, 1024
syscall
	move $t0, $a0
	addi $t1, $zero, -1
	length_in_string_3:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, length_in_string_3
	move $t3, $t1
addi $t3, $t0, -2
sb $zero, 0($t3)
move $t0, $a0
addi $a0, $t1, 1
li $v0, 9
syscall
move $t1, $v0
copy_in_3:
lb $t3, 0($t0)
sb $t3, 0($t1)
addi $t0, $t0, 1
addi $t1, $t1, 1
	bnez $t3, copy_in_3
move $a0, $v0
	jr $ra
Razz_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Razz_copy:
	jr $ra
Razz_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Bazz_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
Bazz_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
Bazz_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
Bazz_in_string:
li $v0, 8
la $a0, string_space
li $a1, 1024
syscall
	move $t0, $a0
	addi $t1, $zero, -1
	length_in_string_4:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, length_in_string_4
	move $t3, $t1
addi $t3, $t0, -2
sb $zero, 0($t3)
move $t0, $a0
addi $a0, $t1, 1
li $v0, 9
syscall
move $t1, $v0
copy_in_4:
lb $t3, 0($t0)
sb $t3, 0($t1)
addi $t0, $t0, 1
addi $t1, $t1, 1
	bnez $t3, copy_in_4
move $a0, $v0
	jr $ra
Bazz_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Bazz_copy:
	jr $ra
Bazz_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Main_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Main_copy:
	jr $ra
Main_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
String_type_name:
	la $a0, String
	jr $ra
Int_type_name:
	la $a0, Int
	jr $ra
Bool_type_name:
	la $a0, Bool
	jr $ra
String_abort:
	la $a0, abort
	li $v0, 4
	syscall
	la $a0, String
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Int_abort:
	la $a0, abort
	li $v0, 4
	syscall
	la $a0, Int
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Bool_abort:
	la $a0, abort
	li $v0, 4
	syscall
	la $a0, Bool
	li $v0, 4
	syscall
	li $v0, 10
	syscall
length:
	lw $t0, 0($sp)
	addi $t1, $zero, -1
	loop_len:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, loop_len
	move $a0, $t1
	jr $ra
substr:
	lw $t0, 0($sp)
	addi $t1, $zero, -1
	loop_len_full:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, loop_len_full
	move $t6, $t1
	lw $t0, 0($sp)
	lw $t5, 4($sp)
	add $t0, $t0, $t5
	lw $t1, 8($sp)
	slt $t4, $t5, $zero
	bnez $t4, s_error
	add $t5, $t5, $t1
	slt $t4, $t6, $t5
	bnez $t4, s_error
	addi $t4, $t1, 1
	add $a0, $zero, $t4
	li $v0, 9
	syscall
	move $t3, $v0
	li $t4, 0
	loop_substring:
	lb $t2, 0($t0)
	sb $t2, 0($t3)
	addi $t0, $t0, 1
	addi $t3, $t3, 1
	addi $t4, $t4, 1
	slt $t6, $t4, $t1
	bnez $t6, loop_substring
	move $a0, $v0
	jr $ra
	s_error:
	la $a0, substring_error
	li $v0, 4
	syscall
	li $v0, 10
	syscall
concat:
	lw $t0, 0($sp)
	addi $t1, $zero, -1
	loop_len_concat_one:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, loop_len_concat_one
	lw $t0, 4($sp)
	loop_len_concat_two:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, loop_len_concat_two
	move $t3, $t1
	addi $t3, $t3, 1
	add $a0, $zero, $t3
	li $v0, 9
	syscall
	move $t4, $v0
	lw $t0, 0($sp)
	concat_copy_one:
	lb $t2, 0($t0)
	beq $t2, $zero, end_concat_one
	sb $t2, 0($t4)
	addi $t0, $t0, 1
	addi $t4, $t4, 1
	bnez $t2, concat_copy_one
	end_concat_one:	lw $t0, 4($sp)
	concat_copy_two:
	lb $t2, 0($t0)
	sb $t2, 0($t4)
	addi $t0, $t0, 1
	addi $t4, $t4, 1
	bnez $t2, concat_copy_two
	move $a0, $v0
	jr $ra
VoidError:
	la $a0, void_error
	li $v0, 4
	syscall
	li $v0, 10
	syscall