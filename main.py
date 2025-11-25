from flask import Flask, request
import requests
from handlers import handle_message, send_message
from config import PORT, BOT_TOKEN

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot de rentabilité actif - Version PRO"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        message = data["message"]

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        handle_message(chat_id, text)

    return {"status": "ok"}


if __name__ == "__main__":
    print(f"Bot lancé sur le port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
