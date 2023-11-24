from coollexer.sly_lexer import Lexer
from sly.lex import Token as SlyToken

from tokens import Token
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
        'CLASS', "INHERITS", "IF", "THEN", "ELSE", "FI", "WHILE", "LOOP", "POOL", "LET", "IN", "CASE", "OF", "ESAC", "NEW", "ISVOID", "TRUE", "FALSE",
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

    # Symbols
    TYPE = r'[A-Z][a-zA-Z0-9_]*'
    ID = r'[a-z][a-zA-Z0-9_]*'

    # Reserved words
    _class = r'(?i)class'
    _inherits = r'(?i)inherits'
    _if = r'(?i)if'
    _then = r'(?i)then'
    _else = r'(?i)else'
    _fi = r'(?i)fi'
    _while = r'(?i)while'
    _loop = r'(?i)loop'
    _pool = r'(?i)pool'
    _let = r'(?i)let'
    _in = r'(?i)in'
    _case = r'(?i)case'
    _of = r'(?i)of'
    _esac = r'(?i)esac'
    _new = r'(?i)new'
    _isvoid = r'(?i)isvoid'
    _true = r'(?i)true'
    _false = r'(?i)false'

    ID[_class] = "CLASS"
    ID[_inherits] = "INHERITS"
    ID[_if] = "IF"
    ID[_then] = "THEN"
    ID[_else] = "ELSE"
    ID[_fi] = "FI"
    ID[_while] = "WHILE"
    ID[_loop] = "LOOP"
    ID[_pool] = "POOL"
    ID[_let] = "LET"
    ID[_in] = "IN"
    ID[_case] = "CASE"
    ID[_of] = "OF"
    ID[_esac] = "ESAC"
    ID[_new] = "NEW"
    ID[_isvoid] = "ISVOID"
    ID[_true] = "TRUE"
    ID[_false] = "FALSE"

    TYPE[_class] = "CLASS"
    TYPE[_inherits] = "INHERITS"
    TYPE[_if] = "IF"
    TYPE[_then] = "THEN"
    TYPE[_else] = "ELSE"
    TYPE[_fi] = "FI"
    TYPE[_while] = "WHILE"
    TYPE[_loop] = "LOOP"
    TYPE[_pool] = "POOL"
    TYPE[_let] = "LET"
    TYPE[_in] = "IN"
    TYPE[_case] = "CASE"
    TYPE[_of] = "OF"
    TYPE[_esac] = "ESAC"
    TYPE[_new] = "NEW"
    TYPE[_isvoid] = "ISVOID"
    TYPE[_true] = "TRUE"
    TYPE[_false] = "FALSE"

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
        new_token = Token()
        new_token.column = self.find_column(text, token)
        new_token.type = token.type
        new_token.value = token.value
        new_token.lineno = token.lineno
        new_token.index = token.index
        new_token.end = token.end
        return new_token

    def tokenize(self, text: str):
        return (self.generate_token(t, text) for t in super().tokenize(text))
