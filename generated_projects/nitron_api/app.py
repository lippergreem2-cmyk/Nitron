from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "name": "Nitron API",
        "status": "online"
    }

@app.route("/hello")
def hello():
    return {
        "message": "Hello from Nitron!"
    }

if __name__ == "__main__":
    app.run(debug=True)
