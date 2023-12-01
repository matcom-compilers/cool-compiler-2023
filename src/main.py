from argparse import ArgumentParser
from cool_compiler import CoolCompiler
from utils.errors import *
from pathlib import Path

args = ArgumentParser(prog='python -m coolcmp', description="COOl Compiler 2023.")
args.add_argument("file_path", help="Path to cool file to compile")
args.add_argument('--tab_size', dest='tab_size', default=4, type=int, help='Tab size to convert tabs to spaces, default is 4')
args = args.parse_args()

path = Path(args.file_path)

if not path.exists():
    raise Exception(f'File {path} doesnt exists')

with open(path) as file:
    content = file.read()

cool_compiler = CoolCompiler(content, args.tab_size)

try:
    mips_code = cool_compiler.compile_program()
    
    towrite = Path('../tests/codegen') / f'{path.stem}.mips'
    towrite.resolve()

    with open(towrite, 'w') as f:
        print(mips_code, file=f)

except Error as err:
    print(err)
    exit(1)