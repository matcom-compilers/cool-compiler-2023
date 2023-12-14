# Documentación



#### Cómo ejecutar y compilar. 




El compilador se utiliza desde la carpeta src llamando al archivo `coolc.sh` y a continuación la dirección del archivo de extensión cl que se desea compilar, ejemplo: `./cool.sh /path/file.cl`. Este procedimiento compila su `file.cl` y devuelve un archivo `file.mips` que se ejecuta utilizando el comando `spim -file file.mips`.` 

#### Requisitos adicionales, dependencias, configuración, etc.






- Instalación de la biblioteca `SLY` de python. Se puede instalar mediante el comando `pip install sly`. 
- Instalación del simulador de MIPS `SPIM`. Se puede instalar mediante el comando `sudo apt-get install spim`.


### Arquitectura del compilador


Todo el código del compilador se encuentra en la carpeta COOL dentro de src, este se divide en 4 módulos principales:


 - coollexer: Se encarga de analizar el código fuente y dividirlo en tokens.
 - coolparser: Se encarga de analizar la estructura del código fuente y devolver un árbol de sintaxis abstracta (AST) que recoja la estructura del programa. 
 - semantic: Se encarga de realizar el chequeo semántico del AST recibido del parser y hacer la verificación de la correctitud de tipos.
 - codegen: Luego de realizarse el chequeo semántico a partir del AST se genera el código de bajo nivel mips para ser ejecutado.

Además se encuentran otros módulos auxiliares encargados de los errores en tiempo de compilación y de los diferentes nodos que puede tener el AST.



### Fases del compilador



El flujo de las fases de un compilador sigue un proceso secuencial que transforma el código fuente de un programa en un programa ejecutable. Nuestro compilador de COOL sigue el siguiente flujo de fases:



#### Análisis léxico



Esta fase se encarga de analizar el código fuente y dividirlo en unidades léxicas o tokens, como identificadores, palabras clave, operadores y símbolos.  Se generan los tokens que representan las unidades léxicas del programa.

Para la lexemización, tokenización y parser se utilizó la biblioteca de python `SLY`. Esta es una biblioteca para escribir analizadores léxicos y gramaticales. Se basa libremente en las herramientas tradicionales de construcción de compiladores lex (tokenizar) y yacc (yet another compiler-compiler). Tomando su clase Lexer como base hemos creado nuestro lexer para el lenguaje COOL agregando todos los tokens necesarios para el lenguaje, así como literales,palabras claves y algunas funciones necesarias como los ignore para los comentarios.

Ejemplo de como se definen tokens, literales y otros objetos utilizando el lexer de `SLY`:


```python
tokens = {
        # Symbols
        "NUMBER", "STRING", "TYPE", "ID", 
        # Arithmetic Operators
        "PLUS", "MINUS", "TIMES", "DIVIDE", "LESS", "LESSEQUAL", "EQUAL", "NOT", "BITWISE", "ASSIGN", "DARROW",
        # Reserved words
        'CLASS', "INHERITS", "IF", "THEN", "ELSE", "FI", "WHILE", "LOOP", "POOL", "LET", "IN", "CASE", "OF", "ESAC", "NEW", "ISVOID", "TRUE", "FALSE",
    }
    literals = {"(", ")", "{", "}", ";", ":", ",", ".", "@"}
