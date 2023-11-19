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
