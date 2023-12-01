class Error(Exception):
    def __init__(self, line, column, message):
        """
        Initialize a Cool compiler error.

        Parameters:
        - line (int): Line number where the error occurred.
        - column (int): Column number where the error occurred.
        - message (str): Error message.
        """
        self.line = line
        self.column = column
        self.message = message

class NameError(Error):
    pass

class SyntacticError(Error):
    pass

class SemanticError(Error):
    pass

class AttributeError(Error):
    pass

class LexicographicError(Error):
    pass

class TypeError(Error):
    pass
