import compiler.AST.environment as env
from compiler.AST.ast import CoolProgram, CoolClass, Feature, expr, IntNode, CoolBool, CoolString, CoolLet, ArithmeticOP,Logicar,Assign, CoolID, Context, Dispatch, CoolCase, CoolWhile, CoolIf, CoolBlockScope, CoolCallable, CoolNew

import colorama
from colorama import Fore
colorama.init()
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
count_colors = 0
def get_color():
    global colors
    global count_colors
    count_colors= (1+count_colors)%6
    return colors[count_colors]

#esto es para usar operaciones con valores inmediatos, por ejemplo addi $s0, $1, 5 . Las constantes solo admiten 16 bytes. Valor default = False
USE_i = True

#Esto hace que se reserve pila de forma dinamica y no total. Por ejemplo en let x:int<-1, a:int <- (let <expr>), b:int.... En este caso se reserva memoria para x, luego se reserva para a y luego para b, dado que en el llamado del le que se le asigna a `a` no nos interesa la variable b, pero si la variable x, por lo tanto no se reserva memoria que no se usara en ese llamado. La forma standar sera reservar toda la memoria necesaria para cada varaible del let, DEFAULT = False
DYNAMIC_STACK = True

TYPE_LENGTH= {'Int':4, 'Bool':4, 'String':32,}
TYPES = {}

class CILProgram():
    def __init__(self, program:CoolProgram):
        super().__init__()
        self.types:dict[str,CILType] = {}  # Lista de CILType
        self.methods:list[CILMethod] = []
        self.set_types(program)
        self.generate_methods(program)

    def set_types(self, program:CoolProgram):
        for cclass in program.classes:
            if not cclass.type in env.base_classes:
                self.types[cclass.type]=CILType(cclass)

    def __str__(self) -> str:
        result = ".TYPES\n\n"
        for type in self.types.values():
            result+= str(type)
        result += ".TEXT\n\n"
        for meth in self.methods:
            result+= str(meth)
        return result
    
    def generate_methods(self, cool_program:CoolProgram):
        for cclass in cool_program.classes:
            if cclass.type == 'Main':
                for feature in cclass.features:
                    if isinstance(feature,Feature.CoolDef) and feature.ID.id == 'main':
                        self.methods.append(CILMethod(feature, self))

        for cclass in cool_program.classes:
            if not cclass.type in env.base_classes:
                for feature in cclass.features:
                    if isinstance(feature,Feature.CoolDef):
                        if not(cclass.type == 'Main' and feature.ID.id == 'main'):
                            self.methods.append(CILMethod(feature, self))
    
class CILType():
    def __init__(self, cclass:CoolClass):
        self.name = cclass.type
        self.methods:list[CILId] = []  # Lista de CILMethod
        self.attributes:list[CILVar] = []  # Lista de CILAttribute
        self.atrs = {}
        self.space = self.get_all_from(cclass)
        TYPES[self.name] = self

    def get_all_from(self, cclass:CoolClass):
        self.process_class(cclass)
        return self.set_space()

    def set_space(self):
        result = 0
        for atr in self.attributes:
            result += atr.space
            
        # for met in self.methods:
        #     result += met.space
        TYPE_LENGTH[self.name] = result
    
    def process_class(self,cclass:CoolClass):
        if cclass.type != env.object_type_name:
            self.process_class(cclass.inherit_class)

        for feature in cclass.features:
            space = 0
            if isinstance(feature,Feature.CoolAtr):
                self.atrs[feature.ID.id] = space 
                # if feature.get_type == env.string_type_name:
                #     self.attributes.append(CILVar(f'{self.name}_{feature.ID.id}', value=feature.value,space=32))
                #     space += 32
                # else:
                self.attributes.append(CILVar(f'{self.name}_{feature.ID.id}', value=feature.value,space=4))
                space += 4
            else:    
                self.methods.append(CILId(f'{self.name}_{feature.ID.id}')) #Esto apunta a una dirccion de memoria y su tamanno siempre es 4 bytes
    
    def __str__(self) -> str:
        result = f'\n.{self.name}'+' {\n'
        for atr in self.attributes:
            result+= f'\tattribute {atr};\n'
        for met in self.methods:
            result+= f'\tmethod {met};\n'
        return result +'}\n'

