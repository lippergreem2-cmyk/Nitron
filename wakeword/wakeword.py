import subprocess


class WakeWord:

    def listen(self):
        print("Listening for wake word...")
        try:
            result = subprocess.check_output(
                ["termux-speech-to-text"],
                text=True,
                timeout=15
            )
            text = result.strip().lower()
            if text:
                print("Heard:", text)
            return text
        except subprocess.TimeoutExpired:
            return ""
        except Exception as error:
            print("Wake word listen error:", error)
            return ""

    def detected(self):
        text = self.listen()
        return "nitron" in text
