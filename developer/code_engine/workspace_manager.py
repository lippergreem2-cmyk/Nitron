from pathlib import Path
import os


class WorkspaceManager:

    def __init__(self):

        self.root = Path.home() / "Nitron" / "GeneratedProjects"
        self.root.mkdir(parents=True, exist_ok=True)

    def workspace(self):

        return self.root

    def project(self, name):

        path = self.root / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def vscode(self, project):

        os.system(f'code "{project}"')

    def android_studio(self, project):

        os.system(f'studio "{project}"')

    def list_projects(self):

        return sorted(
            p.name
            for p in self.root.iterdir()
            if p.is_dir()
        )
