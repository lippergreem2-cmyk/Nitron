# ==========================================================
# NITRON MEMORY SYSTEM v2.0
# Long term memory for Brain
# ==========================================================

import os
import json


MEMORY_FILE = os.path.expanduser(
    "~/Nitron/memory.json"
)


class Memory:


    def __init__(self):

        self.data = {}

        self.load()



    def load(self):

        try:

            if os.path.exists(MEMORY_FILE):

                with open(
                    MEMORY_FILE,
                    "r"
                ) as file:

                    self.data = json.load(file)


        except Exception:

            self.data = {}



    def save(self):

        try:

            with open(
                MEMORY_FILE,
                "w"
            ) as file:

                json.dump(
                    self.data,
                    file,
                    indent=4
                )


        except Exception as error:

            print(
                "Memory save error:",
                error
            )



    def remember(
        self,
        key,
        value
    ):

        self.data[key] = value

        self.save()

        return True



    def recall(
        self,
        key,
        default=None
    ):

        return self.data.get(
            key,
            default
        )



    def forget(
        self,
        key
    ):

        if key in self.data:

            del self.data[key]

            self.save()

            return True


        return False



    def show(self):

        return self.data




memory = Memory()
