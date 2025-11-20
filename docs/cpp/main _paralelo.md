# Mapa de calor (C++ Paralelizado )

## Función main:
 * Función principal que configura y ejecuta la simulación de difusión térmica 2D Valida los argumentos de entrada y establece las dimensiones físicas del dominio. Calcula los pasos espaciales y el paso de tiempo estable, reserva memoria para las matrices y las inicializa. En cada iteración temporal, mantiene un cuadrado central a alta temperatura y aplica la ecuación de difusión. El cálculo de la difusión se paraleliza mediante OpenMP usando paralelismo de memoria compartida, permitiendo que múltiples hilos actualicen distintas regiones de la matriz en forma concurrente. Se miden los tiempos, se guardan los resultados finales y se libera la memoria reservada antes de finalizar la ejecución..
 * Parámetros:
     * argc, argv -> argumentos de línea de comandos:
                     [1] número de filas (Nx)
                     [2] número de columnas (Ny)
                     [3] número de iteraciones temporales (Nt)
                     
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
  int num_threads;
  
  // Bucle principal de tiempo (simulación)
  for(int n = 0; n < Nt; ++n){
    llenar_centro(Nx, Ny, centro_medios, current); // mantiene el centro caliente
    #pragma omp parallel 
    {
      num_threads = omp_get_num_threads();   
      recalcular_matriz(Nx, Ny, current, prox, alpha, dx, dy, dt); // aplica difusión
    }
    // Intercambia punteros (sin copiar matrices)
    temp=current;
    current=prox;
    prox=temp;	
  }
  double time_2 = seconds();
  std::cout << "# Num Threads: " << num_threads << std::endl;
  std::cout << "# Time: " << time_2 - time_1 << std::endl;
  
  // Guarda los resultados en archivo
  guardar_datos( Nx, Ny, current);
  
  // Libera la memoria dinámica
  delete[] current;
  delete[] prox;
  return 0;
}
```
