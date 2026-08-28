"""
Nitron Task Manager
"""

import time


class TaskManager:

    def __init__(self):
        self.tasks = []

    def add(self, task_type, prompt):

        self.tasks.append({
            "type": task_type,
            "prompt": prompt,
            "status": "waiting",
            "created": time.time()
        })

        return f"Task added ({task_type})."

    def next(self):

        for task in self.tasks:

            if task["status"] == "waiting":

                task["status"] = "running"

                return task

        return None

    def finish(self, task):

        task["status"] = "finished"

    def list(self):

        return self.tasks

    def clear(self):

        self.tasks.clear()


tasks = TaskManager()
