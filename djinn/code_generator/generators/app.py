import shutil
from typing import List

import libcst as cst
from consts import INSTALLED_APPS_SETTINGS_PATH, PARENT_PACKAGE, SOURCE
from django.conf import settings
from utils import get_assign_name

BASE_DIR = settings.BASE_DIR


class RenameApp(cst.CSTTransformer):
    def __init__(self, app_label) -> None:
        self.app_label = app_label

    def leave_Assign(
        self, original_node: cst.Assign, updated_node: cst.Assign
    ) -> (
        cst.BaseSmallStatement
        | cst.FlattenSentinel[cst.BaseSmallStatement]
        | cst.RemovalSentinel
    ):
        print(get_assign_name(updated_node))
        if get_assign_name(updated_node) == "name":
            return updated_node.with_changes(
                value=cst.SimpleString(value=f'"{self.app_label}"'),
            )
        else:
            return original_node


class TransformSettings(cst.CSTTransformer):
    def __init__(self, app_label) -> None:
        self.app_label = app_label

    def leave_Assign(
        self, original_node: cst.Assign, updated_node: cst.Assign
    ) -> (
        cst.BaseSmallStatement
        | cst.FlattenSentinel[cst.BaseSmallStatement]
        | cst.RemovalSentinel
    ):
        # comma=MaybeSentinel.DEFAULT,
        if get_assign_name(updated_node) in ["INSTALLED_APPS"]:
            # check if last element is comma or not and add the label to it
            elements: List[cst.Element] = updated_node.value.elements
            last_element: cst.Element = elements[-1]
            elements = list(elements)
            if last_element.comma == cst.MaybeSentinel.DEFAULT:
                # comma does not exisit
                pass
                last_element.comma = cst.Comma()
                last_element[-1] = last_element
            else:
                # comma does exists
                pass
            elements.append(
                cst.Element(
                    value=cst.SimpleString(f'"{self.app_label}"'), comma=cst.Comma()
                )
            )
            return updated_node.with_changes(value=cst.List(elements=tuple(elements)))

        return super().leave_Assign(original_node, updated_node)


class AppGenerator:
    def __init__(self, app_name) -> None:
        self.app_name = app_name
        self.app_label = f"{PARENT_PACKAGE}.{self.app_name}"
        self.app_folder = SOURCE / "app"
        self.new_app_folder = SOURCE / app_name

    def delete_if_folder_exists(self):
        if self.new_app_folder.exists():
            print("folder exist.Deleting....")
            shutil.rmtree(self.new_app_folder)

    def add_to_setting(self):
        with open(INSTALLED_APPS_SETTINGS_PATH, "r") as f:
            source = f.read()
        tree = cst.parse_module(source)
        ts = TransformSettings(self.app_label)
        updated_tree = tree.visit(ts)
        with open(INSTALLED_APPS_SETTINGS_PATH, "w") as f:
            f.write(updated_tree.code)

    def check_if_foldername_exists(self):
        app_folder = BASE_DIR / f"{PARENT_PACKAGE}" / f"{self.app_name}"
        return app_folder.exists()

    def copy_to_temp(self):
        self.delete_if_folder_exists()
        shutil.copytree(self.app_folder, self.new_app_folder)

    def move_to_base_dir(self):
        shutil.move(
            self.new_app_folder, BASE_DIR / f"{PARENT_PACKAGE}" / f"{self.app_name}"
        )

    def transform_and_move(self):
        app_file = self.new_app_folder / "apps.py"
        with open(app_file, "r") as f:
            source = f.read()
        tree = cst.parse_module(source)
        r = RenameApp(self.app_label)
        updated_tree = tree.visit(r)
        with open(app_file, "w") as f:
            f.write(updated_tree.code)
        self.move_to_base_dir()
