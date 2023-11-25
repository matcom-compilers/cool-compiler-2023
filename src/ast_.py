from constants import TYPE_NOT_PRIMITIVE
from collections import deque
from collections.abc import Iterable

class ASTNode:
    def set_tracker(self, line, col):
        self.line = line
        self.col = col
    
    def set_static_type(self, t):
        self.static_type = t
        
    def get_children(self):
        if issubclass(self.__class__, Iterable):
            return list(self)
        
        attr_list = [attr for attr in self.__dict__ if isinstance(getattr(self, attr), ASTNode)]
        name_list = [getattr(self, attr) for attr in attr_list]
        
        return name_list
    
    def class_name(self):
        return self.__class__.__name__
    
    def __repr__(self) -> str:
        return f"<{self.class_name()}>"

class Formal(ASTNode):
    def __init__(self, id, type) -> None:
        self.id = id
        self.type = type
    
    def __repr__(self) -> str:
        return f"<Formal {self.id}>"

class NodeContainer(deque, ASTNode):
    def __repr__(self) -> str:
        return f"<NodeContainer({len(self)})>"

class Program(ASTNode):
    def __init__(self, cls_list = NodeContainer()) -> None:
        self.cls_list = cls_list
        
class Class(ASTNode):
    def __init__(self, type, opy_inherits = None, feat_list = NodeContainer(), can_inherit = True, reserved_attrs = [], type_obj = TYPE_NOT_PRIMITIVE) -> None:
        self.type = type
        self.opt_inherits = opy_inherits
        self.feat_list = feat_list
        self.children = []
        self.can_inherit = can_inherit
        self.methods = {}
        self.attrs = {}
        self.reserved_attrs = [AttrTypeInfo(), AttrSizeInfo()] + reserved_attrs
        self.type_obj = type_obj
        
        #type checker
        self.parent = None
        self.td = 0
        self.tf = 0
        self.level = 0
        self.self_type = None
    
    def __repr__(self) -> str:
        return f"<Class {self.type}>"

class Self_Type(Class):
    def __init__(self) -> None:
        Class.__init__(self, Type("SELF_TYPE"))
    
    def __repr__(self) -> str:
        return f"SELF_TYPE {self.parent.type}"

class Feature(ASTNode):
    pass

class Method(Feature):
    def __init__(self, id, formal_list, type, expr=None):
        self.id = id
        self.formal_list = formal_list
        self.type = type
        self.expr = expr  #None for native methods
        self._sign = tuple([ formal.type.value for formal in self.formal_list ] + [self.type.value])

    def get_signature(self):
        return self._sign

    def __repr__(self):
        return f'<Method {self.id}{self.get_signature()}>'

class Attribute(Feature):
    def __init__(self, id, type, opt_expr_init):
        self.id = id
        self.type = type
        self.opt_expr_init = opt_expr_init  #can be None
    
    def __repr__(self):
        return f'<Attribute {self.id}>'

class Expr(ASTNode):
    pass

class Assignment(Expr):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __repr__(self):
        return f'<Assignment {self.id}>'

class Dispatch(Expr):
    def __init__(self, expr, opt_type, id, expr_list = NodeContainer()):
        self.expr = expr
        self.opt_type = opt_type  #can be None
        self.id = id
        self.expr_list = expr_list

    def __repr__(self):
        return f'<Dispatch {self.id}>'

class If(Expr):
    pass

class While(Expr):
    pass

class Block(Expr):
    pass

class LetVar(Expr):
    pass

class Let(Expr):
    pass

class CaseVar(Expr):
    pass

class CaseBranch(Expr):
    pass

class Case(Expr):
    pass

class New(Expr):
    pass

class UnaryOp(Expr):
    pass

class IsVoid(UnaryOp):
    pass

class Not(UnaryOp):
    pass

class IntComp(UnaryOp):
    pass

class BinaryOp(Expr):
    pass

class Plus(BinaryOp):
    pass

class Minus(BinaryOp):
    pass

class Star(BinaryOp):
    pass

class Div(BinaryOp):
    pass

class Less(BinaryOp):
    pass

class LessEq(BinaryOp):
    pass

class Eq(BinaryOp):
    pass

class Terminal(Expr):
    pass

class Type(Terminal):
    pass

class Id(Terminal):
    pass

class Int(Terminal):
    pass

class String(Terminal):
    pass

class Bool(Terminal):
    pass

#FOR CODE GENERATION

class AttrTypeInfo:
    pass

class AttrSizeInfo:
    pass