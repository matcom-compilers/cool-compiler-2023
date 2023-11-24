 
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