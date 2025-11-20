# Mapa de calor (C++ API Serial)

## Función Recalcular matriz
 * Función que recalcula los valores de temperatura (difusión térmica) usando un esquema explícito en diferencias finitas
 * Parámetros:
     * Nx, Ny -> dimensiones de la matriz
     * current -> matriz actual
     * prox    -> matriz siguiente
     * alpha   -> coeficiente de difusión
     * dx, dy  -> tamaño de paso espacial
     * dt      -> paso de tiempo
```cpp
#include <iostream>
#include <cmath>
#include <fstream>
#include <algorithm> 
#include <sys/time.h>

int recalcular_matriz( int Nx, int Ny, double *current, double *prox, double alpha, double dx, double dy, double dt){
  // Recorre la matriz (excepto bordes)
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
