from pathlib import Path


class TemplateManager:

    def __init__(self):

        self.root = (
            Path.home()
            / "Nitron"
            / "developer"
            / "templates"
        )

    def template(self, category, filename):

        file = self.root / category / filename

        if not file.exists():
            return None

        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    def save(self, category, filename, content):

        folder = self.root / category
        folder.mkdir(parents=True, exist_ok=True)

        file = folder / filename

        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    def categories(self):

        return [
            p.name
            for p in self.root.iterdir()
            if p.is_dir()
        ]
