from error import Error


class Visitor:

    def __init__(self, types: dict = {}):
        self.types = types
        self.basic_types: dict = {
            'object': None, 'IO': None, 'Int': None, 'String': None, 'Bool': None}
        self.types['object'] = None
        self.types['IO'] = None
        # Is the tree of heritance, In each "key" there is a class and its "value" is the class from which it inherits.
        self.tree = {}
        self.error = Error()

    def _check_cycle(self, class_):
        temp_class = class_
        lineage = set()
        lineage.add(class_)
        while temp_class in self.tree.keys():
            if temp_class in self.tree.keys():
                if self.types[temp_class].inherits in lineage:
                    raise Exception(f'Inheritance cycle {class_}')
                lineage.add(self.types[temp_class].inherits)
                temp_class = self.tree[temp_class]

    def visit_program(self, node):
        for i in node.classes:
            if i.type in self.types.keys():
                raise Exception('Repeated class name')
            self.types[i.type] = i

        for cls in node.classes:

            if cls.inherits:
                if not cls.inherits in self.types.keys():
                    if cls.inherits in self.basic_types:
                        raise Exception(
                            f'Class {cls.type} cannot inherit class {cls.inherits}. ')
                    raise Exception(
                        f'Class {cls.type} inherits from an undefined class {cls.inherits}.')
                self.tree[cls.type] = cls.inherits
                self._check_cycle(cls.type)

    def visit_class(self, node):
        # TODO to define an error for repeated attributes and methods
        # TODO verify if the type of the attribute is defined
        # TODO veryfy if the type and the count of the formal parameters in a heritance method is the same as the original method to subscribe
        features_node = set()
        for feat in node.features:
            if feat.id in features_node:
                raise Exception(
                    f'Repeated feature name {feat.id} in {node.type}')
            if feat.type not in self.types.keys() and not (feat.type in self.basic_types.keys()):
                raise Exception(f'Undefined type {feat.type}')
            features_node.add(feat.id)

        node.features = {i.id: i for i in node.features}

        if node.inherits:
            for inh_attr in node.inherits.features.keys():
                if inh_attr in node.features.keys():
                    if not (node.inherits.features[inh_attr].type == node.features[inh_attr].type):
                        raise Exception(
                            f'Can not subscribe the attribute {inh_attr} with different type in {node.type} and {node.inherits.type}')

    def visit_method(self, node):
        pass
    # TODO check if every expr in the method is conform with its type and every formal (variable declaration) is correct

    # def visit_variable(self, node):
    #     pass

    def visit_attribute(self, node):
        if node.expr:
            if not node.expr.type == node.type:
                raise Exception(
                    f'The attribute {node.id} is not conform to the type {node.type}')

    # def visit_expression(self, node):
    #     pass
