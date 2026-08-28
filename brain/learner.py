"""
Nitron Learner
"""

import json
import os
from datetime import datetime

try:
    from brain.knowledge_formatter import formatter
except ImportError:
    from knowledge_formatter import formatter


class Learner:

    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(__file__),
            "learned_knowledge.json"
        )

        self.knowledge = self.load()

    def load(self):

        if not os.path.exists(self.file):
            return {}

        try:
            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)

        except Exception:
            return {}

    def save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.knowledge,
                f,
                indent=4,
                ensure_ascii=False
            )

    def learn(self, topic, source, content):

        topic = topic.strip().lower()

        if isinstance(content, dict):

            entry = formatter.format(
                topic,
                source,
                content
            )

        else:

            entry = {
                "topic": topic,
                "title": topic.title(),
                "source": source,
                "date": str(datetime.now()),
                "summary": str(content),
                "keywords": [],
                "sections": {},
                "examples": [],
                "related_topics": [],
                "notes": [],
                "confidence": 1.0
            }

        self.knowledge[topic] = entry

        self.save()

        return entry

    def learn_image(self, image_result, source="image"):
        """
        Learn structured, sanitized information from an image analysis.

        Raw OCR is never stored. Potential passwords, credentials,
        tokens, and other sensitive text are excluded.
        """

        if not isinstance(image_result, dict):
            raise ValueError("image_result must be a dictionary.")

        topics = image_result.get("topics", [])

        if not topics:
            topics = [{"topic": "image_analysis"}]

        topic_names = [
            str(item.get("topic", "")).strip().lower()
            for item in topics
            if isinstance(item, dict) and item.get("topic")
        ]

        topic_names = list(dict.fromkeys(topic_names))

        # ------------------------------------------------------
        # SAFE IMAGE METADATA
        # ------------------------------------------------------

        metadata = {
            "width": image_result.get("width"),
            "height": image_result.get("height"),
            "format": image_result.get("format"),
            "mode": image_result.get("mode"),
        }

        # ------------------------------------------------------
        # SAFE VISION INFORMATION
        # ------------------------------------------------------

        vision = image_result.get("vision", {})

        safe_vision = {
            "success": bool(
                isinstance(vision, dict)
                and vision.get("success")
            ),
            "model": (
                str(vision.get("model", ""))
                if isinstance(vision, dict)
                else ""
            ),
        }

        if isinstance(vision, dict) and vision.get("success"):
            safe_vision["analysis"] = str(
                vision.get("analysis", "")
            ).strip()

        elif isinstance(vision, dict):
            safe_vision["error_type"] = str(
                vision.get("error_type", "unavailable")
            )

        # ------------------------------------------------------
        # SAFE PUBLIC RESEARCH REFERENCES
        # ------------------------------------------------------

        safe_research = image_result.get("research", {})
        research_items = []

        if isinstance(safe_research, dict):

            for item in safe_research.get("results", [])[:5]:

                if not isinstance(item, dict):
                    continue

                title = str(
                    item.get("title", "")
                ).strip()

                url = str(
                    item.get("url", "")
                ).strip()

                if title and url:
                    research_items.append({
                        "title": title,
                        "url": url,
                    })

        # ------------------------------------------------------
        # BUILD A USEFUL SAFE SUMMARY
        # ------------------------------------------------------

        summary_parts = []

        if topic_names:
            summary_parts.append(
                "The image was classified as involving "
                + ", ".join(topic_names)
                + "."
            )

        if safe_vision.get("success"):
            analysis = safe_vision.get("analysis", "")

            if analysis:
                # Keep the learned vision description bounded.
                summary_parts.append(
                    "Vision analysis: "
                    + analysis[:1200]
                )

        else:
            summary_parts.append(
                "Detailed vision analysis was unavailable."
            )

        if research_items:
            research_titles = [
                item["title"]
                for item in research_items
            ]

            summary_parts.append(
                "Related public research included: "
                + "; ".join(research_titles)
                + "."
            )

        summary = " ".join(summary_parts).strip()

        if not summary:
            summary = (
                "Image analyzed. Detected topics: "
                + ", ".join(topic_names)
                + "."
            )

        # ------------------------------------------------------
        # STRUCTURED LEARNED DATA
        # ------------------------------------------------------

        safe_data = {
            "title": (
                "Image analysis: "
                + str(
                    image_result.get(
                        "filename",
                        "image"
                    )
                )
            ),

            "summary": summary,

            "sections": {
                "image_metadata": metadata,

                "topics": topic_names,

                "vision": safe_vision,

                "research": {
                    "query": str(
                        safe_research.get(
                            "query",
                            ""
                        )
                    ),
                    "results": research_items,
                },
            },

            "related_topics": topic_names,

            "confidence": (
                1.0
                if safe_vision["success"]
                else 0.7
            ),
        }

        # ------------------------------------------------------
        # SAVE UNDER EACH DETECTED TOPIC
        # ------------------------------------------------------

        learned = []

        for topic in topic_names:

            entry = self.learn(
                topic,
                source,
                safe_data,
            )

            learned.append(entry)

        return learned

    def recall(self, topic):

        topic = topic.strip().lower()

        return self.knowledge.get(
            topic,
            None
        )

    def topics(self):

        return sorted(
            self.knowledge.keys()
        )

    def exists(self, topic):

        topic = topic.strip().lower()

        return topic in self.knowledge

    def remove(self, topic):

        topic = topic.strip().lower()

        if topic in self.knowledge:

            del self.knowledge[topic]

            self.save()

            return True

        return False


