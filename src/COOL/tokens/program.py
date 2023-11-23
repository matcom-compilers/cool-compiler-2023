from typing import List

from tokens import Token
from tokens.classdef import Class


class Program(Token):
    def __init__(self, classes: List[Class]) -> None:
        self.classes = classes
    
    def execute(self):
        for _class in self.classes:
            _class.execute()
    
    def check(self):
        raise NotImplementedError()
