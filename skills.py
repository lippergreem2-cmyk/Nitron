"""
Nitron Skills Manager
"""

class Skills:

    def __init__(self):
        self.skills = {}

    def register(self, name, function):
        self.skills[name.lower()] = function

    def execute(self, name, *args):

        name = name.lower()

        if name not in self.skills:
            return f"Skill '{name}' not found."

        return self.skills[name](*args)

    def list(self):
        return sorted(self.skills.keys())


skills = Skills()
