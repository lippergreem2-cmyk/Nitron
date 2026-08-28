# ctf_tools.py

import base64
import hashlib


def ctf_help():

    menu = """
============================================================
NITRON CTF HELPER
============================================================

Available Commands

1. base64_encode <text>
2. base64_decode <text>
3. md5 <text>
4. sha1 <text>
5. sha256 <text>
6. help
7. exit

============================================================
"""

    print(menu)

    while True:

        cmd = input("CTF> ").strip()

        if cmd.lower() == "exit":
            print("Leaving CTF Helper...")
            break

        elif cmd.lower() == "help":
            print(menu)

        elif cmd.startswith("base64_encode "):

            text = cmd[14:]

            print(
                base64.b64encode(
                    text.encode()
                ).decode()
            )

        elif cmd.startswith("base64_decode "):

            text = cmd[14:]

            try:
                print(
                    base64.b64decode(
                        text
                    ).decode()
                )
            except Exception:
                print("Invalid Base64 string.")

        elif cmd.startswith("md5 "):

            text = cmd[4:]

            print(
                hashlib.md5(
                    text.encode()
                ).hexdigest()
            )

        elif cmd.startswith("sha1 "):

            text = cmd[5:]

            print(
                hashlib.sha1(
                    text.encode()
                ).hexdigest()
            )

        elif cmd.startswith("sha256 "):

            text = cmd[7:]

            print(
                hashlib.sha256(
                    text.encode()
                ).hexdigest()
            )

        else:
            print("Unknown command. Type help.")


if __name__ == "__main__":

    ctf_help()
