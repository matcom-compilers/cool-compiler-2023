from typing import List

from nodes import Node
from nodes.classdef import Class


class Program(Node):
    def __init__(self, classes: List[Class]) -> None:
        self.classes = classes
    
    def execute(self):
        for _class in self.classes:
            _class.execute()
    
    def check(self):
        raise NotImplementedError()
