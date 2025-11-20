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
= c^2\left(
\frac{\partial^2 u}{\partial x^2}
+ \frac{\partial^2 u}{\partial y^2}
\right), \qquad t>0,
$$

sustituyendo $c^2=\alpha$ entonces:

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

* condiciones de frontera (por ejemplo, Neumann)

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

Para frontera Neumann:

Las condiciones de **Neumann** establecen el valor de la **derivada normal de la temperatura en la frontera**.  
Para un sistema **aislado térmicamente**, esto significa que **no hay flujo de calor a través de las fronteras**, es decir:

$$
\frac{\partial u}{\partial n} = 0
$$

donde $n$ es la dirección normal a la frontera.

En términos discretos (diferencias finitas):

$$
u_{\text{frontera}} = u_{\text{nodo vecino interior}}
$$

Esto refleja el valor interior hacia el borde, simulando que **el calor no puede escapar**.

---

 en el código

En la función `recalcular_matriz` se implementa de la siguiente manera:

```cpp
// Condiciones de frontera (bordes reflejan el valor interior)
for (int j = 0; j < Ny; ++j) {
    prox[0 * Ny + j] = prox[1 * Ny + j];         // borde izquierdo
    prox[(Nx - 1) * Ny + j] = prox[(Nx - 2) * Ny + j];   // borde derecho
}
for (int i = 0; i < Nx; ++i) {
    prox[i * Ny + 0] = prox[i * Ny + 1];         // borde inferior
    prox[i * Ny + (Ny - 1)] = prox[i * Ny + (Ny - 2)];   // borde superior
}
```

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
		




