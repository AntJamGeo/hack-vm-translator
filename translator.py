import sys
import os

import vmtools

def write(input_file, module, code_writer):
    code_writer.module = module
    with vmtools.Parser(input_file) as parser:
        while parser.has_more_commands:
            code_writer.write(parser.words, parser.line)
            parser.advance()

def main():
    path = sys.argv[1]
    dirname, basename = os.path.split(path)
    base_no_ext, ext = os.path.splitext(basename)

    if os.path.isdir(path):
        os.chdir(path)
        with vmtools.CodeWriter(basename, True) as code_writer:
            for entry in os.scandir():
                base_no_ext, ext = os.path.splitext(entry.name)
                if ext == ".vm":
                    write(entry.path, base_no_ext, code_writer)
    elif os.path.isfile(path) and ext == ".vm":
        if dirname:
            os.chdir(dirname)
        with vmtools.CodeWriter(base_no_ext, False) as code_writer:
            write(basename, base_no_ext, code_writer)
    else:
        raise TypeError("Argument must be directory or .vm file.")

if __name__ == "__main__":
    main()
