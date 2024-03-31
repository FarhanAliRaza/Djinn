from typing import TYPE_CHECKING, List

import libcst as cst
from libcst.helpers import parse_template_statement
from utils import get_assign_name

if TYPE_CHECKING:
    from ..base import Generator


class UrlTransformer(cst.CSTTransformer):
    def __init__(self, gen, add_register=False, add_import=False) -> None:
        self.gen: Generator = gen
        self.add_import = add_import
        self.add_register = add_register

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        # add import atthe top of the file sorting will be sorted by formatter
        if self.add_import:
            node = parse_template_statement(
                f"from .views.{self.gen.model_name.lower()} import {self.gen.model_name}ViewSet"
            )
            newbody = [node] + list(original_node.body)
            return updated_node.with_changes(body=tuple(newbody))
        if self.add_register:
            node = parse_template_statement(
                f'router.register(r"{self.gen.model_name.lower()}s", {self.gen.model_name}ViewSet, "{self.gen.model_name.lower()}s_viewset")'
            )
            newbody: List[cst.SimpleStatementLine] = list(original_node.body)
            insert_at = -1
            for idx, st in enumerate(newbody):
                # print(st)
                if isinstance(st.body[0], cst.Assign):
                    if get_assign_name(st.body[0]) == "urlpatterns":
                        insert_at = idx
                        break
            newbody.insert(insert_at, node)
            return updated_node.with_changes(body=tuple(newbody))
        return original_node


class UrlDiff:
    def __init__(self, gen, old_cst) -> None:
        self.gen: Generator = gen
        self.old_cst: cst.Module = old_cst

    def run(self):
        reg_str = f'router.register(r"{self.gen.model_name.lower()}s", {self.gen.model_name}ViewSet,'
        import_str = f"from .views.{self.gen.model_name.lower()} import {self.gen.model_name}ViewSet"
        modifed = False
        if import_str not in self.old_cst.code:
            modifed = True
            ut = UrlTransformer(self.gen, add_import=True, add_register=False)
            self.old_cst = self.old_cst.visit(ut)
        if reg_str not in self.old_cst.code:
            modifed = True
            ut = UrlTransformer(self.gen, add_import=False, add_register=True)
            self.old_cst = self.old_cst.visit(ut)

        return modifed, self.old_cst
