from pathlib import Path
"""\nfrom pathlib import Path\nNitron Reasoning Engine\n"""

import re

from brain.memory import memory

try:
    from brain.knowledge_engine import knowledge
except ImportError:
    knowledge = None

try:
    from brain.learner import learner
except ImportError:
    learner = None

try:
    from brain.search_engine import search_engine
except ImportError:
    search_engine = None


class ReasoningEngine:

    def __init__(self):
        self.name = "Nitron Reasoning Engine"

    def analyze(self, command):
        """\n        Analyze a command and classify its intent.\n        """

        command = command.lower().strip()

        categories = {

            "academy": [
                "teach",
                "learn",
                "lesson",
                "academy",
                "study"
            ],

            "developer": [
                "build",
                "create",
                "generate",
                "project",
                "website",
                "app",
                "code",
                "program",
                "programming",
                "write",
                "modify",
                "debug",
                "test",
                "analyze"
            ],

            "trading": [
                "trade",
                "gold",
                "forex",
                "bitcoin",
                "crypto",
                "market"
            ],

            "weather": [
                "weather",
                "forecast"
            ],

            "music": [
                "music",
                "song",
                "play"
            ],

            "system": [
                "time",
                "date"
            ]
        }

        for category, words in categories.items():

            if any(word in command for word in words):
                return category

        return "chat"

    def explain(self, topic):
        """\n        Search the built-in knowledge base.\n        """

        if knowledge is None:
            return "Knowledge engine is unavailable."

        result = knowledge.get_category(topic)

        if result:
            return result

        return f"I don't know enough about '{topic}'."

    def search_learned(self, keyword):
        """\n        Find genuinely relevant learned knowledge.\n\n        Matching priority:\n            1. Exact topic\n            2. Topic contains the requested subject\n            3. Title contains the requested subject\n            4. Summary/content contains the subject\n\n        Common question words are ignored.\n        Unrelated learned topics must not be returned.\n        """

        if learner is None:
            return {}

        if not keyword:
            return {}

        text = str(keyword).lower().strip()

        stop_words = {
            "what", "what's", "whats",
            "is", "are", "am",
            "an", "a", "the",
            "tell", "me", "about",
            "explain", "describe",
            "who", "how", "why",
            "where", "when",
            "can", "you", "please",
            "do", "does", "did",
            "this", "that", "it",
            "to", "of", "for",
            "in", "on", "and"
        }

        words = re.findall(
            r"[a-zA-Z0-9_]+",
            text
        )

        words = [
            word
            for word in words
            if word not in stop_words
            and len(word) >= 2
        ]

        if not words:
            return {}

        results = {}

        # --------------------------------------------------
        # CAPABILITY INDEX
        #
        # Learned capabilities act as a routing signal.
        # The capability registry does not replace learned
        # knowledge; it helps us find the most relevant
        # learned topic.
        # --------------------------------------------------

        capability_matches = []

        try:

            from brain.skill_registry import find_for_task

            capability_matches = find_for_task(
                text
            )

        except Exception:

            capability_matches = []

        capability_topics = {}

        for capability in capability_matches:

            if not isinstance(
                capability,
                dict
            ):
                continue

            capability_name = str(
                capability.get("name", "")
            ).strip().lower()

            if capability_name:

                capability_topics[
                    capability_name
                ] = capability

        for topic, data in learner.knowledge.items():

            topic_text = str(topic).lower().strip()

            if isinstance(data, dict):

                title = str(
                    data.get("title", "")
                ).lower().strip()

                summary = data.get(
                    "summary",
                    ""
                )

                if not isinstance(summary, str):

                    old_content = data.get(
                        "content",
                        {}
                    )

                    if isinstance(old_content, dict):
                        summary = old_content.get(
                            "summary",
                            ""
                        )
                    else:
                        summary = str(old_content)

                summary_text = str(summary).lower()

            else:

                title = ""
                summary_text = str(data).lower()

            score = 0

            # --------------------------------------------------
            # CAPABILITY MATCHING
            #
            # A registered capability is strong evidence that
            # this learned topic is relevant to the request.
            # --------------------------------------------------

            capability = capability_topics.get(
                topic_text
            )

            if capability:

                confidence = float(
                    capability.get(
                        "confidence",
                        0
                    )
                )

                # A registered capability is strong evidence
                # that this exact learned topic is relevant.
                capability_words = re.findall(
                    r"[a-zA-Z0-9_]+",
                    topic_text
                )

                # Give capability matches a large base bonus.
                score += 300

                # Specific multi-word capabilities get a much
                # stronger bonus than broad capabilities such
                # as "python".
                if len(capability_words) > 1:
                    score += (
                        (len(capability_words) - 1)
                        * 500
                    )

                # Confidence still contributes to ranking.
                score += int(
                    60 * confidence
                )

            # --------------------------------------------------
            # TOPIC MATCHING
            # --------------------------------------------------

            exact_topic = False
            topic_match_count = 0

            for word in words:

                if word == topic_text:
                    score += 100
                    exact_topic = True

                elif word in topic_text:
                    score += 40
                    topic_match_count += 1

            # --------------------------------------------------
            # TITLE MATCHING
            # --------------------------------------------------

            for word in words:

                if word in title:
                    score += 20

            # --------------------------------------------------
            # CONTENT MATCHING
            # --------------------------------------------------

            for word in words:

                if word in summary_text:
                    score += 3

            # --------------------------------------------------
            # RELEVANCE GATE
            #
            # A learned topic must actually match the requested
            # subject. Content-only accidental matches are not
            # enough.
            # --------------------------------------------------

            if not exact_topic and topic_match_count == 0:

                title_match = any(
                    word in title
                    for word in words
                )

                if not title_match:
                    continue

            # --------------------------------------------------
            # QUALITY BONUS
            # --------------------------------------------------

            if title and summary_text.strip():
                score += 10

            if score > 0:

                results[topic] = {
                    "score": score,
                    "data": data
                }

        # Highest relevance first.

        if not results:
            return {}

        ranked = sorted(
            results.items(),
            key=lambda item: item[1]["score"],
            reverse=True
        )

        return dict(ranked)


    def _normalize_learned(self, topic, data):
        """\n        Convert learned knowledge into a clean answer.\n\n        Supports normal learned knowledge and structured image\n        knowledge without exposing raw OCR or sensitive text.\n        """

        if not isinstance(data, dict):
            return {
                "message": str(data),
                "learned": True,
                "topic": topic,
            }

        title = str(data.get("title", "")).strip()
        summary = str(data.get("summary", "")).strip()

        # ------------------------------------------------------
        # Older learner format
        # ------------------------------------------------------

        if not summary:
            content = data.get("content", {})

            if isinstance(content, dict):
                summary = str(
                    content.get("summary", "")
                ).strip()

                if not title:
                    title = str(
                        content.get("title", "")
                    ).strip()

            elif content:
                summary = str(content).strip()

        # ------------------------------------------------------
        # Structured image knowledge
        # ------------------------------------------------------

        sections = data.get("sections", {})

        if not isinstance(sections, dict):
            sections = {}

        image_metadata = sections.get(
            "image_metadata",
            {}
        )

        image_topics = sections.get(
            "topics",
            []
        )

        vision = sections.get(
            "vision",
            {}
        )

        research = sections.get(
            "research",
            {}
        )

        is_image = (
            "image_metadata" in sections
            or "topics" in sections
            or (
                isinstance(title, str)
                and title.lower().startswith(
                    "image analysis:"
                )
            )
        )

        if is_image:

            parts = []

            if summary:
                parts.append(summary)

            if image_topics:
                topic_list = [
                    str(item).strip()
                    for item in image_topics
                    if str(item).strip()
                ]

                if topic_list:
                    parts.append(
                        "Learned image topics: "
                        + ", ".join(topic_list)
                        + "."
                    )

            if isinstance(image_metadata, dict):

                width = image_metadata.get("width")
                height = image_metadata.get("height")
                image_format = image_metadata.get("format")

                if width and height:
                    parts.append(
                        f"Image dimensions: {width}x{height}."
                    )

                if image_format:
                    parts.append(
                        f"Image format: {image_format}."
                    )

            if isinstance(vision, dict):

                if vision.get("success"):
                    analysis = str(
                        vision.get("analysis", "")
                    ).strip()

                    if analysis:
                        parts.append(
                            "Vision analysis: "
                            + analysis[:1200]
                        )

                else:
                    parts.append(
                        "Detailed vision analysis was unavailable."
                    )

            if isinstance(research, dict):

                research_results = research.get(
                    "results",
                    []
                )

                if isinstance(research_results, list):
                    titles = []

                    for item in research_results[:5]:

                        if not isinstance(item, dict):
                            continue

                        title_text = str(
                            item.get("title", "")
                        ).strip()

                        if title_text:
                            titles.append(title_text)

                    if titles:
                        parts.append(
                            "Related public research: "
                            + "; ".join(titles)
                            + "."
                        )

            if parts:
                summary = " ".join(parts)

        # ------------------------------------------------------
        # Final fallback
        # ------------------------------------------------------

        if not summary:
            summary = (
                "I learned about "
                + str(topic)
                + "."
            )

        result = {
            "message": summary,
            "topic": topic,
            "learned": True,
        }

        if title:
            result["title"] = title

        if data.get("source"):
            result["source"] = data.get("source")

        if is_image:
            result["image_learned"] = True

            if image_topics:
                result["detected_topics"] = image_topics

            if image_metadata:
                result["image_metadata"] = image_metadata

            if research:
                result["research"] = research

        return result

    def _is_code_generation_request(self, question):
        """\n        Detect programming and software-development requests.\n\n        These requests are handled before learned knowledge so that\n        documentation does not override a request to create something.\n        """
        text = str(question).lower().strip()

        phrases = (
            "generate code",
            "write code",
            "create code",
            "make code",
            "give me code",
            "show me code",
            "provide code",
            "write a program",
            "create a program",
            "make a program",
            "build a program",
            "program this",
            "program it",
            "write a script",
            "create a script",
            "make a script",
            "build a script",
            "create an app",
            "create an application",
            "build an app",
            "build an application",
            "make an app",
            "make an application",
            "develop an app",
            "develop an application",
            "create a website",
            "create an website",
            "build a website",
            "build an website",
            "make a website",
            "develop a website",
            "create a web app",
            "create a web application",
            "build a web app",
            "build a web application",
            "create an ai",
            "build an ai",
            "make an ai",
            "create artificial intelligence",
            "build artificial intelligence",
            "python code",
            "javascript code",
            "java code",
            "kotlin code",
            "html code",
            "css code",
            "bash code",
            "shell script",
            "python program",
            "javascript program",
            "java program",
            "kotlin program",
            "calculator code",
            "calculator program",
            "coding project",
            "software project",
            "programming project",
        )

        if any(phrase in text for phrase in phrases):
            return True

        actions = (
            "generate",
            "write",
            "create",
            "build",
            "make",
            "develop",
            "program",
        )

        objects = (
            "code",
            "program",
            "script",
            "app",
            "application",
            "website",
            "web app",
            "web application",
            "ai",
            "software",
            "game",
            "video game",
            "pygame",
            "termux",
            "termux tool",
            "termux script",
            "cli",
            "command line",
        )

        return (
            any(word in text for word in actions)
            and any(word in text for word in objects)
        )

    def _detect_project_type(self, question):
        """Detect the type of software project requested."""

        text = str(question).lower().strip()

        if "website" in text:
            return "website"

        if "web app" in text or "web application" in text:
            return "web_app"

        if "android app" in text or "android application" in text:
            return "android_app"

        if "kotlin app" in text:
            return "android_app"

        if "api" in text:
            return "api"

        if "ai" in text or "artificial intelligence" in text:
            return "ai_project"

        if "calculator" in text:
            return "calculator"

        if "script" in text and "javascript" not in text:
            return "script"

        if (
            "game" in text
            or "video game" in text
            or "pygame" in text
        ):
            return "game"

        if (
            "termux" in text
            or "termux tool" in text
            or "termux script" in text
        ):
            return "termux_tool"

        if "desktop app" in text or "desktop application" in text:
            return "desktop_app"

        if "cli" in text or "command line" in text:
            return "cli_tool"

        if "program" in text:
            return "program"

        if "python" in text:
            return "python_program"

        return "software_project"

    def _detect_language(self, question):
        """Detect the requested programming language."""

        text = str(question).lower().strip()

        languages = (
            ("python", "python"),
            ("javascript", "javascript"),
            ("typescript", "typescript"),
            ("kotlin", "kotlin"),
            ("java", "java"),
            ("html", "html"),
            ("css", "css"),
            ("bash", "bash"),
            ("shell", "bash"),
            ("c++", "cpp"),
            ("c#", "csharp"),
            ("rust", "rust"),
            ("go", "go"),
        )

        for keyword, language in languages:
            if keyword in text:
                return language

        return None

    def _extract_project_name(self, question):
        """Extract a clean project name from a natural-language request."""
        text = str(question).strip()
        lower = text.lower()

        markers = (
            " called ",
            " named ",
            " name ",
        )

        stop_phrases = (
            ". use ",
            ". using ",
            ". with ",
            ". in ",
            ". generate ",
            ". create ",
            ". make ",
            " use ",
            " using ",
            " with ",
            " generate ",
            " create ",
            " make ",
        )

        for marker in markers:
            position = lower.find(marker)

            if position < 0:
                continue

            name_start = position + len(marker)
            name = text[name_start:].strip()
            name_lower = name.lower()

            cut_positions = []

            for phrase in stop_phrases:
                cut = name_lower.find(phrase)
                if cut >= 0:
                    cut_positions.append(cut)

            if cut_positions:
                name = name[:min(cut_positions)].strip()

            name = name.rstrip(" .!?,")

            if name:
                return name

        return "Nitron Project"

    def _build_project_plan(self, question):
        """Build a structured plan for a software project."""

        project_type = self._detect_project_type(question)
        language = self._detect_language(question)
        name = self._extract_project_name(question)

        # Sensible defaults when the user does not specify a language.
        if language is None:
            defaults = {
                "website": "html",
                "web_app": "javascript",
                "android_app": "kotlin",
                "calculator": "python",
                "game": "python",
                "termux_tool": "python",
                "script": "python",
                "cli_tool": "python",
                "desktop_app": "python",
                "ai_project": "python",
                "api": "python",
                "python_program": "python",
            }

            language = defaults.get(project_type, "python")

        return {
            "generated": True,
            "project_type": project_type,
            "language": language,
            "name": name,
            "files": [],
        }

    def _generate_project_files(self, plan):
        """Generate starter files for a structured project."""

        project_type = plan.get("project_type")
        language = plan.get("language")
        name = plan.get("name", "Nitron Project")

        files = []

        if project_type == "website":
            files = [
                {
                    "path": "index.html",
                    "content": f"""<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{name}</title>\n    <link rel="stylesheet" href="style.css">\n</head>\n<body>\n    <main>\n        <h1>{name}</h1>\n        <p>Welcome to {name}.</p>\n    </main>\n    <script src="script.js"></script>\n</body>\n</html>\n"""
                },
                {
                    "path": "style.css",
                    "content": """body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 40px;\n}\n\nmain {\n    max-width: 900px;\n    margin: auto;\n}\n"""
                },
                {
                    "path": "script.js",
                    "content": f"""console.log("{name} loaded.");\n"""
                },
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nWebsite generated by Nitron.\n\nOpen index.html in a web browser.\n"""
                }
            ]

        elif project_type == "web_app":
            files = [
                {
                    "path": "index.html",
                    "content": f"""<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>{name}</title>\n    <link rel="stylesheet" href="style.css">\n</head>\n<body>\n    <main id="app">\n        <h1>{name}</h1>\n        <p>Your web app is ready.</p>\n        <button id="actionButton">Click me</button>\n        <p id="output"></p>\n    </main>\n    <script src="script.js"></script>\n</body>\n</html>\n"""
                },
                {
                    "path": "style.css",
                    "content": """body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 40px;\n}\n\n#app {\n    max-width: 900px;\n    margin: auto;\n}\n\nbutton {\n    padding: 10px 20px;\n    cursor: pointer;\n}\n"""
                },
                {
                    "path": "script.js",
                    "content": f"""const button = document.getElementById("actionButton");\nconst output = document.getElementById("output");\n\nbutton.addEventListener("click", () => {{\n    output.textContent = "{name} is working!";\n}});\n"""
                },
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nWeb application generated by Nitron.\n\nOpen index.html in a web browser.\n"""
                }
            ]

        elif project_type == "calculator":
            files = [
                {
                    "path": "main.py",
                    "content": f"""# {name}\n# Generated by Nitron\n\ndef calculator():\n    print("{name}")\n    print("1. Add")\n    print("2. Subtract")\n    print("3. Multiply")\n    print("4. Divide")\n\n    first = float(input("First number: "))\n    operator = input("Operation (+, -, *, /): ")\n    second = float(input("Second number: "))\n\n    if operator == "+":\n        result = first + second\n    elif operator == "-":\n        result = first - second\n    elif operator == "*":\n        result = first * second\n    elif operator == "/":\n        if second == 0:\n            print("Cannot divide by zero.")\n            return\n        result = first / second\n    else:\n        print("Unknown operation.")\n        return\n\n    print("Result:", result)\n\n\nif __name__ == "__main__":\n    calculator()\n"""
                },
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nPython calculator generated by Nitron.\n\nRun:\n\npython main.py\n"""
                }
            ]

        elif project_type == "game":
            if language == "python":
                files = [
                    {
                        "path": "main.py",
                        "content": f"""# {name}\n# Python game generated by Nitron\n\nimport random\n\ndef play_game():\n    print("{name}")\n    print("Guess the number!")\n\n    target = random.randint(1, 10)\n\n    while True:\n        try:\n            guess = int(input("Choose a number from 1 to 10: "))\n        except ValueError:\n            print("Please enter a number.")\n            continue\n\n        if guess == target:\n            print("You win!")\n            break\n\n        if guess < target:\n            print("Too low.")\n        else:\n            print("Too high.")\n\n\nif __name__ == "__main__":\n    play_game()\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nPython game generated by Nitron.\n\nRun:\n\npython main.py\n"""
                    }
                ]
            else:
                files = [
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nGame project generated by Nitron.\n\nLanguage: {language}\n"""
                    }
                ]

        elif project_type == "termux_tool":
            if language in ("bash", "shell"):
                files = [
                    {
                        "path": "nitron_tool.sh",
                        "content": f"""#!/data/data/com.termux/files/usr/bin/bash\n# {name}\n# Termux tool generated by Nitron\n\necho "{name}"\necho "Termux tool is running."\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nTermux tool generated by Nitron.\n\nRun:\n\nchmod +x nitron_tool.sh\n./nitron_tool.sh\n"""
                    }
                ]
            else:
                files = [
                    {
                        "path": "main.py",
                        "content": f"""#!/usr/bin/env python3\n# {name}\n# Termux tool generated by Nitron\n\nimport os\nimport platform\n\ndef main():\n    print("{name}")\n    print("Termux tool is running.")\n    print("Python:", platform.python_version())\n    print("System:", platform.system())\n\n    home = os.path.expanduser("~")\n    print("Home:", home)\n\n\nif __name__ == "__main__":\n    main()\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nTermux tool generated by Nitron.\n\nRun:\n\npython main.py\n"""
                    }
                ]

        elif project_type == "program":
            if language == "python":
                files = [
                    {
                        "path": "main.py",
                        "content": f"""# {name}\n# Generated by Nitron\n\ndef main():\n    print("{name} is running.")\n\n\nif __name__ == "__main__":\n    main()\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nPython program generated by Nitron.\n\nRun:\n\npython main.py\n"""
                    }
                ]

            elif language == "javascript":
                files = [
                    {
                        "path": "index.js",
                        "content": f"""// {name}\n// Generated by Nitron\n\nfunction main() {{\n    console.log("{name} is running.");\n}}\n\nmain();\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nJavaScript program generated by Nitron.\n\nRun:\n\nnode index.js\n"""
                    }
                ]

            elif language == "kotlin":
                files = [
                    {
                        "path": "Main.kt",
                        "content": f"""// {name}\n// Generated by Nitron\n\nfun main() {{\n    println("{name} is running.")\n}}\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nKotlin program generated by Nitron.\n"""
                    }
                ]

            elif language == "java":
                files = [
                    {
                        "path": "Main.java",
                        "content": f"""// {name}\n// Generated by Nitron\n\npublic class Main {{\n    public static void main(String[] args) {{\n        System.out.println("{name} is running.");\n    }}\n}}\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nJava program generated by Nitron.\n"""
                    }
                ]

            elif language == "bash":
                files = [
                    {
                        "path": "main.sh",
                        "content": f"""#!/usr/bin/env bash\n# {name}\n# Generated by Nitron\n\necho "{name} is running."\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nBash program generated by Nitron.\n\nRun:\n\nchmod +x main.sh\n./main.sh\n"""
                    }
                ]

            elif language == "rust":
                files = [
                    {
                        "path": "main.rs",
                        "content": f"""// {name}\n// Generated by Nitron\n\nfn main() {{\n    println!("{name} is running.");\n}}\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nRust program generated by Nitron.\n\nRun:\n\nrustc main.rs -o main\n./main\n"""
                    }
                ]

            elif language == "go":
                files = [
                    {
                        "path": "main.go",
                        "content": f"""package main\n\nimport "fmt"\n\n// {name}\n// Generated by Nitron\n\nfunc main() {{\n    fmt.Println("{name} is running.")\n}}\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nGo program generated by Nitron.\n\nRun:\n\ngo run main.go\n"""
                    }
                ]

            elif language == "typescript":
                files = [
                    {
                        "path": "main.ts",
                        "content": f"""// {name}\n// Generated by Nitron\n\nfunction main(): void {{\n    console.log("{name} is running.");\n}}\n\nmain();\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nTypeScript program generated by Nitron.\n"""
                    }
                ]

            elif language == "cpp":
                files = [
                    {
                        "path": "main.cpp",
                        "content": f"""#include <iostream>\n\nint main() {{\n    std::cout << "{name} is running." << std::endl;\n    return 0;\n}}\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nC++ program generated by Nitron.\n\nRun:\n\ng++ main.cpp -o main\n./main\n"""
                    }
                ]

            elif language == "csharp":
                files = [
                    {
                        "path": "Program.cs",
                        "content": f"""using System;\n\nclass Program\n{{\n    static void Main()\n    {{\n        Console.WriteLine("{name} is running.");\n    }}\n}}\n"""
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nC# program generated by Nitron.\n"""
                    }
                ]

            else:
                # Generic fallback for a learned programming language.
                # Never reduce a learned programming capability to
                # README-only output.
                safe_language = str(language).strip().lower()

                extension_map = {{
                    "ruby": "rb",
                    "php": "php",
                    "swift": "swift",
                    "perl": "pl",
                    "lua": "lua",
                    "dart": "dart",
                    "scala": "scala",
                }}

                extension = extension_map.get(
                    safe_language,
                    "txt"
                )

                source_name = (
                    "main."
                    + extension
                )

                files = [
                    {
                        "path": source_name,
                        "content": (
                            f"// {name}\n"
                            f"// Generated by Nitron\n"
                            f"// Language: {language}\n\n"
                            f"// Starter source generated for "
                            f"{language}.\n"
                        )
                    },
                    {
                        "path": "README.md",
                        "content": f"""# {name}\n\nProgram generated by Nitron.\n\nLanguage: {language}\n\nSource file: {source_name}\n"""
                    }
                ]

        elif language == "python":
            files = [
                {
                    "path": "main.py",
                    "content": f"""# {name}\n# Generated by Nitron\n\ndef main():\n    print("{name} is running.")\n\n\nif __name__ == "__main__":\n    main()\n"""
                },
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nPython project generated by Nitron.\n\nRun:\n\npython main.py\n"""
                }
            ]

        elif language == "javascript":
            files = [
                {
                    "path": "index.js",
                    "content": f"""// {name}\n// Generated by Nitron\n\nfunction main() {{\n    console.log("{name} is running.");\n}}\n\nmain();\n"""
                },
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nJavaScript project generated by Nitron.\n\nRun:\n\nnode index.js\n"""
                }
            ]

        elif project_type == "android_app":
            files = [
                {
                    "path": "MainActivity.kt",
                    "content": f"""package com.example.nitron\n\nimport android.os.Bundle\nimport androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {{\n\n    override fun onCreate(savedInstanceState: Bundle?) {{\n        super.onCreate(savedInstanceState)\n    }}\n}}\n"""
                },
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nAndroid application generated by Nitron.\n\nLanguage: Kotlin\n"""
                }
            ]

        else:
            files = [
                {
                    "path": "README.md",
                    "content": f"""# {name}\n\nProject generated by Nitron.\n\nProject type: {project_type}\nLanguage: {language}\n"""
                }
            ]

        return files

    def generate_project(self, question, output_dir=None):
        """Generate a project and write all files to disk."""

        question = str(question).strip()

        plan = self._build_project_plan(question)
        files = self._generate_project_files(plan)

        if output_dir is None:
            safe_name = plan.get("name", "Nitron Project")

            safe_name = "".join(
                character
                if character.isalnum() or character in "._-"
                else "_"
                for character in safe_name
            ).strip("_")

            if not safe_name:
                safe_name = "Nitron_Project"

            base_dir = (
                Path.home()
                / "Nitron"
                / "generated_projects"
            )

            output_dir = base_dir / safe_name

            # Avoid overwriting an existing generated project.
            counter = 2

            while output_dir.exists():
                output_dir = base_dir / f"{safe_name}_{counter}"
                counter += 1

        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        written_files = []

        for item in files:
            file_path = output_dir / item["path"]

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            file_path.write_text(
                item["content"],
                encoding="utf-8"
            )

            written_files.append(str(file_path))

        return {
            "success": True,
            "generated": True,
            "project_type": plan.get("project_type"),
            "language": plan.get("language"),
            "name": plan.get("name"),
            "directory": str(output_dir),
            "files": files,
            "written_files": written_files
        }

    def _generate_code(self, question):
        """\n        Generate simple programming examples locally.\n        """

        text = str(question).lower().strip()

        if "calculator" in text and "python" in text:

            calculator_code = '''def calculator():
    print("Simple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    first = float(input("Enter the first number: "))
    operator = input("Enter an operation (+, -, *, /): ")
    second = float(input("Enter the second number: "))

    if operator == "+":
        result = first + second

    elif operator == "-":
        result = first - second

    elif operator == "*":
        result = first * second

    elif operator == "/":
        if second == 0:
            print("Cannot divide by zero.")
            return

        result = first / second

    else:
        print("Unknown operation.")
        return

    print("Result:", result)


calculator()
'''

            return {
                "message": (
                    "Here is a simple Python calculator.\n\n"
                    "```python\n"
                    + calculator_code
                    + "```"
                ),
                "topic": "python calculator",
                "generated": True,
                "language": "python"
            }

        if "python" in text:
            return {
                "message": (
                    "I can generate Python code for that. "
                    "Tell me what you want the program to do."
                ),
                "generated": True,
                "language": "python"
            }

        return {
            "message": (
                "I can generate code for that. "
                "Tell me the programming language and what you want the program to do."
            ),
            "generated": True
        }


    def _record_skill_success(self, skill, project):
        """Increase confidence after a successful project generation."""

        if not skill or not isinstance(skill, dict):
            return skill

        try:
            from brain.skill_registry import register

            name = skill.get("name")
            if not name:
                return skill

            old_confidence = float(
                skill.get("confidence", 0.0)
            )

            new_confidence = min(
                1.0,
                old_confidence + 0.10
            )

            project_type = str(
                project.get("project_type", "")
            )

            language = str(
                project.get("language", "")
            )

            evidence = [
                "successful project generation",
                f"project_type:{project_type}",
                f"language:{language}",
            ]

            return register(
                name=name,
                description=skill.get(
                    "description",
                    ""
                ),
                abilities=skill.get(
                    "abilities",
                    []
                ),
                prerequisites=skill.get(
                    "prerequisites",
                    []
                ),
                confidence=new_confidence,
                evidence=(
                    skill.get("evidence", [])
                    + evidence
                ),
                handlers=skill.get(
                    "handlers",
                    []
                ),
            )

        except Exception:
            return skill


    def answer(self, question):
        """\n        Answer a question using this priority:\n\n        1. Relevant learned knowledge\n        2. Built-in knowledge\n        3. Automatic web learning\n        4. Internal search fallback\n        """

        question = str(question).strip()

        # ==================================================
        # 0. INTELLIGENT CAPABILITY ROUTING
        # ==================================================
        # Decide what the user actually wants BEFORE allowing
        # a learned capability to intercept the request.
        #
        # Knowledge questions about Python must remain knowledge
        # questions. They must not be sent to the programming
        # operation handler merely because "Python" is a learned
        # programming capability.
        # ==================================================

        explicit_learn_command = bool(
            re.match(
                r"^learn\\s+.+$",
                question,
                re.IGNORECASE
            )
        )

        knowledge_question = bool(
            re.match(
                r"^(how|what|why|when|where|who|which|"
                r"can you explain|could you explain|"
                r"tell me about|describe)\\b",
                question,
                re.IGNORECASE
            )
        )

        explicit_explanation = bool(
            re.match(
                r"^(explain|describe|tell me about|"
                r"what is|what are|how does|how do|"
                r"why does|why do)\\b",
                question,
                re.IGNORECASE
            )
        )

        # Only treat a request as programming when it contains
        # an actual programming action.
        programming_action = self._is_code_generation_request(
            question
        )

        # ==================================================
        # LEARNED CAPABILITY EXECUTION
        # ==================================================
        # Never allow a programming capability to intercept a
        # normal knowledge/explanation question.
        # ==================================================

        try:
            from brain.skill_registry import best_for_task

            learned_skill = None

            if (
                not explicit_learn_command
                and not knowledge_question
                and not explicit_explanation
                and programming_action
            ):
                learned_skill = best_for_task(question)

            if learned_skill:
                learned_handlers = learned_skill.get(
                    "handlers",
                    []
                )

                learned_type = str(
                    learned_skill.get(
                        "capability_type",
                        ""
                    )
                ).lower()

                if (
                    learned_handlers
                    and "learned.programming" in learned_handlers
                    and programming_action
                ):
                    from brain.skill_handlers import learned_programming

                    return learned_programming(question)

                if (
                    learned_handlers
                    and "learned.knowledge" in learned_handlers
                ):
                    from brain.skill_handlers import learned_knowledge

                    return learned_knowledge(question)

                if (
                    learned_type in {
                        "framework",
                        "language",
                    }
                    and programming_action
                ):
                    return {
                        "module": "learned",
                        "action": "capability",
                        "skill": learned_skill.get(
                            "name",
                            ""
                        ),
                        "handlers": learned_handlers,
                        "confidence": learned_skill.get(
                            "confidence",
                            0
                        ),
                        "capability_type": learned_type,
                    }

        except Exception:
            pass

        # ==================================================
        # 0B. CODE GENERATION
        # ==================================================
        # Explicit programming requests go through the normal
        # project/code generation pipeline.
        # ==================================================

        # ==================================================
        # 1. EXPLICIT CAPABILITY LEARNING
        # ==================================================
        # "learn X" means explicitly learn X and register it
        # as a reusable Nitron capability.
        # This must run BEFORE learned/built-in knowledge so
        # existing answers cannot intercept the command.
        # ==================================================

        learn_match = re.match(
            r"^learn\s+(?:about\s+)?(.+?)\??$",
            question,
            re.IGNORECASE
        )

        if learn_match:

            learn_topic = learn_match.group(1).strip(
                " ?.! "
            )

            if not learn_topic:

                return {
                    "message":
                        "I need a topic to learn about."
                }

            try:

                from brain.study import study_engine
                import requests
                import urllib.parse

                # --------------------------------------------------
                # Search Wikipedia for several candidates.
                #
                # Do not blindly accept the first result. Wikipedia
                # often returns a broad parent topic for specialized
                # subjects such as "Python decorators".
                # --------------------------------------------------

                api_url = (
                    "https://en.wikipedia.org/w/api.php?"
                    + urllib.parse.urlencode({
                        "action": "query",
                        "format": "json",
                        "list": "search",
                        "srsearch": learn_topic,
                        "srlimit": 10,
                        "utf8": 1
                    })
                )

                response = requests.get(
                    api_url,
                    headers={
                        "User-Agent": "Nitron/1.0"
                    },
                    timeout=10
                )

                response.raise_for_status()

                data = response.json()

                results = data.get(
                    "query",
                    {}
                ).get(
                    "search",
                    []
                )

                if not results:

                    return {
                        "message":
                            f"I could not find reliable information about {learn_topic}.",
                        "learned": False,
                        "topic": learn_topic
                    }

                # --------------------------------------------------
                # Choose the most relevant article.
                # Exact title matches receive the highest score.
                # Multi-word title matches are preferred over broad
                # parent articles.
                # --------------------------------------------------

                requested_words = set(
                    re.findall(
                        r"[a-zA-Z0-9_]+",
                        learn_topic.lower()
                    )
                )

                def wikipedia_score(result):

                    title = str(
                        result.get("title", "")
                    ).strip()

                    title_lower = title.lower()

                    title_words = set(
                        re.findall(
                            r"[a-zA-Z0-9_]+",
                            title_lower
                        )
                    )

                    requested_lower = learn_topic.lower().strip()
                    score = 0

                    # Exact title match gets maximum priority.
                    if title_lower == requested_lower:
                        score += 2000

                    # Wikipedia often uses a singular canonical title
                    # when the user asks for a plural subject.
                    # Example: "black holes" -> "Black hole".
                    canonical_requested = requested_lower
                    if canonical_requested.endswith("s"):
                        canonical_requested = canonical_requested[:-1]

                    if title_lower == canonical_requested:
                        score += 1800

                    # Exact requested phrase in title.
                    if requested_lower in title_lower:
                        score += 300

                    # Requested-word overlap.
                    score += (
                        len(
                            requested_words
                            & title_words
                        )
                        * 100
                    )

                    # Small specificity bonus.
                    score += min(
                        len(title_words),
                        10
                    )

                    # Penalize obvious list/specialized articles when
                    # the requested topic is a broad subject.
                    specialized_markers = {
                        "list",
                        "fiction",
                        "thermodynamics",
                        "cosmology",
                        "calcutta",
                        "sun",
                    }

                    if title_words & specialized_markers:
                        score -= 250

                    return score

                # --------------------------------------------------
                # Prefer an article whose title actually represents
                # the requested subject.
                #
                # Broad parent articles such as:
                #   "Outline of the Python programming language"
                #
                # must not beat a specific article merely because
                # they contain the word "Python".
                # --------------------------------------------------

                ranked_results = sorted(
                    results,
                    key=wikipedia_score,
                    reverse=True
                )

                print(
                    "Wikipedia candidates:"
                )

                for candidate in ranked_results:
                    print(
                        " -",
                        candidate.get("title", ""),
                        "| score:",
                        wikipedia_score(candidate)
                    )
                # --------------------------------------------------
                # FINAL WIKIPEDIA SELECTION
                # The ranking scorer is authoritative.
                # Do not override a canonical article merely because
                # the requested phrase appears inside another title.
                # Example: "black holes" -> "Black hole".
                # --------------------------------------------------
                best_result = ranked_results[0]



                print(
                    "Selected:",
                    best_result.get(
                        "title",
                        learn_topic
                    )
                )

                title = best_result.get(
                    "title",
                    learn_topic
                )

                article_url = (
                    "https://en.wikipedia.org/wiki/"
                    + urllib.parse.quote(
                        title.replace(" ", "_")
                    )
                )

                print(
                    "Wikipedia candidates:"
                )

                for candidate in sorted(
                    results,
                    key=wikipedia_score,
                    reverse=True
                )[:5]:

                    print(
                        " -",
                        candidate.get("title"),
                        "| score:",
                        wikipedia_score(candidate)
                    )

                print(
                    "Selected:",
                    title
                )

                print("=" * 50)
                print("NITRON EXPLICIT CAPABILITY LEARNING")
                print("=" * 50)
                print("DEBUG SELECTED TITLE:", repr(title))
                print("DEBUG ARTICLE URL:", repr(article_url))
                print(f"Topic : {learn_topic}")
                print(f"Source: {article_url}")
                print()

                learned_result = study_engine.study(
                    learn_topic,
                    article_url
                )

                if not isinstance(
                    learned_result,
                    dict
                ):
                    learned_result = {
                        "status": "error",
                        "summary": str(learned_result)
                    }

                if learned_result.get(
                    "status"
                ) != "success":

                    return {
                        "message": (
                            "I found the topic, but learning failed: "
                            + str(
                                learned_result.get(
                                    "summary",
                                    "unknown error"
                                )
                            )
                        ),
                        "learned": False,
                        "topic": learn_topic,
                        "source": article_url
                    }

                # --------------------------------------------------
                # Register the learned topic as a reusable capability.
                # --------------------------------------------------

                capability_result = None

                try:

                    from brain.learner import learn_and_register

                    description = (
                        learned_result.get(
                            "summary",
                            ""
                        )
                        or f"Learned knowledge about {learn_topic}."
                    )

                    capability_result = learn_and_register(
                        topic=learn_topic,
                        description=description,
                        abilities=[
                            f"understand {learn_topic}",
                            f"work with {learn_topic}",
                            f"answer questions about {learn_topic}"
                        ],
                        evidence=[
                            article_url
                        ]
                    )

                    print(
                        f"[Capability] Registered: {learn_topic}"
                    )

                except Exception as capability_error:

                    print(
                        "[Capability] Registration warning: "
                        f"{capability_error}"
                    )

                # --------------------------------------------------
                # --------------------------------------------------
                # Return the freshly learned Wikipedia result.
                # Do NOT recall the old topic entry here because it
                # may contain stale metadata/title from an earlier learn.
                # --------------------------------------------------
                fresh = learner.recall(learn_topic) if learner else None

                if fresh:
                    result = self._normalize_learned(
                        learn_topic,
                        fresh
                    )

                    # Preserve the Wikipedia article selected for this
                    # learning operation instead of stale title metadata.
                    result["title"] = title
                    result["source"] = article_url
                    result["learned"] = True
                    result["capability_registered"] = (
                        capability_result is not None
                    )

                    return result

                summary = learned_result.get(
                    "summary",
                    ""
                )

                return {
                    "message": summary
                    or f"I learned about {learn_topic}.",
                    "topic": learn_topic,
                    "source": article_url,
                    "learned": True,
                    "capability_registered": (
                        capability_result is not None
                    )
                }

            except Exception as error:

                return {
                    "message": (
                        "I could not complete learning for "
                        f"{learn_topic}: {error}"
                    ),
                    "topic": learn_topic,
                    "learned": False
                }

        # ==================================================
        # 2. LEARNED KNOWLEDGE
        # ==================================================

        learned = self.search_learned(question)

        if learned:

            topic = next(iter(learned))

            return self._normalize_learned(
                topic,
                learned[topic]["data"]
                if isinstance(learned[topic], dict)
                and "data" in learned[topic]
                else learned[topic]
            )

        # ==================================================
        # 2. BUILT-IN KNOWLEDGE
        # ==================================================

        if knowledge:

            try:

                built_in = knowledge.get_category(
                    question
                )

                if built_in:
                    return built_in

            except Exception:
                pass

        # ==================================================
        # 3. AUTOMATIC WEB LEARNING
        # ==================================================

        try:

            from brain.study import study_engine

            import requests
            import urllib.parse

            # ----------------------------------------------
            # Extract the actual subject from the question
            # ----------------------------------------------

            search_text = question.strip()

            patterns = [
                r"^learn\s+about\s+(.+?)\??$",
                r"^learn\s+(.+?)\??$",
                r"^what\s+is\s+(.+?)\??$",
                r"^what\s+are\s+(.+?)\??$",
                r"^who\s+is\s+(.+?)\??$",
                r"^who\s+are\s+(.+?)\??$",
                r"^tell\s+me\s+about\s+(.+?)\??$",
                r"^explain\s+(.+?)\??$",
                r"^describe\s+(.+?)\??$"
            ]

            for pattern in patterns:

                match = re.match(
                    pattern,
                    search_text,
                    re.IGNORECASE
                )

                if match:

                    search_text = match.group(
                        1
                    ).strip()

                    break

            search_text = search_text.strip(" ?.!")

            if not search_text:
                return {
                    "message":
                        "I need a topic to learn about."
                }

            # ----------------------------------------------
            # Search Wikipedia for the subject
            # ----------------------------------------------

            api_url = (
                "https://en.wikipedia.org/w/api.php?"
                + urllib.parse.urlencode({
                    "action": "query",
                    "format": "json",
                    "list": "search",
                    "srsearch": search_text,
                    "srlimit": 1
                })
            )

            response = requests.get(
                api_url,
                headers={
                    "User-Agent": "Nitron/1.0"
                },
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            results = data.get(
                "query",
                {}
            ).get(
                "search",
                []
            )

            if results:

                title = results[0].get(
                    "title",
                    search_text
                )

                article_url = (
                    "https://en.wikipedia.org/wiki/"
                    + urllib.parse.quote(
                        title.replace(" ", "_")
                    )
                )

                print("=" * 50)
                print("NITRON AUTOMATIC LEARNING")
                print("=" * 50)
                print(f"Topic : {search_text}")
                print(f"Source: {article_url}")
                print()

                learned_result = study_engine.study(
                    search_text,
                    article_url
                )

                if learned_result.get(
                    "status"
                ) == "success":

                    # ------------------------------------------
                    # IMPORTANT:
                    # Use the exact topic we just saved.
                    # ------------------------------------------

                    fresh = learner.recall(
                        search_text
                    )

                    if fresh:

                        return self._normalize_learned(
                            search_text,
                            fresh
                        )

                    # Fallback to the processed result.

                    summary = learned_result.get(
                        "summary",
                        ""
                    )

                    if summary:

                        return {
                            "message": summary,
                            "topic": search_text,
                            "source": article_url,
                            "learned": True
                        }

        except Exception as error:

            try:

                from brain.memory import log

                log(
                    f"Automatic web learning error: {error}",
                    "warning"
                )

            except Exception:
                pass

        # ==================================================
        # 4. INTERNAL SEARCH FALLBACK
        # ==================================================

        if search_engine:

            try:

                results = search_engine.search(
                    question
                )

                if results:
                    return results

            except Exception:
                pass

        return {
            "message":
                "I haven't learned enough about that yet."
        }


    def think(self, question):
        """\n        Alias for answer().\n        """

        return self.answer(question)

    def learn_topic(self, topic, url):
        """\n        Learn from a website.\n        """

        try:

            from brain.study import study_engine

            return study_engine.study(
                topic,
                url
            )

        except Exception as e:

            return str(e)

    def remember_fact(self, key, value):
        """\n        Store a fact.\n        """

        memory.remember(
            key,
            value
        )

        return "Fact remembered."

    def recall_fact(self, key):
        """\n        Recall a stored fact.\n        """

        return memory.recall(
            key,
            "I don't remember that."
        )

    def compare(self, first, second):
        """\n        Compare two values.\n        """

        if first == second:
            return "They are the same."

        return "They are different."

    def status(self):
        """\n        Return Nitron brain status.\n        """

        learned = 0

        if learner:
            learned = len(
                learner.knowledge
            )

        return {
            "name": self.name,
            "knowledge_loaded": knowledge is not None,
            "learning_enabled": learner is not None,
            "search_enabled": search_engine is not None,
            "learned_topics": learned
        }


reasoning = ReasoningEngine()
