class CoolError(Exception):
    def __init__(self, line, column, type_, message):
        self.line = line
        self.col = column
        self._type = type_
        self.message = message

    
    def __str__(self) -> str:
        return f'({self.line},{self.col}) - {self._type}: ERROR "{self.message}"'

    
    def __repr__(self):
        return str(self)

# class CompilerError(CoolError):
#     def __init__(self, message):
#         CoolError.__init__(self, 0, 0, "CompilerError", message)


class LexicographicError:
    def __init__(self, line, column, message):
        # CoolError.__init__(self, line, column, "LexicographicError", message)
        self.line = line
        self.col = column
        self.message = message

    
    def __str__(self) -> str:
        return f'{self.line, self.col} - LexicographicError: {self.message}'

    def __repr__(self):
        return str(self)

class SyntacticError(CoolError):
    def __init__(self, line, column, message):
        CoolError.__init__(self, line, column, "SyntacticError", message)

    def __str__(self):
        return f'({self.line}, {self.col}) - {self._type}: ERROR at or near "{self.message}"'


class SemanticError(CoolError):
    def __init__(self, line, column, message):
        CoolError.__init__(self, line, column, "SemanticError", message)


# class TypeError(CoolError):
#     def __init__(self, line, column, message):
#         CoolError.__init__(self, line, column, "TypeError", message)


# class NameError(CoolError):
#     def __init__(self, line, column, message):
#         CoolError.__init__(self, line, column, "NameError", message)


# class AttributeError(CoolError):
#     def __init__(self, line, column, message):
#         CoolError.__init__(self, line, column, "AttributeError", message)
