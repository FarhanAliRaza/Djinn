import libcst as cst
from .serializer import SerializerTransformer


class Diff:

    def __init__(self, old_file_path, new_file_path, gen) -> None:

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
        self.new_cst = self.file_to_cst(self.new_file_path)
        # print(self.old_cst)
        self.gen.str_fields = [f.name for f in self.gen.model._meta.get_fields()]
        print()
        print("-------------------------------")
        print()
        # print(self.new_cst)
        visitor = SerializerTransformer(self.gen)
        self.old_cst.visit(visitor)
        # transformer = SerializeTransformer(self.gen)
        # self.old_cst.visit(transformer)

    # for serializer
    def serializer_diff():
        pass
