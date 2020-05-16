class Block:

    block: dict

    structured_types = ['list', 'set', 'queue', 'stack']

    def __init__(self):
        self.block = dict()

    def add_variable(self, var_name, var_type):
        if var_name not in self.block.keys() or (not Block.is_type_undef(var_type) and var_name in self.block.keys()):
            self.block[var_name] = var_type

    def find_variable(self, var_name):
        return var_name in self.block.keys()

    def get_type(self, var_name):
        return self.block.get(var_name, "undef")

    @staticmethod
    def is_type_structured(var_type, structured_type=None):
        if structured_type is None:
            return any([Block.is_type_structured(var_type, structured_type)
                        for structured_type in Block.structured_types])
        return isinstance(var_type, tuple) and len(var_type) == 2 and var_type[0] == structured_type

    @staticmethod
    def is_type_undef(var_type):
        if Block.is_type_structured(var_type):
            return Block.is_type_undef(var_type[1])
        return var_type == "undef"


class VarTable:

    table: list

    def __init__(self):
        self.table = []

    def enter_env(self):
        self.table.append(Block())

    def exit_env(self):
        if len(self.table) != 0:
            self.table.pop()

    def add_variable(self, var_name, var_type):
        is_exists = self.find_variable(var_name)
        if not is_exists or (is_exists and not Block.is_type_undef(var_type)):
            if len(self.table) != 0:
                self.table[-1].add_variable(var_name, var_type)

    def find_variable(self, var_name):
        for block in self.table[::-1]:
            if block.find_variable(var_name):
                return True
        return False

    def get_type(self, var_name):
        for block in self.table[::-1]:
            if block.find_variable(var_name):
                return block.get_type(var_name)
        return "undef"
