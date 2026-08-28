import os
import shutil
from datetime import datetime

CURRENT = os.getcwd()


def plugin():

    return {

        "name": "File Manager",

        "description": "Browse and manage files.",

        "commands": [

            "files",

            "file manager",

            "explorer"

        ],

        "run": run

    }


def help_menu():

    print("""

=========================
NITRON FILE MANAGER
=========================

Commands

help

pwd

ls

cd <folder>

mkdir <folder>

touch <file>

read <file>

write <file>

delete <file>

copy <source> <destination>

move <source> <destination>

rename <old> <new>

size <file>

info <file>

exit

""")


def list_files():

    for item in sorted(os.listdir(CURRENT)):

        print(item)


def run(command):

    global CURRENT

    help_menu()

    while True:

        cmd = input("Files> ").strip()

        if cmd == "":

            continue

        if cmd.lower() in ["exit","quit","back"]:

            return "Leaving File Manager."

        if cmd.lower() == "help":

            help_menu()

        elif cmd.lower() == "pwd":

            print(CURRENT)

        elif cmd.lower() == "ls":

            list_files()

        elif cmd.startswith("cd "):

            folder = cmd[3:].strip()

            new = os.path.join(CURRENT, folder)

            if os.path.isdir(new):

                CURRENT = os.path.abspath(new)

            else:

                print("Folder not found.")

        elif cmd.startswith("mkdir "):

            os.makedirs(os.path.join(CURRENT, cmd[6:].strip()), exist_ok=True)

            print("Folder created.")

        elif cmd.startswith("touch "):

            open(os.path.join(CURRENT, cmd[6:].strip()), "a").close()

            print("File created.")

        elif cmd.startswith("read "):

            try:

                with open(os.path.join(CURRENT, cmd[5:].strip()), "r") as f:

                    print(f.read())

            except Exception as e:

                print(e)

        elif cmd.startswith("write "):

            name = cmd[6:].strip()

            print("Enter text. Type END on its own line to save.")

            lines = []

            while True:

                line = input()

                if line == "END":

                    break

                lines.append(line)

            with open(os.path.join(CURRENT, name), "w") as f:

                f.write("\n".join(lines))

            print("Saved.")

        elif cmd.startswith("delete "):

            try:

                os.remove(os.path.join(CURRENT, cmd[7:].strip()))

                print("Deleted.")

            except Exception as e:

                print(e)

        elif cmd.startswith("copy "):

            try:

                args = cmd.split(maxsplit=2)

                shutil.copy(

                    os.path.join(CURRENT, args[1]),

                    os.path.join(CURRENT, args[2])

                )

                print("Copied.")

            except Exception as e:

                print(e)

        elif cmd.startswith("move "):

            try:

                args = cmd.split(maxsplit=2)

                shutil.move(

                    os.path.join(CURRENT, args[1]),

                    os.path.join(CURRENT, args[2])

                )

                print("Moved.")

            except Exception as e:

                print(e)

        elif cmd.startswith("rename "):

            try:

                args = cmd.split(maxsplit=2)

                os.rename(

                    os.path.join(CURRENT, args[1]),

                    os.path.join(CURRENT, args[2])

                )

                print("Renamed.")

            except Exception as e:

                print(e)

        elif cmd.startswith("size "):

            try:

                size = os.path.getsize(

                    os.path.join(CURRENT, cmd[5:].strip())

                )

                print(size, "bytes")

            except Exception as e:

                print(e)

        elif cmd.startswith("info "):

            try:

                file = os.path.join(CURRENT, cmd[5:].strip())

                print("Name:", os.path.basename(file))

                print("Size:", os.path.getsize(file), "bytes")

                print("Modified:", datetime.fromtimestamp(os.path.getmtime(file)))

            except Exception as e:

                print(e)

        else:

            print("Unknown command.")
