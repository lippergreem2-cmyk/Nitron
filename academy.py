# ~/Nitron/academy.py

try:
    from academy.python_teacher import ask_python
except:
    ask_python = None


try:
    from academy.cpp_teacher import ask_cpp
except:
    ask_cpp = None


def teach(subject, topic="topics"):

    subject = subject.lower()

    if subject == "python" and ask_python:
        return ask_python(topic)

    if subject in ["c++", "cpp"] and ask_cpp:
        return ask_cpp(topic)


    return f"I don't have the {subject} teacher yet."
