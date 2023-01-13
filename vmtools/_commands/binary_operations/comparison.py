from abc import abstractmethod

from vmtools._commands.binary_operations._base import BinaryOperation

class Comparison(BinaryOperation):
    _count = 0

    @abstractmethod
    def __init__(self):
        Comparison._count += 1
        self._operation = (
                # The M-register holds arg1 and the D-register holds
                # arg2, so first find their difference and store it in
                # D. We also set the M-register (which is currently
                # the top of the stack) to -1 to indicate a boolean
                # value of True.
                "D=M-D\nM=-1\n"
                # We have an A-Instruction @END_OF_COMP.count followed
                # by a comparison command, where the value of the
                # D-register is compared to 0, and will jump to the
                # end if the comparison is true, or set the top of the
                # stack to 0 if false.
                # For example, if we are doing a check for whether
                # arg1 > arg2, we know that D = arg1 - arg2, so we
                # will check whether D > 0 by using D;JGT.
                # If true, we will jump a few lines down to continue
                # to the next commands, as we already set the top of
                # the stack to -1, while if false, we will update the
                # top of the stack to hold 0 instead.
                f"@END_OF_COMP.{Comparison._count}\n{self._OP_STR}"
                "@SP\nA=M-1\nM=0\n"
                f"(END_OF_COMP.{Comparison._count})\n"
                )
        super().__init__()


class Equals(Comparison):
    _OP_STR = "D;JEQ\n"

    def __init__(self):
        super().__init__()

class GreaterThan(Comparison):
    _OP_STR = "D;JGT\n"
    
    def __init__(self):
        super().__init__()

class LessThan(Comparison):
    _OP_STR = "D;JLT\n"

    def __init__(self):
        super().__init__()

