from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

RASA_API = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_message = request.json["message"]

    response = requests.post(
        RASA_API,
        json={"sender": "user", "message": user_message}
    )

    bot_messages = response.json()

    if bot_messages:
        return jsonify(bot_messages[0]["text"])
    else:
        return jsonify("Sorry, I didn't understand that.")

if __name__ == "__main__":
    app.run(port=8000)