import sys
import os

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

        # In directory translation, we need to initialise first, so
        # this will be set to true. For a single file, this is false.
        self._initialise = initialise

        # The current function being translated. This is needed for
        # labels and return address symbols.
        self._function = None

        # The name of the current module. This is needed for static
        # variable symbols.
        self.module = basename

    def __enter__(self):
        self._file = open(self._file_path, "w")
        if self._initialise:
            self._sys_init()
        return self

    def __exit__(self, *args):
        self._file.close()

    def write(self, words, line):
        """
        Write a command into the output file.

        A command object gets created and we use the write command of
        the command to add code to the output file.

        Parameters
        ----------
        words : list
            A list of keywords found on a line by the Parser.
        line : int
            The current line number in the input file (for locating
            errors in a .vm file).

        """
        self._file.write("// " + " ".join(words) + "\n") # adds comments
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
        if len(words) == 1:
            # Separate comparison commands from other one-word
            # commands as they need to be rebuilt each time they are
            # called; comparisons have a counter that must be
            # incremented, while the other one-word commands consist
            # of exactly the same assembly code each time.
            if words[0] in _COMPARISONS:
                return _COMPARISONS[words[0]]()
            elif words[0] in _OTHER_ONE_WORD_OPS:
                return _OTHER_ONE_WORD_OPS[words[0]]

        elif len(words) == 2:
            # The label commands take one arg: the label. To build
            # them, we also need the name of the function that they
            # were called in to create the symbol.
            if words[0] == "label":
                return Label(words[1], self._function)
            elif words[0] == "goto":
                return GoTo(words[1], self._function)
            elif words[0] == "if-goto":
                return IfGoTo(words[1], self._function)

        elif len(words) == 3:
            # Push and pop commands have two args: the desired memory
            # segment and the index. To build these, we also input
            # the current module in case we need to make a static
            # variable symbol.
            if words[0] == "push":
                if words[1] in _SEGMENTS:
                    return Push(words[1], words[2], self.module)
            elif words[0] == "pop":
                if words[1] in _SEGMENTS and words[1] != "constant":
                    return Pop(words[1], words[2], self.module)

            # Call also takes two args: the function name and the
            # number of arguments to be passed to the function.
            elif words[0] == "call":
                return Call(words[1], words[2])

            # Function takes a function name and the number of local
            # variables needed. Here, we also update the function
            # attribute of the code writer as this indicates we are
            # entering a new function definition, so this should be
            # reflected in label symbols.
            elif words[0] == "function":
                self._function = words[1]
                return Function(words[1], words[2])

        # If nothing has been returned at this point, the command
        # is invalid.
        print(
            f"Invalid command found in module '{self.module}' on line"
            f" {line} : {' '.join(words)}"
            )
        self._file.close()
        os.remove(self._file_path)
        sys.exit(1)

_COMPARISONS = {
        "eq": Equals,
        "gt": GreaterThan,
        "lt": LessThan
        }
_OTHER_ONE_WORD_OPS = {
        "add": Add(),
        "sub": Subtract(),
        "neg": Negate(),
        "and": And(),
        "or": Or(),
        "not": Not(),
        "return": Return()
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
