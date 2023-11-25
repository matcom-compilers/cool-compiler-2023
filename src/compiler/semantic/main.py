from parser.count_characters import count_chars
from parser.cool_parser import CoolLexer, CoolParser
from AST.ast import CoolProgram
from semantic.semantic_ import semantic, Semantic
from semantic.semantic_visitor import init_classes, init_types, validate_program

import os
import colorama
from colorama import Fore
colorama.init()

base_dir = os.getcwd()
base_url = os.path.join(base_dir, "tests/semantic/")

def all():
    cases = [case for case in os.listdir(base_url) if case.endswith('.cl')] 
    cases.sort()

    for i in range(0,len(cases)):
        case = cases[i]
        simple_case(case,i)
        
def simple_case(case, i):
    semantic.errors = []
    case_error = case[:-3] + '_error.txt'
    dir = '/'.join([base_url,case])
    dir_error = '/'.join([base_url,case_error])
    with open(dir, "r") as f:
        code = f.read()
    with open(dir_error, "r") as f:
        error = f.read()

    lexer = CoolLexer()
    parser = CoolParser(lexer = lexer)
    program = parser.parse(lexer.tokenize(code))
    validate_program(program)

    if len(semantic.errors) > 0:
        e = str(semantic.errors[0])
        if e[:9] != error[:9]:
            print(Fore.RED)
        else:
            print(Fore.GREEN)
            # print(f'CASE {i+1} PASSED')
        print(f'\n\n\n######################### {case} #############################')
        print('----------------------SEMANTIC ERRORS---------------------------')
        for e in semantic.errors:
            print(e)
        print ("\n---------------------EXPECTED ERRORS:-------------------------")
        print(error) 
    else:
        print(Fore.RED)
        print(f'\n\n\n######################### {case} #############################')
        print(code)
        print('----------------------SEMANTIC ERRORS---------------------------')
        print("<empty>")
        print ("\n---------------------EXPECTED ERRORS:-------------------------")
        print(error) 
                

def one_case(case):
    base_dir = os.getcwd()
    base_url = os.path.join(base_dir, "tests/semantic/")
    dir = os.path.join(base_url,case)

    with open(dir, "r") as f:
        content = f.read()

    lexer = CoolLexer()
    parser = CoolParser(lexer = lexer)
    tokens = lexer.tokenize(content)

    if len(lexer.errors) > 0: raise Exception(str(lexer.errors[0]))

    program:CoolProgram = parser.parse(tokens)
    if len(parser.errors) > 0: raise Exception(str(parser.errors[0]))

    validate_program(program)

    for error in semantic.errors:
        print(error)
