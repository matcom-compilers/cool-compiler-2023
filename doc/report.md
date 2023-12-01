# Cool Compiler

- Darío Fragas González C411
- Abraham González Rivero C412

### 1. Detalles técnicos

AQUI SE HABLARIA DE LOS REQUERIMIENTOS DEL PROYECTO Y FORMAS DE EJECUTARLO

Estructura y organización de los directorios del proyecto a partir de la carpeta _src_:

```bash
.
├── codegen
│      ├── __init__.py
│      ├── cil_ast.py
│      ├── cil_to_mips.py
│      ├── cocl_to_cil.py
│      ├── mips_ast.py
│      └──  mips_codegen.py
├── parsing
│      ├── __init__.py
│      ├── ast.py
│      ├── lex.py
│      └── parser.py
├── semantic
│      ├── __init__.py
│      ├── context.py
│      ├── scope.py
│      ├── type_builder.py
│      ├── type_checker.py
│      ├── type_collector.py
│      └── types.py
├─ test_cool
│      ├── dispatch.cl
│      └── formals.cl
├─ utils
│      ├── loggers.py
│      └── visitor.py
├── cool.py
├── coolc.sh
├── makefile
├── Readme.md
```

### 2. Arquitectura del Compilador

  El desarrollo del proyecto se dividió en 3 módulos principales: codegen, parsing y semantic.

#### Análisis lexicográfico

**Análisis léxico**
Este proceso se realiza en _lex.py_.
 Proceso que comienza con el análisis de código de cool que se desea compilar, su función
principal es convertir la cadena de caracteres en una cadena de token. Los token son la
primera abstracción que se le aplica al código, estos son subcadenas que son
lexicográficamente significativas y según este significado se les asigna un tipo (literal,
keyword, type, identificador, number, string, etc).

El lexer se auxilia de la clase _CharacterStream_ para manipular la cadena:

```python
class CharacterStream:
    def __init__(self, source_code: str):(...)
    
    def next_char(self) -> Optional[str]:(...)

    def peek_char(self) -> Optional[str]:(...)

    def get_position(self)-> CharPosition:(...)
        
    def reset(self):(...)
```

Esta clase ofrece herramientas para manipular la cadena como: obtener el próximo carácter de la cadena, obtener la posición,línea y columna, en que se encuentra el carácter, étc.

En la clase _TokenType_ se definen todos los tipos de token que pudieran encontrarse en la cadena:

```python
class TokenType(Enum):
    OBJECTID = "OBJECTID"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"
    DOT = "DOT"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    AT = "AT"
    (...)
    EOF = "EOF"
```

Para representar un token se define la clase _Token_ que posee un valor, un tipo y la posición en que se encuentra el token.

```python
 def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
        log.debug(
            f"Created Token:",
            extra={"type": type, "location":          position,"value": value},
        )
```
La clase _Lexer_ se encarga de la tokenización de la cadena. Se inicializa recibiendo una cadena, la cual convierte a un _CharacterStream_, explicado anteriormente. Posee además un conjunto de keywords que se mapean a tokens y una lista de errores. La tokenización se realiza en el método _lex_ el cual va consumiendo los caracteres de la cadena llamando al método _fetch_token_ quien va realizando la validación de los caracteres y armando los tokens. Si un error es detectado se reporta pero se continua la ejecución.

```python
 class Lexer:
    def __init__(self, stream):
      (...)
       
    def error(self, message, position: Optional[CharPosition] = None):
      (...)
        
    def fetch_token(self):
      (...)
       
    def lex(self):
      (...)
``` 
**Análisis sintáctico**

El proceso de parsing se realiza en _parser.py_. La clase Parser se encarga de realizar esta tarea. Nuestra implementación se inicializa al recibir una lista de tokens.

La definición de los nodos del _AST_(árbol de sintaxis abstracta) se encuentra implementada en _ast.py_. Todo nodo posee un valor, un tipo y una posición e implementan el patrón visitor. Se muestran algunos nodos como ejemplo:

