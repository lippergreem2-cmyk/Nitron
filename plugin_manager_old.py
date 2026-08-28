    def plugin_info(self, name):

        if name not in self.plugins:
            return None

        plugin = self.plugins[name]

        return {
            "name": plugin.get("name", "Unknown"),
            "description": plugin.get("description", ""),
            "commands": plugin.get("commands", []),
            "version": plugin.get("version", "1.0"),
            "author": plugin.get("author", "Nitron")
        }

    def list_plugins(self):

        if not self.plugins:
            print("No plugins loaded.")
            return

        print("\n========== PLUGINS ==========\n")

        for name, plugin in sorted(self.plugins.items()):

            print(name)

            if plugin.get("description"):
                print("  Description :", plugin["description"])

            if plugin.get("version"):
                print("  Version     :", plugin.get("version", "1.0"))

            if plugin.get("author"):
                print("  Author      :", plugin.get("author", "Unknown"))

            print("  Commands")

            for command in plugin.get("commands", []):

                print("   -", command)

            print()

    def reload(self):

        print("Reloading plugins...")

        self.load_plugins()

        print("Loaded", len(self.plugins), "plugins.")

    def unload(self, name):

        if name in self.plugins:

            del self.plugins[name]

            return True

        return False

    def exists(self, name):

        return name in self.plugins

    def count(self):

        return len(self.plugins)

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for name, plugin in self.plugins.items():

            if keyword in name.lower():

                results.append(name)

                continue

            if keyword in plugin.get("description", "").lower():

                results.append(name)

                continue

            for cmd in plugin.get("commands", []):

                if keyword in cmd.lower():

                    results.append(name)

                    break

        return sorted(results)import json
import time

