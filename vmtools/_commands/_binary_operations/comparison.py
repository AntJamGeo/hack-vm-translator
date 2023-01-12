from abc import abstractmethod

from vmtools._commands._binary_operations._base import BinaryOperation

class Comparison(BinaryOperation):
    _comp_op = [
            # The D-register holds arg1 and the M-register holds
            # arg2, so first find their difference and store it in D.
            "D=D-M",
            # We have an A-Instruction @COMP_TRUE.count followed by
            # a comparison command, where the value of the D-register
            # is compared to 0, and will jump to COMP_TRUE.count if
            # the comparison is true.
            # For example, if we are doing a check for whether
            # arg1 > arg2, we know that D = arg1 - arg2, so we will 
            # check whether D > 0 by using a D;JGT instruction.
            # If true, we will jump a few lines down to set D=-1
            # (indicating true), while if not, we continue to the 
            # next line to set D=0 (indicating false).
            # The final push to the stack is handled by superclass.
            None, # @COMP_TRUE.count
            None, # D;{jump operation}
            "D=0",
            None, # @COMP_PUSH.count
            "0;JMP",
            None, # (COMP_TRUE.count)
            "D=-1",
            None,  # (COMP_PUSH.count)
            ""
            ]
    _count = 0

    @abstractmethod
    def __init__(self):
        Comparison._count += 1
        Comparison._comp_op[1] = f"@COMP_TRUE.{Comparison._count}"
        Comparison._comp_op[2] = self._OP_STR
        Comparison._comp_op[4] = f"@COMP_PUSH.{Comparison._count}"
        Comparison._comp_op[6] = f"(COMP_TRUE.{Comparison._count})"
        Comparison._comp_op[8] = f"(COMP_PUSH.{Comparison._count})"
        super().__init__("\n".join(Comparison._comp_op))


class Equals(Comparison):
    _OP_STR = "D;JEQ"

    def __init__(self):
        super().__init__()

class GreaterThan(Comparison):
    _OP_STR = "D;JGT"
    
    def __init__(self):
        super().__init__()

class LessThan(Comparison):
    _OP_STR = "D;JLT"

    def __init__(self):
        super().__init__()