```python
    class ProgramNode(Node):
    def __init__(self, classes, location):
        self.classes: List[ClassNode] = classes
        super().__init__(location)

    def __str__(self) -> str:
        return "\n".join(str(c) for c in self.classes)

    class FeatureNode(Node):
    def __init__(self, location):
        super().__init__(location)

    class AttributeNode(FeatureNode):
    def __init__(self, name, attr_type, init: "ExpressionNode", location):
        super().__init__(location)
        self.name = name
        self.attr_type = attr_type
        self.init = init
```

Para parsear se utiliza el método _parse_. En este se origina el árbol de sintaxis abstracta.  El parser construye los distintos nodos en profundidad, o sea , primero los hijos y luego el padre. Por ejemplo, para construir el nodo _Program_, raíz del _AST_ de _COOL_, ya se deben haber construido todos los nodos Class. Cada nodo conoce sus posibles reglas de derivación y como evitar errores de desambiguación entre las producciones a la hora de determinar que producción aplicar. El método _eat_ se encarga de consumir el token y validar que cumpla con los requisitos de la producción en cuestión.

**Producciones**
```
program := [[class]]+
class ::= class TYPE [inherits TYPE] { [[feature; ]]∗}
feature := ID method
                 | ID attribute

                 | ID : TYPE [ <- expr]
method := ( [ formal [[, formal]]*] ) : TYPE { expr }
formals := formal [[, formal]]*
expr ::=ID <- expr
            | expr [@TYPE].ID( [ expr [[ , expr ]]∗] )
            | ID( [ expr  [[ , expr ]] ∗] )
            | if expr then expr else expr if
            | while expr loop expr pool
            | { [[ expr ; ]]+}
            | let ID : TYPE [<-expr] [[,ID : TYPE [<- expr ]]]∗in expr
            | case expr of [[ID : TYPE => expr; ]]+esac
            |new TYPE
            |isvoid expr
            |expr+expr
            |expr− expr
            |expr∗expr
            |expr/expr
            | ̃expr
            |expr<expr
            |expr<=expr
            |expr=expr
            |not expr
            |(expr)
            |ID
            |integer
            |string
            |true
            |false
```

**Análisis semántico**

El análisis semántico se realiza en el módulo _semantic_.En esta fase es donde se revisa que se cumplan todos los predicados semánticos que caracterizan
al lenguaje _COOL_ y por tanto se revisa la consistencia y uso correcto de los tipos declarados.
Para el chequeo semántico son necesarios tres recorridos sobre el _AST_ obtenido del proceso de _parsing_
. La primera para recolectar los tipos para el contexto, la segunda para definir los
atributos y métodos de cada tipo y la tercera para realizar el chequeo de tipos. Utilizando el
patrón _Visitor_ es como realizamos los pertinentes recorridos por el _AST_.

La clase TypeCollector definida en _type_collector.py_se verán solo las declaraciones de clases, para guardar todos los tipos definidos en el lenguaje.

Para ellos nos apoyaremos de un contexto, clase _Context_ definida en _context.py_ y que funciona parecido a un diccionario, en el
cual se guardaran los tipos de las clases a medida que las vamos visitando.

```python
    class TypeCollector(Visitor):
    def __init__(self) -> None:
        self.context = None
        self.errors = []

    def error(self, message, location, type, value):
      (...)
        

    def visit__ProgramNode(self, node: ProgramNode):
      (...)
        
    def visit__ClassNode(self, node: ClassNode):
      (...)
        
```

Luego de realizar el recorrido y haber encontrado todos los tipos, se procede a ejecutar una
segunda pasada por el _AST_. De esta tarea, se encarga el _TypeBuilder_ definido en _type_builder.py_. _TypeBuilder_ pasará por cada tipo encontrado para construirlo
junto con sus atributos y métodos. A este visitor se le pasa el contexto generado por el _TypeCollector_.py
. En este punto la tarea principal es la de visitar los atributos y métodos de los
tipos y agregárselos, sin antes haber realizado algunas comprobaciones, como que no se definan
atributos de tipos que no existen, o que se redefinan atributos de los padres o que existan
múltiples atributos con el mismo nombre. Análisis semejantes son hechos con las funciones,
impidiendo la creación de métodos ya existentes en una misma clase o funciones que son
sobrescritas por herencia sigan teniendo la misma cantidad de argumentos y tipo de retorno.
Para el caso de herencia se lanzan errores cuando se hereda de tipos que no existen.

