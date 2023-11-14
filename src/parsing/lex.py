from collections import namedtuple
from logging import getLogger
from typing import Optional

log = getLogger(__name__)


CharPosition = namedtuple("CharPosition", ["line", "column"])


class CharacterStream:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 0
        self.previous_position = self.get_position()

    def next_char(self) -> Optional[str]:
        if self.position >= len(self.source_code):
            return None
        char = self.source_code[self.position]
        self.position += 1
        self.previous_position = self.get_position()
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def peek_char(self) -> Optional[str]:
        if self.position >= len(self.source_code):
            return None
        return self.source_code[self.position]

    def get_position(self) -> CharPosition:
        return CharPosition(self.line, self.column)

    def reset(self):
        self.position = 0
        self.line = 1
        self.column = 0


class TokenType:
    OBJECTID = "OBJECTID"
    TYPEID = "TYPEID"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"
    DOT = "DOT"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    AT = "AT"
    TILDE = "TILDE"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    DIV = "DIV"
    LEQ = "LEQ"
    LOWER = "LOWER"
    EQUAL = "EQUAL"
    ASSIGN = "ASSIGN"
    CASSIGN = "CASSIGN"
    OPAR = "OPAR"
    CPAR = "CPAR"
    OCUR = "OCUR"
    CCUR = "CCUR"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FI = "FI"
    IF = "IF"
    IN = "IN"
    INHERITS = "INHERITS"
    ISVOID = "ISVOID"
    LET = "LET"
    LOOP = "LOOP"
    POOL = "POOL"
    THEN = "THEN"
    WHILE = "WHILE"
    CASE = "CASE"
    ESAC = "ESAC"
    NEW = "NEW"
    OF = "OF"
    NOT = "NOT"
    TRUE = "TRUE"
    SINGLE_LINE_COMMENT = "SINGLE_LINE_COMMENT"
    MULTI_LINE_COMMENT = "MULTI_LINE_COMMENT"


class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position


