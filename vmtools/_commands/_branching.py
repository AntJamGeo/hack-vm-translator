from abc import abstractmethod

from vmtools._commands._base import Command

class Branching(Command):
    @abstractmethod
    def __init__(self, label):
        super().__init__()
        self._label = label

class Label(Branching):
    def __init__(self, label):
        super().__init__(label)

    def _build_asm(self):
        self._asm.append(f"({self._label})")

class GoTo(Branching):
    def __init__(self, label):
        super().__init__(label)

    def _build_asm(self):
        self._asm.extend((f"@{self._label}", "0;JMP"))

class IfGoTo(Branching):
    def __init__(self, label):
        super().__init__(label)

    def _build_asm(self):
        self._asm.extend(("@SP",
                          "AM=M-1",
                          "D=M",
                          f"@{self._label}",
                          "D;JNE"))
