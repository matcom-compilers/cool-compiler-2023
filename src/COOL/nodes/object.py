from typing import Any

from COOL.nodes import Node


class Object(Node):
    def __init__(self, line: int, column: int, value: Any) -> None:
        self.value = value
        super().__init__(line, column)

    def check(self,visitor):
        return 'Object'
    
    def execute(self):
        return self.value


class Interger(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)

    def check(self,visitor):
        return 'Int'


class String(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)

    
    def check(self,visitor):
        return 'String'


class Boolean(Object):
    def __init__(self, line: int, column: int, value: Any) -> None:
        super().__init__(line, column, value)

    def check(self,visitor):
        return 'Bool'
