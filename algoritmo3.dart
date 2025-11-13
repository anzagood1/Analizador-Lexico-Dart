// Algoritmo de prueba analizador léxico

class Producto {
  String nombre;
  int cantidad;
  float precio;
  bool disponible;

  Producto(this.nombre, this.cantidad, this.precio, this.disponible);

  void mostrarInfo() {
    print('Producto: $nombre');
    print('Cantidad: $cantidad');
    print('Precio: ${precio.toString()}');
    print(disponible ? 'Disponible' : 'No disponible');
  }
}

void main() {
  var productos = [
    Producto('Teclado', 10, 29.99, true),
    Producto('Mouse', 0, 15.5, false),
    Producto('Monitor', 5, 150.0, true),
  ];

  for (var p in productos) {
    if (p.disponible && p.cantidad > 0) {
      p.mostrarInfo();
      if (p.precio > 100) {
        print('Producto premium.');
      } else {
        print('Producto estándar.');
      }
    } else {
      print('Producto fuera de stock.');
    }
  }

  /* Comentario
  en bloque */

  var resultado = (5 + 3) * 2 - 4 / 2;
  var bandera = true || false && !false;

  print('Resultado: $resultado');
  print('Bandera: $bandera');
}
