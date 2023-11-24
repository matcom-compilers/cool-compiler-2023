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

        # self.classes = {i.type: i for i in self.classes}
        self.classes = self.visitor.types

        for class_ in self.classes.values():
            if class_:
                class_.inherits = self.classes[class_.inherits] if class_.inherits else None

        for _class in self.classes.values():
            if _class:
                _class.check(self.visitor)
