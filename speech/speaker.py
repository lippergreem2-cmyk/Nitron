import subprocess


class Speaker:

    def __init__(self):

        self.engine = "termux-tts-speak"

    def speak(self, text):

        print("Nitron:", text)

        try:

            subprocess.run([
                self.engine,
                text
            ])

        except Exception:

            print("Text-to-Speech is not available.")

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
