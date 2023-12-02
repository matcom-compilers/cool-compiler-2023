from ply import lex
from sympy import true
from errors import LexicographicError
from utils import tokens, keywords, literals


class CoolLexer:
    def __init__(self):
        self.keywords = keywords
        self.tokens = tokens
        self.literals = literals

        self.states = (('comment', 'exclusive'), ('string', 'exclusive'))

        self.errors = []

        self.lexer = lex.lex(module=self)
        self.lexer.col = 1
        self.lexer.lineno = 1
        self.lexer.linestart = 0


    def compute_column(self, t):
        t.column = t.lexpos - t.lexer.linestart + 1


    def tokenize(self, data):
        self._lexer.input(data)
        while True:
            token = self._lexer.token()
            if not token:
                break
            yield token

    # #
    
    def t_AT(self, t):
        r'@'
        self.compute_column(t)
        return t

    def t_COLON(self, t):
        r':'
        self.compute_column(t)
        return t
    
    def t_SEMICOLON(self, t):
        r';'
        self.compute_column(t)
        return t

    def t_COMMA(self, t):
        r','
        self.compute_column(t)
        return t

    def t_DOT(self, t):
        r'\.'
        self.compute_column(t)
        return t

    def t_LPAREN(self, t):
        r'\('
        self.compute_column(t)
        return t

    def t_RPAREN(self, t):
        r'\)'
        self.compute_column(t)
        return t
    
    def t_LBRACE(self, t):
        r'\{'
        self.compute_column(t)
        return t

    def t_RBRACE(self, t):
        r'\}'
        self.compute_column(t)
        return t
        
    def t_PLUS(self, t):
        r'\+'
        self.compute_column(t)
        return t

    def t_MINUS(self, t):
        r'\-'
        self.compute_column(t)
        return t

    def t_STAR(self, t):
        r'\*'
        self.compute_column(t)
        return t

    def t_DIV(self, t):
        r'/'
        self.compute_column(t)
        return t

    def t_NOT(self, t):
        r"\~"
        self.compute_column(t)
        return t    
    
    def t_EQUAL(self, t):
        r'='
        self.compute_column(t)
        return t

    def t_LESS(self, t):
        r'<'
        self.compute_column(t)
        return t

    def t_LESSEQ(self, t):
        r'\<='
        self.compute_column(t)
        return t

    def t_ASSIGN(self, t):
        r'\<-'
        self.compute_column(t)
        return t
    
    def t_ARROW(self, t):
        r'\=>'
        self.compute_column(t)
        return t
    
    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value.lower(), 'TYPE')
        self.compute_column(t)
        return t
    
    def t_ID(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value.lower(), 'ID')
        self.compute_column(t)
        return t
    
    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        self.compute_column(t)
        return t

    # Comments #

    def t_one_line_comment(self, t):
        r'--.*($|\n)'
        self.compute_column(t)
        t.lexer.lineno += 1
        t.lexer.linestart = t.lexer.lexpos
    
    def t_multi_line_comment(self, t):
        r'\(\*'
        self.compute_column(t)
        t.lexer.level = 1
        t.lexer.begin('comments')

    def t_comments_open(self, t):
        r'\(\*'
        self.compute_column(t)
        t.lexer.level += 1

    def t_comments_close(self, t):
        r'\*\)'
        self.compute_column(t)
        t.lexer.level -= 1
        if t.lexer.level == 0:
            t.lexer.begin('INITIAL')

    
    def t_comments_error(self, t):
        t.lexer.skip(1)

    def t_comments_eof(self, t):
        self.compute_column(t)
        if t.lexer.level > 0:
            self.eof_comment = True
            
    def t_comments_error(self, t):
        t.lexer.skip(1)

    def t_comments_eof(self, t):
        self.compute_column(t)
        if t.lexer.level > 0:
            self.errors.append(LexicographicError(message=
                'EOF in comment', line=t.lineno, column=t.column))

    ## 

    # Strings #

    def t_strings(self, t):
        r'\''
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string = ''
        t.lexer.backslash = False
        t.lexer.begin('string')

    def t_string_end(self, t):
        r'(?<!\\)"'
        self.compute_column(t)

        if t.lexer.backslash:
            t.lexer.string += '\''
            t.lexer.backslash = False
        else:
            t.value = t.lexer.string
            t.type = 'STRING'
            t.lexer.begin('INITIAL')
        
            return t
        
    
    def t_strings_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.compute_column(t)

        t.lexer.linestart = t.lexer.lexpos

        if not t.lexer.backslash:
            self.errors.append(LexicographicError(message=
                'Undeterminated string constant', line=t.lineno, column=t.column))
            t.lexer.begin('INITIAL')

    def t_strings_nill(self, t):
        r'\0'
        self.compute_column(t)
        self.errors.append(LexicographicError(message=
            'Null caracter in string', line=t.lineno, column=t.column))

    def t_strings_consume(self, t):
        r'[^\n]'

        if t.lexer.backslash:
            if t.value == 'b':
                t.lexer.string += '\b'
            elif t.value == 't':
                t.lexer.string += '\t'
            elif t.value == 'f':
                t.lexer.string += '\f'
            elif t.value == 'n':
                t.lexer.string += '\n'
            elif t.value == '\\':
                t.lexer.string += '\\'
            else:
                t.lexer.string += t.value

            t.lexer.backslash = False
        else:
            if t.value != '\\':
                t.lexer.string += t.value
            else:
                t.lexer.backslash = True

    def t_strings_eof(self, t):
        self.compute_column(t)
        self.errors.append(LexicographicError(message=
            'EOF in string constant', line=t.lineno, column=t.column))

    ##

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos

    def t_error(self, t):
        self.compute_column(t)
        self.errors.append(LexicographicError(message=
            f'ERROR \'{t.value[0]}\'', line=t.lineno, column=t.column))
        t.lexer.skip(1)
