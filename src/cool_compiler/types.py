from typing import Mapping, List, Tuple, Optional
from collections import deque


class StdType:
    Bool = "Bool"
    Int = "Int"
    String = "String"
    IO = "IO"
    Object = "Object"


class TypeEnvironment:
    def __init__(self, type: str):
        self.type = type
        self._object_types: Mapping[str, str] = {}
        self._method_types: Mapping[str, Tuple[List[str], str]] = {}

    def get_object_type(self, name: str):
        return self._object_types.get(name)

    def set_object_type(self, name: str, type: str):
        self._object_types[name] = type

    def get_method_type(self, name: str):
        return self._method_types.get(name)

    def set_method_type(self, name: str, type: str):
        self._method_types[name] = type

    def clone(self):
        te = TypeEnvironment(self.type)

        te._object_types = dict(**self._object_types)
        for key, value in self._method_types.items():
            te._method_types[key] = (
                value[0].copy(),
                value[1]
            )

        return te


_TYPE_TO_TE: Mapping[str, 'TypeEnvironment'] = {}
_TYPE_TO_PARENTTYPE: Mapping[str, str] = {}
_SELF_TYPE = 'SELF_TYPE'


def type_env_of(type: str):
    if type in _TYPE_TO_TE:
        return _TYPE_TO_TE[type]

    te = TypeEnvironment(type)
    _TYPE_TO_TE[type] = te
    return te


def make_inherit(type: str, parent_type: str):
    _TYPE_TO_PARENTTYPE[type] = parent_type


def inherits(type: str, parent_type: str):
    if parent_type == StdType.Object:
        return True

    t = type
    while t != None and t != StdType.Object:
        if t == parent_type:
            return True

        t = _TYPE_TO_PARENTTYPE[t]

    return False


def union_type(types: List[str]):
    type_set = set(types)
    if len(type_set) == 1:
        return type_set.pop()

    ancestors_list = []

    for type in type_set:
        ancestors = deque()

        t = type
        while True:
            parent = _TYPE_TO_PARENTTYPE.get(t)
            if parent != None:
                ancestors.appendleft(parent)
                t = parent
            else:
                break

        ancestors_list.append(ancestors)

    least_type: Optional[str] = None
    for types in zip(*ancestors_list):
        type_set = set(types)
        if len(type_set) == 1:
            least_type = type_set.pop()
        else:
            break

    return least_type if least_type != None else StdType.Object


def normalize(type: str, te: TypeEnvironment):
    return type if type != _SELF_TYPE else te.type
