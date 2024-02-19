from ..utils import space, danger_print
import libcst as cst
from libcst import BaseStatement, FlattenSentinel, RemovalSentinel, BaseElement
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..generator import Generator


class ListTransformerRemove(cst.CSTTransformer):
    def __init__(self, gen, custom_fields) -> None:
        self.gen = gen
        self.custom_fields = custom_fields

    def remove_quotes(self, s: str):
        return s.replace('"', "").replace("'", "")

    def leave_Element(
        self, original_node: cst.Element, updated_node: cst.Element
    ) -> BaseElement | FlattenSentinel[BaseElement] | RemovalSentinel:

        s_value = self.remove_quotes(original_node.value.value)
        if s_value in self.gen.str_fields or s_value in self.custom_fields:
            # "fields still in model do not change"
            return updated_node
        else:
            # fields is removed
            danger_print(f"Removing {s_value} field from fields in serializer")
            return original_node.deep_remove(original_node)
            # el.deep_remove(el)


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
        self.gen = gen

    def get_assign_name(self, node: cst.Assign):
        return node.targets[0].target.value

    def visit_Assign(self, node: cst.Assign) -> bool | None:
        # check if field is custom field
        # this is a hack if it is a call type it must be custom field
        if isinstance(node.value, cst.Call):
            name = self.get_assign_name(node)
            print(f"{name} is custom fields")
            self.custom_fields.append(name)

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign):
        # print(original_node, "leave assignment")
        name = self.get_assign_name(original_node)
        print(name, "hello")
        if name in self.defined:
            if name == "model":
                pass
            if name == "fields":
                print("checking fields")
                value = original_node.value
                if isinstance(value, cst.SimpleString):
                    # value is __all__
                    # dont do anything
                    pass

                elif isinstance(value, cst.List):
                    print(self.custom_fields, "custom fields")
                    # this will remove any field which is not in custom field or does not exist in the model
                    l = ListTransformerRemove(
                        gen=self.gen, custom_fields=self.custom_fields
                    )

                    return original_node.visit(l)

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
            print()
            print("-----------------------------")
            print()
            c = ClassTransformer(self.gen)
            modified_class = original_node.visit(c)
            return modified_class
        return original_node
