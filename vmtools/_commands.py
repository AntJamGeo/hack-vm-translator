class Command:
    def __init__(self):
        self._asm = []
        self._asm_string = None

    @property
    def asm_string(self):
        if self._asm_string is None:
            self._asm.append("")
            self._asm_string = "\n".join(self._asm)
        return self._asm_string

    def write(self, out_file):
        out_file.write(self.asm_string)

class Arithmetic(Command):
    _POP_ARGS = ("@SP", "AM=M-1", "D=M", "@R13", "M=D", "@SP", "A=M-1", "D=M")
    _GO_TO_ARG = ("@SP", "A=M-1")
    _DO_ADD = ("@R13", "D=D+M")
    _DO_SUB = ("@R13", "D=D-M")
    _DO_NEG = "M=-M"
    _DO_EQ = "D;JEQ"
    _DO_GT = "D;JGT"
    _DO_LT = "D;JLT"
    _DO_AND = ("@R13", "D=D&M")
    _DO_OR = ("@R13", "D=D|M")
    _DO_NOT = "M=!M"
    _PUSH_RESULT = ("@SP", "A=M-1", "M=D")
    _comparison_count = 0

    def __init__(self, binary, operation, comment):
        super().__init__()
        self._asm.append(comment)
        if binary:
            self._asm.extend(Arithmetic._POP_ARGS)
            self._asm.extend(operation)
            self._asm.extend(Arithmetic._PUSH_RESULT)
        else:
            self._asm.extend(Arithmetic._GO_TO_ARG)
            self._asm.append(operation)

    @classmethod
    def _make_comparison(cls, operation):
        Arithmetic._comparison_count += 1
        return ("@R13", "D=D-M", f"@TRUE{cls._comparison_count}", operation,
                "D=0", f"@BOOL{cls._comparison_count}", "0;JMP",
                f"(TRUE{cls._comparison_count})", "D=-1",
                f"(BOOL{cls._comparison_count})")

class Add(Arithmetic):
    def __init__(self):
        super().__init__(True, Arithmetic._DO_ADD, "//add")

class Subtract(Arithmetic):
    def __init__(self):
        super().__init__(True, Arithmetic._DO_SUB, "//subtract")

class Negate(Arithmetic):
    def __init__(self):
        super().__init__(False, Arithmetic._DO_NEG, "//negate")

class Equals(Arithmetic):
    def __init__(self):
        operation = Arithmetic._make_comparison(Arithmetic._DO_EQ)
        super().__init__(True, operation, "//equals")

class GreaterThan(Arithmetic):
    def __init__(self):
        operation = Arithmetic._make_comparison(Arithmetic._DO_GT)
        super().__init__(True, operation, "//greater than")

class LessThan(Arithmetic):
    def __init__(self):
        operation = Arithmetic._make_comparison(Arithmetic._DO_LT)
        super().__init__(True, operation, "//less than")

class And(Arithmetic):
    def __init__(self):
        super().__init__(True, Arithmetic._DO_AND, "//and")

class Or(Arithmetic):
    def __init__(self):
        super().__init__(True, Arithmetic._DO_OR, "//or")

class Not(Arithmetic):
    def __init__(self):
        super().__init__(False, Arithmetic._DO_NOT, "//not")


class Push(Command):
    def __init__(self, segment, index):
        super().__init__()

class Pop(Command):
    def __init__(self, segment, index):
        super().__init__()


def make_command(command, line):
    inputs = command.split()
    if inputs[0] in _AL_OPS:
        if len(inputs) != 1:
            raise Exception()
        return _AL_OPS[inputs[0]]()
    elif inputs[0] == "push":
        if len(inputs) != 3:
            raise Exception()
        return Push(inputs[1], inputs[2])
    elif inputs[0] == "pop":
        if len(inputs) != 3:
            raise Exception()
        return Pop(inputs[1], inputs[2])
    else:
        raise Exception()

_AL_OPS = {"add": Add,
           "sub": Subtract,
           "neg": Negate,
           "eq": Equals,
           "gt": GreaterThan,
           "lt": LessThan,
           "and": And,
           "or": Or,
           "not": Not}
