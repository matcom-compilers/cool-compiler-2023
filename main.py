from src.COOL.run import lexer
from src.COOL.run import parser


b = parser.parse(lexer.tokenize('2+2*3 \n 3-2'))

for i in b:
    print(i)
