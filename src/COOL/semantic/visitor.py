from COOL.error import Error


class Visitor:

    def __init__(self, types: dict = {}):
        self.types = types
        self.basic_types: dict = {
            'object': None, 'IO': None, 'Int': None, 'String': None, 'Bool': None}
        self.types['object'] = None
        self.types['IO'] = None
        self.tree = {}# Is the tree of heritance, In each "key" there is a class and its "value" is the class from which it inherits.
        self.errors = []

    def _check_cycle(self, class_:str, node):
        temp_class = class_
        lineage = set()
        lineage.add(class_)
        while temp_class in self.tree.keys():
            # if temp_class in self.tree.keys():
            if self.types[temp_class].inherits in lineage:
                self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Class {class_}, or an ancestor of {class_}, is involved in an inheritance cycle.'))
            lineage.add(self.types[temp_class].inherits)
            temp_class = self.tree[temp_class]

    def _search_lineage(self,class_:str):
        temp_class = class_
        lineage = []
        lineage.append(class_)
        while temp_class in self.tree.keys():
            lineage.append(self.types[temp_class].inherits)
            temp_class = self.tree[temp_class]
        return lineage

    def _search_feature_name_in_lineage(self, lineage:list, feature:str, type_:type):
        feature_equals=[]
        for i in lineage:
            if not i:
                break
            for comprobate_feat in self.types.get(i).features:
                if feature == comprobate_feat.id:
                    if type(comprobate_feat) == type_:
                        feature_equals.append(comprobate_feat)
        return feature_equals
    
    def visit_program(self, node):
        for i in node.classes:
            if i.type in self.types.keys():
                #TODO search this error
                self.errors.append(Error.error(i.line,i.column,"TypeError",'Repeated class name {node.type}'))
            self.types[i.type] = i

        for cls in node.classes:
            if cls.type in self.basic_types.keys():
                self.error.append(Error.error(cls.line, cls.column, 'SemanticError',
                    f'Redefinition of basic class {cls.type}.'))
            if cls.inherits:
                if not cls.inherits in self.types.keys():
                    if cls.inherits in self.basic_types:
                        self.error.append(Error.error(cls.line, cls.column, 'InheritanceError',
                            f'Class {cls.type} cannot inherit class {cls.inherits}. '))
                    self.error.append(Error.error(cls.line, cls.column, 'TypeError',
                        f'Class {cls.type} inherits from an undefined class {cls.inherits}.'))
                self.tree[cls.type] = cls.inherits
                self._check_cycle(cls.type,cls)

    def visit_class(self, node):
        # TODO to define an error for repeated attributes and methods
        # TODO verify if the type of the attribute is defined
        # TODO veryfy if the type and the count of the formal parameters in a heritance method is the same as the original method to subscribe
        features_node = set()
        for feat in node.features:
            if feat.id in features_node:
                #TODO search an error for this
                self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Repeated feature name {feat.id} in {node.type}'))

            if feat.type not in self.types.keys() and not (feat.type in self.basic_types.keys()):
                #TODO search an error for this
                self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Undefined type {feat.type}'))

            features_node.add(feat.id)

        lineage = self._search_lineage(node.type)

        for attrb in node.attributes:
            equals_attrbs = self._search_feature_name_in_lineage(lineage,attrb.id,type(attrb))
            if len(equals_attrbs) > 0:
                equal_attrb = equals_attrbs[0]
                if attrb.type != equal_attrb.type:
                    #TODO search this error
                    self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible type of attribute in {attrb.id} in {node.type}'))
                # if attrb.expr:
                #     if not attrb.expr.type == attrb.type:
                #         #TODO search this error
                #         self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible type of attribute in {attrb.id} in {node.type}'))


        for meth in node.methods:
            equals_methods = self._search_feature_name_in_lineage(lineage, meth.id, type(meth))
            if len(equals_methods) > 0:
                equal_meth = equals_methods[0]
                if len(meth.formals) != len(equal_meth.formals):
                    #TODO search this error
                    self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible number of formals in {meth.id} in {node.type}'))
                for j in range(len(meth.formals)):
                    if meth.formals[j].type != equal_meth.formals[j].type:
                        #TODO search this error
                        self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible type of formals in {meth.id} in {node.type}'))
                if meth.type != equal_meth.type:
                    #TODO search this error
                    self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible return type in {meth.id} in {node.type}'))
            

        node.methods={i.id:i for i in node.methods}
        node.attributes={i.id:i for i in node.attributes}
        node.features = {i.id: i for i in node.features}

        # if node.inherits:
        #     for inh_attr in node.inherits.features.keys():
        #         if inh_attr in node.features.keys():
        #             if not (node.inherits.features[inh_attr].type == node.features[inh_attr].type):
        #                 self.errors.append(Error.error(node.line,node.column,'',f'Can not subscribe the attribute {inh_attr} with different type in {node.type} and {node.inherits.type}'))
        #                     f'')

    def visit_method(self, node):
        pass
    # TODO check if every expr in the method is conform with its type and every formal (variable declaration) is correct

    # def visit_variable(self, node):
    #     pass

    def visit_attribute(self, node):
        pass

        # if node.expr:
        #     if not node.expr.type == node.type:
        #         #TODO search this error
        #         self.errors.append(Error.error(node.line,node.column,'SemanticError',f'Incompatible type of attribute in {node.id} in {node.type}'))
                    
        # #TODO when an attribute does have the same static and dynamic type(or not inheritance)
        #TypeError: Inferred type F of initialization of attribute test does not conform to declared type B. 
    # def visit_expression(self, node):
    #     pass
