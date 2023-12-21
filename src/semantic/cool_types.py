from src.utils.errors import *
from semantic import *

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        if parent.name == 'String' or parent.name == 'Int' or parent.name == 'Bool':
            raise SemanticError(f'Invalid parent type, cannot inherit from {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)


class ObjectType(Type):
    def __init__(self, pos):
        super.__init__(self)
        self.name = 'Object'
        self.methods()

    def methods(self):
        self.define_method(name='abort', param_names=[], param_types=[], return_type=self)
        self.define_method(name='type_name', param_names=[], param_types=[], return_type=StringType())
        self.define_method(name='copy', param_names=[], param_types=[], return_type=SelfType())
        
    
    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, ObjectType)
    
class IOType(Type):
    def __init__(self):
        super().__init__(self)
        self.name = 'IO'
        self.methods()

    def methods(self):
        self.define_method(name='out_string', param_names=['x'], param_types=[StringType()], return_type=SelfType())
        self.define_method(name='out_string', param_names=['x'], param_types=[IntType()], return_type=IntType())
        self.define_method(name='in_string', param_names=[], param_types=[], return_type=StringType())
        self.define_method(name='in_int', param_names=[], param_types=[], return_type=IntType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IOType)


class StringType(Type):
    # default = ''
    def __init__(self):
        super().__init__()
        self.name = 'String'
        self.methods() 
    
    def methods(self):
        self.define_method(name='length', param_names=[], param_types=[], return_type=IntType())
        self.define_method(name='concat', param_names=['s'], param_types=[self], return_type=self)
        self.define_method(name='substr', param_names=['i', 'l'], param_types=[IntType(), IntType()], return_type=self)
    

    def conforms_to(self, other):
        return other.name == 'Object' or other.name == self.name

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, StringType)



class IntType(Type):
    # default = 0
    def __init__(self):
        super().__init__(self)
        self.name = 'Int'
    
    def conforms_to(self, other):
        return other.name == 'Object' or other.name == self.name

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IntType)


class BoolType(Type):
    # default = false
    def __init__(self):
        super().__init__(self)
        self.name = 'Bool'

    
    def conforms_to(self, other):
        return other.name == 'Object' or other.name == self.name

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, BoolType)
 

class SelfType(Type):
    def __init__(self):
        super().__init__(self)
        self.name = 'SELF_TYPE'

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, SelfType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, SelfType)

