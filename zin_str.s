.data
str: .asciiz "Hello, World!\n"

.text
.globl main

main:
    # Imprimir el string
    li $v0, 4
    la $a0, str
    syscall

    # Salir del programa
    li $v0, 10
    syscall




in_string:
li $v0, 8
la $a0, string_space
li $a1, 1024
syscall
	move $t0, $a0
	addi $t1, $zero, -1
	jisus12:
	lb $t2, 0($t0)
	addi $t0, $t0, 1
	addi $t1, $t1, 1
	bnez $t2, jisus12
	move $t3, $t1
addi $t3, $t0, -2
sb $zero, 0($t3)
move $t0, $a0
addi $a0, $t1, 1
li $v0, 9
syscall
move $t1, $v0
paco45:
lb $t3, 0($t0)
sb $t3, 0($t1)
addi $t0, $t0, 1
addi $t1, $t1, 1
	bnez $t3, paco45
move $a0, $v0
	jr $ra