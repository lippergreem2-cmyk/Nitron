from academy.mathematics import MathTeacher
from quiz.math_quiz import MathQuiz
from quiz.random_quiz import RandomMathQuiz
from quiz.progress import show_progress, recommendation
from quiz.study_tracker import StudyTracker
from quiz.tutor import PersonalTutor
from quiz.exam_system import ExamSystem


class LearningHub:

    def __init__(self):

        self.teacher = MathTeacher()

        self.quiz = MathQuiz()

        self.random = RandomMathQuiz()

        self.study = StudyTracker()

        self.tutor = PersonalTutor()

        self.exam = ExamSystem()

    def start(self):

        print()
        print("====================================")
        print("       NITRON LEARNING HUB")
        print("====================================")
        print("1. Teach Mathematics")
        print("2. Mathematics Quiz")
        print("3. Random Quiz")
        print("4. Study Progress")
        print("5. Study Timetable")
        print("6. Tutor Recommendation")
        print("7. Motivation")
        print("8. Report Cards")
        print("9. Average Score")
        print("0. Exit")
        print("====================================")

        while True:

            choice = input("\nChoose: ").strip()

            if choice == "1":

                topic = input("Topic: ")

                self.study.study_today()

                self.teacher.teach(topic)

            elif choice == "2":

                topic = input("Topic: ")

                self.study.study_today()

                self.quiz.start(topic)

            elif choice == "3":

                self.study.study_today()

                self.random.daily_quiz()

            elif choice == "4":

                print(show_progress())

                print()

                print(recommendation())

            elif choice == "5":

                self.study.timetable()

            elif choice == "6":

                print()

                print(self.tutor.recommend_subject())

                print()

                print(self.tutor.strongest_subject())

            elif choice == "7":

                print()

                print(self.tutor.motivate())

            elif choice == "8":

                self.exam.show_reports()

            elif choice == "9":

                print()

                print("Average Percentage:")

                print(self.exam.average(), "%")

            elif choice == "0":

                print()

                print("Leaving Learning Hub...")

                break

            else:

                print("Invalid option.")
