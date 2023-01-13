from abc import abstractmethod

from vmtools._commands._base import Command

class UnaryOperation(Command):
    @abstractmethod
    def __init__(self):
        self._asm = (
                # We simply go to the top of the stack and perform
                # the unary operation on it.
                "@SP\nA=M-1\n"
                f"{self._OP_STR}"
                )

class Negate(UnaryOperation):
    _OP_STR = "M=-M\n"

    def __init__(self):
        super().__init__()

class Not(UnaryOperation):
    _OP_STR = "M=!M\n"

    def __init__(self):
        super().__init__()

