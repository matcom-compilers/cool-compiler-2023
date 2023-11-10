import os
import re
import yaml
import logging
from typing import List
from typing import Dict
from re import Pattern

from src.compiler.token import Token


logger = logging.getLogger(__name__)


# TODO: implementation for comment
# TODO: add errors
class Lexer:
    _rules: Dict[str, Pattern]
    _ignore: Pattern
    _newline: Pattern
    _comment: Pattern

    def __init__(self, rules_filepath: str) -> None:
        self._colect_rules(rules_filepath)
    
    @property
    def rules(self):
        return self._rules
    
    @property
    def ignore(self):
        return self._ignore
    
    @property
    def newline(self):
        return self._newline
    
    @property
    def comment(self):
        return self._comment

    def _colect_rules(self, filepath: str):
        '''
        Load the file with token definitions.
        '''
        if not os.path.isfile(filepath) or not filepath.endswith(".yml"):
            raise
        with open(filepath, "r") as f:
            rules = yaml.safe_load(f)
            if not isinstance(rules, dict):
                raise
            
            token_rules = rules.get("tokens", {})
            self._rules = {}
            for name, rule in zip(token_rules.keys(), token_rules.values()):
                self._rules.update({name: re.compile(rule)})
            self._ignore = re.compile(rules.get("ignore", ""))
            self._newline = re.compile(rules.get("newline", ""))
            self._comment = re.compile(rules.get("comment", ""))

    def tokenize(self, text: str) -> List[Token]:
        '''
        Tokenize the text.
        '''
        position = 0
        line_counter = 0
        while position < len(text):
            if self.ignore.match(string=text, pos=position):
                logger.debug("match ignore")
                position+=1
                continue
            if self.newline.match(string=text, pos=position):
                logger.debug("match newline")
                line_counter+=1
                position+=1
                continue
            for rule_name, rule in zip(self.rules.keys(), self.rules.values()):
                match = rule.match(string=text, pos=position)
                if match:
                    logger.debug("match rule")
                    value = match.group(0)
                    position = match.end()
                    yield Token(name=rule_name, value=value, line=line_counter)
                    break
            if not match:
                # TODO: add error
                raise ValueError(f"Invalid token at line {line_counter} position {position}")
