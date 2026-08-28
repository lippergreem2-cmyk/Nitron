package com.nitron.bubble

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class CybernetXActivity : AppCompatActivity() {

    private lateinit var languageSpinner: Spinner
    private lateinit var lessonTitle: TextView
    private lateinit var lessonText: TextView
    private lateinit var codeEditor: EditText
    private lateinit var output: TextView
    private lateinit var progress: TextView

    private var lesson = 0

    private val lessons = listOf(
        Lesson(
            "C++ — Lesson 1",
            """
Learn your first C++ program.

C++ programs normally start with main().

The #include <iostream> line gives us access
to standard input and output.

Your goal:

Print:

Hello, CybernetX!
""".trimIndent(),
            """
#include <iostream>

int main() {
    std::cout << "Hello, CybernetX!";
    return 0;
}
""".trimIndent()
        ),

        Lesson(
            "C++ — Lesson 2",
            """
Learn variables.

A variable stores information.

Example:

int score = 100;

Your goal:

Create a variable called score
with the value 100 and print it.
""".trimIndent(),
            """
#include <iostream>

int main() {
    int score = 100;
    std::cout << score;
    return 0;
}
""".trimIndent()
        ),

        Lesson(
            "C++ — Lesson 3",
            """
Learn user input.

std::cin lets your program receive
information from the user.

Your goal:

Create an integer called age
and read an age from the user.
""".trimIndent(),
            """
#include <iostream>

int main() {
    int age;
    std::cin >> age;
    std::cout << age;
    return 0;
}
""".trimIndent()
        )
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_cybernetx)

        languageSpinner = findViewById(R.id.languageSpinner)
        lessonTitle = findViewById(R.id.lessonTitle)
        lessonText = findViewById(R.id.lessonText)
        codeEditor = findViewById(R.id.codeEditor)
        output = findViewById(R.id.output)
        progress = findViewById(R.id.progress)

        val languages = arrayOf(
            "C++",
            "Python",
            "Java",
            "JavaScript",
            "Kotlin",
            "SQL",
            "HTML / CSS",
            "Algorithms",
            "AI / Machine Learning",
            "Linux",
            "Defensive Cybersecurity"
        )

        languageSpinner.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            languages
        )

        findViewById<Button>(R.id.runButton).setOnClickListener {
            runCode()
        }

        findViewById<Button>(R.id.checkButton).setOnClickListener {
            checkAnswer()
        }

        findViewById<Button>(R.id.hintButton).setOnClickListener {
            showHint()
        }

        findViewById<Button>(R.id.nextButton).setOnClickListener {
            nextLesson()
        }

        loadLesson()
    }

    private fun loadLesson() {
        val current = lessons[lesson]

        lessonTitle.text = current.title
        lessonText.text = current.description
        codeEditor.setText(current.startingCode)

        progress.text =
            "Lesson ${lesson + 1} / ${lessons.size}"

        output.text =
            "Output will appear here..."
    }

    private fun runCode() {
        output.text =
            """
> CybernetX
> Code received.

This Android training screen is ready.
The next step is connecting the Run button
to your local compiler.
""".trimIndent()
    }

    private fun checkAnswer() {
        val code = codeEditor.text.toString()

        when (lesson) {

            0 -> {
                if (
                    code.contains("std::cout") &&
                    code.contains("Hello, CybernetX!")
                ) {
                    output.text =
                        "✓ Correct!\n\nYou successfully used std::cout."
                } else {
                    output.text =
                        "✗ Not quite.\n\nHint: use std::cout to print the required text."
                }
            }

            1 -> {
                if (
                    code.contains("int score") &&
                    code.contains("100") &&
                    code.contains("std::cout")
                ) {
                    output.text =
                        "✓ Correct!\n\nYou created and printed a variable."
                } else {
                    output.text =
                        "✗ Not quite.\n\nHint: create int score = 100; and print score."
                }
            }

            2 -> {
                if (
                    code.contains("int age") &&
                    code.contains("std::cin")
                ) {
                    output.text =
                        "✓ Correct!\n\nYou successfully used user input."
                } else {
                    output.text =
                        "✗ Not quite.\n\nHint: declare int age and use std::cin."
                }
            }
        }
    }

    private fun showHint() {
        output.text =
            when (lesson) {
                0 -> "Hint: std::cout is used to print text."
                1 -> "Hint: use int score = 100;"
                2 -> "Hint: use std::cin >> age;"
                else -> "Keep practicing!"
            }
    }

    private fun nextLesson() {
        if (lesson < lessons.size - 1) {
            lesson++
            loadLesson()
        } else {
            output.text =
                "🎉 Course section complete!\n\nMore CybernetX lessons can be added next."
        }
    }

    data class Lesson(
        val title: String,
        val description: String,
        val startingCode: String
    )
}
