import os

from _ast import Assign, ClassDef, ImportFrom
import libcst as cst

from typing import Any, List, Tuple, Dict, Optional
import ast
import astor
from pathlib import Path
from consts import SOURCE, GENERATED, GenType
from utils import get_app_file_path
from diff.diff import Diff


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

        # pprintast(node)
        return node


class SerializeTransformer(ast.NodeTransformer):
    def __init__(self, gen) -> None:
        self.gen = gen

    def change_class_name(self, node: ast.ClassDef):
        if node.name == "ModelSerializer":
            node.name = f"{self.gen.model_name}Serializer"
            return node
        return node

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
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
        with open(SOURCE / "serializers.py") as f:
            source = f.read()
        self.tree = ast.parse(source)

    def get_old_file_path(self):
        return get_app_file_path(
            filename=self.gen.model_name.lower(),
            app_path=self.gen.app_path,
            type=GenType.SERIALIZER,
        )

    def generate_serializer(self):
        # pprintast(self.tree)
        new_tree = SerializeTransformer(self.gen).visit(self.tree)
        # pprintast(new_tree)
        new_file_path = GENERATED / "serializers.py"
        with open(GENERATED / "serializers.py", "w") as f:
            f.write(astor.to_source(new_tree))
        # TODO:For now just append to the path in future we will use libsct to diff what is changed

        if not os.path.exists(self.get_old_file_path()):
            with open(self.get_old_file_path(), "a+") as f:
                f.write(astor.to_source(new_tree))

        else:
            # file does exist diff it
            d = Diff(
                old_file_path=self.get_old_file_path(),
                new_file_path=new_file_path,
                gen=self.gen,
            )
            d.serializer_diff()


if __name__ == "__main__":
    pass
