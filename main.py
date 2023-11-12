from src.COOL.run import lexer

a = lexer.tokenize('(2+ 31) *5 \n       24/3')

for i in a:
    print(i)
