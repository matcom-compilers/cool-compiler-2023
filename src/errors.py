class Error(Exception):
    def __init__(self, line, column, type_, message):
        self.line = line
        self.col = column
        self._type = type_
        self.message = message

    
    def __str__(self) -> str:
        return f'({self.line}, {self.col}) - {self._type}: ERROR "{self.message}"'


class CompilerError(Error):
    def __init__(self, message):
        Error.__init__(self, 0, 0, "CompilerError", message)


class LexicographicError(Error):
    def __init__(self, line, column, message):
        Error.__init__(self, line, column, "LexicographicError", message)


class SyntacticError(Error):
    def __init__(self, line, column, message):
        Error.__init__(self, line, column, "SyntacticError", message)


class SemanticError(Error):
    def __init__(self, line, column, message):
        Error.__init__(self, line, column, "SemanticError", message)


class TypeError(Error):
    def __init__(self, line, column, message):
        Error.__init__(self, line, column, "TypeError", message)


class NameError(Error):
    def __init__(self, line, column, message):
        Error.__init__(self, line, column, "NameError", message)


class AttributeError(Error):
    def __init__(self, line, column, message):
        Error.__init__(self, line, column, "AttributeError", message)
