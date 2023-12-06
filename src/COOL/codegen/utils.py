

class Instruction:
    def __init__(self, opcode, *args):
        self.opcode = opcode
        self.args = args

    def __str__(self):
        return f"{INDENT}{self.opcode} {' '.join(map(str, self.args))}"
    
    def __repr__(self):
        return str(self)


class Label:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}:"
    
    def __repr__(self):
        return str(self)


class Comment:
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return f"{INDENT}{COMMENT.format(comment=self.comment)}"
    
    def __repr__(self):
        return str(self)


NULL = "null"

TRUE = "true"

FALSE = "false"

NEWLINE = "\\n"

INDENT = "    "

COMMENT = "# {comment}\n"


DATA_SECTION =\
f"""
# Data section
.data
newline:  .asciiz  "{NEWLINE}"
{NULL}:     .word    0
{TRUE}:     .byte    1
{FALSE}:    .byte    0
"""

TEXT_SECTION =\
"""\n
# Text section
.text

.globl main
main:
    jal Main
    jal Main_main

    j exit

"""
