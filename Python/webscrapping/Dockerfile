# Usamos la imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app/webscrapping

# Copiamos los archivos necesarios al contenedor
COPY requirements.txt .
COPY webscrapping.py .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar la aplicación
CMD ["python", "webscrapping.py"]
