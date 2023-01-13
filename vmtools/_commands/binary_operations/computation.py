from vmtools._commands.binary_operations._base import BinaryOperation

class Add(BinaryOperation):
    def __init__(self):
        self._operation = "M=D+M\n"
        super().__init__()

class Subtract(BinaryOperation):
    def __init__(self):
        self._operation = "M=M-D\n"
        super().__init__()

class And(BinaryOperation):
    def __init__(self):
        self._operation = "M=D&M\n"
        super().__init__()

class Or(BinaryOperation):
    def __init__(self):
        self._operation = "M=D|M\n"
        super().__init__()

