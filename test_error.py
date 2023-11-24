import os
from pathlib import Path
import sys
module = "./src/COOL/"
sys.path.append(module)

from src.COOL import CoolLexer
from src.COOL import CoolParser
from src.COOL.utils import load_file


folder = "/home/dionisio35/Documents/GitHub/cool-compiler-2023/tests/lexer/"
files = sorted([os.path.join(folder, f) for f in os.listdir(folder)])
cls = files[::2]
out = files[1::2]


for _cl, _out in zip(cls, out):
    loaded_file = load_file(_cl)
    with open(_out, "r") as f:
        expected = f.readlines()
    lexer = CoolLexer()
    parser = CoolParser()
    print(f"Testing {Path(_cl).name}:")
    print("Expected:")
    for line in expected:
        print(f"{line.strip()}")
    print("Got:")
    for i in lexer.tokenize(loaded_file):
        pass
    print()

    # break



# file = "./tests/lexer/string3.cl"
# loaded_file = load_file(file)

# lexer = CoolLexer()
# # parser = CoolParser()


# for i in lexer.tokenize(loaded_file):
#     pass
