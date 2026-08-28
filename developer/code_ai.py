# ==========================================================
# NITRON CODE AI v4.0
# REAL AI CODE GENERATION
# ==========================================================

from developer.ai_code_generator import AICodeGenerator

from developer.code_engine.generator import ProjectGenerator
from developer.code_engine.fixer import CodeFixer

from developer.code_engine.website_generator import WebsiteGenerator
from developer.code_engine.webapp_generator import WebAppGenerator
from developer.code_engine.fullstack_generator import FullStackGenerator
from developer.code_engine.chatbot_generator import ChatbotGenerator
from developer.code_engine.api_generator import APIGenerator
from developer.code_engine.ai_generator import AIGenerator


class CodeAI:

    def __init__(self):

        # ==================================================
        # REAL AI CODE ENGINE
        # ==================================================

        self.ai_code = AICodeGenerator()

        # ==================================================
        # SPECIALIZED ENGINES
        # ==================================================

        self.generator = ProjectGenerator()
        self.fixer = CodeFixer()

        self.website = WebsiteGenerator()
        self.webapp = WebAppGenerator()
        self.fullstack = FullStackGenerator()
        self.chatbot = ChatbotGenerator()
        self.api = APIGenerator()
        self.ai = AIGenerator()

    # ======================================================
    # MAIN PROCESSOR
    # ======================================================

    def process(self, command):

        if not command:
            return "Please tell me what you want to build."

        command = command.strip()

        if not command:
            return "Please tell me what you want to build."

        text = command.lower()
        words = text.split()

        # ==================================================
        # HELP
        # ==================================================

        if text in (
            "developer",
            "code ai",
            "builder",
            "developer help",
            "coding help"
        ):
            return self.help()

        # ==================================================
        # CHECK PROJECT
        # ==================================================

        if text.startswith("check project"):

            parts = command.split(maxsplit=2)

            if len(parts) < 3:
                return "Please provide the project name."

            name = parts[2].strip()

            return self.fixer.scan(
                "GeneratedProjects/" + name
            )

        # ==================================================
        # TEST PROJECT
        # ==================================================

        if text.startswith("test project"):

            parts = command.split(maxsplit=2)

            if len(parts) < 3:
                return "Please provide the project name."

            name = parts[2].strip()

            return self.fixer.scan(
                "GeneratedProjects/" + name
            )

        # ==================================================
        # SPECIALIZED FULLSTACK BUILDER
        # ==================================================

        if (
            "fullstack" in words
            or "full-stack" in words
        ):

            # If the user gives a detailed request,
            # allow the real AI engine to handle it.

            if self.is_detailed_request(command):
                return self.ai_code.generate_code(
                    command
                )

            name = self.get_name(
                words,
                command.split(),
                "website",
                "FullStackProject"
            )

            return self.fullstack.create(name)

        # ==================================================
        # SPECIALIZED WEBSITE BUILDER
        # ==================================================

        if (
            text.startswith("create website")
            and not self.is_detailed_request(command)
        ):

            name = self.get_name(
                words,
                command.split(),
                "website",
                "NitronWebsite"
            )

            return self.website.create(name)

        # ==================================================
        # SPECIALIZED WEB APP BUILDER
        # ==================================================

        if (
            "web" in words
            and "app" in words
            and not self.is_detailed_request(command)
        ):

            name = self.get_name(
                words,
                command.split(),
                "app",
                "NitronWebApp"
            )

            return self.webapp.create(name)

        # ==================================================
        # SPECIALIZED CHATBOT BUILDER
        # ==================================================

        if (
            "chatbot" in words
            and not self.is_detailed_request(command)
        ):

            name = self.get_name(
                words,
                command.split(),
                "chatbot",
                "NitronChatbot"
            )

            return self.chatbot.create(name)

        # ==================================================
        # SPECIALIZED API BUILDER
        # ==================================================

        if (
            "api" in words
            and not self.is_detailed_request(command)
        ):

            name = self.get_name(
                words,
                command.split(),
                "api",
                "NitronAPI"
            )

            return self.api.create(name)

        # ==================================================
        # AI PROJECT
        # ==================================================

        if (
            "ai" in words
            and "create" in words
            and not self.is_detailed_request(command)
        ):

            name = self.get_name(
                words,
                command.split(),
                "ai",
                "NitronAI"
            )

            return self.ai.create(name)

        # ==================================================
        # EXPLICIT REAL CODE REQUEST
        # ==================================================

        if self.is_ai_generation_command(text):

            return self.ai_code.generate_code(
                command
            )

        # ==================================================
        # FRAMEWORK REQUESTS
        # ==================================================

        frameworks = (
            "react",
            "flutter",
            "django",
            "fastapi",
            "flask",
            "node",
            "typescript",
            "javascript",
            "python",
            "java",
            "c++",
            "cpp",
            "kotlin"
        )

        if any(
            framework in words
            for framework in frameworks
        ):

            return self.ai_code.generate_code(
                command
            )

        # ==================================================
        # GENERAL BUILD REQUEST
        # ==================================================

        build_words = (
            "build",
            "make",
            "develop",
            "program",
            "code",
            "create",
            "generate",
            "write"
        )

        if any(
            word in words
            for word in build_words
        ):

            return self.ai_code.generate_code(
                command
            )

        # ==================================================
        # UNKNOWN
        # ==================================================

        return (
            "I don't know how to build that yet.\n"
            "Say 'developer' to see my coding capabilities."
        )

    # ======================================================
    # AI GENERATION COMMAND DETECTION
    # ======================================================

    def is_ai_generation_command(
        self,
        text
    ):

        triggers = (

            "generate code",
            "generate a program",
            "generate an app",
            "generate a website",

            "write code",
            "write a program",
            "write an app",

            "create a python",
            "create a javascript",
            "create a java",
            "create a c++",
            "create a cpp",
            "create a calculator",

            "build a python",
            "build a javascript",
            "build a java",
            "build a program",
            "build an app",

            "make a python",
            "make a javascript",
            "make an app",
            "make a program"
        )

        return any(
            trigger in text
            for trigger in triggers
        )

    # ======================================================
    # DETECT DETAILED REQUEST
    # ======================================================

    def is_detailed_request(
        self,
        command
    ):

        words = command.lower().split()

        # Short commands such as:
        #
        # create website MySite
        #
        # should use the specialized builder.

        if len(words) <= 4:
            return False

        detail_words = (
            "with",
            "that",
            "which",
            "including",
            "using",
            "where",
            "allow",
            "allows",
            "support",
            "database",
            "login",
            "authentication",
            "payment",
            "dashboard",
            "search",
            "upload",
            "register",
            "users",
            "admin"
        )

        return any(
            word in words
            for word in detail_words
        )

    # ======================================================
    # GET PROJECT NAME
    # ======================================================

    def get_name(
        self,
        words,
        original_words,
        keyword,
        default
    ):

        try:

            index = words.index(
                keyword
            ) + 1

            if index < len(
                original_words
            ):

                return original_words[index]

        except Exception:

            pass

        return default

    # ======================================================
    # HELP
    # ======================================================

    def help(self):

        return """
============================================================
NITRON CODE AI v4.0
============================================================

REAL AI CODE GENERATION

Examples:

  create a Python calculator

  build a Python todo application

  write a Python program that organizes files

  create a JavaScript game

  build a FastAPI backend

  create a React dashboard

  create a chatbot with memory

  make a website with login and a database

  build a complete e-commerce application


SPECIALIZED BUILDERS

  create website MySite

  create fullstack website StoreAI

  create web app Dashboard

  create chatbot TutorBot

  create api ShopAPI

  create ai VisionAI


PROJECT TOOLS

  check project ProjectName

  test project ProjectName


FRAMEWORKS

  Python
  JavaScript
  TypeScript
  React
  Node
  FastAPI
  Flask
  Django
  Flutter
  Java
  C++
  Kotlin


NITRON PIPELINE

User request
     |
     v
CodeAI
     |
     v
AI Code Generator
     |
     v
AI Provider
     |
     v
JSON project
     |
     v
CodeGenerator
     |
     v
GeneratedProjects/


============================================================
"""

    # ======================================================
    # TEST
    # ======================================================

if __name__ == "__main__":

    code_ai = CodeAI()

    print(
        code_ai.help()
    )
