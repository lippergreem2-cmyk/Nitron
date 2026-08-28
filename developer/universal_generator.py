"""
Nitron Universal Project Generator
"""

import os

PROJECTS = os.path.expanduser("~/Nitron/generated_projects")

os.makedirs(PROJECTS, exist_ok=True)


class UniversalGenerator:

    def __init__(self):
        self.projects = {}

    def register(self, name, creator):
        self.projects[name.lower()] = creator

    def create(self, project_type):

        key = project_type.lower().strip()

        if key not in self.projects:
            return (
                f"Unknown project: {project_type}\n"
                "Register a generator first."
            )

        return self.projects[key]()


generator = UniversalGenerator()
