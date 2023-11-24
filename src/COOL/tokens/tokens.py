from sly.lex import Token as SlyToken


class Token(SlyToken):
    column: int
