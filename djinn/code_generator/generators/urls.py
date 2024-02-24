from _ast import Assign, ClassDef, ImportFrom
import libcst as cst
import ast
import astor
from pathlib import Path
from ..consts import SOURCE, GENERATED, GenType
from ..utils import get_app_file_path, get_assign_name, space
import os
from ..diff.diff import Diff
from typing import TYPE_CHECKING
from libcst import (
    BaseSmallStatement,
    FlattenSentinel,
    BaseSmallStatement,
    RemovalSentinel,
)
from libcst.helpers import (
    get_full_name_for_node,
    parse_template_expression,
    parse_template_module,
    parse_template_statement,
)

if TYPE_CHECKING:
    from ..generator import Generator


class UrlTransformer(cst.CSTTransformer):
    def __init__(self, gen) -> None:
        self.gen: Generator = gen

    def leave_ImportFrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> BaseSmallStatement | FlattenSentinel[BaseSmallStatement] | RemovalSentinel:

        if isinstance(updated_node.module.value, cst.Name):
            name = get_full_name_for_node(updated_node.module.value)
            if name == "views":
                template = f"from .views.{self.gen.model_name.lower()} import {self.gen.model_name}ViewSet"
                node = parse_template_statement(template)
                return node.body[0]
        return super().leave_ImportFrom(original_node, updated_node)

    def leave_Call(
        self, original_node: cst.Call, updated_node: cst.Call
    ) -> cst.BaseExpression:

        if get_full_name_for_node(original_node) == "router.register":
            # ok now change then names
            template = f'router.register(r"{self.gen.model_name.lower()}s", {self.gen.model_name}ViewSet, "{self.gen.model_name.lower()}_view")'
            node = parse_template_expression(template)
            return node
        return super().leave_Call(original_node, updated_node)


class GenerateUrl:
    def __init__(self, gen) -> None:
        self.gen: Generator = gen
        with open(SOURCE / "urls.py") as f:
            source = f.read()
        self.tree = cst.parse_module(source)

    def get_old_file_path(self):
        return get_app_file_path(
            filename=self.gen.model_name.lower(),
            app_path=self.gen.app_path,
            type=GenType.URL,
        )

    def generate_urls(self):
        # pprintast(self.tree)
        print("\n")
        print(self.gen.get_label())
        print("\n")
        vt = UrlTransformer(self.gen)
        modified_tree = self.tree.visit(vt)
        # pprintast(new_tree)
        with open(GENERATED / "urls.py", "w") as f:
            f.write(modified_tree.code)
        print(self.get_old_file_path())
        old_file_path = self.get_old_file_path()
        if not os.path.exists(old_file_path):
            with open(old_file_path, "a+") as f:
                f.write(modified_tree.code)
        else:
            print("does  exits")
            # file does exist diff it
            d = Diff(gen=self.gen, old_file_path=old_file_path)
            d.url_diff()


if __name__ == "__main__":
    pass
