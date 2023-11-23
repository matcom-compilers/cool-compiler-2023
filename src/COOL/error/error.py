

class Error:
    @classmethod
    def error(cls, line: int, column: int, error_type: str, message: str):
        print(f"({line}, {column}) - {error_type}: {message}")
        # exit(1)