# API Reference (Matrix)

### Resolución numérica de la ecuación de calor en 2D en un rectángulo}

#### 1. Planteamiento del problema

Sea el rectángulo
$$
0 < x < L_x, \qquad 0 < y < L_y,
$$
y la ecuación de calor
$$
\frac{\partial u}{\partial t}
= \alpha\left(
\frac{\partial^2 u}{\partial x^2}
+ \frac{\partial^2 u}{\partial y^2}
\right), \qquad t>0,
$$
con:

* condición inicial
$$
u(x,y,0) = f(x,y),
$$

* condiciones de frontera (por ejemplo, Dirichlet)
$$
u(x,y,t) = g(x,y,t)\quad \text{en la frontera}.
$$

donde $\alpha \gt 0$ es la difusividad térmica.

#### 2. Discretización del dominio
Dividimos el dominio espacial como:
$$
x_i = i\,\Delta x,\quad i=0,\dots,N_x,\qquad
y_j = j\,\Delta y,\quad j=0,\dots,N_y,
$$
donde
$$
\Delta x = \frac{L_x}{N_x},\qquad \Delta y = \frac{L_y}{N_y}.
$$

El tiempo se discretiza como
$$
t^n = n\,\Delta t,\qquad n=0,1,2,\dots
$$

Usamos la notación
$$
u_{i,j}^n \approx u(x_i,y_j,t^n).
$$

#### 3. Aproximaciones de derivadas espaciales
Para la segunda derivada en $x$:
$$
\frac{\partial^2 u}{\partial x^2}(x_i,y_j,t^n)
\approx 
\frac{
u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n
}{\Delta x^2}.
$$

Para la segunda derivada en $y$:
$$
\frac{\partial^2 u}{\partial y^2}(x_i,y_j,t^n)
\approx 
\frac{
u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n
}{\Delta y^2}.
$$

#### 4. Aproximación de la derivada temporal
Usamos diferencia hacia adelante:
$$
\frac{\partial u}{\partial t}(x_i,y_j,t^n)
\approx
\frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t}.
$$

#### 5. Esquema explícito FTCS

Combinando las aproximaciones, la ecuación de calor queda:
$$
\frac{u_{i,j}^{n+1} - u_{i,j}^{n}}{\Delta t}
=
\alpha\left(
\frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2}
+
\frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2}
\right).
$$

Definimos los parámetros de estabilidad:
$$
\lambda_x = \frac{\alpha\Delta t}{\Delta x^2},\qquad
\lambda_y = \frac{\alpha\Delta t}{\Delta y^2}.
$$

Despejando $u_{i,j}^{n+1}$:
$$
\boxed{
u_{i,j}^{n+1}
=
u_{i,j}^n
+
\lambda_x\left(u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n\right)
+
\lambda_y\left(u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n\right)
}
$$

Este esquema se aplica únicamente en los nodos interiores:
$$
i = 1,\dots,N_x-1,\qquad j = 1,\dots,N_y-1.
$$

#### 6. Condición inicial

$$
u_{i,j}^0 = f(x_i,y_j),\qquad \forall i,j.
$$

#### 7. Condiciones de frontera

Para frontera Dirichlet:
$$
u_{0,j}^n = g(0,y_j,t^n),\qquad
u_{N_x,j}^n = g(L_x,y_j,t^n),
$$
$$
u_{i,0}^n = g(x_i,0,t^n),\qquad
u_{i,N_y}^n = g(x_i,L_y,t^n).
$$

#### 8. Condición de estabilidad

Para el esquema explícito en 2D se requiere:
$$
\lambda_x + \lambda_y \le \frac{1}{2},
$$
lo cual equivale a:
$$
\Delta t \le 
\frac{1}{
2\alpha\left(\frac{1}{\Delta x^2} + \frac{1}{\Delta y^2}\right)
}.
$$

Si $\Delta x = \Delta y = h$, entonces:
$$
\Delta t \le \frac{h^2}{4\alpha}.
$$

#### 9. Algoritmo del esquema explícito

 1. Elegir $N_x$, $N_y$, $\Delta t$ y verificar estabilidad.
 
 2. Construir la malla $(x_i,y_j)$.
 
 3. Imponer la condición inicial $u_{i,j}^0$.
 
 4. Para cada paso de tiempo $n$:
 
        1. Imponer las condiciones de frontera.
		
        2. Actualizar los nodos interiores con la ecuación explícita:
		
      $$
        u_{i,j}^{n+1} =
        u_{i,j}^n
        +
        \lambda_x\left(u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n\right)
        +
        \lambda_y\left(u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n\right).
      $$
		
#### 10. Esquema implícito (idea general)

El esquema explícito requiere $\Delta t$ muy pequeño. Los esquemas implícitos permiten usar pasos más grandes resolviendo sistemas lineales.

##### 10.1 Backward Euler

$$
\frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t}
=
\alpha\left(
\frac{u_{i+1,j}^{n+1} - 2u_{i,j}^{n+1} + u_{i-1,j}^{n+1}}{\Delta x^2}
+
\frac{u_{i,j+1}^{n+1} - 2u_{i,j}^{n+1} + u_{i,j-1}^{n+1}}{\Delta y^2}
\right).
$$

En forma matricial:
$$
A\,\mathbf{u}^{n+1} = \mathbf{u}^n + \text{(fronteras)}.
$$

##### 10.2 Crank--Nicolson

$$
\frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t}
=
\alpha\,\frac{1}{2}
\left[
\Delta_h u_{i,j}^n
+
\Delta_h u_{i,j}^{n+1}
\right].
$$

Esto produce:
$$
\left(I - \frac{\Delta t\,\alpha}{2}A\right)\mathbf{u}^{n+1}
=
\left(I + \frac{\Delta t\,\alpha}{2}A\right)\mathbf{u}^{n}
+ \text{(fronteras)}.
$$



