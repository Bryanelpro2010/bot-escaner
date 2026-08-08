import os
import requests
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Webhook de Discord
WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK", 
    "https://discord.com/api/webhooks/1531012524017848333/7X7hwOlIm-moZXrCt1U4-VOqn8Dgyh6rVoPQaaMksYueDpPtRIO_vZ7YoYnhH1Mo282S"
)

PLACE_ID = "109983668079237"

last_target_server = {
    "job_id": "",
    "brainrot": "",
    "priority": 0,
    "place_id": PLACE_ID,
    "players": 0
}

PRIORITIES = {
    1: {"name": "🟢 COMÚN", "color": 5635925},
    2: {"name": "🔵 RARO", "color": 5592575},
    3: {"name": "🟣 ÉPICO", "color": 11141290},
    4: {"name": "🟡 LEGENDARIO", "color": 16776960},
    5: {"name": "🔴 MÍTICO", "color": 16733005},
    6: {"name": "⚡ BRAINROT GOD", "color": 16755200},
    7: {"name": "👑 SECRETO", "color": 65535},
    8: {"name": "🔥 OG EXCLUSIVO", "color": 16711680}
}

recent_reports = {}

def is_duplicate(job_id, brainrot_name):
    key = f"{job_id}_{brainrot_name}"
    current_time = time.time()
    for k in list(recent_reports.keys()):
        if current_time - recent_reports[k] > 300:
            del recent_reports[k]
    if key in recent_reports:
        return True
    recent_reports[key] = current_time
    return False

@app.route('/')
def home():
    return "Servidor Serverhoop Activo 24/7", 200

@app.route('/report', methods=['POST'])
def receive_report():
    global last_target_server
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Sin datos"}), 400

    brainrot_name = data.get("brainrot", "Desconocido")
    priority = int(data.get("priority", 1))
    finder = data.get("finder", "Anónimo")
    job_id = data.get("job_id", "")
    place_id = data.get("place_id", PLACE_ID)
    players_count = int(data.get("players", 0))

    og_list = ["Strawberry Elephant", "Skibidi Toilet", "John Pork", "Meowl", "Headlees Horseman", "Spyder Elephant"]
    if brainrot_name in og_list:
        priority = 8

    if job_id:
        last_target_server = {
            "job_id": job_id,
            "brainrot": brainrot_name,
            "priority": priority,
            "place_id": place_id,
            "players": players_count
        }

    if is_duplicate(job_id, brainrot_name):
        return jsonify({"status": "ignored", "message": "Duplicado"}), 200

    tier = PRIORITIES.get(priority, PRIORITIES[8] if priority == 8 else PRIORITIES[1])
    join_link = f"https://www.roblox.com/games/start?placeId={place_id}&gameInstanceId={job_id}"

    payload = {
        "content": "🚨 **¡ATENCIÓN @everyone! BRAINROT DE ALTO VALOR DETECTADO**" if priority >= 5 else None,
        "embeds": [{
            "title": f"{tier['name']} - {brainrot_name}",
            "description": f"¡Un jugador ha detectado un Brainrot en vivo!\n\n👉 **[HAZ CLIC AQUÍ PARA ENTRAR AL SERVIDOR]({join_link})**",
            "color": tier["color"],
            "fields": [
                {"name": "🧠 Brainrot", "value": f"**{brainrot_name}**", "inline": True},
                {"name": "⭐ Prioridad", "value": f"Nivel {priority}", "inline": True},
                {"name": "👥 Jugadores", "value": f"{players_count} activos", "inline": True},
                {"name": "👤 Encontrado por", "value": finder, "inline": True},
                {"name": "🆔 JobID", "value": f"`{job_id}`", "inline": False}
            ],
            "footer": {"text": "Bryan Community Network Scanner 24/7"}
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

    return jsonify({"status": "success"}), 200

@app.route('/get-target', methods=['GET'])
def get_target():
    return jsonify(last_target_server), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    return jsonify(last_target_server), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
