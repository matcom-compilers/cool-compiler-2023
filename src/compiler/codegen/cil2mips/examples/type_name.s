.data
A: .asciiz "A"
B: .asciiz "B"
Main: .asciiz "Main"
str1: .asciiz "Redefinicion de type_name en A"
str2: .asciiz "Redefinicion de type_name en B"
.text
.globl main
main:
	jal __init_Main__
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	jal Main_main
	li $v0, 10
	syscall
A_type_name:
	li $a0, 31
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
B_type_name:
	li $a0, 31
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str2
	copy_1:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_1
	move $t0, $v0
	move $a0, $t0
	jr $ra
Main_main:
	#Region Let
	addi $sp, $sp, -4
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	jal __init_A__
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	move $t0, $a0
	sw $t0, 0($sp)
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	jal __init_B__
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	move $t0, $a0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 12($sp)
	move $s2, $t0
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	jal A_type_name
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	sw $a0, 4($sp)
	jal out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	addi $sp, $sp, 4
	addi $sp, $sp, 4
	#End Region Let
	jr $ra
__init_A__:
	li $a0, 4
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, A
	sw $t0, 0($s1)
	move $a0, $s1
	jr $ra
__init_B__:
	li $a0, 4
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, B
	sw $t0, 0($s1)
	move $a0, $s1
	jr $ra
__init_Main__:
	li $a0, 4
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Main
	sw $t0, 0($s1)
	move $a0, $s1
	jr $ra
__init_IO__:
	li $a0, 4
	li $v0, 9
	syscall
	move $a0, $v0
	jr $ra
out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra