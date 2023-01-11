from vmtools._commands import make_command

class CodeWriter:
    """
    An assembly language code writer.

    Uses information obtained from a VM language command to write
    the equivalent command in assembly language to an output file.

    Attributes
    ----------
    module : str
        Name of the current module.

    Methods
    -------
    write(words, line)
        Write a command into the output file.
    """

    def __init__(self, basename):
        self._file_path = basename + ".asm"
        self._file = None
        self.module = None

    def __enter__(self):
        self._file = open(self._file_path, "w")
        return self

    def __exit__(self, *args):
        self._file.close()

    def write(self, words, line):
        make_command(words, line, self.module).write(self._file)

