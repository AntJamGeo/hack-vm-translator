import sys

import vmtools
from vmtools import Command

class InvalidFileTypeError(Exception):
    pass


if __name__ == "__main__":
    in_file_path = sys.argv[1]
    if in_file_path.endswith(".vm"):
        out_file_path = in_file_path[:-2] + "asm"
        with vmtools.Parser(in_file_path) as parser, \
             vmtools.CodeWriter(out_file_path) as code_writer:
            while parser.has_more_commands:
                code_writer.write(parser.command, parser.line)
                parser.advance()
    else:
        raise InvalidFileTypeError("Argument should be a .vm file.")
