

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

class Data:
    def __init__(self, name, type, *args):
        self.name = name
        self.type = type
        self.args = args

    def __str__(self):
        return f"{self.name}:  {self.type} {', '.join(self.args)}"
    
    def __repr__(self):
        return str(self)

class Section:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f".{self.name}"
    
    def __repr__(self):
        return str(self)

NULL = "null"

TRUE = "true"

FALSE = "false"

NEWLINE = "\\n"

INDENT = "    "

COMMENT = "# {comment}\n"
