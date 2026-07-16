import os
import sys
import time
import random
import requests
from datetime import datetime
from dotenv import load_dotenv

# Evitar errores de codificación con emojis en consolas de Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Configuración
INTERVALO_MONITOR = int(os.getenv("INTERVALO_MONITOR", "10"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Lista de servidores a monitorear y su estado inicial (True = UP, False = DOWN)
SERVIDORES = {
    "Web Frontend": True,
    "Payment Gateway": True,
    "Database Master": False,
    "Auth API Service": True,
    "Caching Redis": True
}

# Probabilidades de cambio de estado (para simular caídas y recuperaciones)
PROB_CAIDA = 0.15       # 15% de probabilidad de que un servidor UP se caiga
PROB_RECUPERACION = 0.50 # 50% de probabilidad de que un servidor DOWN se recupere

def obtener_marca_tiempo():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def enviar_alerta_discord(mensaje):
    if not DISCORD_WEBHOOK_URL:
        return False
    try:
        payload = {"content": mensaje}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        return response.status_code == 204 or response.status_code == 200
    except Exception as e:
        print(f"[{obtener_marca_tiempo()}] ❌ Error al enviar alerta a Discord: {e}")
        return False

def enviar_alerta_telegram(mensaje):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensaje,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"[{obtener_marca_tiempo()}] ❌ Error al enviar alerta a Telegram: {e}")
        return False

def notificar_alerta(servidor, estado_nuevo):
    timestamp = obtener_marca_tiempo()
    if estado_nuevo:
        # Recuperación
        mensaje_consola = f"\033[92m[{timestamp}] ✅ [RECUPERADO] El servidor '{servidor}' ha vuelto a estar en línea.\033[0m"
        mensaje_alerta = f"✅ **[RECUPERACIÓN]** El servidor **{servidor}** ha vuelto a estar en línea a las `{timestamp}`."
    else:
        # Caída
        mensaje_consola = f"\033[91m[{timestamp}] 🚨 [CRÍTICO] ¡El servidor '{servidor}' se ha caído!\033[0m"
        mensaje_alerta = f"🚨 **[CRÍTICO]** ¡El servidor **{servidor}** se ha caído a las `{timestamp}`! Requiere atención inmediata."

    # Mostrar en consola siempre
    print(mensaje_consola)

    # Enviar a Discord
    if DISCORD_WEBHOOK_URL:
        if enviar_alerta_discord(mensaje_alerta):
            print(f"[{timestamp}] 💬 Alerta enviada a Discord exitosamente.")
        else:
            print(f"[{timestamp}] ⚠️ Falló el envío de alerta a Discord.")

    # Enviar a Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        if enviar_alerta_telegram(mensaje_alerta):
            print(f"[{timestamp}] 💬 Alerta enviada a Telegram exitosamente.")
        else:
            print(f"[{timestamp}] ⚠️ Falló el envío de alerta a Telegram.")

    # Si no hay canales configurados
    if not DISCORD_WEBHOOK_URL and not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        print(f"[{timestamp}] ℹ️ Modo simulación local: Configura variables en un archivo .env o en el entorno para recibir alertas reales.")

def simular_monitoreo():
    print("=" * 60)
    print(f"🚀 Iniciando Simulador de Monitoreo de Servidores")
    print(f"⏰ Intervalo de verificación: {INTERVALO_MONITOR} segundos")
    print(f"📢 Canales activos:")
    print(f"   - Discord: {'ACTIVO' if DISCORD_WEBHOOK_URL else 'INACTIVO (Mock)'}")
    print(f"   - Telegram: {'ACTIVO' if (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID) else 'INACTIVO (Mock)'}")
    print("=" * 60)

    try:
        while True:
            print(f"\n[{obtener_marca_tiempo()}] 🔍 Verificando estado de los servidores...")
            
            # Revisar cada servidor
            for servidor, estado_actual in SERVIDORES.items():
                # Simular cambio de estado aleatorio
                cambio = random.random()
                
                if estado_actual: # El servidor está activo
                    if cambio < PROB_CAIDA:
                        # Servidor se cae
                        SERVIDORES[servidor] = False
                        notificar_alerta(servidor, False)
                else: # El servidor está caído
                    if cambio < PROB_RECUPERACION:
                        # Servidor se recupera
                        SERVIDORES[servidor] = True
                        notificar_alerta(servidor, True)
            
            # Mostrar resumen de estados actuales en consola
            estados_str = ", ".join([f"{s}: {'✅ UP' if e else '🚨 DOWN'}" for s, e in SERVIDORES.items()])
            print(f"[{obtener_marca_tiempo()}] Resumen: {estados_str}")
            
            # Esperar hasta la siguiente iteración
            time.sleep(INTERVALO_MONITOR)

    except KeyboardInterrupt:
        print(f"\n[{obtener_marca_tiempo()}] 🛑 Simulador detenido por el usuario.")

if __name__ == "__main__":
    simular_monitoreo()
