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
        "STRING",
        "ASSIGN",
        "COLON",
        "SEMICOLON",
        "CASE_THEN",
        "COMMA",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "SUM",
        "SUB",
        "TIMES",
        "DIV",
        "GE",
        "LE",
        "GT",
        "LT",
        "EQ"
    }

    # ignore
    @_(r'\s+')
    def ignore_whitespace(self, t):
        self.lineno += t.value.count('\n')

    @_(r'--')
    def ignore_single_comment(self):
        next_newline_index = self.text.find('\n', self.index)

        if (next_newline_index == -1):
            self.index = len(self.text)
        else:
            self.index = next_newline_index

    @_(r'\(\*')
    def ignore_multiline_comment(self):
        balance = 1
        l, r = r'\(\*', r'\*\)'

        while len(self.text) - self.index > 1:
            s = self.text[self.index: self.index+2]

            if s == r:
                balance -= 1
                self.index += 2
            elif s == l:
                balance += 1
                self.index += 2
            else:
                self.index += 1

            if balance == 0:
                return

        self.index = len(self.text)

    # error
    def error(self, t):
        print(
            f'cool lexer error: illegal character \'{t.value[0]}\' at (line {self.lineno}, column {self.index}).')
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

    # operators and other literals
    ASSIGN = r'<-'
    COLON = r':'
    SEMICOLON = r';'
    CASE_THEN = r'=>'
    COMMA = ','

    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'

    SUM = r'\+'
    SUB = r'-'
    TIMES = r'\*'
    DIV = r'/'

    GE = r'>='
    LE = r'<='
    GT = r'>'
    LT = r'<'
    EQ = r'='
