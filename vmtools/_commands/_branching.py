from vmtools._commands._base import Command

class Label(Command):
    def __init__(self, label):
        self._instructions = [f"({label})\n"]
        super().__init__()

class GoTo(Command):
    _instructions = [
            None,
            "0;JMP\n"
            ]

    def __init__(self, label):
        GoTo._instructions[0] = f"@{label}\n"
        super().__init__()

class IfGoTo(Command):
    _instructions = [
            "@SP\nAM=M-1\nD=M\n",
            None,
            "D;JNE\n"
            ]

    def __init__(self, label):
        IfGoTo._instructions[1] = f"@{label}\n"
        super().__init__()

