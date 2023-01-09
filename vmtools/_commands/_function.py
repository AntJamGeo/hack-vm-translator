from vmtools._commands._base import Command, PUSH

class Call(Command):
    _count = 0

    def __init__(self, func_name, num_args):
        super().__init__()
        self._func_name = func_name
        self._num_args = num_args

    def _build_asm(self):
        super()._build_asm(f"// call {self._func_name} {self._num_args}")
        Call._count += 1
        label = f"@{self._func_name}$ret.{Call._count}"
        self._asm.extend(("@SP", "D=M", f"@{self._num_args}", "D=D-A",
            "@R13", "M=D"))
        self._asm.extend((f"{label}", "D=A"))
        self._asm.extend(PUSH)
        for segment in ("LCL", "ARG", "THIS", "THAT"):
            self._asm.extend((f"@{segment}", "D=M"))
            self._asm.extend(PUSH)
        self._asm.extend(("@R13", "D=M", "@ARG", "M=D"))
        self._asm.extend(("@SP", "D=M", "@LCL", "M=D"))
        self._asm.extend((f"@{self._func_name}", "0;JMP"))
        self._asm.append(f"({label})")

class Function(Command):
    def __init__(self, func_name, num_vars):
        super().__init__()
        self._func_name = func_name
        self._num_vars = num_vars

    def _build_asm(self):
        super()._build_asm(f"// function {self._func_name} {self._num_vars}")
        self._asm.append(f"({self._func_name})")
        self._asm.extend(("@SP", "A=M"))
        for _ in range(int(self._num_vars)):
            self._asm.extend(("M=0", "AD=A+1"))
        self._asm.extend(("@SP", "M=D"))

class Return(Command):
    def __init__(self):
        super().__init__()

    def _build_asm(self):
        super()._build_asm("// return")
        self._asm.extend(("@LCL", "D=M", "@R13", "M=D"))
        self._asm.extend(("@5", "A=D-A", "D=M", "@R14", "M=D"))
        self._asm.extend(("@SP", "A=M-1", "D=M", "@ARG", "A=M", "M=D"))
        self._asm.extend(("D=A+1", "@SP", "M=D"))
        for segment in ("THAT", "THIS", "ARG", "LCL"):
            self._asm.extend(("@R13", "AM=M-1", "D=M", f"@{segment}", "M=D"))
        self._asm.extend(("@R14", "A=M", "0;JMP"))
