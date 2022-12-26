# Generic Translation Error
class VMTranslatorError(Exception):
    def __init__(self, line, command, info=None):
        self.line = line
        self.command = command
        self.info = " " + info if info is not None else ""
        super().__init__(f"Bad command on line {self.line}:"
                         + f" '{self.command}'.{self.info}")

# Too Many Arguments in the Provided Command
class TooManyArgsError(VMTranslatorError):
    def __init__(self, parser):
        super().__init__(parser.line, parser.command, "Too many arguments.")

# Unrecognised Keyword Provided
class UnrecognisedKeywordError(VMTranslatorError):
    def __init__(self, parser, keyword):
        super().__init__(parser.line, parser.command,
                f"Keyword '{keyword}' not recognised.")

# Missing Argument
class MissingArgumentError(VMTranslatorError):
    def __init__(self, parser, arg_index):
        super().__init__(parser.line, parser.command,
                f"{parser.command_type} needs argument at index {arg_index}.")
