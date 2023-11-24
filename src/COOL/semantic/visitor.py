
class Visitor:

    def __init__(self, types: dict = {'object': None, 'IO': None, 'Int': None, 'String': None, 'Bool': None}):
        self.types = types

    def visit_program(self, node):
        class_names = set()
        # TODO to define an error for repeated classes, inheritance of undefined classes and inheritance cycle
        for cls in node.classes:
            if cls.inherits and (not cls.inherits in class_names):
                raise Exception('The class it inherits from is not defined')

            if cls.type in class_names:
                raise Exception('Repeated class name')
            self.types[cls.type] = cls
            inherit_cls = []
            inherit_cls.append(cls.type)
            cls_now = cls
            while cls_now.inherits:
                if cls_now.inherits in inherit_cls:
                    raise Exception('Inheritance cycle')
                cls_now = self.types[cls_now.inherits]
                inherit_cls.append(cls_now)

            class_names.add(cls.type)

    def visit_class(self, node):
        # TODO to define an error for repeated attributes and methods
        # TODO verify if the type of the attribute is defined
        # TODO verify if exist any conflict between this attributes and inherited attributes
        features_node = set()
        for feat in node.features:
            if feat in features_node:
                raise Exception('Repeated feature name')
            if feat.type not in self.types:
                raise Exception('Undefined type')
            features_node.add(feat)
        if node.inherits:
            for inh_attr in node.inherits.features.keys():
                if inh_attr in node.attributes and not (node.inherits.attributes[inh_attr].type == node.attributes[inh_attr].type):
                    raise Exception(
                        'Can not subscribe a attribute with different type')

    def visit_method(self, node):
        pass

    def visit_variable(self, node):
        pass

    # def visit_attribute(self, node):
    #     pass

    # def visit_expression(self, node):
    #     pass
