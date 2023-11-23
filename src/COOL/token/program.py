from typing import Any
from typing import List
from src.COOL.semantic.visitor import Visitor
from src.COOL.token import Token
from src.COOL.token.classdef import Class


class Program(Token):
    def __init__(self, classes: List[Class]) -> None:
        self.visitor = Visitor()
        self.classes = classes

    def execute(self):
        for _class in self.classes:
            _class.execute()

    def check(self):
        self.visitor.visit_program(self)

        for class_ in self.classes.keys():
            class_.inherits = self.classes[class_.inherits]

        self.classes = {i.type: i for i in self.classes}

        self.visitor.types.update(self.classes)

        for _class in self.classes:
            _class.check(self.visitor)
