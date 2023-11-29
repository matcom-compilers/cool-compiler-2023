from typing import List

from COOL.semantic.visitor import Visitor_Program
from COOL.nodes import Node
from COOL.nodes.classdef import Class


class Program(Node):
    def __init__(self, classes: List[Class]) -> None:
        self.visitor = Visitor_Program()
        self.classes = classes

    def execute(self):
        for _class in self.classes:
            _class.execute()

    def check(self):
        self.visitor.visit_program(self)

        for class_ in self.classes:
            if class_:
                if class_.inherits and class_.inherits in self.visitor.types.keys() and not  class_.inherits in self.visitor.basic_types.keys():
                    class_.inherits_instance = self.visitor.types[class_.inherits] 
        
        for _class in self.classes:
            if _class:
                _class.check(self.visitor)
        
        return self.visitor.errors