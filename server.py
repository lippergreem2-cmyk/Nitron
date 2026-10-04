from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import ai_brain
from commands import execute

conversation_histories = {}
MAX_HISTORY_MESSAGES = 10  # last 5 exchanges


def flatten_reply(reply):
    """Convert a dict-shaped reply (e.g. a lesson object) into clean text."""
    if isinstance(reply, str):
        return reply

    if isinstance(reply, dict):
        parts = []

        if "message" in reply:
            parts.append(str(reply["message"]))

        lesson = reply.get("lesson")
        if isinstance(lesson, dict):
            if lesson.get("title"):
                parts.append("**" + lesson.get("title", "") + "**")
            if lesson.get("explanation"):
                parts.append(lesson["explanation"])
            if lesson.get("code"):
                parts.append("```python\n" + lesson.get("code", "") + "\n```")
            if lesson.get("output"):
                parts.append("Output: " + lesson.get("output", ""))
            if lesson.get("practice"):
                parts.append("Practice: " + lesson.get("practice", ""))
            if lesson.get("quiz"):
                parts.append("Quiz: " + lesson.get("quiz", ""))

        if parts:
            return "\n\n".join(parts)

        return str(reply)

    return str(reply)


app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        reply = ai_brain.chat(message, history=[])
        return jsonify({"reply": reply})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    user_id = data.get("user_id")

    if not message:
        return jsonify({"response": "I didn't catch a message."}), 400

    key = user_id if user_id else "default"
    history = conversation_histories.get(key, [])

    try:
        reply = execute(message)
        if reply is None:
            reply = ai_brain.chat(message, history=history)

        reply = flatten_reply(reply)

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        conversation_histories[key] = history[-MAX_HISTORY_MESSAGES:]

        result = {"response": reply}
        if user_id:
            result["user_id"] = user_id
        return jsonify(result)

    except Exception as error:
        return jsonify({"response": f"Error: {error}"}), 500


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Nitron server is online"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
