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
