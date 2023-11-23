from sly import Lexer
from error import Error


# TODO: Set lexer error
# TODO: INT, BOOL and others are types?
class CoolLexer(Lexer):
    tokens = {
        # Symbols
        "NUMBER", "STRING", "TYPE", "ID",
        # Arithmetic Operators
        "PLUS", "MINUS", "TIMES", "DIVIDE", "LESS", "LESSEQUAL", "EQUAL", "NOT", "BITWISE", "ASSIGN", "CASE_ARROW",
        # Reserved words
        "CLASS", "INHERITS", "IF", "THEN", "ELSE", "FI", "WHILE", "LOOP", "POOL", "LET", "IN", "CASE", "OF", "ESAC", "NEW", "ISVOID", "TRUE", "FALSE",
    }
    literals = {"(", ")", "{", "}", ";", ":", ",", ".", "@"}
    
    # Comments
    ignore = " \t"
    ignore_comment = r'--.*'
    @_(r'\(\*(.|\n)*?\*\)')
    def ignore_comment_multiline(self, t):
        self.lineno += t.value.count("\n")
    
    # Newline
    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    # Arithmetic Operators
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    ASSIGN = r"<-"
    LESSEQUAL = r"<="
    LESS = r"<"
    CASE_ARROW = r"=>"
    EQUAL = r"="
    NOT = r"not"
    BITWISE= r"~"

    # Reserved words
    CLASS = r"class"
    INHERITS = r"inherits"
    IF = r"if"
    THEN = r"then"
    ELSE = r"else"
    FI = r"fi"
    WHILE = r"while"
    LOOP = r"loop"
    POOL = r"pool"
    LET = r"let"
    IN = r"in"
    CASE = r"case"
    OF = r"of"
    ESAC = r"esac"
    NEW = r"new"
    ISVOID = r"isvoid"
    TRUE = r"true"
    FALSE = r"false"
    
    # Symbols
    TYPE = r"[A-Z][a-zA-Z0-9_]*"
    ID = r"[a-z][a-zA-Z0-9_]*"

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = str(t.value).strip('\"')
        return t

    # Error handling rule
    def error(self, t):
        if t:
            Error.error(self.lineno, self.index, "LexicographicError", f"Error \"{t.value[0]}\"")
            self.index += 1
        else:
            print('HERE')
