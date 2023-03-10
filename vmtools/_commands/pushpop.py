from vmtools._commands._base import Command

class Push(Command):
    def __init__(self, segment, index, module):
        if segment == "static":
            load_d_register = f"@{module}.{index}\nD=M\n"
        elif segment == "pointer":
            pointer = "THAT" if index == "1" else "THIS"
            load_d_register = f"@{pointer}\nD=M\n"
        elif segment == "constant":
            load_d_register = f"@{index}\nD=A\n"
        else:
            load_d_register = (
                    f"{_SEGMENT_MAP[segment]}@{index}\nA=D+A\nD=M\n")
        self._asm = (
                # Places the desired data in the D-register.
                f"{load_d_register}"
                # Increments the stack pointer and adds the data in
                # the D-register to the stack.
                "@SP\nM=M+1\nA=M-1\nM=D\n"
                )

class Pop(Command):
    def __init__(self, segment, index, module):
        if segment == "static":
            initialisation = ""
            update_a_register = f"@{module}.{index}\n"
        elif segment == "pointer":
            pointer = "THAT" if index == "1" else "THIS"
            initialisation = ""
            update_a_register = f"@{pointer}\n"
        else:
            initialisation = (
                    f"{_SEGMENT_MAP[segment]}@{index}\nD=D+A\n@R13\nM=D\n")
            update_a_register = f"@R13\nA=M\n"
        self._asm = (
                # For local, argument, this, that and temp segments,
                # some instructions are needed here. The desired
                # location of the data is stored in R13.
                f"{initialisation}"
                # Static and pointer segment commands start here as it
                # is not necessary to store the desired location in
                # R13.
                # Decrement the stack pointer and put the data in the
                # top of the stack in the D-register to move it to the
                # correct location.
                "@SP\nAM=M-1\nD=M\n"
                # Change A-register here to the desired location of
                # storage.
                f"{update_a_register}"
                # Load the data.
                "M=D\n"
                )

_SEGMENT_MAP = {"local": "@LCL\nD=M\n",
                "argument": "@ARG\nD=M\n",
                "this": "@THIS\nD=M\n",
                "that": "@THAT\nD=M\n",
                "temp": "@5\nD=A\n"}
