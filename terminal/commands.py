import os
import subprocess


class CommandExecutor:

    def __init__(self):
        self.current_directory = os.getcwd()

    def execute(self, command):

        try:

            result = subprocess.run(
                command,
                shell=True,
                cwd=self.current_directory,
                capture_output=True,
                text=True
            )

            if result.stdout:
                return result.stdout.strip()

            if result.stderr:
                return result.stderr.strip()

            return ""

        except Exception as error:
            return str(error)
