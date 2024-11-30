import os
from .package import Package
from .module import Module

def build_file_structure(folder_path, ext='py', parent_package=None):
    """
    Recursively builds the file structure starting from the given folder_path.

    Args:
        folder_path (str): The root directory to start scanning.
        ext (str): File extension to filter for Modules. Defaults to 'py'.
        parent_package (Package, optional): The parent Package for recursion.

    Returns:
        Package: The root Package object representing the folder structure.
    """
    current_package = Package(os.path.basename(folder_path), parent=parent_package)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            child_package = build_file_structure(item_path, ext, current_package)
            if child_package.children:
                current_package.add_child(child_package)
        elif item.split('.')[-1] == ext:
            module = Module(item, parent=current_package)
            module.parse(item_path)
            current_package.add_child(module)

    return current_package