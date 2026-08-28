import subprocess
import shutil


class ToolRunner:

    def exists(self, tool):

        return shutil.which(tool) is not None

    def run(self, command, cwd=None):

        try:

            result = subprocess.run(
                command,
                cwd=cwd,
                shell=True,
                text=True,
                capture_output=True
            )

            if result.returncode == 0:

                return result.stdout.strip()

            return result.stderr.strip()

        except Exception as e:

            return str(e)
