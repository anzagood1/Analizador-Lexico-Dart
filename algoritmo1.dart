// Programa de prueba para el analizador léxico
var nombre = "Lisbeth";
var edad = 20;
var altura? = 1.68;
final PI = 3.1416;
const saludo = 'Hola Mundo';

int contador = 0;
bool activo = true;
String mensaje = "Analizador léxico funcionando";

// Estructura condicional
if (edad > 18 && activo) {
  print("Usuario adulto y activo");
} else {
  print("Usuario inactivo o menor de edad");
}

// Bucle while
while (contador < 3) {
  print("Contador: " + contador.toString());
  contador = contador + 1;
}

// Bucle for
for (var i = 0; i < 5; i++) {
  print("Iteración número " + i.toString());
}

// Expresiones y operadores
var resultado = (edad + altura) / 2 * PI;
print(resultado);
