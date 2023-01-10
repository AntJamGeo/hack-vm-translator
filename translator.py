import sys
import os

import vmtools

def write(input_file, code_writer):
    with vmtools.Parser(input_file) as parser:
        while parser.has_more_commands:
            code_writer.write(parser.words, parser.line, parser.module_name)
            parser.advance()

def main():
    dirname, basename = os.path.split(sys.argv[1])
    base_no_ext, ext = os.path.splitext(basename)
    if dirname:
        os.chdir(dirname)

    if os.path.isdir(basename):
        with vmtools.CodeWriter(basename) as code_writer:
            stack = [basename]
            while stack:
                path = stack.pop()
                for entry in os.scandir(path):
                    if entry.is_dir():
                        stack.append(entry)
                    else:
                        ext = os.path.splitext(entry.path)[1]
                        if ext == ".vm":
                            write(entry.path, code_writer)
    elif os.path.isfile(basename) and ext == ".vm":
        with vmtools.CodeWriter(base_no_ext) as code_writer:
            write(basename, code_writer)
    else:
        raise TypeError("Argument must be directory or .vm file.")

if __name__ == "__main__":
    main()
