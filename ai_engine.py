"""
Nitron AI Engine
"""

class AIEngine:

    def __init__(self):

        self.backends = {}

        self.current = None

    def register(self, name, backend):

        self.backends[name] = backend

        if self.current is None:
            self.current = name

    def use(self, name):

        if name not in self.backends:
            return False

        self.current = name
        return True

    def current_backend(self):

        return self.current

    def ask(self, prompt):

        if self.current is None:
            return "No AI backend loaded."

        return self.backends[self.current](prompt)


engine = AIEngine()
