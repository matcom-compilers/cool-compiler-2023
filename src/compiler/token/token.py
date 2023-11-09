import re
from re import Pattern
from typing import Any


class Token:
    '''
    Base class for tokens.
    '''
    name: str
    value: Any
    line: int
    position: int

    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token({self.value})"
        

class DefToken:
    '''
    Base class for the tokens definitions.\n
    Conmtains the rules for the definition of the token and generate it.
    '''
    name: str
    rule: str
    regex: Pattern

    def __init__(self, name: str, rule: str) -> None:
        self.name = name
        self.rule = rule
        self.regex = re.compile(rule)
    
    def match(self, text: str, position: int=0):
        return self.regex.match(string=text, pos=position)
