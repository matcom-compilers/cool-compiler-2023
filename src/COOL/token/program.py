from typing import Any
from typing import List
from src.COOL.semantic.visitor import Visitor
from src.COOL.token import Token
from src.COOL.token.classdef import Class


class Program(Token):
    def __init__(self, classes: List[Class]) -> None:
        self.classes = classes
        self.visitor = Visitor()
    def execute(self):
        for _class in self.classes:
            _class.execute()
    
    def check(self):
        self.visitor.visit_program(self)
        for _class in self.classes:
            _class.check(self.visitor)
        

    
