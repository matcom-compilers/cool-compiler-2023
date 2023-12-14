

class Error:
    @classmethod
    def error(cls, line: int, column: int, error_type: str, message: str) -> str:
        return f"({line}, {column}) - {error_type}: {message}"
