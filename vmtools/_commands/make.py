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


def make_command(words, line, module_name):
    """Make a command.

    Parameters
    ----------
    words : list
        A list of keywords found on a line by the Parser.
    line : int
        The current line number in the input file (for locating
        errors in a .vm file).
    module_name : str
        The name of the module.

    Returns
    -------
    Command
        A command object for writing assembly code into a .asm
        file.
    """
    if words[0] in _AL_OPS:
        if len(words) != 1:
            raise Exception()
        return _AL_OPS[words[0]]
    elif words[0] == "push":
        if len(words) != 3:
            raise Exception()
        if words[1] not in _SEGMENTS:
            raise Exception()
        return Push(words[1], words[2], module_name)
    elif words[0] == "pop":
        if len(words) != 3:
            raise Exception()
        if words[1] not in _SEGMENTS or words[1] == "constant":
            raise Exception()
        return Pop(words[1], words[2], module_name)
    elif words[0] == "label":
        if len(words) != 2:
            raise Exception()
        return Label(words[1])
    elif words[0] == "goto":
        if len(words) != 2:
            raise Exception()
        return GoTo(words[1])
    elif words[0] == "if-goto":
        if len(words) != 2:
            raise Exception()
        return IfGoTo(words[1])
    elif words[0] == "call":
        if len(words) != 3:
            raise Exception()
        return Call(words[1], words[2])
    elif words[0] == "function":
        if len(words) != 3:
            raise Exception()
        return Function(words[1], words[2])
    elif words[0] == "return":
        if len(words) != 1:
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
