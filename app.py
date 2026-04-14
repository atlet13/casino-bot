import random
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="web", static_url_path="")

balance = 100
house_edge = 0.6  # 0.0 - чесно, 1.0 - жорсткий обман

# ====== ГОЛОВНА СТОРІНКА ======
@app.route("/")
def index():
    return send_from_directory("web", "index.html")


# ====== PLINKO ======
@app.route("/plinko", methods=["POST"])
def plinko():
    global balance

    data = request.json
    bet = float(data["bet"])

    if bet > balance:
        return jsonify({"error": "Not enough money"})

    balance -= bet

    # шанс виграшу залежить від house_edge
    if random.random() > house_edge:
        win = bet * random.choice([2, 5, 10, 20])
    else:
        win = 0

    balance += win

    return jsonify({
        "win": win,
        "balance": balance
    })


# ====== BLACKJACK ======
def draw_card():
    return random.choice([2,3,4,5,6,7,8,9,10,10,10,11])

@app.route("/blackjack/start", methods=["POST"])
def blackjack_start():
    global balance

    data = request.json
    bet = float(data["bet"])

    if bet > balance:
        return jsonify({"error": "No money"})

    balance -= bet

    player = [draw_card(), draw_card()]
    dealer = [draw_card(), draw_card()]

    return jsonify({
        "player": player,
        "dealer": [dealer[0], "?"],
        "bet": bet
    })


@app.route("/blackjack/hit", methods=["POST"])
def blackjack_hit():
    data = request.json
    player = data["player"]

    player.append(draw_card())

    return jsonify({"player": player})


@app.route("/blackjack/stand", methods=["POST"])
def blackjack_stand():
    global balance

    data = request.json
    player = data["player"]
    dealer = data["dealer"]
    bet = data["bet"]

    while sum(dealer) < 17:
        dealer.append(draw_card())

    player_sum = sum(player)
    dealer_sum = sum(dealer)

    win = 0

    if player_sum > 21:
        win = 0
    elif dealer_sum > 21 or player_sum > dealer_sum:
        win = bet * 2
    elif player_sum == dealer_sum:
        win = bet
    else:
        win = 0

    balance += win

    return jsonify({
        "dealer": dealer,
        "win": win,
        "balance": balance
    })


# ====== АДМІН ======
@app.route("/set-edge", methods=["POST"])
def set_edge():
    global house_edge

    data = request.json
    house_edge = float(data["edge"])

    return jsonify({"status": "ok", "edge": house_edge})


# ====== ЗАПУСК ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)