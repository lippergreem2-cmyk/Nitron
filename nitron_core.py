"""
Nitron Core
"""

from automation_manager import automation
from workflow_manager import workflow
from memory_manager import memory


class NitronCore:

    def __init__(self):

        self.version = "2.0"

        self.name = "Nitron"

        self.status = "Online"

    def info(self):

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status
        }

    def create_game(self, name):

        memory.remember("last_game", name)

        return automation.create_game(name)

    def create_website(self, name):

        memory.remember("last_website", name)

        return automation.create_website(name)

    def create_chatbot(self, name):

        memory.remember("last_chatbot", name)

        return automation.create_chatbot(name)

    def create_api(self, name):

        memory.remember("last_api", name)

        return automation.create_api(name)

    def generate_image(self, prompt):

        memory.remember("last_image", prompt)

        return automation.generate_image(prompt)

    def generate_video(self, prompt):

        memory.remember("last_video", prompt)

        return automation.generate_video(prompt)

    def generate_code(self, prompt):

        memory.remember("last_code", prompt)

        return automation.generate_code(prompt)


nitron = NitronCore()
