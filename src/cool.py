import argparse
import logging
import os

from parsing.lex import Lexer
from parsing.parser import Parser
from semantic.type_collector import TypeCollector
from utils.loggers import LoggerUtility

log = LoggerUtility().get_logger()


def main():
    parser = argparse.ArgumentParser(description="IceBox Compiler")
    parser.add_argument("input_file", type=str, help="Input source code file")
    parser.add_argument(
        "--output_file",
        type=str,
        help="Output file (default: same as input with .mips extension)",
    )
    parser.add_argument("--lexer", action="store_true", help="Run only the lexer stage")
    parser.add_argument(
        "--parser", action="store_true", help="Run only to parsing stage"
    )
    parser.add_argument("-t", action="store_true", help="Print Tokens from lexer stage")
    parser.add_argument(
        "--log-level", type=str, help="Set the log level (default: INFO)"
    )

    # Add other compiler stages as needed
    options = parser.parse_args()
    exit_code = 0

    # Set Log Level
    if options.log_level is not None:
        log.setLevel(options.log_level.upper())
    else:
        log.setLevel("INFO")

    # If no output file is specified, use the input file name with a .mips extension
    if options.output_file is None:
        base_name = os.path.splitext(options.input_file)[0]
        options.output_file = base_name + ".mips"

    # Try to open and read the input file
    try:
        with open(options.input_file, "r") as f:
            source_code = f.read()
    except Exception as e:
        print(f"CompileError: {e}")
        exit(1)

    # Run the appropriate compiler stages based on the flags
    lexer = Lexer(source_code)
    tokens, errors = lexer.lex()

    if options.t:
        for t in tokens:
            print(f"{t.type} | {t.value} | {t.position}")

    if errors:
        for error in errors:
            print(error)
        exit_code = 1
        exit(exit_code)

    if options.lexer:
        exit(exit_code)

    ### Parsing

    parser = Parser(tokens)
    program = parser.parse()

    parser_errors = parser.errors
    if parser_errors:
        for error in parser_errors:
            print(error)
        exit_code = 1
        exit(exit_code)

    if options.parser:
        exit(exit_code)

    assert program is not None
    ### Collect types
    type_collector = TypeCollector()
    program.accept(type_collector)

    if type_collector.errors:
        for error in type_collector.errors:
            print(error)
        exit_code = 1
        exit(exit_code)

    ######

    exit(exit_code)


if __name__ == "__main__":
    main()