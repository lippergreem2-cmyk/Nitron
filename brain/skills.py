"""
Nitron Skills Manager
"""


class Skills:
    def __init__(self):
        self.skills = {}

    def register(self, name, description, function=None):
        """
        Add a new skill.
        """
        self.skills[name] = {
            "description": description,
            "function": function
        }

    def remove(self, name):
        """
        Remove a skill.
        """
        if name in self.skills:
            del self.skills[name]

    def exists(self, name):
        """
        Check if a skill exists.
        """
        return name in self.skills

    def get(self, name):
        """
        Get a skill.
        """
        return self.skills.get(name)

    def list(self):
        """
        List all skills.
        """
        return self.skills

    def run(self, name, *args, **kwargs):
        """
        Execute a skill.
        """
        skill = self.get(name)

        if skill and skill["function"]:
            return skill["function"](*args, **kwargs)

        return "Skill not available."


skills = Skills()


# Default Nitron skills
skills.register(
    "academy",
    "Teach programming and other subjects"
)

skills.register(
    "developer",
    "Create software projects"
)

skills.register(
    "voice",
    "Listen and speak"
)

skills.register(
    "trading",
    "Analyze markets"
)
