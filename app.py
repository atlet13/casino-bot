from flask import Flask, send_from_directory, request, jsonify
import random, json, os

app = Flask(__name__, static_folder="web", static_url_path="")

DB = "db.json"
SETTINGS = {"edge": 0.6}  # контроль шансів
stats = {"plays": 0, "wins": 0}
games = {}

# ---------- DB ----------
def load():
    if not os.path.exists(DB):
        return {}
    with open(DB, "r") as f:
        return json.load(f)

def save(db):
    with open(DB, "w") as f:
        json.dump(db, f)

def get_user(uid):
    db = load()
    if uid not in db:
        db[uid] = {"balance": 100}
        save(db)
    return db[uid]

def set_user(uid, data):
    db = load()
    db[uid] = data
    save(db)

# ---------- ROUTES ----------
@app.route("/")
def home():
    return send_from_directory("web", "index.html")

@app.route("/balance", methods=["POST"])
def balance():
    uid = str(request.json["user_id"])
    return jsonify(get_user(uid))

# ---------- PLINKO ----------
@app.route("/play", methods=["POST"])
def play():
    data = request.json
    uid = str(data["user_id"])
    bet = float(data["bet"])

    user = get_user(uid)

    if user["balance"] < bet:
        return {"error": "Нема балансу"}

    user["balance"] -= bet

    if random.random() < SETTINGS["edge"]:
        mult = 0
    else:
        mult = random.choice([2,4,8])

    win = bet * mult
    user["balance"] += win

    stats["plays"] += 1
    if win > 0:
        stats["wins"] += 1

    set_user(uid, user)

    return {"mult": mult, "win": win, "balance": user["balance"]}

# ---------- BLACKJACK ----------
cards = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

def draw_card():
    return random.choice(cards)

def hand_value(hand):
    value = 0
    aces = 0

    for c in hand:
        if c in ["J","Q","K"]:
            value += 10
        elif c == "A":
            value += 11
            aces += 1
        else:
            value += int(c)

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

@app.route("/bj/start", methods=["POST"])
def bj_start():
    data = request.json
    uid = str(data["user_id"])
    bet = float(data["bet"])

    user = get_user(uid)

    if user["balance"] < bet:
        return {"error": "Нема балансу"}

    user["balance"] -= bet

    player = [draw_card(), draw_card()]
    dealer = [draw_card()]

    games[uid] = {"player": player, "dealer": dealer, "bet": bet}

    set_user(uid, user)

    return {"player": player, "dealer": dealer, "balance": user["balance"]}

@app.route("/bj/hit", methods=["POST"])
def bj_hit():
    uid = str(request.json["user_id"])
    game = games.get(uid)

    game["player"].append(draw_card())

    if hand_value(game["player"]) > 21:
        return {"result": "lose", "player": game["player"]}

    return {"player": game["player"]}

@app.route("/bj/stand", methods=["POST"])
def bj_stand():
    uid = str(request.json["user_id"])
    game = games.get(uid)

    dealer = game["dealer"]

    while hand_value(dealer) < 17:
        dealer.append(draw_card())

    player_val = hand_value(game["player"])
    dealer_val = hand_value(dealer)

    user = get_user(uid)

    if random.random() < SETTINGS["edge"]:
        result = "lose"
    elif dealer_val > 21 or player_val > dealer_val:
        user["balance"] += game["bet"] * 2
        result = "win"
    else:
        result = "lose"

    set_user(uid, user)

    return {"dealer": dealer, "result": result, "balance": user["balance"]}

# ---------- ADMIN ----------
@app.route("/admin/set_edge", methods=["POST"])
def set_edge():
    if request.json.get("key") != "admin123":
        return {"error": "no access"}
    SETTINGS["edge"] = float(request.json["edge"])
    return {"ok": True}

@app.route("/stats")
def get_stats():
    return stats

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)