CONFIG_FILE = "plugins/plugins.json"


    def load_settings(self):

        if not os.path.exists(CONFIG_FILE):

            self.settings = {

                "enabled": [],

                "disabled": []

            }

            self.save_settings()

            return

        with open(CONFIG_FILE, "r") as f:

            self.settings = json.load(f)


    def save_settings(self):

        with open(CONFIG_FILE, "w") as f:

            json.dump(self.settings, f, indent=4)


    def enable_plugin(self, name):

        if name in self.settings["disabled"]:

            self.settings["disabled"].remove(name)

        if name not in self.settings["enabled"]:

            self.settings["enabled"].append(name)

        self.save_settings()


    def disable_plugin(self, name):

        if name in self.settings["enabled"]:

            self.settings["enabled"].remove(name)

        if name not in self.settings["disabled"]:

            self.settings["disabled"].append(name)

        self.save_settings()


    def is_enabled(self, name):

        return name not in self.settings["disabled"]


    def log(self, message):

        with open("plugins/plugin.log", "a") as f:

            now = time.strftime("%Y-%m-%d %H:%M:%S")

            f.write(f"[{now}] {message}\n")


    def statistics(self):

        return {

            "loaded": len(self.plugins),

            "enabled": len(self.settings["enabled"]),

            "disabled": len(self.settings["disabled"])

        }


    def execute(self, command):

        command = command.lower()

        for plugin in self.plugins.values():

            if plugin["name"] in self.settings["disabled"]:

                continue

            if command in plugin["commands"]:

                self.log(f"Running {plugin['name']}")

                return plugin["run"](command)

        return None    # ============================
    # CATEGORIES
    # ============================

    def categories(self):

        groups = {}

        for name, plugin in self.plugins.items():

            category = plugin.get("category", "General")

            if category not in groups:

                groups[category] = []

            groups[category].append(name)

        return groups


    def plugins_in_category(self, category):

        result = []

        for name, plugin in self.plugins.items():

            if plugin.get("category", "General").lower() == category.lower():

                result.append(name)

        return sorted(result)


    # ============================
    # COMMAND LOOKUP
    # ============================

    def command_exists(self, command):

        command = command.lower()

        for plugin in self.plugins.values():

            if command in plugin.get("commands", []):

                return True

        return False


    def find_plugin(self, command):

        command = command.lower()

        for name, plugin in self.plugins.items():

            if command in plugin.get("commands", []):

                return name

        return None


    # ============================
    # STARTUP
    # ============================

    def startup(self):

        for plugin in self.plugins.values():

            if "startup" in plugin:

                try:

                    plugin["startup"]()

                except Exception as error:

                    print("Startup Error:", error)


    # ============================
    # SHUTDOWN
    # ============================

    def shutdown(self):

        for plugin in self.plugins.values():

            if "shutdown" in plugin:

                try:

                    plugin["shutdown"]()

                except Exception as error:

                    print("Shutdown Error:", error)


    # ============================
    # LOGGING
    # ============================

    def log(self, message):

        from datetime import datetime

        with open("plugin.log", "a") as file:

            file.write(

                "[" +

                datetime.now().strftime("%Y-%m-%d %H:%M:%S") +

                "] " +

                str(message) +

                "\n"

            )


    # ============================
    # SAFE EXECUTION
    # ============================

    def run_plugin(self, name, command):

        if name not in self.plugins:

            return None

        plugin = self.plugins[name]

        if not plugin.get("enabled", True):

            return "Plugin is disabled."

        try:

            self.log("Running " + name)

            return plugin["run"](command)

        except Exception as error:

            self.log(error)

            return "Plugin crashed."    # ============================
    # PLUGIN SETTINGS
    # ============================

    def set_setting(self, plugin_name, key, value):

        if plugin_name not in self.plugins:

            return False

        if "settings" not in self.plugins[plugin_name]:

            self.plugins[plugin_name]["settings"] = {}

        self.plugins[plugin_name]["settings"][key] = value

        return True


    def get_setting(self, plugin_name, key, default=None):

        if plugin_name not in self.plugins:

            return default

        return self.plugins[plugin_name].get("settings", {}).get(key, default)


    # ============================
    # PERMISSIONS
    # ============================

    def grant_permission(self, plugin_name, permission):

        if plugin_name not in self.plugins:

            return False

        permissions = self.plugins[plugin_name].setdefault("permissions", [])

        if permission not in permissions:

            permissions.append(permission)

        return True


    def revoke_permission(self, plugin_name, permission):

        if plugin_name not in self.plugins:

            return False

        permissions = self.plugins[plugin_name].setdefault("permissions", [])

        if permission in permissions:

            permissions.remove(permission)

        return True


    def has_permission(self, plugin_name, permission):

        if plugin_name not in self.plugins:

            return False

        return permission in self.plugins[plugin_name].get("permissions", [])


    # ============================
    # PRIORITY
    # ============================

    def set_priority(self, plugin_name, priority):

        if plugin_name not in self.plugins:

            return False

        self.plugins[plugin_name]["priority"] = priority

        return True


    def sorted_plugins(self):

        return sorted(

            self.plugins.items(),

            key=lambda item: item[1].get("priority", 100)

        )


    # ============================
    # ALIASES
    # ============================

    def register_alias(self, plugin_name, alias):

        if plugin_name not in self.plugins:

            return False

        aliases = self.plugins[plugin_name].setdefault("aliases", [])

        if alias not in aliases:

            aliases.append(alias)

        return True


    def resolve_alias(self, alias):

        alias = alias.lower()

        for name, plugin in self.plugins.items():

            for a in plugin.get("aliases", []):

                if alias == a.lower():

                    return name

        return None


    # ============================
    # USAGE STATISTICS
    # ============================

    def record_usage(self, plugin_name):

        if plugin_name not in self.plugins:

            return

        count = self.plugins[plugin_name].get("usage", 0)

        self.plugins[plugin_name]["usage"] = count + 1


    def most_used(self):

        if not self.plugins:

            return None

        return max(

            self.plugins.items(),

            key=lambda item: item[1].get("usage", 0)

        )[0]    # =====================================
    # DEPENDENCIES
    # =====================================

    def check_dependencies(self, plugin_name):

        if plugin_name not in self.plugins:

            return False

        plugin = self.plugins[plugin_name]

        dependencies = plugin.get("dependencies", [])

        missing = []

        for dependency in dependencies:

            if dependency not in self.plugins:

                missing.append(dependency)

        if missing:

            return {

                "ok": False,

                "missing": missing

            }

        return {

            "ok": True,

            "missing": []

        }

    # =====================================
    # VERSION
    # =====================================

    def plugin_version(self, plugin_name):

        if plugin_name not in self.plugins:

            return None

        return self.plugins[plugin_name].get("version", "1.0.0")

    def compare_version(self, plugin_name, version):

        current = self.plugin_version(plugin_name)

        if current == version:

            return 0

        if current > version:

            return 1

        return -1

    # =====================================
    # HEALTH CHECK
    # =====================================

    def health(self):

        report = {}

        for name in self.plugins:

            try:

                plugin = self.plugins[name]

                report[name] = {

                    "status": "Healthy",

                    "commands": len(plugin.get("commands", [])),

                    "enabled": plugin.get("enabled", True),

                    "version": plugin.get("version", "1.0")

                }

            except Exception as error:

                report[name] = {

                    "status": "Broken",

                    "error": str(error)

                }

        return report

    # =====================================
    # DIAGNOSTICS
    # =====================================

    def diagnostics(self):

        print()

        print("========== NITRON PLUGIN DIAGNOSTICS ==========")

        print()

        print("Plugins Loaded :", len(self.plugins))

        print()

        for name in sorted(self.plugins):

            plugin = self.plugins[name]

            print(name)

            print(" Version :", plugin.get("version", "1.0"))

            print(" Enabled :", plugin.get("enabled", True))

            print(" Commands:", len(plugin.get("commands", [])))

            print()

    # =====================================
    # AUTO LOAD ORDER
    # =====================================

    def load_order(self):

        ordered = sorted(

            self.plugins.items(),

            key=lambda item: item[1].get("priority", 100)

        )

        return [name for name, _ in ordered]

    # =====================================
    # RELOAD ONE PLUGIN
    # =====================================

    def reload_plugin(self, plugin_name):

        filename = plugin_name + ".py"

        filepath = os.path.join(PLUGIN_FOLDER, filename)

        if not os.path.exists(filepath):

            return False

        try:

            spec = importlib.util.spec_from_file_location(plugin_name, filepath)

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            self.plugins[module.plugin()["name"]] = module.plugin()

            return True

        except Exception:

            return False    # =====================================
    # EVENT SYSTEM
    # =====================================

    def emit(self, event, *args, **kwargs):

        results = []

        for name, plugin in self.plugins.items():

            if not plugin.get("enabled", True):
                continue

            events = plugin.get("events", {})

            if event in events:

                try:

                    results.append(events[event](*args, **kwargs))

                except Exception as error:

                    self.log(f"{name} event '{event}' failed: {error}")

        return results


    # =====================================
    # BROADCAST MESSAGE
    # =====================================

    def broadcast(self, message):

        responses = []

        for name, plugin in self.plugins.items():

            if not plugin.get("enabled", True):
                continue

            if "receive" in plugin:

                try:

                    responses.append(plugin["receive"](message))

                except Exception as error:

                    self.log(error)

        return responses


    # =====================================
    # BEFORE / AFTER HOOKS
    # =====================================

    def before_execute(self, command):

        self.emit("before_execute", command)


    def after_execute(self, command, result):

        self.emit("after_execute", command, result)


    # =====================================
    # TIMER SUPPORT
    # =====================================

    def run_timers(self):

        for name, plugin in self.plugins.items():

            if not plugin.get("enabled", True):
                continue

            if "timer" in plugin:

                try:

                    plugin["timer"]()

                except Exception as error:

                    self.log(error)


    # =====================================
    # PLUGIN METRICS
    # =====================================

    def metrics(self):

        report = {}

        for name, plugin in self.plugins.items():

            report[name] = {

                "commands": len(plugin.get("commands", [])),

                "usage": plugin.get("usage", 0),

                "enabled": plugin.get("enabled", True),

                "version": plugin.get("version", "1.0"),

                "priority": plugin.get("priority", 100)

            }

        return report


    # =====================================
    # RESET USAGE COUNTERS
    # =====================================

    def reset_usage(self):

        for plugin in self.plugins.values():

            plugin["usage"] = 0


    # =====================================
    # SAVE METRICS
    # =====================================

    def save_metrics(self):

        import json

        with open("plugin_metrics.json", "w") as file:

            json.dump(self.metrics(), file, indent=4)


    # =====================================
    # LOAD METRICS
    # =====================================

    def load_metrics(self):

        import json

        if not os.path.exists("plugin_metrics.json"):

            return

        with open("plugin_metrics.json", "r") as file:

            metrics = json.load(file)

        for name in metrics:

            if name in self.plugins:

                self.plugins[name]["usage"] = metrics[name].get("usage", 0)    # ======================================
    # TASK QUEUE
    # ======================================

    def add_task(self, plugin, command):

        if not hasattr(self, "task_queue"):

            self.task_queue = []

        self.task_queue.append({

            "plugin": plugin,

            "command": command,

            "time": time.time()

        })

    def run_queue(self):

        if not hasattr(self, "task_queue"):

            return

        while self.task_queue:

            task = self.task_queue.pop(0)

            self.run_plugin(

                task["plugin"],

                task["command"]

            )

    def clear_queue(self):

        self.task_queue = []

    def queue_size(self):

        return len(getattr(self, "task_queue", []))

    # ======================================
    # SCHEDULER
    # ======================================

    def schedule(self, plugin, command, seconds):

        if not hasattr(self, "scheduled"):

            self.scheduled = []

        self.scheduled.append({

            "plugin": plugin,

            "command": command,

            "run_at": time.time() + seconds

        })

    def scheduler_tick(self):

        if not hasattr(self, "scheduled"):

            return

        now = time.time()

        remaining = []

        for task in self.scheduled:

            if now >= task["run_at"]:

                self.run_plugin(

                    task["plugin"],

                    task["command"]

                )

            else:

                remaining.append(task)

        self.scheduled = remaining    # ======================================
    # PLUGIN MARKETPLACE
    # ======================================

    def install_plugin(self, source, destination=None):

        import shutil

        if destination is None:

            destination = os.path.join(

                PLUGIN_FOLDER,

                os.path.basename(source)

            )

        if not os.path.exists(source):

            return False

        shutil.copy(source, destination)

        self.log("Installed " + os.path.basename(source))

        self.reload()

        return True


    def uninstall_plugin(self, plugin_name):

        filename = plugin_name + ".py"

        path = os.path.join(

            PLUGIN_FOLDER,

            filename

        )

        if not os.path.exists(path):

            return False

        os.remove(path)

        self.plugins.pop(plugin_name, None)

        self.log("Removed " + plugin_name)

        return True


    # ======================================
    # BACKUP
    # ======================================

    def backup_plugins(self):

        import shutil

        backup = "plugins_backup"

        if os.path.exists(backup):

            shutil.rmtree(backup)

        shutil.copytree(

            PLUGIN_FOLDER,

            backup

        )

        self.log("Plugin backup created.")

        return backup


    def restore_backup(self):

        import shutil

        backup = "plugins_backup"

        if not os.path.exists(backup):

            return False

        if os.path.exists(PLUGIN_FOLDER):

            shutil.rmtree(PLUGIN_FOLDER)

        shutil.copytree(

            backup,

            PLUGIN_FOLDER

        )

        self.reload()

        self.log("Plugins restored.")

        return True


    # ======================================
    # EXPORT PLUGIN LIST
    # ======================================

    def export_plugin_list(self):

        data = []

        for plugin in self.plugins.values():

            data.append({

                "name": plugin.get("name"),

                "version": plugin.get("version"),

                "author": plugin.get("author"),

                "category": plugin.get("category"),

                "commands": plugin.get("commands")

            })

        with open(

            "plugins.json",

            "w"

        ) as file:

            json.dump(

                data,

                file,

                indent=4

            )

        return "plugins.json"


    # ======================================
    # IMPORT SETTINGS
    # ======================================

    def import_settings(self, filename):

        if not os.path.exists(filename):

            return False

        with open(filename) as file:

            self.config = json.load(file)

        self.save_config()

        return True    # ======================================
    # PLUGIN UPDATE CHECKER
    # ======================================

    def update_plugin(self, plugin_name, new_file):

        if plugin_name not in self.plugins:

            return False

        import shutil

        destination = os.path.join(

            PLUGIN_FOLDER,

            plugin_name + ".py"

        )

        shutil.copy(new_file, destination)

        self.reload_plugin(plugin_name)

        self.log(plugin_name + " updated.")

        return True


    # ======================================
    # PLUGIN REPORT
    # ======================================

    def generate_report(self):

        report = []

        report.append("=" * 50)

        report.append("NITRON PLUGIN REPORT")

        report.append("=" * 50)

        report.append("")

        report.append("Total Plugins : " + str(len(self.plugins)))

        report.append("")

        for name in sorted(self.plugins):

            plugin = self.plugins[name]

            report.append("Plugin : " + name)

            report.append("Version : " + str(plugin.get("version","1.0")))

            report.append("Author : " + str(plugin.get("author","Unknown")))

            report.append("Category : " + str(plugin.get("category","General")))

            report.append("Enabled : " + str(plugin.get("enabled",True)))

            report.append("Commands :")

            for cmd in plugin.get("commands",[]):

                report.append("  - " + cmd)

            report.append("")

        filename = "plugin_report.txt"

        with open(filename,"w") as file:

            file.write("\n".join(report))

        return filename


    # ======================================
    # RESET MANAGER
    # ======================================

    def reset(self):

        self.plugins.clear()

        self.failed.clear()

        self.history.clear()

        self.disabled.clear()

        self.load_plugins()

        self.log("Plugin manager reset.")


    # ======================================
    # SHUTDOWN
    # ======================================

    def shutdown_manager(self):

        self.save_config()

        self.save_metrics()

        self.log("Plugin manager shutdown.")

        return True


    # ======================================
    # SUMMARY
    # ======================================

    def summary(self):

        print()

        print("========== NITRON ==========")

        print("Loaded Plugins :", len(self.plugins))

        print("Failed Plugins :", len(self.failed))

        print("Disabled Plugins :", len(self.disabled))

        print("Queue Size :", self.queue_size() if hasattr(self,"queue_size") else 0)

        print("============================")