learner = Learner()


# ============================================================
# NITRON CAPABILITY CLASSIFICATION
# ============================================================

def classify_capability(topic, description=""):
    """
    Determine what kind of capability Nitron learned.

    This is intentionally generic. The learned name and
    description are used to classify the capability instead
    of hard-coding individual languages or technologies.
    """

    text = (
        str(topic) + " " + str(description)
    ).lower()

    # Human languages
    language_terms = [
        "human language",
        "spoken language",
        "natural language",
        "language",
        "idiom",
    ]

    if any(term in text for term in language_terms):
        programming_terms = [
            "programming language",
            "programming",
            "code",
            "software",
        ]

        if not any(
            term in text
            for term in programming_terms
        ):
            return "language"

    # Programming / coding
    programming_terms = [
        "programming",
        "programming language",
        "program",
        "coding",
        "code",
        "software development",
        "scripting",
    ]

    if any(term in text for term in programming_terms):
        return "programming"

    # Frameworks / libraries / platforms
    framework_terms = [
        "framework",
        "library",
        "sdk",
        "api",
        "platform",
        "toolkit",
    ]

    if any(term in text for term in framework_terms):
        return "framework"

    # Web technologies
    web_terms = [
        "html",
        "css",
        "javascript",
        "web development",
        "website",
        "web application",
    ]

    if any(term in text for term in web_terms):
        return "web"

    return "knowledge"


def capability_handler_for(capability_type):
    """
    Return the generic handler appropriate for a capability type.
    """

    handlers = {
        "language": "learned.language",
        "programming": "learned.programming",
        "framework": "learned.framework",
        "web": "learned.programming",
        "knowledge": "learned.knowledge",
    }

    return handlers.get(
        capability_type,
        "learned.knowledge"
    )


