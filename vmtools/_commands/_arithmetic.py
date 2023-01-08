from vmtools._commands._base import Command

class BinaryOperation(Command):
    _POP_ARGS = ("@SP", "AM=M-1", "D=M", "@R13", "M=D", "@SP", "A=M-1", "D=M")
    _PUSH_RESULT = ("@SP", "A=M-1", "M=D")

    def _build_asm(self, operation, comment=None):
        super()._build_asm(comment)
        self._asm.extend(BinaryOperation._POP_ARGS)
        self._asm.extend(operation)
        self._asm.extend(BinaryOperation._PUSH_RESULT)

class UnaryOperation(Command):
    _GO_TO_ARG = ("@SP", "A=M-1")
    _DO_NEG = "M=-M"
    _DO_NOT = "M=!M"

    def _build_asm(self, operation, comment=None):
        super()._build_asm(comment)
        self._asm.extend(UnaryOperation._GO_TO_ARG)
        self._asm.append(operation)

class Computation(BinaryOperation):
    _DO_ADD = ("@R13", "D=D+M")
    _DO_SUB = ("@R13", "D=D-M")
    _DO_AND = ("@R13", "D=D&M")
    _DO_OR = ("@R13", "D=D|M")

class Comparison(BinaryOperation):
    _DO_EQ = "D;JEQ"
    _DO_GT = "D;JGT"
    _DO_LT = "D;JLT"
    _count = 0

    def _build_asm(self, operation, comment=None):
        super()._build_asm(operation, comment)

    @classmethod
    def _make_operation(cls, operation):
        Comparison._count += 1
        return ("@R13", "D=D-M", f"@COMPARISON_TRUE{Comparison._count}",
                operation, "D=0", f"@COMPARISON_PUSH{Comparison._count}",
                "0;JMP", f"(COMPARISON_TRUE{Comparison._count})",
                "D=-1", f"(COMPARISON_PUSH{Comparison._count})")

    def _encode(self):
        return super()._encode(True)

class Negate(UnaryOperation):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm(UnaryOperation._DO_NEG, "// negate")

class Not(UnaryOperation):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm(UnaryOperation._DO_NOT, "// not")

class Add(Computation):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm(Computation._DO_ADD, "// add")

class Subtract(Computation):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm(Computation._DO_SUB, "// subtract")

class And(Computation):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm(Computation._DO_AND, "// and")

class Or(Computation):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm(Computation._DO_OR, "// or")

class Equals(Comparison):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        operation = Comparison._make_operation(Comparison._DO_EQ)
        super()._build_asm(operation, "// equals")

class GreaterThan(Comparison):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        operation = Comparison._make_operation(Comparison._DO_GT)
        super()._build_asm(operation, "// greater than")

class LessThan(Comparison):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        operation = Comparison._make_operation(Comparison._DO_LT)
        super()._build_asm(operation, "// less than")
