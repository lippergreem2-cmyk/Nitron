import random

QUIZZES = {

    "algebra": [

        {
            "question": "Solve x + 5 = 12",
            "answer": "7"
        },

        {
            "question": "Solve 2x = 20",
            "answer": "10"
        },

        {
            "question": "Simplify 3x + 4x",
            "answer": "7x"
        }

    ],

    "fractions": [

        {
            "question": "1/2 + 1/2 = ?",
            "answer": "1"
        },

        {
            "question": "3/4 + 1/4 = ?",
            "answer": "1"
        }

    ],

    "geometry": [

        {
            "question": "How many degrees are in a straight angle?",
            "answer": "180"
        },

        {
            "question": "How many sides does a pentagon have?",
            "answer": "5"
        }

    ]

}


class MathQuiz:

    def __init__(self):

        self.score = 0

        self.total = 0

    def start(self, topic):

        topic = topic.lower().strip()

        if topic not in QUIZZES:

            print("Topic not found.")

            return

        questions = QUIZZES[topic][:]

        random.shuffle(questions)

        self.score = 0

        self.total = len(questions)

        for q in questions:

            print()

            print(q["question"])

            answer = input("Answer: ").strip().lower()

            if answer == q["answer"].lower():

                print("Correct.")

                self.score += 1

            else:

                print("Wrong.")

                print("Correct answer:", q["answer"])

        print()

        print("Quiz Finished")

        print("Score:", self.score, "/", self.total)

        percentage = (self.score / self.total) * 100

        print("Percentage:", round(percentage, 1), "%")

        if percentage >= 80:

            print("Excellent.")

        elif percentage >= 50:

            print("Good. Keep practicing.")

        else:

            print("You should revise this topic.")
