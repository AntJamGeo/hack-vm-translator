import sys
import os

import vmtools

def write(input_file, module, code_writer):
    # Set the module attribute of the code writer to organise label
    # commands.
    code_writer.module = module
    # Use a parser to sweep through the file and write the commands
    # into the output .asm file.
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
            # Scan the directory for .vm files, all of which will be
            # used to create a single .asm file.
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
        print("The provided path does not match any directory or .vm file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
