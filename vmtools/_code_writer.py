from vmtools._commands import Command

class CodeWriter:
    def __init__(self, file_path):
        self._file_path = file_path

    def __enter__(self):
        self._file = open(self._file_path, "w")
        return self

    def __exit__(self, *args):
        self._file.close()

    def write_arithmetic(self, arg):
        self._file.write(arg + "\n")

    def write_push_pop(self, arg1, arg2):
        self._file.write(arg1 + " " + arg2 + "\n")
