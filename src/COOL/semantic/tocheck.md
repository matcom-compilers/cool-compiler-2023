 
##### program
- todas las clases definidas en el programa tienen una declaración correspondiente

- todas las clases referenciadas existan y no haya clases duplicadas 
 
- las clases que heredan de otras existan 

- no haya ciclos en la herencia
 

##### class

- los atributos y métodos utilizados en el programa estén correctamente declarados en las clases correspondientes.

- las operaciones y asignaciones utilizadas sean válidas y compatibles

- no haya atributos o métodos utilizados sin ser declarados y que no haya declaraciones duplicadas. 
 
- no haya métodos con el mismo nombre pero con diferentes tipos de parámetros o tipos de retorno. 
 
- verificar que la herencia de las clases no cause conflictos en los tipos con variables que tengan el mismo nombre pero que sean de tipos diferentes.

- verificar que los tipos de retorno de los métodos sean válidos y compatibles con los tipos de retorno de los métodos de la clase padre.

##### expresion

- los tipos utilizados en las operaciones y asignaciones sean válidos y compatibles. 


##### assignment

- verificar que el tipo de la expresión sea compatible con el tipo de la variable a la que se le asigna o cumpla el principio de sustitución de tipos en la herencia.


# Important
- todos los atributos tienen alcance local a la clase y todos los métodos tienen alcance global => la única forma de proporcionar acceso al estado del objeto en Cool es a través de métodos. 

- Los nombres de las características deben comenzar con una letra minúscula.

- Los nombres de las clases deben comenzar con una letra mayúscula.

- Ningún nombre de método puede definirse varias veces en una clase y ningún nombre de atributo puede definirse varias veces en una clase, pero un método y un atributo pueden tener el mismo nombre.

 - La variable especial self se refiere al objeto en el que se despachó el método, que, en el ejemplo, es c mismo. $???????$ Hay una forma especial new C que genera un objeto nuevo de la clase C.

-  Una clase solo puede heredar de una sola clase; esto se llama acertadamente "herencia única".
<!-- 
- La clase Object es la clase raíz de todas las clases en Cool.

- La clase IO es la clase que define las operaciones de entrada y salida estándar.
-->
-  hay un tipo SELF TYPE que se puede usar en circunstancias especiales. $????????$


- Cada variable debe tener un 
declaración de tipo en el punto en que se introduce, ya sea en un let, case o como el parámetro formal de un método.

- si C hereda de P, directa o indirectamente, entonces un C se puede usar donde un P sería suficiente. 

- El tipo SELF TYPE se utiliza para referirse al tipo de la variable self.

- SELF TYPE puede utilizarse en los siguientes lugares: new SELF TYPE, como el tipo de retorno de un 
método, como el tipo declarado de una variable let, o como el tipo declarado de un atributo. No se permiten otros usos de SELF TYPE.

-  el verificador de tipos infiere un tipo para cada expresión en el programa. 

- istinguir entre el tipo asignado por el verificador de tipos a una expresión en tiempo de compilación, al que llamaremos el tipo estático de la expresión, y el o los tipos a los que la expresión puede evaluarse durante la ejecución, a los que llamaremos tipos dinámicos. $??????$

- cada bloque tiene al menos una expresion, se evaluan de izquierda a derecha

- el valor de un bloque es el valor de la última expresión en el bloque.

- El tipo estático de un bloque es el tipo estático de la última expresión. 

- 

##### - No entendi lo de tipos estaticos y dinamicos en coolya entendi OK

- Cuando se crea un nuevo objeto de una clase, todos los atributos heredados y locales deben inicializarse. 

- El orden de inicialización de los atributos es el siguiente: primero se inicializan los atributos heredados, en orden de declaración en la clase padre, luego se inicializan los atributos locales, en orden de declaración en la clase actual.

- Todas las variables en Cool se inicializan para contener valores del tipo apropiado. El valor especial void 
es un miembro de todos los tipos y se utiliza como la inicialización predeterminada para las variables donde no se proporciona inicialización por parte del usuario. 

- Puede haber cero o más parámetros formales. Los identificadores utilizados en la lista de parámetros formales deben ser distintos entre sí.

- si una clase C hereda un método f de una clase ancestro P, entonces C puede anular la definición heredada de f siempre que el número de argumentos, los tipos de los parámetros formales y el tipo de retorno sean exactamente los mismos en ambas definiciones. 

- Las expresiones más simples son las constantes. Las constantes booleanas son true y false. Las constantes enteras son cadenas de dígitos no signadas, como 0, 123 y 007. Las constantes de cadena son secuencias de caracteres encerradas entre comillas dobles, como "Esto es una cadena". Las constantes de cadena pueden tener como máximo 1024 caracteres de longitud. 