```

Además de tokenizar la entrada el análisis léxico puede detectar tokens que no pertenecen al léxico del lenguaje de programación, como caracteres no válidos o secuencias que no tienen significado dentro del lenguaje, el uso incorrecto de operadores o símbolos, que podrían indicar algún problema en la escritura del código, puede identificar si se han escrito incorrectamente palabras clave o identificadores, también detecta errores relacionados con la delimitación de tokens, como la falta de cierre de comillas en cadenas de texto, paréntesis sin emparejar, corchetes o llaves mal balanceados, entre otros.


#### Análisis sintáctico



El analizador sintáctico verifica la estructura del código fuente según las reglas gramaticales del lenguaje de programación COOL. Se construye un AST que representa la estructura jerárquica del programa. Este árbol se utiliza para analizar la corrección sintáctica verificando si las expresiones y declaraciones del programa cumplen con las reglas de la gramática. 

Para la obtención del AST se utilizaron las reglas gramaticales definidas en el manual de COOL, incluída la precedencia y asociatividad, junto al algoritmo de análisis sintáctico (parser) LALR(1) implementado en `SLY`. Un analizador LALR (Look-Ahead LR)  es una versión simplificada de un analizador LR canónico, para analizar un texto de acuerdo con un conjunto de reglas de producción especificadas por una gramática formal para un lenguaje.

Al igual que con otros tipos de gramáticas LR, un analizador o gramática LALR es bastante eficiente para encontrar el único análisis de abajo hacia arriba correcto en un solo escaneo de izquierda a derecha sobre el flujo de entrada, porque no necesita usar el retroceso. El analizador siempre utiliza una búsqueda anticipada, representando LALR(1) una búsqueda anticipada de un token.

`SLY` brinda una interfaz sencilla y cómoda para definir la gramática del lenguaje, además de permitir definir la precedencia y asociatividad de los operadores.

Ejemplo de como se define la precedencia y asociatividad utilizando el parser de `SLY`:

```python
 precedence = (
       ('right', 'ASSIGN'),
       ('nonassoc', 'NOT'),
       ('nonassoc', 'EQUAL', 'LESS', 'LESSEQUAL'),
       ('left', 'PLUS', 'MINUS'),
       ('left', 'TIMES', 'DIVIDE'),
       ('right', 'ISVOID'),
       ('left', 'BITWISE'),
       ('nonassoc', '@'),
       ('nonassoc', 'NUMBER'),
       ('nonassoc', '(',')'),
       ('left', '.'),
    )
```

Ejemplo de como se define una regla de la gramática utilizando el parser de `SLY`:
```python
@_('ID "(" formals ")" ":" TYPE "{" expr "}"')
    def feature(self, p: YaccProduction):
        return Method(
            line=p.lineno,
            column=self._get_column_from_production(p),
            id=p.ID,
            type=p.TYPE,
            formals=p.formals,
            expr=p.expr
        )
```
En este ejemplo de código la función feature  utiliza la información del objeto  YaccProduction  para crear el objeto  Method . El nombre del método se obtiene del token  ID , el tipo de retorno se obtiene del token  TYPE , los parámetros se obtienen del objeto  formals  y el cuerpo del método se obtiene del objeto expr . 

El análisis sintáctico verifica si las construcciones del código cumplen con la gramática del lenguaje de programación. Puede identificar errores como uso incorrecto de operadores, expresiones mal formadas, estructuras de control incompletas, entre otros.


 
#### Análisis semántico 


Durante esta fase, se realiza un análisis más profundo del programa para verificar la coherencia y consistencia semántica. Se comprueba si las variables están correctamente declaradas, si los tipos de datos son compatibles y si se cumplen las reglas semánticas del lenguaje. 


En el análisis semántico del lenguaje Cool, se realizan diversas tareas para verificar la coherencia y corrección del programa en términos de su significado y contexto. Está implementado utilizando el patrón visitor en dos momentos, donde cada uno de los nodos del AST es una clase que realiza su chequeo semántico llamando a su visitor correspondiente dentro de la clase visitor.

Los dos momentos del chequeo son: 


- Primeramente a la hora de la declaración de las clases y herencias, donde verifica que no existan errores de herencia, conflictos de nombres, que no se creen herencias cíclicas, que no se redefinan atributos y que los métodos se redefinan de forma correcta. 

- En segundo lugar, se realiza el chequeo de tipos de las expresiones, donde se verifica que los tipos de las expresiones sean correctos, la consistencia de los tipos utilizados en las diferentes expresiones, que los tipos de los argumentos en los llamados a métodos sean correctos, que las variables estén declaradas y siempre se utilicen en su ámbito correspondiente, que no se realicen operaciones entre tipos incompatibles, que los retornos de las funciones sean consecuentes con su tipo, además de la correcta utilización de cada uno de los recursos del lenguaje (condicionales, ciclos, let, case, etc...) cumpliendo las indicaciones del manual de COOL.


Todo el análisis semántico se maneja desde la clase Program en específico su método check:

```python
 def check(self):
        try:
            self.visitor.visit_program(self)

            for class_ in self.classes:
                if class_:
                    if class_.inherits and class_.inherits in self.visitor.types.keys() and not  class_.inherits in self.visitor.basic_types.keys():
                        class_.inherits_instance = self.visitor.types[class_.inherits] 
            
            for _class in self.classes:
                if _class:
                    _class.check(self.visitor)

            for _class in self.classes:
                class_visitor =  Visitor_Class( scope= {
                    'type': _class.type, 
                    'inherits': _class.inherits, 
                    'features': _class.features_dict, 
                    'methods': _class.methods_dict, 
                    'attributes': _class.attributes_dict, 
                    'inherits_instance': _class.inherits_instance, 
                    'line': _class.line, 
                    'column': _class.column,
                    'lineage': _class.lineage,
                    'all_types':self.visitor.types,
                    'inheritance_tree':self.visitor.tree,
                    'basic_types':self.visitor.basic_types,
                    'type': _class.type
                    })
                for feature in _class.features:
                    feature.check(class_visitor)

        except Exception as e:
            return [e]
