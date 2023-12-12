.data
input_buffer:   .space  1024    # Espacio para almacenar la cadena de entrada
prompt:         .asciiz "Ingrese una cadena: "

.text
main:
	li $v0, 4
    la $a0, prompt
    syscall

    # Leer la cadena de entrada

	# Imprimir la cadena de entrada
	# li $v0, 4
	# la $a0, input_buffer
	# syscall
	jal IO_in_string

	jal IO_out_string
	# Terminar el programa
	li $v0, 10
	syscall

# IO_in_int:
#     li $v0 5
#     syscall 
#     move $t0 $v0
#     li $a0 8
#     li $v0 9
#     syscall 
#     la $t1 Int
#     sw $t1 0($v0)
#     sw $t0 4($v0)
#     move $t0 $v0
#     jr $ra


# Function to read String
IO_in_string:
    la $a0 input_buffer
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



# Function to print String
IO_out_string:
    lw $t0 4($sp)
    lw $t0 4($t0)
    move $a0 $t0
    li $v0 4
    syscall 
    lw $t0 0($sp)
    jr $ra

