import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
PLACE_ID = "109983668079237"

@app.route('/get-target', methods=['GET'])
def get_target():
    # Petición limpia y nueva cada vez que se llama a la URL
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?limit=10"
    try:
        # User-Agent es vital para que Roblox no bloquee la petición
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json().get("data", [])
            if data:
                # Devuelve el primer servidor encontrado en este instante
                return jsonify({"jobId": data[0].get("id")}), 200
    except:
        pass
    return jsonify({"jobId": ""}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
