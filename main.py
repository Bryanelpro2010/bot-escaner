import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = "109983668079237"

@app.route('/get-target', methods=['GET'])
def get_target():
    cursor = ""
    # 10 ciclos de 100 servidores = 1000 servidores
    for _ in range(10): 
        url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=100&cursor={cursor}"
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if res.status_code == 200:
                data = res.json()
                for srv in data.get("data", []):
                    # Filtro exacto de 6 a 7 jugadores
                    if 6 <= srv.get("playing", 0) <= 7:
                        return jsonify({"job_id": srv["id"], "place_id": PLACE_ID})
                
                cursor = data.get("nextPageCursor")
                if not cursor: break
        except: break
    
    return jsonify({"job_id": "NONE", "place_id": PLACE_ID})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
