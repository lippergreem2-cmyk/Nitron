import os


class TemplateManager:

    def __init__(self):

        self.template_dir = "templates"

        os.makedirs(self.template_dir, exist_ok=True)


    def save_template(self, name, text):

        filename = os.path.join(

            self.template_dir,

            f"{name}.txt"

        )

        with open(filename, "w", encoding="utf-8") as f:

            f.write(text)

        return f"{name} template saved."


    def load_template(self, name):

        filename = os.path.join(

            self.template_dir,

            f"{name}.txt"

        )

        if not os.path.exists(filename):

            return None

        with open(filename, "r", encoding="utf-8") as f:

            return f.read()


    def list_templates(self):

        templates = []

        for file in os.listdir(self.template_dir):

            if file.endswith(".txt"):

                templates.append(file[:-4])

        templates.sort()

        return templates


    def delete_template(self, name):

        filename = os.path.join(

            self.template_dir,

            f"{name}.txt"

        )

        if os.path.exists(filename):

            os.remove(filename)

            return "Template deleted."

        return "Template not found."


    def template_exists(self, name):

        filename = os.path.join(

            self.template_dir,

            f"{name}.txt"

        )

        return os.path.exists(filename)


    def export_template(self, name, output):

        data = self.load_template(name)

        if data is None:

            return "Template not found."

        with open(output, "w", encoding="utf-8") as f:

            f.write(data)

        return "Template exported."


    def import_template(self, filename):

        if not os.path.exists(filename):

            return "File not found."

        name = os.path.basename(filename)

        destination = os.path.join(

            self.template_dir,

            name

        )

        with open(filename, "r", encoding="utf-8") as src:

            data = src.read()

        with open(destination, "w", encoding="utf-8") as dst:

            dst.write(data)

        return "Template imported."


if __name__ == "__main__":

    manager = TemplateManager()

    print(manager.list_templates())
