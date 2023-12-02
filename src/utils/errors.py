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

    def __str__(self):
        return '({},{}) - {}: {}'.format(self.line, self.column, self.__class__.__name__, self.message)


class NameError(Error):
    pass


class SyntacticError(Error):
    pass


class SemanticError(Error):
    pass


class AttributeError(Error):
    pass


class LexicographicError(Error):
    def __init__(self, message):
        self.msg = message

    def __str__(self) -> str:
        return self.msg


class TypeError(Error):
    pass
