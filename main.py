import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1531012524017848333/7X7hwOlIm-moZXrCt1U4-VOqn8Dgyh6rVoPQaaMksYueDpPtRIO_vZ7YoYnhH1Mo282S"

def send_status():
    data = {
        "embeds": [{
            "title": "🟢 BOT EN LA NUBE ACTIVO 24/7",
            "description": "El bot está ejecutándose correctamente en Render sin consumir recursos de tu teléfono/PC.",
            "color": 3066993,
            "footer": {"text": "Bryan Joiner Cloud Monitor"}
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Mensaje enviado a Discord correctamente.")
    except Exception as e:
        print(f"Error al enviar: {e}")

send_status()

while True:
    time.sleep(3600)
  
