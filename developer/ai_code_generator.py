# ==========================================================
# NITRON AI CODE GENERATOR v1.0
# PART 2
# OLLAMA + QWEN PROJECT BUILDER
# ==========================================================

import json
import re
import subprocess
from pathlib import Path


# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

GENERATED_PROJECTS = (
    ROOT_DIR / "GeneratedProjects"
)

GENERATED_PROJECTS.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# OLLAMA CONFIGURATION
# ==========================================================

OLLAMA_COMMAND = "ollama"

DEFAULT_MODEL = "qwen2.5-coder:1.5b"


# ==========================================================
# AI CODE GENERATOR
# ==========================================================

class AICodeGenerator:

    def __init__(
        self,
        model=DEFAULT_MODEL
    ):

        self.model = model

        self.provider = "ollama"

        self.available = self.check_ollama()

    # ======================================================
    # CHECK OLLAMA
    # ======================================================

    def check_ollama(self):

        try:

            result = subprocess.run(
                [
                    OLLAMA_COMMAND,
                    "--version"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )

            return result.returncode == 0

        except Exception:

            return False

    # ======================================================
    # PROVIDER INFORMATION
    # ======================================================

    def provider_info(self):

        return {
            "provider": self.provider,
            "model": self.model,
            "available": self.available
        }

    # ======================================================
    # ASK OLLAMA
    # ======================================================

    def ask_ollama(self, prompt):

        if not self.available:

            return {
                "success": False,
                "error": "Ollama is not available."
            }

        try:

            result = subprocess.run(
                [
                    OLLAMA_COMMAND,
                    "run",
                    self.model,
                    prompt
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=600
            )

            if result.returncode != 0:

                return {
                    "success": False,
                    "error": (
                        result.stderr.strip()
                        or "Ollama returned an error."
                    )
                }

            return {
                "success": True,
                "output": result.stdout.strip()
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "error": "Ollama timed out."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # PROJECT NAME
    # ======================================================

    def safe_project_name(self, name):

        name = str(name).strip()

        result = []

        for char in name:

            if char.isalnum():

                result.append(char)

            elif char in (
                " ",
                "-",
                "_"
            ):

                result.append("_")

        name = "".join(result)

        name = re.sub(
            r"_+",
            "_",
            name
        )

        name = name.strip("_")

        if not name:

            name = "NitronProject"

        return name[:80]

    # ======================================================
    # BUILD SYSTEM PROMPT
    # ======================================================

    def build_prompt(self, request):

        return f"""
You are Nitron's autonomous software development AI.

The user wants you to build this project:

{request}

Your job is to design the project and return ALL required
source files.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do not use Markdown.
3. Do not use code fences.
4. The JSON must have this structure:

{{
    "project": "ProjectName",
    "description": "Short description",
    "files": {{
        "relative/path/file.ext": "complete file contents"
    }}
}}

5. Every file must contain complete usable code.
6. Do not create empty placeholder files unless absolutely
   necessary.
7. Use sensible folders.
8. Include README.md.
9. Include configuration files when needed.
10. Include frontend and backend files when the project
    requires both.
11. Include tests when appropriate.
12. Make the project runnable.
13. Do not explain anything outside the JSON.
14. Never include secrets, passwords or API keys.
15. Prefer simple technologies that can run locally.
16. Make reasonable decisions yourself instead of asking
    the user unnecessary questions.

The project must be generated from this request:

{request}
"""

    # ======================================================
    # EXTRACT JSON
    # ======================================================

    def extract_json(self, text):
        import json
        import re

        text = text.strip()

        # Remove ANSI terminal escape sequences
        text = re.sub(r"\\x1b\\[[0-9;?]*[ -/]*[@-~]", "", text)
        text = re.sub(r"\\x1b\\][^\\x07]*(?:\\x07|\\x1b\\\\)", "", text)

        # Remove markdown fences
        text = re.sub(r"^\\s*```(?:json)?\\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\\s*```\\s*$", "", text)
        text = text.strip()

        # Normal JSON
        try:
            return json.loads(text)
        except Exception:
            pass

        # Convert triple-quoted file values into JSON strings
        pattern = r'("files"\\s*:\\s*\\{.*?)(\\}\s*\\})'

        def fix_triple_quotes(match):
            block = match.group(1)
            block = re.sub(
                r'(""")\\s*(.*?)\\s*(""")',
                lambda m: json.dumps(m.group(2)),
                block,
                flags=re.DOTALL
            )
            return block + match.group(2)

        text = re.sub(
            r'(""")\\s*(.*?)\\s*(""")',
            lambda m: json.dumps(m.group(2)),
            text,
            flags=re.DOTALL
        )

        # Try again
        try:
            return json.loads(text)
        except Exception:
            pass

        # Extract outer JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            candidate = text[start:end + 1]

            try:
                return json.loads(candidate)
            except Exception:
                pass

        return None

    # ======================================================
    # VALIDATE PROJECT
    # ======================================================

    def validate_project(self, data):

        if not isinstance(
            data,
            dict
        ):

            return False

        if "files" not in data:

            return False

        if not isinstance(
            data["files"],
            dict
        ):

            return False

        return True

    # ======================================================
    # SAFE FILE PATH
    # ======================================================

    def safe_file_path(
        self,
        project_dir,
        relative_path
    ):

        relative_path = str(
            relative_path
        ).replace("\\", "/")

        # Prevent absolute paths

        if relative_path.startswith("/"):

            return None

        # Prevent dangerous traversal

        parts = Path(
            relative_path
        ).parts

        if ".." in parts:

            return None

        path = (
            project_dir /
            relative_path
        ).resolve()

        project_dir = (
            project_dir.resolve()
        )

        try:

            path.relative_to(
                project_dir
            )

        except ValueError:

            return None

        return path

    # ======================================================
    # WRITE PROJECT
    # ======================================================

    def write_project(
        self,
        project_name,
        files
    ):

        project_name = (
            self.safe_project_name(
                project_name
            )
        )

        project_dir = (
            GENERATED_PROJECTS /
            project_name
        )

        project_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        written_files = []

        for filename, content in files.items():

            path = self.safe_file_path(
                project_dir,
                filename
            )

            if path is None:

                continue

            if not isinstance(
                content,
                str
            ):

                content = str(content)

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            path.write_text(
                content,
                encoding="utf-8"
            )

            written_files.append(
                str(
                    path.relative_to(
                        project_dir
                    )
                )
            )

        return (
            project_dir,
            written_files
        )

    # ======================================================
    # GENERATE PROJECT
    # ======================================================

    def generate(self, request):

        request = str(
            request
        ).strip()

        if not request:

            return {
                "success": False,
                "error": "No project request."
            }

        # ----------------------------------------------
        # Check Ollama
        # ----------------------------------------------

        if not self.available:

            return {
                "success": False,
                "error": (
                    "Ollama is unavailable. "
                    "Make sure Ollama is installed "
                    "and the model exists."
                )
            }

        # ----------------------------------------------
        # Create prompt
        # ----------------------------------------------

        prompt = self.build_prompt(
            request
        )

        # ----------------------------------------------
        # Ask AI
        # ----------------------------------------------

        response = self.ask_ollama(
            prompt
        )

        if not response.get(
            "success"
        ):

            return response

        output = response.get(
            "output",
            ""
        )

        # ----------------------------------------------
        # Parse JSON
        # ----------------------------------------------

        data = self.extract_json(
            output
        )

        if data is None:

            return {
                "success": False,
                "error": (
                    "Ollama returned invalid "
                    "project JSON."
                ),
                "raw": output[:4000]
            }

        # ----------------------------------------------
        # Validate
        # ----------------------------------------------

        if not self.validate_project(
            data
        ):

            return {
                "success": False,
                "error": (
                    "AI returned an invalid "
                    "project structure."
                )
            }

        # ----------------------------------------------
        # Project name
        # ----------------------------------------------

        project_name = data.get(
            "project",
            "NitronProject"
        )

        # ----------------------------------------------
        # Write files
        # ----------------------------------------------

        project_dir, written_files = (
            self.write_project(
                project_name,
                data["files"]
            )
        )

        # ----------------------------------------------
        # Result
        # ----------------------------------------------

        return {

            "success": True,

            "project": project_name,

            "path": str(
                project_dir
            ),

            "provider": self.provider,

            "model": self.model,

            "description": data.get(
                "description",
                ""
            ),

            "files": written_files

        }


# ==========================================================
# SIMPLE FUNCTION
# ==========================================================

def generate_project(
    request,
    model=DEFAULT_MODEL
):

    generator = AICodeGenerator(
        model=model
    )

    return generator.generate(
        request
    )


# ==========================================================
# TEST
# ==========================================================

def test_generator():

    print("=" * 60)
    print("NITRON AI CODE GENERATOR TEST")
    print("=" * 60)

    generator = AICodeGenerator()

    print()

    print(
        "Provider:",
        generator.provider
    )

    print(
        "Model:",
        generator.model
    )

    print(
        "Ollama:",
        "ONLINE"
        if generator.available
        else "OFFLINE"
    )

    print()

    if not generator.available:

        print(
            "Ollama is not available."
        )

        return

    print(
        "Testing Ollama..."
    )

    result = generator.ask_ollama(
        "Reply with exactly: NITRON ONLINE"
    )

    if result.get("success"):

        print(
            "Ollama response:"
        )

        print(
            result["output"]
        )

    else:

        print(
            "Error:",
            result.get("error")
        )


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    test_generator()
