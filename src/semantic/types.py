from collections import OrderedDict


class SemanticError(Exception):
    pass


class Attribute:
    def __init__(self, name, typex, location):
        self.name = name
        self.type = typex
        self.location = location

    def __str__(self):
        return f"[attr] {self.name} : {self.type.name};"

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, params_types, return_type, location):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type
        self.location = location

    def __str__(self):
        params = ", ".join(
            f"{n}:{t.name}" for n, t in zip(self.param_names, self.param_types)
        )
        return f"[method] {self.name}({params}): {self.return_type.name};"

    def __eq__(self, other):
        return (
            other.name == self.name
            and other.return_type == self.return_type
            and other.param_types == self.param_types
        )


class Type:
    def __init__(self, name: str, defined_location=None):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.ref = True
        self.defined_location = defined_location

    def set_parent(self, parent):
        self.parent = parent

    def is_attribute_defined(self, name: str):
        try:
            self.get_attribute(name)
            return True
        except SemanticError:
            return False

    def get_attribute(self, name: str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )

    def get_attribute_parent(self, name: str):
        try:
            next(attr for attr in self.attributes if attr.name == name)
            return self
        except StopIteration:
            if self.parent is None:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )
            try:
                return self.parent.get_attribute_parent(name)
            except SemanticError:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )

    def define_attribute(self, name: str, typex, location):
        attribute = Attribute(name, typex, location)
        self.attributes.append(attribute)
        return attribute

    def is_method_defined(self, name):
        try:
            self.get_method(name)
            return True
        except SemanticError:
            return False

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def get_method_parent(self, name: str):
        try:
            next(method for method in self.methods if method.name == name)
            return self
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method_parent(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type, location
    ):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type, location)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = (
            OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        )
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return (
            other.bypass()
            or self == other
            or self.parent is not None
            and self.parent.conforms_to(other)
        )

    def bypass(self):
        return False

    @staticmethod
    def is_builtin_type(name: str):
        return name in ["Object", "IO", "Int", "String", "Bool"]

    def __str__(self):
        output = f"type {self.name}"
        parent = "" if self.parent is None else f" : {self.parent.name}"
        output += parent
        output += " {"
        output += "\n\t" if self.attributes or self.methods else ""
        output += "\n\t".join(str(x) for x in self.attributes)
        output += "\n\t" if self.attributes else ""
        output += "\n\t".join(str(x) for x in self.methods)
        output += "\n" if self.methods else ""
        output += "}\n"
        return output

    def __repr__(self):
        return str(self)


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, "<error>")

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, ErrorType)


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, "Object")

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, "Int")
        Type.set_parent(self, ObjectType())
        self.ref = False

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)


class StringType(Type):
    def __init__(self):
        Type.__init__(self, "String")
        Type.set_parent(self, ObjectType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(Type):
    def __init__(self):
        Type.__init__(self, "Bool")
        Type.set_parent(self, ObjectType())
        self.ref = False

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)


class SelfType(Type):
    def __init__(self):
        Type.__init__(self, "SELF_TYPE")

    def __eq__(self, other):
        return isinstance(other, SelfType)


class IOType(Type):
    def __init__(self):
        Type.__init__(self, "IO")
        Type.set_parent(self, ObjectType())

    def __eq__(self, other):
        return isinstance(other, IOType)
