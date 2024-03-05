import libcst as cst
from diff.serializer import SerializerTransformer
from diff.urls import UrlDiff
from utils import danger_print


class Diff:

    def __init__(
        self,
        gen,
        old_file_path,
        new_file_path=None,
    ) -> None:

        self.old_file_path = old_file_path
        self.new_file_path = new_file_path
        self.gen = gen
        self.init_cst()

    def file_to_cst(self, path):
        with open(path, "r") as f:
            source = f.read()
            return cst.parse_module(source)

    def init_cst(self):
        self.old_cst = self.file_to_cst(self.old_file_path)
        if self.new_file_path:
            self.new_cst = self.file_to_cst(self.new_file_path)
        # print(self.old_cst)
        self.gen.str_fields = [f.name for f in self.gen.model._meta.get_fields()]

    # for serializer
    def serializer_diff(self):
        visitor = SerializerTransformer(self.gen)
        modified_tree = self.old_cst.visit(visitor)
        self.write_to_file(modified_tree)

    def write_to_file(self, modified_tree):
        with open(self.old_file_path, "w+") as f:
            danger_print(
                f"Writing to the already present file > {self.old_file_path}",
            )
            f.write(modified_tree.code)
            print("writting done")

    def url_diff(self):
        d = UrlDiff(self.gen, self.old_cst)
        changed, modified_tree = d.run()
        if changed:
            self.write_to_file(modified_tree)
        else:
            print("url already exist")
