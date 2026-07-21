from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Aquí puedes agregar o cambiar las URLs que quieras monitorear
SITIOS = [
    {"nombre": "Google", "url": "https://www.google.com"},
    {"nombre": "GitHub", "url": "https://github.com"},
    {"nombre": "Sitio Falso (Para probar error)", "url": "https://este-sitio-no-existe.com"}
]

@app.get("/api/status")
def revisar_estado():
    resultados = []
    for sitio in SITIOS:
        try:
            # Hacemos la petición a la web
            respuesta = requests.get(sitio["url"], timeout=5)
            estado = "Activo" if respuesta.status_code == 200 else "Caído"
        except:
            estado = "Caído"
        
        resultados.append({
            "nombre": sitio["nombre"],
            "url": sitio["url"],
            "estado": estado
        })
    return resultados

@app.get("/", response_class=HTMLResponse)
def cargar_dashboard():
    # Esta ruta lee y muestra tu archivo HTML
    with open("index.html", "r", encoding="utf-8") as archivo:
        return archivo.read()

# Permite ejecutar el script directamente con 'python monitor.py'
if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor de monitoreo en http://localhost:8000")
    uvicorn.run("monitor:app", host="0.0.0.0", port=8000, reload=True)
