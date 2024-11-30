from tabulate import tabulate

def table_view(module):
        """
        Displays the module information as a table.
        """
        table = []

        # Adding imports Row at the top
        table.append(["Imports", ", ".join(module.imports)])

        # Adding the default code
        if module.default:
            table.append(["Default", f"{module.default}"])

        # Adding functions
        for func_name, func in module.functions.items():
            table.append([f"Function_{func_name}", f"{func.code}", f"Docstring:\n{func.docstring}"])

        # Adding classes
        for class_name, class_obj in module.classes.items():
            table.append([f"Class_{class_name}", "", f"Docstring:\n{class_obj.docstring}\nNum_Methods: {len(class_obj.functions)}"])
            for func_name, func in class_obj.functions.items():
                table.append([f"  Method_{func_name}", f"{func.code}", f"Docstring:\n{func.docstring}"])

        # Adding __main__
        if module.main:
            table.append(["Main", f"{module.main}"])

        print(tabulate(table, headers=["Type", "Code", "Extra Info"], tablefmt="fancy_grid"))