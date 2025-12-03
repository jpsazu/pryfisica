import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    """
      ## Función principal
      * Usa una matriz con las temperaturas correspondienes a cada punto.
      * Hace una simulación (animación) de como cambia la temperatura en cada punto con el paso del tiempo, usando la ecuación de calor.
      * Utiliza la función **update** para recalcular las temperaturas.
      * Usa la librería **matplotlib** para generar imágenes (frames) de un video
      * Aplica la función **FuncAnimation** pasándole como parámetro la función **update** con sus respectivos parámetros, para que actualize los datos y genere cada frame de la animación.
    """
    # Parámetros físicos y numéricos
    Lx, Ly = 1.0, 1.0     # Tamaño del dominio en las direcciones x e y (1 metro x 1 metro)
    Nx, Ny = 100, 100     # Número de puntos de la malla en x e y
    dx = Lx / Nx          # Espaciamiento entre nodos en x
    dy = Ly / Ny          # Espaciamiento entre nodos en y
    alpha = 0.01          # Difusividad térmica (m^2/s), controla qué tan rápido se propaga el calor

    # Paso de tiempo (dt) calculado usando la condición de estabilidad CFL
    # Para el método explícito, dt <= 0.25 * min(dx, dy)^2 / alpha
    dt = 0.25 * min(dx, dy)**2 / alpha  # Paso de tiempo (según condición CFL)
    Nt = 100             # Número total de pasos de tiempo de la simulación

    # Creación de la matriz
    u = np.zeros((Nx, Ny)) # Matriz 2D para la temperatura, inicialmente en 0 °C

    # Establece tamaño de la fuente (centro) de calor
    cento_medios=(Nx//10)//2  # Mitad del tamaño del cuadrado caliente
    cx, cy = Nx//2, Ny//2     # Coordenadas del centro del dominio

    # Crea una figura y un eje para la animación
    fig, ax = plt.subplots()  

    # Muestra la matriz de temperatura como una imagen en 2D
    img = ax.imshow(u, extent=[0, Lx, 0, Ly], origin='lower', cmap='hot', vmin=0, vmax=100)

    # Barra de color que muestra la escala de temperaturas
    cbar = plt.colorbar(img, ax=ax, label='Temperatura')

    # Etiquetas y título
    ax.set_title("Difusión de calor en 2D")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Crea la animación con la función de actualización 'update'
    ani = animation.FuncAnimation(fig, update, frames=Nt, interval=50, blit=False, fargs=(u,Nx,Ny,cento_medios,cx,cy,dx,dy,alpha,dt,img,ax,fig,Nt))

    # Muestra la simulación en pantalla
    plt.show()
    
def update(frame,u,Nx,Ny,cento_medios,cx,cy,dx,dy,alpha,dt,img,ax,fig,Nt):
    """
      ## Función update
      * Actualiza la matriz de temperatura **u** en cada paso de tiempo.
      * Pone los nuevos valores en una matriz auxiliar (**u_new**) para no sobre-escribir los actuales 
      * Luego toma la auxiliar como actual y generea el frame (imagen) correspondiente del video
      * Para calcular los nuevos valores usa la ecuación de calor en 2D
      * Aplica apropiadamente el cálculo para el área interna y para los bordes
      
      Args:
           frame(int): Numero de Fotograma
           u(matriz): Matriz anterior
           Nx(int): Cantidad de columnas
           Ny(int): Cantidad de filas
           cento_medios(int): mitad del numero de celdas del cuadrado central (fuente)
           cx(int): cordenada del centro en x
           cy(int): cordenada del centro en y
           dx(float): Espaciamiento entre nodos en x
           dy(float): Espaciamiento entre nodos en y
           alpha(float): coeficiente de difusividad térmica (m^2/s)
           dt(float): Paso de tiempo
           img(matplotlib.image.AxesImage): imagen que se va a actualizar
           ax(matplotlib.axes._axes.Axes): El área dentro de la figura donde se dibujan las gráficas
           fig(matplotlib.figure.Figure):la figura completa
           Nt(int):Número total de pasos de tiempo de la simulación
           
     Returns:
           (image):mapa de calor generado a partir de u
    """    

    # Establece el centro como fuente de calor
    u[cx-cento_medios:cx+cento_medios, cy-cento_medios:cy+cento_medios] = 100.0
    
    # Copia la matriz actual para evitar sobrescribir durante el cálculo
    u_new = u.copy()
    
    # Recalcula temperaturas interiores de la matriz (sin incluir los bordes)
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            # Ecuación de difusión discreta (método explícito)
            u_new[i,j] = u[i,j] + alpha * dt * (
                (u[i+1,j] - 2*u[i,j] + u[i-1,j]) / dx**2 +  # Segunda derivada en x
                (u[i,j+1] - 2*u[i,j] + u[i,j-1]) / dy**2    # Segunda derivada en y
            )
            
    # Recalcula temperatura de los bordes           
    u_new[0, :] = u_new[1, :]       # Borde superior
    u_new[-1, :] = u_new[-2, :]     # Borde inferior
    u_new[:, 0] = u_new[:, 1]       # Borde izquierdo
    u_new[:, -1] = u_new[:, -2]     # Borde derecho

    # Actualizamos la matriz original con los nuevos valores
    u[:,:] = u_new
    
    # Actualizamos la imagen mostrada
    img.set_array(u)
    
    # Actualizamos el título con el número de paso actual
    ax.set_title(f"Difusión de calor - paso {frame}")
    
    if frame>=Nt-1:
        plt.close(fig)
        
    return [img]

if __name__ == "__main__":
    main()
