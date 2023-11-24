from sly import Lexer
from sly.lex import Token as SlyToken

from coollexer.tokens import LexToken
from error import Error


# TODO: Set lexer error
# TODO: INT, BOOL and others are types?
# FIX: comments and string to accept everything
# TODO: test lexer commets, mised, string
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
    
    # FIX: string regex
    # "((?:[^"\\]|\\.)*?)"
    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = str(t.value).strip('\"')
        return t

    # FIX: detect missing " and *) at the end
    # Error handling rule
    def error(self, t: SlyToken):
        self.index += 1
        index = self.find_column(self.text, t)
        Error.error(
            line=self.lineno,
            column=index,
            error_type="LexicographicError",
            message=f"Error \"{t.value[0]}\""
        )
    
    def find_column(self, text: str, token: SlyToken):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr)
        return column

    def generate_token(self, token: SlyToken, text: str):
        new_token = LexToken()
        new_token.column = self.find_column(text, token)
        new_token.type = token.type
        new_token.value = token.value
        new_token.lineno = token.lineno
        new_token.index = token.index
        new_token.end = token.end
        return new_token

    def tokenize(self, text: str):
        return (self.generate_token(t, text) for t in super().tokenize(text))
