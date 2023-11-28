from typing import Mapping, List, Tuple, Type
from collections import deque


class StdType:
    Bool = "Bool"
    Int = "Int"
    String = "String"
    IO = "IO"
    Object = "Object"


class _TypeEnvironment:
    def __init__(self, type: str):
        self._type = type
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


TypeEnvironment = Type[_TypeEnvironment]


_TYPE_TO_TE: Mapping[str, '_TypeEnvironment'] = {}


def type_env_of(type: str):
    if type in _TYPE_TO_TE:
        return _TYPE_TO_TE[type]

    te = _TypeEnvironment(type)
    _TYPE_TO_TE[type] = te
    return te


_TYPE_TO_PARENTTYPE: Mapping[str, str] = {}


def inherits(type: str, parent_type: str):
    _TYPE_TO_PARENTTYPE[type] = parent_type


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

    least_type = StdType.Object
    for types in zip(*ancestors_list):
        type_set = set(types)
        if len(type_set) == 1:
            least_type = type_set.pop()
        else:
            break

    return least_type
