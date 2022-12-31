class Command:
    def write(self, out_file):
        out_file.write("dummy text\n")

class Arithmetic(Command):
    def __init__(self, binary):
        if binary:
            pass
        else:
            pass

class Add(Arithmetic):
    def __init__(self):
        super().__init__(True)

class Subtract(Arithmetic):
    def __init__(self):
        super().__init__(True)

class Negate(Arithmetic):
    def __init__(self):
        super().__init__(False)

class Equals(Arithmetic):
    def __init__(self):
        super().__init__(True)

class GreaterThan(Arithmetic):
    def __init__(self):
        super().__init__(True)

class LessThan(Arithmetic):
    def __init__(self):
        super().__init__(True)

class And(Arithmetic):
    def __init__(self):
        super().__init__(True)

class Or(Arithmetic):
    def __init__(self):
        super().__init__(True)

class Not(Arithmetic):
    def __init__(self):
        super().__init__(False)

class Push(Command):
    def __init__(self, segment, index):
        pass

class Pop(Command):
    def __init__(self, segment, index):
        pass


def make_command(inputs):
    if inputs[0] in _AL_OPS:
        if len(inputs) != 1:
            raise Exception()
        return _AL_OPS[inputs[0]]
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

_AL_OPS = {"add": Add(),
           "sub": Subtract(),
           "neg": Negate(),
           "eq": Equals(),
           "gt": GreaterThan(),
           "lt": LessThan(),
           "and": And(),
           "or": Or(),
           "not": Not()}
