from sly import Lexer


class CoolLexer(Lexer):
    tokens = {
        "NUMBER",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "LESS",
        "LESSEQUAL",
        "EQUAL",
        "NOT",
        "BITWISE",
        "CLASS",
        "INHERITS",
        "ASSIGN",
        "INT",
        "STRING",
        "BOOL",
        "TRUE",
        "FALSE",
        "TYPE",
        "ID",
    }

    literals = {"(", ")", "{", "}", ";", ":"}
    
    ignore = " \t"
    ignore_comment = r'--.*'
    ignore_comment_paren = r'\(\*.*\*\)'
    
    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    LESS = r"<"
    LESSEQUAL = r"<="
    EQUAL = r"="
    NOT = r"not"
    BITWISE= r"~"
    CLASS = r"class"
    INHERITS = r"inherits"
    ASSIGN = r"<-"
    INT = r"Int"
    STRING = r"String"
    BOOL = r"Bool"
    TRUE = r"true"
    FALSE = r"false"
    TYPE = r"[A-Z][a-zA-Z0-9_]*"
    ID = r"[a-z][a-zA-Z0-9_]*"

