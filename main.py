from src.COOL.run import lexer
from src.COOL.run import parser


b = parser.parse(lexer.tokenize('2*2-2+(5+2)'))
print(b)