```python
  class TypeBuilder(Visitor):
    def __init__(self, context: Context, errors=None):
      (...)
        

    def error(self, message, location, type, value):
      (...)

    def visit__ProgramNode(self, node: ProgramNode):
      (...)
        
    def visit__ClassNode(self, node: ClassNode):
      (...)
        
    def visit__AttributeNode(self, node: AttributeNode):
      (...)
        

    def visit__MethodNode(self, node: MethodNode):
      (...)
```

Finalmente en el último recorrido del _AST_ ,_TypeChecker_, definido en _type_checker.py_ ,se encarga de chequear todos los
nodos del _AST_ cerciorándose de que cumplan con las reglas definidas para ellos. Por ejemplo en
esta fase es donde resolvemos conflictos de realizar operaciones binarias sobre tipos que no lo
permiten (ejemplo sumar dos _strings_ ). Otro de los análisis es que para trabajar con una variable
en una clase, esta ha de estar definida, ya sea como atributo o como una variable dentro de un
let, etc. Es por ello que es de vital importancia en este recorrido el uso de un _scope_, definido en _scope.py_ , este concepto
permite conocer las variables que tenemos visibles en los diferentes niveles. Esto es de vital
importancia pues cuando tratamos funciones que reciben argumentos con nombres iguales a
atributos de clase, queremos tratar con el argumento, y no con los atributos de la clase. Es por
ellos que cada clase define su propio y este es pasado a sus hijos, pero las expresiones
como el case y let, que puede definir nuevas variables, reciben su propio _scope_, con lo que se
desambigua entre todas las variables declaradas. 
El TypeChecker es la herramienta
fundamental que permite llevar a cabo el polimorfismo en el lenguaje, pues junto con el
se verifica que un tipo pueda ser sustituido por otro, además que es esencial para determinar
atributos que se definen en clases padre y se utilizan en una clase hijo, etc.

```python
class TypeChecker(Visitor):
    def __init__(self, context: Context, errors=None):
        

    def error(self, message, location, type, value):
        

    def visit__ProgramNode(self, node: ProgramNode, scope=None):
        

    def visit__ClassNode(self, node: ClassNode, scope: Scope):
        

    def visit__AttributeNode(self, node: AttributeNode, scope: Scope):
        


    def visit__MethodNode(self, node: MethodNode, scope: Scope):
       

    def visit__AssignNode(self, node: AssignNode, scope: Scope):
        

    def visit__DispatchNode(self, node: DispatchNode, scope: Scope):
        

    def visit__BinaryOperatorNode(self, node: BinaryOperatorNode, scope: Scope):
        

    def visit__UnaryOperatorNode(self, node, scope):
        

    def visit__IfNode(self, node: IfNode, scope: Scope):
        

    def visit__BlockNode(self, node: BlockNode, scope: Scope):
        

    def visit__LetNode(self, node: LetNode, scope: Scope):
        

    def visit__CaseNode(self, node: CaseNode, scope: Scope):
        

    def visit__CaseOptionNode(self, node: CaseOptionNode, scope: Scope):
        

    def visit__NewNode(self, node: NewNode, scope: Scope):
        

    def visit__IsVoidNode(self, node: IsVoidNode, scope: Scope):
        

    def visit__NotNode(self, node: NotNode, scope: Scope):
       

    def visit__PrimeNode(self, node: PrimeNode, scope: Scope):
       

    def visit__IdentifierNode(self, node: IdentifierNode, scope: Scope):
       

    def visit__IntegerNode(self, node: IntegerNode, scope: Scope):
        
    def visit__StringNode(self, node: StringNode, scope: Scope):
       

    def visit__BooleanNode(self, node: BooleanNode, scope: Scope):
      

    def visit__MethodCallNode(self, node: MethodCallNode, scope: Scope):
        

    def visit__WhileNode(self, node: WhileNode, scope: Scope):
        
