from vmtools._commands import Add
from vmtools._commands import Subtract
from vmtools._commands import Equals
from vmtools._commands import GreaterThan
from vmtools._commands import LessThan
from vmtools._commands import And
from vmtools._commands import Or
from vmtools._commands import Negate
from vmtools._commands import Not
from vmtools._commands import Push
from vmtools._commands import Pop
from vmtools._commands import Label
from vmtools._commands import GoTo
from vmtools._commands import IfGoTo
from vmtools._commands import Call
from vmtools._commands import Function
from vmtools._commands import Return


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

    def __init__(self, basename, initialise):
        self._file_path = basename + ".asm"
        self._file = None
        self._initialise = initialise
        self._function = None
        self.module = basename

    def __enter__(self):
        self._file = open(self._file_path, "w")
        if self._initialise:
            self._sys_init()
        return self

    def __exit__(self, *args):
        self._file.close()

    def write(self, words, line):
        self._file.write("// " + " ".join(words) + "\n")
        self._make_command(words, line).write(self._file)

    def _sys_init(self):
        self._file.write(
                "@261\nD=A\n@SP\nM=D\n"
                "@Sys.init\n0;JMP\n"
                )

    def _make_command(self, words, line):
        """
        Make a command.

        Parameters
        ----------
        words : list
            A list of keywords found on a line by the Parser.
        line : int
            The current line number in the input file (for locating
            errors in a .vm file).

        Returns
        -------
        Command
            A command object for writing assembly code into a .asm
            file.
        """
        if words[0] in _COMPARISONS:
            if len(words) != 1:
                raise Exception()
            return _COMPARISONS[words[0]]()
        elif words[0] in _OTHER_AL_OPS:
            if len(words) != 1:
                raise Exception()
            return _OTHER_AL_OPS[words[0]]
        elif words[0] == "push":
            if len(words) != 3:
                raise Exception()
            if words[1] not in _SEGMENTS:
                raise Exception()
            return Push(words[1], words[2], self.module)
        elif words[0] == "pop":
            if len(words) != 3:
                raise Exception()
            if words[1] not in _SEGMENTS or words[1] == "constant":
                raise Exception()
            return Pop(words[1], words[2], self.module)
        elif words[0] == "label":
            if len(words) != 2:
                raise Exception()
            return Label(words[1], self._function)
        elif words[0] == "goto":
            if len(words) != 2:
                raise Exception()
            return GoTo(words[1], self._function)
        elif words[0] == "if-goto":
            if len(words) != 2:
                raise Exception()
            return IfGoTo(words[1], self._function)
        elif words[0] == "call":
            if len(words) != 3:
                raise Exception()
            return Call(words[1], words[2])
        elif words[0] == "function":
            if len(words) != 3:
                raise Exception()
            self._function = words[1]
            return Function(words[1], words[2])
        elif words[0] == "return":
            if len(words) != 1:
                raise Exception()
            return Return()
        else:
            raise Exception()

_COMPARISONS = {
        "eq": Equals,
        "gt": GreaterThan,
        "lt": LessThan
        }
_OTHER_AL_OPS = {
        "add": Add(),
        "sub": Subtract(),
        "neg": Negate(),
        "and": And(),
        "or": Or(),
        "not": Not()
        }
_SEGMENTS = {
        "local",
        "argument",
        "this",
        "that",
        "constant",
        "static",
        "temp",
        "pointer"
        }
