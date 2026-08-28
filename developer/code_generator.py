# ==========================================================
# NITRON REAL CODE GENERATOR v2.0
# ==========================================================

import os
import json
import shutil


class CodeGenerator:

    def __init__(self, workspace=None):

        if workspace is None:
            workspace = os.path.expanduser(
                "~/Nitron/GeneratedProjects"
            )

        self.workspace = os.path.abspath(workspace)

        os.makedirs(
            self.workspace,
            exist_ok=True
        )

    # ======================================================
    # SAFE PROJECT NAME
    # ======================================================

    def _safe_name(self, name):

        name = str(name).strip()

        if not name:
            return "NewProject"

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "_- "
        )

        cleaned = ""

        for char in name:

            if char in allowed:
                cleaned += char
            else:
                cleaned += "_"

        cleaned = cleaned.strip()

        return cleaned or "NewProject"

    # ======================================================
    # SAFE FILE PATH
    # ======================================================

    def _safe_relative_path(self, relative_path):

        if not relative_path:
            raise ValueError(
                "File path cannot be empty."
            )

        relative_path = str(
            relative_path
        ).replace("\\", "/")

        relative_path = os.path.normpath(
            relative_path
        )

        if (
            relative_path == ".."
            or relative_path.startswith(
                ".." + os.sep
            )
        ):

            raise ValueError(
                "Invalid file path."
            )

        if os.path.isabs(
            relative_path
        ):

            raise ValueError(
                "Absolute file paths are not allowed."
            )

        return relative_path

    # ======================================================
    # CREATE PROJECT
    # ======================================================

    def create_project(self, project_name):

        project_name = self._safe_name(
            project_name
        )

        project_path = os.path.join(
            self.workspace,
            project_name
        )

        os.makedirs(
            project_path,
            exist_ok=True
        )

        return project_path

    # ======================================================
    # WRITE FILE
    # ======================================================

    def write_file(
        self,
        project_path,
        relative_path,
        content
    ):

        relative_path = self._safe_relative_path(
            relative_path
        )

        project_path = os.path.abspath(
            project_path
        )

        file_path = os.path.abspath(
            os.path.join(
                project_path,
                relative_path
            )
        )

        if not (
            file_path == project_path
            or file_path.startswith(
                project_path + os.sep
            )
        ):

            raise ValueError(
                "File path is outside project."
            )

        os.makedirs(
            os.path.dirname(
                file_path
            ),
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                str(content)
            )

        return file_path

    # ======================================================
    # WRITE AI PROJECT
    # ======================================================

    def write_ai_project(
        self,
        project_name,
        files,
        description=""
    ):

        if not isinstance(
            files,
            dict
        ):

            raise TypeError(
                "AI project files must be a dictionary."
            )

        project_path = self.create_project(
            project_name
        )

        created_files = []

        for relative_path, content in files.items():

            if not isinstance(
                relative_path,
                str
            ):

                raise TypeError(
                    "File names must be strings."
                )

            file_path = self.write_file(
                project_path,
                relative_path,
                content
            )

            created_files.append(
                os.path.relpath(
                    file_path,
                    project_path
                ).replace("\\", "/")
            )

        manifest = self.create_manifest(
            project_path,
            project_name,
            description
        )

        return {
            "success": True,
            "project": project_name,
            "path": project_path,
            "files": sorted(
                created_files
            ),
            "manifest": manifest
        }

    # ======================================================
    # WRITE COMPLETE PROJECT
    # ======================================================

    def write_project(
        self,
        project_name,
        files
    ):

        return self.write_ai_project(
            project_name,
            files
        )

    # ======================================================
    # READ FILE
    # ======================================================

    def read_file(
        self,
        project_path,
        relative_path
    ):

        relative_path = self._safe_relative_path(
            relative_path
        )

        file_path = os.path.abspath(
            os.path.join(
                project_path,
                relative_path
            )
        )

        project_path = os.path.abspath(
            project_path
        )

        if not file_path.startswith(
            project_path + os.sep
        ):

            raise ValueError(
                "File path is outside project."
            )

        if not os.path.isfile(
            file_path
        ):

            raise FileNotFoundError(
                file_path
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    # ======================================================
    # READ PROJECT
    # ======================================================

    def read_project(
        self,
        project_path
    ):

        project_path = os.path.abspath(
            os.path.expanduser(
                project_path
            )
        )

        if not os.path.isdir(
            project_path
        ):

            raise FileNotFoundError(
                project_path
            )

        project_files = {}

        for root, directories, files in os.walk(
            project_path
        ):

            directories[:] = [
                directory
                for directory in directories
                if directory not in (
                    "__pycache__",
                    ".git"
                )
            ]

            for filename in files:

                full_path = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    full_path,
                    project_path
                ).replace("\\", "/")

                try:

                    with open(
                        full_path,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        project_files[
                            relative_path
                        ] = file.read()

                except (
                    UnicodeDecodeError,
                    PermissionError
                ):

                    continue

        return project_files

    # ======================================================
    # UPDATE FILE
    # ======================================================

    def update_file(
        self,
        project_path,
        relative_path,
        content
    ):

        return self.write_file(
            project_path,
            relative_path,
            content
        )

    # ======================================================
    # DELETE FILE
    # ======================================================

    def delete_file(
        self,
        project_path,
        relative_path
    ):

        relative_path = self._safe_relative_path(
            relative_path
        )

        file_path = os.path.abspath(
            os.path.join(
                project_path,
                relative_path
            )
        )

        project_path = os.path.abspath(
            project_path
        )

        if not file_path.startswith(
            project_path + os.sep
        ):

            raise ValueError(
                "File path is outside project."
            )

        if not os.path.isfile(
            file_path
        ):

            return False

        os.remove(
            file_path
        )

        return True

    # ======================================================
    # DELETE PROJECT
    # ======================================================

    def delete_project(
        self,
        project_name
    ):

        project_name = self._safe_name(
            project_name
        )

        project_path = os.path.join(
            self.workspace,
            project_name
        )

        if not os.path.isdir(
            project_path
        ):

            return False

        shutil.rmtree(
            project_path
        )

        return True

    # ======================================================
    # PROJECT MANIFEST
    # ======================================================

    def create_manifest(
        self,
        project_path,
        project_name,
        description=""
    ):

        files = self.read_project(
            project_path
        )

        manifest = {

            "name": project_name,

            "description": description,

            "files": sorted(
                files.keys()
            )

        }

        manifest_path = self.write_file(
            project_path,
            "nitron_project.json",
            json.dumps(
                manifest,
                indent=4
            )
        )

        return {

            "path": manifest_path,

            "name": project_name,

            "description": description,

            "files": manifest["files"]

        }

    # ======================================================
    # PROJECT EXISTS
    # ======================================================

    def project_exists(
        self,
        project_name
    ):

        project_name = self._safe_name(
            project_name
        )

        return os.path.isdir(
            os.path.join(
                self.workspace,
                project_name
            )
        )

    # ======================================================
    # GET PROJECT PATH
    # ======================================================

    def get_project_path(
        self,
        project_name
    ):

        project_name = self._safe_name(
            project_name
        )

        return os.path.join(
            self.workspace,
            project_name
        )

    # ======================================================
    # LIST PROJECTS
    # ======================================================

    def list_projects(self):

        if not os.path.isdir(
            self.workspace
        ):

            return []

        return sorted(
            name
            for name in os.listdir(
                self.workspace
            )
            if os.path.isdir(
                os.path.join(
                    self.workspace,
                    name
                )
            )
        )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("NITRON REAL CODE GENERATOR v2.0")
    print("=" * 60)

    generator = CodeGenerator()

    result = generator.write_ai_project(

        "NitronGeneratorTestV2",

        {

            "main.py":
                'def main():\n'
                '    print("Hello from Nitron AI!")\n'
                '\n'
                '\n'
                'if __name__ == "__main__":\n'
                '    main()\n',

            "utils/helper.py":
                'def hello(name):\n'
                '    return f"Hello, {name}!"\n',

            "README.md":
                "# Nitron AI Generator Test\n\n"
                "Generated by Nitron.\n"

        },

        "Testing Nitron's real AI code generator."

    )

    print()
    print("Project created successfully.")
    print()
    print("Project:")
    print(result["project"])
    print()
    print("Location:")
    print(result["path"])
    print()
    print("Files:")

    for filename in result["files"]:

        print(
            "  -",
            filename
        )

    print()
    print("Available projects:")

    for project in generator.list_projects():

        print(
            "  -",
            project
        )

    print()
    print("=" * 60)
    print("GENERATOR TEST COMPLETE")
    print("=" * 60)
