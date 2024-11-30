from .visualization import table_view
from .parser.fs_module import parse_py

class Module:
    def __init__(self, name, parent, parse=False):
        """
        Represents a file in the file structure.

        Args:
            name (str): The name of the file.
            parent (Package): The parent Package object.
        """
        self.name = name
        self.parent = parent
        self.parsed = parse
        if parse: self.parse()

    def __getitem__(self, index):
        return self.children[index]

    @property
    def path(self):
        return f'{self.parent.path}/{self.name}'

    def parse(self):
        self.imports = []
        self.functions = {}
        self.classes = {}
        self.main = ""  # Code under __main__ block
        self.default = ""  # Code outside any function/class/__main__

        self.imports, self.classes, self.functions, self.main, self.default = parse_py(self.path)
        self.parsed = True

    def __str__(self):
        """String representation of the Module."""
        if not self.parsed : return self.name
        result = f"Module: {self.name}\n"
        result += f"  Imports: {self.imports}\n"
        result += f"  Functions: {[func for func in self.functions]}\n"
        result += f"  Classes: {[clas for clas in self.classes]}\n"
        result += f"  Main: {self.main}\n"
        result += f"  Default: {self.default}\n"
        return result
    __repr__ = __str__

    def view(self):
        if self.parsed:
            table_view(self)
