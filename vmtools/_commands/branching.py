from vmtools._commands._base import Command

class Label(Command):
    def __init__(self, label, function):
        self._asm = f"({function}${label})\n"

class GoTo(Command):
    def __init__(self, label, function):
        self._asm = f"@{function}${label}\n0;JMP\n"

class IfGoTo(Command):
    def __init__(self, label, function):
        self._asm = (
                "@SP\nAM=M-1\nD=M\n"
                f"@{function}${label}\nD;JNE\n"
                )

