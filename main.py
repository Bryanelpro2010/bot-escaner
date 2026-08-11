import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# ID del juego configurada
PLACE_ID = "109983668079237"

@app.route('/')
def home():
    return "Servidor Serverhop Activo 24/7", 200

@app.route('/get-target', methods=['GET'])
def get_target():
    try:
        url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?sortOrder=Asc&limit=50"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            servers = response.json().get("data", [])
            
            # Filtro estricto: Busca exclusivamente servidores con 6 o 7 jugadores (ni más ni menos)
            for srv in servers:
                playing = srv.get("playing", 0)
                max_players = srv.get("maxPlayers", 0)
                
                if 6 <= playing <= 7 and playing < max_players:
                    return jsonify({
                        "job_id": srv.get("id"),
                        "place_id": PLACE_ID
                    }), 200
                    
    except Exception as e:
        print(f"Error en /get-target: {e}")

    return jsonify({
        "job_id": "",
        "place_id": PLACE_ID
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
