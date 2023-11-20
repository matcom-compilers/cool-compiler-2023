from typing import Any
from abc import ABC, abstractmethod

class Token(ABC):
    '''
    Base class for tokens.
    '''
    name: str
    value: Any
    line: int
    position: int

    def __init__(self, name: str, value: Any, line: int) -> None:
        self.name = name
        self.value = value
        self.line = line
    
    def __repr__(self) -> str:
        return f"Token(name=\"{self.name}\", value={self.value})"
    
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def check(self):
        pass

    

