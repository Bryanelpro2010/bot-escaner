import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

PLACE_ID = "109983668079237"

@app.route('/')
def home():
    return "Servidor Serverhop Activo 24/7", 200

@app.route('/get-target', methods=['GET'])
def get_target():
    cursor = ""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Intentamos buscar hasta en 3 páginas diferentes de servidores para asegurarnos de encontrar uno
    for _ in range(3):
        try:
            url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?sortOrder=Asc&limit=100"
            if cursor:
                url += f"&cursor={cursor}"
                
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                servers = data.get("data", [])
                cursor = data.get("nextPageCursor")
                
                # Buscamos estrictamente de 6 a 7 jugadores
                for srv in servers:
                    playing = srv.get("playing", 0)
                    max_players = srv.get("maxPlayers", 0)
                    
                    if 6 <= playing <= 7 and playing < max_players:
                        return jsonify({
                            "job_id": srv.get("id"),
                            "place_id": PLACE_ID
                        }), 200
                        
                if not cursor:
                    break
        except Exception as e:
            print(f"Error en bucle de búsqueda: {e}")
            break

    # Si de plano ningún servidor en todo el juego tiene 6-7 jugadores en ese momento, 
    # como último recurso devolvemos el primer servidor disponible que tenga espacio para no trabarte.
    try:
        fallback_url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?sortOrder=Asc&limit=10"
        fallback_res = requests.get(fallback_url, headers=headers, timeout=5)
        if fallback_res.status_code == 200:
            servers = fallback_res.json().get("data", [])
            for srv in servers:
                if srv.get("playing", 0) < srv.get("maxPlayers", 0):
                    return jsonify({
                        "job_id": srv.get("id"),
                        "place_id": PLACE_ID
                    }), 200
    except:
        pass

    return jsonify({
        "job_id": "",
        "place_id": PLACE_ID
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
