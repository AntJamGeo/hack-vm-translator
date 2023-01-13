from abc import abstractmethod

from vmtools._commands._base import Command

class BinaryOperation(Command):
    @abstractmethod
    def __init__(self):
        self._asm = (
                # Decrement stack pointer by one. Put arg2 in the
                # D-register, then decrement the A-register by one so
                # that the M-register contains arg1.
                "@SP\nAM=M-1\nD=M\nA=A-1\n"
                # The correct operation is inserted here to complete
                # the command's translation to assembly.
                f"{self._operation}"
                )

