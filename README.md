\# Analizador de Compiladores para Dart (Python + PLY)



Este proyecto implementa un analizador completo (\*\*Léxico, Sintáctico y Semántico\*\*) para un subconjunto del lenguaje de programación \*\*Dart\*\*. Ha sido desarrollado en Python utilizando la librería `PLY` (Python Lex-Yacc) e incluye una interfaz gráfica (GUI) construida con `Tkinter` para facilitar la visualización del proceso de compilación y las pruebas de código.



\## 📋 Descripción de Módulos



El sistema está dividido en cuatro componentes principales que trabajan en conjunto:



\### 1. Análisis Léxico (`AnalizadorLexDart.py`)

Este módulo se encarga de la tokenización de la entrada.

\* \*\*Identificación de Tokens:\*\* Reconoce identificadores, números (enteros y flotantes), cadenas de texto y símbolos especiales.

\* \*\*Palabras Reservadas:\*\* Soporte para `abstract`, `async`, `await`, `class`, `const`, `final`, `implements`, `try`, `catch`, `var`, `void`, entre otras.

\* \*\*Operadores:\*\*

&nbsp;   \* Aritméticos: `+`, `-`, `\*`, `/`.

&nbsp;   \* Lógicos y Relacionales: `\&\&`, `||`, `!`, `==`, `!=`, `<`, `>`.

&nbsp;   \* \*\*Bitwise (Bit a bit):\*\* `\&`, `|`, `^`, `~`, `<<`, `>>`.

\* \*\*Manejo de Errores:\*\* Reporta caracteres desconocidos indicando la línea específica del error.



\### 2. Análisis Sintáctico (`AnalizadorSinDart.py`)

Define la gramática libre de contexto y valida la estructura del código.

\* \*\*Declaraciones:\*\* Variables tipadas (`int`, `bool`, `List`, `Queue`) y dinámicas (`var`).

\* \*\*Estructuras de Control:\*\* `if`, `else`, `else if`, `while`, `for` estándar y `for-in`.

\* \*\*Funciones:\*\*

&nbsp;   \* Declaración de funciones `void` y con retorno.

&nbsp;   \* Funciones asíncronas (`Future`, `async`, `await`).

&nbsp;   \* Funciones flecha (Lambdas `=>`).

\* \*\*POO:\*\* Definición de clases, clases abstractas e interfaces.

\* \*\*Colecciones:\*\* Sintaxis específica para `List` y `Queue`.



\### 3. Análisis Semántico (Integrado)

Realiza validaciones lógicas durante el parseo para asegurar la coherencia del programa:

\* \*\*Tabla de Símbolos:\*\* Registra variables y funciones para controlar el ámbito (scope).

\* \*\*Verificación de Tipos:\*\* Detecta asignaciones incompatibles (ej. asignar un `String` a un `int`) y permite conversiones válidas (ej. `int` a `float`).

\* \*\*Inferencia:\*\* Deduce tipos en declaraciones `var` basándose en el valor asignado.

\* \*\*Validación de Existencia:\*\* Alerta si se intenta usar una variable o función no declarada.



\### 4. Interfaz Gráfica (`interface.py`)

Proporciona un entorno visual amigable para el usuario:

\* \*\*Editor de Código:\*\* Área de texto con scroll para escribir el código fuente.

\* \*\*Live Preview:\*\* Panel de salida que muestra los resultados del análisis en tiempo real.

\* \*\*Funciones:\*\* Botones para "Evaluar código" y "Resetear" la entrada.



---



\## 🛠️ Requisitos e Instalación



\### Prerrequisitos

\* \*\*Python 3.x\*\* instalado.

\* Librería \*\*PLY\*\* (Python Lex-Yacc).

