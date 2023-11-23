from typing import List

from semantic.visitor import Visitor
from tokens import Token
from tokens.classdef import Class


class Program(Token):
    def __init__(self, classes: List[Class]) -> None:
        self.visitor = Visitor()
        self.classes = classes

    def execute(self):
        for _class in self.classes:
            _class.execute()

    def check(self):
        self.visitor.visit_program(self)

        for class_ in self.classes:
            class_.inherits = self.classes[class_.inherits]

        self.classes = {i.type: i for i in self.classes}

        self.visitor.types.update(self.classes)

        for _class in self.classes:
            _class.check(self.visitor)
