class Package:
    def __init__(self, path, parent=None):
        """
        Represents a folder in the file structure.

        Args:
            name (str): The name of the folder.
            parent (Package, optional): The parent Package object. Defaults to None.
        """
        self.path = path
        self.parent = parent
        self.children = []  # List of child Packages or Modules

    def __getitem__(self, index):
        return self.children[index]

    @property
    def name(self):
        return self.path.split('/')[-1]

    def add_child(self, child):
        """Adds a child (Package or Module) to the current Package."""
        self.children.append(child)

    def __str__(self, indent=0):
        """
        Returns a string representation of the Package, showing only direct children.

        Returns:
            str: The name of the package and its direct children.
        """
        result = " " * indent + f"Package: {self.name}\n"
        for child in self.children:
            if isinstance(child, Package):
                result += child.__str__(indent + 4)  # Recursive call with increased indentation
            else:
                result += " " * (indent + 4) + f"- {child.name}\n"
        return result
    __repr__ = __str__
