from enum import Enum


def concat(script: str, rule: str, indent: bool = True, newline: bool = True):
    return script + (NEWLINE if newline else "") + (INDENT if indent else "") + rule

NEWLINE = "\n"

INDENT = "    "

COMMENT = "# {comment}\n"

class TYPES(Enum):
    INT = ".word"
    BOOL = ".byte"
    STRING = ".asciiz"

DATA_SECTION =\
"""
# Data section
.data
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

CREATE_CLASS=\
"""
# Create class {class_name}
{class_name}:
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



"""
class:
    - variables en data section con nombre {class}_{variable}
    - function en text section con nombre {class}_{function}
    - como seria para guardar las variables correspondientes a las instancias de la clase?

atribute:
    - variable en data section con nombre {class}_{variable}
    - tienen un valor por defecto
    - deberia haber una funcion que se encargue de asignarle el valor inicial?
    porque si lo saca de un expr no se puede hacer en data section

method:
    - variables en data section con nombre {class}_{method}_{variable}
    - function en text section con nombre {class}_{method}
    - tiene un return que sería el valor de la ultima expresion

jumps:
    - se puede crear un label jump con una serie de if por cada metodo 
    y una variable para el metodo al que se va a saltar
    - se pueden crear variables en data section con la direccion de memoria de cada metodo



"""

