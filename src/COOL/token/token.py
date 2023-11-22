from abc import ABC
from abc import abstractmethod
from typing import Any

class Token(ABC):
    '''
    Base class for tokens.
    '''
    line: int
    position: int

    def __init__(self, line: int) -> None:
        self.line = line
    
    # def __repr__(self) -> str:
    #     return f"Token(name=\"{self.__name__}\")"

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.execute(*args, **kwds)
    
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def check(self):
        pass

