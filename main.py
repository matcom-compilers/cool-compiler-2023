from src.COOL.run import lexer
from src.COOL.run import parser


b = parser.parse(lexer.tokenize('(2+2)*3-2 \n 5*3-2*8'))

for i in b:
    print(i.__dict__)