class CILMethod():
    def __init__(self, cool_meth: Feature.CoolDef, cil_program: CILProgram):
        super().__init__()
        self.name = f'{cool_meth.father.type}_{cool_meth.ID.id}'
        self.body:list[CILExpr] = []  # Lista de CILExpr, representa el cuerpo del método
        self.params:list[CILId] = []
        self.locals:list[CILVar] = []
        self.context = {}
        self.set_vars(cool_meth, cil_program)
        self.set_body(cool_meth)
    
    def set_vars(self, cool_meth:Feature.CoolDef, cil_program:CILProgram):
        # for atr in cil_program.types[cool_meth.father.type].attributes:
        #     self.locals.append(atr)
        #     self.context[atr.id.id] = pos
        #     pos+=4
        
        #el scope del metodo posee los parametros, los parametros estaran en orden en la pila. El contexto define la posicion del parametro en la pila     
        #queda por parte del invocador guardar los valores que se le pasan por parametros y la instancia en la pila. Esto se hace en el callable
        self.context[env.self_name] = 0
        pos= 0
        for param in cool_meth.params.childs():
            self.params.append(param)
            pos+=4
            self.context[param.id] = pos
        
    def set_body(self, cool_meth:Feature.CoolDef):    
        body = Body()
        DivExpression(cool_meth.scope, body, self.context)
        self.body = [e for e in body.expressions if e.use_in_code_line]
        if self.name != 'Main_main':
            self.body.insert(0,Label(self.name))
        else:
            self.body.insert(0,Label('main'))
        
        if self.name == 'Main_main':
            self.body.append(CloseProgram(body.return_value()))
        else:    
            self.body.append(CILReturn(body.return_value()))
        

    def __str__(self) -> str:
        result = str(self.body[0])
        result += '{\n'
        for local in self.locals:
            result+= f'\tLocal {local};\n'
        for param in self.params:
            result+= f'\tParam {param};\n'
        i = 0
        for e in self.body:
            if i > 0:
                if isinstance (e,CILCommet):
                    result+= f'\t{e}\n'
                else:
                    result+= f'\t{e};\n'
            i+=1
        return result +'}\n'

class TempNames:
    used_id = [False, False,False, False, False, False, False, False, False]

    def get_name():
        for i in range(len(TempNames.used_id)):
            if not TempNames.used_id[i]:
                TempNames.used_id[i]= True
                return f"temp_{i}"
        else:    
            TempNames.used_id.append(True)
            return f"expr_{len(TempNames.used_id)-1}"
    
    def free(names:list):
        for name in names:
            if name == 'a0': continue
            id = int(name[5:])
            TempNames.used_id[id] = False
    def free_all():
        TempNames.used_id = [False, False,False, False, False, False, False, False, False]

class NameTempExpression:
    id = -1  # Contador para generar identificadores
    def get_name():
        NameTempExpression.id+=1
        return f"expr_{NameTempExpression.id}"

class NameLabel():
    label_id:dict[str:int] = {}  # Contador para generar identificadores
    def __init__(self, label = 'else') -> None:
        self.label = label
        if NameLabel.label_id.__contains__(label):
            NameLabel.label_id[label]+=1
        else:
            NameLabel.label_id[label]=0
    
    def get(self):
        return f"{self.label}_{NameLabel.label_id[self.label]}"

class CILExpr():
    def __init__(self) -> None:
        self.use_in_code_line = True
        self.tab_lv = 0
        self.return_void = False

    def add_tab_lv(self):
        self.tab_lv+=1    

class CILVoid(CILExpr):
    def __init__(self) -> None:
        super().__init__()
        self.return_void = True
        self.use_in_code_line = False

class Label(CILExpr):
    def __init__(self, name_label) -> None:
        super().__init__()
        self.name = name_label + ':'

    def __str__(self) -> str:
        # return f"{Fore.MAGENTA}{self.name}{Fore.WHITE}"
        return f"{self.name}"
    def __repr__(self) -> str:
        return self.__str__()
    
class CILId(CILExpr):
    def __init__(self, name):#, space = 4) -> None:
        super().__init__()
        self.use_in_code_line = False #esto implica que estara en el cuerpo que se esta analizando para tenerlo presente como valor de retorno, pero no se usa en el codigo, salvo en el caso exepcional de usarlo de return.
        self.name = name
        self.dest = name
        self.space = 4

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return str(self)

class CILVar(CILId):
    def __init__(self, name, space=4, value = None) -> None:
        super().__init__(name)
        self.space = space
        self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return f'{self.name}'
        else:
            return f'{self.name} = {self.value}'
            
    def __repr__(self) -> str:
        return str(self)

class CILReturn(CILExpr):
    def __init__(self, e) -> None:
        self.ret = e
    def __str__(self) -> str:
        return f'return {self.ret}'
    def __repr__(self) -> str:
        return self.__str__()    

