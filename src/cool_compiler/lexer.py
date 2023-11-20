from .sly import Lexer


class CoolLexer(Lexer):
    # all tokens
    tokens = {
        "CASE",
        "CLASS",
        "ELSE",
        "ESAC",
        "FALSE",
        "FI",
        "IF",
        "INHERITS",
        "IN",
        "ISVOID",
        "LET",
        "NEW",
        "NOT",
        "LOOP",
        "OF",
        "POOL",
        "SELF",
        "SELF_TYPE",
        "THEN",
        "TRUE",
        "WHILE",
        "ID",
        "INTEGER",
        "STRING"
    }

    # ignore
    ignore = r' \t'
    ignore_newline = r'\n+'

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # error
    def error(self, t):
        print(f'Illegal character \'{t.value[0]}\'')
        self.index += 1

    # keywords and special identifiers
    CASE = r'case'
    CLASS = r'class'
    ELSE = r'else'
    ESAC = r'esac'
    FALSE = r'false'
    FI = r'fi'
    IF = r'if'
    INHERITS = r'inherits'
    IN = r'in'
    ISVOID = r'isvoid'
    LET = r'let'
    NEW = r'new'
    NOT = r'not'
    LOOP = r'loop'
    OF = r'of'
    POOL = r'pool'
    SELF = r'self'
    SELF_TYPE = r'SELF_TYPE'
    THEN = r'then'
    TRUE = r'true'
    WHILE = r'while'

    # identifier and literals
    ID = r'[a-zA-Z_][a-zA-Z_\d]*'
    INTEGER = r'(0|-?[1-9]\d*)'
    STRING = r'"([^"\\\n]|\\[\n\S])*"'

    # string literal normalization
    def STRING(self, t):
        t.value = t.value[1:-1]\
            .replace('\\n', '\n')\
            .replace('\\\n', '\n')\
            .replace('\\b', '\b')\
            .replace('\\t', '\t')\
            .replace('\\f', '\f')\
            .replace('\\', '')
