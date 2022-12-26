from ._commands import Command

class Parser:
    def __init__(self, file_path):
        self._file_path = file_path

    def __enter__(self):
        self._file = open(self._file_path, "r")
        self._has_more_commands = True
        self.advance()
        return self

    def __exit__(self, *args):
        self._file.close()

    def has_more_commands(self):
        return self._has_more_commands

    def advance(self):
        while True:
            line = self._file.readline()
            if line:
                self._command = strip_line(line)
                if self._command:
                    return
            else:
                self._has_more_commands = False
                return


def strip_line(line):
    """Remove any whitespace and comments from a line."""
    comment_index = line.find("//")
    if comment_index != -1:
        return line[:comment_index].strip()
    return line.strip()
