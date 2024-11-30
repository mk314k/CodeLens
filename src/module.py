import ast
from .obj import funcObj, classObj

class Module:
    def __init__(self, name, parent):
        """
        Represents a file in the file structure.

        Args:
            name (str): The name of the file.
            parent (Package): The parent Package object.
        """
        self.name = name
        self.parent = parent
        self.imports = []  # List of import strings
        self.functions = {}  # funcObj instances
        self.classes = {}  # classObj instances
        self.main = ""  # Code under __main__ block
        self.default = ""  # Code outside any function/class/__main__

    def parse(self, file_path):
        """Parses the file to extract imports, functions, classes, and code."""
        with open(file_path, "r") as f:
            source_code = f.read()

        try:
            tree = ast.parse(source_code)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return

        # Track lines used by functions and classes to identify "default" code
        used_lines = set()

        # Process top-level imports
        for node in tree.body:
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self.imports.append(self._get_import_string(node))

        # Process classes and functions
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                self.classes[node.name] = self._process_class(node, source_code, used_lines)
            elif isinstance(node, ast.FunctionDef):
                self.functions[node.name]=self._process_function(node, source_code, used_lines)

        # Process __main__ block
        for node in tree.body:
            if isinstance(node, ast.If) and hasattr(node.test, "left") and isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__":
                self.main = self._extract_code(node, source_code)
                used_lines.update(range(node.lineno, node.end_lineno + 1))

        # Extract default code (code outside any function, class, or __main__)
        self.default = self._extract_default_code(source_code, used_lines)

    def _get_import_string(self, node):
        """Extracts import statements as strings."""
        if isinstance(node, ast.Import):
            return "import " + ", ".join(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            return f"from {module} import " + ", ".join(alias.name for alias in node.names)

    def _process_class(self, node, source_code, used_lines):
        """Processes a class definition."""
        used_lines.update(range(node.lineno, node.end_lineno + 1))
        docstring = ast.get_docstring(node)
        cls = classObj(docstring)
        for body_node in node.body:
            if isinstance(body_node, ast.FunctionDef):
                cls.functions[body_node.name] = self._process_function(body_node, source_code, used_lines)
        return cls

    def _process_function(self, node, source_code, used_lines):
        """Processes a function definition."""
        used_lines.update(range(node.lineno, node.end_lineno + 1))
        code = self._extract_code(node, source_code)
        docstring = ast.get_docstring(node)
        return funcObj(code, docstring)

    def _extract_code(self, node, source_code):
        """Extracts the code corresponding to an AST node."""
        lines = source_code.splitlines()
        return "\n".join(lines[node.lineno - 1:node.end_lineno])

    def _extract_default_code(self, source_code, used_lines):
        """Extracts code outside any function, class, or __main__ block."""
        lines = source_code.splitlines()
        default_lines = [
            line for i, line in enumerate(lines, start=1) if i not in used_lines and line.strip()
        ]
        return "\n".join(default_lines)

    def __str__(self):
        """String representation of the Module."""
        result = f"Module: {self.name}\n"
        result += f"  Imports: {self.imports}\n"
        result += f"  Functions: {[func.code for func in self.functions]}\n"
        result += f"  Classes: {[cls.docstring for cls in self.classes]}\n"
        result += f"  Main: {self.main}\n"
        result += f"  Default: {self.default}\n"
        return result
    __repr__ = __str__