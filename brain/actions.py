"""
Nitron Actions
"""

from brain.executor import executor


class Actions:
    """
    Defines actions that Nitron can perform.
    """

    def open_app(self, app_name):
        return f"Opening {app_name}..."

    def teach(self, subject):
        return f"Starting {subject} lesson..."

    def create_project(self, project_name):
        return f"Creating project '{project_name}'..."

    def search(self, query):
        return f"Searching for '{query}'..."

    def trade(self, symbol):
        return f"Analyzing market for {symbol}..."

    def play_music(self, song):
        return f"Playing '{song}'..."

    def tell_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def tell_date(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def execute(self, command):
        """
        Forward a command to the executor.
        """
        return executor.execute(command)


actions = Actions()
