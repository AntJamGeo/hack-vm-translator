class Parser:
    """
    A VM parser.

    Loads a module and extracts the commands and arguments from each
    line in the module.

    Attributes
    ----------
    has_more_commands : bool
        True if more commands are left in the module to be parsed.
    words : str
        The words found in the current command.
    line : int
        The current line number of the module being processed.

    Methods
    -------
    advance()
        Advance to the next command to be parsed. Should only be
        called if has_more_commands is True.
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._file = None
        self._has_more_commands = False
        self._words = None
        self._line = None

    def __enter__(self):
        self._file = open(self._file_path, "r")
        self._line = 0
        self._has_more_commands = True
        self.advance()
        return self

    def __exit__(self, *args):
        self._file.close()

    def advance(self):
        """
        Advance to the next command.

        Should only be called if has_more_commands is True.
        """
        while True:
            self._line += 1
            line = self._file.readline()
            if line:
                self._words = extract_words(line)
                if self._words:
                    return
            else:
                self._has_more_commands = False
                return

    @property
    def has_more_commands(self):
        return self._has_more_commands

    @property
    def words(self):
        return self._words

    @property
    def line(self):
        return self._line


def extract_words(line):
    """Extract the important information from a line of VM code."""

    # Remove any whitespace and comments from a line.
    comment_index = line.find("//")
    if comment_index != -1:
        return line[:comment_index].strip().split()
    return line.strip().split()
