from typing import Optional


class Scope:
    def __init__(self, parent_scope: Optional["Scope"] = None):
        self._vars = {}
        self._parent = parent_scope

    def get_var(self, name: str, recursive=True):
        var = self._vars.get(name)
        if var != None:
            return var

        if recursive and self._parent != None:
            return self._parent.get_var(name, recursive)

        return None

    def set_var(self, name: str, var, recursive: bool):
        if name in self._vars:
            self._vars[name] = var
        elif recursive and self._parent != None:
            self._parent.set_var(name, var, recursive)
