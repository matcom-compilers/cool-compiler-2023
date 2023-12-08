.data
str: .asciiz "Hello, World!"
subStr: .asciiz "World"

.text
.globl main

main:
    # Puntero al inicio de la cadena
    la $s0, str

    # Puntero al inicio del substring
    la $s1, subStr

    # Longitud del substring
    li $t0, 5

loop:
    lb $t1, 0($s0)      # Cargar un byte de la cadena
    lb $t2, 0($s1)      # Cargar un byte del substring

    beqz $t1, not_found # Si llegamos al final de la cadena, no se encontró el substring
    beqz $t2, found     # Si llegamos al final del substring, se encontró el substring

    bne $t1, $t2, next  # Si los bytes no son iguales, pasar al siguiente byte de la cadena

    addiu $s0, $s0, 1   # Avanzar al siguiente byte de la cadena
    addiu $s1, $s1, 1   # Avanzar al siguiente byte del substring
    addiu $t0, $t0, -1  # Decrementar la longitud restante del substring

    bnez $t0, loop      # Si aún hay bytes restantes en el substring, continuar la búsqueda

found:
    # El substring se encontró en la cadena
    # Aquí puedes agregar el código que deseas ejecutar cuando se encuentra el substring
    j end

not_found:
    # El substring no se encontró en la cadena
    # Aquí puedes agregar el código que deseas ejecutar cuando no se encuentra el substring

end:
    # Salir del programa
    li $v0, 10
    syscall