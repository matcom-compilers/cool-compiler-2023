from src.COOL.run import lexer,parser

# from src.COOL import SLYLexer
# from src.COOL import CoolParser


a = lexer.tokenize('(2+ 31) *5 \n       24/3')
for i in a:
    print(i)


# b = parser.parse(a)
b = parser.parse(lexer.tokenize('(2+ 31) *5 \n       24/3'))

for i in b:
    print(i)











