import sys
module = "./src/COOL/"
sys.path.append(module)

from src.COOL import CoolLexer


file =\
'''
"kjas\"lnnsdj\nfljrdsaf"
@.$.@
@*%*@
"alkjfldajf""dasfadsf
'''


print("    Lexer:\n")
lexer = CoolLexer()

ast = list(lexer.tokenize(file))
print()
for i in ast:
    print(i)