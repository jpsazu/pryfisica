# Utiliza una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el código de tu aplicación al contenedor
COPY . /app

# Instala las dependencias de la aplicación (necesitarás un archivo requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "-m", "src.salary"]
