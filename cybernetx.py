import os
import shutil
import subprocess
import tempfile

LANGUAGES = {
    "Python": {
        "file": "main.py",
        "check": "python",
        "run": lambda f: ["python", f],
    },
    "JavaScript": {
        "file": "main.js",
        "check": "node",
        "run": lambda f: ["node", f],
    },
    "TypeScript": {
        "file": "main.ts",
        "check": "ts-node",
        "run": lambda f: ["ts-node", f],
    },
    "C": {
        "file": "main.c",
        "check": "clang",
        "run": lambda f: ["sh", "-c", f"clang '{f}' -o '{f}.out' && '{f}.out'"],
    },
    "C++": {
        "file": "main.cpp",
        "check": "clang++",
        "run": lambda f: ["sh", "-c", f"clang++ '{f}' -o '{f}.out' && '{f}.out'"],
    },
    "Java": {
        "file": "Main.java",
        "check": "javac",
        "run": lambda f: ["sh", "-c", f"javac '{f}' && java -cp '{os.path.dirname(f)}' Main"],
    },
    "Kotlin": {
        "file": "Main.kt",
        "check": "kotlinc",
        "run": lambda f: ["kotlinc", f, "-include-runtime", "-d", f + ".jar"],
    },
    "Go": {
        "file": "main.go",
        "check": "go",
        "run": lambda f: ["go", "run", f],
    },
    "Rust": {
        "file": "main.rs",
        "check": "rustc",
        "run": lambda f: ["sh", "-c", f"rustc '{f}' -o '{f}.out' && '{f}.out'"],
    },
    "PHP": {
        "file": "main.php",
        "check": "php",
        "run": lambda f: ["php", f],
    },
    "Ruby": {
        "file": "main.rb",
        "check": "ruby",
        "run": lambda f: ["ruby", f],
    },
    "Perl": {
        "file": "main.pl",
        "check": "perl",
        "run": lambda f: ["perl", f],
    },
    "Bash": {
        "file": "main.sh",
        "check": "bash",
        "run": lambda f: ["bash", f],
    },
}


def clear():
    os.system("clear")


def available_languages():
    return [
        name
        for name, data in LANGUAGES.items()
        if shutil.which(data["check"])
    ]


def banner():
    print("""
╔══════════════════════════════════════════════╗
║                 CYBERNETX                   ║
╠══════════════════════════════════════════════╣
║          MULTI-LANGUAGE CODE PLATFORM       ║
╚══════════════════════════════════════════════╝
""")


def choose_language():
    available = available_languages()

    print("Available languages:\n")

    for i, language in enumerate(available, 1):
        print(f"  [{i}] {language}")

    print()
    choice = input("Select language: ").strip()

    try:
        index = int(choice) - 1
        return available[index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        input("Press Enter...")
        return None


def editor(language):
    data = LANGUAGES[language]

    clear()
    banner()

    print(f"Language: {language}")
    print(f"File:     {data['file']}")
    print()
    print("Enter your code.")
    print("Type END on its own line when finished.")
    print()

    lines = []

    while True:
        line = input("│ ")

        if line == "END":
            break

        lines.append(line)

    code = "\n".join(lines)

    if not code.strip():
        return

    with tempfile.TemporaryDirectory() as directory:

        filename = os.path.join(directory, data["file"])

        with open(filename, "w") as f:
            f.write(code)

        print()
        print("════════ OUTPUT ════════")

        try:
            command = data["run"](filename)

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.stdout:
                print(result.stdout)

            if result.stderr:
                print(result.stderr)

            print(f"\nExit code: {result.returncode}")

        except subprocess.TimeoutExpired:
            print("Program stopped: 30-second timeout.")

        except Exception as e:
            print("Execution error:", e)

        input("\nPress Enter to return...")


def main():
    while True:

        clear()
        banner()

        print("[1] Code")
        print("[2] Installed languages")
        print("[3] Exit")
        print()

        choice = input("CybernetX > ").strip()

        if choice == "1":

            language = choose_language()

            if language:
                editor(language)

        elif choice == "2":

            clear()
            banner()

            for language in available_languages():
                print("✓", language)

            input("\nPress Enter...")

        elif choice == "3":
            clear()
            print("CybernetX closed.")
            break


if __name__ == "__main__":
    main()
