class CodeWriter:
    """
    An assembly language code writer.

    Uses information obtained from a VM language command to write
    the equivalent command in assembly language to an output file.

    Methods
    -------
    write_arithmetic(arg)
        Write an arithmetic/logical command into the output file.
    write_push_pop(arg1, arg2)
        Write a push/pop command into the output file.
    """

    def __init__(self, file_path):
        self._file_path = file_path

    def __enter__(self):
        self._file = open(self._file_path, "w")
        return self

    def __exit__(self, *args):
        self._file.close()

    def write(self, command):
        command.write(self._file)

