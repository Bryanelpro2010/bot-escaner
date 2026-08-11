import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = "109983668079237"

@app.route('/get-target', methods=['GET'])
def get_target():
    # Buscamos en la primera página de servidores disponibles
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        if response.status_code == 200:
            servers = response.json().get("data", [])
            # Toma el primer servidor que tenga espacio libre y no sea el actual
            for srv in servers:
                if srv.get("playing", 0) < srv.get("maxPlayers", 0):
                    return jsonify({
                        "job_id": srv.get("id"),
                        "place_id": PLACE_ID
                    }), 200
    except:
        pass
    
    # Si algo falla, devuelve un error básico para que el script de Roblox no se quede colgado
    return jsonify({"job_id": "ERROR", "place_id": PLACE_ID}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
