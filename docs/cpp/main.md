# Mapa de calor (C++ API Serial)

## Función main:
 * Función principal que ejecuta la simulación de difusión térmica en 2D. Lee las dimensiones de la matriz y el número de iteraciones desde la línea de comandos. Inicializa el dominio, calcula parámetros físicos (dx, dy, dt) y realiza la evolución temporal aplicando difusión y manteniendo una región caliente en el centro. También mide el tiempo total de la simulación y guarda los resultados finales en un archivo.
 * Parámetros:
     *  argc, argv -> argumentos de entrada: Nx (filas), Ny (columnas), Nt (iteraciones)
 * Retorna:
     * 0 si la ejecución fue correcta
     * 1 si hay error en los argumentos
```cpp
#include <iostream>
#include <cmath>
#include <fstream>
#include <algorithm> 
#include <sys/time.h>

int main(int argc, char* argv[]) {
   // Verifica argumentos de entrada
   if(argc != 4){
    std::cerr <<"Debe escribir tres argumentos numerode filas numero de columnas numero de iteraciones" << std::endl;
    exit(1);
  } 
   
  // Dimensiones físicas del dominio
  double Lx=1.0;
  double Ly=1.0;
  int Nx; //Numero de filas
  int Ny; //Numero de columnas
  int Nt; //Numero de iteraciones (tiempo)
  
  // Conversión segura de argumentos
  try{
    Nx=std::stoi(argv[1]);
    Ny=std::stoi(argv[2]);
    Nt = std::stoi(argv[3]);
  }catch(const std::out_of_range& e) {
    std::cerr << "Error: el número está fuera del rango de int." << std::endl;
  } 
  
  // Cálculo de pasos espaciales y temporales
  double dx= Lx/Nx;
  double dy= Ly/Ny;
  double alpha=0.01; // coeficiente de difusión
  double dt=(0.25*std::min(dx, dy)*std::min(dx, dy))/alpha; // paso de tiempo estable
  
  // Reserva dinámica de memoria
  double *current= new double[Nx*Ny];
  double *prox=new double[Nx*Ny];
  double *temp;
  
  // Inicializa la matriz con ceros
  for(int i = 0; i < Nx; ++i) {
      for(int j = 0; j < Ny; ++j) {
          current[(i * Ny) + j] = 0;
      }
  }

  // Define el tamaño del cuadrado caliente en el centro
  double centro_medios= (Nx/10)/2;
  
  // Mide el tiempo de simulación
  double time_1 = seconds();
  
  // Bucle principal de tiempo (simulación)
  for(int n = 0; n < Nt; ++n){
    llenar_centro(Nx, Ny, centro_medios, current); // mantiene el centro caliente
    recalcular_matriz(Nx, Ny, current, prox, alpha, dx, dy, dt); // aplica difusión
    
    // Intercambia punteros (sin copiar matrices)
    temp=current;
    current=prox;
    prox=temp;	
  }
  double time_2 = seconds();
  std::cout << "# Time: " << time_2 - time_1 << std::endl;
  
  // Guarda los resultados en archivo
  guardar_datos( Nx, Ny, current);
  
  // Libera la memoria dinámica
  delete[] current;
  delete[] prox;
  return 0;
}
```
