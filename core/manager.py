"""
Nitron Module Manager
"""

class Manager:
    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        """
        Register a module with Nitron.
        """
        self.modules[name] = module

    def unregister(self, name):
        """
        Remove a module.
        """
        if name in self.modules:
            del self.modules[name]

    def get(self, name):
        """
        Get a registered module.
        """
        return self.modules.get(name)

    def exists(self, name):
        """
        Check if a module exists.
        """
        return name in self.modules

    def list_modules(self):
        """
        Return all registered module names.
        """
        return sorted(self.modules.keys())

    def count(self):
        """
        Return the number of registered modules.
        """
        return len(self.modules)

    def clear(self):
        """
        Remove all modules.
        """
        self.modules.clear()
