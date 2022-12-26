class CodeWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, "w")
        return self

    def __exit__(self, *args):
        self.file.close()
