import os
import platform

def main():
    print("Nitron Project")
    print("Termux tool is running.")
    print("Python:", platform.python_version())
    print("System:", platform.system())

    home = os.path.expanduser("~")
    print("Home:", home)


if __name__ == "__main__":
    main()