```

Este es el encargado de almacenar los diferentes visitor que se utilizan a lo largo del proceso y brindarles la información de toda la estructura de las clases presentes. Además que envia a las clases y a las diferentes expresiones a realizar sus respectivos chequeos.

Luego cada expresión se encarga de su propio chequeo haciendo uso de la función del visitor que le ha sido asignada desde su método check.
Ej:

```python
    def check(self, visitor:Visitor_Class):
        return visitor.visit_dispatch(self)
```

Todas estas funciones retornan el tipo estático de la expresión correspondiente, lo que ayuda en gran manera la realización del chequeo de las expresiones que las engloban. 

Esta fase es crucial para garantizar que el programa cumpla con las reglas y restricciones del lenguaje, verificando la corrección de tipos, la coherencia en la herencia, entre otros aspectos fundamentales para el funcionamiento adecuado del programa.



### Generación de código

En esta última fase, se genera código MIPS a partir del AST generado en la fase anterior. Para esto se utilizó el patrón similar visitor, donde se recorre el AST y se genera el código MIPS correspondiente a cada nodo, dadas las implementaciones especificas que se facilitan en los nodos. Las clases que implementan el patrón visitor son las siguientes:

- `Codegen`: Clase principal que se encarga de recibir el AST y generar el código MIPS correspondiente a cada nodo.
- `MipsVisitor`: Clase que define los métodos que se utilizan para generar el código MIPS de cada nodo.
- `Node`: Clase abstracta que define los métodos que se utilizan para generar el código MIPS de cada nodo en la función abstracta `codegen`.

Se recorre el AST a partir del llamado de `Codegen` iniciando por el `Node` llamado `Program` y se recorre el AST de forma recursiva, generando líneas de código MIPS almacenadas como los tipos:

- `Instruction`: Clase que define las instrucciones MIPS.
- `Label`: Clase que define las etiquetas MIPS.
- `Comment`: Clase que define los comentarios MIPS.
- `Data`: Clase que define los datos a almacenar en el segmento de datos MIPS.

Al finalizar el recorrido del AST se genera el archivo `.mips` con el código MIPS generado, el cual se puede ejecutar con el simulador `spim`.

#### Stack

Para el manejo del Stack se tienen varios métodos que se encargan de almacenar y recuperar los valores de las variables en el Stack. Entre estos está `get_variable` el cual dado el id de la variable y sabiendo el estado actual de la ejecución del programa, se encarga de indicar la posición de la variable en el Stack. Al igual que al entrar en un scope se mueve el offset del Stack y al salir se recupera el offset anterior.

En el caso de los métodos, al entrar en estos siempre se almacena como primer valor en el Stack el valor del self, para luego poder acceder a los atributos de la clase. Y una vez dentro del método se almacena el valor del registro de retorno `$ra` para luego poder retornar al lugar donde se llamó el método.

#### Heap

Todos los objetos creados en el programa se almacenan en el Heap, teniendo en su primera posición un puntero al tipo del objeto, mientras que este lo que almacena en su pocision 0 es el string con el nombre del tipo del objeto y en la posición 1 un puntero a su padre en el árbol de herencia.

Para instanciar un objeto se crea un espacio en el Heap con el tamaño del objeto y se llama al label con nombre `{object}_class` pasandole como self el puntero al objeto creado. Este label se encarga de inicializar los atributos del objeto y retornar el puntero al objeto creado.

Para acceder a los atributos de un objeto se utiliza el método `get_variable` el cual vimos anteriormente, el cual dado el id del atributo y el estado actual de la ejecución del programa, se encarga de indicar la posición del atributo en el objeto.

Para acceder a los métodos de un objeto se utiliza el método `get_method` el cual dado el id del método y el estado actual de la ejecución del programa, se encarga de indicar la posición del método en el objeto.



