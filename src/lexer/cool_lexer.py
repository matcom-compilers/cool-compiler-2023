from utils.errors import *  # import LexicographicError
from ply import lex

from utils.utils import tokens, keywords, literals


class CoolLexer:
    def __init__(self) -> None:
        self.errors = []

        self.keywords = keywords

        self.tokens = tokens

        self.states = (("comment", "exclusive"), ("string", "exclusive"))

        self.lexer = lex.lex(module=self)
        self.lexer.col = 1

        self.data = ""

        self.str_val = ""
        self.str_line = 0
        self.str_col = 0
        self.str_end = False
        self.str_new_line = False

    def tokenize(self, data):
        self.data = data
        self.lexer.input(data)
        # print(data)
        a = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            a.append(tok)

        self.lexer.lineno = 1
        self.lexer.linestart = 0
        return a

    def pos(self, token):
        line_start = self.data.rfind("\n", 0, token.lexpos) + 1
        token.col = (token.lexpos - line_start) + 1  # token.lexer.col
        token.line = token.lexer.lineno
        # token.lexer.col += len(token.value)

    def find_column(self, token):
        line_start = self.data.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def t_LESSEQ(self, t):
        r"<="
        self.pos(t)
        return t

    def t_ASSIGN(self, t):
        r"<-"
        self.pos(t)
        return t

    def t_ARROW(self, t):
        r"=>"
        self.pos(t)
        return t

    def t_TYPE(self, t):
        r"[A-Z][a-zA-Z_0-9]*"
        self.pos(t)
        t.type = self.keywords.get(t.value.lower(), "TYPE")
        return t

    def t_ID(self, t):
        r"[a-z][a-zA-Z_0-9]*"
        self.pos(t)
        t.type = self.keywords.get(t.value.lower(), "ID")
        return t

    def t_INT(self, t):
        r"\d+"
        self.pos(t)
        t.value = int(t.value)
        return t

    def t_string(self, t):
        r'"'
        self.str_val = '"'
        self.pos(t)
        self.str_line = t.line
        self.str_col = t.col
        self.str_end = False
        t.lexer.begin("string")

    def t_string_end(self, t):
        r'(?<!\\)"'
        self.str_end = True
        t.line = self.str_line
        t.col = self.str_col
        t.lexer.begin("INITIAL")
        t.type = "STRING"
        t.value = self.str_val + t.value
        for index, char in enumerate(t.value):
            if char == "\0":
                null_col = t.col + index
                null_line = t.line
                self.errors.append(
                    LexicographicError(
                        line=null_line,
                        column=null_col,
                        message="String contains null character",
                    )
                )
        # t.value += t.value[1:-1]
        return t

    def t_string_space(self, t):
        r"\s"
        if t.value == "\n" and not self.str_new_line:
            self.pos(t)
            self.errors.append(
                LexicographicError(
                    line=t.line, column=t.col, message="Unterminated string constant"
                )
            )
            t.lexer.lineno += len(t.value)
            t.lexer.col = 1
            t.lexer.begin("INITIAL")
        if t.value == "\n" and self.str_new_line:
            self.pos(t)
            t.lexer.lineno += len(t.value)
            t.lexer.col = 1

    def t_string_pass(self, t):
        r"."
        self.str_val += t.value
        if t.value == "\\":
            self.str_new_line = True
        else:
            self.str_new_line = False

    def t_string_eof(self, t):
        self.pos(t)
        self.errors.append(
            LexicographicError(
                line=t.line, column=t.col, message="EOF in string constant"
            )
        )

    def t_comment(self, t):
        r"\(\*"
        t.lexer.level = 1
        t.lexer.begin("comment")

    def t_comment_lcomment(self, t):
        r"\(\*"
        t.lexer.level += 1

    def t_comment_rcomment(self, t):
        r"\*\)"
        t.lexer.level -= 1
        if t.lexer.level == 0:
            t.type = "COMMENT_LINE"
            t.lexer.begin("INITIAL")

    def t_comment_pass(self, t):
        r".|\n"
        self._end_comment = False
        if t.value == "\n":
            t.lexer.lineno += 1
            t.lexer.col = 1
        else:
            t.lexer.col += len(t.value)

    def t_comment_newline(self, t):
        r"\n"
        t.lexer.lineno += 1

    def t_ignore_COMMENT_LINE(self, t):
        r"--.*($|\n)"
        t.lexer.lineno += 1
        t.lexer.col = 1

    def t_comment_eof(self, t):
        self.pos(t)
        if t.lexer.level > 0:
            self.errors.append(
                LexicographicError(line=t.line, column=t.col, message="EOF in comment")
            )

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        t.lexer.col = 1

    def t_WHITESPACE(self, t):
        r"\s"
        if t.value == "\t":
            t.lexer.col += 4
        else:
            t.lexer.col += len(t.value)

    def t_PLUS(self, t):
        r"\+"
        t.type = "PLUS"
        self.pos(t)
        return t

    def t_MINUS(self, t):
        r"-"
        t.type = "MINUS"
        self.pos(t)
        return t

    def t_STAR(self, t):
        r"\*"
        t.type = "STAR"
        self.pos(t)
        return t

    def t_DIV(self, t):
        r"/"
        t.type = "DIV"
        self.pos(t)
        return t

    def t_COMPL(self, t):
        r"~"
        t.type = "COMPL"
        self.pos(t)
        return t

    def t_EQUAL(self, t):
        r"="
        t.type = "EQUAL"
        self.pos(t)
        return t

    def t_LESS(self, t):
        r"<"
        t.type = "LESS"
        self.pos(t)
        return t

    def t_COLON(self, t):
        r":"
        t.type = "COLON"
        self.pos(t)
        return t

    def t_LBRACE(self, t):
        r"\{"
        t.type = "LBRACE"
        self.pos(t)
        return t

    def t_RBRACE(self, t):
        r"\}"
        t.type = "RBRACE"
        self.pos(t)
        return t

    def t_AT(self, t):
        r"@"
        t.type = "AT"
        self.pos(t)
        return t

    def t_COMMA(self, t):
        r","
        t.type = "COMMA"
        self.pos(t)
        return t

    def t_DOT(self, t):
        r"\."
        t.type = "DOT"
        self.pos(t)
        return t

    def t_LPAREN(self, t):
        r"\("
        t.type = "LPAREN"
        self.pos(t)
        return t

    def t_RPAREN(self, t):
        r"\)"
        t.type = "RPAREN"
        self.pos(t)
        return t

    def t_SEMICOLON(self, t):
        r";"
        t.type = "SEMICOLON"
        self.pos(t)
        return t

    def t_ANY_error(self, t):
        self.pos(t)
        line = t.line
        col = t.col
        self.errors.append(
            LexicographicError(line=line, column=col, message=f'ERROR "{t.value[0]}"')
        )
        t.lexer.skip(1)
