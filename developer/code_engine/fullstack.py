from developer.code_engine.generator import ProjectGenerator
from developer.code_engine.backend import BackendGenerator
from developer.code_engine.database import DatabaseGenerator


class FullStackGenerator:

    def __init__(self):

        self.website = ProjectGenerator()
        self.backend = BackendGenerator()
        self.database = DatabaseGenerator()


    def create(self, name):

        results = []

        results.append(
            self.website.website(name)
        )

        results.append(
            self.backend.create_api(
                name + "_backend"
            )
        )

        results.append(
            self.database.create_sqlite(
                name + "_database"
            )
        )


        return "\n".join(results)
