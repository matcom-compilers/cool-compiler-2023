from ast_ import *

class CILCodeGenerator:
    def __init__(self, class_references):
        self.class_references = class_references

    def generate_code(self, ast_root):
        pass
    
    # Visitor pattern
    def visit(self, node):
        pass
    
    # Atomic Expressions
    def visit_Int(self, node):
        pass

    def visit_Bool(self, node):
        pass

    def visit_String(self, node):
        pass

    def visit_Id(self, node):
        pass

    def visit_New(self, node):
        pass

    # Arithmetic Operations
    def visit_Plus(self, node):
        pass

    def visit_Minus(self, node):
        pass

    def visit_Mult(self, node):
        pass

    def visit_Div(self, node):
        pass

    # Comparison Operations
    def visit_Eq(self, node):
        pass

    def visit_Less(self, node):
        pass

    def visit_LessEq(self, node):
        pass

    # Unary Operations
    def visit_IsVoid(self, node):
        pass

    def visit_IntComp(self, node):
        pass

    def visit_Not(self, node):
        pass

    # Control Flow Operations
    def visit_If(self, node):
        pass

    def visit_While(self, node):
        pass

    # Let Expression
    def visit_LetVar(self, node):
        pass

    def visit_Let(self, node):
        pass

    # Case Expression
    def visit_CaseVar(self, node):
        pass

    def visit_CaseBranch(self, node):
        pass

    def visit_Case(self, node):
        pass

    # Dispatch Operation
    def visit_Dispatch(self, node):
        pass

    # Assignment Operation
    def visit_Assignment(self, node):
        pass

    # Block Operation
    def visit_Block(self, node):
        pass

    # Self Type Handling
    def visit_Self_Type(self, node):
        pass

    # Class Definition
    def visit_Class(self, node):
        pass

    def visit_Formal(self, node):
        pass

    def visit_Method(self, node):
        pass

    def visit_Attribute(self, node):
        pass

    

    

    

    

    

    

    

    

    

    

    