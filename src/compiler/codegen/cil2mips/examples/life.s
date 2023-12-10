.data
abort: .asciiz "Abort called from class"
case_error: .asciiz "error case not have dinamyc type"
substring_error: .asciiz "error substring is out of range"
String: .asciiz "String"
Bool: .asciiz "Bool"
Int: .asciiz "Int"
Void: .asciiz "Void"
string_space: .space 1024
newline: .asciiz "\n"
Board: .asciiz "Board"
CellularAutomaton: .asciiz "CellularAutomaton"
Main: .asciiz "Main"
str3: .asciiz "\n"
str4: .asciiz "\n"
str5: .asciiz "\n"
str6: .asciiz " "
str7: .asciiz " "
str8: .asciiz " "
str9: .asciiz " "
str10: .asciiz " "
str11: .asciiz " "
str12: .asciiz " "
str13: .asciiz " "
str14: .asciiz " "
str15: .asciiz " "
str16: .asciiz " "
str17: .asciiz " "
str18: .asciiz " "
str19: .asciiz " "
str20: .asciiz "X"
str21: .asciiz "X"
str22: .asciiz "X"
str23: .asciiz "X"
str24: .asciiz "X"
str25: .asciiz "X"
str26: .asciiz "X"
str27: .asciiz "X"
str28: .asciiz "X"
str29: .asciiz "X"
str30: .asciiz "X"
str31: .asciiz "-"
str32: .asciiz "-"
str33: .asciiz ""
str34: .asciiz "\nPlease chose a number:\n"
str35: .asciiz "t1: A cross\n"
str36: .asciiz "t2: A slash from the upper left to lower right\n"
str37: .asciiz "t3: A slash from the upper right to lower left\n"
str38: .asciiz "t4: An X\n"
str39: .asciiz "t5: A greater than sign \n"
str40: .asciiz "t6: A less than sign\n"
str41: .asciiz "t7: Two greater than signs\n"
str42: .asciiz "t8: Two less than signs\n"
str43: .asciiz "t9: A 'V'\n"
str44: .asciiz "t10: An inverse 'V'\n"
str45: .asciiz "t11: Numbers 9 and 10 combined\n"
str46: .asciiz "t12: A full grid\n"
str47: .asciiz "t13: A 'T'\n"
str48: .asciiz "t14: A plus '+'\n"
str49: .asciiz "t15: A 'W'\n"
str50: .asciiz "t16: An 'M'\n"
str51: .asciiz "t17: An 'E'\n"
str52: .asciiz "t18: A '3'\n"
str53: .asciiz "t19: An 'O'\n"
str54: .asciiz "t20: An '8'\n"
str55: .asciiz "t21: An 'S'\n"
str56: .asciiz "Your choice => "
str57: .asciiz "\n"
str58: .asciiz " XX  XXXX XXXX  XX  "
str59: .asciiz "    X   X   X   X   X    "
str60: .asciiz "X     X     X     X     X"
str61: .asciiz "X   X X X   X   X X X   X"
str62: .asciiz "X     X     X   X   X    "
str63: .asciiz "    X   X   X     X     X"
str64: .asciiz "X  X  X  XX  X      "
str65: .asciiz " X  XX  X  X  X     "
str66: .asciiz "X   X X X   X  "
str67: .asciiz "  X   X X X   X"
str68: .asciiz "X X X X X X X X"
str69: .asciiz "XXXXXXXXXXXXXXXXXXXXXXXXX"
str70: .asciiz "XXXXX  X    X    X    X  "
str71: .asciiz "  X    X  XXXXX  X    X  "
str72: .asciiz "X     X X X X   X X  "
str73: .asciiz "  X X   X X X X     X"
str74: .asciiz "XXXXX   X   XXXXX   X   XXXX"
str75: .asciiz "XXX    X   X  X    X   XXXX "
str76: .asciiz " XX X  XX  X XX "
str77: .asciiz " XX X  XX  X XX X  XX  X XX "
str78: .asciiz " XXXX   X    XX    X   XXXX "
str79: .asciiz "                         "
str84: .asciiz ""
str80: .asciiz "Would you like to continue with the next generation? \n"
str81: .asciiz "Please use lowercase y or n for your answer [y]: "
str82: .asciiz "\n"
str83: .asciiz "n"
str89: .asciiz ""
str85: .asciiz "\n\n"
str86: .asciiz "Would you like to choose a background pattern? \n"
str87: .asciiz "Please use lowercase y or n for your answer [n]: "
str88: .asciiz "y"
str92: .asciiz ""
str90: .asciiz "Welcome to the Game of Life.\n"
str91: .asciiz "There are many initial states to choose from. \n"
str2: .asciiz ""
StaticVoid: .word Void, 4
StaticObject: .word Object_inherits, 8, Object_type_name, Object_abort, Object_copy

StaticIO: .word IO_inherits, 8, IO_type_name, IO_abort, IO_copy, IO_out_string, IO_out_int, IO_in_string, IO_in_int

StaticBoard: .word Board_inherits, 20, Board_type_name, Board_abort, Board_copy, Board_out_string, Board_out_int, Board_in_string, Board_in_int, Board_size_of_board, Board_board_init

StaticCellularAutomaton: .word CellularAutomaton_inherits, 24, CellularAutomaton_type_name, CellularAutomaton_abort, CellularAutomaton_copy, CellularAutomaton_out_string, CellularAutomaton_out_int, CellularAutomaton_in_string, CellularAutomaton_in_int, CellularAutomaton_size_of_board, CellularAutomaton_board_init, CellularAutomaton_init, CellularAutomaton_print, CellularAutomaton_num_cells, CellularAutomaton_cell, CellularAutomaton_north, CellularAutomaton_south, CellularAutomaton_east, CellularAutomaton_west, CellularAutomaton_northwest, CellularAutomaton_northeast, CellularAutomaton_southeast, CellularAutomaton_southwest, CellularAutomaton_neighbors, CellularAutomaton_cell_at_next_evolution, CellularAutomaton_evolve, CellularAutomaton_option, CellularAutomaton_prompt, CellularAutomaton_prompt2

StaticMain: .word Main_inherits, 28, Main_type_name, Main_abort, Main_copy, Main_out_string, Main_out_int, Main_in_string, Main_in_int, Main_size_of_board, Main_board_init, Main_init, Main_print, Main_num_cells, Main_cell, Main_north, Main_south, Main_east, Main_west, Main_northwest, Main_northeast, Main_southeast, Main_southwest, Main_neighbors, Main_cell_at_next_evolution, Main_evolve, Main_option, Main_prompt, Main_prompt2, Main_main

Object_inherits: .word -1, -1, -1, 1, -1, -1, -1, -1

IO_inherits: .word -1, -1, -1, -1, 1, -1, -1, -1

Board_inherits: .word -1, -1, -1, 3, 2, 1, -1, -1

CellularAutomaton_inherits: .word -1, -1, -1, 4, 3, 2, 1, -1

Main_inherits: .word -1, -1, -1, 5, 4, 3, 2, 1

.text
.globl main
main:
	jal __init_Main__
	addi $sp, $sp, -4
	sw $a0, 0($sp)
	jal Main_main
	li $v0, 10
	syscall
