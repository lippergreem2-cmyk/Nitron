import os


class ProjectGenerator:

    def __init__(self):
        self.output = "GeneratedProjects"

        os.makedirs(
            self.output,
            exist_ok=True
        )


    def create_project(self, name):

        project_path = os.path.join(
            self.output,
            name
        )

        os.makedirs(
            project_path,
            exist_ok=True
        )

        return project_path



    def create_file(self, path, filename, content):

        file_path = os.path.join(
            path,
            filename
        )

        with open(file_path, "w") as file:
            file.write(content)


        return file_path



    def website(self, name):

        project = self.create_project(name)


        self.create_file(
            project,
            "index.html",
            """
<!DOCTYPE html>
<html>
<head>
<title>Nitron Generated Website</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<h1>Created by Nitron AI</h1>
<p>This is a real generated website.</p>

<script src="app.js"></script>

</body>
</html>
"""
        )


        self.create_file(
            project,
            "style.css",
            """
body {
    background: black;
    color: white;
    text-align: center;
    font-family: Arial;
}
"""
        )


        self.create_file(
            project,
            "app.js",
            """
console.log("Nitron website running");
"""
        )


        return "Website created: " + project
