"""
Nitron Conversation Manager
Controls the full conversation flow.
"""

from brain.conversation.state import state
from brain.conversation.pace import pace
from brain.conversation.interrupt import interrupt


class ConversationManager:

    def __init__(self):
        self.active = True


    def start_listening(self):
        state.listen()


    def start_response(self, response):
        state.speaking()
        state.update_response(response)


    def finish_response(self):
        state.wait()


    def user_message(self, message):
        state.update_message(message)

        if interrupt.is_interrupted():
            interrupt.reset()

        state.listen()


    def get_status(self):
        return {
            "state": state.status(),
            "pace": pace.settings(),
            "interrupted": interrupt.is_interrupted()
        }


manager = ConversationManager()
