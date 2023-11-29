from errors import *
from ast_ import *

class SemanticChecker:
    def __init__(self, ast_root) -> None:
        self.ast_root = ast_root
    
    def dfs_search(self, node, seen, up):
        seen[node.type.value] = up[node.type.value] = True
        
        for child in node.children:
            if child.type.value not in seen:
                self.dfs_search(child, seen, up)
            elif up[child.type.value]:
                raise SemanticError(child.type.line, child.type.column, f'Cycle detected in class hierarchy involving {node} and {child}')
        
        up[node.type.value] = False
        
    def check_cycles(self):
        seen = {}
        up = {}
        
        for _class in self.ast_root.cls_list:
            if _class.type.value not in seen:
                self.dfs_search(_class, seen, up)