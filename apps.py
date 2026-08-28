import subprocess
import os

def launch(package):
    try:
        installed = os.popen(
            f"cmd package list packages --user 0 | grep {package}"
        ).read()

        if not installed.strip():
            return False

        result = subprocess.run(
            [
                "am",
                "start",
                "-a",
                "android.intent.action.MAIN",
                "-c",
                "android.intent.category.LAUNCHER",
                "-p",
                package
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return False

        if "Error" in result.stdout or "Error" in result.stderr:
            return False

        return True

    except Exception:
        return False
