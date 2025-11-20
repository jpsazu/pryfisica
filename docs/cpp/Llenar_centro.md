# Mapa de calor (C++ API Serial)

## Función Llenar Centro
 * Función que llena el centro de la matriz con temperatura 100.0 C
 * Parámetros:
     * Nx, Ny         -> dimensiones de la matriz
     * centro_medios  -> tamaño del cuadrado central
     * current        -> puntero a la matriz actual
```cpp
#include <iostream>
#include <cmath>
#include <fstream>
#include <algorithm> 
#include <sys/time.h>

int llenar_centro(int Nx, int Ny, double centro_medios, double *current) {
    for(int i = ((Nx/2) - centro_medios); i < (Nx/2) + centro_medios; ++i) {
        for(int j = (Ny/2) - centro_medios; j < ((Ny/2) + centro_medios); ++j) {
            current[(i * Ny) + j] = 100.0; // asigna valor 100 en el centro
        }
    }
    return 0;
}
```
