from argparse import ArgumentParser
from cool_compiler import CoolCompiler
from utils.errors import *
from pathlib import Path

args = ArgumentParser(prog='python3 -m main',
                      description="Cool compiler 2023.")
args.add_argument("file_path", help="Path to cool file to compile")
args = args.parse_args()

path = Path(args.file_path)

if not path.exists():
    raise Exception(f'File {path} doesnt exists')

with open(path) as file:
    content = file.read()

try:
    cool_compiler = CoolCompiler(content)

    mips_code = cool_compiler.compile_program()

    towrite = Path('../tests/codegen') / f'{path.stem}.mips'
    towrite.resolve()

    with open(towrite, 'w') as f:
        print(mips_code, file=f)
        
except Error as err:
    print(err)
    exit(1)
