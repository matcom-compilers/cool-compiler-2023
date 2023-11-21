from typing import Any
from typing import List

from src.COOL.token import Token
from src.COOL.token.classdef import Class


class Program(Token):
    def __init__(self, classes: List[Class]) -> None:
        self.classes = classes
    
    def execute(self):
        for _class in self.classes:
            _class.execute()
    
    def check(self):
        raise NotImplementedError()
