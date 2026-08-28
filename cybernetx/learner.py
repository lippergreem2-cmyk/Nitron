import os

COURSES = {
    "1": ("Python", "python"),
    "2": ("C++", "cpp"),
    "3": ("Java", "java"),
    "4": ("JavaScript", "javascript"),
    "5": ("Web Development", "web"),
    "6": ("Android / Kotlin", "android"),
    "7": ("Databases / SQL", "sql"),
    "8": ("Algorithms", "algorithms"),
    "9": ("AI / Machine Learning", "ai"),
    "10": ("Linux / Termux", "linux"),
    "11": ("Defensive Cybersecurity", "cybersecurity"),
}


def clear():
    os.system("clear")


def cpp_course():
    while True:
        clear()

        print("""
╔══════════════════════════════════════════════╗
║             CYBERNETX • C++                 ║
║              BEGINNER COURSE                ║
╚══════════════════════════════════════════════╝
""")

        print("[1] Lesson 1 — Your first C++ program")
        print("[2] Lesson 2 — Printing text")
        print("[3] Lesson 3 — Variables")
        print("[4] Lesson 4 — User input")
        print("[5] Back to Learning Lab")
        print()

        choice = input("C++ > ").strip()

        if choice == "1":
            cpp_lesson_1()
        elif choice == "2":
            cpp_lesson_2()
        elif choice == "3":
            cpp_lesson_3()
        elif choice == "4":
            cpp_lesson_4()
        elif choice == "5":
            return


def cpp_lesson_1():
    clear()

    print("""
╔══════════════════════════════════════════════╗
║              C++ — LESSON 1                 ║
║           YOUR FIRST PROGRAM                ║
╚══════════════════════════════════════════════╝

Step 1:

#include <iostream>

This gives your program access to input/output tools.

Step 2:

int main() {
}

This is where your program starts.

Your complete program is:

#include <iostream>

int main() {
}

Now try creating it yourself.
""")

    input("\nPress Enter to return to C++ lessons...")


def cpp_lesson_2():
    clear()

    print("""
╔══════════════════════════════════════════════╗
║              C++ — LESSON 2                 ║
║              PRINTING TEXT                  ║
╚══════════════════════════════════════════════╝

We can print text using:

std::cout

Example:

#include <iostream>

int main() {
    std::cout << "Hello, CybernetX!";
    return 0;
}

Your challenge:

Make the program print:

Hello, C++

Don't worry about the answer yet.
Try it yourself first.
""")

    input("\nPress Enter to return to C++ lessons...")


def cpp_lesson_3():
    clear()

    print("""
╔══════════════════════════════════════════════╗
║              C++ — LESSON 3                 ║
║                VARIABLES                   ║
╚══════════════════════════════════════════════╝

A variable stores information.

Example:

int age = 15;

Here:

int  = the type
age  = the variable name
15   = the value

Try creating:

int score = 100;

Then print score using std::cout.
""")

    input("\nPress Enter to return to C++ lessons...")


def cpp_lesson_4():
    clear()

    print("""
╔══════════════════════════════════════════════╗
║              C++ — LESSON 4                 ║
║                 INPUT                     ║
╚══════════════════════════════════════════════╝

C++ can receive information from the user.

Example:

int age;

std::cin >> age;

std::cin means:
"get input from the user."

Your challenge:

Ask the user for their age
and then print it.
""")

    input("\nPress Enter to return to C++ lessons...")


def show_courses():
    clear()

    print("""
╔══════════════════════════════════════════════╗
║                  CYBERNETX                  ║
║                LEARNING LAB                 ║
╚══════════════════════════════════════════════╝
""")

    print("Choose what you want to learn:\n")

    for number, (name, _) in COURSES.items():
        print(f"[{number}] {name}")

    print("[0] Exit")
    print()


def start_course(course):
    name, folder = COURSES[course]

    if folder == "cpp":
        cpp_course()
        return

    clear()

    print(f"""
╔══════════════════════════════════════════════╗
║              CYBERNETX LESSON              ║
╚══════════════════════════════════════════════╝

Course: {name}

This course is being prepared.
""")

    input("\nPress Enter to return to Learning Lab...")


def main():
    while True:
        show_courses()

        choice = input("CybernetX > ").strip()

        if choice == "0":
            clear()
            print("CybernetX Learning Lab closed.")
            return

        if choice in COURSES:
            start_course(choice)
        else:
            print("\nInvalid choice.")
            input("Press Enter to return...")


if __name__ == "__main__":
    main()
