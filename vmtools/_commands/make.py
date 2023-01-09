from vmtools._commands._arithmetic import Add
from vmtools._commands._arithmetic import Subtract
from vmtools._commands._arithmetic import Negate
from vmtools._commands._arithmetic import Equals
from vmtools._commands._arithmetic import GreaterThan
from vmtools._commands._arithmetic import LessThan
from vmtools._commands._arithmetic import And
from vmtools._commands._arithmetic import Or
from vmtools._commands._arithmetic import Not
from vmtools._commands._pushpop import Push
from vmtools._commands._pushpop import Pop
from vmtools._commands._branching import Label
from vmtools._commands._branching import GoTo
from vmtools._commands._branching import IfGoTo
from vmtools._commands._function import Call
from vmtools._commands._function import Function
from vmtools._commands._function import Return


def make_command(arguments, line, file_name):
    """Make a command.

    Parameters
    ----------
    arguments : list
        A list of keywords found on a line by the Parser.
    line : int
        The current line number in the input file (for locating
        errors in a .vm file).
    file_name : string
        The name of the file (for static commands).

    Returns
    -------
    Command
        A command object for writing assembly code into a .asm
        file.
    """
    if arguments[0] in _AL_OPS:
        if len(arguments) != 1:
            raise Exception()
        return _AL_OPS[arguments[0]]
    elif arguments[0] == "push":
        if len(arguments) != 3:
            raise Exception()
        if arguments[1] not in _SEGMENTS:
            raise Exception()
        return Push(arguments[1], arguments[2], file_name)
    elif arguments[0] == "pop":
        if len(arguments) != 3:
            raise Exception()
        if arguments[1] not in _SEGMENTS or arguments[1] == "constant":
            raise Exception()
        return Pop(arguments[1], arguments[2], file_name)
    elif arguments[0] == "label":
        if len(arguments) != 2:
            raise Exception()
        return Label(arguments[1])
    elif arguments[0] == "goto":
        if len(arguments) != 2:
            raise Exception()
        return GoTo(arguments[1])
    elif arguments[0] == "if-goto":
        if len(arguments) != 2:
            raise Exception()
        return IfGoTo(arguments[1])
    elif arguments[0] == "call":
        if len(arguments) != 3:
            raise Exception()
        return Call(arguments[1], arguments[2])
    elif arguments[0] == "function":
        if len(arguments) != 3:
            raise Exception()
        return Function(arguments[1], arguments[2])
    elif arguments[0] == "return":
        if len(arguments) != 1:
            raise Exception()
        return Return()
    else:
        raise Exception()

_AL_OPS = {"add": Add(),
           "sub": Subtract(),
           "neg": Negate(),
           "eq": Equals(),
           "gt": GreaterThan(),
           "lt": LessThan(),
           "and": And(),
           "or": Or(),
           "not": Not()}
_SEGMENTS = {"local",
             "argument",
             "this",
             "that",
             "constant",
             "static",
             "temp",
             "pointer"}