- Las constantes pertenecen a las clases básicas Bool, Int y String. El valor de una constante es un objeto de la clase básica correspondiente. 

- Los nombres de las variables locales, los parámetros formales de los métodos, self y los atributos de clase son todas expresiones. 

- El identificador self puede ser referenciado, pero es un error asignar a self o vincular self en un let, un case o como parámetro formal. También es ilegal tener atributos con el nombre self. 

- el tipo est'atico de la expresi'on debe ajustarse al tipo declarado del identificador 

- Existen tres formas de despacho(llamada a metodo) en Cool: despacho estático, despacho dinámico y despacho automático.

- 
Las otras formas de despacho son: 
<id>(<expr>,...,<expr>) 
<expr>@<type>.id(<expr>,...,<expr>) 
 
La primera forma es una forma abreviada de self.<id>(<expr>,...,<expr>). 
 
La segunda forma proporciona una forma de acceder a métodos de clases padre que han sido ocultados por redefiniciones en clases hijas. En lugar de utilizar la clase de la expresión más a la izquierda para determinar el método, se utiliza el método de la clase especificada explícitamente. Por ejemplo, e@B.f() invoca el método f en la clase B en el objeto que es el valor de e. Para esta forma de despacho, el tipo estático a la izquierda de "@" debe ajustarse al tipo especificado a la derecha de "@".


- Las expresiones opcionales en el cuerpo de let son inicialización; la otra expresión es el cuerpo. 

- En un let primero se evalúa <expr1> y el resultado se vincula a <id1>. Luego se evalúa <expr2> y el resultado vinculado a <id2>, y así sucesivamente, hasta que todas las variables en el let se inicializan. (Si la inicialización de <idk> se omite, se utiliza la inicialización predeterminada del tipo <tipok>.)

- A continuación, el cuerpo del let se evalua. El valor del let es el valor del cuerpo. 

- Los identificadores de let <id1>,...,<idn> son visibles en el cuerpo del let. Además, identificadores <id1>,...,<idk> son visibles en la inicialización de <idm> para cualquier m > k. 

- Si un identificador se define varias veces en un let, las vinculaciones posteriores ocultan las anteriores.

- Cada let expresión debe introducir al menos un identificador. 

- El tipo de una expresión de inicialización debe cumplir con el tipo declarado del identificador. 

- El tipo de let es el tipo del cuerpo. 

- El <expr> de un let se extiende tanto (abarca tantos tokens) como lo permita la gramática.

- 




### Execution


- cumplir el principio de sustitución de tipos en la herencia.

- cumpplir el polimorfismo en las llamadas a métodos.


### Chat-gpt says

Durante el chequeo semántico en el lenguaje Cool, se verifican diversas reglas y restricciones para garantizar que el programa sea válido y tenga un comportamiento semánticamente correcto. Aquí hay algunos aspectos clave que se deben verificar durante el chequeo semántico:

Declaraciones de clases y herencia: Se verifica que las clases estén correctamente definidas y que no haya ciclos en la herencia. Además, se comprueba que no se herede de clases prohibidas, como la clase Int, String o Bool.

Declaraciones de atributos: Se verifica que los atributos estén correctamente definidos y que no haya atributos duplicados en una clase. También se comprueba que los tipos de los atributos sean válidos y estén definidos.

Declaraciones de métodos: Se verifica que los métodos estén correctamente definidos y que no haya métodos duplicados en una clase. Además, se comprueba que los tipos de los parámetros y el tipo de retorno sean válidos y estén definidos.

Uso de variables y atributos: Se verifica que las variables y atributos utilizados estén previamente declarados. También se comprueba que los tipos de las variables y atributos sean correctos y coincidan con los tipos esperados.

Tipos de expresiones: Se verifica que los tipos de las expresiones sean coherentes y compatibles entre sí. Por ejemplo, se comprueba que no se realicen operaciones aritméticas entre tipos no numéricos.

Chequeo de tipos estáticos y dinámicos: Se realiza la verificación de tipos estáticos para garantizar que las asignaciones y operaciones sean válidas en tiempo de compilación. Además, se realiza la verificación de tipos dinámicos para garantizar que las operaciones y llamadas a métodos se realicen en objetos válidos y con los tipos correctos.

Reglas de alcance y visibilidad: Se verifica que las variables y atributos estén dentro de su alcance adecuado y que no se realicen accesos no permitidos a variables privadas desde fuera de la clase.

Reglas de herencia y redefinición de métodos: Se verifica que los métodos heredados sean correctamente redefinidos en las clases derivadas y que cumplan con las restricciones de covarianza y contravarianza.

Estos son solo algunos ejemplos de las verificaciones que se realizan durante el chequeo semántico en el lenguaje Cool. El objetivo es garantizar la coherencia y la corrección semántica del programa antes de proceder a la generación de código.