class Lexer:
    def __init__(self, stream):
        self.stream = CharacterStream(stream)
        self.keywords = {
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "fi": TokenType.FI,
            "if": TokenType.IF,
            "in": TokenType.IN,
            "inherits": TokenType.INHERITS,
            "isvoid": TokenType.ISVOID,
            "let": TokenType.LET,
            "loop": TokenType.LOOP,
            "pool": TokenType.POOL,
            "then": TokenType.THEN,
            "while": TokenType.WHILE,
            "case": TokenType.CASE,
            "esac": TokenType.ESAC,
            "new": TokenType.NEW,
            "of": TokenType.OF,
            "not": TokenType.NOT,
            "true": TokenType.TRUE,
        }
        self.errors = []

    def error(self, message, position: Optional[CharPosition] = None):
        if position is None:
            position = self.stream.previous_position
        row, col = position
        self.errors.append(f"({row}, {col}) - LexicographicError: {message}")

    def fetch_token(self):
        while True:
            char = self.stream.next_char()
            if char is None:
                return None

            if char.isspace():
                continue

            peek_char = self.stream.peek_char()
            # Keywords and identifiers
            if char.isalpha():
                identifier = char
                while peek_char is not None and (
                    peek_char.isalnum() or peek_char == "_"
                ):
                    identifier += peek_char
                    self.stream.next_char()  # consume peek_char
                    peek_char = self.stream.peek_char()

                if identifier in self.keywords:
                    log.debug(
                        f"Add Token Keyword {identifier} at {self.stream.get_position()}"
                    )
                    return Token(
                        type=self.keywords[identifier],
                        value=identifier,
                        position=self.stream.get_position(),
                    )
                else:
                    log.debug(
                        f"Add Token ObjectID {identifier} at {self.stream.get_position()}"
                    )
                    return Token(
                        type=TokenType.OBJECTID,
                        value=identifier,
                        position=self.stream.get_position(),
                    )

            # Numbers
            if char.isdigit():
                number = char
                while peek_char is not None and peek_char.isdigit():
                    number += peek_char
                    peek_char = self.stream.next_char()

                return Token(
                    type=TokenType.INT_CONST,
                    value=int(number),
                    position=self.stream.get_position(),
                )

            if char == '"':
                string = ""
                while True:
                    char = self.stream.next_char()
                    if char is None:
                        self.error(
                            "Unterminated string constant", self.stream.get_position()
                        )
                        return None
                    if char == "\n":
                        self.error(
                            "Unterminated string constant",
                        )
                        return None
                    if char == "\0":
                        self.error(
                            "String contains null character",
                        )
                        return None

                    if char == "\\":
                        peek_char = self.stream.peek_char()
                        if peek_char == "\n":  # ignore escaped newlines
                            self.stream.next_char()  # consume '\n'
                            continue
                        if peek_char in {"n", "t", "b", "f", "\\", '"'}:
                            escape_dict = {
                                "n": "\n",
                                "t": "\t",
                                "b": "\b",
                                "f": "\f",
                                "\\": "\\",
                                '"': '"',
                            }
                            string += escape_dict[peek_char]
                            self.stream.next_char()  # consume escaped
                            continue

                    if char == '"':
                        return Token(
                            type=TokenType.STRING_CONST,
                            value=string,
                            position=self.stream.get_position(),
                        )

                    string += char  # type: ignore

            # Single-line comments
            if char == "-":
                peek_char = self.stream.peek_char()
                if peek_char == "-":
                    comment = ""
                    self.stream.next_char() # consume -
                    peek_char = self.stream.peek_char()
                    while peek_char != "\n" and peek_char is not None:
                        comment += peek_char
                        self.stream.next_char()
                        peek_char = self.stream.peek_char()
                    if peek_char is None:
                        self.error("EOF in comment")
                        return None
                    return Token(type=TokenType.SINGLE_LINE_COMMENT, value=comment, position=self.stream.get_position())
                    
            # Multi-line comments
            if char == "(" and peek_char == "*":
                self.stream.next_char()  # consume '*'
                comment = ""
                while True:
                    char = self.stream.next_char()
                    if char is None:
                        self.error("EOF in comment", self.stream.get_position())
                        return None

                    if char == "*" and self.stream.peek_char() == ")":
                        token = Token(
                            type=TokenType.MULTI_LINE_COMMENT,
                            value=comment,
                            position=self.stream.get_position(),
                        )
                        self.stream.next_char()  # consume ')'
                        return token

                    comment += char

            # Operators and punctuation
            if char == ".":
                return Token(
                    type=TokenType.DOT,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == ",":
                return Token(
                    type=TokenType.COMMA,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == ":":
                return Token(
                    type=TokenType.COLON,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == ";":
                return Token(
                    type=TokenType.SEMICOLON,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "@":
                return Token(
                    type=TokenType.AT,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "~":
                return Token(
                    type=TokenType.TILDE,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "+":
                return Token(
                    type=TokenType.PLUS,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "-":
                return Token(
                    type=TokenType.MINUS,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "*":
                return Token(
                    type=TokenType.STAR,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "/":
                return Token(
                    type=TokenType.DIV,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "<":
                if peek_char == "=":
                    self.stream.next_char()
                    return Token(
                        type=TokenType.LEQ,
                        value="<=",
                        position=self.stream.get_position(),
                    )
                elif peek_char == "-":
                    self.stream.next_char()
                    return Token(
                        type=TokenType.ASSIGN,
                        value="<-",
                        position=self.stream.get_position(),
                    )
                else:
                    return Token(
                        type=TokenType.LOWER,
                        value="<",
                        position=self.stream.get_position(),
                    )

            if char == "=":
                if peek_char == ">":
                    self.stream.next_char()  # consume '>'
                    return Token(
                        type=TokenType.CASSIGN,
                        value="=>",
                        position=self.stream.get_position(),
                    )
                else:
                    return Token(
                        type=TokenType.EQUAL,
                        value="=",
                        position=self.stream.get_position(),
                    )

            if char == "(":
                return Token(
                    type=TokenType.OPAR,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == ")":
                return Token(
                    type=TokenType.CPAR,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "{":
                return Token(
                    type=TokenType.OCUR,
                    value=char,
                    position=self.stream.get_position(),
                )

            if char == "}":
                return Token(
                    type=TokenType.CCUR,
                    value=char,
                    position=self.stream.get_position(),
                )

            self.error(f'ERROR "{char}"')
            return None

    def lex(self):
        self.stream.reset()
        tokens = []
        while True:
            token = self.fetch_token()
            if token is None:
                break
            tokens.append(token)
        return tokens, self.errors
