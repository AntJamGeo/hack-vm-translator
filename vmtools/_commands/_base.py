from abc import ABC, abstractmethod

class Command(ABC):
    """An abstract base class for commands.

    All commands are initialised with an empty list that will contain
    the assembly commands needed to execute the command, an empty
    assembly code string, and a requirement to be built, which means
    the assembly code in the list will need to be joined together to
    produce a string of commands that can be written into the output
    file. Depending on the type of command, it may need rebuilding
    again, in which case _require_build will remain True, otherwise
    the first time _asm_string is built, that is how it will remain
    for the lifetime of the Command object. The process of building
    the string is done by the _encode function, which gets called
    when the write function is called so that the correct string of
    assembly commands is written to the output file.

    Methods
    -------
    write(out_file)
        Write the command in assembly code into the output file.
    """
    @abstractmethod
    def __init__(self):
        self._require_build = True
        self._asm = []
        self._asm_string = ""

    def write(self, out_file):
        out_file.write(self._encode())

    def _encode(self, require_rebuild=False):
        if self._require_build:
            self._asm = []
            self._build_asm()
            self._asm.append("")
            self._asm_string = "\n".join(self._asm)
            self._require_build = require_rebuild
        return self._asm_string

    @abstractmethod
    def _build_asm(self, comment=None):
        if comment is not None:
            self._asm.append(comment)

PUSH = ("@SP", "M=M+1", "A=M-1", "M=D")
POP = ("@SP", "AM=M-1", "D=M")
