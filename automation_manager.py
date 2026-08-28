"""
Nitron Automation Manager
"""

from task_manager import tasks
from job_manager import jobs


class AutomationManager:

    def run(self, task_type, prompt):

        job_id = jobs.create(task_type, prompt)

        jobs.start(job_id)

        tasks.add(task_type, prompt)

        result = f"{task_type.capitalize()} task scheduled."

        jobs.finish(job_id, result)

        return {
            "job_id": job_id,
            "status": "finished",
            "result": result
        }

    def create_game(self, name):

        return self.run("game", name)

    def create_website(self, name):

        return self.run("website", name)

    def create_chatbot(self, name):

        return self.run("chatbot", name)

    def create_api(self, name):

        return self.run("api", name)

    def generate_image(self, prompt):

        return self.run("image", prompt)

    def generate_video(self, prompt):

        return self.run("video", prompt)

    def generate_code(self, prompt):

        return self.run("code", prompt)


automation = AutomationManager()
