import os


class CodeFixer:

    def __init__(self):
        pass


    def scan(self, project):

        if not os.path.exists(project):
            return "Project not found."


        problems = []

        for root, dirs, files in os.walk(project):

            for file in files:

                path = os.path.join(root, file)


                try:

                    with open(
                        path,
                        "r",
                        errors="ignore"
                    ) as f:

                        code = f.read()


                    if file.endswith(".py"):

                        if "print(" in code and code.count("(") != code.count(")"):
                            problems.append(
                                f"Possible bracket error: {path}"
                            )


                    if file.endswith(".html"):

                        if "<html>" not in code:
                            problems.append(
                                f"HTML structure issue: {path}"
                            )


                except Exception as e:

                    problems.append(
                        str(e)
                    )


        if problems:

            return "\n".join(problems)


        return "No problems found."


    def repair_message(self):

        return (
            "Nitron checked the project. "
            "Automatic repair engine ready."
        )
