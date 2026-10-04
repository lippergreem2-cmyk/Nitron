import subprocess


class CommandListener:

    def listen(self):
        print("Waiting for your command...")
        try:
            result = subprocess.check_output(
                ["termux-speech-to-text"],
                text=True,
                timeout=15
            )
            command = result.strip()
            if command:
                print("Command:", command)
            return command
        except subprocess.TimeoutExpired:
            return ""
        except Exception as error:
            print("Listen error:", error)
            return ""

    def get_command(self):
        while True:
            command = self.listen()
            if command != "":
                return command
