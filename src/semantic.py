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
                raise SemanticError(child.type.line, child.type.col, f'Cycle detected in class hierarchy involving {node} and {child}')
        
        up[node.type.value] = False
        
    def check_inheritance(self):
        seen = {}
        up = {}
        
        for _class in self.ast_root.cls_list:
            if _class.type.value not in seen:
                self.dfs_search(_class, seen, up)
    
    def build_class_hierarchy(self, native_classes):
        classes_refs = {}
        
        for _class in native_classes:
            classes_refs[_class.type.value] = _class
        
        for _class in self.ast_root.cls_list:
            if _class.type.value in classes_refs:
                raise SemanticError(_class.type.line, _class.type.col, f'Class {_class} is redefined')
            
            classes_refs[_class.type.value] = _class
        
        self.ast_root.cls_list = list(self.ast_root.cls_list)
        self.ast_root.cls_list.sort(key = lambda _class: _class.type.line, reverse = True)
        
        for _class in native_classes:
            self.ast_root.cls_list.append(_class)
        
        for _class in self.ast_root.cls_list:
            for feature in _class.feat_list:
                if isinstance(feature, Method):
                    if feature.id.value in _class.methods:
                        raise SemanticError(feature.id.line, feature.id.col, f'Method {feature} is redefined in class {_class}')
                    
                    _class.methods[feature.id.value] = feature
                
                else:
                    if feature.id.value in _class.attrs:
                        raise SemanticError(feature.id.line, feature.id.col, f'Attribute {feature} is redefined in class {_class}')
            
            if _class.type.value == 'Object':
                continue
            
            name = (_class.opt_inherits or Type('Object')).value
            
            if name not in classes_refs:
                assert _class.opt_inherits
                raise TypeError(_class.opt_inherits.line, _class.opt_inherits.col, f'Class {_class} inherits from undefined class {_class.opt_inherits}')
            
            parent = classes_refs[name]
            
            if not parent.can_inherit:
                raise SemanticError(_class.opt_inherits.line, _class.opt_inherits.col, f'Class {_class} inherits from final class {parent}')
            
            parent.children.append(_class)
        
        if "Main" not in classes_refs:
            raise TypeError(1, 1, f"Class {Type('Main')} is not defined")
        
        main_class = classes_refs["Main"]
        
        if "main" not in main_class.methods:
            raise SemanticError(main_class.type.line, main_class.type.col, f"Class {main_class} does not contain method {Id('main')}")
        
        ref = main_class.methods["main"]
        
        if len(ref.get_signature()) > 1:
            raise SemanticError(ref.id.line, ref.id.col, f"Method {ref} should not receive arguments")
        
        if "SELF_TYPE" in classes_refs:
            raise SemanticError(ref.type.line, ref.type.col, f"Cannot declare {ref}")
        
        classes_refs["SELF_TYPE"] = Class(Type("SELF_TYPE"))
        
        for _class in self.ast_root.cls_list:
            _class.self_type = Self_Type()
            _class.children.append(_class.self_type)
        
        self.ast_root.cls_list.extend([_class.self_type for _class in self.ast_root.cls_list])
        
        return classes_refs