def capability_abilities(topic, capability_type):
    """
    Generate abilities appropriate to the learned capability.
    """

    topic = str(topic).strip()

    if capability_type == "language":
        return [
            f"understand {topic}",
            f"read {topic}",
            f"write {topic}",
            f"translate {topic}",
            f"answer in {topic}",
            f"converse in {topic}",
            f"speak {topic}",
        ]

    if capability_type == "programming":
        return [
            f"understand {topic}",
            f"write {topic}",
            f"create using {topic}",
            f"build using {topic}",
            f"modify {topic}",
            f"debug {topic}",
            f"test {topic}",
            f"analyze {topic}",
            f"explain {topic}",
        ]

    if capability_type == "framework":
        return [
            f"understand {topic}",
            f"use {topic}",
            f"build with {topic}",
            f"configure {topic}",
            f"integrate {topic}",
            f"modify {topic}",
            f"debug {topic}",
            f"test {topic}",
            f"explain {topic}",
        ]

    if capability_type == "web":
        return [
            f"understand {topic}",
            f"write {topic}",
            f"create {topic}",
            f"build using {topic}",
            f"modify {topic}",
            f"debug {topic}",
            f"test {topic}",
            f"validate {topic}",
        ]

    return [
        f"understand {topic}",
        f"explain {topic}",
        f"answer questions about {topic}",
        f"apply {topic}",
        f"analyze {topic}",
        f"work with {topic}",
    ]


# ============================================================
# NITRON CAPABILITY LEARNING
# ============================================================

def learn_capability(
    topic,
    description="",
    abilities=None,
    evidence=None,
    capability_type="knowledge",
    handlers=None,
    input_schema=None
):
    """
    Learn a topic and register it as a usable Nitron capability.
    """
    try:
        from brain.skill_registry import learn_skill

        return learn_skill(
            name=topic,
            description=description,
            abilities=abilities or [],
            evidence=evidence or [],
            handlers=handlers or [],
            capability_type=capability_type,
            input_schema=input_schema
        )
    except Exception as e:
        print(f"[Capability] Could not register skill: {e}")
        return None

# ============================================================
# CAPABILITY TYPE DETECTION
# ============================================================

LANGUAGE_NAMES = {
    "english",
    "spanish",
    "french",
    "german",
    "italian",
    "portuguese",
    "arabic",
    "swahili",
    "kiswahili",
    "chinese",
    "mandarin",
    "japanese",
    "korean",
    "hindi",
    "russian",
    "turkish",
    "dutch",
    "greek",
}

def detect_capability_type(topic, description=""):
    """
    Determine the broad capability category of learned knowledge.

    Classification is generic and based on the topic plus its
    description. Unknown subjects intentionally fall back to
    "knowledge".
    """

    text = (
        str(topic) + " " + str(description)
    ).strip().lower()

    normalized = str(topic).strip().lower()

    # ----------------------------------------------------------
    # HUMAN LANGUAGES
    # ----------------------------------------------------------

    if normalized in LANGUAGE_NAMES:
        return "language"

    language_markers = [
        "human language",
        "spoken language",
        "natural language",
        "translation language",
        "language used for communication",
    ]

    programming_markers = [
        "programming language",
        "programming",
        "software development",
        "source code",
        "coding",
        "scripting",
    ]

    if any(marker in text for marker in language_markers):
        if not any(
            marker in text
            for marker in programming_markers
        ):
            return "language"

    # ----------------------------------------------------------
    # PROGRAMMING
    # ----------------------------------------------------------

    programming_terms = [
        "programming language",
        "programming",
        "program",
        "coding",
        "code",
        "software development",
        "software engineering",
        "scripting",
    ]

    if any(term in text for term in programming_terms):
        return "programming"

    # Common programming-language names are also recognized
    # when the description is short or generic.

    programming_languages = {
        "python",
        "javascript",
        "typescript",
        "java",
        "kotlin",
        "c",
        "c++",
        "c#",
        "rust",
        "go",
        "golang",
        "swift",
        "ruby",
        "php",
        "perl",
        "lua",
        "dart",
        "scala",
        "r",
        "bash",
        "shell",
        "powershell",
    }

    if normalized in programming_languages:
        return "programming"

    # ----------------------------------------------------------
    # FRAMEWORKS / LIBRARIES / SDKs / APIs
    # ----------------------------------------------------------

    framework_terms = [
        "framework",
        "library",
        "sdk",
        "api",
        "toolkit",
        "runtime",
    ]

    if any(term in text for term in framework_terms):
        return "framework"

    known_frameworks = {
        "fastapi",
        "django",
        "flask",
        "react",
        "react native",
        "vue",
        "angular",
        "svelte",
        "spring",
        "spring boot",
        "express",
        "next.js",
        "nextjs",
        "tensorflow",
        "pytorch",
    }

    if normalized in known_frameworks:
        return "framework"

    # ----------------------------------------------------------
    # WEB TECHNOLOGIES
    # ----------------------------------------------------------

    web_terms = [
        "html",
        "css",
        "javascript",
        "web development",
        "website",
        "web application",
        "web app",
        "frontend",
        "front-end",
        "backend",
        "back-end",
    ]

    if any(term in text for term in web_terms):
        return "web"

    # ----------------------------------------------------------
    # EVERYTHING ELSE
    # ----------------------------------------------------------
    #
    # Astronomy, physics, mathematics, history, chess, music,
    # networking, geography, etc. all become general knowledge
    # capabilities without needing hard-coded subject lists.
    # ----------------------------------------------------------

    return "knowledge"


