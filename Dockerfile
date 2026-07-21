FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# Evitar que Python almacene en búfer stdout y stderr (útil para ver logs en Docker de inmediato)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend y el archivo HTML para el frontend
COPY monitor.py index.html ./

# Exponer el puerto en el que corre FastAPI
EXPOSE 8000

CMD ["python", "monitor.py"]
