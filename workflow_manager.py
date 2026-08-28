"""
Nitron Workflow Manager
"""

class WorkflowManager:

    def __init__(self):

        self.workflows = {}

    def create(self, name, steps):

        self.workflows[name] = {
            "name": name,
            "steps": steps
        }

        return f"Workflow '{name}' created."

    def run(self, name):

        if name not in self.workflows:
            return f"Workflow '{name}' not found."

        workflow = self.workflows[name]

        print(f"Running workflow: {name}")

        for number, step in enumerate(workflow["steps"], start=1):
            print(f"[{number}] {step}")

        return "Workflow completed."

    def list(self):

        return list(self.workflows.keys())

    def delete(self, name):

        if name in self.workflows:
            del self.workflows[name]
            return True

        return False


workflow = WorkflowManager()
