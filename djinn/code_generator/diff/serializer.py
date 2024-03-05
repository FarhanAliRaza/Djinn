from utils import space, danger_print, get_assign_name
import libcst as cst
from libcst import BaseStatement, FlattenSentinel, RemovalSentinel, BaseElement
from typing import TYPE_CHECKING, List
from libcst.helpers import (
    get_full_name_for_node,
    parse_template_expression,
    parse_template_statement,
)

if TYPE_CHECKING:
    from ..base import Generator


def remove_quotes(s: str):
    return s.replace('"', "").replace("'", "")


class ListTransformerRemove(cst.CSTTransformer):
    def __init__(self, gen, custom_fields) -> None:
        self.gen = gen
        self.custom_fields = custom_fields

    def leave_Element(
        self, original_node: cst.Element, updated_node: cst.Element
    ) -> BaseElement | FlattenSentinel[BaseElement] | RemovalSentinel:

        s_value = remove_quotes(original_node.value.value)
        if s_value in self.gen.str_fields or s_value in self.custom_fields:
            # "fields still in model do not change"
            return updated_node
        else:
            # fields is removed
            danger_print(f"Removing {s_value} field from fields in serializer")
            return updated_node.deep_remove(updated_node)


class ClassTransformer(cst.CSTTransformer):

    custom_fields = []
    defined = [
        "model",
        "fields",
        "exclude",
        "depth",
        "read_only_fields",
    ]

    def __init__(self, gen) -> None:
        self.gen: Generator = gen

    def visit_Assign(self, node: cst.Assign) -> bool | None:
        # check if field is custom field

        # this is a hack if it is a call type it must be custom field
        if isinstance(node.value, cst.Call):
            name = get_assign_name(node)
            print(f"{name} is custom fields")
            self.custom_fields.append(name)

    def init_already_present_fields(self, node: cst.List):
        field_list = []
        for el in node.elements:
            field_list.append(remove_quotes(el.value.value))
        return field_list

    # creating a new list is easier then changing the list tree
    def create_new_list_node(self, fields: List[str]) -> cst.List:
        template = "["
        for f in fields:
            template += f"'{f}',"
        template += "]"
        return parse_template_expression(template)

    def add_fields(self, node: cst.List, fields) -> cst.List:
        already_present_fields = self.init_already_present_fields(node)
        if not fields:
            return node
        for field in fields:
            name = field.name
            if name in already_present_fields:
                continue
            else:
                already_present_fields.append(name)

        return self.create_new_list_node(already_present_fields)

    def transform_field(self, original_node: cst.Assign, fields):
        value = original_node.value
        if isinstance(value, cst.SimpleString):
            # value is __all__
            # dont do anything
            return original_node

        elif isinstance(value, cst.List):
            # print(self.custom_fields, "custom fields")
            # print(value, "this is the value")
            # this will remove any field which is not in custom field or does not exist in the model
            l = ListTransformerRemove(gen=self.gen, custom_fields=self.custom_fields)
            modified_list_node: cst.List = value.visit(l)
            updated_value: cst.List = self.add_fields(modified_list_node, fields)
            return original_node.with_changes(value=modified_list_node)

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign):
        # print(original_node, "leave assignment")
        name = get_assign_name(original_node)
        if name in self.defined:
            if name == "model":
                pass
            if name == "fields":
                print("checking fields")
                return self.transform_field(original_node, self.gen.fields)

            elif name == "read_only_fields":
                print("checking custom fields")
                return self.transform_field(original_node, self.gen.read_only_fields)
            elif name == "exclude":
                print("checking exclude")
                return self.transform_field(original_node, [])

        space()

        return updated_node


class SerializerTransformer(cst.CSTTransformer):

    def __init__(self, gen) -> None:
        self.gen: Generator = gen

        self.serializer_class = f"{self.gen.model_name}Serializer"

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:

        if original_node.name.value == self.serializer_class:
            c = ClassTransformer(self.gen)
            modified_class = updated_node.visit(c)
            return modified_class

        return original_node
