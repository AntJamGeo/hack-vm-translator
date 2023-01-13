from abc import ABC, abstractmethod

class Command(ABC):
    """
    An abstract base class for commands.

    All non-abstract subclasses should have an asm variable that
    contains the asm instructions for that command. The write method
    can then be used to write these instructions into the provided
    output file.

    Methods
    -------
    write(out_file)
        Write the command in assembly code into the output file.
    """
    @abstractmethod
    def __init__(self):
        self._asm = None
        raise NotImplementedError

    def write(self, out_file):
        out_file.write(self._asm)

