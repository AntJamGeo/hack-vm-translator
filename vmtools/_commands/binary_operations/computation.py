from abc import abstractmethod

from vmtools._commands.binary_operations._base import BinaryOperation

class Computation(BinaryOperation):
    @abstractmethod
    def __init__(self):
        super().__init__(self._OP_STR)

class Add(Computation):
    _OP_STR = "M=D+M\n"

    def __init__(self):
        super().__init__()

class Subtract(Computation):
    _OP_STR = "M=M-D\n"

    def __init__(self):
        super().__init__()

class And(Computation):
    _OP_STR = "M=D&M\n"

    def __init__(self):
        super().__init__()

class Or(Computation):
    _OP_STR = "M=D|M\n"

    def __init__(self):
        super().__init__()

