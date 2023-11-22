
class Visitor:

    def visit_program(self,node):
        class_names = set()
        #TODO to define an error for repeated classes and inheritance of undefined classes
        for cls in node.classes:
            if not cls.inherits in class_names:
                error('the class it inherits from is not defined')
            if cls.name in class_names: 
                error('Repeated class name')
            class_names.add(cls.type)

    def visit_class(self, node):
        #TODO to define an error for repeated attributes and methods
        #TODO verify if the type of the attribute is defined
        #TODO verify if exist any conflict between this attributes and inherited attributes
        ...

    def visit_method(self, node):
        pass

    def visit_variable(self, node):
        pass

    def visit_attribute(self, node):
        pass
    
    def visit_expression(self, node):
        pass



