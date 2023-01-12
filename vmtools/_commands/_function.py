from vmtools._commands._base import Command

class Call(Command):
    _instructions = [
            # Generate a return address label.
            None, # @label
            (
                # Push this label to the stack.
                "D=A\n@SP\nM=M+1\nA=M-1\nM=D\n"
                # Push LCL, ARG, THIS and THAT to the stack to save
                # the current state.
                "@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
                "@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
                "@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
                "@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n"
                # Save SP-5-num_args to ARG as this is the location
                # of the first argument. Start by finding SP-5.
                "@SP\nD=M\n@5\nD=D-A\n"
                ),
            # Then get the number of arguments.
            None, # @num_args
            (
                # Subtract this from the D-register and save to ARG.
                "D=D-A\n@ARG\nM=D\n"
                # Reposition LCL to SP.
                "@SP\nD=M\n@LCL\nM=D\n"
                ),
            # Now that the state has been saved, we can jump to the
            # function to execute its code.
            None, # @func_name
            "0;JMP\n",
            # Once the function has finished executing, it should
            # jump back here using the return address stored on the
            # stack. This is done by placing the return address label
            # here.
            None  # (label)
            ]
    _count = 0

    def __init__(self, func_name, num_args):
        Call._count += 1
        label = f"@{func_name}$ret.{Call._count}"
        Call._instructions[1] = f"@{num_args}\n"
        Call._instructions[3] = f"@{label}\n"
        Call._instructions[5] = f"@{func_name}\n"
        Call._instructions[7] = f"({label})\n"
        super().__init__()


class Function(Command):
    _instructions = [
            # Start with the function name label.
            None, # (func_name)
            # Then go to the stack and push num_vars local variables.
            "@SP\nA=M\n",
            None, # M=0\nAD=A+1\n repeated num_vars times
            # Update the value of the stack pointer.
            "@SP\nM=D\n"
            ]

    def __init__(self, func_name, num_vars):
        Function._instructions[0] = f"({func_name})\n"
        Function._instructions[2] = (
                "".join(["M=0\nAD=A+1\n" for _ in range(int(num_vars))]))
        super().__init__()


class Return(Command):
    _instructions = [
            (
                # Store the address at the frame's end in R13
                "@LCL\nD=M\n@R13\nM=D\n"
                # Store the return address in R14
                "@5\nA=D-A\nD=M\n@R14\nM=D\n"
                # Store the return value where argument 0 was (which will now
                # be top of the stack)
                "@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n"
                # Update stack pointer to just after the return value
                "D=A+1\n@SP\nM=D\n"
                # Restore local, argument, this and that
                "@R13\nAM=M-1\nD=M\n@THAT\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@THIS\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@ARG\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@LCL\nM=D\n"
                # Jump to the return address
                "@R14\nA=M\n0;JMP\n"
                )
            ]

    def __init__(self):
        super().__init__()