class CILAttribute():
    def __init__(self, name):
        super().__init__()
        self.name = name

class CILAssign(CILExpr):
    def __init__(self, dest:str, source, is_temp = True):
        super().__init__()
        self.dest:str = dest      # Vrle a la que se asigna el valor
        # self.dest:CILVar = CILVar(dest)      # Vrle a la que se asigna el valor
        self.source:CILExpr = source  # Expresin que se asigna a la variable
        self.is_temp = is_temp

    def __str__(self):
        return f"{self.dest} = {self.source}"
    def __repr__(self) -> str:
        return self.__str__()

class CILArithmeticOp(CILExpr):
    def __init__(self, left, right, operation, constant = False):
        super().__init__()
        self.left = left       # lado izquierdo
        self.right = right     # lado derecho
        self.operation = operation  #('+', '-', '*', '/')
        self.constant = constant

    def __str__(self):
        return f"{self.left} {self.operation} {self.right}"
    def __repr__(self) -> str:
        return self.__str__()
    
class CILLogicalOP(CILExpr):
    def __init__(self,left, right, operation):
        super().__init__()
        self.operation = operation
        self.left = left   
        self.right = right

    def __str__(self):
        return f"{self.left} {self.operation} {self.right}"
    def __repr__(self) -> str:
        return self.__str__()

class CILIf(CILExpr):
    def __init__(self, condition, else_label, _while = False):
        super().__init__()
        self._while = _while
        self.condition = condition
        self.else_label = else_label 
        # self.then_label = then_label

    def __str__(self):
        # return f'if not {self.condition} GOTO {Fore.MAGENTA}{self.else_label}{Fore.WHITE}'
        return f'if not {self.condition} GOTO {self.else_label}'
    def __repr__(self) -> str:
        return self.__str__()

class CILWhile(CILExpr):
    
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition  # Expresn que determina el bucle
        self.body = body           

    def __str__(self):
        body_str = " ".join(str(node) for node in self.body)
        return f"while {self.condition.get_id()} loop {body_str} pool"

class CILCallLocal(CILExpr):
    def __init__(self, id:CoolID, pos) -> None:
        super().__init__()
        self.name = id.id
        self.pos = pos #esta es la posicion relativa en la pila.

    def __str__(self) -> str:
        return f'GETLOCAL {self.name}({self.pos})'
    
    def __repr__(self) -> str:
        return self.__str__()

class CILCallAtr(CILExpr):
    def __init__(self, id:CoolID) -> None:
        super().__init__()
        self.name = id.id
    def __str__(self) -> str:
        return f'GETATTR {self.name}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
class CILCall(CILExpr):
    def __init__(self, instance, method, arguments):
        super().__init__()
        self.instance = instance  
        self.method = method     
        self.arguments = arguments 

    def __str__(self):
        args_str = ", ".join(arg.get_id() for arg in self.arguments)
        return f"{self.get_id()} = call {self.instance.get_id()}.{self.method}({args_str})"

class CILBlock(CILExpr):

    def __init__(self, instructions):
        super().__init__()
        self.instructions = instructions  # instruccion de bloq

    def __str__(self):
        instr_str = " ".join(str(instr) for instr in self.instructions)
        return f"{{ {instr_str} }}"

class CILAllocate(CILExpr):
    
    def __init__(self, type_name):
        super().__init__()
        self.type_name = type_name  # El nombre del tipo que se asigna memoria

    def __str__(self):
        return f"{self.get_id()} = ALLOCATE {self.type_name}"

class CILFree(CILExpr):
    
    def __init__(self, instance):
        super().__init__()
        self.instance = instance  # La instancia de memoria qse libera

    def __str__(self):
        return f"FREE {self.instance.get_id()}"

class CILCommet(CILExpr):
    def __init__(self, text = '#comment') -> None:
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        result = self.text
        # result = Fore.GREEN + self.text + Fore.WHITE
        return result
    def __repr__(self) -> str:
        return str(self)

class GOTO(CILExpr):
    def __init__(self, label) -> None:
        super().__init__()
        self.label = label
        self.return_void = True
    def __str__(self) -> str:
        return f"GOTO {self.label}"    
        # return f"GOTO {Fore.YELLOW}{self.label}{Fore.WHITE}"    
    def __repr__(self) -> str:
        return self.__str__()

class ReserveSTACK(CILExpr):
    def __init__(self, space ) -> None:
        super().__init__()
        self.space = space
    def __str__(self) -> str:
        return f"Reserve Stack {self.space}"    
    def __repr__(self) -> str:
        return self.__str__()
    
