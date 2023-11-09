import re
import yaml
from typing import List
from typing import Dict

from src.compiler.token.token import Token
from src.compiler.token.token import DefToken


# TODO: set lines and position in tokens
# TODO: implementation for ignore
class Lexer:
    tokens: List[DefToken]
    ignore: str

    def __init__(self, token_definitions_path: str) -> None:
        token_definitions = self.__load_token_definitions(token_definitions_path)
        self.tokens = self.__generate_tokens(token_definitions)
        self.ignore = " "

    def __split_lines(self, text: str) -> List[str]:
        '''
        Split the text in lines.
        '''
        return text.splitlines()
    
    def __split_ignore(self, text: str) -> List[str]:
        '''
        Split the text by the ignore rule.
        '''
        if not self.ignore:
            return [text]
        return re.split(self.ignore, text)
    
    # FIX: the position is not correct
    def __split_tokens(self, text: str, line: int) -> List[Token]:
        '''
        Split the text by the tokens.
        '''
        position = 0
        tokens = []
        while position < len(text):
            match = None
            for base_token in self.tokens:
                match = base_token.match(text=text, position=position)
                if match:
                    value = match.group(0)
                    tokens.append(Token(name=base_token.name, value=value))
                    position = match.end()
                    break
            if not match:
                # TODO: add error
                raise ValueError(f"Invalid token at line {line} position {position}")
        return tokens

    def __load_token_definitions(self, filepath: str) -> Dict[str, str]:
        '''
        Load the file with token definitions.
        '''
        with open(filepath, "r") as f:
            tokens_dict = yaml.safe_load(f)
            if not isinstance(tokens_dict, dict):
                raise
            return tokens_dict.get("tokens", {})
    
    def __generate_tokens(self, token_definitions: Dict[str, str]) -> List[DefToken]:
        '''
        Generate the tokens from the definitions.
        '''
        tokens = []
        for name, rule in zip(token_definitions.keys(), token_definitions.values()):
            tokens.append(DefToken(name=name, rule=rule))
        return tokens

    # TODO: the return should be a generator?
    def tokenize(self, text: str) -> List[Token]:
        '''
        Tokenize the text.
        '''
        line_counter = 0
        tokens = []
        text_lines = self.__split_lines(text)
        for line in text_lines:
            line_counter+=1
            splited_ignored = self.__split_ignore(line)
            for subtext in splited_ignored:
                subtext_tokens = self.__split_tokens(text=subtext, line=line_counter)
                tokens.extend(subtext_tokens)
        return tokens
