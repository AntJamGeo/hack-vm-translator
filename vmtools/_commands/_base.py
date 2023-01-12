from abc import ABC, abstractmethod

class Command(ABC):
    """An abstract base class for commands.

    All non-abstract subclasses should have a private instructions
    variable, which is a list of strings containing assembly code
    instructions. On initialisation of an instance, the list should
    be updated as necessary, and will then be joined together by
    calling super().__init__() to produce a single string containing
    the assembly code instructions to be written to the output file.

    Methods
    -------
    write(out_file)
        Write the command in assembly code into the output file.
    """
    @abstractmethod
    def __init__(self):
        self._asm = "".join(self._instructions)

    def write(self, out_file):
        out_file.write(self._asm)

