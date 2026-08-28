import os
import importlib


class PluginManager:

    def __init__(self):

        self.plugins = {}


    def discover(self, folder="."):

        self.plugins.clear()

        for file in os.listdir(folder):

            if not file.endswith(".py"):
                continue

            if file.startswith("__"):
                continue

            if file == "plugin_manager.py":
                continue

            name = file[:-3]

            self.plugins[name] = {

                "enabled": True,

                "file": file

            }

        return list(self.plugins.keys())


    def enable(self, name):

        if name in self.plugins:

            self.plugins[name]["enabled"] = True

            return f"{name} enabled."

        return "Plugin not found."


    def disable(self, name):

        if name in self.plugins:

            self.plugins[name]["enabled"] = False

            return f"{name} disabled."

        return "Plugin not found."


    def list_plugins(self):

        result = []

        for name, info in self.plugins.items():

            status = "Enabled" if info["enabled"] else "Disabled"

            result.append(f"{name} - {status}")

        return result


    def load(self, name):

        if name not in self.plugins:

            return None

        if not self.plugins[name]["enabled"]:

            return None

        try:

            module = importlib.import_module(name)

            return module

        except Exception as e:

            print(e)

            return None


    def reload(self, name):

        try:

            module = importlib.import_module(name)

            importlib.reload(module)

            return f"{name} reloaded."

        except Exception as e:

            return str(e)


    def load_all(self):

        loaded = []

        for name in self.plugins:

            if self.plugins[name]["enabled"]:

                module = self.load(name)

                if module:

                    loaded.append(name)

        return loaded


    def plugin_count(self):

        return len(self.plugins)


    def enabled_count(self):

        return len(

            [

                p

                for p in self.plugins.values()

                if p["enabled"]

            ]

        )


    def disabled_count(self):

        return len(

            [

                p

                for p in self.plugins.values()

                if not p["enabled"]

            ]

        )


if __name__ == "__main__":

    manager = PluginManager()

    manager.discover()

    print("Plugins:")

    for plugin in manager.list_plugins():

        print(plugin)
