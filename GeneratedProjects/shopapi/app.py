from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "name": "Nitron API",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "health": "ok"
    })


if __name__ == "__main__":
    app.run(debug=True)
