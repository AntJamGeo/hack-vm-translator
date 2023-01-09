from vmtools._commands._base import Command

class Call(Command):
    def __init__(self, func_name, num_args):
        super().__init__()
        self._func_name = func_name
        self._num_args = num_args

class Function(Command):
    def __init__(self, func_name, num_vars):
        super().__init__()
        self._func_name = func_name
        self._num_vars = num_vars

class Return(Command):
    def __init__(self):
        super().__init__()
