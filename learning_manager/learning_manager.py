"""
NITRON LEARNING MANAGER
Handles topics Nitron learns, stores, and later teaches.
"""

import json
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

# Keep the folder exactly where Nitron is already using it.
LEARNED_DIR = ROOT_DIR / "learned"
LEARNED_DIR.mkdir(parents=True, exist_ok=True)


class LearningManager:

    def __init__(self):
        self.pending_topic = None
        self.pending_request = None

    # ======================================================
    # SAFE NAME
    # ======================================================

    def safe_name(self, name):
        name = str(name).strip().lower()

        name = re.sub(
            r"[^a-z0-9_-]+",
            "_",
            name
        )

        name = re.sub(
            r"_+",
            "_",
            name
        )

        return name.strip("_") or "topic"

    # ======================================================
    # TOPIC FOLDER
    # ======================================================

    def topic_folder(self, topic):
        return LEARNED_DIR / self.safe_name(topic)

    # ======================================================
    # ASK USER FOR PERMISSION
    # ======================================================

    def request_learning(self, topic):

        topic = str(topic).strip()

        if not topic:
            return "What would you like me to learn?"

        self.pending_topic = topic
        self.pending_request = "learning"

        return (
            f"Sure, Boss. I can learn {topic}. "
            "Would you like me to write code and create a folder "
            "to save what I learn so I can teach it to you later?"
        )

    # ======================================================
    # USER ANSWER
    # ======================================================

    def answer_permission(self, answer):

        answer = str(answer).strip().lower()

        if self.pending_topic is None:
            return None

        topic = self.pending_topic

        yes_words = (
            "yes",
            "yeah",
            "yep",
            "sure",
            "okay",
            "ok",
            "do it",
            "create it",
            "save it",
            "go ahead"
        )

        no_words = (
            "no",
            "nope",
            "not now",
            "don't",
            "do not"
        )

        if answer in yes_words:

            result = self.start_learning(
                topic,
                save=True
            )

            self.pending_topic = None
            self.pending_request = None

            return result

        if answer in no_words:

            self.pending_topic = None
            self.pending_request = None

            return (
                f"Alright, Boss. I'll learn {topic} "
                "without creating a learning folder."
            )

        return (
            "Would you like me to create a folder and write "
            "code to save what I learn? Please say yes or no."
        )

    # ======================================================
    # START LEARNING
    # ======================================================

    def start_learning(self, topic, save=True):

        folder = self.topic_folder(topic)

        if save:

            folder.mkdir(
                parents=True,
                exist_ok=True
            )

            (folder / "lessons").mkdir(
                exist_ok=True
            )

            (folder / "code").mkdir(
                exist_ok=True
            )

            knowledge_file = folder / "knowledge.json"

            if not knowledge_file.exists():

                knowledge_file.write_text(
                    json.dumps(
                        {
                            "topic": topic,
                            "status": "learning",
                            "lessons": [],
                            "code": [],
                            "notes": []
                        },
                        indent=4
                    ),
                    encoding="utf-8"
                )

            readme = folder / "README.md"

            if not readme.exists():

                readme.write_text(
                    f"# Nitron Learning: {topic}\n\n"
                    f"This folder contains knowledge Nitron learned "
                    f"about {topic}.\n\n"
                    "Nitron can use this material later to teach "
                    "the topic.\n",
                    encoding="utf-8"
                )

            return (
                f"Yes, Boss. I'll learn {topic}, "
                "write useful code when appropriate, "
                "and save what I learn in:\n"
                f"{folder}"
            )

        return (
            f"Alright, Boss. I've started learning {topic}."
        )

    # ======================================================
    # SAVE KNOWLEDGE
    # ======================================================

    def save_knowledge(
        self,
        topic,
        title,
        explanation,
        code="",
        practice="",
        quiz=""
    ):

        folder = self.topic_folder(topic)

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        lessons_dir = folder / "lessons"
        code_dir = folder / "code"

        lessons_dir.mkdir(
            exist_ok=True
        )

        code_dir.mkdir(
            exist_ok=True
        )

        knowledge_file = folder / "knowledge.json"

        # --------------------------------------------------
        # LOAD EXISTING DATABASE
        # --------------------------------------------------

        if knowledge_file.exists():

            try:

                data = json.loads(
                    knowledge_file.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception:

                data = {}

        else:

            data = {}

        data.setdefault(
            "topic",
            topic
        )

        data.setdefault(
            "status",
            "learning"
        )

        data.setdefault(
            "lessons",
            []
        )

        data.setdefault(
            "code",
            []
        )

        data.setdefault(
            "notes",
            []
        )

        # --------------------------------------------------
        # DUPLICATE CHECK
        # --------------------------------------------------

        for existing in data["lessons"]:

            old_title = str(
                existing.get(
                    "title",
                    ""
                )
            ).strip().lower()

            old_explanation = str(
                existing.get(
                    "explanation",
                    ""
                )
            ).strip().lower()

            new_title = str(
                title
            ).strip().lower()

            new_explanation = str(
                explanation
            ).strip().lower()

            if (
                old_title == new_title
                and
                old_explanation == new_explanation
            ):

                return (
                    f"Lesson already saved for {topic}. "
                    "I will not create a duplicate."
                )

        # --------------------------------------------------
        # CREATE NEW LESSON
        # --------------------------------------------------

        lesson = {
            "title": title,
            "explanation": explanation,
            "practice": practice,
            "quiz": quiz
        }

        data["lessons"].append(
            lesson
        )

        lesson_number = len(
            data["lessons"]
        )

        lesson_file = (
            lessons_dir /
            f"lesson_{lesson_number}.json"
        )

        lesson_file.write_text(
            json.dumps(
                lesson,
                indent=4
            ),
            encoding="utf-8"
        )

        # --------------------------------------------------
        # SAVE CODE
        # --------------------------------------------------

        if code:

            code_file = (
                code_dir /
                f"example_{lesson_number}.py"
            )

            code_file.write_text(
                str(code),
                encoding="utf-8"
            )

            code_path = str(
                code_file
            )

            if code_path not in data["code"]:

                data["code"].append(
                    code_path
                )

        # --------------------------------------------------
        # SAVE DATABASE
        # --------------------------------------------------

        knowledge_file.write_text(
            json.dumps(
                data,
                indent=4
            ),
            encoding="utf-8"
        )

        return (
            f"Saved lesson {lesson_number} "
            f"for {topic}."
        )

    # ======================================================
    # CHECK LEARNED TOPIC
    # ======================================================

    def has_learned(self, topic):

        folder = self.topic_folder(topic)

        return (
            folder.exists()
            and
            (folder / "knowledge.json").exists()
        )

    # ======================================================
    # LIST LEARNED TOPICS
    # ======================================================

    def list_topics(self):

        if not LEARNED_DIR.exists():
            return []

        topics = []

        for item in LEARNED_DIR.iterdir():

            if item.is_dir():
                topics.append(
                    item.name
                )

        return sorted(topics)

    # ======================================================
    # READ KNOWLEDGE
    # ======================================================

    def get_knowledge(self, topic):

        file = (
            self.topic_folder(topic)
            / "knowledge.json"
        )

        if not file.exists():
            return None

        try:

            return json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return None


learning_manager = LearningManager()
