from _ast import Assign, ClassDef, ImportFrom
import libcst as cst
from parser import Parser
from utils import pprintast
from typing import Any, List, Tuple, Dict, Optional
import ast
import astor


class RewriteClassAttr(ast.NodeTransformer):

    def __init__(self, gen):
        self.gen = gen

    def change_model_name(self, node: ast.Assign):
        node.value = ast.Name(id=f"{self.gen.model_name}", ctx=ast.Load())
        return node

    def change_fields(self, node: ast.Assign, fields):
        lof = [ast.Constant(value=str(field.name)) for field in fields]
        node.value.elts = lof
        return node

    def visit_Assign(self, node: Assign) -> Any:

        if node.targets[0].id == "model":
            newNode = ast.copy_location(self.change_model_name(node), node)
            return newNode

        elif node.targets[0].id == "fields":
            newNode = ast.copy_location(self.change_fields(node, self.gen.fields), node)

        elif node.targets[0].id == "read_only_fields":

            newNode = ast.copy_location(
                self.change_fields(node, self.gen.read_only_fields), node
            )

        pprintast(node)
        print("-----------------")
        return node


class RewriteClassName(ast.NodeTransformer):
    def __init__(self, gen) -> None:
        self.gen = gen

    def change_class_name(self, node: ast.ClassDef):
        if node.name == "ModelSerializer":
            node.name = f"{self.gen.model_name}Serializer"
            return node
        return node

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        print("imports")
        pprintast(node)
        if node.module == "models":
            node.names[0].name = self.gen.model_name
        return node

    def visit_ClassDef(self, node: ClassDef) -> Any:
        newNode = ast.copy_location(self.change_class_name(node), node)
        newNode = RewriteClassAttr(self.gen).visit(newNode)
        return newNode


class GenerateSerializer:
    def __init__(self, gen) -> None:
        self.gen = gen
        with open("example_serializers.py") as f:
            source = f.read()
        self.tree = ast.parse(source)

    def get_line_start_end(self):
        for cls in self.p.classes:
            if cls.name == "ModelSerializer":
                print(cls.body)
                self.line_start = cls.lineno
                self.line_end = cls.end_lineno
                return
        raise Exception("No ModelSerializer class found")

    def generate_serializer(self):
        # pprintast(self.tree)
        print("\n")
        print("\n")
        print(self.gen.get_label())

        new_tree = RewriteClassName(self.gen).visit(self.tree)
        pprintast(new_tree)
        with open("generated/serializers.py", "w") as f:
            f.write(astor.to_source(new_tree))

        # self.p.tree

        # for node in ast.walk(self.p.tree):
        #     print(str(node))


if __name__ == "__main__":
    pass
