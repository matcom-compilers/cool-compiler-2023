import os
from pathlib import Path
import sys
module = "./src/"
sys.path.append(module)

from src.COOL import CoolLexer
from src.COOL import CoolParser
from src.COOL.utils import load_file
from src.COOL.semantic import Semantic


def check_errors(errors):
    if errors:
        for error in errors:
            print(error)

def main():
    folder = "./tests/semantic/"
    files = sorted([os.path.join(folder, f) for f in os.listdir(folder)])
    cls = [f for f in files if f.endswith(".cl")]
    out = [f[:-3] + "_error.txt" for f in cls]

    for _cl, _out in zip(cls, out):
        loaded_file = load_file(_cl)
        with open(_out, "r") as f:
            expected = f.readlines()
        
        lexer = CoolLexer()
        
        print(f"Testing {Path(_cl).name}:")
        print("Expected:")
        for line in expected:
            print(f"{line.strip()}")
        
        print("Got:")
        tokens, errors = lexer.tokenize(loaded_file)

        parser = CoolParser()
        ast, errors = parser.parse(tokens)

        errors = Semantic.check(ast)
        check_errors(errors)

        print()


if __name__ == "__main__":
    main()