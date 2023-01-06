from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def __init__(self):
        self._require_build = True
        self._asm = []
        self._asm_string = ""

    def write(self, out_file):
        out_file.write(self._encode())

    def _encode(self, require_rebuild=False):
        if self._require_build:
            self._asm = []
            self._build_asm()
            self._asm.append("")
            self._asm_string = "\n".join(self._asm)
            self._require_build = require_rebuild
        return self._asm_string

    @abstractmethod
    def _build_asm(self, comment=None):
        if comment is not None:
            self._asm.append(comment)

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


class Push(Command):
    def __init__(self, segment, index, file_name):
        super().__init__()
        self._segment = segment
        self._index = index
        self._file_name = file_name

    def _build_asm(self):
        super()._build_asm(f"// push {self._segment} {self._index}")
        segment = _SEGMENTS[self._segment]
        if segment == "static":
            self._asm.extend((f"@{self._file_name}.{self._index}", "D=M"))
        elif segment == "pointer":
            pointer = "THAT" if self._index == "1" else "THIS"
            self._asm.extend((f"@{pointer}", "D=M"))
        elif segment == "constant":
            self._asm.extend((f"@{self._index}", "D=A"))
        else:
            register = "A" if segment == "5" else "M"
            self._asm.extend((f"@{segment}", f"D={register}",
                              f"@{self._index}", "A=D+A", "D=M"))
        self._asm.extend(_PUSH)

class Pop(Command):
    def __init__(self, segment, index, file_name):
        super().__init__()
        self._segment = segment
        self._index = index
        self._file_name = file_name

    def _build_asm(self):
        super()._build_asm(f"// pop {self._segment} {self._index}")
        segment = _SEGMENTS[self._segment]
        if segment == "static":
            self._asm.extend(_POP)
            self._asm.extend((f"@{self._file_name}.{self._index}", "M=D"))
        elif segment == "pointer":
            pointer = "THAT" if self._index == "1" else "THIS"
            self._asm.extend(_POP)
            self._asm.extend((f"@{pointer}", "M=D"))
        else:
            register = "A" if segment == "5" else "M"
            self._asm.extend((f"@{segment}",
                              f"D={register}",
                              f"@{self._index}",
                              "D=D+A",
                              "@R13",
                              "M=D"))
            self._asm.extend(_POP)
            self._asm.extend(("@R13", "A=M", "M=D"))

def make_command(arguments, line, file_name):
    if arguments[0] in _AL_OPS:
        if len(arguments) != 1:
            raise Exception()
        return _AL_OPS[arguments[0]]
    elif arguments[0] == "push":
        if len(arguments) != 3:
            raise Exception()
        if arguments[1] not in _SEGMENTS:
            raise Exception()
        return Push(arguments[1], arguments[2], file_name)
    elif arguments[0] == "pop":
        if len(arguments) != 3:
            raise Exception()
        if arguments[1] not in _SEGMENTS or arguments[1] == "constant":
            raise Exception()
        return Pop(arguments[1], arguments[2], file_name)
    else:
        raise Exception()

_AL_OPS = {"add": Add(),
           "sub": Subtract(),
           "neg": Negate(),
           "eq": Equals(),
           "gt": GreaterThan(),
           "lt": LessThan(),
           "and": And(),
           "or": Or(),
           "not": Not()}
_SEGMENTS = {"local": "LCL",
             "argument": "ARG",
             "this": "THIS",
             "that": "THAT",
             "constant": "constant",
             "static": "static",
             "temp": "5",
             "pointer": "pointer"}
_PUSH = ("@SP", "M=M+1", "A=M-1", "M=D")
_POP = ("@SP", "AM=M-1", "D=M")
