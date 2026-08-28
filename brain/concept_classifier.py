"""
Nitron Concept Classifier
"""


class ConceptClassifier:

    def __init__(self):

        self.categories = {

            "languages": {
                "python",
                "java",
                "javascript",
                "typescript",
                "c",
                "c++",
                "c#",
                "go",
                "rust",
                "php",
                "kotlin",
                "swift"
            },

            "frameworks": {
                "fastapi",
                "django",
                "flask",
                "starlette",
                "react",
                "vue",
                "angular",
                "laravel"
            },

            "libraries": {
                "pydantic",
                "numpy",
                "pandas",
                "requests",
                "beautifulsoup",
                "bs4",
                "matplotlib"
            },

            "standards": {
                "openapi",
                "json",
                "schema",
                "swagger",
                "http",
                "https",
                "rest"
            },

            "databases": {
                "sqlite",
                "mysql",
                "postgresql",
                "mongodb",
                "redis"
            },

            "tools": {
                "uvicorn",
                "git",
                "docker",
                "github",
                "linux",
                "termux"
            }

        }

    def classify(self, concepts):

        result = {}

        for category in self.categories:

            result[category] = []

        result["unknown"] = []

        for concept in concepts:

            found = False

            for category, values in self.categories.items():

                if concept.lower() in values:

                    result[category].append(concept)

                    found = True

                    break

            if not found:

                result["unknown"].append(concept)

        return result


classifier = ConceptClassifier()
