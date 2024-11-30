import os
from ..package import Package
from ..module import Module

def build_fs(folder_path, ext='py', parent_package=None, parse_module=False):
    """
    Recursively builds the file structure starting from the given folder_path.

    Args:
        folder_path (str): The root directory to start scanning.
        ext (str): File extension to filter for Modules. Defaults to 'py'.
        parent_package (Package, optional): The parent Package for recursion.

    Returns:
        Package: The root Package object representing the folder structure.
    """
    current_package = Package(folder_path, parent=parent_package)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            child_package = build_fs(item_path, ext, current_package, parse_module=parse_module)
            if child_package.children:
                current_package.add_child(child_package)
        elif item.split('.')[-1] == ext:
            module = Module(item, parent=current_package, parse=parse_module)
            current_package.add_child(module)

    return current_package