Board_size_of_board:
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal length
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	jr $ra
Board_board_init:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Board_size_of_board
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 0($sp)
	li $t1, 15
	beq $t0, $t1, compare_0
	addi $t0, $zero, 0
	j end_compare_22
	compare_0:
	addi $t0, $zero, 1
	end_compare_22:
	beq $t0, $zero, else_0
	li $t0, 3
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_0
else_0:
	lw $t0, 0($sp)
	li $t1, 16
	beq $t0, $t1, compare_1
	addi $t0, $zero, 0
	j end_compare_23
	compare_1:
	addi $t0, $zero, 1
	end_compare_23:
	beq $t0, $zero, else_1
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_1
else_1:
	lw $t0, 0($sp)
	li $t1, 20
	beq $t0, $t1, compare_2
	addi $t0, $zero, 0
	j end_compare_24
	compare_2:
	addi $t0, $zero, 1
	end_compare_24:
	beq $t0, $zero, else_2
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_2
else_2:
	lw $t0, 0($sp)
	li $t1, 21
	beq $t0, $t1, compare_3
	addi $t0, $zero, 0
	j end_compare_25
	compare_3:
	addi $t0, $zero, 1
	end_compare_25:
	beq $t0, $zero, else_3
	li $t0, 3
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 7
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_3
else_3:
	lw $t0, 0($sp)
	li $t1, 25
	beq $t0, $t1, compare_4
	addi $t0, $zero, 0
	j end_compare_26
	compare_4:
	addi $t0, $zero, 1
	end_compare_26:
	beq $t0, $zero, else_4
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_4
else_4:
	lw $t0, 0($sp)
	li $t1, 28
	beq $t0, $t1, compare_5
	addi $t0, $zero, 0
	j end_compare_27
	compare_5:
	addi $t0, $zero, 1
	end_compare_27:
	beq $t0, $zero, else_5
	li $t0, 7
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_5
else_5:
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
endif_5:
endif_4:
endif_3:
endif_2:
endif_1:
endif_0:
	lw $t0, 4($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
CellularAutomaton_size_of_board:
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal length
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	jr $ra
CellularAutomaton_board_init:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Board_size_of_board
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 0($sp)
	li $t1, 15
	beq $t0, $t1, compare_6
	addi $t0, $zero, 0
	j end_compare_28
	compare_6:
	addi $t0, $zero, 1
	end_compare_28:
	beq $t0, $zero, else_6
	li $t0, 3
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_6
else_6:
	lw $t0, 0($sp)
	li $t1, 16
	beq $t0, $t1, compare_7
	addi $t0, $zero, 0
	j end_compare_29
	compare_7:
	addi $t0, $zero, 1
	end_compare_29:
	beq $t0, $zero, else_7
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_7
else_7:
	lw $t0, 0($sp)
	li $t1, 20
	beq $t0, $t1, compare_8
	addi $t0, $zero, 0
	j end_compare_30
	compare_8:
	addi $t0, $zero, 1
	end_compare_30:
	beq $t0, $zero, else_8
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_8
else_8:
	lw $t0, 0($sp)
	li $t1, 21
	beq $t0, $t1, compare_9
	addi $t0, $zero, 0
	j end_compare_31
	compare_9:
	addi $t0, $zero, 1
	end_compare_31:
	beq $t0, $zero, else_9
	li $t0, 3
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 7
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_9
else_9:
	lw $t0, 0($sp)
	li $t1, 25
	beq $t0, $t1, compare_10
	addi $t0, $zero, 0
	j end_compare_32
	compare_10:
	addi $t0, $zero, 1
	end_compare_32:
	beq $t0, $zero, else_10
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_10
else_10:
	lw $t0, 0($sp)
	li $t1, 28
	beq $t0, $t1, compare_11
	addi $t0, $zero, 0
	j end_compare_33
	compare_11:
	addi $t0, $zero, 1
	end_compare_33:
	beq $t0, $zero, else_11
	li $t0, 7
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_11
else_11:
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
endif_11:
endif_10:
endif_9:
endif_8:
endif_7:
endif_6:
	lw $t0, 4($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
CellularAutomaton_init:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	sw $t0, 20($t1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_board_init
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	move $a0, $t0
	jr $ra
CellularAutomaton_print:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 0
	sw $t0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 8($sp)
	lw $t0, 16($t0)
	sw $t0, 0($sp)
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str3
	copy_0:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_0
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
loop_0:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	slt $t0, $t0, $t1
	beq $t0, $zero, end_while_0
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -12
	sw $s2, 0($sp)
	lw $t0, 40($sp)
	sw $t0, 4($sp)
	lw $t0, 44($sp)
	lw $t0, 12($t0)
	sw $t0, 8($sp)
	lw $s2, 16($sp)
	jal substr
	addi $sp, $sp, 12
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str4
	copy_1:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_1
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	lw $t1, 8($sp)
	lw $t1, 12($t1)
	add $t0, $t0, $t1
	sw $t0, 4($sp)
	j loop_0
end_while_0:
	la $a0, StaticVoid
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str5
	copy_2:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_2
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
CellularAutomaton_num_cells:
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal length
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	jr $ra
CellularAutomaton_cell:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	addi $t0, $t0, -1
	lw $t1, 4($sp)
	slt $t0, $t0, $t1
	beq $t0, $zero, else_12
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str6
	copy_3:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_3
	move $t0, $v0
	j endif_12
else_12:
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -12
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	sw $t0, 4($sp)
	li $t0, 1
	sw $t0, 8($sp)
	lw $s2, 16($sp)
	jal substr
	addi $sp, $sp, 12
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_12:
	move $a0, $t0
	jr $ra
CellularAutomaton_north:
	li $t0, 0
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	sub $t1, $t1, $t2
	slt $t1, $t1, $t0
	beq $t1, $zero, else_13
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str7
	copy_4:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_4
	move $t0, $v0
	j endif_13
else_13:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	lw $t1, 16($sp)
	lw $t1, 12($t1)
	sub $t0, $t0, $t1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_13:
	move $a0, $t0
	jr $ra
CellularAutomaton_south:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	add $t1, $t1, $t2
	slt $t0, $t0, $t1
	beq $t0, $zero, else_14
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str8
	copy_5:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_5
	move $t0, $v0
	j endif_14
else_14:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	lw $t1, 16($sp)
	lw $t1, 12($t1)
	add $t0, $t0, $t1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_14:
	move $a0, $t0
	jr $ra
CellularAutomaton_east:
	lw $t0, 4($sp)
	addi $t0, $t0, 1
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	addi $t1, $t1, 1
	beq $t0, $t1, compare_12
	addi $t0, $zero, 0
	j end_compare_34
	compare_12:
	addi $t0, $zero, 1
	end_compare_34:
	beq $t0, $zero, else_15
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str9
	copy_6:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_6
	move $t0, $v0
	j endif_15
else_15:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_15:
	move $a0, $t0
	jr $ra
CellularAutomaton_west:
	lw $t0, 4($sp)
	li $t1, 0
	beq $t0, $t1, compare_13
	addi $t0, $zero, 0
	j end_compare_35
	compare_13:
	addi $t0, $zero, 1
	end_compare_35:
	beq $t0, $zero, else_16
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str10
	copy_7:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_7
	move $t0, $v0
	j endif_16
else_16:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	beq $t0, $t1, compare_14
	addi $t0, $zero, 0
	j end_compare_36
	compare_14:
	addi $t0, $zero, 1
	end_compare_36:
	beq $t0, $zero, else_17
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str11
	copy_8:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_8
	move $t0, $v0
	j endif_17
else_17:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, -1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_17:
endif_16:
	move $a0, $t0
	jr $ra
CellularAutomaton_northwest:
	li $t0, 0
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	sub $t1, $t1, $t2
	slt $t1, $t1, $t0
	beq $t1, $zero, else_18
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str12
	copy_9:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_9
	move $t0, $v0
	j endif_18
else_18:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	beq $t0, $t1, compare_15
	addi $t0, $zero, 0
	j end_compare_37
	compare_15:
	addi $t0, $zero, 1
	end_compare_37:
	beq $t0, $zero, else_19
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str13
	copy_10:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_10
	move $t0, $v0
	j endif_19
else_19:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, -1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_north
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_19:
endif_18:
	move $a0, $t0
	jr $ra
CellularAutomaton_northeast:
	li $t0, 0
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	sub $t1, $t1, $t2
	slt $t1, $t1, $t0
	beq $t1, $zero, else_20
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str14
	copy_11:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_11
	move $t0, $v0
	j endif_20
else_20:
	lw $t0, 4($sp)
	addi $t0, $t0, 1
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	addi $t1, $t1, 1
	beq $t0, $t1, compare_16
	addi $t0, $zero, 0
	j end_compare_38
	compare_16:
	addi $t0, $zero, 1
	end_compare_38:
	beq $t0, $zero, else_21
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str15
	copy_12:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_12
	move $t0, $v0
	j endif_21
else_21:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_north
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_21:
endif_20:
	move $a0, $t0
	jr $ra
CellularAutomaton_southeast:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	add $t1, $t1, $t2
	slt $t0, $t0, $t1
	beq $t0, $zero, else_22
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str16
	copy_13:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_13
	move $t0, $v0
	j endif_22
else_22:
	lw $t0, 4($sp)
	addi $t0, $t0, 1
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	addi $t1, $t1, 1
	beq $t0, $t1, compare_17
	addi $t0, $zero, 0
	j end_compare_39
	compare_17:
	addi $t0, $zero, 1
	end_compare_39:
	beq $t0, $zero, else_23
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str17
	copy_14:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_14
	move $t0, $v0
	j endif_23
else_23:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_south
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_23:
endif_22:
	move $a0, $t0
	jr $ra
CellularAutomaton_southwest:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	add $t1, $t1, $t2
	slt $t0, $t0, $t1
	beq $t0, $zero, else_24
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str18
	copy_15:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_15
	move $t0, $v0
	j endif_24
else_24:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	beq $t0, $t1, compare_18
	addi $t0, $zero, 0
	j end_compare_40
	compare_18:
	addi $t0, $zero, 1
	end_compare_40:
	beq $t0, $zero, else_25
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str19
	copy_16:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_16
	move $t0, $v0
	j endif_25
else_25:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, -1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_south
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_25:
endif_24:
	move $a0, $t0
	jr $ra
CellularAutomaton_neighbors:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_north
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	la $t0, str20
	loop_compare_0:
	lb $s5, 0($a0)
	lb $s6, 0($t0)
	addiu $a0, $a0, 1
	addiu $t0, $t0, 1
	bne $s5, $s6, end_not_equals_0
	bnez $s5, loop_compare_0
	li $a0, 1
	j end_compare_0
	end_not_equals_0:
	li $a0, 0
	end_compare_0:
	beq $a0, $zero, else_26
	li $t0, 1
	j endif_26
else_26:
	li $t0, 0
endif_26:
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_south
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str21
	loop_compare_1:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_1
	bnez $s5, loop_compare_1
	li $a0, 1
	j end_compare_1
	end_not_equals_1:
	li $a0, 0
	end_compare_1:
	beq $a0, $zero, else_27
	li $t1, 1
	j endif_27
else_27:
	li $t1, 0
endif_27:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_east
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str22
	loop_compare_2:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_2
	bnez $s5, loop_compare_2
	li $a0, 1
	j end_compare_2
	end_not_equals_2:
	li $a0, 0
	end_compare_2:
	beq $a0, $zero, else_28
	li $t1, 1
	j endif_28
else_28:
	li $t1, 0
endif_28:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_west
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str23
	loop_compare_3:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_3
	bnez $s5, loop_compare_3
	li $a0, 1
	j end_compare_3
	end_not_equals_3:
	li $a0, 0
	end_compare_3:
	beq $a0, $zero, else_29
	li $t1, 1
	j endif_29
else_29:
	li $t1, 0
endif_29:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_northeast
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str24
	loop_compare_4:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_4
	bnez $s5, loop_compare_4
	li $a0, 1
	j end_compare_4
	end_not_equals_4:
	li $a0, 0
	end_compare_4:
	beq $a0, $zero, else_30
	li $t1, 1
	j endif_30
else_30:
	li $t1, 0
endif_30:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_northwest
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str25
	loop_compare_5:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_5
	bnez $s5, loop_compare_5
	li $a0, 1
	j end_compare_5
	end_not_equals_5:
	li $a0, 0
	end_compare_5:
	beq $a0, $zero, else_31
	li $t1, 1
	j endif_31
else_31:
	li $t1, 0
endif_31:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_southeast
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str26
	loop_compare_6:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_6
	bnez $s5, loop_compare_6
	li $a0, 1
	j end_compare_6
	end_not_equals_6:
	li $a0, 0
	end_compare_6:
	beq $a0, $zero, else_32
	li $t1, 1
	j endif_32
else_32:
	li $t1, 0
endif_32:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_southwest
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str27
	loop_compare_7:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_7
	bnez $s5, loop_compare_7
	li $a0, 1
	j end_compare_7
	end_not_equals_7:
	li $a0, 0
	end_compare_7:
	beq $a0, $zero, else_33
	li $t1, 1
	j endif_33
else_33:
	li $t1, 0
endif_33:
	add $t0, $t0, $t1
	move $a0, $t0
	jr $ra
CellularAutomaton_cell_at_next_evolution:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_neighbors
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 3
	beq $a0, $t0, compare_19
	addi $a0, $zero, 0
	j end_compare_41
	compare_19:
	addi $a0, $zero, 1
	end_compare_41:
	beq $a0, $zero, else_34
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str28
	copy_17:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_17
	move $t0, $v0
	j endif_34
else_34:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_neighbors
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 2
	beq $a0, $t0, compare_20
	addi $a0, $zero, 0
	j end_compare_42
	compare_20:
	addi $a0, $zero, 1
	end_compare_42:
	beq $a0, $zero, else_35
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	la $t0, str29
	loop_compare_8:
	lb $s5, 0($a0)
	lb $s6, 0($t0)
	addiu $a0, $a0, 1
	addiu $t0, $t0, 1
	bne $s5, $s6, end_not_equals_8
	bnez $s5, loop_compare_8
	li $a0, 1
	j end_compare_8
	end_not_equals_8:
	li $a0, 0
	end_compare_8:
	beq $a0, $zero, else_36
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str30
	copy_18:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_18
	move $t0, $v0
	j endif_36
else_36:
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str31
	copy_19:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_19
	move $t0, $v0
endif_36:
	j endif_35
else_35:
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str32
	copy_20:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_20
	move $t0, $v0
endif_35:
endif_34:
	move $a0, $t0
	jr $ra
CellularAutomaton_evolve:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 0
	sw $t0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_num_cells
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str33
	copy_21:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_21
	move $t0, $v0
	sw $t0, 0($sp)
loop_1:
	lw $t0, 8($sp)
	lw $t1, 4($sp)
	slt $t0, $t0, $t1
	beq $t0, $zero, end_while_1
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 28($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 40($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell_at_next_evolution
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 4($sp)
	lw $s2, 12($sp)
	jal concat
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 8($sp)
	addi $t0, $t0, 1
	sw $t0, 8($sp)
	j loop_1
end_while_1:
	la $a0, StaticVoid
	lw $t0, 0($sp)
	lw $t1, 12($sp)
	sw $t0, 20($t1)
	lw $t0, 12($sp)
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
CellularAutomaton_option:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 27
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str34
	copy_22:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_22
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str35
	copy_23:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_23
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 49
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str36
	copy_24:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_24
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 49
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str37
	copy_25:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_25
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 11
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str38
	copy_26:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_26
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 27
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str39
	copy_27:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_27
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 23
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str40
	copy_28:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_28
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str41
	copy_29:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_29
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str42
	copy_30:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_30
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 12
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str43
	copy_31:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_31
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 22
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str44
	copy_32:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_32
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 33
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str45
	copy_33:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_33
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 19
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str46
	copy_34:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_34
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 13
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str47
	copy_35:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_35
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 18
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str48
	copy_36:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_36
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 13
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str49
	copy_37:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_37
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str50
	copy_38:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_38
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str51
	copy_39:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_39
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 13
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str52
	copy_40:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_40
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str53
	copy_41:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_41
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str54
	copy_42:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_42
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str55
	copy_43:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_43
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str56
	copy_44:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_44
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_in_int
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str57
	copy_45:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_45
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	li $t1, 1
	beq $t0, $t1, compare_21
	addi $t0, $zero, 0
	j end_compare_43
	compare_21:
	addi $t0, $zero, 1
	end_compare_43:
	beq $t0, $zero, else_37
	li $a0, 21
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str58
	copy_46:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_46
	move $t0, $v0
	j endif_37
else_37:
	lw $t0, 0($sp)
	li $t1, 2
	beq $t0, $t1, compare_22
	addi $t0, $zero, 0
	j end_compare_44
	compare_22:
	addi $t0, $zero, 1
	end_compare_44:
	beq $t0, $zero, else_38
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str59
	copy_47:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_47
	move $t0, $v0
	j endif_38
else_38:
	lw $t0, 0($sp)
	li $t1, 3
	beq $t0, $t1, compare_23
	addi $t0, $zero, 0
	j end_compare_45
	compare_23:
	addi $t0, $zero, 1
	end_compare_45:
	beq $t0, $zero, else_39
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str60
	copy_48:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_48
	move $t0, $v0
	j endif_39
else_39:
	lw $t0, 0($sp)
	li $t1, 4
	beq $t0, $t1, compare_24
	addi $t0, $zero, 0
	j end_compare_46
	compare_24:
	addi $t0, $zero, 1
	end_compare_46:
	beq $t0, $zero, else_40
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str61
	copy_49:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_49
	move $t0, $v0
	j endif_40
else_40:
	lw $t0, 0($sp)
	li $t1, 5
	beq $t0, $t1, compare_25
	addi $t0, $zero, 0
	j end_compare_47
	compare_25:
	addi $t0, $zero, 1
	end_compare_47:
	beq $t0, $zero, else_41
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str62
	copy_50:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_50
	move $t0, $v0
	j endif_41
else_41:
	lw $t0, 0($sp)
	li $t1, 6
	beq $t0, $t1, compare_26
	addi $t0, $zero, 0
	j end_compare_48
	compare_26:
	addi $t0, $zero, 1
	end_compare_48:
	beq $t0, $zero, else_42
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str63
	copy_51:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_51
	move $t0, $v0
	j endif_42
else_42:
	lw $t0, 0($sp)
	li $t1, 7
	beq $t0, $t1, compare_27
	addi $t0, $zero, 0
	j end_compare_49
	compare_27:
	addi $t0, $zero, 1
	end_compare_49:
	beq $t0, $zero, else_43
	li $a0, 21
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str64
	copy_52:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_52
	move $t0, $v0
	j endif_43
else_43:
	lw $t0, 0($sp)
	li $t1, 8
	beq $t0, $t1, compare_28
	addi $t0, $zero, 0
	j end_compare_50
	compare_28:
	addi $t0, $zero, 1
	end_compare_50:
	beq $t0, $zero, else_44
	li $a0, 21
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str65
	copy_53:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_53
	move $t0, $v0
	j endif_44
else_44:
	lw $t0, 0($sp)
	li $t1, 9
	beq $t0, $t1, compare_29
	addi $t0, $zero, 0
	j end_compare_51
	compare_29:
	addi $t0, $zero, 1
	end_compare_51:
	beq $t0, $zero, else_45
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str66
	copy_54:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_54
	move $t0, $v0
	j endif_45
else_45:
	lw $t0, 0($sp)
	li $t1, 10
	beq $t0, $t1, compare_30
	addi $t0, $zero, 0
	j end_compare_52
	compare_30:
	addi $t0, $zero, 1
	end_compare_52:
	beq $t0, $zero, else_46
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str67
	copy_55:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_55
	move $t0, $v0
	j endif_46
else_46:
	lw $t0, 0($sp)
	li $t1, 11
	beq $t0, $t1, compare_31
	addi $t0, $zero, 0
	j end_compare_53
	compare_31:
	addi $t0, $zero, 1
	end_compare_53:
	beq $t0, $zero, else_47
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str68
	copy_56:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_56
	move $t0, $v0
	j endif_47
else_47:
	lw $t0, 0($sp)
	li $t1, 12
	beq $t0, $t1, compare_32
	addi $t0, $zero, 0
	j end_compare_54
	compare_32:
	addi $t0, $zero, 1
	end_compare_54:
	beq $t0, $zero, else_48
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str69
	copy_57:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_57
	move $t0, $v0
	j endif_48
else_48:
	lw $t0, 0($sp)
	li $t1, 13
	beq $t0, $t1, compare_33
	addi $t0, $zero, 0
	j end_compare_55
	compare_33:
	addi $t0, $zero, 1
	end_compare_55:
	beq $t0, $zero, else_49
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str70
	copy_58:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_58
	move $t0, $v0
	j endif_49
else_49:
	lw $t0, 0($sp)
	li $t1, 14
	beq $t0, $t1, compare_34
	addi $t0, $zero, 0
	j end_compare_56
	compare_34:
	addi $t0, $zero, 1
	end_compare_56:
	beq $t0, $zero, else_50
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str71
	copy_59:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_59
	move $t0, $v0
	j endif_50
else_50:
	lw $t0, 0($sp)
	li $t1, 15
	beq $t0, $t1, compare_35
	addi $t0, $zero, 0
	j end_compare_57
	compare_35:
	addi $t0, $zero, 1
	end_compare_57:
	beq $t0, $zero, else_51
	li $a0, 22
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str72
	copy_60:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_60
	move $t0, $v0
	j endif_51
else_51:
	lw $t0, 0($sp)
	li $t1, 16
	beq $t0, $t1, compare_36
	addi $t0, $zero, 0
	j end_compare_58
	compare_36:
	addi $t0, $zero, 1
	end_compare_58:
	beq $t0, $zero, else_52
	li $a0, 22
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str73
	copy_61:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_61
	move $t0, $v0
	j endif_52
else_52:
	lw $t0, 0($sp)
	li $t1, 17
	beq $t0, $t1, compare_37
	addi $t0, $zero, 0
	j end_compare_59
	compare_37:
	addi $t0, $zero, 1
	end_compare_59:
	beq $t0, $zero, else_53
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str74
	copy_62:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_62
	move $t0, $v0
	j endif_53
else_53:
	lw $t0, 0($sp)
	li $t1, 18
	beq $t0, $t1, compare_38
	addi $t0, $zero, 0
	j end_compare_60
	compare_38:
	addi $t0, $zero, 1
	end_compare_60:
	beq $t0, $zero, else_54
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str75
	copy_63:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_63
	move $t0, $v0
	j endif_54
else_54:
	lw $t0, 0($sp)
	li $t1, 19
	beq $t0, $t1, compare_39
	addi $t0, $zero, 0
	j end_compare_61
	compare_39:
	addi $t0, $zero, 1
	end_compare_61:
	beq $t0, $zero, else_55
	li $a0, 17
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str76
	copy_64:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_64
	move $t0, $v0
	j endif_55
else_55:
	lw $t0, 0($sp)
	li $t1, 20
	beq $t0, $t1, compare_40
	addi $t0, $zero, 0
	j end_compare_62
	compare_40:
	addi $t0, $zero, 1
	end_compare_62:
	beq $t0, $zero, else_56
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str77
	copy_65:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_65
	move $t0, $v0
	j endif_56
else_56:
	lw $t0, 0($sp)
	li $t1, 21
	beq $t0, $t1, compare_41
	addi $t0, $zero, 0
	j end_compare_63
	compare_41:
	addi $t0, $zero, 1
	end_compare_63:
	beq $t0, $zero, else_57
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str78
	copy_66:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_66
	move $t0, $v0
	j endif_57
else_57:
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str79
	copy_67:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_67
	move $t0, $v0
endif_57:
endif_56:
endif_55:
endif_54:
endif_53:
endif_52:
endif_51:
endif_50:
endif_49:
endif_48:
endif_47:
endif_46:
endif_45:
endif_44:
endif_43:
endif_42:
endif_41:
endif_40:
endif_39:
endif_38:
endif_37:
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
CellularAutomaton_prompt:
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str84
	copy_68:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_68
	move $t0, $v0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 56
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str80
	copy_69:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_69
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 50
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str81
	copy_70:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_70
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_in_string
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str82
	copy_71:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_71
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	la $t1, str83
	loop_compare_9:
	lb $s5, 0($t0)
	lb $s6, 0($t1)
	addiu $t0, $t0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_9
	bnez $s5, loop_compare_9
	li $t0, 1
	j end_compare_9
	end_not_equals_9:
	li $t0, 0
	end_compare_9:
	beq $t0, $zero, else_58
	li $t0, 0
	j endif_58
else_58:
	li $t0, 1
endif_58:
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
CellularAutomaton_prompt2:
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str89
	copy_72:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_72
	move $t0, $v0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 5
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str85
	copy_73:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_73
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 50
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str86
	copy_74:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_74
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 50
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str87
	copy_75:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_75
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_in_string
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 0($sp)
	la $t1, str88
	loop_compare_10:
	lb $s5, 0($t0)
	lb $s6, 0($t1)
	addiu $t0, $t0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_10
	bnez $s5, loop_compare_10
	li $t0, 1
	j end_compare_10
	end_not_equals_10:
	li $t0, 0
	end_compare_10:
	beq $t0, $zero, else_59
	li $t0, 1
	j endif_59
else_59:
	li $t0, 0
endif_59:
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_size_of_board:
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal length
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	jr $ra
Main_board_init:
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Board_size_of_board
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 0($sp)
	li $t1, 15
	beq $t0, $t1, compare_42
	addi $t0, $zero, 0
	j end_compare_64
	compare_42:
	addi $t0, $zero, 1
	end_compare_64:
	beq $t0, $zero, else_60
	li $t0, 3
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_60
else_60:
	lw $t0, 0($sp)
	li $t1, 16
	beq $t0, $t1, compare_43
	addi $t0, $zero, 0
	j end_compare_65
	compare_43:
	addi $t0, $zero, 1
	end_compare_65:
	beq $t0, $zero, else_61
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_61
else_61:
	lw $t0, 0($sp)
	li $t1, 20
	beq $t0, $t1, compare_44
	addi $t0, $zero, 0
	j end_compare_66
	compare_44:
	addi $t0, $zero, 1
	end_compare_66:
	beq $t0, $zero, else_62
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_62
else_62:
	lw $t0, 0($sp)
	li $t1, 21
	beq $t0, $t1, compare_45
	addi $t0, $zero, 0
	j end_compare_67
	compare_45:
	addi $t0, $zero, 1
	end_compare_67:
	beq $t0, $zero, else_63
	li $t0, 3
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 7
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_63
else_63:
	lw $t0, 0($sp)
	li $t1, 25
	beq $t0, $t1, compare_46
	addi $t0, $zero, 0
	j end_compare_68
	compare_46:
	addi $t0, $zero, 1
	end_compare_68:
	beq $t0, $zero, else_64
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_64
else_64:
	lw $t0, 0($sp)
	li $t1, 28
	beq $t0, $t1, compare_47
	addi $t0, $zero, 0
	j end_compare_69
	compare_47:
	addi $t0, $zero, 1
	end_compare_69:
	beq $t0, $zero, else_65
	li $t0, 7
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 4
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
	j endif_65
else_65:
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 8($t1)
	li $t0, 5
	lw $t1, 4($sp)
	sw $t0, 12($t1)
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	sw $t0, 16($t1)
endif_65:
endif_64:
endif_63:
endif_62:
endif_61:
endif_60:
	lw $t0, 4($sp)
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_init:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	sw $t0, 20($t1)
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_board_init
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	move $a0, $t0
	jr $ra
Main_print:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 0
	sw $t0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 8($sp)
	lw $t0, 16($t0)
	sw $t0, 0($sp)
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str3
	copy_76:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_76
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
loop_2:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	slt $t0, $t0, $t1
	beq $t0, $zero, end_while_2
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -12
	sw $s2, 0($sp)
	lw $t0, 40($sp)
	sw $t0, 4($sp)
	lw $t0, 44($sp)
	lw $t0, 12($t0)
	sw $t0, 8($sp)
	lw $s2, 16($sp)
	jal substr
	addi $sp, $sp, 12
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str4
	copy_77:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_77
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	lw $t1, 8($sp)
	lw $t1, 12($t1)
	add $t0, $t0, $t1
	sw $t0, 4($sp)
	j loop_2
end_while_2:
	la $a0, StaticVoid
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str5
	copy_78:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_78
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_num_cells:
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal length
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	jr $ra
Main_cell:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	addi $t0, $t0, 1
	lw $t1, 4($sp)
	slt $t0, $t0, $t1
	beq $t0, $zero, else_66
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str6
	copy_79:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_79
	move $t0, $v0
	j endif_66
else_66:
	lw $t0, 0($sp)
	lw $t0, 20($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -12
	sw $s2, 0($sp)
	lw $t0, 24($sp)
	sw $t0, 4($sp)
	li $t0, 1
	sw $t0, 8($sp)
	lw $s2, 16($sp)
	jal substr
	addi $sp, $sp, 12
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_66:
	move $a0, $t0
	jr $ra
Main_north:
	li $t0, 0
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	sub $t1, $t1, $t2
	slt $t1, $t1, $t0
	beq $t1, $zero, else_67
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str7
	copy_80:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_80
	move $t0, $v0
	j endif_67
else_67:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	lw $t1, 16($sp)
	lw $t1, 12($t1)
	sub $t0, $t0, $t1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_67:
	move $a0, $t0
	jr $ra
Main_south:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	add $t1, $t1, $t2
	slt $t0, $t0, $t1
	beq $t0, $zero, else_68
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str8
	copy_81:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_81
	move $t0, $v0
	j endif_68
else_68:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	lw $t1, 16($sp)
	lw $t1, 12($t1)
	add $t0, $t0, $t1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_68:
	move $a0, $t0
	jr $ra
Main_east:
	lw $t0, 4($sp)
	addi $t0, $t0, 1
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	addi $t1, $t1, 1
	beq $t0, $t1, compare_48
	addi $t0, $zero, 0
	j end_compare_70
	compare_48:
	addi $t0, $zero, 1
	end_compare_70:
	beq $t0, $zero, else_69
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str9
	copy_82:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_82
	move $t0, $v0
	j endif_69
else_69:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_69:
	move $a0, $t0
	jr $ra
Main_west:
	lw $t0, 4($sp)
	li $t1, 0
	beq $t0, $t1, compare_49
	addi $t0, $zero, 0
	j end_compare_71
	compare_49:
	addi $t0, $zero, 1
	end_compare_71:
	beq $t0, $zero, else_70
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str10
	copy_83:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_83
	move $t0, $v0
	j endif_70
else_70:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	beq $t0, $t1, compare_50
	addi $t0, $zero, 0
	j end_compare_72
	compare_50:
	addi $t0, $zero, 1
	end_compare_72:
	beq $t0, $zero, else_71
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str11
	copy_84:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_84
	move $t0, $v0
	j endif_71
else_71:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_71:
endif_70:
	move $a0, $t0
	jr $ra
Main_northwest:
	li $t0, 0
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	sub $t1, $t1, $t2
	slt $t1, $t1, $t0
	beq $t1, $zero, else_72
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str12
	copy_85:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_85
	move $t0, $v0
	j endif_72
else_72:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	beq $t0, $t1, compare_51
	addi $t0, $zero, 0
	j end_compare_73
	compare_51:
	addi $t0, $zero, 1
	end_compare_73:
	beq $t0, $zero, else_73
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str13
	copy_86:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_86
	move $t0, $v0
	j endif_73
else_73:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_north
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_73:
endif_72:
	move $a0, $t0
	jr $ra
Main_northeast:
	li $t0, 0
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	sub $t1, $t1, $t2
	slt $t1, $t1, $t0
	beq $t1, $zero, else_74
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str14
	copy_87:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_87
	move $t0, $v0
	j endif_74
else_74:
	lw $t0, 4($sp)
	addi $t0, $t0, 1
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	addi $t1, $t1, 1
	beq $t0, $t1, compare_52
	addi $t0, $zero, 0
	j end_compare_74
	compare_52:
	addi $t0, $zero, 1
	end_compare_74:
	beq $t0, $zero, else_75
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str15
	copy_88:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_88
	move $t0, $v0
	j endif_75
else_75:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_north
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_75:
endif_74:
	move $a0, $t0
	jr $ra
Main_southeast:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	add $t1, $t1, $t2
	slt $t0, $t0, $t1
	beq $t0, $zero, else_76
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str16
	copy_89:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_89
	move $t0, $v0
	j endif_76
else_76:
	lw $t0, 4($sp)
	addi $t0, $t0, 1
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	addi $t1, $t1, 1
	beq $t0, $t1, compare_53
	addi $t0, $zero, 0
	j end_compare_75
	compare_53:
	addi $t0, $zero, 1
	end_compare_75:
	beq $t0, $zero, else_77
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str17
	copy_90:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_90
	move $t0, $v0
	j endif_77
else_77:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_south
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_77:
endif_76:
	move $a0, $t0
	jr $ra
Main_southwest:
	lw $t0, 0($sp)
	lw $t0, 16($t0)
	lw $t1, 4($sp)
	lw $t2, 0($sp)
	lw $t2, 12($t2)
	add $t1, $t1, $t2
	slt $t0, $t0, $t1
	beq $t0, $zero, else_78
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str18
	copy_91:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_91
	move $t0, $v0
	j endif_78
else_78:
	lw $t0, 4($sp)
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	div $t0, $t1
	mflo $t0
	lw $t1, 0($sp)
	lw $t1, 12($t1)
	mul $t0, $t0, $t1
	lw $t1, 4($sp)
	beq $t0, $t1, compare_54
	addi $t0, $zero, 0
	j end_compare_76
	compare_54:
	addi $t0, $zero, 1
	end_compare_76:
	beq $t0, $zero, else_79
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str19
	copy_92:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_92
	move $t0, $v0
	j endif_79
else_79:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	addi $t0, $t0, 1
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_south
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
endif_79:
endif_78:
	move $a0, $t0
	jr $ra
Main_neighbors:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_north
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	la $t0, str20
	loop_compare_11:
	lb $s5, 0($a0)
	lb $s6, 0($t0)
	addiu $a0, $a0, 1
	addiu $t0, $t0, 1
	bne $s5, $s6, end_not_equals_11
	bnez $s5, loop_compare_11
	li $a0, 1
	j end_compare_11
	end_not_equals_11:
	li $a0, 0
	end_compare_11:
	beq $a0, $zero, else_80
	li $t0, 1
	j endif_80
else_80:
	li $t0, 0
endif_80:
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_south
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str21
	loop_compare_12:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_12
	bnez $s5, loop_compare_12
	li $a0, 1
	j end_compare_12
	end_not_equals_12:
	li $a0, 0
	end_compare_12:
	beq $a0, $zero, else_81
	li $t1, 1
	j endif_81
else_81:
	li $t1, 0
endif_81:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_east
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str22
	loop_compare_13:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_13
	bnez $s5, loop_compare_13
	li $a0, 1
	j end_compare_13
	end_not_equals_13:
	li $a0, 0
	end_compare_13:
	beq $a0, $zero, else_82
	li $t1, 1
	j endif_82
else_82:
	li $t1, 0
endif_82:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_west
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str23
	loop_compare_14:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_14
	bnez $s5, loop_compare_14
	li $a0, 1
	j end_compare_14
	end_not_equals_14:
	li $a0, 0
	end_compare_14:
	beq $a0, $zero, else_83
	li $t1, 1
	j endif_83
else_83:
	li $t1, 0
endif_83:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_northeast
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str24
	loop_compare_15:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_15
	bnez $s5, loop_compare_15
	li $a0, 1
	j end_compare_15
	end_not_equals_15:
	li $a0, 0
	end_compare_15:
	beq $a0, $zero, else_84
	li $t1, 1
	j endif_84
else_84:
	li $t1, 0
endif_84:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_northwest
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str25
	loop_compare_16:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_16
	bnez $s5, loop_compare_16
	li $a0, 1
	j end_compare_16
	end_not_equals_16:
	li $a0, 0
	end_compare_16:
	beq $a0, $zero, else_85
	li $t1, 1
	j endif_85
else_85:
	li $t1, 0
endif_85:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_southeast
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str26
	loop_compare_17:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_17
	bnez $s5, loop_compare_17
	li $a0, 1
	j end_compare_17
	end_not_equals_17:
	li $a0, 0
	end_compare_17:
	beq $a0, $zero, else_86
	li $t1, 1
	j endif_86
else_86:
	li $t1, 0
endif_86:
	add $t0, $t0, $t1
	lw $t1, 0($sp)
	move $s2, $t1
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $ra, 4($sp)
	sw $s2, 8($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t1, 24($sp)
	sw $t1, 4($sp)
	lw $s2, 16($sp)
	jal CellularAutomaton_southwest
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	lw $ra, 4($sp)
	lw $s2, 8($sp)
	addi $sp, $sp, 12
	la $t1, str27
	loop_compare_18:
	lb $s5, 0($a0)
	lb $s6, 0($t1)
	addiu $a0, $a0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_18
	bnez $s5, loop_compare_18
	li $a0, 1
	j end_compare_18
	end_not_equals_18:
	li $a0, 0
	end_compare_18:
	beq $a0, $zero, else_87
	li $t1, 1
	j endif_87
else_87:
	li $t1, 0
endif_87:
	add $t0, $t0, $t1
	move $a0, $t0
	jr $ra
Main_cell_at_next_evolution:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_neighbors
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 3
	beq $a0, $t0, compare_55
	addi $a0, $zero, 0
	j end_compare_77
	compare_55:
	addi $a0, $zero, 1
	end_compare_77:
	beq $a0, $zero, else_88
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str28
	copy_93:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_93
	move $t0, $v0
	j endif_88
else_88:
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_neighbors
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	li $t0, 2
	beq $a0, $t0, compare_56
	addi $a0, $zero, 0
	j end_compare_78
	compare_56:
	addi $a0, $zero, 1
	end_compare_78:
	beq $a0, $zero, else_89
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 20($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	la $t0, str29
	loop_compare_19:
	lb $s5, 0($a0)
	lb $s6, 0($t0)
	addiu $a0, $a0, 1
	addiu $t0, $t0, 1
	bne $s5, $s6, end_not_equals_19
	bnez $s5, loop_compare_19
	li $a0, 1
	j end_compare_19
	end_not_equals_19:
	li $a0, 0
	end_compare_19:
	beq $a0, $zero, else_90
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str30
	copy_94:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_94
	move $t0, $v0
	j endif_90
else_90:
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str31
	copy_95:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_95
	move $t0, $v0
endif_90:
	j endif_89
else_89:
	li $a0, 2
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str32
	copy_96:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_96
	move $t0, $v0
endif_89:
endif_88:
	move $a0, $t0
	jr $ra
Main_evolve:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 0
	sw $t0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_num_cells
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str33
	copy_97:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_97
	move $t0, $v0
	sw $t0, 0($sp)
loop_3:
	lw $t0, 8($sp)
	lw $t1, 4($sp)
	slt $t0, $t0, $t1
	beq $t0, $zero, end_while_3
	lw $t0, 0($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 28($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 40($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_cell_at_next_evolution
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 4($sp)
	lw $s2, 12($sp)
	jal concat
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 8($sp)
	addi $t0, $t0, 1
	sw $t0, 8($sp)
	j loop_3
end_while_3:
	la $a0, StaticVoid
	lw $t0, 0($sp)
	lw $t1, 12($sp)
	sw $t0, 20($t1)
	lw $t0, 12($sp)
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_option:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 27
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str34
	copy_98:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_98
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str35
	copy_99:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_99
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 49
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str36
	copy_100:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_100
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 49
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str37
	copy_101:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_101
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 11
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str38
	copy_102:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_102
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 27
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str39
	copy_103:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_103
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 23
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str40
	copy_104:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_104
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str41
	copy_105:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_105
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str42
	copy_106:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_106
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 12
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str43
	copy_107:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_107
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 22
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str44
	copy_108:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_108
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 33
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str45
	copy_109:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_109
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 19
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str46
	copy_110:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_110
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 13
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str47
	copy_111:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_111
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 18
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str48
	copy_112:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_112
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 13
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str49
	copy_113:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_113
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str50
	copy_114:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_114
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str51
	copy_115:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_115
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 13
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str52
	copy_116:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_116
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str53
	copy_117:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_117
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str54
	copy_118:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_118
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 14
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str55
	copy_119:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_119
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str56
	copy_120:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_120
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_in_int
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str57
	copy_121:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_121
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	li $t1, 1
	beq $t0, $t1, compare_57
	addi $t0, $zero, 0
	j end_compare_79
	compare_57:
	addi $t0, $zero, 1
	end_compare_79:
	beq $t0, $zero, else_91
	li $a0, 21
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str58
	copy_122:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_122
	move $t0, $v0
	j endif_91
else_91:
	lw $t0, 0($sp)
	li $t1, 2
	beq $t0, $t1, compare_58
	addi $t0, $zero, 0
	j end_compare_80
	compare_58:
	addi $t0, $zero, 1
	end_compare_80:
	beq $t0, $zero, else_92
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str59
	copy_123:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_123
	move $t0, $v0
	j endif_92
else_92:
	lw $t0, 0($sp)
	li $t1, 3
	beq $t0, $t1, compare_59
	addi $t0, $zero, 0
	j end_compare_81
	compare_59:
	addi $t0, $zero, 1
	end_compare_81:
	beq $t0, $zero, else_93
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str60
	copy_124:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_124
	move $t0, $v0
	j endif_93
else_93:
	lw $t0, 0($sp)
	li $t1, 4
	beq $t0, $t1, compare_60
	addi $t0, $zero, 0
	j end_compare_82
	compare_60:
	addi $t0, $zero, 1
	end_compare_82:
	beq $t0, $zero, else_94
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str61
	copy_125:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_125
	move $t0, $v0
	j endif_94
else_94:
	lw $t0, 0($sp)
	li $t1, 5
	beq $t0, $t1, compare_61
	addi $t0, $zero, 0
	j end_compare_83
	compare_61:
	addi $t0, $zero, 1
	end_compare_83:
	beq $t0, $zero, else_95
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str62
	copy_126:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_126
	move $t0, $v0
	j endif_95
else_95:
	lw $t0, 0($sp)
	li $t1, 6
	beq $t0, $t1, compare_62
	addi $t0, $zero, 0
	j end_compare_84
	compare_62:
	addi $t0, $zero, 1
	end_compare_84:
	beq $t0, $zero, else_96
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str63
	copy_127:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_127
	move $t0, $v0
	j endif_96
else_96:
	lw $t0, 0($sp)
	li $t1, 7
	beq $t0, $t1, compare_63
	addi $t0, $zero, 0
	j end_compare_85
	compare_63:
	addi $t0, $zero, 1
	end_compare_85:
	beq $t0, $zero, else_97
	li $a0, 21
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str64
	copy_128:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_128
	move $t0, $v0
	j endif_97
else_97:
	lw $t0, 0($sp)
	li $t1, 8
	beq $t0, $t1, compare_64
	addi $t0, $zero, 0
	j end_compare_86
	compare_64:
	addi $t0, $zero, 1
	end_compare_86:
	beq $t0, $zero, else_98
	li $a0, 21
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str65
	copy_129:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_129
	move $t0, $v0
	j endif_98
else_98:
	lw $t0, 0($sp)
	li $t1, 9
	beq $t0, $t1, compare_65
	addi $t0, $zero, 0
	j end_compare_87
	compare_65:
	addi $t0, $zero, 1
	end_compare_87:
	beq $t0, $zero, else_99
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str66
	copy_130:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_130
	move $t0, $v0
	j endif_99
else_99:
	lw $t0, 0($sp)
	li $t1, 10
	beq $t0, $t1, compare_66
	addi $t0, $zero, 0
	j end_compare_88
	compare_66:
	addi $t0, $zero, 1
	end_compare_88:
	beq $t0, $zero, else_100
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str67
	copy_131:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_131
	move $t0, $v0
	j endif_100
else_100:
	lw $t0, 0($sp)
	li $t1, 11
	beq $t0, $t1, compare_67
	addi $t0, $zero, 0
	j end_compare_89
	compare_67:
	addi $t0, $zero, 1
	end_compare_89:
	beq $t0, $zero, else_101
	li $a0, 16
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str68
	copy_132:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_132
	move $t0, $v0
	j endif_101
else_101:
	lw $t0, 0($sp)
	li $t1, 12
	beq $t0, $t1, compare_68
	addi $t0, $zero, 0
	j end_compare_90
	compare_68:
	addi $t0, $zero, 1
	end_compare_90:
	beq $t0, $zero, else_102
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str69
	copy_133:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_133
	move $t0, $v0
	j endif_102
else_102:
	lw $t0, 0($sp)
	li $t1, 13
	beq $t0, $t1, compare_69
	addi $t0, $zero, 0
	j end_compare_91
	compare_69:
	addi $t0, $zero, 1
	end_compare_91:
	beq $t0, $zero, else_103
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str70
	copy_134:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_134
	move $t0, $v0
	j endif_103
else_103:
	lw $t0, 0($sp)
	li $t1, 14
	beq $t0, $t1, compare_70
	addi $t0, $zero, 0
	j end_compare_92
	compare_70:
	addi $t0, $zero, 1
	end_compare_92:
	beq $t0, $zero, else_104
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str71
	copy_135:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_135
	move $t0, $v0
	j endif_104
else_104:
	lw $t0, 0($sp)
	li $t1, 15
	beq $t0, $t1, compare_71
	addi $t0, $zero, 0
	j end_compare_93
	compare_71:
	addi $t0, $zero, 1
	end_compare_93:
	beq $t0, $zero, else_105
	li $a0, 22
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str72
	copy_136:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_136
	move $t0, $v0
	j endif_105
else_105:
	lw $t0, 0($sp)
	li $t1, 16
	beq $t0, $t1, compare_72
	addi $t0, $zero, 0
	j end_compare_94
	compare_72:
	addi $t0, $zero, 1
	end_compare_94:
	beq $t0, $zero, else_106
	li $a0, 22
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str73
	copy_137:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_137
	move $t0, $v0
	j endif_106
else_106:
	lw $t0, 0($sp)
	li $t1, 17
	beq $t0, $t1, compare_73
	addi $t0, $zero, 0
	j end_compare_95
	compare_73:
	addi $t0, $zero, 1
	end_compare_95:
	beq $t0, $zero, else_107
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str74
	copy_138:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_138
	move $t0, $v0
	j endif_107
else_107:
	lw $t0, 0($sp)
	li $t1, 18
	beq $t0, $t1, compare_74
	addi $t0, $zero, 0
	j end_compare_96
	compare_74:
	addi $t0, $zero, 1
	end_compare_96:
	beq $t0, $zero, else_108
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str75
	copy_139:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_139
	move $t0, $v0
	j endif_108
else_108:
	lw $t0, 0($sp)
	li $t1, 19
	beq $t0, $t1, compare_75
	addi $t0, $zero, 0
	j end_compare_97
	compare_75:
	addi $t0, $zero, 1
	end_compare_97:
	beq $t0, $zero, else_109
	li $a0, 17
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str76
	copy_140:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_140
	move $t0, $v0
	j endif_109
else_109:
	lw $t0, 0($sp)
	li $t1, 20
	beq $t0, $t1, compare_76
	addi $t0, $zero, 0
	j end_compare_98
	compare_76:
	addi $t0, $zero, 1
	end_compare_98:
	beq $t0, $zero, else_110
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str77
	copy_141:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_141
	move $t0, $v0
	j endif_110
else_110:
	lw $t0, 0($sp)
	li $t1, 21
	beq $t0, $t1, compare_77
	addi $t0, $zero, 0
	j end_compare_99
	compare_77:
	addi $t0, $zero, 1
	end_compare_99:
	beq $t0, $zero, else_111
	li $a0, 29
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str78
	copy_142:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_142
	move $t0, $v0
	j endif_111
else_111:
	li $a0, 26
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str79
	copy_143:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_143
	move $t0, $v0
endif_111:
endif_110:
endif_109:
endif_108:
endif_107:
endif_106:
endif_105:
endif_104:
endif_103:
endif_102:
endif_101:
endif_100:
endif_99:
endif_98:
endif_97:
endif_96:
endif_95:
endif_94:
endif_93:
endif_92:
endif_91:
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_prompt:
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str84
	copy_144:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_144
	move $t0, $v0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 56
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str80
	copy_145:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_145
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 50
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str81
	copy_146:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_146
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_in_string
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 3
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str82
	copy_147:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_147
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 0($sp)
	la $t1, str83
	loop_compare_20:
	lb $s5, 0($t0)
	lb $s6, 0($t1)
	addiu $t0, $t0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_20
	bnez $s5, loop_compare_20
	li $t0, 1
	j end_compare_20
	end_not_equals_20:
	li $t0, 0
	end_compare_20:
	beq $t0, $zero, else_112
	li $t0, 0
	j endif_112
else_112:
	li $t0, 1
endif_112:
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_prompt2:
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str89
	copy_148:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_148
	move $t0, $v0
	sw $t0, 0($sp)
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 5
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str85
	copy_149:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_149
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 50
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str86
	copy_150:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_150
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 50
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str87
	copy_151:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_151
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal CellularAutomaton_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 4($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal CellularAutomaton_in_string
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	lw $t0, 0($sp)
	la $t1, str88
	loop_compare_21:
	lb $s5, 0($t0)
	lb $s6, 0($t1)
	addiu $t0, $t0, 1
	addiu $t1, $t1, 1
	bne $s5, $s6, end_not_equals_21
	bnez $s5, loop_compare_21
	li $t0, 1
	j end_compare_21
	end_not_equals_21:
	li $t0, 0
	end_compare_21:
	beq $t0, $zero, else_113
	li $t0, 1
	j endif_113
else_113:
	li $t0, 0
endif_113:
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
Main_main:
	#Region Let
	addi $sp, $sp, -4
	li $t0, 1
	sw $t0, 0($sp)
	#Region Let
	addi $sp, $sp, -4
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str92
	copy_152:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_152
	move $t0, $v0
	sw $t0, 0($sp)
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 31
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str90
	copy_153:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_153
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Main_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	li $a0, 49
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str91
	copy_154:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_154
	move $t0, $v0
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	jal Main_out_string
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
loop_4:
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal Main_prompt2
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	beq $a0, $zero, end_while_4
	li $t0, 1
	sw $t0, 4($sp)
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal Main_option
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	sw $a0, 0($sp)
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	jal __init_CellularAutomaton__
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	move $t0, $a0
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -8
	sw $s2, 0($sp)
	lw $t0, 16($sp)
	sw $t0, 4($sp)
	lw $s2, 12($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 44($t0)
	jal $t0
	addi $sp, $sp, 8
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	sw $a0, 24($t0)
	lw $t0, 8($sp)
	lw $t0, 24($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 48($t0)
	jal $t0
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
loop_5:
	lw $t0, 4($sp)
	beq $t0, $zero, end_while_5
	lw $t0, 8($sp)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	jal Main_prompt
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	beq $a0, $zero, else_114
	lw $t0, 8($sp)
	lw $t0, 24($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 100($t0)
	jal $t0
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	lw $t0, 8($sp)
	lw $t0, 24($t0)
	move $s2, $t0
	addi $sp, $sp, -8
	sw $ra, 0($sp)
	sw $s2, 4($sp)
	addi $sp, $sp, -4
	sw $s2, 0($sp)
	lw $s2, 8($sp)
	move $t0, $s2
	lw $t0, 4($t0)
	lw $t0, 48($t0)
	jal $t0
	addi $sp, $sp, 4
	lw $ra, 0($sp)
	lw $s2, 4($sp)
	addi $sp, $sp, 8
	j endif_114
else_114:
	li $t0, 0
	sw $t0, 4($sp)
	move $a0, $t0
endif_114:
	j loop_5
end_while_5:
	la $a0, StaticVoid
	j loop_4
end_while_4:
	la $a0, StaticVoid
	lw $t0, 8($sp)
	addi $sp, $sp, 4
	#End Region Let
	addi $sp, $sp, 4
	#End Region Let
	move $a0, $t0
	jr $ra
__init_Board__:
	li $a0, 20
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Board
	sw $t0, 0($s1)
	la $t0, StaticBoard
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 0
	sw $t0, 8($s1)
	li $t0, 0
	sw $t0, 12($s1)
	li $t0, 0
	sw $t0, 16($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_CellularAutomaton__:
	li $a0, 24
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, CellularAutomaton
	sw $t0, 0($s1)
	la $t0, StaticCellularAutomaton
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 0
	sw $t0, 8($s1)
	li $t0, 0
	sw $t0, 12($s1)
	li $t0, 0
	sw $t0, 16($s1)
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str2
	copy_155:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_155
	move $t0, $v0
	sw $t0, 20($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_Main__:
	li $a0, 28
	li $v0, 9
	syscall
	move $s1, $v0
	la $t0, Main
	sw $t0, 0($s1)
	la $t0, StaticMain
	sw $t0, 4($s1)
	addi $sp, $sp, -4
	sw $s1, 0($sp)
	li $t0, 0
	sw $t0, 8($s1)
	li $t0, 0
	sw $t0, 12($s1)
	li $t0, 0
	sw $t0, 16($s1)
	li $a0, 1
	li $v0, 9
	syscall
	move $s4, $v0
	la $s3, str2
	copy_156:
	lb $t0, 0($s3)
	sb $t0, 0($s4)
	addiu $s3, $s3, 1
	addiu $s4, $s4, 1
	bnez $t0, copy_156
	move $t0, $v0
	sw $t0, 20($s1)
	la $a0, StaticVoid
	sw $a0, 24($s1)
	addi $sp, $sp, 4
	move $a0, $s1
	jr $ra
__init_IO__:
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, StaticIO
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
Board_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
Board_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
Board_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
Board_in_string:
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
Board_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
Board_copy:
	jr $ra
Board_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
CellularAutomaton_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
CellularAutomaton_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
CellularAutomaton_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
CellularAutomaton_in_string:
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
CellularAutomaton_type_name:
	lw $t0, 0($sp)
	lw $t1, 0($t0)
	move $a0, $t1
	jr $ra
CellularAutomaton_copy:
	jr $ra
CellularAutomaton_abort:
	la $a0, abort
	li $v0, 4
	syscall
	lw $t0, 0($sp)
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	li $v0, 10
	syscall
Main_out_string:
	lw $a0, 4($sp)
	li $v0, 4
	syscall
	lw $a0, 0($sp)
	jr $ra
Main_out_int:
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 0($sp)
	jr $ra
Main_in_int:
	li $v0, 5
	syscall
	move $a0, $v0
	jr $ra
Main_in_string:
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
