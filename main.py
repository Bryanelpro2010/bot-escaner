import os
import requests
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Webhook de Discord configurado por defecto
WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK", 
    "https://discord.com/api/webhooks/1531012524017848333/7X7hwOlIm-moZXrCt1U4-VOqn8Dgyh6rVoPQaaMksYueDpPtRIO_vZ7YoYnhH1Mo282S"
)

PLACE_ID = "109983668079237"

# Mapeo de colores y nombres por nivel de prioridad
PRIORITIES = {
    1: {"name": "🟢 COMÚN", "color": 5635925},
    2: {"name": "🔵 RARO", "color": 5592575},
    3: {"name": "🟣 ÉPICO", "color": 11141290},
    4: {"name": "🟡 LEGENDARIO", "color": 16776960},
    5: {"name": "🔴 MÍTICO", "color": 16733005},
    6: {"name": "⚡ BRAINROT GOD", "color": 16755200},
    7: {"name": "👑 SECRETO", "color": 65535}
}

# Registro en memoria para evitar alertas duplicadas (Límite: 1 cada 5 minutos por servidor/brainrot)
recent_reports = {}

def is_duplicate(job_id, brainrot_name):
    key = f"{job_id}_{brainrot_name}"
    current_time = time.time()
    
    # Limpiar registros de más de 300 segundos
    for k in list(recent_reports.keys()):
        if current_time - recent_reports[k] > 300:
            del recent_reports[k]

    if key in recent_reports:
        return True
    
    recent_reports[key] = current_time
    return False

@app.route('/')
def home():
    return "Servidor de Radar de Brainrots Activo 24/7 en Render", 200

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Sin datos"}), 400

    brainrot_name = data.get("brainrot", "Desconocido")
    priority = int(data.get("priority", 1))
    finder = data.get("finder", "Anónimo")
    job_id = data.get("job_id", "")
    place_id = data.get("place_id", PLACE_ID)

    if is_duplicate(job_id, brainrot_name):
        return jsonify({"status": "ignored", "message": "Reporte duplicado"}), 200

    tier = PRIORITIES.get(priority, PRIORITIES[1])
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
                {"name": "👤 Encontrado por", "value": finder, "inline": True},
                {"name": "🆔 JobID", "value": f"`{job_id}`", "inline": False}
            ],
            "footer": {"text": "Bryan Community Network Scanner 24/7"}
        }]
    }

    try:
        res = requests.post(WEBHOOK_URL, json=payload)
        if res.status_code in [200, 204]:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "code": res.status_code}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
