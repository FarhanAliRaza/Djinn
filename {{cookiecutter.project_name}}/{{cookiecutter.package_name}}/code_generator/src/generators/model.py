import shutil
import sys
from pathlib import Path
from typing import List
import libcst as cst
from django.apps import apps
from rich import print
from consts import GENERATED, SOURCE

field_map = {
    "str": "models.CharField(max_length=255)",
    "text": "models.TextField()",
    "choice": "models.CharField()",
    "int": "models.IntegerField(default=0)",
    "float": "models.FloatField(default=0.0)",
    "bool": "models.BooleanField(default=False)",
    "slug": "models.SlugField(max_length=10)",
    "update": "models.DateTimeField(auto_now=True)",
    "create": "models.DateTimeField(auto_now_add=True)",
}


class ChoiceTransformer(cst.CSTTransformer):
    def __init__(self, choice_field) -> None:
        self.choice_field = choice_field

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> (
        cst.BaseStatement | cst.FlattenSentinel[cst.BaseStatement] | cst.RemovalSentinel
    ):
        name = self.choice_field["name"].capitalize()
        return updated_node.with_changes(name=cst.Name(value=f"{name}Choice"))

    def leave_IndentedBlock(
        self, original_node: cst.IndentedBlock, updated_node: cst.IndentedBlock
    ) -> cst.BaseSuite:
        newbody = []
        for idx, field in enumerate(self.choice_field["values"]):
            fi = cst.parse_statement(f"{field} = '{field}'")
            newbody.append(fi)
        return updated_node.with_changes(body=newbody)


class ModelTransormer(cst.CSTTransformer):
    def __init__(self, model_name, fields) -> None:
        self.model_name = model_name
        self.fields = fields
        print(self.fields)

    def leave_IndentedBlock(
        self, original_node: cst.IndentedBlock, updated_node: cst.IndentedBlock
    ) -> cst.BaseSuite:
        newbody = []
        for field in self.fields:
            if field["field_type"] in [
                "str",
                "text",
                "int",
                "float",
                "bool",
                "update",
                "create",
            ]:
                name = field["name"]
                dj_field = field["dj_field"]
                fi = cst.parse_statement(f"{name} = {dj_field}")
                newbody.append(fi)
            elif field["field_type"] == "choice":
                name = field["name"]
                first_value_as_default = field["values"][0]
                fi = cst.parse_statement(
                    f"{name} = models.CharField(max_length=100, choices={name.capitalize()}Choice.choices, default={name.capitalize()}Choice.{first_value_as_default})"
                )
                newbody.append(fi)

        return updated_node.with_changes(body=newbody)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> (
        cst.BaseStatement | cst.FlattenSentinel[cst.BaseStatement] | cst.RemovalSentinel
    ):
        # change name

        return updated_node.with_changes(name=cst.Name(value=f"{self.model_name}"))


class AdminTransformer(cst.CSTTransformer):
    def __init__(self, model_name) -> None:
        self.model_name = model_name

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        old_body: List[cst.SimpleStatementLine] = list(updated_node.body)
        statement = cst.parse_statement(f"from .models import {self.model_name}")
        register_statement = cst.parse_statement(
            f"admin.site.register({self.model_name})"
        )

        old_body.insert(0, statement)
        old_body.append(register_statement)
        return updated_node.with_changes(body=tuple(old_body))


class InitTransformer(cst.CSTTransformer):
    def __init__(self, model_name) -> None:
        self.model_name = model_name

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        old_body: List[cst.SimpleStatementLine] = list(updated_node.body)
        statement = cst.parse_statement(
            f"from .{self.model_name.lower()} import * # noqa: F403"
        )

        old_body.append(statement)
        return updated_node.with_changes(body=tuple(old_body))


class ModelGenerator:
    def __init__(self, app_name, model_name, fields) -> None:
        self.app_name = app_name
        self.model_name = model_name
        self.app_path: Path = Path(apps.get_app_config(self.app_name).path)
        self.fields = fields
        self.cleaned_fields = []

    def parse_field(self, field):
        # field should be name:type
        try:
            name, field_type = field.split(":")
            values = None
            if "," in field_type:
                values = field_type.split(",")
                field_type = "choice"
            dj_field = field_map.get(field_type)
            if not dj_field:
                print(
                    f"[bold red]No django field type found.'{field}' is not valid field. Valid name is[/bold red][bold green] name:type [/bold green] [bold red] valid types are {list(field_map.keys())} [/bold red]"
                )
                sys.exit()
            return {
                "name": name,
                "field_type": field_type,
                "values": values if values else [],
                "dj_field": dj_field,
            }
        except Exception as e:
            print(e)
            print(
                f"[bold red]'{field}' is not valid field. Valid name is[/bold red][bold green] name.type [/bold green] [bold red] valid types are {field_map.keys()} [/bold red]"
            )
            sys.exit()

    def parse_fields(self):
        for field in self.fields:
            self.cleaned_fields.append(self.parse_field(field))

    def create_model(self):
        with open(GENERATED / "models.py", "w") as f:
            f.write("from django.db import models\n\n")
        for field in self.cleaned_fields:
            if field["field_type"] == "choice":
                with open(SOURCE / "text_choice.py", "r") as f:
                    source = f.read()
                tree = cst.parse_module(source)
                ct = ChoiceTransformer(choice_field=field)
                updated_tree = tree.visit(ct)
                with open(GENERATED / "models.py", "a") as f:
                    f.write(updated_tree.code)

        with open(SOURCE / "models.py", "r") as f:
            source = f.read()

        tree = cst.parse_module(source)

        mt = ModelTransormer(model_name=self.model_name, fields=self.cleaned_fields)
        updated_tree = tree.visit(mt)
        with open(GENERATED / "models.py", "a") as f:
            f.write(updated_tree.code)

    def copy_over_code_to_app(self):
        shutil.move(
            GENERATED / "models.py",
            self.app_path / "models" / f"{self.model_name.lower()}.py",
        )

    def add_to_admin(self):
        file_path = self.app_path / "admin.py"

        with open(file_path, mode="r") as f:
            source = f.read()
        tree = cst.parse_module(source)
        at = AdminTransformer(self.model_name)
        updated_tree = tree.visit(at)
        with open(file_path, mode="w") as f:
            source = f.write(updated_tree.code)

    def export_model(self):
        file_path = self.app_path / "models" / "__init__.py"
        with open(file_path, mode="r") as f:
            source = f.read()
        tree = cst.parse_module(source)
        at = InitTransformer(self.model_name)
        updated_tree = tree.visit(at)
        with open(file_path, mode="w") as f:
            source = f.write(updated_tree.code)

    def check_if_file_exists(self):
        file_path = self.app_path / "models" / f"{self.model_name.lower()}.py"
        return file_path.exists()
