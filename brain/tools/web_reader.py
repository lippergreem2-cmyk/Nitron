"""
Nitron Conversation State
Controls conversation modes:
- listening
- speaking
- waiting
Handles interruptions and conversation flow.
"""


class ConversationState:

    def __init__(self):
        self.mode = "listening"

        self.last_message = ""
        self.last_response = ""

        self.waiting_for_next = False


    def listen(self):
        """
        Nitron is listening to the user.
        """

        self.mode = "listening"
        self.waiting_for_next = False


    def speaking(self):
        """
        Nitron is currently responding.
        """

        self.mode = "speaking"
        self.waiting_for_next = False


    def wait(self):
        """
        Nitron finished speaking and waits
        for the user's next response.
        """

        self.mode = "waiting"
        self.waiting_for_next = True


    def interrupt(self):
        """
        User interrupted Nitron.
        Stop current response and return to listening mode.
        """

        self.mode = "listening"
        self.waiting_for_next = False


    def update_message(self, message):
        """
        Save the user's latest message.
        """

        self.last_message = message


    def update_response(self, response):
        """
        Save Nitron's latest response.
        """

        self.last_response = response


    def status(self):
        """
        Return current conversation state.
        """

        return {
            "mode": self.mode,
            "waiting": self.waiting_for_next,
            "last_message": self.last_message,
            "last_response": self.last_response
        }


# Global conversation state
state = ConversationState()
