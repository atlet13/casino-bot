import os
import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__, static_folder="web")

BOT_TOKEN = "8659665258:AAFyL7OZBZqkU-D7iaE2auHyf73KdYyeeIM"
WEBAPP_URL = "https://casino-bot-1-p7mp.onrender.com"

# ===== ГОЛОВНА СТОРІНКА =====
@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("web", path)

# ===== TELEGRAM WEBHOOK =====
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]

        send_keyboard(chat_id)

    return "ok"

# ===== ВІДПРАВКА КНОПКИ =====
def send_keyboard(chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    keyboard = {
        "keyboard": [
            [{
                "text": "🎰 Відкрити казино",
                "web_app": {"url": WEBAPP_URL}
            }]
        ],
        "resize_keyboard": True
    }

    requests.post(url, json={
        "chat_id": chat_id,
        "text": "🎰 Натисни кнопку",
        "reply_markup": keyboard
    })

# ===== ЗАПУСК =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)