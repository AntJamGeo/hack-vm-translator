from abc import abstractmethod

from vmtools._commands._base import Command

class BinaryOperation(Command):
    _instructions = [
            (
                # Pop the two arguments from the stack and decrement
                # the stack pointer by one
                "@SP\nAM=M-1\nD=M\n"
                # The second argument gets stored in R13
                "@R13\nM=D\n"
                # The first argument gets stored in the D-register
                "@SP\nA=M-1\nD=M\n"
                # Move to R13 to pick up arg2 again
                "@R13\n"
                ),
            # With arg1 in the D-register and arg2 in R13, we can
            # perform the operation by going to R13. The correct
            # operation is inserted here to complete the command's
            # translation to assembly.
            None,
            # The result is then pushed onto the stack.
            "@SP\nA=M-1\nM=D\n"
            ]

    @abstractmethod
    def __init__(self, operation):
        BinaryOperation._instructions[1] = operation
        super().__init__()

