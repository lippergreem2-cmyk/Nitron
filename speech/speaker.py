import subprocess


class Speaker:

    def __init__(self):

        self.engine = "termux-tts-speak"
        self.rate = "0.95"   # slightly slower than default = more natural
        self.pitch = "1.0"
        self.current_process = None

    def speak(self, text, interruptible=False):

        print("Nitron:", text)

        try:

            args = [
                self.engine,
                "-r", self.rate,
                "-p", self.pitch,
                text,
            ]

            if interruptible:
                # Non-blocking: caller can poll is_speaking() / call stop()
                self.current_process = subprocess.Popen(args)
                return self.current_process
            else:
                subprocess.run(args)
                return None

        except Exception as e:

            print(f"Text-to-Speech is not available: {e}")
            return None

    def is_speaking(self):
        return self.current_process is not None and self.current_process.poll() is None

    def stop(self):
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
            except Exception:
                pass
        self.current_process = None

    def wake_up(self):

        self.speak(
            "Yes Boss Nimrod. How can I help you?"
        )

    def goodbye(self):

        self.speak(
            "Goodbye Boss Nimrod."
        )

    def thinking(self):

        self.speak(
            "Please wait. I am thinking."
        )

    def error(self):

        self.speak(
            "Sorry Boss Nimrod. I didn't understand."
        )
