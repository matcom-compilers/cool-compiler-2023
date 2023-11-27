from typing import List

from COOL.semantic.visitor import Visitor
from COOL.nodes import Node
from COOL.nodes.classdef import Class

from COOL.nodes.codegen_rules import DATA_SECTION
from COOL.nodes.codegen_rules import TEXT_SECTION
from COOL.nodes.codegen_rules import COMMENT


class Program(Node):
    def __init__(self, classes: List[Class]) -> None:
        self.visitor = Visitor()
        self.classes = classes

    def execute(self):
        mips_script_data = DATA_SECTION
        mips_script_text = TEXT_SECTION
        
        for _class in self.classes:
            data, text = _class.execute()
            data, text = "".join(data), "".join(text)
            mips_script_data += COMMENT.format(comment=f"Variables of class {_class.type}:\n")
            mips_script_data += data
            mips_script_text += COMMENT.format(comment=f"Functions of class {_class.type}:\n")
            mips_script_text += text
        
        mips_script = mips_script_data + mips_script_text
        return mips_script

    def check(self):
        self.visitor.visit_program(self)

        self.classes = self.visitor.types

        for class_ in self.classes.values():
            if class_:
                class_.inherits = self.classes[class_.inherits] if (class_.inherits and class_.inherits in self.classes.keys()) else None

        for _class in self.classes.values():
            if _class:
                _class.check(self.visitor)
        return self.visitor.errors