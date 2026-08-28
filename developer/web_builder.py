# ==========================================================
# NITRON WEB BUILDER v2.0
# Creates complete web project structure
# ==========================================================

from pathlib import Path
import re


class WebBuilder:

    def __init__(self, root=None):

        if root is None:
            root = (
                Path(__file__).resolve().parent.parent
                / "GeneratedProjects"
                / "Websites"
            )

        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # NAME
    # ======================================================

    def clean_name(self, name):

        name = str(name).strip()

        name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            name
        )

        if not name:
            name = "NitronWebsite"

        return name

    # ======================================================
    # DIRECTORIES
    # ======================================================

    def create_directories(self, project):

        directories = [
            "frontend",
            "frontend/css",
            "frontend/js",
            "frontend/assets",
            "frontend/components",
            "frontend/pages",

            "backend",
            "backend/routes",
            "backend/models",
            "backend/services",
            "backend/config",
            "backend/middleware",

            "database",
            "database/migrations",

            "tests",
            "tests/frontend",
            "tests/backend",

            "docs"
        ]

        for directory in directories:

            (project / directory).mkdir(
                parents=True,
                exist_ok=True
            )

    # ======================================================
    # FILE WRITER
    # ======================================================

    def write_file(
        self,
        project,
        relative_path,
        content
    ):

        path = project / relative_path

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            content,
            encoding="utf-8"
        )

        return relative_path

    # ======================================================
    # CREATE PROJECT
    # ======================================================

    def create(self, name):

        name = self.clean_name(name)

        project = self.root / name

        self.create_directories(project)

        files = []

        # ==================================================
        # INDEX HTML
        # ==================================================

        content = (
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "    <meta charset=\"UTF-8\">\n"
            "    <meta name=\"viewport\" "
            "content=\"width=device-width, initial-scale=1.0\">\n"
            f"    <title>{name}</title>\n"
            "    <link rel=\"stylesheet\" "
            "href=\"css/style.css\">\n"
            "</head>\n"
            "<body>\n"
            "    <header>\n"
            f"        <h1>{name}</h1>\n"
            "        <nav>\n"
            "            <a href=\"index.html\">Home</a>\n"
            "        </nav>\n"
            "    </header>\n"
            "\n"
            "    <main>\n"
            f"        <h2>Welcome to {name}</h2>\n"
            "        <p>This website was created by Nitron.</p>\n"
            "    </main>\n"
            "\n"
            "    <footer>\n"
            "        <p>Powered by Nitron</p>\n"
            "    </footer>\n"
            "\n"
            "    <script src=\"js/app.js\"></script>\n"
            "</body>\n"
            "</html>\n"
        )

        files.append(
            self.write_file(
                project,
                "frontend/index.html",
                content
            )
        )

        # ==================================================
        # CSS
        # ==================================================

        content = (
            "* {\n"
            "    box-sizing: border-box;\n"
            "}\n"
            "\n"
            "body {\n"
            "    margin: 0;\n"
            "    font-family: Arial, sans-serif;\n"
            "    background: #f5f5f5;\n"
            "    color: #222;\n"
            "}\n"
            "\n"
            "header {\n"
            "    padding: 20px;\n"
            "    background: white;\n"
            "}\n"
            "\n"
            "nav a {\n"
            "    text-decoration: none;\n"
            "}\n"
            "\n"
            "main {\n"
            "    min-height: 70vh;\n"
            "    padding: 40px;\n"
            "    max-width: 1000px;\n"
            "    margin: auto;\n"
            "}\n"
            "\n"
            "footer {\n"
            "    padding: 20px;\n"
            "    text-align: center;\n"
            "    background: white;\n"
            "}\n"
        )

        files.append(
            self.write_file(
                project,
                "frontend/css/style.css",
                content
            )
        )

        # ==================================================
        # JAVASCRIPT
        # ==================================================

        content = (
            "document.addEventListener("
            "\"DOMContentLoaded\", function () {\n"
            "\n"
            "    console.log("
            "\"Nitron web application started.\"\n"
            "    );\n"
            "\n"
            "});\n"
        )

        files.append(
            self.write_file(
                project,
                "frontend/js/app.js",
                content
            )
        )

        # ==================================================
        # BACKEND
        # ==================================================

        content = (
            "# ==================================================\n"
            f"# {name} BACKEND\n"
            "# Generated by Nitron\n"
            "# ==================================================\n"
            "\n"
            "from http.server import "
            "BaseHTTPRequestHandler, HTTPServer\n"
            "import json\n"
            "\n"
            "\n"
            "class Handler(BaseHTTPRequestHandler):\n"
            "\n"
            "    def send_json(self, status, data):\n"
            "\n"
            "        body = json.dumps(data).encode(\"utf-8\")\n"
            "\n"
            "        self.send_response(status)\n"
            "        self.send_header("
            "\"Content-Type\", \"application/json\")\n"
            "        self.send_header("
            "\"Content-Length\", str(len(body)))\n"
            "        self.end_headers()\n"
            "\n"
            "        self.wfile.write(body)\n"
            "\n"
            "\n"
            "    def do_GET(self):\n"
            "\n"
            "        if self.path == \"/api/health\":\n"
            "\n"
            "            self.send_json(\n"
            "                200,\n"
            "                {\n"
            "                    \"status\": \"ok\",\n"
            f"                    \"project\": \"{name}\"\n"
            "                }\n"
            "            )\n"
            "\n"
            "            return\n"
            "\n"
            "        self.send_json(\n"
            "            404,\n"
            "            {\"error\": \"Not found\"}\n"
            "        )\n"
            "\n"
            "\n"
            "def main():\n"
            "\n"
            "    server = HTTPServer(\n"
            "        (\"127.0.0.1\", 8000),\n"
            "        Handler\n"
            "    )\n"
            "\n"
            f"    print(\"{name} backend running "
            "on http://127.0.0.1:8000\")\n"
            "\n"
            "    try:\n"
            "        server.serve_forever()\n"
            "    except KeyboardInterrupt:\n"
            "        print(\"Server stopped.\")\n"
            "    finally:\n"
            "        server.server_close()\n"
            "\n"
            "\n"
            "if __name__ == \"__main__\":\n"
            "    main()\n"
        )

        files.append(
            self.write_file(
                project,
                "backend/app.py",
                content
            )
        )

        # ==================================================
        # BACKEND PACKAGE FILES
        # ==================================================

        for path in [
            "backend/routes/__init__.py",
            "backend/models/__init__.py",
            "backend/services/__init__.py",
            "backend/config/__init__.py",
            "backend/middleware/__init__.py"
        ]:

            files.append(
                self.write_file(
                    project,
                    path,
                    "# Nitron module\n"
                )
            )

        # ==================================================
        # DATABASE
        # ==================================================

        content = (
            "-- Nitron database schema\n"
            "\n"
            "CREATE TABLE IF NOT EXISTS users (\n"
            "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
            "    name TEXT NOT NULL,\n"
            "    email TEXT UNIQUE NOT NULL,\n"
            "    created_at TIMESTAMP "
            "DEFAULT CURRENT_TIMESTAMP\n"
            ");\n"
        )

        files.append(
            self.write_file(
                project,
                "database/schema.sql",
                content
            )
        )

        files.append(
            self.write_file(
                project,
                "database/migrations/README.md",
                "# Database Migrations\n\n"
                "Put database migration files here.\n"
            )
        )

        # ==================================================
        # TESTS
        # ==================================================

        files.append(
            self.write_file(
                project,
                "tests/backend/test_backend.py",
                "def test_backend():\n"
                "    assert True\n"
            )
        )

        files.append(
            self.write_file(
                project,
                "tests/frontend/test_frontend.py",
                "def test_frontend():\n"
                "    assert True\n"
            )
        )

        # ==================================================
        # README
        # ==================================================

        content = (
            f"# {name}\n"
            "\n"
            "Full-stack web project generated by Nitron.\n"
            "\n"
            "## Structure\n"
            "\n"
            "- frontend/\n"
            "- backend/\n"
            "- database/\n"
            "- tests/\n"
            "- docs/\n"
            "\n"
            "## Start Backend\n"
            "\n"
            "```bash\n"
            "cd backend\n"
            "python app.py\n"
            "```\n"
            "\n"
            "## API\n"
            "\n"
            "GET /api/health\n"
        )

        files.append(
            self.write_file(
                project,
                "README.md",
                content
            )
        )

        # ==================================================
        # DOCUMENTATION
        # ==================================================

        files.append(
            self.write_file(
                project,
                "docs/architecture.md",
                f"# {name} Architecture\n\n"
                "The project contains frontend, backend, "
                "database, tests and documentation.\n"
            )
        )

        files.append(
            self.write_file(
                project,
                "docs/api.md",
                "# API Documentation\n\n"
                "## GET /api/health\n\n"
                "Returns backend health information.\n"
            )
        )

        return {
            "success": True,
            "project": name,
            "type": "web",
            "path": str(project),
            "files": files
        }


# ==========================================================
# PUBLIC FUNCTION
# ==========================================================

def build_web(name):

    builder = WebBuilder()

    return builder.create(name)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    result = build_web("TestWebsite")

    print("=" * 60)
    print("NITRON WEB BUILDER TEST")
    print("=" * 60)
    print()

    print("Project:", result["project"])
    print("Location:", result["path"])
    print()
    print("Created files:")

    for filename in result["files"]:
        print(" -", filename)

    print()
    print("Web project created successfully.")
