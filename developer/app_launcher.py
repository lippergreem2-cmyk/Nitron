# ==========================================================
# NITRON APP LAUNCHER v1.0
# Android Development Environment Launcher
# ==========================================================

import subprocess


class AppLauncher:

    def __init__(self):
        self.apps = {
            "vscode": [
                "com.microsoft.vscode"
            ],
            "android_studio": [
                "com.google.android.studio"
            ],
            "antigravity": [
                "com.google.android.apps.antigravity"
            ],
        }

    def package_installed(self, package):
        try:
            result = subprocess.run(
                ["pm", "path", package],
                capture_output=True,
                text=True
            )

            return result.returncode == 0 and bool(
                result.stdout.strip()
            )

        except Exception:
            return False

    def find_app(self, name):
        name = name.lower().strip()

        packages = self.apps.get(name, [])

        for package in packages:
            if self.package_installed(package):
                return package

        return None

    def launch(self, name):
        package = self.find_app(name)

        if not package:
            return {
                "success": False,
                "error": f"{name} is not installed or not detected."
            }

        try:
            result = subprocess.run(
                [
                    "monkey",
                    "-p",
                    package,
                    "1"
                ],
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "package": package,
                "output": result.stdout.strip()
            }

        except Exception as error:
            return {
                "success": False,
                "error": str(error)
            }

    def status(self):
        result = {}

        for name in self.apps:
            result[name] = self.find_app(name)

        return result


if __name__ == "__main__":

    launcher = AppLauncher()

    print("=" * 60)
    print("NITRON APP LAUNCHER v1.0")
    print("=" * 60)

    print()

    for name, package in launcher.status().items():
        print(
            f"{name}: "
            + (package or "NOT INSTALLED")
        )

    print("=" * 60)
