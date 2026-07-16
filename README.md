# Simulador de Monitoreo de Servidores con Alertas

Este proyecto contiene un script en Python que simula el monitoreo del estado de varios servidores críticos de una empresa (ej. Frontend, Base de datos, APIs). Si un servidor pasa de estar activo (UP) a estar caído (DOWN), o viceversa, el script envía una alerta automática a un canal de Discord o Telegram.

El proyecto está preparado para ser empaquetado y ejecutado dentro de un contenedor **Docker**.

## Estructura del Proyecto

- `monitor.py`: Script de Python con la lógica de simulación de monitoreo y envío de alertas a webhooks/APIs.
- `requirements.txt`: Dependencias necesarias (`requests` para las peticiones HTTP y `python-dotenv` para cargar variables de entorno).
- `Dockerfile`: Configuración para empaquetar la aplicación en un contenedor de Docker.
- `.env.example`: Plantilla de variables de entorno para configurar las alertas y el intervalo de monitoreo.

---

## Configuración de Alertas (Opcional)

Si deseas recibir alertas reales en Discord o Telegram, realiza lo siguiente antes de ejecutar:

1. Crea una copia del archivo `.env.example` y llámala `.env`:
   ```bash
   cp .env.example .env
   ```
2. Configura los canales:
   - **Discord**: Crea un Webhook en la configuración de tu canal de Discord e introduce la URL obtenida en `DISCORD_WEBHOOK_URL`.
   - **Telegram**: Crea un bot conversando con `@BotFather` para obtener el Token. Luego obtén tu ID de chat con `@userinfobot`. Llena `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`.
   
*Nota: Si no configuras ninguno de los dos, el script funcionará en **Modo Simulación Local** mostrando las alertas en la consola en color rojo/verde.*

---

## Ejecución Local (Sin Docker)

Si quieres probarlo directamente en tu máquina local:

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el monitor:
   ```bash
   python monitor.py
   ```

---

## Ejecución con Docker (Recomendado)

Sigue estos pasos para empaquetar y ejecutar la aplicación con Docker:

### 1. Construir la Imagen de Docker
Usa el siguiente comando desde el directorio raíz del proyecto para crear la imagen:
```bash
docker build -t server-monitor .
```

### 2. Ejecutar el Contenedor

#### Opción A: Ejecución en Modo Simulación Local (Sin Alertas Externas)
Ejecuta el contenedor sin pasar variables de entorno. Las alertas se imprimirán en los logs del contenedor:
```bash
docker run --name mi-monitor server-monitor
```

#### Opción B: Ejecución con Alertas Reales (Pasando el archivo `.env`)
Si configuraste el archivo `.env`, puedes pasarle las variables al contenedor al iniciarlo:
```bash
docker run --name mi-monitor --env-file .env server-monitor
```

### 3. Detener el Contenedor
Para detener el monitor de forma limpia, usa:
```bash
docker stop mi-monitor
```

Para volver a iniciarlo:
```bash
docker start -a mi-monitor
```
