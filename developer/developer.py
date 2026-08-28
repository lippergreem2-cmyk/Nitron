import os


class Developer:

    def say(self, text):
        return text

    def create_folder(self, name):
        os.makedirs(name, exist_ok=True)
        return f"Folder '{name}' created."

    def create_html(self, name):
        with open(f"{name}.html", "w") as f:
            f.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>Hello</h1>\n</body>\n</html>")
        return f"{name}.html created."

    def create_css(self, name):
        with open(f"{name}.css", "w") as f:
            f.write("body {\n    font-family: Arial;\n}")
        return f"{name}.css created."

    def create_js(self, name):
        with open(f"{name}.js", "w") as f:
            f.write('console.log("Nitron");')
        return f"{name}.js created."

    def create_python(self, name):
        with open(f"{name}.py", "w") as f:
            f.write('print("Hello from Nitron")')
        return f"{name}.py created."

    def create_json(self, name):
        with open(f"{name}.json", "w") as f:
            f.write("{}")
        return f"{name}.json created."

    def create_text(self, name):
        with open(f"{name}.txt", "w") as f:
            f.write("Created by Nitron")
        return f"{name}.txt created."

    def create_markdown(self, name):
        with open(f"{name}.md", "w") as f:
            f.write("# Nitron")
        return f"{name}.md created."

    def create_readme(self):
        with open("README.md", "w") as f:
            f.write("# Project")
        return "README.md created."
