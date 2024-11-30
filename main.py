import os
from src import build_file_structure


if __name__ == '__main__':
    folder_path = "."  # Replace with your folder path
    if os.path.exists(folder_path):
        root_package = build_file_structure(folder_path)
        print(root_package)  # Prints the root package and its direct children
    else:
        print(f"The folder path '{folder_path}' does not exist.")