# .data
# input_buffer:   .space  1024    # Espacio para almacenar la cadena de entrada
# prompt:         .asciiz "Ingrese una cadena: "

# .text
# main:
#     # Imprimir mensaje para solicitar la entrada
#     li $v0, 4
#     la $a0, prompt
#     syscall

#     # Leer la cadena de entrada
#     li $v0, 8
#     la $a0, input_buffer
#     li $a1, 1024
#     syscall

#     # Imprimir la cadena de entrada
#     li $v0, 4
#     la $a0, input_buffer
#     syscall

#     # Terminar el programa
#     li $v0, 10
#     syscall


.data
input_buffer:   .space  1024    # Espacio para almacenar la cadena de entrada
prompt:         .asciiz "Ingrese una cadena: "

.text
main:
    # Imprimir mensaje para solicitar la entrada
    li $v0, 4
    la $a0, prompt
    syscall

    # Leer la cadena de entrada
    li $v0, 8
    la $a0, input_buffer
    li $a1, 1024
    syscall

    # Imprimir la cadena de entrada
    li $v0, 4
    la $a0, input_buffer
    syscall

    # Terminar el programa
    li $v0, 10
    syscall

