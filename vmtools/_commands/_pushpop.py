from vmtools._commands._base import Command, PUSH, POP

class Push(Command):
    def __init__(self, segment, index, file_name):
        super().__init__()
        self._segment = segment
        self._index = index
        self._file_name = file_name

    def _build_asm(self):
        super()._build_asm(f"// push {self._segment} {self._index}")
        if self._segment == "static":
            self._asm.extend((f"@{self._file_name}.{self._index}", "D=M"))
        elif self._segment == "pointer":
            pointer = "THAT" if self._index == "1" else "THIS"
            self._asm.extend((f"@{pointer}", "D=M"))
        elif self._segment == "constant":
            self._asm.extend((f"@{self._index}", "D=A"))
        else:
            segment, register = _SEGMENT_MAP[self._segment]
            self._asm.extend((f"@{segment}", f"D={register}",
                              f"@{self._index}", "A=D+A", "D=M"))
        self._asm.extend(PUSH)

class Pop(Command):
    def __init__(self, segment, index, file_name):
        super().__init__()
        self._segment = segment
        self._index = index
        self._file_name = file_name

    def _build_asm(self):
        super()._build_asm(f"// pop {self._segment} {self._index}")
        if self._segment == "static":
            self._asm.extend(POP)
            self._asm.extend((f"@{self._file_name}.{self._index}", "M=D"))
        elif self._segment == "pointer":
            pointer = "THAT" if self._index == "1" else "THIS"
            self._asm.extend(POP)
            self._asm.extend((f"@{pointer}", "M=D"))
        else:
            segment, register = _SEGMENT_MAP[self._segment]
            self._asm.extend((f"@{segment}",
                              f"D={register}",
                              f"@{self._index}",
                              "D=D+A",
                              "@R13",
                              "M=D"))
            self._asm.extend(POP)
            self._asm.extend(("@R13", "A=M", "M=D"))

_SEGMENT_MAP = {"local": ("LCL", "M"),
                "argument": ("ARG", "M"),
                "this": ("THIS", "M"),
                "that": ("THAT", "M"),
                "temp": ("5", "A")}
