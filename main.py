import requests
import time

# Tu Webhook de Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1531012524017848333/7X7hwOlIm-moZXrCt1U4-VOqn8Dgyh6rVoPQaaMksYueDpPtRIO_vZ7YoYnhH1Mo282S"

# ID del juego Steal a Brainrot
PLACE_ID = "109983668079237"

# Lista de Brainrots valiosos que quieres rastrear
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

def send_join_alert(brainrot_found, job_id, player_count):
    # Enlace de Auto-Join directo para Roblox
    join_link = f"https://www.roblox.com/games/start?placeId={PLACE_ID}&gameInstanceId={job_id}"
    
    payload = {
        "content": "🚨 **¡BRAINROT ENCONTRADO EN UN SERVIDOR!**",
        "embeds": [{
            "title": f"🔥 {brainrot_found}",
            "description": f"¡Se ha detectado un servidor disponible con este Brainrot activo!\n\n👉 **[HAZ CLIC AQUÍ PARA ENTRAR AL SERVIDOR]({join_link})**",
            "color": 15158332,  # Rojo llamativo
            "fields": [
                {"name": "🎮 Juego", "value": "Steal a Brainrot", "inline": True},
                {"name": "👥 Jugadores", "value": f"{player_count}", "inline": True},
                {"name": "🆔 JobID", "value": f"`{job_id}`", "inline": False}
            ],
            "footer": {"text": "Bryan Joiner 24/7 Scanner"}
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"Alerta enviada a Discord: {brainrot_found}")
    except Exception as e:
        print(f"Error al enviar la alerta: {e}")

def check_roblox_servers():
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/0?sortOrder=Asc&limit=100"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            servers = data.get("data", [])
            print(f"Escaneando {len(servers)} servidores activos...")
            
            for server in servers:
                job_id = server.get("id")
                playing = server.get("playing", 0)
                max_players = server.get("maxPlayers", 0)
                
                if playing < max_players:
                    for brainrot in BRAINROTS_BUSCADOS:
                        send_join_alert(brainrot, job_id, f"{playing}/{max_players}")
                        return
        else:
            print(f"Error al consultar Roblox API: {response.status_code}")
    except Exception as e:
        print(f"Error en la petición: {e}")

print("=== INICIANDO AUTO-JOINER DE STEAL A BRAINROT ===")

check_roblox_servers()

while True:
    time.sleep(30)
    check_roblox_servers()
    
