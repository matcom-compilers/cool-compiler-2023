import itertools

from semantic.types import Type


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.class_name = None
        self.method_name = None

    def __len__(self):
        return len(self.locals)

    def create_child(self, class_name=None, method_name=None):
        child = Scope(self)
        self.children.append(child)
        child.class_name = class_name
        child.method_name = method_name
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def remove_variable(self, vname):
        self.locals = [v for v in self.locals if v.name == vname]

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itertools.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return (
                self.parent.find_variable(vname, self.index)
                if self.parent is not None
                else None
            )

    def find_variable_or_attribute(self, vname, current_type: Type):
        var = self.find_variable(vname)
        if var is None:
            if current_type.is_attribute_defined(vname):
                return current_type.get_attribute(vname)
            else:
                return None
        else:
            return var

    def is_defined(self, vname, current_type):
        return self.find_variable_or_attribute(vname, current_type) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def child_find_variable(self, vname):
        var = next(x for x in self.locals if x.name == vname)
        if var is not None:
            return self
        else:
            for child in self.children:
                child.child_find_variable(vname)
