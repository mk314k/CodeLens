import ast
from ..obj import funcObj, classObj

def parse_py(file_path):
    """Parses the file to extract imports, functions, classes, and code."""
    imports = []
    classes = {}
    functions = {}
    main_code = ''
    default_code = ''

    with open(file_path, "r") as f:
        source_code = f.read()

    try:
        tree = ast.parse(source_code)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return
    
    lines = source_code.splitlines()
    used_lines = set() # Tracking lines used by functions and classes to identify "default" code

    extract_code = lambda node : "\n".join(lines[node.lineno - 1:node.end_lineno])
    
    def process_function(node):
        """Processes a function definition."""
        used_lines.update(range(node.lineno, node.end_lineno + 1))
        code = extract_code(node)
        docstring = ast.get_docstring(node)
        return funcObj(code, docstring)

          
    for node in tree.body:
        # Processing top-level imports 
        if isinstance(node, ast.Import):
            used_lines.update(range(node.lineno, node.end_lineno + 1))
            imports.append("import " + ", ".join(alias.name for alias in node.names))
        elif isinstance(node, ast.ImportFrom):
            used_lines.update(range(node.lineno, node.end_lineno + 1))
            module = node.module if node.module else ""
            imports.append(f"from {module} import " + ", ".join(alias.name for alias in node.names))

        # Processing classes and functions
        elif isinstance(node, ast.ClassDef):
            used_lines.update(range(node.lineno, node.end_lineno + 1))
            docstring = ast.get_docstring(node)
            cls_obj = classObj(docstring)
            for body_node in node.body:
                if isinstance(body_node, ast.FunctionDef):
                    cls_obj.functions[body_node.name] = process_function(body_node)
            classes[node.name] = cls_obj
        elif isinstance(node, ast.FunctionDef):
            functions[node.name] = process_function(node)

        # Processing __main__ block
        elif isinstance(node, ast.If) and hasattr(node.test, "left") and isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__":
            main_code = extract_code(node)
            used_lines.update(range(node.lineno, node.end_lineno + 1))

    # Extracting default code (code outside any function, class, or __main__)
    default_lines = [line for i, line in enumerate(lines, start=1) if i not in used_lines and line.strip()]
    default_code = "\n".join(default_lines)

    return imports, classes, functions, main_code, default_code