class FreeStack(CILExpr):
    def __init__(self, space) -> None:
        super().__init__()
        self.space = space
    def __str__(self) -> str:
        return f"Free Stack {self.space}"    
    def __repr__(self) -> str:
        return self.__str__()

class StoreLocal(CILExpr):
    def __init__(self, name, pos, value, register ='$t', type = env.int_type_name) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.pos = pos #esta es la posicion relativa en la pila.
        self.dest = value
        self.register = f'{register}{value[5:]}'
        self.type = type
        if value == 'a0':
            self.register = '$a0'

    def __str__(self) -> str:
        return f'{self.name} => STORELOCAL {self.value}({self.pos})'
    
    def __repr__(self) -> str:
        return self.__str__()

class CallDispatch(CILExpr):
    def __init__(self,meth:CoolCallable, instance: CoolID,arguments = []) -> None:
        super().__init__()
        self.meth = meth
        self.context:Context = instance.get_class_context()
        self.type = self.context.type
        self.arguments = arguments
    
    def __str__(self) -> str:
        return f'CALL {isinstance.id}.{self.meth}{self.arguments}'    

class CallMethod(CILExpr):
    def __init__(self,label) -> None:
        super().__init__()
        self.label = label
    
    def __str__(self) -> str:
        return f'GOTO self.{self.label}'    

class ToA0(CILExpr):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    def __str__(self) -> str:
        return f'a0 = {self.value}'
    
class FromA0(CILExpr):
    def __init__(self) -> None:
        super().__init__()
        self.dest = 'a0'
        self.use_in_code_line = False
    def __str__(self) -> str:
        return f'a0'    

class CloseProgram(CILExpr):
    def __init__(self, e) -> None:
        super().__init__()
        self.use_in_code_line = False
        self.ret = e

    def __str__(self) -> str:
        return f'CLOSE'
        # return f'{Fore.RED}CLOSE{Fore.WHITE}'

class MipsLine(CILExpr):
    def __init__(self, line) -> None:
        super().__init__()
        self.line = line

################################################## PROCESADOR DE COOL ###########################################################
class Body:
    def __init__(self) -> None:
        self.expressions:list[CILExpr] = []
    
    def add_expr(self, e:CILExpr):
        self.expressions.append(e)
    
    def current(self):
        index = 1
        for i in range(len(self.expressions)-1, -1,-1):
            if isinstance(self.expressions[i], CILCommet)\
                or isinstance(self.expressions[i], FreeStack)\
                or isinstance(self.expressions[i], ReserveSTACK):
                index+=1
            else:
                break
            
        if len(self.expressions)>=index:
            return self.expressions[-index]
    
    def current_value(self):
        return self.current().dest
        

    def return_value(self):
        if self.current().return_void:
            return ""
        else:
            return self.current_value()

class IsType:
    def simple_type(e): return IsType.simple_id(e) or IsType.int(e) or  IsType.string(e) or IsType.bool(e)
    def atr(e): return IsType.id(e) and e.is_atr(e.id)
    def int(e): return isinstance(e, IntNode)
    def string(e): return isinstance(e, CoolString)
    def bool(e): return isinstance(e, CoolBool)
    def id(e): return isinstance(e, CoolID)
    def local(e): return isinstance(e, CoolID) and not e.is_atr(e.id)
    def simple_id(e): return IsType.id(e) and not IsType.atr(e)
    def arithmetic(e): return isinstance(e, ArithmeticOP)
    def logical(e): return isinstance(e, Logicar)
    def let(e): return isinstance(e, CoolLet)
    def block(e): return isinstance(e, CoolBlockScope)
    def assign(e): return isinstance(e, Assign)
    def dispatch(e): return isinstance(e, Dispatch)
    def callable(e): return isinstance(e, CoolCallable)
    def new(e): return isinstance(e, CoolNew)
    def _if(e): return isinstance(e, CoolIf)
    def _while(e): return isinstance(e, CoolWhile)

