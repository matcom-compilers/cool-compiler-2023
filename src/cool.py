import argparse
import logging

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Generic Compiler")
    parser.add_argument("input_field", type=str, help="Path to the input file")
    parser.add_argument("output_field", type=str, help="Path to the output file")
    parser.add_argument("--lexer", action="store_true", help="Run only the lexer stage")
    parser.add_argument(
        "--parser", action="store_true", help="Run only the syntax analysis stage"
    )
    # Add other compiler stages as needed
    args = parser.parse_args()
    exit_code = 0

    # Read the input file
    try:
        with open(args.input_field, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        log.error(f"File {args.input_field} not found")
        exit(1)

    from parsing.lex import Lexer

    # If no options are specified, run the full compilation process
    lexer = Lexer(source_code)
    tokens, errors = lexer.lex()
    for error in errors:
        exit_code = 1
        print(error)
    if args.lexer:
        exit(exit_code)

    # Handle lexer errors if necessary
    # parser = Parser(tokens)
    # ast, errors = parser.parse()
    # Handle parser errors if necessary
    # Continue with the rest of the compilation process...
    exit(exit_code)


if __name__ == "__main__":
    main()
