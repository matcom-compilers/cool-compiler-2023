from sly import Lexer


class SLYLexer(Lexer):
    tokens = {
        "NUMBER",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "LPAREN",
        "RPAREN",
        "EQUAL",
        "LESSTHAN",
        "LESSEQUAL"
    }

    ignore = " \t"

    # Special handling rules
    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    NUMBER = r"\d+"
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    LPAREN = r"\("
    RPAREN = r"\)"
    EQUAL = r"=="
    LESSTHAN = r"<"
    LESSEQUAL = r"<="