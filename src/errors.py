class Error(Exception):
    def __init__(self, line, col, msg) -> None:
        self.line = line
        self.column = col
        self.msg = msg


class SyntacticError(Error):
    pass