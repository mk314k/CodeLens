class funcObj:
    def __init__(self, code, docstring):
        self.code = code
        self.docstring = docstring


class classObj:
    def __init__(self, docstring):
        self.docstring = docstring
        self.functions = {}  # funcObj instances