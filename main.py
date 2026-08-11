import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = "109983668079237"

@app.route('/get-target', methods=['GET'])
def get_target():
    cursor = ""
    # Revisa hasta 3 páginas (300 servidores) para asegurar encontrar uno de 6-7
    for _ in range(3):
        url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100&cursor={cursor}"
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
            if res.status_code == 200:
                data = res.json()
                for srv in data.get("data", []):
                    # Filtro exacto que tú quieres: entre 6 y 7 jugadores
                    playing = srv.get("playing", 0)
                    if 6 <= playing <= 7:
                        return jsonify({
                            "job_id": srv.get("id"),
                            "place_id": PLACE_ID
                        }), 200
                
                cursor = data.get("nextPageCursor")
                if not cursor:
                    break
        except:
            break
            
    # Si de verdad ninguno tiene 6-7 en ese momento, devuelve vacío
    return jsonify({"job_id": "", "place_id": PLACE_ID}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
