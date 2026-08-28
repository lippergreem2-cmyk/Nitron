# ==========================================================
# NITRON BUILDER MANAGER v8.0
# Controls all Nitron project builders
# ==========================================================


from .python_builder import PythonBuilder
from .developer import Developer
from .game_builder import GameBuilder
from .automation_builder import AutomationBuilder
from .assistant_builder import AssistantBuilder
from .machine_learning_builder import MachineLearningBuilder
from .deep_learning_builder import DeepLearningBuilder
from .computer_vision_builder import ComputerVisionBuilder
from .nlp_builder import NLPBuilder
from .robotics_builder import RoboticsBuilder
from .blockchain_builder import BlockchainBuilder
from .data_science_builder import DataScienceBuilder
from .cloud_builder import CloudBuilder
from .operating_system_builder import OperatingSystemBuilder
from .project_generator import ProjectGenerator
from .package_builder import PackageBuilder



class BuilderManager:


    def __init__(self):

        self.python = PythonBuilder()

        self.developer = Developer()

        self.games = GameBuilder()

        self.automation = AutomationBuilder()

        self.assistant = AssistantBuilder()

        self.ml = MachineLearningBuilder()

        self.deep = DeepLearningBuilder()

        self.cv = ComputerVisionBuilder()

        self.nlp = NLPBuilder()

        self.robotics = RoboticsBuilder()

        self.blockchain = BlockchainBuilder()

        self.data = DataScienceBuilder()

        self.cloud = CloudBuilder()

        self.os = OperatingSystemBuilder()

        self.projects = ProjectGenerator()

        self.package = PackageBuilder()



    def builders(self):

        return {

            "python": self.python,

            "developer": self.developer,

            "games": self.games,

            "automation": self.automation,

            "assistant": self.assistant,

            "machine_learning": self.ml,

            "deep_learning": self.deep,

            "computer_vision": self.cv,

            "nlp": self.nlp,

            "robotics": self.robotics,

            "blockchain": self.blockchain,

            "data_science": self.data,

            "cloud": self.cloud,

            "operating_system": self.os,

            "projects": self.projects,

            "package": self.package

        }



    def list_builders(self):

        return sorted(
            self.builders().keys()
        )



    def has_builder(self, name):

        return name in self.builders()



    def get_builder(self, name):

        return self.builders().get(name)



    # ======================================================
    # COMMAND HANDLER
    # ======================================================

    def handle(self, command):

        command = command.lower().strip()



        # Python projects

        if command.startswith(
            "create python project"
        ):

            name = command.replace(
                "create python project",
                "",
                1
            ).strip()


            if not name:

                name = "new_project"


            return self.python.create_program(
                name
            )



        # Games

        if "snake game" in command:

            if hasattr(
                self.games,
                "snake"
            ):

                return self.games.snake()



        if "racing game" in command:

            if hasattr(
                self.games,
                "racing"
            ):

                return self.games.racing()



        # AI assistant projects

        if "assistant" in command:

            if hasattr(
                self.assistant,
                "create"
            ):

                return self.assistant.create(
                    command
                )



        # Machine learning

        if "machine learning" in command:

            if hasattr(
                self.ml,
                "create"
            ):

                return self.ml.create(
                    command
                )



        return None





if __name__ == "__main__":


    manager = BuilderManager()


    print(
        "Nitron Builder Manager v8.0"
    )


    print(
        "---------------------------"
    )


    for item in manager.list_builders():

        print(
            item
        )
