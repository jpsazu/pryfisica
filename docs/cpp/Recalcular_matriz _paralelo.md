# Mapa de calor (C++ API Paralelizado)

## Función Recalcular matriz
 * Función que recalcula la matriz de temperatura usando el esquema de difusión 2D plica la ecuación de difusión mediante diferencias finitas recorriendo la zona interna de la matriz (excluyendo bordes). El cálculo principal se paraleliza mediante OpenMP utilizando paralelismo de memoria compartida, permitiendo que múltiples hilos actualicen distintas celdas simultáneamente. Luego se imponen condiciones de frontera reflejando el valor de los puntos interiores adyacentes.
 * Parámetros:
     * Nx, Ny  -> dimensiones de la matriz
     * current  -> puntero a la matriz con los valores actuales
     * prox     -> puntero a la matriz donde se almacenará el siguiente paso temporal
     * alpha    -> coeficiente de difusión térmica
     * dx, dy   -> separación espacial entre puntos en las direcciones x e y
     * dt       -> paso de tiempo
```cpp
#include <iostream>
#include <cmath>
#include <fstream>
#include <algorithm> 
#include <sys/time.h>

int recalcular_matriz( int Nx, int Ny, double *current, double *prox, double alpha, double dx, double dy, double dt){
  // Recorre la matriz (excepto bordes)
  #pragma omp for
  for(int i = 1; i < Nx-1; ++i){
    for(int j = 1; j < Ny-1; ++j){
      prox[(i*Ny) + j] = current[(i * Ny) + j]+
      alpha*dt*((current[((i+1)*Ny)+j]-2*current[(i * Ny) + j]+current[((i-1)*Ny)+j])/(dx*dx)+
      (current[(i * Ny) + j+1]-2*current[(i * Ny) + j]+current[(i * Ny) + j-1])/(dy*dy));
    }
  }
  
  // Condiciones de frontera (bordes reflejan el valor interior)
  for (int j = 0; j < Ny; ++j) {
    prox[0 * Ny + j] = prox[1 * Ny + j];         // borde izquierdo
    prox[(Nx - 1) * Ny + j] = prox[(Nx - 2) * Ny + j];   // borde derecho
  }
  for (int i = 0; i < Nx; ++i) {
    prox[i * Ny + 0] = prox[i * Ny + 1];         // borde inferior
    prox[i * Ny + (Ny - 1)] = prox[i * Ny + (Ny - 2)];   // borde superior
  }
  
  return 0;
}
```
