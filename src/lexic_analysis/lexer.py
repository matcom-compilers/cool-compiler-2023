import ply.lex as lex
import ply.yacc as yacc
from semantic_analysis.ast_ import Id, Type, String, Int, Bool

class Lexer(object):
    
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, errorlog=yacc.NullLogger(), **kwargs)
        self.lexer.errors = []
    
    keywords = {
        'not': 'NOT',
        'class': 'CLASS',
        'inherits': 'INHERITS',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'fi': 'FI',
        'while': 'WHILE',
        'loop': 'LOOP',
        'pool': 'POOL',
        'let': 'LET',
        'in': 'IN',
        'case': 'CASE',
        'of': 'OF',
        'new': 'NEW',
        'esac': 'ESAC',
        'isvoid': 'ISVOID'
    }
    
    tokens = [
        #identifiers
        'TYPE', 'ID',

        #built-in
        'INT', 'STRING', 'BOOL',

        #operators
        'PLUS', 'MUL', 'DIV', 'MINUS', 'LESS', 'LESS_EQ', 'EQ', 'INT_COMP', 'ASSIGN',

        #literals
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COLON', 'SEMICOLON', 'DOT', 'COMMA', 'CAST',

        #others
        'ARROW'] + list(keywords.values())
    
    # Simple rules
    t_PLUS = r'\+'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_MINUS = r'\-'
    t_LESS = r'\<'
    t_LESS_EQ = r'\<\='
    t_EQ = r'\='
    t_INT_COMP = r'\~'

    t_ASSIGN = r'\<\-'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COLON = r'\:'
    t_SEMICOLON = r'\;'
    t_DOT = r'\.'
    t_COMMA = r'\,'
    t_CAST = r'\@'

    t_ARROW = r'\=\>'
    
    @lex.TOKEN(r'[a-z][A-Za-z_0-9]*')
    def t_ID(self, t):
        if t.value.lower() == 'true':
            t.value = Bool('true')
            t.type = 'BOOL'
        elif t.value.lower() == 'false':
            t.value = Bool('false')
            t.type = 'BOOL'
        else:
            t.type = self.keywords.get(t.value.lower(), 'ID')
            t.value = Id(t.value)

        t.value.set_tracker(t.lexer.lineno, self.find_column(t))
        return t
    
    @lex.TOKEN(r'[A-Z][A-Za-z_0-9]*')
    def t_TYPE(self, t):
        t.type = self.keywords.get(t.value.lower(), 'TYPE')
        t.value = Type(t.value)
        t.value.set_tracker(t.lexer.lineno, self.find_column(t))
        
        return t

    @lex.TOKEN(r'\d+')
    def t_INT(self, t):
        t.value = Int(t.value)
        t.value.set_tracker(t.lexer.lineno, self.find_column(t))

        return t

    @lex.TOKEN(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t\f\r'
    t_ignore_line_comment = r'\-\-[^\n]*'

    def find_column(self, t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
        return t.lexpos - line_start + 1

    def t_error(self, t):
        self.lexer.errors.append(f'({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: ERROR \"{t.value[0]}\"')
        t.lexer.skip(1)


    states = (('COMMENT','exclusive'), ('STRING', 'exclusive'))

    @lex.TOKEN(r'\(\*')
    def t_begin_COMMENT(self, t):
        t.lexer.push_state('COMMENT')
        t.lexer.nesting_level_of_comment = 1

    @lex.TOKEN(r'\(\*')
    def t_COMMENT_nest(self, t):
        t.lexer.nesting_level_of_comment += 1

    @lex.TOKEN(r'\*\)')
    def t_COMMENT_end(self, t):
        t.lexer.nesting_level_of_comment -= 1
        if t.lexer.nesting_level_of_comment == 0:
            t.lexer.pop_state()

    @lex.TOKEN(r'\n+')
    def t_COMMENT_newline(self, t):
        t.lexer.lineno += len(t.value)

    def t_COMMENT_eof(self, t):
        self.lexer.errors.append(f'({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: EOF in comment')

    def t_COMMENT_error(self, t):
        t.lexer.skip(1)

    @lex.TOKEN(r'\"')
    def t_begin_STRING(self, t):
        t.lexer.push_state('STRING')
        t.lexer.string_backslashed = False
        t.lexer.stringbuf = ''

    @lex.TOKEN(r'\n')
    def t_STRING_newline(self, t):
        t.lexer.lineno += 1

        if not t.lexer.string_backslashed:
            self.lexer.errors.append(f"({t.lexer.lineno - 1}, {self.find_column(t)}) - LexicographicError: Unterminated string constant")
            t.lexer.pop_state()
            #t.lexer.skip(1)
        else:
            t.lexer.stringbuf += "\n"
            t.lexer.string_backslashed = False

    @lex.TOKEN(r'\"')
    def t_STRING_end(self, t):
        if t.lexer.string_backslashed:
            t.lexer.stringbuf += '"'
            t.lexer.string_backslashed = False
        else:
            t.lexer.pop_state()
            t.type = "STRING"
            t.value = String(t.lexer.stringbuf)
            t.value.set_tracker(t.lexer.lineno, self.find_column(t) - len(t.value.value) - 1)

            return t

    @lex.TOKEN('\0')
    def t_STRING_null(self, t):
        self.lexer.errors.append(f'({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: String contains null character')


    @lex.TOKEN(r'[^\n]')
    def t_STRING_line(self, t):
        if t.lexer.string_backslashed:
            if t.value == 'b':
                t.lexer.stringbuf += '\b'
            elif t.value == 't':
                t.lexer.stringbuf += '\t'
            elif t.value == 'n':
                t.lexer.stringbuf += '\n'
            elif t.value == 'f':
                t.lexer.stringbuf += '\f'
            elif t.value == '\\':
                t.lexer.stringbuf += '\\'
            else:
                t.lexer.stringbuf += t.value
            t.lexer.string_backslashed = False
        else:
            if t.value == '\\':
                t.lexer.string_backslashed = True
            else:
                t.lexer.stringbuf += t.value

    def t_STRING_eof(self, t):
        self.lexer.errors.append(f'({t.lexer.lineno}, {self.find_column(t)}) - LexicographicError: EOF in string constant')
