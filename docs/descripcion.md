#Difusión del Calor

##Mecanismo 
El mecanismo implementado consiste en simular como el calor se difunde radialmente a partir de una fuente de calor colocada en el centro hacia la periferia de un área rectangular. 

##Formula de difusión

$$
\frac{\partial u}{\partial t}
= \alpha\left(
\frac{\partial^2 u}{\partial x^2}
+ \frac{\partial^2 u}{\partial y^2}
\right), \qquad t>0,
$$

##Simulación
   Se simula cómo la difusión se da a lo largo del tiempo, recalculando iterativamente la intensidad del calor en cada punto del área rectangular (matriz) y generando la imágen (frame) correspondiente a cada iteración. Para hacer el recálculo se usa la fórmula de difusión indicada en el apartado anterior

##Implementación
Se hacen dos implementaciones: una en lenguaje Python y dos en lenguaje C++, una secuencial y otra usando paralelismo de memoria compartida con OpenMP
