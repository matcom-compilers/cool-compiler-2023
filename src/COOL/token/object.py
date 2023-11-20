from typing import Any

from src.COOL.token import Token


class Object(Token):
    def __init__(self, line: int, value: Any) -> None:
        self.value = value
        super().__init__(line)
    
    def execute(self):
        return self.value

class Interger(Object):
    def __init__(self, line: int, value: Any) -> None:
        super().__init__(line, value)
    
    def check(self):
        raise NotImplementedError()

class String(Object):
    def __init__(self, line: int, value: Any) -> None:
        super().__init__(line, value)
    
    def check(self):
        raise NotImplementedError()

class Boolean(Object):
    def __init__(self, line: int, value: Any) -> None:
        super().__init__(line, value)
    
    def check(self):
        raise NotImplementedError()
