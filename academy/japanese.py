LESSONS = {

    1: {
        "title": "Greetings",
        "words": [

            ("おはよう", "Ohayō", "Good morning"),
            ("こんにちは", "Konnichiwa", "Hello"),
            ("こんばんは", "Konbanwa", "Good evening"),
            ("ありがとう", "Arigatō", "Thank you"),
            ("さようなら", "Sayōnara", "Goodbye")

        ]
    }

}


def lesson(number):

    if number not in LESSONS:

        return "Lesson not found."

    data = LESSONS[number]

    text = ""

    text += f"Japanese Lesson {number}\n"
    text += f"{data['title']}\n\n"

    for japanese, pronunciation, english in data["words"]:

        text += f"Japanese: {japanese}\n"
        text += f"Pronunciation: {pronunciation}\n"
        text += f"Meaning: {english}\n\n"

    return text


def teach():

    return lesson(1)


if __name__ == "__main__":

    print(teach())
