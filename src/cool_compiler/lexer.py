from .sly import Lexer


def insensitive(word):
    return ''.join(
        [f'[{ch}{ch.upper()}]' for ch in word.lower()]
    )


class CoolLexer(Lexer):
    # all tokens
    tokens = {
        'CASE',
        'CLASS',
        'ELSE',
        'ESAC',
        'FI',
        'IF',
        'INHERITS',
        'IN',
        'ISVOID',
        'LET',
        'NEW',
        'NOT',
        'LOOP',
        'OF',
        'POOL',
        'THEN',
        'WHILE',

        'FALSE',
        'TRUE',

        'SELF',
        'SELF_TYPE',

        'ID',
        'INTEGER',
        'STRING',

        'ASSIGN',
        'COLON',
        'SEMICOLON',
        'CASE_THEN',
        'COMMA',
        'AT',
        'DOT',
        'NEG',

        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',

        'SUM',
        'SUB',
        'TIMES',
        'DIV',

        'GE',
        'LE',
        'GT',
        'LT',
        'EQ'
    }

    # ignored
    @_(r'\s+')  # type: ignore
    def ignore_whitespace(self, t):
        self.lineno += t.value.count('\n')

    @_(r'--')  # type: ignore
    def ignore_single_comment(self, _):
        next_newline_index = self.text.find('\n', self.index)

        if (next_newline_index == -1):
            self.index = len(self.text)
        else:
            self.index = next_newline_index

    @_(r'\(\*')  # type: ignore
    def ignore_multiline_comment(self, _):
        balance = 1
        l, r = '(*', '*)'

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
    CASE = insensitive('case')
    CLASS = insensitive('class')
    ELSE = insensitive('else')
    ESAC = insensitive('esac')
    FI = insensitive('fi')
    IF = insensitive('if')
    INHERITS = insensitive('inherits')
    IN = insensitive('in')
    ISVOID = insensitive('isvoid')
    LET = insensitive('let')
    NEW = insensitive('new')
    NOT = insensitive('not')
    LOOP = insensitive('loop')
    OF = insensitive('of')
    POOL = insensitive('pool')
    THEN = insensitive('then')
    WHILE = insensitive('while')

    FALSE = 'false'
    TRUE = 'true'

    SELF = 'self'
    SELF_TYPE = 'SELF_TYPE'

    # identifier and literals
    ID = r'[a-zA-Z_][a-zA-Z_\d]*'

    @_(r'\d+')  # type: ignore
    def INTEGER(self, t):
        i = 0
        while t.value[i] == '0':
            i += 1

        t.value = t.value[i:] if i < len(t.value) else '0'
        return t

    @_(r'"([^\n"\\]|\\(\n|[^\n]))*"')  # type: ignore
    def STRING(self, t):
        chars = []
        escaping = False

        for ch in t.value[1:-1]:
            if escaping:
                if ch == 'n':
                    chars.append('\n')
                elif ch == 'b':
                    chars.append('\b')
                elif ch == 't':
                    chars.append('\t')
                elif ch == 'f':
                    chars.append('\f')
                else:
                    # if correct multiline string literal, '\n' char is added here
                    chars.append(ch)

                escaping = False

            elif ch == '\\':
                escaping = True
            else:
                chars.append(ch)

        t.value = ''.join(chars)
        return t

    # operators and other literals
    ASSIGN = r'<-'
    COLON = r':'
    SEMICOLON = r';'
    CASE_THEN = r'=>'
    COMMA = r','
    AT = r'@'
    DOT = r'\.'
    NEG = r'~'

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
