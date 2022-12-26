from vmtools._commands import Command
from vmtools._exceptions import TooManyArgsError
from vmtools._exceptions import UnrecognisedKeywordError
from vmtools._exceptions import MissingArgumentError

class Parser:
    _CMAP = {"add": Command.ARITHMETIC,
             "sub": Command.ARITHMETIC,
             "neg": Command.ARITHMETIC,
             "eq": Command.ARITHMETIC,
             "gt": Command.ARITHMETIC,
             "lt": Command.ARITHMETIC,
             "and": Command.ARITHMETIC,
             "or": Command.ARITHMETIC,
             "not": Command.ARITHMETIC,
             "push": Command.PUSH,
             "pop": Command.POP}

    def __init__(self, file_path):
        self._file_path = file_path
        self._file = None
        self._has_more_commands = False
        self._command = None
        self._command_type = None
        self._arg1 = None
        self._arg2 = None
        self._line = None

    def __enter__(self):
        self._file = open(self._file_path, "r")
        self._line = 0
        self._has_more_commands = True
        self.advance()
        return self

    def __exit__(self, *args):
        self._file.close()

    def advance(self):
        while True:
            self._line += 1
            line = self._file.readline()
            if line:
                self._command = strip_line(line)
                if self._command:
                    self._parse()
                    return
            else:
                self._has_more_commands = False
                return

    @property
    def has_more_commands(self):
        return self._has_more_commands

    @property
    def command(self):
        return self._command

    @property
    def command_type(self):
        return self._command_type

    @property
    def arg1(self):
        if self._arg1 is None:
            raise MissingArgumentError(self)
        return self._arg1

    @property
    def arg2(self):
        if self._arg2 is None:
            raise MissingArgumentError(self)
        return self._arg2

    @property
    def line(self):
        return self._line

    def _parse(self):
        inputs = self._command.split()
        if len(inputs) > 3:
            raise TooManyArgsError(self)
        self._command_type = Parser._CMAP.get(inputs[0])
        print(self._command_type)
        if self._command_type is Command.ARITHMETIC:
            self._arg1, self._arg2 = inputs[0], None
        elif (self._command_type is Command.PUSH
                or self._command_type is Command.POP):
            self._arg1, self._arg2 = inputs[1], inputs[2]
        else:
            raise UnrecognisedKeywordError(self, inputs[0])

def strip_line(line):
    """Remove any whitespace and comments from a line."""
    comment_index = line.find("//")
    if comment_index != -1:
        return line[:comment_index].strip()
    return line.strip()
