from vmtools._commands import Command

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

    def write_arithmetic(self, command):
        """
        Write an arithmetic/logical command into the output file.

        Parameters
        ----------
        command : str
            The type of arithmetic/logical operation.
        """
        self._file.write(command + "\n")

    def write_push_pop(self, command, segment, index):
        """
        Write a push/pop command into the output file.

        Parameters
        ----------
        command : Command
            Either push or pop.
        segment : str
            The memory segment where the command operates.
        index : int
            Memory location within the segment where the command
            operates.
        """
        self._file.write(segment + " " + index + "\n")
