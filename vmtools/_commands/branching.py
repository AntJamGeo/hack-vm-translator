from vmtools._commands._base import Command

class Label(Command):
    def __init__(self, label, function):
        # A simple enough command to not require joining a list of
        # strings together
        self._asm = f"({function}${label})\n"

class GoTo(Command):
    def __init__(self, label, function):
        # A simple enough command to not require joining a list of
        # strings together
        self._asm = f"@{function}${label}\n0;JMP\n"

class IfGoTo(Command):
    _instructions = [
            "@SP\nAM=M-1\nD=M\n",
            None,
            "D;JNE\n"
            ]

    def __init__(self, label, function):
        IfGoTo._instructions[1] = f"@{function}${label}\n"
        super().__init__()

