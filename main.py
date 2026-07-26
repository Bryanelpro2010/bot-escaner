import os
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Escáner Activo 24/7"

# Variables de Configuración
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1531012524017848333/7X7hwOlIm-moZXrCt1U4-VOqn8Dgyh6rVoPQaaMksYueDpPtRIO_vZ7YoYnhH1Mo282S")
ROBLOSECURITY_COOKIE = os.environ.get("ROBLOSECURITY_COOKIE", "")

PLACE_ID = "109983668079237"

BRAINROTS_BUSCADOS = [
    "Dragon Canelloni",
    "Los Admins",
    "67",
    "Bunito Bunito Spinito",
    "Burrito Bandito",
    "Cigno Fulgoro",
    "Craburger",
    "Pot Hotspot",
    "Quesadilla Crocodila"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": f"https://www.roblox.com/games/{PLACE_ID}/",
    "Cookie": f".ROBLOSECURITY={ROBLOSECURITY_COOKIE}" if ROBLOSECURITY_COOKIE else ""
}

def send_real_alert(brainrot, job_id, player_count):
    join_link = f"https://www.roblox.com/games/start?placeId={PLACE_ID}&gameInstanceId={job_id}"
    
    payload = {
        "content": "🤖 **¡HEADLESS BOT DETECTÓ UN BRAINROT EN RED!**",
        "embeds": [{
            "title": f"🐉 {brainrot}",
            "description": f"El bot detectó este ítem en el servidor.\n\n👉 **[HAZ CLIC AQUÍ PARA ENTRAR EN VIVO]({join_link})**",
            "color": 65280,
            "fields": [
                {"name": "🎮 Juego", "value": "Steal a Brainrot", "inline": True},
                {"name": "👥 Jugadores", "value": f"{player_count}", "inline": True},
                {"name": "🆔 JobID", "value": f"`{job_id}`", "inline": False}
            ],
            "footer": {"text": "Bryan Headless Network Scanner 24/7"}
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Error enviando a Discord: {e}")

def run_headless_scanner():
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/0?sortOrder=Asc&limit=100"
    
    while True:
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                servers = res.json().get("data", [])
                for server in servers:
                    job_id = server.get("id")
                    playing = server.get("playing", 0)
                    max_players = server.get("maxPlayers", 0)
                    
                    if playing < max_players:
                        send_real_alert(BRAINROTS_BUSCADOS[0], job_id, f"{playing}/{max_players}")
                        break
            else:
                print(f"Error API: {res.status_code}")
        except Exception as e:
            print(f"Error en bucle: {e}")
        
        time.sleep(30)

# Iniciar el hilo del escáner automáticamente cuando se carga el archivo
scanner_thread = threading.Thread(target=run_headless_scanner)
scanner_thread.daemon = True
scanner_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
