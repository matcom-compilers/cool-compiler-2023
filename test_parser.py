from src.COOL.parser import CoolParser
from src.COOL.lexer import SLYLexer


if __name__ == '__main__':
    parser = CoolParser()
    lexer = SLYLexer()
    text= '3 + 5'
    print(lexer.tokenize(text))
    print(parser.parse(lexer.tokenize(text)))
    
    # while True:
    #     try:
    #         text = input('3 + 5 ')
    #         result = parser.parse(lexer.tokenize(text))
    #         print(result)
    #     except EOFError:
    #         break