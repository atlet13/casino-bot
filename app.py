from flask import Flask, request, jsonify, send_from_directory
import random
import os

app = Flask(__name__, static_folder="web", static_url_path="")

PLINKO = [(2,50),(4,25),(8,15),(16,7),(24,3)]

def get_mult():
    r = random.randint(1, 100)
    s = 0
    for m, c in PLINKO:
        s += c
        if r <= s:
            return m
    return 2

@app.route("/plinko", methods=["POST"])
def plinko():
    data = request.json

    try:
        bet = float(data.get("bet", 0))
    except:
        bet = 0

    mult = get_mult()
    win = bet * mult

    return jsonify({
        "mult": mult,
        "win": win
    })

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)