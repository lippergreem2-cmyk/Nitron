class ChatBot:

    def __init__(self):

        self.responses = {

            "hello": "Hello!",
            "hi": "Hi there!",
            "how are you": "I'm doing great.",
            "bye": "Goodbye!"

        }

    def reply(self, message):

        message = message.lower()

        return self.responses.get(
            message,
            "I don't understand yet."
        )