# ============================================================
# NITRON UNIVERSAL CAPABILITY LEARNING
# ============================================================

def learn_and_register(
    topic,
    description="",
    abilities=None,
    evidence=None
):
    """
    Universal Nitron learning entry point.

    Learned information becomes a typed capability with an
    appropriate generic execution handler.
    """

    topic = str(topic).strip()

    if not topic:
        return None

    # ------------------------------------------------------
    # CLASSIFY CAPABILITY
    # ------------------------------------------------------

    capability_type = detect_capability_type(
        topic,
        description
    )

    handler = capability_handler_for(
        capability_type
    )

    # ------------------------------------------------------
    # STORE KNOWLEDGE
    # ------------------------------------------------------

    knowledge_result = None

    try:

        knowledge_result = learner.learn(
            topic,
            source="nitron_learning",
            content=description or (
                f"Learned knowledge about {topic}."
            )
        )

    except Exception as e:

        print(
            f"[Learner] Knowledge learning warning: {e}"
        )

    # ------------------------------------------------------
    # BUILD TYPE-SPECIFIC ABILITIES
    # ------------------------------------------------------

    default_abilities = capability_abilities(
        topic,
        capability_type
    )

    combined_abilities = list(
        dict.fromkeys(
            default_abilities
            + (abilities or [])
        )
    )

    # ------------------------------------------------------
    # REGISTER CAPABILITY
    # ------------------------------------------------------

    try:

        from brain.skill_registry import learn_skill

        capability_result = learn_skill(
            name=topic,
            description=description,
            abilities=combined_abilities,
            evidence=evidence or [
                "Nitron learning system"
            ],
            handlers=[handler]
        )

        # --------------------------------------------------
        # UPDATE CAPABILITY METADATA
        # --------------------------------------------------

        from brain.skill_registry import (
            _load,
            _save,
            normalize
        )

        skills = _load()

        key = normalize(topic)

        if key in skills:

            skills[key]["capability_type"] = (
                capability_type
            )

            skills[key]["input_schema"] = {}

            skills[key]["handlers"] = list(
                dict.fromkeys(
                    skills[key].get(
                        "handlers",
                        []
                    )
                    + [handler]
                )
            )

            _save(skills)

            capability_result = skills[key]

    except Exception as e:

        print(
            f"[Capability] Registration warning: {e}"
        )

        capability_result = None

    return {
        "topic": topic,
        "knowledge": knowledge_result,
        "capability": capability_result,
        "capability_type": capability_type,
        "handler": handler,
        "abilities": combined_abilities,
        "status": "learned"
    }


def capability_status(topic):
    try:
        from brain.skill_registry import get_skill
        return get_skill(topic)
    except Exception:
        return None
