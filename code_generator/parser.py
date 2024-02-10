import ast


class Parser:
    classes = []
    functions = []
    imports = []

    def __init__(self, code):
        self.tree = ast.parse(code)
        self.get_classes()
        self.get_functions()
        self.get_imports()

    def get_classes(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self.classes.append(node)

    def get_functions(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append(node)

    def get_imports(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                self.imports.append(node.names[0].name)
            if isinstance(node, ast.ImportFrom):
                self.imports.append(node.module)
                for alias in node.names:
                    self.imports.append(alias.name)
