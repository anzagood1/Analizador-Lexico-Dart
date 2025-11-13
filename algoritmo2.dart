void main() {
  List<int> numeros = [10, 5, 27, 3, 15];

  int maximo = encontrarNumeroMaximo(numeros);

  print("La lista de números es: $numeros");
  print("El número más grande de la lista es: $maximo");
}

int encontrarNumeroMaximo(List<int> lista) {
  
  if (lista.isEmpty) {
    return 0;
  }

  int maxActual = lista[0];

  for (int numero in lista) {
    if (numero > maxActual) {
      maxActual = numero;
    }
  }

  return maxActual;
}