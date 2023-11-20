from sly import Lexer as Lex


class Lexer(Lex):
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
        "LPAREN",
        "RPAREN",
        "ID",
        "TYPE",
        "CLASS",
        "INHERITS",
        "ASSIGN",
        "INT",
        "STRING",
        "BOOL",
        "TRUE",
        "FALSE",
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
    LPAREN = r"\("
    RPAREN = r"\)"
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    TYPE = r"[A-Z][a-zA-Z0-9_]*"
    CLASS = r"class"
    INHERITS = r"inherits"
    ASSIGN = r"<-"
    INT = r"Int"
    STRING = r"String"
    BOOL = r"Bool"
    TRUE = r"true"
    FALSE = r"false"
