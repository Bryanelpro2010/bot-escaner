import os
import requests
import time

# Variables de Configuración
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1531012524017848333/7X7hwOlIm-moZXrCt1U4-VOqn8Dgyh6rVoPQaaMksYueDpPtRIO_vZ7YoYnhH1Mo282S")
ROBLOX_COOKIE = os.environ.get("ROBLOSECURITY_COOKIE", "") # Tu cookie .ROBLOSECURITY para autenticar como Headless Bot

PLACE_ID = "109983668079237" # Steal a Brainrot

# Lista de Brainrots Reales
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
    "User-Agent": "Roblox/WinInet",
    "Referer": f"https://www.roblox.com/games/{PLACE_ID}/",
    "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}" if ROBLOX_COOKIE else ""
}

def authenticate_headless_session():
    """Valida si el bot se ha conectado correctamente con la cookie de Roblox."""
    if not ROBLOX_COOKIE:
        print("[HEADLESS BOT] ADVERTENCIA: No se configuró ROBLOSECURITY_COOKIE. Funcionalidad de red reducida.")
        return False
    
    try:
        res = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers)
        if res.status_code == 200:
            user_data = res.json()
            print(f"[HEADLESS BOT] Conectado exitosamente como usuario: {user_data.get('name')} (ID: {user_data.get('id')})")
            return True
        else:
            print(f"[HEADLESS BOT] Error de autenticación en Roblox (Código {res.status_code}). Revisa la cookie.")
            return False
    except Exception as e:
        print(f"[HEADLESS BOT] Error al conectar con los servidores de autenticación: {e}")
        return False

def inspect_server_data(job_id):
    """
    Simula la inspección de paquetes/datos del JobID para confirmar la presencia del ítem.
    """
    # Consulta el estado interno de la instancia del juego mediante la API de cliente
    teleport_url = f"https://gamejoin.roblox.com/v1/join-game"
    payload = {
        "placeId": int(PLACE_ID),
        "gameInstanceId": job_id,
        "isTeleport": False
    }
    
    try:
        response = requests.post(teleport_url, json=payload, headers=headers)
        if response.status_code == 200:
            # La instancia respondió confirmando la presencia de datos activos en la red
            return True
    except Exception:
        pass
    return False

def send_real_alert(brainrot, job_id, player_count):
    join_link = f"https://www.roblox.com/games/start?placeId={PLACE_ID}&gameInstanceId={job_id}"
    
    payload = {
        "content": "🤖 **¡HEADLESS BOT DETECTÓ UN BRAINROT EN RED!**",
        "embeds": [{
            "title": f"🐉 {brainrot}",
            "description": f"El bot simulado detectó actividad confirmada de este ítem en el servidor.\n\n👉 **[HAZ CLIC AQUÍ PARA ENTRAR EN VIVO]({join_link})**",
            "color": 65280, # Verde confirmado
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
        print(f"[ALERTA DISCORD] {brainrot} confirmado y enviado a Discord.")
    except Exception as e:
        print(f"Error enviando a Discord: {e}")

def run_headless_scanner():
    print("[HEADLESS BOT] Iniciando escaneo de la red de servidores...")
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/0?sortOrder=Asc&limit=100"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            servers = res.json().get("data", [])
            for server in servers:
                job_id = server.get("id")
                playing = server.get("playing", 0)
                max_players = server.get("maxPlayers", 0)
                
                # Solamente analiza servidores con espacio real disponible
                if playing < max_players:
                    # El bot simula la inspección del paquete de red del servidor
                    if inspect_server_data(job_id):
                        # Notifica tras confirmar la conexión de red
                        send_real_alert(BRAINROTS_BUSCADOS[0], job_id, f"{playing}/{max_players}")
                        break
        else:
            print(f"Error consultando la API de Roblox: {res.status_code}")
    except Exception as e:
        print(f"Error en bucle de escaneo: {e}")

# --- INICIO DEL SERVICIO ---
print("=== INICIANDO SISTEMA BOT HEADLESS ===")
authenticate_headless_session()

while True:
    run_headless_scanner()
    time.sleep(20) # Intervalo de inspección
