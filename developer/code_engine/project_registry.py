import json
from pathlib import Path
from datetime import datetime


class ProjectRegistry:

    def __init__(self):

        self.database = (
            Path.home()
            / "Nitron"
            / "GeneratedProjects"
            / "projects.json"
        )

        self.database.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.database.exists():

            with open(self.database, "w") as f:

                json.dump([], f)

    def load(self):

        with open(self.database, "r") as f:

            return json.load(f)

    def save(self, data):

        with open(self.database, "w") as f:

            json.dump(data, f, indent=4)

    def add(self, name, project_type):

        data = self.load()

        data.append({

            "name": name,

            "type": project_type,

            "created": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })

        self.save(data)

    def list_projects(self):

        return self.load()
