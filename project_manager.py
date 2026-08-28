from pathlib import Path
from datetime import datetime


class ProjectManager:

    def __init__(self):

        self.workspace = Path.home() / "Nitron" / "GeneratedProjects"
        self.workspace.mkdir(parents=True, exist_ok=True)

    def create_project(self, name):

        project = self.workspace / name

        project.mkdir(parents=True, exist_ok=True)

        return project

    def create_folder(self, project, folder):

        path = project / folder

        path.mkdir(parents=True, exist_ok=True)

        return path

    def write(self, project, filename, content):

        file = project / filename

        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "w", encoding="utf-8") as f:

            f.write(content)

        return file

    def read(self, project, filename):

        file = project / filename

        if not file.exists():
            return None

        with open(file, "r", encoding="utf-8") as f:

            return f.read()

    def exists(self, name):

        return (self.workspace / name).exists()

    def info(self, name):

        project = self.workspace / name

        if not project.exists():

            return None

        return {
            "name": name,
            "location": str(project),
            "created": datetime.fromtimestamp(
                project.stat().st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S")
        }
