from vmtools._commands import make_command

class CodeWriter:
    """
    An assembly language code writer.

    Uses information obtained from a VM language command to write
    the equivalent command in assembly language to an output file.

    Methods
    -------
    write(command)
        Write a command into the output file.
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._file_name = '.'.join(file_path[:-4].split('/'))
        self._file = None

    def __enter__(self):
        self._file = open(self._file_path, "w")
        return self

    def __exit__(self, *args):
        self._file.close()

    def write(self, args, line):
        make_command(args, line, self._file_name).write(self._file)

