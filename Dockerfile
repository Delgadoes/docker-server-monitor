# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Creamos el directorio de trabajo
WORKDIR /app

# Copiamos todos nuestros archivos (monitor.py e index.html) al contenedor
COPY . /app

# Instalamos el motor web y las herramientas necesarias
RUN pip install --no-cache-dir fastapi uvicorn requests

# Le decimos al contenedor que abra el puerto 8000 hacia el exterior
EXPOSE 8000

# El nuevo comando de encendido: ejecuta Uvicorn escuchando en todas las interfaces de red
CMD ["uvicorn", "monitor:app", "--host", "0.0.0.0", "--port", "8000"]