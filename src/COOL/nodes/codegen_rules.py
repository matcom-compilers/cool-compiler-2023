from enum import Enum


# TODO: calculate size of data
# TODO: all data will be given in $t0 ?
# NOTE: the strings cant be generated in .text section

def concat(script: str, rule: str, indent: bool = True, newline: bool = True):
    return script + (NEWLINE if newline else "") + (INDENT if indent else "") + rule

def string_length(string: str):
    return len(string) + 1

NULL = "null"

TRUE = "true"

FALSE = "false"

NEWLINE = "\n"

INDENT = "    "

COMMENT = "# {comment}\n"

class Types(Enum):
    INT = ".word"
    BOOL = ".byte"
    STRING = ".asciiz"

DATA_SECTION =\
"""
# Data section
.data
newline:  .asciiz  "\n"
null:     .word    0
true:     .byte    1
false:    .byte    0
"""

SET_VAR_IN_DATA_SECTION=\
"""    {owner}_{var_name}: {type} {value}
"""

TEXT_SECTION =\
"""\n
# Text section
.text

.globl main
main:\n
"""

REQUEST_MEMORY=\
"""
    # Request memory
    li $a0, {memory}
    li $v0, 9
    syscall
    mv ${register}, $v0
"""

STORE_DATA=\
"""
    # Store data
    li $t0, {data}
    sw $t0, {offset}(${register})
"""

LOAD_DATA=\
"""
    # Load data
    lw $t0, {offset}(${register})
"""

CREATE_CLASS=\
"""
# Create class {class_name}
{class_name}:
{request_memory}

{attributes}
"""

CREATE_FUNCTION=\
"""
# Create function {function_name}
{function_name}:
"""

STORE_VALUES_IN_REGISTER=\
"""    li ${register}, {value}
"""

STORE_VALUES_IN_VARS=\
"""    sw ${register}, {offset}(${fp})
"""

ARITMETIC=\
"""    {operation} ${register}, ${register1}, ${register2}
"""

UNARY_ARITMETIC=\
"""    {operation} ${register}, ${register1}
"""

EXIT=\
"""
    # Exit program
    li $v0, 10
    syscall
"""


"""
booleans:
    - true: 1 / false: 0
    - mempry = 1 byte

integers:
    - dan su propio valor
    - memory = 4 bytes

strings:
    - se deben guardar en el heap? o data section?
    - every char is 1 byte

id:
    - direccion de memoria de la variable?

not:
    - UNARY_ARITMETIC

method:
    - label de la funcion con nombre de la clase y el metodo

new:
    - go to the class label
    - return the address of the object





"""
