import os


class BackendGenerator:

    def __init__(self):
        self.output = "GeneratedProjects"
        os.makedirs(self.output, exist_ok=True)


    def create_api(self, name):

        project = os.path.join(
            self.output,
            name
        )

        os.makedirs(project, exist_ok=True)


        files = {

"server.py":
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Nitron generated API running"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
""",


"requirements.txt":
"""
flask
"""
        }


        for filename, content in files.items():

            with open(
                os.path.join(project, filename),
                "w"
            ) as f:
                f.write(content)


        return f"Backend API created: {project}"
