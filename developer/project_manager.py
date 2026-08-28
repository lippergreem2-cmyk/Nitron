# ==========================================================
# NITRON PROJECT MANAGER v2.0
# PART 3
# CREATE + INSPECT + RUN + TEST + CHECK + MANAGE
# ==========================================================

import shutil
import subprocess
from pathlib import Path


# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT_DIR / "GeneratedProjects"

PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# PROJECT MANAGER
# ==========================================================

class ProjectManager:

    def __init__(self, root=None):
        self.root = Path(
            root or PROJECTS_DIR
        ).resolve()

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # SAFE PROJECT NAME
    # ======================================================

    def safe_name(self, name):

        name = str(name).strip()

        if not name:
            return "NitronProject"

        result = []

        for char in name:

            if char.isalnum():
                result.append(char)

            elif char in (" ", "-", "_"):
                result.append("_")

        cleaned = "".join(result)

        while "__" in cleaned:
            cleaned = cleaned.replace(
                "__",
                "_"
            )

        cleaned = cleaned.strip("_")

        return cleaned or "NitronProject"

    # ======================================================
    # PROJECT PATH
    # ======================================================

    def project_path(self, name):

        safe = self.safe_name(name)

        path = (
            self.root / safe
        ).resolve()

        try:

            path.relative_to(
                self.root
            )

        except ValueError:

            return None

        return path

    # ======================================================
    # FIND EXISTING PROJECT
    # ======================================================

    def find_existing_project(self, name):

        requested = str(name).strip()

        if not requested:
            return None

        # Exact match first
        exact = self.root / requested

        if exact.is_dir():
            return exact

        # Safe-name match
        safe = self.safe_name(requested)

        safe_path = self.root / safe

        if safe_path.is_dir():
            return safe_path

        # Case-insensitive match
        requested_lower = requested.lower()

        for item in self.root.iterdir():

            if (
                item.is_dir()
                and item.name.lower()
                == requested_lower
            ):
                return item

        return None

    # ======================================================
    # LIST PROJECTS
    # ======================================================

    def list_projects(self):

        if not self.root.exists():
            return []

        return sorted(
            item.name
            for item in self.root.iterdir()
            if item.is_dir()
        )

    # ======================================================
    # PROJECT EXISTS
    # ======================================================

    def exists(self, name):

        return (
            self.find_existing_project(name)
            is not None
        )

    # ======================================================
    # CREATE PROJECT
    # ======================================================

    def create_project(
        self,
        name,
        folders=None
    ):

        safe = self.safe_name(name)

        path = self.project_path(safe)

        if path is None:
            return {
                "success": False,
                "error": "Invalid project name."
            }

        if path.exists():

            return {
                "success": False,
                "error": (
                    f"Project '{path.name}' "
                    "already exists."
                )
            }

        try:

            path.mkdir(
                parents=True,
                exist_ok=False
            )

            default_folders = [
                "src",
                "tests",
                "docs"
            ]

            folders = (
                folders
                if folders is not None
                else default_folders
            )

            for folder in folders:

                (
                    path / str(folder)
                ).mkdir(
                    parents=True,
                    exist_ok=True
                )

            readme = path / "README.md"

            readme.write_text(
                f"# {safe}\n\n"
                "Created by Nitron Project Manager.\n",
                encoding="utf-8"
            )

            return {
                "success": True,
                "project": safe,
                "path": str(path)
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # INSPECT PROJECT
    # ======================================================

    def inspect(self, name):

        path = self.find_existing_project(name)

        if path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{name}' "
                    "was not found."
                )
            }

        files = []

        for item in path.rglob("*"):

            if item.is_file():

                try:

                    files.append(
                        str(
                            item.relative_to(path)
                        )
                    )

                except Exception:
                    pass

        return {
            "success": True,
            "project": path.name,
            "path": str(path),
            "files": sorted(files),
            "file_count": len(files)
        }

    # ======================================================
    # PROJECT STATUS
    # ======================================================

    def status(self, name):

        info = self.inspect(name)

        if not info.get("success"):
            return info

        path = Path(info["path"])

        directories = []

        for item in path.rglob("*"):

            if item.is_dir():

                try:

                    directories.append(
                        str(
                            item.relative_to(path)
                        )
                    )

                except Exception:
                    pass

        return {
            "success": True,
            "project": info["project"],
            "path": info["path"],
            "files": info["file_count"],
            "directories": len(directories),

            "has_readme": (
                path / "README.md"
            ).is_file(),

            "has_backend": (
                path / "backend"
            ).is_dir(),

            "has_frontend": (
                path / "frontend"
            ).is_dir(),

            "has_tests": (
                path / "tests"
            ).is_dir(),

            "has_database": (
                path / "database"
            ).is_dir(),

            "has_src": (
                path / "src"
            ).is_dir()
        }

    # ======================================================
    # FIND FILE
    # ======================================================

    def find_file(
        self,
        project,
        filename
    ):

        project_path = self.find_existing_project(
            project
        )

        if project_path is None:
            return None

        filename = str(filename).strip()

        if not filename:
            return None

        # Direct path first
        direct = (
            project_path / filename
        ).resolve()

        try:

            direct.relative_to(
                project_path
            )

        except ValueError:

            return None

        if direct.is_file():
            return direct

        # Search recursively
        for item in project_path.rglob(
            Path(filename).name
        ):

            if item.is_file():

                return item

        return None

    # ======================================================
    # READ FILE
    # ======================================================

    def read_file(
        self,
        project,
        filename
    ):

        path = self.find_file(
            project,
            filename
        )

        if path is None:

            return {
                "success": False,
                "error": (
                    f"File '{filename}' "
                    "was not found."
                )
            }

        try:

            project_path = self.find_existing_project(
                project
            )

            return {
                "success": True,
                "project": project_path.name,
                "file": str(
                    path.relative_to(
                        project_path
                    )
                ),
                "content": path.read_text(
                    encoding="utf-8"
                )
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # WRITE FILE
    # ======================================================

    def write_file(
        self,
        project,
        filename,
        content
    ):

        project_path = self.find_existing_project(
            project
        )

        if project_path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{project}' "
                    "was not found."
                )
            }

        target = (
            project_path / str(filename)
        ).resolve()

        try:

            target.relative_to(
                project_path
            )

        except ValueError:

            return {
                "success": False,
                "error": "Invalid file path."
            }

        try:

            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            target.write_text(
                str(content),
                encoding="utf-8"
            )

            return {
                "success": True,
                "project": project_path.name,
                "file": str(
                    target.relative_to(
                        project_path
                    )
                ),
                "path": str(target)
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # DELETE PROJECT
    # ======================================================

    def delete_project(self, name):

        path = self.find_existing_project(name)

        if path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{name}' "
                    "was not found."
                )
            }

        try:

            shutil.rmtree(path)

            return {
                "success": True,
                "project": name,
                "message": "Project deleted."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # RUN PYTHON
    # ======================================================

    def run_python(
        self,
        project,
        filename="main.py",
        timeout=60
    ):

        project_path = self.find_existing_project(
            project
        )

        if project_path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{project}' "
                    "was not found."
                )
            }

        target = (
            project_path / filename
        ).resolve()

        try:

            target.relative_to(
                project_path
            )

        except ValueError:

            return {
                "success": False,
                "error": "Invalid file path."
            }

        if not target.is_file():

            return {
                "success": False,
                "error": (
                    f"{filename} "
                    "does not exist."
                )
            }

        try:

            result = subprocess.run(

                [
                    "python",
                    str(target)
                ],

                cwd=str(project_path),

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                text=True,

                timeout=timeout

            )

            return {
                "success": (
                    result.returncode == 0
                ),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "project": project_path.name,
                "file": filename
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "error": "Program timed out."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # TEST PYTHON PROJECT
    # ======================================================

    def test_python(
        self,
        project,
        timeout=120
    ):

        project_path = self.find_existing_project(
            project
        )

        if project_path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{project}' "
                    "was not found."
                )
            }

        tests_dir = project_path / "tests"

        if not tests_dir.is_dir():

            return {
                "success": False,
                "error": (
                    "No tests directory "
                    "was found."
                )
            }

        try:

            result = subprocess.run(

                [
                    "python",
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tests"
                ],

                cwd=str(project_path),

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                text=True,

                timeout=timeout

            )

            return {
                "success": (
                    result.returncode == 0
                ),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "error": "Tests timed out."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # CHECK PYTHON SYNTAX
    # ======================================================

    def check_python(self, project):

        project_path = self.find_existing_project(
            project
        )

        if project_path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{project}' "
                    "was not found."
                )
            }

        python_files = list(
            project_path.rglob("*.py")
        )

        errors = []
        checked = 0

        for file in python_files:

            try:

                result = subprocess.run(

                    [
                        "python",
                        "-m",
                        "py_compile",
                        str(file)
                    ],

                    stdout=subprocess.PIPE,

                    stderr=subprocess.PIPE,

                    text=True

                )

                checked += 1

                if result.returncode != 0:

                    errors.append({
                        "file": str(
                            file.relative_to(
                                project_path
                            )
                        ),
                        "error": (
                            result.stderr
                            or "Syntax error."
                        )
                    })

            except Exception as error:

                errors.append({
                    "file": str(
                        file.relative_to(
                            project_path
                        )
                    ),
                    "error": str(error)
                })

        return {
            "success": len(errors) == 0,
            "checked": checked,
            "errors": errors
        }

    # ======================================================
    # RUN COMMAND
    # ======================================================

    def run_command(
        self,
        project,
        command,
        timeout=60
    ):

        project_path = self.find_existing_project(
            project
        )

        if project_path is None:

            return {
                "success": False,
                "error": (
                    f"Project '{project}' "
                    "was not found."
                )
            }

        if isinstance(command, str):

            command = command.split()

        if not command:

            return {
                "success": False,
                "error": "No command supplied."
            }

        try:

            result = subprocess.run(

                command,

                cwd=str(project_path),

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                text=True,

                timeout=timeout

            )

            return {
                "success": (
                    result.returncode == 0
                ),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "error": "Command timed out."
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }

    # ======================================================
    # HANDLE NATURAL COMMANDS
    # ======================================================

    def handle(self, command):

        text = str(command).strip()
        lower = text.lower()

        # --------------------------------------------------
        # LIST
        # --------------------------------------------------

        if lower in (
            "list projects",
            "show projects",
            "my projects",
            "show my projects"
        ):

            projects = self.list_projects()

            if not projects:

                return (
                    "You don't have any "
                    "generated projects yet."
                )

            return (
                "Nitron projects:\n\n"
                + "\n".join(
                    f"- {project}"
                    for project in projects
                )
            )

        # --------------------------------------------------
        # CREATE
        # --------------------------------------------------

        for prefix in (
            "create project ",
            "new project "
        ):

            if lower.startswith(prefix):

                name = text[
                    len(prefix):
                ].strip()

                if not name:

                    return (
                        "What should I name "
                        "the project?"
                    )

                result = self.create_project(
                    name
                )

                if not result["success"]:

                    return result["error"]

                return (
                    f"Project "
                    f"'{result['project']}' "
                    "created successfully."
                )

        # --------------------------------------------------
        # INSPECT / STATUS
        # --------------------------------------------------

        for prefix in (
            "inspect project ",
            "show project ",
            "project status "
        ):

            if lower.startswith(prefix):

                name = text[
                    len(prefix):
                ].strip()

                info = self.status(name)

                if not info["success"]:
                    return info["error"]

                return (
                    f"Project: "
                    f"{info['project']}\n"
                    f"Location: "
                    f"{info['path']}\n"
                    f"Files: "
                    f"{info['files']}\n"
                    f"Directories: "
                    f"{info['directories']}\n"
                    f"README: "
                    f"{info['has_readme']}\n"
                    f"Frontend: "
                    f"{info['has_frontend']}\n"
                    f"Backend: "
                    f"{info['has_backend']}\n"
                    f"Tests: "
                    f"{info['has_tests']}\n"
                    f"Database: "
                    f"{info['has_database']}\n"
                    f"Source: "
                    f"{info['has_src']}"
                )

        # --------------------------------------------------
        # CHECK
        # --------------------------------------------------

        prefix = "check project "

        if lower.startswith(prefix):

            name = text[
                len(prefix):
            ].strip()

            result = self.check_python(name)

            if not result["success"]:

                if result.get("errors"):

                    return (
                        "Project has "
                        f"{len(result['errors'])} "
                        "Python error(s).\n\n"
                        + "\n".join(
                            f"- {item['file']}: "
                            f"{item['error']}"
                            for item in result["errors"]
                        )
                    )

                return result.get(
                    "error",
                    "Project check failed."
                )

            return (
                "Project checked successfully.\n"
                f"Python files checked: "
                f"{result['checked']}\n"
                "No Python syntax errors found."
            )

        # --------------------------------------------------
        # RUN
        # --------------------------------------------------

        prefix = "run project "

        if lower.startswith(prefix):

            remainder = text[
                len(prefix):
            ].strip()

            parts = remainder.split()

            if not parts:
                return "Which project should I run?"

            project = parts[0]

            filename = (
                parts[1]
                if len(parts) > 1
                else "main.py"
            )

            result = self.run_python(
                project,
                filename
            )

            if not result["success"]:

                return (
                    "Project failed to run.\n\n"
                    + result.get(
                        "error",
                        result.get(
                            "stderr",
                            "Unknown error."
                        )
                    )
                )

            output = result.get(
                "stdout",
                ""
            ).strip()

            if not output:

                output = (
                    "Project finished "
                    "successfully."
                )

            return (
                "Project ran successfully.\n\n"
                + output
            )

        # --------------------------------------------------
        # TEST
        # --------------------------------------------------

        prefix = "test project "

        if lower.startswith(prefix):

            name = text[
                len(prefix):
            ].strip()

            result = self.test_python(name)

            if result["success"]:

                return (
                    "All project tests passed.\n\n"
                    + result.get(
                        "stdout",
                        ""
                    )
                )

            return (
                "Project tests failed.\n\n"
                + result.get("stdout", "")
                + "\n"
                + result.get("stderr", "")
                + "\n"
                + result.get("error", "")
            )

        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        prefix = "delete project "

        if lower.startswith(prefix):

            name = text[
                len(prefix):
            ].strip()

            result = self.delete_project(name)

            if not result["success"]:
                return result["error"]

            return (
                f"Project '{name}' "
                "deleted successfully."
            )

        # --------------------------------------------------
        # UNKNOWN
        # --------------------------------------------------

        return None


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

project_manager = ProjectManager()


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def list_projects():
    return project_manager.list_projects()


def create_project(name, folders=None):
    return project_manager.create_project(
        name,
        folders
    )


def inspect_project(name):
    return project_manager.inspect(name)


def status_project(name):
    return project_manager.status(name)


def read_project_file(project, filename):
    return project_manager.read_file(
        project,
        filename
    )


def write_project_file(
    project,
    filename,
    content
):
    return project_manager.write_file(
        project,
        filename,
        content
    )


def run_project(
    name,
    filename="main.py"
):
    return project_manager.run_python(
        name,
        filename
    )


def test_project(name):
    return project_manager.test_python(name)


def check_project(name):
    return project_manager.check_python(name)


def delete_project(name):
    return project_manager.delete_project(name)


# ==========================================================
# TEST
# ==========================================================

def test_manager():

    print("=" * 60)
    print("NITRON PROJECT MANAGER TEST")
    print("=" * 60)

    print()

    projects = list_projects()

    print("Generated projects:")

    if projects:

        for project in projects:
            print(" -", project)

    else:
        print(" No projects yet.")

    print()

    print("Project manager ready.")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    test_manager()
