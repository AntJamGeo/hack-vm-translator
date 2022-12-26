from ._commands import Command

class CodeWriter:
    def __init__(self, file_path):
        self._file_path = file_path

    def __enter__(self):
        self._file = open(self._file_path, "w")
        return self

    def __exit__(self, *args):
        self._file.close()
