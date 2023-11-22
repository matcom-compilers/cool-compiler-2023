
class Visitor:

    def visit_program(self,node):
        class_names = set()
        #TODO to define an error for repeated classes and inheritance of undefined classes
        for cls in node.classes:
            if cls.inherited in class_names: pass
            else: error('Undefined inheritance class')
            if cls.name in class_names: 
                error('Repeated class name')

    def visit_class(self, node):
        pass

    def visit_method(self, node):
        pass

    def visit_variable(self, node):
        pass

    def visit_attribute(self, node):
        pass
    
    def visit_expression(self, node):
        pass



