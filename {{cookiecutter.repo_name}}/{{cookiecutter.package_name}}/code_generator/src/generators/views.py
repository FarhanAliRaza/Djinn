import ast
import os
from typing import TYPE_CHECKING

import libcst as cst
from consts import GENERATED, SOURCE, GenType
from libcst import BaseSmallStatement, FlattenSentinel, RemovalSentinel
from libcst.helpers import get_full_name_for_node, parse_template_statement
from utils import get_app_file_path, get_assign_name

if TYPE_CHECKING:
    from ..base import Generator


class QuerySetTransformer(cst.CSTTransformer):
    def __init__(self, model_name):
        self.model_name = model_name

    def leave_Name(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.BaseExpression:
        if get_full_name_for_node(original_node) == "Model":
            return updated_node.with_changes(value=self.model_name)
        return super().leave_Name(original_node, updated_node)


class RewriteClassAttr(cst.CSTTransformer):
    def __init__(self, gen):
        self.gen: Generator = gen

    def leave_Assign(
        self, original_node: cst.Assign, updated_node: cst.Assign
    ) -> BaseSmallStatement | FlattenSentinel[BaseSmallStatement] | RemovalSentinel:
        name = get_assign_name(original_node)

        if name == "serializer_class":
            return updated_node.with_changes(
                value=cst.Name(value=f"{self.gen.model_name}Serializer")
            )

        return super().leave_Assign(original_node, updated_node)

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.BaseStatement | FlattenSentinel[cst.BaseStatement] | RemovalSentinel:
        # print(original_node)
        if get_full_name_for_node(original_node) == "get_queryset":
            qt = QuerySetTransformer(self.gen.model_name)
            return updated_node.visit(qt)
        return super().leave_FunctionDef(original_node, updated_node)


class ViewTransformer(cst.CSTTransformer):
    def __init__(self, gen) -> None:
        self.gen: Generator = gen
        self.serializer_name = f"{self.gen.model_name}Serializer"

    def change_class_name(self, node: ast.ClassDef):
        if node.name == "ModelViewClass":
            node.name = f"{self.gen.model_name}Serializer"
            return node
        return node

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.BaseStatement | FlattenSentinel[cst.BaseStatement] | RemovalSentinel:
        if get_full_name_for_node(original_node) == "ModelViewClass":
            rca = RewriteClassAttr(self.gen)
            updated_node = original_node.visit(rca)
            return updated_node.with_changes(
                name=cst.Name(value=f"{self.gen.model_name}ViewSet")
            )

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> BaseSmallStatement | FlattenSentinel[BaseSmallStatement] | RemovalSentinel:
        if updated_node.module.value == "models":
            return updated_node.with_deep_changes(
                updated_node,
                names=[cst.ImportAlias(name=cst.Name(value=self.gen.model_name))],
            )
        elif isinstance(updated_node.module.value, cst.Name):
            name = get_full_name_for_node(updated_node.module.value)
            if name == "serializers":
                template = f"from ..serializers.{self.gen.model_name.lower()} import {self.serializer_name}"
                node = parse_template_statement(template)
                return node.body[0]
        return super().leave_ImportFrom(original_node, updated_node)

    # def visit_ClassDef(self, node: ClassDef) -> Any:
    #     newNode = ast.copy_location(self.change_class_name(node), node)
    #     newNode = RewriteClassAttr(self.gen).visit(newNode)
    #     return newNode


class GenerateView:
    def __init__(self, gen) -> None:
        self.gen: Generator = gen
        with open(SOURCE / "views.py") as f:
            source = f.read()
        self.tree = cst.parse_module(source)

    def get_old_file_path(self):
        return get_app_file_path(
            filename=self.gen.model_name.lower(),
            app_path=self.gen.app_path,
            type=GenType.VIEW,
        )

    def generate_view(self):
        # pprintast(self.tree)
        vt = ViewTransformer(self.gen)
        modified_tree = self.tree.visit(vt)
        # pprintast(new_tree)
        with open(GENERATED / "views.py", "w") as f:
            f.write(modified_tree.code)
        if not os.path.exists(self.get_old_file_path()):
            with open(self.get_old_file_path(), "a+") as f:
                f.write(modified_tree.code)

        else:
            # file does exist diff it
            pass
            # as view is the same and there are two things queryset and serializer_class
            # so like if you have changed something in the model the view remains the same mostly
            # becase i do not mention any field in the generated code for now
            # so i will not change anything here
            # d = Diff(
            #     old_file_path=self.get_old_file_path(),
            #     new_file_path=new_file_path,
            #     gen=self.gen,
            # )
            # d.serializer_diff()

        # self.p.tree

        # for node in ast.walk(self.p.tree):
        #     print(str(node))


if __name__ == "__main__":
    pass