class DivExpression:
    def __init__ (self, e:expr, body:Body, scope = {}):
        if IsType.arithmetic(e):
            DivExpression.arithmetic(e, body, scope)
        if IsType.logical(e):
            DivExpression.logical(e, body, scope)
        if IsType.atr(e):
            DivExpression.atr(e,body, scope) 
        # if IsType.id(e):
            # DivExpression.id_value(e,body) 
        if IsType.local(e):
            DivExpression.local_var(e,body, scope) 
        if IsType.let(e):
            DivExpression.let(e,body, scope)
        if IsType.block(e):
            DivExpression.block(e,body, scope)
        if IsType.assign(e):
            DivExpression.assing(e,body, scope)
        if IsType.dispatch(e):
            DivExpression.dispatch(e,body, scope)    
        if IsType.new(e):
            DivExpression.new(e,body, scope)    
        if IsType._if(e):
            DivExpression._if(e,body, scope)
        if IsType._while(e):
            DivExpression._while(e,body, scope)
        if IsType.int(e):
            DivExpression.int(e,body, scope)    
        if IsType.callable(e):
            DivExpression.callable(e,body, scope)    

    def arithmetic(aritmetic: ArithmeticOP, body:Body, scope:dict = {}):
        # lefth_is_id_and_not_atr = IsType.id(aritmetic.left) and not aritmetic.left.is_atr()
        # right_is_id_and_not_atr = IsType.id(aritmetic.right) and not aritmetic.right.is_atr()
        
        mult_div = (aritmetic.op == '/' or aritmetic.op == '*')

        # if (IsType.int(aritmetic.left) or lefth_is_id_and_not_atr)  and (IsType.int(aritmetic.right) or right_is_id_and_not_atr ):
        if (IsType.int(aritmetic.left)) and (IsType.int(aritmetic.right) ) and not mult_div and USE_i:
            body.add_expr(CILAssign(TempNames.get_name(),aritmetic.left))
            left_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILArithmeticOp(left_value,aritmetic.right, aritmetic.op, constant=True)))
            TempNames.free([left_value])
        elif isinstance(aritmetic.left, IntNode) and (aritmetic.op == '+') and not mult_div and USE_i:# or lefth_is_id_and_not_atr):
            DivExpression(aritmetic.right,body,scope)
            rigth_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILArithmeticOp(rigth_value,aritmetic.left,aritmetic.op, constant=True)))
            TempNames.free([rigth_value])
            # body.add_expr(CILAssign(TempNames.get_name(),CILArithmeticOp(aritmetic.left,body.current_value(),aritmetic.op)))
        # elif (isinstance(aritmetic.right, IntNode) or right_is_id_and_not_atr):
        elif (isinstance(aritmetic.right, IntNode))and not mult_div and USE_i:
            DivExpression(aritmetic.left,body,scope)
            left_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILArithmeticOp(body.current_value(),aritmetic.right,aritmetic.op, constant=True)))
            TempNames.free([ left_value])
        else:
            DivExpression(aritmetic.left,body,scope)
            left_value = body.current_value()
            DivExpression(aritmetic.right,body,scope)
            rigth_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILArithmeticOp(left_value,rigth_value,aritmetic.op)))
            #cuando yo termino una operacion aritmetica, yo puedo volver a utilizar los variables donde no guarde el resultado, dado la naturaleza del codigo recursivo que va desde hijos a padres, solo me interesa conservar la varable donde se asigno el valor de la operacion. Luego las variables que use en el cuerpo de la operacion no las necesito, por lo tanto pueden volver a usarse.
            TempNames.free([left_value,rigth_value])
    
    def logical(logicar:Logicar, body:Body, scope:dict = {}):
        if logicar.op != '=':
            DivExpression.logicar_not_eq(logicar, body, scope)
        else:
            pass
            
    def logicar_not_eq(logicar:Logicar, body:Body, scope:dict = {}):
        lefth_is_id_and_not_atr = IsType.id(logicar.left) and not logicar.left.is_atr()
        right_is_id_and_not_atr = IsType.id(logicar.right) and not logicar.right.is_atr()

        # if (IsType.int(logicar.left) or lefth_is_id_and_not_atr)  and (IsType.int(logicar.right) or right_is_id_and_not_atr ):
        if (IsType.int(logicar.left)) and (IsType.int(logicar.right)):
            body.add_expr(CILAssign(TempNames.get_name(),logicar.left))
            left_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),logicar.right))
            rigth_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILLogicalOP(left_value,rigth_value, logicar.op)))
            TempNames.free([left_value,rigth_value])

        elif isinstance(logicar.left, IntNode) or lefth_is_id_and_not_atr:
            body.add_expr(CILAssign(TempNames.get_name(),logicar.left))
            left_value = body.current_value()
            DivExpression(logicar.right,body,scope)
            rigth_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILLogicalOP(left_value,rigth_value,logicar.op)))
            TempNames.free([left_value,rigth_value])
        
        elif isinstance(logicar.right, IntNode) or right_is_id_and_not_atr:
            body.add_expr(CILAssign(TempNames.get_name(),logicar.right))
            rigth_value = body.current_value()
            DivExpression(logicar.left,body,scope)
            left_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILLogicalOP(body.current_value(),rigth_value,logicar.op)))
            TempNames.free([left_value,rigth_value])
        else:
            DivExpression(logicar.left,body,scope)
            left_value = body.current_value()
            DivExpression(logicar.right,body,scope)
            rigth_value = body.current_value()
            body.add_expr(CILAssign(TempNames.get_name(),CILLogicalOP(left_value,rigth_value,logicar.op)))
            TempNames.free([left_value,rigth_value])
    
    def int(_int:IntNode, body:Body, scope:dict = {}):
        body.add_expr(CILAssign(TempNames.get_name(),_int))

    def atr(id:CoolID, body:Body, scope:dict = {}):
        body.add_expr(CILAssign(TempNames.get_name(),CILCallAtr(id)))
    
    def atr(id:CoolID, body:Body, scope:dict = {}):
        body.add_expr(CILAssign(TempNames.get_name(),CILCallLocal(id,scope[id.id])))
    
    def local_var(vvar, body:Body, scope:dict = {}):
        #Si el scope tiene dos posiciones para ua variable entonces, se ha definido que la variable que se usa para definir a una con su mismo nombre estara en la posicion 1, y la variable nueva creada es la que esta en la posision 0.
        if isinstance(scope[vvar.id], list):
            body.add_expr(CILAssign(TempNames.get_name(),CILCallLocal(vvar,scope[vvar.id])))
        else:
            body.add_expr(CILAssign(TempNames.get_name(),CILCallLocal(vvar,scope[vvar.id])))
    
    def full_space_let(let, body:Body, scope:dict = {}):
        color = get_color()
        body.add_expr(CILCommet(f'#Region Let'))
        # body.add_expr(CILCommet(f'{color}#Region Let'))
        
        let_scope:dict= {}
        length = 0
        pos = 0
        
        for vvar in let.let:
            if vvar.get_type() == env.string_type_name:
                length += 32
            else:
                length += 4
        
        
        for var in scope.keys():
            #esto toma el scope superior y en caso de tener que sobreescrbir variables se hace debajo. Como se vuelve a reservar pila, la posicion de las variables de scpe anteriro con respecto al puntero de pila deben deben aumentar.
            let_scope[var] = scope[var] + length 
        #Reservar espacio en la pila para un tamanno = length
        body.add_expr(ReserveSTACK(length))
        
        for vvar in let.let:
            if not scope.__contains__(vvar.id):
                let_scope[vvar.id] = pos 
            else:
                if not isinstance(scope[vvar.id], list):
                    let_scope[vvar.id] = [pos, scope[vvar.id]]
                else:
                    let_scope[vvar.id] = [pos, scope[vvar.id][1]]

            move = 4 
            if vvar.get_type() == env.string_type_name:
                move = 32
            
            pos += move
            
            if vvar.value is not None:
                DivExpression(vvar.value, body, scope = let_scope)
                temp = body.current_value()
                if isinstance(let_scope[vvar.id],list):
                    body.add_expr(StoreLocal(vvar.id, value = body.current_value(), pos= let_scope[vvar.id][0]))
                else:
                    body.add_expr(StoreLocal(vvar.id, value = body.current_value(), pos= let_scope[vvar.id]))
                TempNames.free([temp])    
            else:
                pass #este es el caso de una instancia de clase, hay que analizarlo
            
            #Cuando la variable ya salga de su definicion, del cuerpo del let, hay que eliminar la tupla y dejarlo solo en el valor como entero
            if isinstance(let_scope[vvar.id], list):
                let_scope[vvar.id] = let_scope[vvar.id][0]
        
        DivExpression(let.in_scope, body, scope = let_scope)
        #Liberar espacio de la pila una vez se sale del let, el scope anterior al del let debe salir igual que antes por recursividad
        body.add_expr(FreeStack(length))        
        body.add_expr(CILCommet(f'#End Region Let'))
        # body.add_expr(CILCommet(f'{color}#End Region Let'))

    def let(let:CoolLet, body:Body, scope:dict = {}):
        color = get_color()
        # body.add_expr(CILCommet(f'{color}#Region Let'))
        body.add_expr(CILCommet(f'#Region Let'))
        
        let_scope:dict= {}
        length = 0
        pos = 0
        for vvar in let.let:
            if vvar.get_type() == env.string_type_name:
                length += 32
            else:
                length += 4

        for var in scope.keys():
            #esto inicializa cada variable del scope anterior en su posicion anterior, se hace esto para usar el scope recursivo
            let_scope[var] = scope[var] 
        
        for vvar in let.let:
            if not scope.__contains__(vvar.id):
                let_scope[vvar.id] = 0 #Como se agrega una por una las variables a la pila, lo que se hace es mover la posicion del resto y agregar la nueva en la posicion 0 
                # let_scope[vvar.id] = pos 
            else:
                #va a tener dos posiciones, en la posicion 0 estara la variable principal, y en la posicion 1 estara la referencia a la vieja
                #esto es para el caso que quiera en la defincion de a variable `x` usar una variable con el nombre `x` en el scope anterior
                if not isinstance(scope[vvar.id], list):
                    let_scope[vvar.id] = [0, scope[vvar.id]]
                else:
                    #si entra aqui quiere decir que no ha salido de la definicion de la variable, y esta tratando de definir otra con el mimo nombre, por ejemplo en el caso de let x<- let x<-<expr que usa `x`> y la variable `x`` existe en el scope anterior, entonces si va a usar `x` dentro de lainicializacion del segundo let al cual le llega el scope del primer let, a ese let le llegara un scope con `scope[x] = (p1,p2)`, donde p2 es la posicion de la primera de las x, la que en ese momento esta defnida, luego esa sera la x que nos interesa llamar en la expresion donde se inicializara la `x` del segundo let. Por tanto para buscar el valor de `x` en la pila se buscara la posicion 1, scope[1]. Cuando se termina de defnir una variable la x que esta en la pila se sobreescribe por la nueva.(Ultima linea del For).
                    let_scope[vvar.id] = [0, scope[vvar.id][1]]

            move = 4 
            # if vvar.get_type() == env.string_type_name:
            #     move = 32
            
            pos += move
            body.add_expr(ReserveSTACK(move))
            
            for var in scope.keys():
                #Esto mueve los datos de contextos superiores de forma dinamica, en caso que la variable del scope anterior tenga igual nombre que una nueva no se hace este movimiento
                if vvar.id != var:
                    let_scope[var] += move
                else:
                    #si en el scope anterior hay una variable con el mismo nombre, esta tendra dos posiciones, se mueve la posicion 1
                    let_scope[var][1] += move
                    pass
            
            for var in let_scope.keys():
                #las variales que no son de scope anterior hay que moverlas tambien, ya que se crea espacio uno a uno
                if var not in scope and var != vvar.id:
                    let_scope[var] += move
                
            
            # if vvar.value is not None:
            if vvar.get_type() == env.int_type_name:
                DivExpression(vvar.value, body, scope = let_scope)
                temp = body.current_value()
                if isinstance(let_scope[vvar.id],list):
                    body.add_expr(StoreLocal(vvar.id, value = body.current_value(), pos= let_scope[vvar.id][0]))
                else:
                    body.add_expr(StoreLocal(vvar.id, value = body.current_value(), pos= let_scope[vvar.id]))
                TempNames.free([temp])    
            else:
                pass #este es el caso de una instancia de clase, hay que analizarlo
            
            #Cuando la variable ya salga de su definicion, del cuerpo del let, hay que eliminar la tupla y dejarlo solo en el valor como entero
            if isinstance(let_scope[vvar.id], list):
                let_scope[vvar.id] = let_scope[vvar.id][0]
        
        DivExpression(let.in_scope, body, scope = let_scope)
        #Liberar espacio de la pila una vez se sale del let, el scope anterior al del let debe salir igual que antes por recursividad
        body.add_expr(FreeStack(length))        
        # body.add_expr(CILCommet(f'{color}#End Region Let'))
        body.add_expr(CILCommet(f'#End Region Let'))

    def assing(assign: Assign, body:Body, scope:dict = {}):
        if assign.left.id in scope:
            #estamos tratando con una variable local, luego hay que guardar su valor en la pila
            DivExpression(assign.right, body, scope)
            temp = body.current_value()
            if isinstance(scope[assign.left.id],list):
                body.add_expr(StoreLocal(assign.left.id, value = body.current_value(), pos= scope[assign.left.id][0]))
            else:
                body.add_expr(StoreLocal(assign.left.id, value = body.current_value(), pos= scope[assign.left.id]))
            TempNames.free([temp])    
        else:
            if IsType.simple_type(assign.right):
                body.add_expr(CILAssign(assign.left.id,assign.right,is_temp=False))
            else:
                DivExpression(assign.right, body, scope)
                body.add_expr(CILAssign(assign.left.id,body.current_value(),is_temp=False))
    
    def block(block:CoolBlockScope, body:Body, scope:dict = {}):
        for e in block.exprs:
            DivExpression(e,body, scope)

    def id_value(e:CoolID,body, scope:dict = {}):
        # if in_params(e):
            #tratarlo como parametro
            # pass
        body.add_expr(CILAssign(TempNames.get_name(),e.id))
        # body.add_expr(CILId(e.id))

    def new(e:CoolID, body, scope:dict = {}):
        body.add_expr(CILAssign(TempNames.get_name,e))
        
    def case(case:CoolCase, scope:dict = {}):
        pass

    def _while(_while:CoolWhile, body:Body, context:dict = {}):
        color = get_color()
        # loop = NameLabel(f'{color}loop').get()
        loop = NameLabel(f'loop').get()
        condition = _while.condition
        scope = _while.loop_scope
        end_while = NameLabel('end_while').get()
        
        body.add_expr(Label(loop)) #Todos los cambios de la condiciona tienen que volverse a pocesar

        # if IsType.bool(condition):
        #     if condition:
        #         body.add_expr(CILIf(IntNode(1),else_label=end_while))
        #     else:
        #         body.add_expr(CILIf(IntNode(0),else_label=end_while))
        # else:
        DivExpression(condition,body, context)
        temp = body.current_value()
        body.add_expr(CILIf(body.current_value(),else_label=end_while, _while=True))
        TempNames.free([temp])
        #end_else

        DivExpression(scope,body,context)
        body.add_expr(GOTO(loop))
        body.add_expr(Label(end_while))
        body.add_expr(CILVoid()) #esto sirve para que se sepa que si el valor de retorno de la funcion es el while, entonces es tipo void

    def _if (_if:CoolIf, body:Body, scope:dict = {}):
        condition = _if.condition
        then_s = _if.then_scope
        else_s = _if.else_scope
        label = NameLabel('else').get()
        label_end = NameLabel('endif').get()
        result_expr = TempNames.get_name()

        if IsType.bool(condition):
            if condition:
                body.add_expr(CILIf(IntNode(1),else_label=label))
            else:
                body.add_expr(CILIf(IntNode(0),else_label=label))
        else:
            DivExpression(condition,body,scope)
            body.add_expr(CILIf(body.current_value(),else_label=label))

        DivExpression(then_s,body,scope)
        body.add_expr(CILAssign(result_expr,body.current_value()))
        # then_return = body.current_value()
        body.add_expr(GOTO(label_end))
        body.add_expr(Label(label))
        DivExpression(else_s,body,scope)
        body.add_expr(CILAssign(result_expr,body.current_value()))
        body.add_expr(Label(label_end))
        body.add_expr(CILId(result_expr))

    def dispatch(dispatch:Dispatch, body:Body, scope:dict = {}):
        callable:CoolCallable = dispatch.function
        type = dispatch.type
        body.add_expr(CILCall(type, callable.id.id,callable.params))
        pass

    def callable(callable:CoolCallable, body:Body, scope:dict = {}):
        context:Context = callable.get_class_context()
        arguments = callable.params
        id = callable.id.id
        label_method = f'{context.type}_{id}'


        #una vez se llega a este punto todo lo anterior deberia haberse guardado debidamente en la pila, luego no se necesita guardar ningun registro temporal. Todo lo que el programador de cool necesita guardado lo esta.
        #Ahora hay que procesar los parametros y pasarlos al methodo que se llama, los registros a0-a3 estan pensados para ello, pero si los parametros son mas de esto se debe usar la pila.
        
        space =len(arguments)*4 + 4
        
        #Cuando se reserva pila hay que mover las posiciones relativas de las variables del scope
        body.add_expr(ReserveSTACK(space))
        for key in scope.keys():
            if isinstance(scope[key], list):
                scope[key][0] +=space
                scope[key][1] +=space
            else:
                scope[key] += space

        #TODO hay que asignarle el self        
        pos = 4
        for arg in arguments:
            DivExpression(arg,body,scope)
            body.add_expr(StoreLocal(name=body.current_value(),pos= pos,value=body.current_value()))
            pos +=4
        
        # Considerar guardar en la pila los valores temprales pa no perderlos.
        body.add_expr(CallMethod(label_method))

        #Cuando se libera la pila hay que mover las posiciones relativas del scoep que se habia modificado
        body.add_expr(FreeStack(space))
        for key in scope.keys():
            if isinstance(scope[key], list):
                scope[key][0] -=space
                scope[key][1] -=space
            else:
                scope[key] -= space

        body.add_expr(FromA0())