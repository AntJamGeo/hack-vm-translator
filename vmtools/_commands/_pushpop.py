from vmtools._commands._base import Command

class Push(Command):
    _OP_INDEX = 0
    _instructions = [
            None, # Places the desired data in the D-register
            # Increments the stack pointer and adds the data in the D-register
            # to the stack
            "@SP\nM=M+1\nA=M-1\nM=D\n"
            ]

    def __init__(self, segment, index, module):
        if segment == "static":
            Push._instructions[Push._OP_INDEX] = f"@{module}.{index}\nD=M\n"
        elif segment == "pointer":
            pointer = "THAT" if index == "1" else "THIS"
            Push._instructions[Push._OP_INDEX] = f"@{pointer}\nD=M\n"
        elif segment == "constant":
            Push._instructions[Push._OP_INDEX] = f"@{index}\nD=A\n"
        else:
            Push._instructions[Push._OP_INDEX] = (
                    f"{_SEGMENT_MAP[segment]}@{index}\nA=D+A\nD=M\n")
        super().__init__()

class Pop(Command):
    _LATTT_INDEX = 0
    _OP_INDEX = 2
    _instructions = [
            # For local, argument, this, that and temp segments (LATTT), some
            # instructions are needed here. The desired location of the data
            # is stored in R13.
            None,
            # Static and pointer segment commands start here as it is not
            # necessary to store the desired location in R13.
            # Decrement the stack pointer and put the data in the top of the
            # stack in the D-register to move it to the correct location.
            "@SP\nAM=M-1\nD=M\n",
            None, # Change A-register here to the desired location of storage
            "M=D\n",
            ]

    def __init__(self, segment, index, module):
        if segment == "static":
            Pop._instructions[Pop._LATTT_INDEX] = ""
            Pop._instructions[Pop._OP_INDEX] = f"@{module}.{index}\n"
        elif segment == "pointer":
            pointer = "THAT" if index == "1" else "THIS"
            Pop._instructions[Pop._LATTT_INDEX] = ""
            Pop._instructions[Pop._OP_INDEX] = f"@{pointer}\n"
        else:
            Pop._instructions[Pop._LATTT_INDEX] = (
                    f"{_SEGMENT_MAP[segment]}@{index}\nD=D+A\n@R13\nM=D\n")
            Pop._instructions[Pop._OP_INDEX] = f"@R13\nA=M\n"
        super().__init__()


_SEGMENT_MAP = {"local": "@LCL\nD=M\n",
                "argument": "@ARG\nD=M\n",
                "this": "@THIS\nD=M\n",
                "that": "@THAT\nD=M\n",
                "temp": "@5\nD=A\n"}
