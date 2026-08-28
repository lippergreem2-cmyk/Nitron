import speech_recognition as sr


class WakeWord:

    def __init__(self):

        self.recognizer = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:

            print("Listening for wake word...")

            self.recognizer.adjust_for_ambient_noise(source)

            audio = self.recognizer.listen(source)

        try:

            text = self.recognizer.recognize_google(audio)

            print("Heard:", text)

            return text.lower()

        except Exception:

            return ""

    def detected(self):

        text = self.listen()

        return (
            "nitron" in text or
            "nitron wake up" in text
        )
