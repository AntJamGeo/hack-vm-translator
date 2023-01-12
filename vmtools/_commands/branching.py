from vmtools._commands._base import Command

class Label(Command):
    def __init__(self, label, function):
        self._instructions = [f"({function}${label})\n"]
        super().__init__()

class GoTo(Command):
    _instructions = [
            None,
            "0;JMP\n"
            ]

    def __init__(self, label, function):
        GoTo._instructions[0] = f"@{function}${label}\n"
        super().__init__()

class IfGoTo(Command):
    _instructions = [
            "@SP\nAM=M-1\nD=M\n",
            None,
            "D;JNE\n"
            ]

    def __init__(self, label, function):
        IfGoTo._instructions[1] = f"@{function}${label}\n"
        super().__init__()

