"""
Nitron Conversation State
Controls conversation modes.
"""


class ConversationState:

    def __init__(self):

        self.mode = "listening"

        self.last_message = ""

        self.last_response = ""

        self.waiting_for_next = False


    def listen(self):

        self.mode = "listening"
        self.waiting_for_next = False


    def speaking(self):

        self.mode = "speaking"


    def wait(self):

        self.mode = "waiting"
        self.waiting_for_next = True


    def interrupt(self):

        self.mode = "listening"
        self.waiting_for_next = False


    def update_message(self, message):

        self.last_message = message


    def update_response(self, response):

        self.last_response = response


    def status(self):

        return {

            "mode": self.mode,

            "waiting": self.waiting_for_next,

            "last_message": self.last_message,

            "last_response": self.last_response

        }


state = ConversationState()
