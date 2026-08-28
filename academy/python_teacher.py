"""
NITRON PYTHON TEACHER
=====================

This module is ONLY for teaching Python to the user.

Important:
    "learn python" is handled by commands.py / learning_manager.
    "teach me python" is handled here.

This prevents Nitron from confusing:
    learn python
with:
    teach me python
"""

from academy.academy import academy


class PythonTeacher:

    def __init__(self):
        self.subject = "python"

    # ----------------------------------------------------------
    # GET ONE LESSON
    # ----------------------------------------------------------

    def teach(self, lesson_number=1):

        try:
            lesson_number = int(lesson_number)
        except (TypeError, ValueError):
            lesson_number = 1

        lesson = academy.get_lesson(
            self.subject,
            lesson_number
        )

        if lesson is None:
            return {
                "message": (
                    f"I couldn't find Python lesson "
                    f"{lesson_number}."
                )
            }

        return {
            "title": lesson.get(
                "title",
                f"Python Lesson {lesson_number}"
            ),
            "explanation": lesson.get(
                "explanation",
                ""
            ),
            "code": lesson.get(
                "code",
                ""
            ),
            "output": lesson.get(
                "output",
                ""
            ),
            "practice": lesson.get(
                "practice",
                ""
            ),
            "quiz": lesson.get(
                "quiz",
                ""
            )
        }

    # ----------------------------------------------------------
    # LIST LESSONS
    # ----------------------------------------------------------

    def list_lessons(self):

        return academy.list_lessons(
            self.subject
        )

    # ----------------------------------------------------------
    # COUNT LESSONS
    # ----------------------------------------------------------

    def total_lessons(self):

        return academy.count(
            self.subject
        )


python_teacher = PythonTeacher()


# ==============================================================
# TEACHING INTERFACE
# ==============================================================

def ask_python(request="topics"):
    """
    Python teaching interface.

    Examples:

        teach me python
        teach python
        python lessons
        lesson 1
        lesson 2
        next lesson
    """

    command = str(request).strip().lower()

    # ----------------------------------------------------------
    # TEACH PYTHON
    # ----------------------------------------------------------

    teach_commands = (
        "",
        "topics",
        "topic",
        "lessons",
        "lesson list",
        "teach me python",
        "teach python",
        "start python lesson",
        "start learning python with me"
    )

    if command in teach_commands:

        lessons = python_teacher.list_lessons()

        if not lessons:

            return {
                "message":
                    "I don't have any Python lessons yet."
            }

        return {
            "message":
                "Let's learn Python together. "
                f"I have {len(lessons)} lessons. "
                "Here is Lesson 1.",
            "lesson":
                python_teacher.teach(1)
        }

    # ----------------------------------------------------------
    # NEXT LESSON
    # ----------------------------------------------------------

    if command in (
        "next",
        "next lesson",
        "continue",
        "continue python",
        "continue learning",
        "next python lesson"
    ):

        return {
            "message":
                "Let's continue with the next Python lesson."
        }

    # ----------------------------------------------------------
    # SPECIFIC LESSON
    # ----------------------------------------------------------

    if command.startswith("lesson "):

        value = command[len("lesson "):].strip()

        try:
            number = int(value)
        except ValueError:
            number = 1

        return {
            "message":
                f"Here is Python Lesson {number}.",
            "lesson":
                python_teacher.teach(number)
        }

    # ----------------------------------------------------------
    # PYTHON TOPIC REQUEST
    # ----------------------------------------------------------

    lessons = python_teacher.list_lessons()

    if lessons:

        return {
            "message":
                f"Let's study Python: {request}",
            "lesson":
                python_teacher.teach(1)
        }

    return {
        "message":
            "I don't have Python lessons available yet."
    }


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    print("NITRON PYTHON TEACHER TEST")
    print("=" * 50)

    print()
    print("Teaching request:")
    print(ask_python("teach me python"))

    print()
    print("Specific lesson:")
    print(ask_python("lesson 1"))
