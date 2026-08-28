"""
Nitron Plugin Manager v2
"""

import os
import traceback
import importlib.util


class PluginManager:

    def __init__(self, plugin_folder="plugins"):

        self.plugin_folder = plugin_folder
        self.plugins = {}

        os.makedirs(self.plugin_folder, exist_ok=True)

        self.load_plugins()

    # ==========================================
    # LOAD PLUGINS
    # ==========================================

    def load_plugins(self):

        self.plugins.clear()

        for filename in os.listdir(self.plugin_folder):

            if not filename.endswith(".py"):
                continue

            path = os.path.join(
                self.plugin_folder,
                filename
            )

            name = filename[:-3]

            try:

                spec = importlib.util.spec_from_file_location(
                    name,
                    path
                )

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                if not hasattr(module, "plugin"):
                    continue

                info = module.plugin()

                info.setdefault("name", name)
                info.setdefault("commands", [])
                info.setdefault("aliases", [])
                info.setdefault("priority", 100)
                info.setdefault("enabled", True)

                self.plugins[info["name"]] = info

            except Exception:

                print(f"Failed to load {name}")
                print(traceback.format_exc())

    # ==========================================
    # EXECUTE
    # ==========================================

    def execute(self, command):

        command = command.lower().strip()

        plugins = sorted(
            self.plugins.values(),
            key=lambda p: p.get("priority", 100)
        )

        for plugin in plugins:

            if not plugin.get("enabled", True):
                continue

            commands = [
                c.lower()
                for c in plugin.get("commands", [])
            ]

            aliases = [
                a.lower()
                for a in plugin.get("aliases", [])
            ]

            match_mode = plugin.get("match_mode", "prefix")

            for trigger in commands + aliases:

                matched = False

                if match_mode == "contains":

                    if trigger in command:
                        matched = True

                else:

                    if (
                        command == trigger
                        or
                        command.startswith(trigger + " ")
                    ):
                        matched = True

                if matched:

                    try:

                        return plugin["run"](command)

                    except Exception:

                        return traceback.format_exc()

        return None

    # ==========================================
    # HELPERS
    # ==========================================

    def plugin_names(self):

        return sorted(self.plugins.keys())

    def plugin_count(self):

        return len(self.plugins)

    def reload(self):

        self.load_plugins()

    def summary(self):

        return {
            "plugins": len(self.plugins),
            "names": self.plugin_names()
        }


plugin_manager = PluginManager()
